# On-call chat export — #litmus-oncall (times UTC)

**[Thu 22:41] priya.n (on-call SRE):** Paging in. Since Tuesday the alerts that keep firing are: ExtractDecodeErrors (15×), ExtractQueueTimeouts (8×), PlanArgParseErrors (8×), JobErrorRate (3×).
**[Thu 22:44] priya.n (on-call SRE):** Job error rate by day (Mon→Thu): 0% / 55% / 52% / 55%.
**[Thu 22:47] marco.d (agent owner):** Nothing changed on our side this week except d-0431 on Tuesday morning, and that was logging only.
**[Thu 22:52] priya.n (on-call SRE):** Kestrel had their quarterly release window Tue 02:00. Their status page says no incidents though.
**[Thu 23:03] lena.k (security):** Flagging: Wednesday 01:00–03:00 we saw a large burst of LitIndex bulk exports from svc-litindex-reindex. That account is not in our inventory. I think a credential has been misused.
**[Thu 23:05] lena.k (security):** My recommendation is to revoke svc-litindex-reindex and rotate all Litmus credentials before anything else.
**[Thu 23:09] marco.d (agent owner):** Can we not revoke things in the middle of the night without checking? I'll look in the morning.
**[Thu 23:15] ola.b (FinOps):** From the billing side: cost per review job was $0.61 on Monday and $0.53 on Thursday.
**[Thu 23:21] priya.n (on-call SRE):** Monday also had CiteRegistry timeouts and some 404s on full text, so not everything in the alert list is new.
**[Thu 23:34] dr.sato (scientist):** A couple of us think this week's reviews feel off compared with last week. Hard to say exactly how.
**[Thu 23:40] marco.d (agent owner):** Could the fallback index be stale? It only gets refreshed quarterly.
**[Thu 23:52] priya.n (on-call SRE):** Exporting 96h of traces (Mon 00:00 → Fri 00:00) for the review team.
**[Fri 00:06] lena.k (security):** For the record, I still think this is an access problem.
**[Fri 08:58] priya.n (on-call SRE):** Escalating to the incident review team. Please root-cause, propose a minimal fix, and do not change production directly.
