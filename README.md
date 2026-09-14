# MongoDB on Kubernetes — Architecture & Cost Proposal

The customer is running MongoDB on Atlas, needs to scale to 2-5 TB of sharded data, and wants reliable backups with point-in-time recovery (PITR) - but Atlas at that scale is getting expensive. This repo is our research and proposal for moving them to a self-managed MongoDB cluster on Kubernetes, and what it would save them.

## The short version

- **Run it with the Percona Operator for MongoDB** on AWS EKS. It's free and open-source, and unlike the other operators out there, it gives us real sharding, automated failover, and backup/PITR without needing a paid enterprise license underneath it.
- **Architecture**: sharded cluster (each shard a 3-node replica set), spread across 3 Availability Zones for high availability, with continuous backups streamed to S3 and point-in-time recovery down to the second.
- **Cost**: based on public Atlas and AWS pricing (we don't have the customer's real invoice yet), self-hosting looks like it could save roughly **50-70%** even after accounting for the engineering time to run it ourselves. Infrastructure-only savings are closer to 80-85%.
- **Timeline**: five phases from proof-of-concept (Nov) through validation, shadow traffic, cutover, and Atlas decommission (targeting March completion).
- **Biggest open item**: we're working off public pricing and typical sizing, not the customer's real numbers. Getting their actual Atlas bill and current data profile is the single best next step to sharpen everything below.



## Read more


| Doc                                                                  | What's in it                                                                                                                                                            |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [docs/architecture.md](docs/architecture.md)                         | Why Percona, the sharded cluster design (with diagram), sizing for 2 TB and 5 TB, high availability, backup/PITR mechanics, and a brief look at security and monitoring |
| [docs/cost-comparison.md](docs/cost-comparison.md)                   | Atlas vs self-hosted cost breakdown for both scale scenarios, and why the gap is so large                                                                               |
| [docs/cost_model.py](docs/cost_model.py)                             | The actual calculator behind those numbers — rerun it with real inputs once we have them                                                                                |
| [docs/risks-and-open-questions.md](docs/risks-and-open-questions.md) | What could go wrong, and the specific questions we need answered by the customer                                                                                        |
| [proposal/customer-proposal.md](proposal/customer-proposal.md)       | The condensed, client-facing version of all of the above                                                                                                                |
| [research-notes/sources.md](research-notes/sources.md)               | Every source used, so claims can be double-checked or refreshed later                                                                                                   |




## How to use this

If you're skimming, this README is enough to get the gist. If you need to go deeper on a specific piece — the actual shard sizing math, the full cost model assumptions, or the week-by-week rollout plan — follow the links above.