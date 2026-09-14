# Risks & Open Questions

## Risks and how we plan to mitigate them

| Risk | Impact | Mitigation |
|---|---|---|
| We're taking on operational responsibility Atlas used to handle | Outages/data loss if under-staffed | Budget real SRE time (see cost model), invest in runbooks, alerting, and drills before cutover |
| Sharded cluster restores cause brief downtime | Longer recovery windows than a managed service might advertise | Set expectations up front; practice restores in Phase 2 so the real RTO is known, not assumed |
| Sizing estimates are based on public pricing, not real usage | Under- or over-provisioning | Load-test with representative data in the POC phase (November) before committing to final sizing |
| Kubernetes/operator upgrades introduce risk over time | Version drift, harder upgrades if delayed | Stay current with Operator releases; test upgrades in staging first, always |
| Team unfamiliarity with self-managed MongoDB operations | Slower incident response initially | Pair with Percona docs/support channel during the first few months; consider a short-term Percona support subscription |
| Data migration itself (Atlas -> self-hosted) is a risk window | Data loss/inconsistency during cutover | Use the dual-write/shadow-traffic approach in Phase 4 rather than a hard cutover |

## Open questions for the customer

These are the specific things that would let us replace estimates with real numbers and firm up the plan:

1. **Atlas billing** — can we get the last 2-3 months of Atlas invoices, plus the current cluster configuration (tier, shard count, region, backup settings)?
2. **Data size and growth** — what's the actual current data size, and what's the expected growth rate over the next 12-24 months?
3. **Performance profile** — peak IOPS, throughput, and concurrent connections, so we size nodes on real numbers instead of storage capacity alone.
4. **RTO / RPO requirements** — how much downtime and data loss is acceptable in a worst-case scenario? This determines backup frequency and whether multi-region DR is actually needed later.
5. **Compliance / data residency** — any regulatory requirements (e.g. data must stay in a specific region, specific encryption standards) that affect the architecture?
6. **Operations model** — will the customer's own team run this day-to-day, will KubeNine provide managed operations, or some hybrid? This materially changes how the "savings" number should be presented to their finance team.
7. **Timeline confirmation** — is November still the confirmed start date, and are there any hard deadlines (e.g. an Atlas contract renewal date) driving the schedule?

---
Back to [README](../README.md) · Previous: [Migration plan](migration-plan.md)
