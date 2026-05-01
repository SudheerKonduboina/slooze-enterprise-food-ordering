# 🏗️ Architecture

## High-Level Architecture

The Slooze Food Ordering Platform follows a **layered clean architecture** pattern with strict separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                     NGINX REVERSE PROXY                      │
│                    (Port 8080 / Port 80)                      │
├──────────────────────────┬──────────────────────────────────┤
│     Next.js Frontend     │       FastAPI Backend             │
│      (Port 3000)         │        (Port 8000)                │
│                          │                                    │
│  ┌──────────────────┐    │  ┌────────────────────────────┐  │
│  │  App Router       │    │  │  API Layer (Routes)         │  │
│  │  Pages & Layouts  │    │  │  ┌──────────────────────┐  │  │
│  │  Components       │────┼──│  │  RBAC Guards          │  │  │
│  │  Context Stores   │    │  │  │  Country Guards       │  │  │
│  └──────────────────┘    │  │  └──────────────────────┘  │  │
│                          │  │  ┌──────────────────────┐  │  │
│                          │  │  │  Service Layer        │  │  │
│                          │  │  │  (Business Logic)     │  │  │
│                          │  │  └──────────────────────┘  │  │
│                          │  │  ┌──────────────────────┐  │  │
│                          │  │  │  Repository Layer     │  │  │
│                          │  │  │  (Data Access)        │  │  │
│                          │  │  └──────────────────────┘  │  │
│                          │  └────────────────────────────┘  │
├──────────────────────────┴──────────────────────────────────┤
│              PostgreSQL          │         Redis             │
│            (Port 5432)           │       (Port 6379)         │
└──────────────────────────────────┴──────────────────────────┘
```

## Backend Component Diagram

```
app/
├── main.py                 ← FastAPI app factory + lifespan
├── core/
│   ├── config.py           ← Pydantic settings
│   ├── security.py         ← JWT + bcrypt
│   ├── logging.py          ← structlog setup
│   └── exceptions.py       ← Custom exception hierarchy
├── database/
│   ├── session.py          ← SQLAlchemy engine + session
│   └── seed.py             ← Test data seeder
├── models/
│   └── models.py           ← SQLAlchemy ORM models
├── schemas/
│   └── schemas.py          ← Pydantic request/response DTOs
├── rbac/
│   ├── permissions.py      ← Role-Permission matrix
│   └── guards.py           ← DI-based auth guards
├── repositories/
│   └── repositories.py     ← Data access layer
├── services/
│   └── services.py         ← Business logic layer
├── api/
│   ├── auth.py             ← Authentication endpoints
│   ├── restaurants.py      ← Restaurant + Menu endpoints
│   ├── orders.py           ← Order management endpoints
│   ├── payments.py         ← Payment method endpoints
│   └── admin.py            ← Dashboard + User management
└── middleware/
    └── logging.py          ← Request logging middleware
```

## Data Flow

### Authentication Flow
```
Client → POST /api/v1/auth/login
  → AuthService.authenticate()
    → UserRepository.get_by_email()
    → verify_password()
    → create_access_token(sub=user_id, role=ROLE, country=COUNTRY)
  ← TokenResponse { access_token, user }
```

### Order Creation Flow
```
Client → POST /api/v1/orders (Bearer Token)
  → JWT decoded → CurrentUser extracted
  → require_permission(CREATE_ORDER) validated
  → OrderService.create_order()
    → RestaurantRepository.get_by_id()
    → CountryGuard.validate(user.country, restaurant.country)
    → MenuItemRepository.get_by_id() for each item
    → Order + OrderItems created
    → DB commit
  ← OrderResponse
```

### Authorization Flow
```
Every protected request:
  1. HTTPBearer extracts JWT
  2. decode_access_token() validates token
  3. User loaded from DB
  4. CurrentUser constructed with role + country
  5. require_permission(action) checks role-permission matrix
  6. CountryGuard.validate() enforces row-level access
  7. Service layer applies business rules
```

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| API Framework | FastAPI | Async support, auto OpenAPI docs, dependency injection |
| ORM | SQLAlchemy 2.0 | Mature, type-safe, supports complex queries |
| Database | PostgreSQL 16 | ACID compliance, JSON support, row-level security |
| Cache | Redis 7 | Sub-millisecond latency, pub/sub for future events |
| Auth | JWT (python-jose) | Stateless, embeds role+country for zero-DB-hit auth |
| Frontend | Next.js 14 | App Router, SSR/SSG, excellent DX |
| Styling | TailwindCSS 3 | Utility-first, design system consistency |
| Animation | Framer Motion | Production-grade React animations |
| Proxy | Nginx | Battle-tested, efficient reverse proxy |
| Container | Docker + Compose | Reproducible environments |
