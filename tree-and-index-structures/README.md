# Trees and Index Structures Guide

A practical reference for tree data structures and storage indexes — B-Trees, B+ Trees, in-memory balanced trees, specialized trees, LSM trees, and when to use each.

Related: [postgresql-performance](../postgresql-performance/README.md) (PostgreSQL index types and tuning) · [high-throughput-systems](../high-throughput-systems/README.md) (LSM write path at scale)

---

## Table of contents

| # | Topic | Include file |
|---|-------|--------------|
| — | [Overview](#overview) | [includes/00-overview.md](includes/00-overview.md) |
| 1 | [B-Trees and B+ Trees](#1-b-trees-and-b-trees) | [includes/01-b-trees-and-b-plus.md](includes/01-b-trees-and-b-plus.md) |
| 2 | [In-memory balanced trees](#2-in-memory-balanced-trees) | [includes/02-in-memory-trees.md](includes/02-in-memory-trees.md) |
| 3 | [Specialized trees](#3-specialized-trees) | [includes/03-specialized-trees.md](includes/03-specialized-trees.md) |
| 4 | [LSM Trees](#4-lsm-trees) | [includes/04-lsm-trees.md](includes/04-lsm-trees.md) |
| 5 | [Decision guides and cheat sheets](#5-decision-guides-and-cheat-sheets) | [includes/05-decision-guides.md](includes/05-decision-guides.md) |
| 6 | [Amplification, complexity, and related topics](#6-amplification-complexity-and-related-topics) | [includes/06-amplification-and-related-topics.md](includes/06-amplification-and-related-topics.md) |

> **Tip:** Open [GUIDE.md](GUIDE.md) for the full combined document in one file.

---

## Overview

Tree families, B+ vs LSM storage camps, and default recommendations by use case.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. B-Trees and B+ Trees

On-disk indexes, pros/cons, hash comparison, and why databases use B+ trees.

See full details → [includes/01-b-trees-and-b-plus.md](includes/01-b-trees-and-b-plus.md)

---

## 2. In-Memory Balanced Trees

BST, AVL, Red-Black, Splay — when to use each in RAM.

See full details → [includes/02-in-memory-trees.md](includes/02-in-memory-trees.md)

---

## 3. Specialized Trees

Trie, heap, segment tree, R-Tree, KD-Tree, Merkle tree, and more.

See full details → [includes/03-specialized-trees.md](includes/03-specialized-trees.md)

---

## 4. LSM Trees

Log-structured merge trees — write path, compaction, LSM vs B+, real-world systems.

See full details → [includes/04-lsm-trees.md](includes/04-lsm-trees.md)

---

## 5. Decision Guides and Cheat Sheets

Mermaid decision flows for storage, in-memory maps, specialized queries, and LSM vs B+.

See full details → [includes/05-decision-guides.md](includes/05-decision-guides.md)

---

## 6. Amplification, Complexity, and Related Topics

Amplification metrics, clustered vs secondary indexes, complexity table, when NOT to use, glossary, and cross-links to PostgreSQL guides.

See full details → [includes/06-amplification-and-related-topics.md](includes/06-amplification-and-related-topics.md)

---

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | B-tree, GIN, partial, and covering indexes in practice |
| [high-throughput-systems](../high-throughput-systems/README.md) | Database throughput layer, when to consider LSM engines |
| [api-design-and-protection](../api-design-and-protection/README.md) | API caching and read-path design |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event store and append-heavy write paths |
| [database-connection-and-security](../database-connection-and-security/README.md) | Connection security is independent of index choice |
| [api-rate-limiting](../api-rate-limiting/README.md) | Overload protection when storage read path saturates |
| [deployment-strategies](../deployment-strategies/README.md) | Deploy when changing index strategy at scale |
