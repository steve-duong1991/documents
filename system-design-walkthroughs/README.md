# System Design Walkthroughs Guide

End-to-end designs for classic interview problems and their real production shapes — requirements, back-of-envelope math, architecture, data model, bottlenecks, and heavy cross-links into the rest of this corpus instead of re-deriving caching, async, or rate-limiting from scratch.

Related: [high-throughput-systems](../high-throughput-systems/README.md) (throughput order and layers) · [api-design-and-protection](../api-design-and-protection/README.md) (gateway, async, idempotency) · [architecture-decisions](../architecture-decisions/README.md) (tradeoff frameworks, ADRs)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [How to approach a design problem](includes/01-how-to-approach.md) |
| 2 | [URL shortener](includes/02-url-shortener.md) |
| 3 | [News feed](includes/03-news-feed.md) |
| 4 | [Chat and presence](includes/04-chat-and-presence.md) |
| 5 | [Ride-sharing and geolocation](includes/05-ride-sharing-geo.md) |
| 6 | [Distributed rate limiter](includes/06-distributed-rate-limiter.md) |
| 7 | [Notification pipeline](includes/07-notification-pipeline.md) |
| 8 | [Search autocomplete](includes/08-search-autocomplete.md) |
| 9 | [Video streaming basics](includes/09-video-streaming-basics.md) |
| 10 | [Decision guide](includes/10-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

---

## Reading paths

| If you are… | Read in order |
|--------------|----------------|
| **Prepping for interviews** | [§1 how to approach](includes/01-how-to-approach.md) → 3–4 walkthroughs covering different bottleneck classes → [§10 decision guide](includes/10-decision-guide.md) scenario table |
| **Writing a design doc for a new feature** | [§10 decision guide](includes/10-decision-guide.md) to classify the problem → closest walkthrough → follow its deep-dive links for the parts that matter to your NFRs |
| **Reviewing someone else's design** | [§10 decision guide](includes/10-decision-guide.md) rollout checklist → confirm requirements, estimates, and a named bottleneck are present |
| **Fan-out / real-time systems** | [§3 news feed](includes/03-news-feed.md) → [§4 chat and presence](includes/04-chat-and-presence.md) → [§7 notification pipeline](includes/07-notification-pipeline.md) |
| **Read-latency-critical systems** | [§2 URL shortener](includes/02-url-shortener.md) → [§8 search autocomplete](includes/08-search-autocomplete.md) → [high-throughput-systems §4 caching](../high-throughput-systems/includes/04-caching-layers.md) |
| **Infra/platform problems (limits, geo, media)** | [§6 distributed rate limiter](includes/06-distributed-rate-limiter.md) → [§5 ride-sharing geo](includes/05-ride-sharing-geo.md) → [§9 video streaming basics](includes/09-video-streaming-basics.md) |

---

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | Caching, async queues/workers, backpressure, multi-region — the mechanics every walkthrough's bottleneck fix links back to |
| [api-design-and-protection](../api-design-and-protection/README.md) | Gateway architecture, async job/webhook patterns, idempotency, object storage/uploads |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limiter algorithms and deployment layers — the depth behind [§6 distributed rate limiter](includes/06-distributed-rate-limiter.md) |
| [postgresql-performance](../postgresql-performance/README.md) | Partitioning, replication, sharding terminology used across the fan-out and geo walkthroughs |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, idempotency, distributed locks, delivery semantics |
| [data-platforms](../data-platforms/README.md) | Search systems, Redis roles, caching coherence beyond one OLTP(Online Transaction Processing) database |
| [apache-kafka](../apache-kafka/README.md) | Event bus product choice behind fan-out and notification pipelines |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Outbox, sagas, and CQRS(Command Query Responsibility Segregation) read models referenced in the feed, chat, and notification walkthroughs |
| [architecture-decisions](../architecture-decisions/README.md) | Tradeoff frameworks and ADRs for writing up the decision after a walkthrough |
| [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) | Realtime transport choice (WebSocket/SSE(Server-Sent Events)/polling) behind the chat and presence walkthrough |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | Trie, radix, and spatial tree structures behind autocomplete and ride-sharing geo |