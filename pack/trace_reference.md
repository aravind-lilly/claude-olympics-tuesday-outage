# Trace Field Reference — `traces.jsonl`

One JSON object per line, one line per **span**. Spans cover Mon 14 Sep 00:00 → Fri 18 Sep 00:00 UTC
and are sorted by start time. Fields that do not apply to a span are omitted.

## Common fields

| Field | Meaning |
|---|---|
| `span_id` | Unique span ID (`sp_` + 12 hex). Use these as evidence in `root_causes.csv`. |
| `trace_id` | The review job (or maintenance run) this span belongs to. |
| `parent_id` | The job's root span, or `null` for root spans and maintenance traffic. |
| `start`, `end`, `duration_ms` | UTC timestamps and duration. |
| `component` | `orchestrator`, `search`, `extract`, `synthesize`, `cite_check`, or `external` (traffic not from Litmus). |
| `kind` | `job` (root span of a review job), `llm_call`, `tool_call`, `connector_request`, `stage`. |
| `name` | Operation name, e.g. `plan`, `fetch_paper`, `extract_findings`, `write_review`, `verify_citations`, `litindex.query`, `redispatch_extract`. |
| `status` | `ok` or `error`. A span can be `ok` and still carry a bad result. |
| `attempt` | Attempt number for retried operations. Re-dispatched stages restart at 1 for their calls. |
| `http_status`, `error_type`, `error_message` | Present on errors and connector responses. |
| `attrs` | Kind-specific attributes (below). |

## Model calls (`kind: llm_call`)

| Field | Meaning |
|---|---|
| `model_requested` | What Litmus asked for (an alias or a snapshot). |
| `model_resolved` | The snapshot Kestrel actually used. |
| `tokens.input` | Uncached input tokens. |
| `tokens.cache_read`, `tokens.cache_write` | Prompt-cache tokens read or written on this call. |
| `tokens.output` | Generated tokens. |
| `tokens.reasoning` | Reasoning tokens (billed as output). |
| `finish_reason` | `stop`, `tool_use`, `length` (hit the output cap), or `error`. |
| `cost_usd` | Cost of this call. |

## Selected `attrs`

| Attribute | On | Meaning |
|---|---|---|
| `job_id`, `papers_found` | job root | Job ID; papers Search returned to the pipeline. |
| `subtasks_planned` | `plan` | Subtasks in the plan. |
| `connector`, `connector_version`, `index` | connector requests | Which connector, version and index answered. |
| `bytes_received` | connector / tool calls | Payload size delivered. |
| `query_mode`, `result_field_read`, `result_count` | `litindex.query` | Keyword or structured query; which response field Search read (`helper` for keyword queries); results parsed. |
| `fallback_used`, `index_snapshot_age_days` | `litindex_cache.query` | Fallback index used; age of its data. |
| `chunk` | `fetch_paper` | `i/n` when result chunking delivered the paper in parts. |
| `queue_wait_ms`, `account_in_flight` | Extract calls | Time spent queued; in-flight requests on the account at rejection. |
| `retry_after_ms`, `retry_policy` | 429 responses | Kestrel's suggested wait; the policy Litmus applied. |
| `records_returned`, `has_more`, `next_cursor`, `cursor_followed` | `citeregistry.lookup` | Pagination state. |
| `citations_total`, `citations_checked`, `verdict` | `verify_citations`, `prepare_citations` | Citations in the review vs. checked. |
| `papers_in_context` | `write_review` | Papers whose findings reached Synthesize. |
| `dangling_markers` | `parse_review` | Citation markers in the review with no reference-list entry. |
| `reason` | `redispatch_extract` | Why the stage was re-dispatched. |
| `service_account`, `client_ip`, `query_type`, `page` | `external` traffic | Non-Litmus traffic details. |
