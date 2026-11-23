# Kestrel AI Platform — Changelog (Apr–Sep 2026)

Entries are listed oldest first. IDs are stable.

## KCL-001 · 2026-04-02 · Console
**Usage dashboard adds per-project breakdown**

The usage dashboard can now group spend by project tag.

## KCL-002 · 2026-04-09 · SDK
**Python SDK 4.2**

Adds typed tool-call helpers. No behaviour changes.

## KCL-003 · 2026-04-12 · Misc
**Console theme update**

Minor improvement. No behaviour change.

## KCL-004 · 2026-04-16 · Models
**kp-2026-02 becomes alias target**

`kestrel-pro-latest` now resolves to `kp-2026-02`.

## KCL-005 · 2026-04-23 · Docs
**Prompt caching guide rewritten**

Clarifies write/read pricing. No behaviour change.

## KCL-006 · 2026-04-30 · Connectors
**LitIndex connector v4 preview**

v4 available for opt-in testing. Response field for query results is `items`.

## KCL-007 · 2026-05-03 · Misc
**Docs search improvements**

Minor improvement. No behaviour change.

## KCL-008 · 2026-05-07 · Security
**SSO session length configurable**

Admins can set console session length from 1 to 24 hours.

## KCL-009 · 2026-05-14 · Console
**Trace explorer: span search**

Search spans by error type and component.

## KCL-010 · 2026-05-21 · SDK
**TypeScript SDK 3.8**

Streaming helpers; no behaviour changes.

## KCL-011 · 2026-05-28 · Regions
**eu-west capacity expansion**

Additional capacity in eu-west.

## KCL-012 · 2026-05-30 · Misc
**Status page RSS**

Minor improvement. No behaviour change.

## KCL-013 · 2026-06-04 · Models
**kp-2025-11 deprecation notice**

`kp-2025-11` will be retired at the September release window.

## KCL-014 · 2026-06-07 · Misc
**Billing CSV export**

Minor improvement. No behaviour change.

## KCL-015 · 2026-06-11 · Connectors
**CiteRegistry v2.4 preview**

v2.4 available for opt-in testing. Paginated responses (20 records) with cursors.

## KCL-016 · 2026-06-18 · Billing
**Invoices show cache read/write lines**

Cache tokens itemised on invoices.

## KCL-017 · 2026-06-25 · Docs
**Rate-limit guide**

New guide on backoff strategies.

## KCL-018 · 2026-06-29 · Misc
**Console keyboard shortcuts**

Minor improvement. No behaviour change.

## KCL-019 · 2026-07-02 · Console
**Alert webhooks**

Send platform alerts to a webhook.

## KCL-020 · 2026-07-09 · SDK
**Python SDK 4.3**

Adds chunked tool-result helpers for large documents.

## KCL-021 · 2026-07-12 · Misc
**Docs: prompt design examples**

Minor improvement. No behaviour change.

## KCL-022 · 2026-07-16 · Security
**Audit log export**

Export console audit logs as CSV.

## KCL-023 · 2026-07-23 · Models
**Release window schedule published**

Model and platform changes ship at quarterly release windows; next window 15 Sep 02:00 UTC.

## KCL-024 · 2026-07-26 · Misc
**Trace retention 30 → 45 days**

Minor improvement. No behaviour change.

## KCL-025 · 2026-07-30 · Connectors
**Connector status page**

Status page for all first-party connectors.

## KCL-026 · 2026-08-04 · Console
**Project budgets**

Set monthly spend budgets per project.

## KCL-027 · 2026-08-06 · SDK
**Go SDK 1.0**

First stable Go SDK.

## KCL-028 · 2026-08-09 · Misc
**Console accessibility fixes**

Minor improvement. No behaviour change.

## KCL-029 · 2026-08-11 · Docs
**Tool schema guide updated**

Explains `additionalProperties` and upcoming strict validation.

## KCL-030 · 2026-08-13 · Platform
**September release window: change summary**

Summary of platform changes taking effect 15 Sep 02:00 UTC. See individual entries.

## KCL-031 · 2026-08-15 · Misc
**SDK deprecation warnings**

Minor improvement. No behaviour change.

## KCL-032 · 2026-08-18 · Security
**API key rotation reminders**

Console reminds admins of keys older than 180 days.

## KCL-033 · 2026-08-20 · Billing
**Annual contract true-ups**

Account rate tiers are re-aligned to contracted volume at the September release window. Account owners have been notified individually.

