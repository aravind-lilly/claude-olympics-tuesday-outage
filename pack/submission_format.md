# Submission Format

## `root_causes.csv`

UTF-8 CSV with this header and one row per root cause:

```
cause_code,component,onset_time,evidence_span_id
```

| Column | Rule |
|---|---|
| `cause_code` | A code from `cause_codes.md`. Each code at most once. |
| `component` | `orchestrator`, `search`, `extract`, `synthesize` or `cite_check` — where the cause first acts. |
| `onset_time` | ISO-8601 UTC, e.g. `2026-09-15T04:30:00Z` — when the cause first affected Litmus. |
| `evidence_span_id` | One `span_id` from your `traces.jsonl` that shows this cause acting. |

## `causal_graph.json`

```json
{"edges": [["NODE_A", "NODE_B"], ["NODE_B", "NODE_C"]]}
```

Node names from `node_vocab.md`. An edge means "directly causes".

## `fix_set.json`

```json
{"operations": [{"op": "...", "...": "...", "note": "optional justification"}]}
```

Operations and parameters from `action_catalog.md`. Applied in order from Tue 15 Sep 02:00 UTC.
An empty list is valid but fixes nothing.