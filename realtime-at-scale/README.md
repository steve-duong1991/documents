# Realtime at Scale Guide

A practical reference for pushing live data to millions of concurrent clients — connection fan-out architecture, pub/sub backplanes, presence/typing systems, and CRDT(Conflict-free Replicated Data Type)/OT(Operational Transformation) for collaborative editing.

Related: [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) (client transport UX) · [api-design-and-protection](../api-design-and-protection/README.md) (HTTP(Hypertext Transfer Protocol) streaming contracts) · [high-throughput-systems](../high-throughput-systems/README.md) (broker throughput)

> **Scope:** This guide owns **fan-out architecture** — how one event reaches millions of open connections, and the backplane, presence, and conflict-resolution mechanics behind it. Client-side transport choice and reconnect UX → [fullstack-bff-and-clients §5](../fullstack-bff-and-clients/includes/05-realtime-ux.md). HTTP(Hypertext Transfer Protocol) streaming/long-poll contract shape → [api-design-and-protection §10C](../api-design-and-protection/includes/10C-async-streaming.md).

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Connection fan-out at scale](includes/01-connection-fanout.md) |
| 2 | [Pub/sub backplanes](includes/02-pubsub-backplanes.md) |
| 3 | [Presence and typing indicators](includes/03-presence-and-typing.md) |
| 4 | [CRDT and OT for collaborative editing](includes/04-crdt-and-ot.md) |
| 5 | [Decision guide](includes/05-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Scaling WebSockets for the first time** | Overview → §1 Connection fan-out → §2 Pub/sub backplanes |
| **Choosing a backplane** | §2 Pub/sub backplanes → §5 Decision guide |
| **Building presence / "who's online"** | §3 Presence and typing → [fullstack §5](../fullstack-bff-and-clients/includes/05-realtime-ux.md) |
| **Building a collaborative editor** | §4 CRDT and OT → §5 Decision guide |
| **Picking a transport for a UI feature** | [fullstack-bff-and-clients §5](../fullstack-bff-and-clients/includes/05-realtime-ux.md) → [api-design §10C](../api-design-and-protection/includes/10C-async-streaming.md) → this guide's §1–§2 |

---

## See also

| Guide | Topics |
|-------|--------|
| [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) | Transport choice, reconnect UX, BFF(Backend for Frontend) socket termination |
| [api-design-and-protection](../api-design-and-protection/README.md) | Streaming/long-poll contracts, webhooks, async job APIs |
| [high-throughput-systems](../high-throughput-systems/README.md) | Message brokers, backpressure, observability at scale |
| [apache-kafka](../apache-kafka/README.md) | Kafka as a backplane: partitions, consumer groups, retention |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, bulkheads for connection servers |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | CRDT/OT ops as an event log; projections for read state |
| [data-platforms](../data-platforms/README.md) | Redis roles beyond pub/sub — caching, rate limits |
| [deployment-strategies](../deployment-strategies/README.md) | Rolling connection servers without mass client drop |
| [sre-and-incidents](../sre-and-incidents/README.md) | Reconnect storms as an incident class |
| [finops-and-cost](../finops-and-cost/README.md) | Cost per open connection; backplane spend |