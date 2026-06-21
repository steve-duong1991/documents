# In-Memory Balanced Trees

When data lives entirely in RAM and you need ordered maps or sets, binary tree variants — not B-Trees — are the usual choice. They optimize for **CPU cache** and **pointer navigation**, not disk pages.

> **Related:** Disk indexes → [§1 B-Trees and B+ Trees](01-b-trees-and-b-plus.md) · Decision flows → [§5 Decision guides](05-decision-guides.md)

---

## Binary Search Tree (BST)

| | |
|--|--|
| **Pros** | Simple; O(log n) average search/insert |
| **Cons** | Degenerates to O(n) on sorted input (linked-list shape) |
| **Use when** | Teaching, tiny sets, or when worst case is acceptable |

---

## AVL Tree

| | |
|--|--|
| **Pros** | Strict balance (heights differ ≤ 1); **fastest lookups** among balanced BSTs |
| **Cons** | More rotations on insert/delete than red-black |
| **Use when** | Read-heavy workloads; lookup latency matters more than write rate |

---

## Red-Black Tree

| | |
|--|--|
| **Pros** | Looser balance → **fewer rotations** on write; still O(log n). Used in `std::map`, Java `TreeMap`, Linux `rbtree` |
| **Cons** | Slightly deeper than AVL → marginally slower lookups |
| **Use when** | **General-purpose ordered map/set** with mixed read/write — default in many standard libraries |

---

## Splay Tree

| | |
|--|--|
| **Pros** | No extra balance fields; **recently accessed nodes move to root** (good for skewed access) |
| **Cons** | Amortized O(log n) but **worst single op can be O(n)**; poor for hard real-time guarantees |
| **Use when** | Caches, temporal locality, some network algorithms |

---

## Skip List

| | |
|--|--|
| **Pros** | O(log n) average search/insert; **easier concurrent updates** than rebalancing BSTs; used in LSM(Log-Structured Merge) memtables |
| **Cons** | More memory than BST (forward pointers); randomness or deterministic levels add complexity |
| **Use when** | Concurrent ordered maps, LevelDB/RocksDB memtables, Redis sorted sets (implementation detail) |

See complexity table → [06-amplification-and-related-topics.md](06-amplification-and-related-topics.md#complexity-cheat-sheet)

---

## B+ Tree vs in-memory balanced BST

| Aspect | B-Tree / B+ | Red-Black / AVL |
|--------|-------------|-----------------|
| Node width | Many keys per node | 1–3 keys typical |
| Optimized for | **Disk pages**, sequential leaf scan | **CPU cache**, pointers |
| Height | Very shallow (fanout 100–1000) | Deeper (fanout 2) |
| Range scan | Excellent (B+ leaf chain) | In-order traversal, more cache misses |
| Implementation cost | High (storage engine) | Moderate (stdlib) |
| Typical home | DB, filesystem | Language runtime, applications |

**Rule of thumb:** Everything in RAM and you need `map`/`set` → **Red-Black or AVL**.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| B+ tree for in-memory ordered map | Red-black / AVL / skip list |
| AVL when write-heavy | Red-black for fewer rotations |
| Splay tree for hard real-time | Bounded worst-case structure |
| BST without balancing | Always use balanced variant |
| Skip list when memory is tight | Red-black unless concurrency requires skip list |
