# Kestrel AI Platform — Documentation (excerpt, current as of 15 Sep 2026)

Kestrel is the hosted model and agent platform Litmus runs on. This excerpt covers the features
Litmus uses or could use. Where Kestrel behaves differently from other platforms you know, this
documentation is authoritative.

## 1. Models, snapshots and aliases

A **snapshot** is a fixed model version. An **alias** points to a snapshot chosen by Kestrel.

| Name | Type | Status | Tool-call argument encoding |
|---|---|---|---|
| `kp-2025-11` | snapshot | **Retired** at the 15 Sep 02:00 UTC release window. Requests fail. | JSON-encoded string |
| `kp-2026-02` | snapshot | Supported until 31 Dec 2026 | JSON-encoded string |
| `kp-2026-08` | snapshot | Released at the 15 Sep 02:00 UTC release window | JSON object |
| `kestrel-pro-latest` | alias | Moves to the newest snapshot at each release window. Since 15 Sep 02:00 UTC: `kp-2026-08` (previously `kp-2026-02`). | Follows the snapshot |

Every model-call trace records both `model_requested` (what the client asked for) and
`model_resolved` (the snapshot that served it).

**Tool-call argument encoding.** Snapshots `kp-2026-08` and later return tool-call `arguments` as a
JSON object. Earlier snapshots return them as a JSON-encoded string. Clients must parse the encoding
their snapshot uses. Clients that call through an alias receive whichever encoding the current
snapshot uses.

## 2. Tool schemas and validation

Custom tools are declared with a JSON schema. From the 15 Sep release window, Kestrel validates
tool-call arguments **strictly** for any custom tool whose schema does not declare
`additionalProperties`: a call containing a property not in the schema is rejected with
HTTP 400 `tool_schema_validation_error` before the tool runs. Schemas that declare
`additionalProperties: true` are unaffected.

Opt-out: setting `schema_validation: lenient` on a tool restores pre-release behaviour until
31 Dec 2026.

## 3. Prompt caching

Kestrel caches a stable prompt prefix so repeated requests do not pay full input price for it.

- **Default lifetime (TTL): 5 minutes** for any caller that does not set one. Before the 15 Sep
  release window the default was **60 minutes**. Callers can set 5, 10, 30 or 60 minutes explicitly.
- The TTL is refreshed each time the entry is read.
- The first request that finds no live entry **writes** it. Requests that start after the write
  completes can read it.
- Pricing: a cache write costs 1.25× the normal input price for the cached tokens; a cache read costs
  0.10×.
- Traces record `tokens.cache_write` and `tokens.cache_read` per call.

## 4. Reasoning

Models can spend **reasoning tokens** before answering. Reasoning tokens are billed at the output
price and appear in traces as `tokens.reasoning`.

- Settings: `off`, `low`, `medium`.
- **Default for alias-addressed calls: `medium`** from the 15 Sep release window (previously `off`).
- Default for snapshot-addressed calls: `off`.
- An explicit setting always overrides the default.

## 5. Output length

`max_output_tokens` caps generated tokens per call. **If a caller does not set it, Kestrel applies
a default: 4,000 tokens** from the 15 Sep release window (previously 16,000). When generation stops
at the cap, the call ends with `finish_reason: "length"` and the output is cut off where it
stopped. Maximum settable value: 32,000.

## 6. Tool-result size

A single tool or connector result delivered to a model is capped at **24 KB** from the 15 Sep
release window (previously 64 KB). This cap is a platform limit and cannot be raised. Larger
results are **truncated at the cap, not rejected** — the receiving step gets the first 24 KB.
Callers fetching large documents should enable **result chunking**, which delivers a large result
as a sequence of chunks of at most 24 KB each.

## 7. Rate limits

Each Kestrel account has a **rate tier** that sets its request allowance. Tiers are set by billing
agreement, not by API settings.

- Requests over the allowance are rejected with HTTP 429 `rate_limited`.
- A 429 response includes `retry_after_ms` — the suggested wait **in milliseconds**.
- **Rejected requests count against the allowance window.** Retrying immediately therefore consumes
  allowance without succeeding.
- Recommended client behaviour: exponential backoff with jitter.

## 8. Concurrency

Each API key may have at most **8 requests in flight** (previously 20; changed at the 15 Sep
release window). Requests beyond the cap wait in a platform queue; a request still waiting after
**30 seconds** fails with HTTP 504 `queue_timeout`. Clients should limit their own parallelism to
the cap.

## 9. Connectors

| Connector | Version | Notes |
|---|---|---|
| LitIndex | v3 | **Sunset** at the 15 Sep release window. |
| LitIndex | v4 | Current. Query results are returned in the field **`items`** (v3 used `results`). Otherwise compatible. |
| CiteRegistry | v2.3 | **Retired** at the 15 Sep release window. |
| CiteRegistry | v2.4 | Current. Lookups return **at most 20 records per response** with `has_more` and `next_cursor`. Set `follow_cursor: true` to have the connector fetch remaining pages automatically. v2.3 returned all records in one response. |

## 10. Pricing (per million tokens)

| | Input | Output (incl. reasoning) | Cache write | Cache read |
|---|---|---|---|---|
| All snapshots | $3.00 | $15.00 | 1.25 × input | 0.10 × input |

## 11. Regions and batch processing

- Regions: `us-east` and `eu-west`. The `eu-west` endpoint hostname changes on 1 Oct 2026; `us-east`
  is unchanged.
- The Batch API (asynchronous bulk requests) is deprecated from 15 Sep 2026 and will be removed on
  31 Mar 2027. Synchronous requests are unaffected.
