# Causal Graph Node Vocabulary

Build `causal_graph.json` only from these node names. An edge `[A, B]` means **A directly causes B**. Draw direct links only — if A causes B and B causes C, submit `[A, B]` and `[B, C]`, not `[A, C]`.

Scoring: each correct edge earns credit; each edge that is not part of this incident's causal structure cancels one and a quarter correct edges. Edges using names not listed here count as wrong.

## Root-cause nodes

Every code in `cause_codes.md` is also a node. A root-cause node should only appear as the start of an edge.

- `BATCH_API_DEPRECATION`
- `CACHE_TTL_DEFAULT_CHANGED`
- `CLOCK_SKEW`
- `CONCURRENCY_CAP_REDUCED`
- `CONNECTOR_FIELD_RENAMED`
- `CONNECTOR_PAGINATION_CHANGED`
- `CREDENTIAL_MISUSE`
- `EMBEDDING_INDEX_STALE`
- `MODEL_ALIAS_DRIFT`
- `OUTPUT_TOKEN_DEFAULT_LOWERED`
- `RATE_TIER_DOWNGRADE`
- `REASONING_DEFAULT_CHANGED`
- `REGION_ENDPOINT_MIGRATION`
- `TOOL_RESULT_LIMIT_LOWERED`
- `TOOL_SCHEMA_STRICTNESS`

## Effect and symptom nodes (alphabetical)

| Node | Meaning |
|---|---|
| `ALERT_FLOOD` | Error-rate alerts fire repeatedly across the incident window. |
| `ARG_PARSE_ERRORS` | The orchestrator fails to parse tool-call arguments returned by its model. |
| `CACHE_MISSES` | Calls that would normally read the prompt cache write it instead. |
| `COST_SPIKE` | Cost per review job rises above normal. |
| `EMPTY_PRIMARY_RESULTS` | The primary literature query returns data that Litmus parses as zero results. |
| `FALLBACK_INDEX_USED` | Search falls back to the cached secondary index (litindex-cache). |
| `IMMEDIATE_RETRY_STORM` | Rejected requests are retried immediately and repeatedly, adding load in the same window. |
| `JOB_FAILURES` | Review jobs end in error. |
| `LATENCY_INCREASE` | Review jobs take longer than normal. |
| `OUTPUT_LENGTH_LIMIT_HIT` | Generation stops because the output token limit is reached (finish_reason = length). |
| `PARTIAL_CITATION_SET` | Cite-check receives only part of the citation records it asked for. |
| `PARTIAL_EXTRACTION` | Findings are extracted from only part of a paper. |
| `QUEUE_TIMEOUTS` | Requests wait in the platform queue past 30 s and fail with HTTP 504. |
| `RATE_LIMIT_REJECTIONS` | Kestrel rejects requests with HTTP 429 because the account rate allowance is exceeded. |
| `REASONING_TOKENS` | Model calls consume reasoning tokens they did not consume before. |
| `SCHEMA_REJECTIONS` | Tool calls are rejected by tool-schema validation before they execute. |
| `STAGE_REDISPATCH` | The orchestrator re-plans and re-runs a whole stage, repeating work already completed. |
| `STALE_INDEX_CONTENT` | The search index serves outdated documents because it was not refreshed. |
| `THIN_REVIEWS` | Reviews are built from fewer papers than the query matched. |
| `TIMESTAMP_DISORDER` | Events are recorded with timestamps out of their true order. |
| `TRUNCATED_REVIEWS` | Reviews end before the review is complete. |
| `TRUNCATED_TOOL_RESULT` | A tool result reaches the model cut off before its end. |
| `UNAUTHORISED_TRAFFIC` | Requests are made by a party or account not authorised to make them. |
| `UNDER_VERIFIED_CITATIONS` | Reviews are marked verified although not every citation was checked. |

## Format

```json
{"edges": [["SOME_CAUSE", "SOME_EFFECT"], ["SOME_EFFECT", "SOME_SYMPTOM"]]}
```
