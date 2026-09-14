#!/usr/bin/env python3
"""
Cost model: MongoDB Atlas (dedicated, sharded) vs self-hosted Percona
Operator for MongoDB on AWS EKS.

This is a small, dependency-free calculator so the numbers in
cost-comparison.md can be regenerated the moment we have the customer's
real Atlas invoice or a firmer sizing estimate. Every input constant below
is a public list price gathered in September 2026 (see research-notes/sources.md)
-- swap them out for actuals as soon as they're available.

Usage:
    python3 cost_model.py
"""

from dataclasses import dataclass, field

HOURS_PER_MONTH = 730

# ---------------------------------------------------------------------------
# Atlas list pricing (per data-bearing node, per hour) -- September 2026
# ---------------------------------------------------------------------------
ATLAS_TIER_HOURLY = {
    "M40": 1.04,
    "M50": 2.00,
    "M60": 3.95,
    "M80": 7.30,
    "M140": 10.99,
    "M200": 14.59,
    "M300": 21.85,
}
ATLAS_CONFIG_SERVER_HOURLY = 0.35   # dedicated config server replica set (3 nodes), approx list rate for small tier
ATLAS_BACKUP_PCT_OF_COMPUTE = 0.06  # continuous cloud backup, rule-of-thumb % of cluster compute spend
ATLAS_SUPPORT_PCT = 0.0             # assume support plan already included/negotiated; set >0 to model Enterprise support


@dataclass
class AtlasScenario:
    name: str
    tier: str
    shards: int
    nodes_per_shard: int = 3
    dedicated_config_server: bool = True

    def monthly_cost(self):
        node_rate = ATLAS_TIER_HOURLY[self.tier]
        data_nodes = self.shards * self.nodes_per_shard
        compute = data_nodes * node_rate * HOURS_PER_MONTH
        config_cost = 0.0
        if self.dedicated_config_server:
            config_cost = 3 * ATLAS_CONFIG_SERVER_HOURLY * HOURS_PER_MONTH
        backup = (compute + config_cost) * ATLAS_BACKUP_PCT_OF_COMPUTE
        support = (compute + config_cost) * ATLAS_SUPPORT_PCT
        total = compute + config_cost + backup + support
        return {
            "compute": compute,
            "config_servers": config_cost,
            "backup": backup,
            "support": support,
            "total": total,
        }


# ---------------------------------------------------------------------------
# AWS self-hosted pricing (us-east-1, on-demand) -- September 2026
# ---------------------------------------------------------------------------
EKS_CONTROL_PLANE_HOURLY = 0.10

EC2_HOURLY = {
    "r6i.large": 0.126,     # 2 vCPU / 16 GB   -> mongos
    "r6i.xlarge": 0.252,    # 4 vCPU / 32 GB   -> config servers
    "r6i.2xlarge": 0.504,   # 8 vCPU / 64 GB   -> shard data nodes
}
RESERVED_DISCOUNT = {
    "on_demand": 1.0,
    "1yr_no_upfront": 0.72,   # approx effective multiplier vs on-demand
    "3yr_no_upfront": 0.55,
}

EBS_GP3_PER_GB_MONTH = 0.08
S3_STANDARD_PER_GB_MONTH = 0.023
MISC_NETWORKING_MONTHLY = 300  # NAT gateways, load balancer, cross-AZ transfer, rough allowance
PMM_MONITORING_NODE_HOURLY = EC2_HOURLY["r6i.large"]  # one node for PMM/monitoring stack

# Ops overhead: engineering/SRE time to run the self-hosted cluster.
# Presented separately so it's never hidden inside "infra savings".
SRE_FTE_FRACTION = 0.5           # portion of one engineer's time
SRE_MONTHLY_LOADED_COST = 12000  # fully loaded monthly cost of one FTE, adjust to customer's market


