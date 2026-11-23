# Cause Codes — Litmus Incident Review

Use these codes in `root_causes.csv`. Each code names a **root cause**: a change that, on its own,
started a chain of effects in Litmus. Symptoms (alerts, retries, slow jobs, high cost) are not root
causes; they belong in your causal graph, not here.

## Rules for claiming a code

- Claim a code only if you believe it is a root cause **of this incident in this system**. A change
  appearing in the Kestrel changelog does not mean Litmus was affected by it.
- Not every code applies. Claiming a code that does not apply costs points.
- Each claim needs a **component** (`orchestrator`, `search`, `extract`, `synthesize`, `cite_check`),
  an **onset time** (when the cause first affected Litmus), and **one evidence span ID** from the
  traces that shows the cause acting. A claim whose evidence span does not show that cause earns no
  credit.
- Claim each code at most once.

## Codes (alphabetical)

| Code | Definition |
|---|---|
| `BATCH_API_DEPRECATION` | A Kestrel batch-processing interface Litmus depends on was deprecated or changed, causing batch work to fail or be rejected. |
| `CACHE_TTL_DEFAULT_CHANGED` | A component that relies on the platform's default prompt-cache lifetime was affected when that default changed, altering cache reuse and therefore cost or latency. |
| `CLOCK_SKEW` | Clocks on different Litmus or Kestrel hosts disagree, causing ordering, expiry or timeout logic to misbehave. |
| `CONCURRENCY_CAP_REDUCED` | A lower limit on simultaneous requests caused Litmus requests beyond the limit to queue, time out or be rejected. |
| `CONNECTOR_FIELD_RENAMED` | A connector version changed the name or location of a response field, so a Litmus component reads the wrong field and treats the response as empty or incomplete. |
| `CONNECTOR_PAGINATION_CHANGED` | A connector changed how many records it returns per response, or how further records are fetched, so a Litmus component processes only part of the available data. |
| `CREDENTIAL_MISUSE` | A credential or service account was used by an unauthorised party or for an unauthorised purpose, producing traffic or actions Litmus did not intend. |
| `EMBEDDING_INDEX_STALE` | A search index or embedding store was not refreshed, so retrieval returns outdated or missing documents. |
| `MODEL_ALIAS_DRIFT` | A component that addresses its model through an alias began receiving a different model snapshot, and a behavioural difference in that snapshot broke something downstream. |
| `OUTPUT_TOKEN_DEFAULT_LOWERED` | A component that does not set its own output length limit was affected when the platform's default limit changed, cutting off generated output. |
| `RATE_TIER_DOWNGRADE` | The account's request-rate allowance fell, so Litmus requests beyond the new allowance were rejected with rate-limit errors. |
| `REASONING_DEFAULT_CHANGED` | A component that does not set its own reasoning mode was affected when the platform's default reasoning behaviour changed, altering token usage or output. |
| `REGION_ENDPOINT_MIGRATION` | A Kestrel regional endpoint used by Litmus moved or changed, causing requests to fail, be redirected, or be served differently. |
| `TOOL_RESULT_LIMIT_LOWERED` | A lower maximum size for tool or connector results caused large results delivered to a Litmus component to be cut off. |
| `TOOL_SCHEMA_STRICTNESS` | Stricter validation of tool definitions or tool-call arguments caused calls that were previously accepted to be rejected. |

## Notes

- A root cause can produce symptoms in components other than the one it first affected. Name the
  component where the cause first acts.
- Kestrel documentation describes Kestrel's behaviour. Where it differs from what you expect of other
  platforms, Kestrel's documentation is authoritative for this incident.
