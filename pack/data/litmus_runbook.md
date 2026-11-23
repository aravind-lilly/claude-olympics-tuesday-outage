# Litmus — Service Runbook (v3.4, owner: Literature Intelligence agent team)

## 1. What Litmus does

Litmus produces literature reviews for Halcyon Bio scientists. Each request is a **review job**,
traced end-to-end under one `trace_id`. Litmus runs in Kestrel region `us-east` only and uses only
synchronous Kestrel requests.

## 2. Pipeline

| Stage | Component | What happens |
|---|---|---|
| 1 | Orchestrator | Plans the job with a model call (`plan`) that returns tool calls for the subagents. Litmus parses each tool call's arguments. |
| 2 | Search | Formulates a query and queries the LitIndex connector. Keyword queries read results through the connector's helper; structured (filtered) queries parse the raw response using the configured `result_field`. If the primary query yields zero papers, Search falls back to `litindex-cache`, a secondary index refreshed quarterly. |
| 3 | Extract | Fetches each paper's full text (`fetch_paper`) and extracts findings with a model call per paper (`extract_findings`). Extract warms the prompt cache with its first call, then fans the remaining calls out in parallel. |
| 4 | Synthesize | Writes the review in one model call (`write_review`) from all extracted findings. |
| 5 | Cite-check | Prepares the citation list, looks citations up in CiteRegistry, and verifies them (`verify_citations`). |

## 3. Retries and re-dispatch

- The orchestrator's **retry policy** governs how subagent requests that fail are retried, up to
  `retry_max` attempts per request.
- If an Extract request still fails after its retries, or a stage cannot complete, the orchestrator
  **re-dispatches the stage**: it re-plans (a new `plan` call) and re-runs the whole stage, including
  calls that had already succeeded. At most two re-dispatches per job.
- A plan call whose tool-call arguments cannot be parsed is attempted up to three times in total.

## 4. Configuration

Litmus configuration has two layers:
- **Base config** — `litmus_config.yaml`, exported nightly.
- **Deployment overlay** — settings applied at deploy time on top of the base config. Some overlay
  settings are recorded in the deployment log; others are managed directly by the agent team.
  Where the base config shows a key as `overlay`, the effective value comes from the overlay.

A key set to `null` uses the Kestrel platform default.

## 5. Constraints you must respect

- **Cite-check cache ≤ 10 minutes.** Cite-check's cached prompt includes the current retraction
  list, rebuilt every 10 minutes. A longer cache lets retracted papers pass verification.
- **Orchestrator reasoning stays `medium`.** Planning quality depends on it. With reasoning off the
  orchestrator over-plans: extra searches and roughly 30% more Extract calls.
- **Job SLA: 20 minutes.** Extract parallelism below 6 makes jobs with more than 12 papers breach
  the SLA.
- **Change control:** every configuration change in an incident fix is a production change and must
  be justified. Unneeded changes add risk.

## 6. Outcome taxonomy (used in incident reviews)

**Hard failures** (job ends in error): plan failed · rate limited after retries · Extract timed out
after retries · citation check failed · SLA exceeded.

**Degraded outputs** (job reports success, output is wrong or incomplete): partial extraction ·
truncated review · thin review (fallback index used because of a fault) · under-verified citations ·
stale citation verification.

## 7. Known background noise

- Some publishers return 404 for full text; Extract skips those papers.
- CiteRegistry occasionally times out; Cite-check retries.
- A small share of queries legitimately match no papers and use the fallback index.

## 8. Maintenance jobs

A **quarterly LitIndex re-index** refreshes `litindex-cache`. It runs under a dedicated service
account owned by the agent team. Ask the agent owner for schedule details.

## 9. Alerting

Rules are evaluated hourly unless stated. Silent degradations do not alert. Consecutive firing
hours are merged into one row in `alert_history.csv`.

| Rule | Fires when |
|---|---|
| `KestrelRateLimited` | ≥ 15 HTTP 429 `rate_limited` responses in an hour |
| `ExtractQueueTimeouts` | ≥ 5 HTTP 504 `queue_timeout` responses in an hour |
| `PlanArgParseErrors` | ≥ 5 `tool_args_parse_error` errors in an hour |
| `CiteSchemaRejections` | ≥ 5 `tool_schema_validation_error` errors in an hour |
| `ExtractDecodeErrors` | ≥ 3 `json_decode_error` errors in an hour |
| `ReviewIncomplete` | ≥ 3 `review_incomplete` errors in an hour |
| `CiteRegistryTimeouts` | ≥ 2 `upstream_timeout` errors in an hour |
| `PaperNotFound` | ≥ 3 HTTP 404 `paper_not_found` responses in an hour |
| `JobErrorRate` | ≥ 15% of jobs started in a 3-hour window ended in error (minimum 6 jobs) |
| `CostPerJobHigh` | Daily cost per job > 1.25 × Monday's (evaluated at end of day) |
| `LitIndexBulkTraffic` (security) | > 60 LitIndex bulk-export requests from one account in 2 hours |