@dataclass
class SelfHostedScenario:
    name: str
    shards: int
    shard_node_type: str = "r6i.2xlarge"
    shard_storage_gb_per_node: int = 1300
    config_node_type: str = "r6i.xlarge"
    config_storage_gb: int = 100
    mongos_count: int = 2
    mongos_node_type: str = "r6i.large"
    backup_storage_gb: int = 1000
    commitment: str = "1yr_no_upfront"

    def monthly_cost(self):
        discount = RESERVED_DISCOUNT[self.commitment]

        shard_nodes = self.shards * 3
        shard_compute = shard_nodes * EC2_HOURLY[self.shard_node_type] * HOURS_PER_MONTH * discount
        shard_storage = shard_nodes * self.shard_storage_gb_per_node * EBS_GP3_PER_GB_MONTH

        config_compute = 3 * EC2_HOURLY[self.config_node_type] * HOURS_PER_MONTH * discount
        config_storage = 3 * self.config_storage_gb * EBS_GP3_PER_GB_MONTH

        mongos_compute = self.mongos_count * EC2_HOURLY[self.mongos_node_type] * HOURS_PER_MONTH * discount

        monitoring_compute = PMM_MONITORING_NODE_HOURLY * HOURS_PER_MONTH * discount

        eks_control_plane = EKS_CONTROL_PLANE_HOURLY * HOURS_PER_MONTH

        backup_storage = self.backup_storage_gb * S3_STANDARD_PER_GB_MONTH

        infra_total = (
            shard_compute + shard_storage
            + config_compute + config_storage
            + mongos_compute
            + monitoring_compute
            + eks_control_plane
            + backup_storage
            + MISC_NETWORKING_MONTHLY
        )

        ops_overhead = SRE_FTE_FRACTION * SRE_MONTHLY_LOADED_COST

        return {
            "shard_compute": shard_compute,
            "shard_storage": shard_storage,
            "config_compute": config_compute,
            "config_storage": config_storage,
            "mongos_compute": mongos_compute,
            "monitoring_compute": monitoring_compute,
            "eks_control_plane": eks_control_plane,
            "backup_storage": backup_storage,
            "networking_misc": MISC_NETWORKING_MONTHLY,
            "infra_total": infra_total,
            "ops_overhead": ops_overhead,
            "total_with_ops": infra_total + ops_overhead,
        }


def fmt(n):
    return f"${n:,.0f}"


def print_scenario(label, atlas: AtlasScenario, self_hosted: SelfHostedScenario):
    a = atlas.monthly_cost()
    s = self_hosted.monthly_cost()

    print(f"\n=== {label} ===")
    print(f"Atlas ({atlas.tier} x {atlas.shards} shards x {atlas.nodes_per_shard} nodes):")
    print(f"  compute:        {fmt(a['compute'])}/mo")
    print(f"  config servers: {fmt(a['config_servers'])}/mo")
    print(f"  backup:         {fmt(a['backup'])}/mo")
    print(f"  TOTAL:          {fmt(a['total'])}/mo   ({fmt(a['total'] * 12)}/yr)")

    print(f"\nSelf-hosted EKS ({self_hosted.shards} shards, {self_hosted.commitment}):")
    print(f"  shard compute+storage: {fmt(s['shard_compute'] + s['shard_storage'])}/mo")
    print(f"  config servers:        {fmt(s['config_compute'] + s['config_storage'])}/mo")
    print(f"  mongos + monitoring:   {fmt(s['mongos_compute'] + s['monitoring_compute'])}/mo")
    print(f"  EKS + networking:      {fmt(s['eks_control_plane'] + s['networking_misc'])}/mo")
    print(f"  backup storage (S3):   {fmt(s['backup_storage'])}/mo")
    print(f"  INFRA TOTAL:           {fmt(s['infra_total'])}/mo   ({fmt(s['infra_total'] * 12)}/yr)")
    print(f"  + ops overhead ({SRE_FTE_FRACTION} FTE): {fmt(s['ops_overhead'])}/mo")
    print(f"  TOTAL incl. ops:       {fmt(s['total_with_ops'])}/mo   ({fmt(s['total_with_ops'] * 12)}/yr)")

    infra_savings_pct = (1 - s["infra_total"] / a["total"]) * 100
    total_savings_pct = (1 - s["total_with_ops"] / a["total"]) * 100
    print(f"\n  Infra-only savings vs Atlas: {infra_savings_pct:.0f}%")
    print(f"  Savings incl. ops overhead:  {total_savings_pct:.0f}%")


if __name__ == "__main__":
    print_scenario(
        "Scenario A: ~2 TB, 2 shards",
        AtlasScenario(name="2TB", tier="M60", shards=2, dedicated_config_server=False),
        SelfHostedScenario(name="2TB", shards=2, shard_storage_gb_per_node=1300, backup_storage_gb=800),
    )

    print_scenario(
        "Scenario B: ~5 TB, 4 shards",
        AtlasScenario(name="5TB", tier="M60", shards=4, dedicated_config_server=True),
        SelfHostedScenario(name="5TB", shards=4, shard_storage_gb_per_node=1600, backup_storage_gb=2000),
    )
