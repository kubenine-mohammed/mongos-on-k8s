# Sources

Notes and links gathered while researching this proposal (September 2026). Pricing figures are public list prices and change often — treat them as directional, not a quote.

## MongoDB operators on Kubernetes

- Percona Operator for MongoDB docs — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/
  - Sharding architecture — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/sharding.html
  - Backups overview — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/backups.html
  - Point-in-time recovery — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/backups-pitr.html
  - Restore (same cluster) — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/backups-restore.html
  - Restore (new cluster) — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/backups-restore-to-new-cluster.html
  - Scaling (shards, config servers, mongos) — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/scaling.html
  - Multi-cluster / multi-region replication — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/replication.html
  - Failover to a replica site — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/replication-failover.html
  - Comparison with other solutions — https://docs.percona.com/percona-operator-for-mongodb/1.23.0/compare.html
  - Limitations — https://github.com/percona/k8spsmdb-docs/blob/main/docs/limitations.md
- Percona blog, "MongoDB Operators: Features, Limitations, and Alternatives" — https://www.percona.com/blog/mongodb-operators-explained-features-limitations-and-open-source-alternatives/
- MongoDB Controllers for Kubernetes (MCK, successor to the Enterprise/Community operators) — https://github.com/mongodb/mongodb-kubernetes
- MongoDBCommunity resource spec — https://www.mongodb.com/docs/kubernetes/current/reference/k8s-operator-community-specification/
- Percona Community blog, multi-cluster MongoDB on GKE with MCS — https://percona.community/blog/2026/06/12/multi-cluster-mongodb-percona-operator/

## MongoDB Atlas pricing

- Atlas cluster configuration costs — https://www.mongodb.com/docs/atlas/billing/cluster-configuration-costs
- Atlas cluster additional settings (sharding, config servers) — https://www.mongodb.com/docs/atlas/cluster-additional-settings
- Atlas dedicated config server transition — https://www.mongodb.com/docs/atlas/transition-to-dedicated-config-servers/
- MongoDB official pricing page — https://www.mongodb.com/pricing
- Third-party pricing breakdown, go-cloud.io — https://go-cloud.io/mongodb-pricing/

## AWS pricing (EKS / EC2 / EBS / S3)

- Amazon EKS pricing — https://aws.amazon.com/eks/pricing/
- EKS pricing explained (2026) — https://atmosly.com/blog/eks-pricing
- EKS pricing breakdown — https://cloudburn.io/blog/amazon-eks-pricing
- EKS cost optimization guide — https://www.cloudzero.com/blog/eks-pricing/
- r6i.large pricing reference — https://calculator.holori.com/aws/ec2/r6i.large/us-east-1
- Amazon EBS pricing — https://aws.amazon.com/ebs/pricing/
- Amazon EBS volume types — https://aws.amazon.com/ebs/volume-types/
- EBS pricing guide — https://cloudchipr.com/blog/aws-ebs-pricing
- AWS Backup pricing — https://aws.amazon.com/backup/pricing/

## What we still need directly from the customer

These aren't available publicly and materially change the numbers in `docs/cost-comparison.md`:

- Current Atlas invoice (last 3 months) and cluster configuration (tier, shard count, region, backup settings)
- Actual data size today and realistic growth rate over the next 12-24 months
- Peak IOPS / throughput / connection counts (for right-sizing nodes, not just storage)
- Required RPO/RTO and any compliance obligations (e.g. data residency, encryption standards)
