# Proposal: Self-Managed MongoDB on Kubernetes

## The situation

You're currently running MongoDB on Atlas, and as your data has grown into the multi-terabyte range, the cost has grown with it. You need a database platform that can comfortably handle 2-5 TB of sharded data, with reliable backups and the ability to recover to any point in time — without the Atlas price tag.

## The recommendation

Move to a self-managed MongoDB deployment on Kubernetes (AWS EKS), running the **Percona Operator for MongoDB** — a free, open-source operator that gives us everything Atlas provides at the database layer (automated sharding, failover, backups, point-in-time recovery) without a commercial license fee sitting on top of it.

Full technical detail is in [docs/architecture.md](../docs/architecture.md); the short version:

- Data is automatically split across shards, each running as a 3-node replica set for high availability.
- Every shard is spread across 3 Availability Zones, so a data center failure doesn't take the database down.
- Backups run continuously, with the ability to restore to any specific second (point-in-time recovery), not just the last nightly snapshot.

## The savings

Using publicly available Atlas and AWS pricing (we don't have your actual Atlas invoice yet — this is the first thing we'd want from you to sharpen these numbers):

| | ~2 TB workload | ~5 TB workload |
|---|---|---|
| Atlas (estimated) | ~$220k/year | ~$450k/year |
| Self-hosted infrastructure only | ~$39k/year | ~$69k/year |
| Self-hosted incl. operations effort | ~$111k/year | ~$141k/year |
| **Realistic savings** | **~50%** | **~69%** |

The gap is largest on raw infrastructure (80%+), but we've deliberately included the cost of the engineering time needed to operate the cluster yourselves, so the "realistic savings" figures are the honest number — not a best-case scenario. Full breakdown and assumptions in [docs/cost-comparison.md](../docs/cost-comparison.md).

## The timeline

Targeting a **November 2026** start:

- **Nov–Dec**: stand up a proof-of-concept cluster, load real-scale data, test backups and failure recovery
- **Jan**: validate performance parity and get security/monitoring sign-off
- **Feb**: shadow production traffic, then cut over
- **Mar**: stabilize, then decommission Atlas

Full plan with milestones: [docs/migration-plan.md](../docs/migration-plan.md).

## What we need from you to move forward

1. Your last 2-3 months of Atlas invoices and current cluster configuration
2. Current data size and expected growth over the next 12-24 months
3. Any hard requirements around recovery time, data loss tolerance, or compliance
4. A decision on who operates the cluster day-to-day (your team, us, or a hybrid) — this affects how the savings numbers ultimately land

Full list: [docs/risks-and-open-questions.md](../docs/risks-and-open-questions.md).

---
See the [README](../README.md) for the full documentation set.
