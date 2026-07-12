# Web Performance

> **Related:** Rendering mode choice → [§2](02-rendering-tradeoffs.md) · Edge/CDN(Content Delivery Network) → [HTS §2 Entry and edge](../../high-throughput-systems/includes/02-entry-and-edge.md) · Caching layers → [HTS §4](../../high-throughput-systems/includes/04-caching-layers.md) · BFF(Backend for Frontend) aggregation budgets → [§3](03-bff-ownership.md)

## At a glance

| Vital | What users feel | Engineering levers |
|-------|-----------------|--------------------|
| **LCP(Largest Contentful Paint)** | Main content appeared | SSR(Server-Side Rendering)/SSG(Static Site Generation), image priority, font strategy, TTFB |
| **INP(Interaction to Next Paint)** | UI reacts to input | Less main-thread JS, break long tasks |
| **CLS(Cumulative Layout Shift)** | Layout jumps | Sizes on images/embeds; reserve space |

**Rule of thumb:** Set **budgets in CI(Continuous Integration)** (bundle bytes + lab vitals); field data (CrUX/RUM) settles arguments.

## Performance path

```mermaid
flowchart LR
    Edge[CDN / edge cache] --> Origin[BFF / app origin]
    Origin --> HTML[HTML + critical CSS]
    HTML --> Assets[JS / images / fonts]
    Assets --> Hydrate[Hydrate / islands]
    Hydrate --> RUM[RUM vitals]
```

## Caching headers (practical)

| Resource | Cache-Control sketch |
|----------|----------------------|
| Fingerprinted JS/CSS | `public, max-age=31536000, immutable` |
| HTML (public SSG) | `public, max-age=60, s-maxage=300` (tune) |
| HTML (personalized) | `private, no-store` or short private |
| BFF JSON (user-specific) | `private, no-store` |
| BFF JSON (public fragment) | Short `s-maxage` + ETag |

Wrong CDN(Content Delivery Network) caching of personalized HTML is a **security bug**, not just a perf smell.

## Asset strategy

| Area | Do |
|------|----|
| JS | Code-split by route; defer non-critical |
| Images | Modern formats; width/height; responsive `srcset` |
| Fonts | Subset; `font-display: swap` or optional; preconnect |
| Third parties | Load after interactive; tag managers carefully |
| API(Application Programming Interface) chatter | Aggregate in BFF; avoid waterfalls |

## Budgets example

| Metric | Budget (example SaaS app) |
|--------|---------------------------|
| Route JS (gzipped) | ≤ 200 KB initial |
| LCP (lab p75) | ≤ 2.5s on mid mobile |
| INP (field p75) | ≤ 200ms |
| BFF home fan-out | ≤ 300ms p95 at edge region |

Tune to product; publish budgets next to the design system.

## Measuring

| Layer | Tooling |
|-------|---------|
| Lab | Lighthouse CI on PRs for key routes |
| Field | RUM + CrUX for real devices |
| Server | TTFB, BFF dependency timings |
| CDN | Hit ratio, origin offload |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Optimizing micro-benchmarks, ignoring LCP | Hero image + TTFB first |
| Caching logged-in HTML on shared CDN | Private / no-store |
| Blocking render on A/B and analytics | Async after paint |
| Giant design-system import on every page | Tree-shake / per-primitive imports |
| No owner for vitals regressions | Budget gate in CI |