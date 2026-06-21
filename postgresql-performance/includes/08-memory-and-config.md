# Memory and Configuration Tuning

PostgreSQL performance depends heavily on memory settings and planner cost constants. Tune once at deploy, then adjust based on workload evidence.

> **Related:** Measure before tuning → [§1 Measurement](01-measurement.md) · Wrong plans on SSD → [§5 Statistics and the planner](05-statistics-and-planner.md) · Connection limits vs memory → [§7 Connection management](07-connection-management.md)

## Key parameters

| Parameter | Rule of thumb | Purpose |
|-----------|---------------|---------|
| **`shared_buffers`** | ~25% of RAM (cap ~8–16 GB) | PostgreSQL page cache |
| **`effective_cache_size`** | ~50–75% of total RAM | Tells planner how much OS cache exists |
| **`work_mem`** | 4–64 MB per operation | Sorts, hashes, merge joins |
| **`maintenance_work_mem`** | 256 MB – 2 GB | Index builds, vacuum, `CREATE INDEX` |
| **`random_page_cost`** | 1.1–1.5 on SSD/NVMe | Planner index vs seq scan preference |
| **`effective_io_concurrency`** | 200+ on NVMe | Concurrent read prefetch |
| **`max_parallel_workers_per_gather`** | 2–4 | Parallel sequential scans/aggregates |

## work_mem warning

`work_mem` is **per sort/hash operation per connection**, not global.

```text
100 connections × 4 hash operations × 64 MB work_mem = up to 25 GB
```

Set conservatively globally; raise per-session for reporting:

```sql
SET work_mem = '256MB';  -- reporting session only
```

## Example production baseline (16 GB RAM, SSD)

```text
shared_buffers = 4GB
effective_cache_size = 12GB
work_mem = 16MB
maintenance_work_mem = 1GB
random_page_cost = 1.1
effective_io_concurrency = 200
max_parallel_workers_per_gather = 2
max_connections = 200
```

Adjust for your RAM and workload — these are starting points, not gospel.

## WAL and checkpoint (write-heavy)

| Parameter | Notes |
|-----------|-------|
| **`wal_buffers`** | Often 16–64 MB on busy systems |
| **`checkpoint_completion_target`** | 0.9 — spread checkpoint IO |
| **`max_wal_size`** | Higher = fewer checkpoints, more WAL disk |

Spiky write latency during checkpoints? Increase `max_wal_size` and tune checkpoint settings.

## When to tune

| Workload signal | Parameter to adjust |
|-----------------|---------------------|
| Planner chooses seq scan on SSD | Lower `random_page_cost` |
| Sorts spill to disk (`external merge`) | Raise `work_mem` (carefully) |
| Slow index builds | Raise `maintenance_work_mem` |
| Large table scans on analytics | Raise `max_parallel_workers_per_gather` |
| OOM under load | Lower `work_mem`; add pooling |

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| High global `work_mem` | OOM under concurrent sorts/hashes | Conservative global; raise per-session for reports |
| `shared_buffers` at 80% of RAM | Starves OS page cache | ~25% of RAM, cap 8–16 GB |
| Copy tuning from blog without workload match | Wrong trade-offs | Change one parameter; measure with `EXPLAIN` and metrics |
| Max parallelism on OLTP | Contention on short queries | Low `max_parallel_workers_per_gather` for OLTP |
| Ignore temp file spikes | Sorts spilling to disk unnoticed | Monitor temp files; tune `work_mem` for heavy queries |

## When NOT to tune blindly

- Don't set `shared_buffers` to 80% of RAM — OS cache matters
- Don't max out parallelism on OLTP — hurts concurrent short queries
- Don't change many parameters at once — measure one change at a time

## Managed databases

RDS, Cloud SQL, Supabase, and Azure expose these via parameter groups. Some require reboot; others are dynamic. Check provider docs for limits.

## Best practices

- Document your baseline and why each value was chosen
- Use **`pg_tune`** or similar calculators as a starting point only
- Revisit after major workload changes (10× data growth, new reporting)
- Monitor temp file usage — sign that `work_mem` is too low
