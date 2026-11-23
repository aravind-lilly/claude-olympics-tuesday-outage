# Fix Action Catalog

`fix_set.json` lists configuration operations, applied in order from the moment of Kestrel's release window (Tue 15 Sep 02:00 UTC). Only these operations exist. Each object has an `op` field plus the parameters shown; an optional `note` field is ignored by scoring.

- Kestrel may **reject** an operation it cannot perform (for example a retired version, or a limit it does not allow). A rejected operation has no effect and counts as an unnecessary change.
- Every operation not needed to fix this incident counts as an **unnecessary change** and can reduce the fix score.

| Operation | What it does | Parameters |
|---|---|---|
| `pin_model` | Address the component's model by a fixed snapshot. | component: orchestrator / synthesize; snapshot: kp-2025-11 / kp-2026-02 / kp-2026-08 |
| `use_model_alias` | Address the component's model through `kestrel-pro-latest`. | component: orchestrator / synthesize |
| `set_tool_arg_parsing` | How the orchestrator parses tool-call arguments. | component: orchestrator; mode: string / object |
| `update_tool_schema` | Set `additionalProperties` on Cite-check's custom tool schema. | component: cite_check; additional_properties: true / false |
| `set_schema_validation` | Tool-schema validation mode for Cite-check's custom tool. | component: cite_check; mode: lenient / strict |
| `set_result_field` | Which raw LitIndex response field Search parses for structured queries (`auto` accepts either). | component: search; field: results / items / auto |
| `set_connector_version` | Pin a connector version. | component: search (LitIndex: v3 / v4) or cite_check (CiteRegistry: v2.3 / v2.4); version |
| `set_follow_cursor` | Whether the CiteRegistry connector fetches all pages. | component: cite_check; enabled: true / false |
| `set_retry_policy` | Orchestrator retry policy for failed subagent requests. | component: orchestrator; policy: immediate / fixed_delay / exp_backoff_jitter |
| `set_retry_max` | Maximum attempts per request before stage re-dispatch. | component: orchestrator; n: 1–10 |
| `request_rate_tier` | Ask Kestrel for a different account rate tier. | tier: string |
| `set_max_fanout` | Maximum Extract calls the orchestrator issues per wave. | component: orchestrator; n: 1–32 |
| `set_max_concurrency` | Client-side limit on Litmus requests in flight across all jobs. | component: orchestrator; n: 1–32 |
| `set_cache_ttl` | Explicit prompt-cache TTL for a component. | component: extract / synthesize / cite_check; minutes: 5 / 10 / 30 / 60 |
| `set_reasoning` | Explicit reasoning mode. | component: orchestrator / synthesize; mode: off / low / medium |
| `set_result_chunking` | Fetch large tool results in chunks of at most the platform cap. | component: extract; enabled: true / false |
| `set_tool_result_limit` | Change the tool-result size cap. | component; kb: integer |
| `set_max_output_tokens` | Explicit output-token cap. | component: synthesize; n: 256–32000 |
| `rollback_deploy` | Roll back a Litmus deploy. | deploy_id: e.g. d-0431 |
| `revoke_service_account` | Revoke a service account. | name: string |
| `rotate_credentials` | Rotate a component's credentials. | component |
| `set_region` | Move Litmus to another Kestrel region. | region: us-east / eu-west |
| `disable_component` | Disable a pipeline component. | component |
| `set_timeout` | Client-side timeout for a component's requests. | component; seconds: integer |
| `clear_cache` | Flush a component's prompt cache. | component |
| `failover_index` | Choose the index Search queries. | component: search; index: litindex / litindex-cache |

## Format

```json
{"operations": [
  {"op": "set_timeout", "component": "search", "seconds": 30, "note": "why this change is needed"}
]}
```
