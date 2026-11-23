#!/usr/bin/env python3
"""Litmus "Tuesday Outage" investigation tool (stdlib only).

Usage: python3 solve.py <pack_dir> [--write <out_dir>]
Prints exactly one JSON object (root_causes, causal_graph, fix_set) to stdout.
With --write also writes root_causes.csv / causal_graph.json / fix_set.json.

Method: compare each trace signature after the Kestrel release window
(Tue 2026-09-15 02:00Z) against the Monday baseline. A cause is claimed only
when a Litmus span shows the symptom acting (changelog entries alone never count).
"""
import csv
import io
import json
import os
import sys
from collections import defaultdict

WINDOW = "2026-09-15T02:00:00"


def load(pack):
    with open(os.path.join(pack, "traces.jsonl")) as f:
        return [json.loads(l) for l in f if l.strip()]


def post(s):
    return s["start"] >= WINDOW


def onset(s):
    return s["start"][:19] + "Z"


def first(spans):
    return min(spans, key=lambda s: s["start"]) if spans else None


def A(s):
    return s.get("attrs") or {}


def detect(S):
    causes, fixes, edges = [], [], []
    lit = [s for s in S if s["component"] != "external"]

    def claim(code, comp, span, at=None):
        causes.append({"cause_code": code, "component": comp,
                       "onset_time": at or onset(span), "evidence_span_id": span["span_id"]})

    # --- connector field renamed: structured LitIndex queries suddenly empty ---
    sq = [s for s in lit if s["name"] == "litindex.query" and A(s).get("query_mode") == "structured"]
    base = [s for s in sq if not post(s)]
    after = [s for s in sq if post(s)]
    if base and after:
        b = sum(A(s).get("result_count", 0) == 0 for s in base) / len(base)
        a = sum(A(s).get("result_count", 0) == 0 for s in after) / len(after)
        zero = [s for s in after if A(s).get("result_count", 0) == 0 and A(s).get("bytes_received", 0) > 0]
        if a > b + 0.4 and zero:
            claim("CONNECTOR_FIELD_RENAMED", "search", first(zero))
            fixes.append({"op": "set_result_field", "component": "search", "field": "items",
                          "note": "LitIndex v4 returns results in `items`; Search parsed `results` -> 0 results -> fallback index"})
            edges += [["CONNECTOR_FIELD_RENAMED", "EMPTY_PRIMARY_RESULTS"],
                      ["EMPTY_PRIMARY_RESULTS", "FALLBACK_INDEX_USED"],
                      ["FALLBACK_INDEX_USED", "THIN_REVIEWS"]]

    # --- tool result limit lowered: fetch_paper payload pinned at exactly 24 KB ---
    cut = [s for s in lit if s["name"] == "fetch_paper" and post(s) and s["status"] == "ok"
           and A(s).get("bytes_received") == 24576 and not A(s).get("chunk")]
    pre_big = [s for s in lit if s["name"] == "fetch_paper" and not post(s) and A(s).get("bytes_received", 0) > 24576]
    dec = [s for s in lit if s.get("error_type") == "json_decode_error"]
    if cut and dec:
        claim("TOOL_RESULT_LIMIT_LOWERED", "extract", first(cut))
        fixes.append({"op": "set_result_chunking", "component": "extract", "enabled": True,
                      "note": "cap is a platform limit (cannot be raised); chunking delivers papers in <=24KB parts"})
        edges += [["TOOL_RESULT_LIMIT_LOWERED", "TRUNCATED_TOOL_RESULT"],
                  ["TRUNCATED_TOOL_RESULT", "PARTIAL_EXTRACTION"]]

    # --- model alias drift -> orchestrator tool-arg parse errors ---
    pe = [s for s in lit if s.get("error_type") == "tool_args_parse_error"]
    if pe:
        # onset = first orchestrator call served by the new snapshot (vendor: alias moved at 02:00, no phasing);
        # parse errors only surface later because early overnight traffic is tiny. Evidence = first parse error.
        base_models = {s.get("model_resolved") for s in lit if s["component"] == "orchestrator"
                       and s["kind"] == "llm_call" and not post(s)}
        drift = [s for s in lit if s["component"] == "orchestrator" and s["kind"] == "llm_call" and post(s)
                 and s.get("model_resolved") not in base_models]
        claim("MODEL_ALIAS_DRIFT", "orchestrator", first(pe), onset(first(drift)) if drift else None)
        fixes.append({"op": "set_tool_arg_parsing", "component": "orchestrator", "mode": "object",
                      "note": "kp-2026-08 (new alias target) returns tool args as objects; parser expects JSON string"})
        edges += [["MODEL_ALIAS_DRIFT", "ARG_PARSE_ERRORS"], ["ARG_PARSE_ERRORS", "JOB_FAILURES"]]

    # --- reasoning default changed: reasoning tokens appear where there were none ---
    for comp in ("synthesize", "orchestrator"):
        calls = [s for s in lit if s["component"] == comp and s["kind"] == "llm_call"]
        b = [s["tokens"]["reasoning"] for s in calls if not post(s)]
        a = [s for s in calls if post(s) and s["tokens"]["reasoning"] > 0]
        if b and sum(b) / len(b) < 1 and a:
            claim("REASONING_DEFAULT_CHANGED", comp, first(a))
            fixes.append({"op": "set_reasoning", "component": comp, "mode": "off",
                          "note": "alias default became medium; Monday baseline was off"})
            edges += [["REASONING_DEFAULT_CHANGED", "REASONING_TOKENS"], ["REASONING_TOKENS", "COST_SPIKE"]]
            break

    # --- concurrency cap reduced: platform queue timeouts ---
    qt = [s for s in lit if s.get("error_type") == "queue_timeout"]
    if qt:
        inflight = max((A(s).get("account_in_flight") or 0) for s in qt)
        # vendor: cap applied from the 02:00 window; first 504 needs >8 in flight, which needs daytime load
        claim("CONCURRENCY_CAP_REDUCED", "extract", first(qt), WINDOW + "Z")
        fixes.append({"op": "set_max_concurrency", "component": "orchestrator", "n": inflight or 8,
                      "note": "keep Litmus in-flight requests at the new per-key cap"})
        edges += [["CONCURRENCY_CAP_REDUCED", "QUEUE_TIMEOUTS"], ["QUEUE_TIMEOUTS", "STAGE_REDISPATCH"],
                  ["STAGE_REDISPATCH", "JOB_FAILURES"], ["STAGE_REDISPATCH", "LATENCY_INCREASE"]]

    # --- rate tier downgrade: 429s on Litmus traffic ---
    rl = [s for s in lit if s.get("http_status") == 429]
    if rl:
        claim("RATE_TIER_DOWNGRADE", rl[0]["component"], first(rl))
        fixes.append({"op": "set_retry_policy", "component": "orchestrator", "policy": "exp_backoff_jitter"})
        edges += [["RATE_TIER_DOWNGRADE", "RATE_LIMIT_REJECTIONS"]]

    # --- tool schema strictness ---
    ts = [s for s in lit if s.get("error_type") == "tool_schema_validation_error"]
    if ts:
        claim("TOOL_SCHEMA_STRICTNESS", "cite_check", first(ts))
        fixes.append({"op": "update_tool_schema", "component": "cite_check", "additional_properties": True})
        edges += [["TOOL_SCHEMA_STRICTNESS", "SCHEMA_REJECTIONS"], ["SCHEMA_REJECTIONS", "JOB_FAILURES"]]

    # --- output token default lowered ---
    ln = [s for s in lit if s["kind"] == "llm_call" and s.get("finish_reason") == "length" and post(s)]
    if ln:
        claim("OUTPUT_TOKEN_DEFAULT_LOWERED", ln[0]["component"], first(ln))
        fixes.append({"op": "set_max_output_tokens", "component": "synthesize", "n": 16000})
        edges += [["OUTPUT_TOKEN_DEFAULT_LOWERED", "OUTPUT_LENGTH_LIMIT_HIT"],
                  ["OUTPUT_LENGTH_LIMIT_HIT", "TRUNCATED_REVIEWS"]]

    # --- citeregistry pagination: more pages exist but were not fetched / under-verified ---
    cr = [s for s in lit if s["name"] == "citeregistry.lookup" and post(s) and A(s).get("has_more")]
    unfollowed = []
    byparent = defaultdict(list)
    for s in lit:
        if s["name"] == "citeregistry.lookup":
            byparent[s["parent_id"]].append(s)
    for s in cr:
        if not any(A(x).get("cursor_followed") for x in byparent[s["parent_id"]]):
            unfollowed.append(s)
    under = [s for s in lit if s["name"] == "verify_citations"
             and A(s).get("citations_checked", 0) < A(s).get("citations_total", 0)]
    if unfollowed or under:
        claim("CONNECTOR_PAGINATION_CHANGED", "cite_check", first(unfollowed or under))
        fixes.append({"op": "set_follow_cursor", "component": "cite_check", "enabled": True})
        edges += [["CONNECTOR_PAGINATION_CHANGED", "PARTIAL_CITATION_SET"],
                  ["PARTIAL_CITATION_SET", "UNDER_VERIFIED_CITATIONS"]]

    # --- not claimed here (no trace evidence in a Litmus span): CACHE_TTL (misses match explicit TTLs),
    # BATCH, REGION, CLOCK_SKEW (no child-before-parent), CREDENTIAL_MISUSE (external traffic never hit
    # Litmus spans), EMBEDDING_INDEX_STALE (fallback age constant, also used on Monday) ---
    seen, uniq = set(), []
    for e in edges:
        if tuple(e) not in seen:
            seen.add(tuple(e)); uniq.append(e)
    return causes, uniq, fixes


def main():
    pack = sys.argv[1]
    S = load(pack)
    causes, edges, fixes = detect(S)
    out = {"root_causes": causes, "causal_graph": {"edges": edges}, "fix_set": {"operations": fixes}}
    if "--write" in sys.argv:
        d = sys.argv[sys.argv.index("--write") + 1]
        os.makedirs(d, exist_ok=True)
        buf = io.StringIO()
        w = csv.DictWriter(buf, ["cause_code", "component", "onset_time", "evidence_span_id"], lineterminator="\n")
        w.writeheader(); w.writerows(causes)
        open(os.path.join(d, "root_causes.csv"), "w").write(buf.getvalue())
        json.dump(out["causal_graph"], open(os.path.join(d, "causal_graph.json"), "w"), indent=1)
        json.dump(out["fix_set"], open(os.path.join(d, "fix_set.json"), "w"), indent=1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
