# 📈 Scaling Strategy

## Current Architecture (Single Node)

The current Docker Compose setup runs all services on a single machine:
- 1 PostgreSQL instance
- 1 Redis instance
- 1 Backend API server (Uvicorn)
- 1 Frontend (Next.js)
- 1 Nginx reverse proxy

## Horizontal Scaling Path

### Phase 1: Multiple API Workers

```yaml
backend:
  deploy:
    replicas: 4
```

FastAPI with Uvicorn supports multiple worker processes. Scale horizontally behind Nginx load balancing.

### Phase 2: Database Scaling

```
                    ┌─────────────┐
                    │   PgBouncer  │  ← Connection pooling
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴──────┐  ┌─┴──────┐  ┌──┴────────┐
        │  Primary    │  │ Read   │  │  Read     │
        │  (Writes)   │  │ Replica│  │  Replica  │
        └────────────┘  └────────┘  └───────────┘
```

- **Read replicas** for query-heavy operations (restaurant listings, menu browsing)
- **PgBouncer** for connection pooling
- **Write primary** for orders, payments, user management

### Phase 3: Kubernetes Deployment

```yaml
# Each service becomes a K8s Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: slooze-backend
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
```

## Caching Strategy

### Current: Redis Cache Layer

```
Client → API → Redis Cache → Database
                  ↓ (miss)
              Database → Redis (set with TTL) → Client
```

### Cache Targets

| Resource | TTL | Strategy |
|----------|-----|----------|
| Restaurant listings | 5 min | Cache-aside |
| Menu items | 5 min | Cache-aside |
| User sessions | 60 min | JWT (stateless) |
| Dashboard stats | 30 sec | Cache-aside |

### Cache Invalidation

- **Write-through**: When a restaurant or menu item is updated, invalidate the cache key
- **TTL-based**: Cache entries expire after their configured TTL
- **Event-driven** (future): Use Redis pub/sub to broadcast invalidation events

## Async Workers (Future)

```
┌──────────┐     ┌─────────────┐     ┌──────────────┐
│  API      │────→│ Redis Queue  │────→│  Celery       │
│  Server   │     │  (Pub/Sub)   │     │  Worker       │
└──────────┘     └─────────────┘     └──────────────┘
```

### Use Cases

- **Email notifications** — Order confirmation, delivery updates
- **Payment processing** — Async payment gateway integration
- **Analytics** — Aggregate order data asynchronously
- **Report generation** — Dashboard data pre-computation

## Load Estimation

| Metric | Estimate |
|--------|----------|
| Concurrent users | 1,000 |
| Requests/second | 500 |
| Database connections | 50 pooled |
| Cache hit ratio target | 85%+ |
| API response time (p95) | <200ms |

## CDN Strategy

For the frontend:
- Static assets served via CDN (CloudFront/CloudFlare)
- Image optimization via Next.js Image component
- Restaurant and food images served from CDN

## Monitoring

- **Application**: Structured logging → ELK Stack / Datadog
- **Infrastructure**: Prometheus + Grafana
- **Errors**: Sentry
- **Performance**: APM (Application Performance Monitoring)
