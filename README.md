# Litmus "Tuesday Outage" - Incident Investigation (variant v04)

Investigation tool and deliverables for the Litmus incident on the (fictional) Kestrel AI Platform,
produced for the Claude Olympics challenge.

## Findings in brief
Five root causes, all starting at the Tue 15 Sep 2026 02:00 UTC Kestrel release window:

| Cause code | Component | What happened |
|---|---|---|
| `CONNECTOR_FIELD_RENAMED` | search | LitIndex v4 returns results in `items`; Search read `results`, got 0 results and fell back to the stale index (thin reviews). |
| `TOOL_RESULT_LIMIT_LOWERED` | extract | Tool-result cap fell 64 KB to 24 KB; papers were cut off, causing decode errors and partial extraction. |
| `REASONING_DEFAULT_CHANGED` | synthesize | Reasoning left unset; the alias default became `medium` (about 16k extra tokens per review, cost up). |
| `MODEL_ALIAS_DRIFT` | orchestrator | `kestrel-pro-latest` moved to a snapshot that returns tool args as objects; the parser expects strings, so plans failed. |
| `CONCURRENCY_CAP_REDUCED` | extract | Per-key cap fell 20 to 8; requests queued past 30 s and returned 504, triggering stage re-dispatch. |

Ruled out (with evidence in `APPROACH_SUMMARY.md`): credential misuse (scheduled re-index), stale fallback
index, rate tier, schema strictness, pagination, output-token default, cache TTL, batch API, region, clock skew.

## Fix (replay-verified, minimal)
`submission/fix_set.json`: `set_result_field`, `set_result_chunking`, `set_tool_arg_parsing`,
`set_reasoning`, `set_max_concurrency`. Staging replay: 0 hard failures, 0 degraded outputs, cost per job
1.05x Monday. Removing any tested operation brought a failure back (see ablation table in `APPROACH_SUMMARY.md`).

## Repository layout
| Path | Purpose |
|---|---|
| `solve.py` | Entry point. `python3 solve.py <pack_dir>` prints one JSON object (`root_causes`, `causal_graph`, `fix_set`). Stdlib only. |
| `litmus_config.json`, `requirements.txt`, `Dockerfile` | Submission contract files (no third-party dependencies). |
| `pack/` | Incident evidence pack for variant v04 (traces, config, deploy log, alerts, chat, docs, vocabularies). |
| `submission/` | `root_causes.csv`, `causal_graph.json`, `fix_set.json` generated from `pack/`. |
| `APPROACH_SUMMARY.md` | Evidence, ruled-out candidates, fix justification, tooling and uncertainty. |

## Usage
```bash
python3 solve.py pack                      # JSON to stdout
python3 solve.py pack --write submission   # also (re)write the three deliverable files
```
`solve.py` compares each trace signature after the release window with the Monday baseline and claims a
cause only when a Litmus span shows it acting. It is written to generalise across variants.

## Notes
- All product, company and platform names in the data are fictional.
- No credentials or tokens are stored in this repository.
