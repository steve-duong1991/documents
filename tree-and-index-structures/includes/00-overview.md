# Overview — Trees and Index Structures

Trees organize data hierarchically. The right structure depends on **access pattern**, **memory hierarchy**, **mutation rate**, and **query types** — not on which name sounds most impressive.

> **Related:**
> - PostgreSQL index types (B-tree, GIN(Generalized Inverted Index), GiST, BRIN(Block-Range Index)) → [postgresql-performance/includes/02-indexing.md](../../postgresql-performance/includes/02-indexing.md)
> - Amplification, complexity, glossary → [06-amplification-and-related-topics.md](06-amplification-and-related-topics.md)

## Tree families at a glance

| Tree family | Core idea | Sweet spot |
|-------------|-----------|------------|
| **BST variants** | In-memory, pointer-heavy, O(log n) search | RAM, moderate size |
| **B-Tree / B+ Tree** | Wide nodes, few disk seeks | Databases, file systems, SSDs |
| **LSM(Log-Structured Merge) Tree** | Append + merge sorted files | Write-heavy KV, time-series, distributed DBs |
| **Trie / Radix** | Prefix on edges | Strings, IPs, routing |
| **Heap** | Parent ≥/≤ children | Priority queues, top-K |
| **Segment / Fenwick** | Range aggregates | Range sum/min on arrays |
| **R-Tree / KD-Tree** | Spatial partitioning | Maps, nearest neighbor |

## Two big storage-engine camps

Most production storage falls into one of two designs:

| | **B+ Tree** | **LSM Tree** |
|--|-------------|--------------|
| **Write model** | Update pages in place | Append to WAL(Write-Ahead Log) + memtable; merge later |
| **Read model** | Few page lookups | Memtable + filters + possibly many files |
| **Range scans** | Excellent (linked leaves) | Good with leveled compaction; weaker at L0 |
| **Typical home** | PostgreSQL, InnoDB, SQLite | RocksDB, Cassandra, Scylla, HBase |

## Default recommendations

| Need | Start here |
|------|------------|
| SQL(Structured Query Language) index, pagination, `BETWEEN` | **B+ Tree** |
| Only `WHERE id = ?`, no sort | **Hash index** (if engine supports it) |
| In-app ordered map | **Red-Black Tree** (default) or **AVL** (lookup-critical) |
| Autocomplete / IP longest prefix | **Trie** or **Radix tree** |
| Job scheduler / event queue | **Heap** |
| Range sum on an array index | **Fenwick** or **Segment tree** |
| Points in a map rectangle | **R-Tree** |
| Closest point in 2D/3D | **KD-Tree** |
| Verify content without full download | **Merkle tree** |
| Write-heavy logs, metrics, KV at scale | **LSM Tree** |

## Document map

| # | Topic | File |
|---|-------|------|
| 1 | B-Trees and B+ Trees | [01-b-trees-and-b-plus.md](01-b-trees-and-b-plus.md) |
| 2 | In-memory balanced trees | [02-in-memory-trees.md](02-in-memory-trees.md) |
| 3 | Specialized trees | [03-specialized-trees.md](03-specialized-trees.md) |
| 4 | LSM Trees | [04-lsm-trees.md](04-lsm-trees.md) |
| 5 | Decision guides and cheat sheets | [05-decision-guides.md](05-decision-guides.md) |
| 6 | Amplification, complexity, related topics | [06-amplification-and-related-topics.md](06-amplification-and-related-topics.md) |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Pick LSM for read-heavy OLTP SQL | B+ tree (PostgreSQL, InnoDB) |
| Use B+ tree for in-app ordered map in RAM | Red-black / AVL |
| Trie for numeric primary-key lookups | B+ tree or hash |
| Ignore read/write amplification trade-offs | See [§6](06-amplification-and-related-topics.md) |
| Choose structure by name, not access pattern | Use [§5 decision guides](05-decision-guides.md) |
