# Litmus — Deployment Log

| Time (UTC) | Deploy | Change |
|---|---|---|
| 2026-08-10 14:22 | d-0402 | Synthesize prompt: house style v7 (wording only) |
| 2026-08-12 10:05 | d-0404 | Dependency bumps (security patches) |
| 2026-08-14 09:12 | ov-01 | Overlay update: `orchestrator.reasoning` → `medium` |
| 2026-08-17 16:40 | d-0407 | Search: query expansion for gene synonyms |
| 2026-08-18 15:40 | ov-02 | Overlay update: `synthesize.max_output_tokens` → `16000` |
| 2026-08-19 11:15 | d-0409 | Dashboard: job duration panel |
| 2026-08-21 14:03 | ov-03 | Overlay update: `cite_check.cache_ttl_minutes` → `10` |
| 2026-08-24 09:30 | d-0412 | Cite-check: improved DOI normalisation |
| 2026-08-26 15:55 | d-0414 | Orchestrator: plan prompt clarifications |
| 2026-08-28 10:31 | ov-04 | Overlay update: `synthesize.reasoning` → unset (use Kestrel default) |
| 2026-08-31 13:10 | d-0418 | Extract: findings schema v3 (adds effect sizes) |
| 2026-09-01 09:55 | ov-05 | Overlay update: `orchestrator.max_concurrency` → unset (use Kestrel default) |
| 2026-09-02 10:45 | d-0421 | Runbook link in alert payloads |
| 2026-09-07 17:20 | d-0425 | Synthesize: section ordering tweak |
| 2026-09-09 12:00 | d-0428 | Load test harness (staging only) |
| 2026-09-15 03:10 | d-0431 | Logging: switch span attribute keys to snake_case (no functional change) |
