# Specialized Trees

Not every problem is “sorted key lookup.” These structures optimize for prefixes, priorities, ranges, space, or integrity proofs.

> **Related:** B+ / LSM(Log-Structured Merge) storage → [§1](01-b-trees-and-b-plus.md), [§4](04-lsm-trees.md) · Decision guide → [§5](05-decision-guides.md)

---

## Trie (Prefix Tree)

| | |
|--|--|
| **Pros** | O(key length) lookup; natural **prefix search**, autocomplete, longest prefix match |
| **Cons** | Memory-heavy (many nodes); poor for dense random keys unless compressed |
| **Use when** | Dictionaries, IP routing, URL/path matching, autocomplete |

---

## Radix Tree / Patricia Trie

| | |
|--|--|
| **Pros** | **Compressed trie** — fewer nodes for sparse/long keys |
| **Cons** | More complex; still key-length dependent |
| **Use when** | Linux kernel routing, memory-efficient string indexes |

---

## Heap (Binary / Binomial / Fibonacci)

| | |
|--|--|
| **Pros** | O(1) min/max; O(log n) insert/extract; simple array layout |
| **Cons** | Not a search structure — no arbitrary key lookup |
| **Use when** | Priority queues, schedulers, Dijkstra, top-K streaming |

---

## Segment Tree / Fenwick Tree (BIT)

| | |
|--|--|
| **Pros** | Range query + point/range update in O(log n) |
| **Cons** | Fixed underlying array; not a general key-value store |
| **Use when** | Range sum/min/max, competitive programming, time-series rollups |

---

## R-Tree (and variants)

| | |
|--|--|
| **Pros** | Indexes **multi-dimensional bounding boxes**; good for spatial queries |
| **Cons** | Heuristic splits; quality depends on data distribution |
| **Use when** | GIS, PostGIS, game spatial indexes, “find objects in this rectangle” |

---

## KD-Tree / Ball Tree

| | |
|--|--|
| **Pros** | Nearest-neighbor and range search in k dimensions |
| **Cons** | Degrades in high dimensions (“curse of dimensionality”) |
| **Use when** | Low-dimensional NN search, ML (small k), point clouds |

---

## Merkle Tree

| | |
|--|--|
| **Pros** | O(log n) proof that a leaf belongs to a root hash |
| **Cons** | Not for general lookup; built for integrity |
| **Use when** | Git, blockchains, distributed sync, content-addressed storage |

---

## Quick reference

| Operation dominates | Structure |
|---------------------|-----------|
| Priority / scheduling | Heap |
| Range aggregates on an array | Segment tree / Fenwick |
| Nearest neighbor (low dim) | KD-Tree / Ball tree |
| Integrity proofs | Merkle tree |
| String prefix / longest match | Trie / Radix |

## Production signals (when to pick this)

| Structure | Typical production use | Usually not in your DB layer |
|-----------|------------------------|------------------------------|
| Trie / Radix | IP routing tables, URL/path routers, autocomplete indexes | PostgreSQL default indexes |
| Heap | Job schedulers, priority queues inside workers | General row lookup |
| Segment / Fenwick | In-process range aggregates on bounded arrays | Disk-backed analytics at scale |
| KD / Ball tree | ML nearest-neighbor (Faiss, scikit pipelines) | SQL(Structured Query Language) `ORDER BY distance` on millions of rows |
| R-tree | GIS (`PostGIS`), spatial indexes on maps | Plain B+ on scalar columns |
| Merkle tree | Git, blockchains, content-addressed sync proofs | Application CRUD indexes |

**Rule of thumb:** Default to **B+ (PostgreSQL)** or **LSM (Cassandra, RocksDB)** for persistence. Specialized trees appear in **libraries, gateways, or search/ML services** — see [§5 Decision guides](05-decision-guides.md).

## Common mistakes

| Mistake | Fix |
|---------|-----|
| B+ tree for autocomplete prefix search | Trie or radix tree |
| Heap when you need arbitrary key lookup | Ordered map (red-black) or hash |
| R-tree for 1D sorted keys | B+ tree |
| KD-tree in high dimensions | Different ANN(Approximate Nearest Neighbor) approach or dimension reduction |
| Merkle tree for general indexing | Use for integrity proofs only |