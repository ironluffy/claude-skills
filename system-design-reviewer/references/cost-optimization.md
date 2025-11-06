# Cloud Cost Optimization Guide

Quick reference for reducing cloud infrastructure costs.

## Resource Right-Sizing

### Compute Instances

**Common Over-Provisioning Signs:**
- CPU utilization consistently <20%
- Memory usage consistently <40%
- No traffic spikes requiring headroom

**Action**: Downgrade instance types, enable auto-scaling

**Savings**: 30-50% on compute costs

### Database Instances

**Optimization Strategies:**
- Add connection pooling (PgBouncer, ProxySQL) → downgrade instance
- Implement read replicas for read-heavy workloads
- Use database caching to reduce query load
- Separate OLTP and OLAP workloads

**Savings**: 20-40% on database costs

## Auto-Scaling Policies

```yaml
# Scale based on actual demand
min_instances: 2
max_instances: 10
target_cpu: 70%    # Scale up at 70% CPU
scale_up_cooldown: 300    # Wait 5 min before scaling up again
scale_down_cooldown: 600  # Wait 10 min before scaling down
```

**Savings**: 40-60% during low-traffic periods

## Serverless Migration

**Good Candidates for Serverless:**
- APIs with unpredictable traffic
- Scheduled tasks/cron jobs
- Webhook handlers
- Low-traffic applications (<1M requests/month)

**Cost Comparison:**
- EC2 t3.small: $15/month (always running)
- Lambda: $0-5/month (pay per invocation)

**Savings**: 70-100% for low-traffic workloads

## Storage Optimization

### S3 Lifecycle Policies

```json
{
  "Rules": [{
    "Filter": {"Prefix": "logs/"},
    "Transitions": [{
      "Days": 30,
      "StorageClass": "STANDARD_IA"
    }, {
      "Days": 90,
      "StorageClass": "GLACIER"
    }],
    "Expiration": {"Days": 365}
  }]
}
```

**Cost Tiers (per GB/month):**
- Standard: $0.023
- Infrequent Access: $0.0125 (46% cheaper)
- Glacier: $0.004 (83% cheaper)

**Savings**: 50-80% on storage costs

### Database Storage

- Archive old records to cheaper storage
- Compress large BLOB/TEXT columns
- Partition large tables by date
- Delete unnecessary indexes

## Reserved Instances & Savings Plans

### When to Use

- Predictable workloads (>1 year)
- Production databases (always running)
- Base capacity (min instances in auto-scaling group)

### Commitment Options

- **1-Year**: 20-30% discount
- **3-Year**: 40-60% discount
- **Convertible**: 10-20% less savings, more flexibility

**ROI**: Payback period of 3-6 months

## Spot Instances

**Use For:**
- Batch processing jobs
- CI/CD build agents
- Development/testing environments
- Fault-tolerant distributed systems

**Savings**: 70-90% vs on-demand pricing

**Risk**: Can be terminated with 2-minute warning

## Data Transfer Optimization

**Cost Reducers:**
- Use CloudFront/CDN to reduce origin data transfer
- Keep traffic within same region/availability zone
- Compress responses (gzip/brotli)
- Use VPC endpoints for AWS service communication

**Typical Costs:**
- Within AZ: Free
- Cross-AZ: $0.01/GB
- Cross-Region: $0.02/GB
- Internet Egress: $0.09/GB

**Savings**: 50-90% on data transfer

## Cost Monitoring

### Essential Metrics

- Cost per request
- Cost per user
- Cost per feature
- Month-over-month growth rate
- Cost allocation by team/project

### Budget Alerts

```yaml
budget:
  amount: 500  # USD per month
  alerts:
    - threshold: 80%    # Alert at $400
      notify: team@company.com
    - threshold: 100%   # Alert at $500
      notify: management@company.com
```

## Quick Wins Checklist

- [ ] Delete unused resources (old snapshots, unattached volumes, orphaned load balancers)
- [ ] Right-size over-provisioned instances
- [ ] Implement storage lifecycle policies
- [ ] Enable auto-scaling for variable workloads
- [ ] Purchase reserved instances for base capacity
- [ ] Use spot instances for fault-tolerant workloads
- [ ] Add CloudFront/CDN for static content
- [ ] Implement connection pooling for databases
- [ ] Set up cost allocation tags
- [ ] Configure budget alerts

**Expected Combined Savings**: 30-50% of total cloud spend