## KCL-034 · 2026-08-25 · Console
**Trace export to object storage**

Daily trace exports can be written to customer storage.

## KCL-035 · 2026-08-27 · Docs
**Concurrency guide**

How to size client-side parallelism.

## KCL-036 · 2026-09-01 · SDK
**Python SDK 4.4**

Adds `follow_cursor` support for CiteRegistry v2.4.

## KCL-037 · 2026-09-03 · Regions
**eu-west endpoint hostname change announced**

The eu-west endpoint hostname changes on 1 Oct 2026. us-east unchanged.

## KCL-038 · 2026-09-05 · Misc
**Docs: release-window FAQ**

Minor improvement. No behaviour change.

## KCL-039 · 2026-09-08 · Platform
**Batch API deprecation announced**

The Batch API is deprecated from 15 Sep 2026 and removed 31 Mar 2027. Synchronous requests unaffected.

## KCL-040 · 2026-09-10 · Console
**Maintenance: console read-only 12 Sep 06:00–07:00 UTC**

Console briefly read-only. API unaffected.

## KCL-041 · 2026-09-12 · Misc
**Status page redesign**

Minor improvement. No behaviour change.

## KCL-042 · 2026-09-15 · Console
**Release window complete**

All September changes deployed. No incidents reported on the status page.

## KCL-043 · 2026-09-15 02:00 UTC · Models
**kp-2026-08 released; alias moves**

`kp-2026-08` released. `kestrel-pro-latest` now resolves to `kp-2026-08`. `kp-2026-08` returns tool-call arguments as JSON objects.

## KCL-044 · 2026-09-15 02:00 UTC · Models
**kp-2025-11 retired**

Requests to `kp-2025-11` now fail.

## KCL-045 · 2026-09-15 02:00 UTC · Tools
**Strict tool-schema validation**

Custom tools whose schema does not declare `additionalProperties` are validated strictly. Opt-out `schema_validation: lenient` available until 31 Dec 2026.

## KCL-046 · 2026-09-15 02:00 UTC · Connectors
**LitIndex v4 GA; v3 sunset**

All LitIndex traffic is served by v4. Query results are returned in `items`.

## KCL-047 · 2026-09-15 02:00 UTC · Connectors
**CiteRegistry v2.4 GA; v2.3 retired**

Lookups return at most 20 records per response with `has_more` and `next_cursor`. Use `follow_cursor: true` to fetch all pages.

## KCL-048 · 2026-09-15 02:00 UTC · Billing
**Rate tiers re-aligned**

Contracted rate tiers take effect. See your account notice.

## KCL-049 · 2026-09-15 02:00 UTC · Platform
**Per-key concurrency cap 20 → 8**

At most 8 requests in flight per API key. Queued requests time out after 30 s with 504 `queue_timeout`.

## KCL-050 · 2026-09-15 02:00 UTC · Caching
**Default prompt-cache TTL 60 → 5 minutes**

Callers that do not set a TTL now get 5 minutes. 10, 30 and 60 minutes remain available explicitly.

## KCL-051 · 2026-09-15 02:00 UTC · Models
**Default reasoning on aliases: medium**

Alias-addressed calls without an explicit reasoning setting now use `medium`. Snapshot-addressed calls unchanged (`off`).

## KCL-052 · 2026-09-15 02:00 UTC · Models
**Default max_output_tokens 16,000 → 4,000**

Applies to calls that do not set `max_output_tokens`.

## KCL-053 · 2026-09-15 02:00 UTC · Tools
**Tool-result size cap 64 KB → 24 KB**

Results above 24 KB are truncated at the cap. Use result chunking for large documents.

## KCL-054 · 2026-09-16 · Docs
**Migration guide: September changes**

Checklist for clients affected by the September window.

## KCL-055 · 2026-09-16 · Connectors
**LitIndex v4: latency improvement**

Median query latency down 12%.

## KCL-056 · 2026-09-16 · Misc
**Console: alias resolution shown on traces**

Minor improvement. No behaviour change.

## KCL-057 · 2026-09-17 · Security
**Service-account inventory view**

Console lists service accounts per project, including those created by agent teams.

## KCL-058 · 2026-09-17 · SDK
**Python SDK 4.5**

Defaults `follow_cursor` to false for backward compatibility.

## KCL-059 · 2026-09-17 · Regions
**us-east maintenance completed**

No customer impact.
