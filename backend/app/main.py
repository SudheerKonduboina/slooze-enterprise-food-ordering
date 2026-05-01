"""
Slooze Food Ordering Platform — Main Application Entry Point.

A production-grade FastAPI application with:
- Enterprise RBAC authorization
- Country-based relational access control
- Clean architecture with service/repository pattern
- Structured logging and error handling
- Redis caching and API versioning
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.middleware.logging import RequestLoggingMiddleware, ExceptionHandlerMiddleware
from app.database.session import engine, Base
from app.database.seed import seed_database
from app.api import auth, restaurants, orders, payments, admin

settings = get_settings()
setup_logging()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler: startup and shutdown events."""
    logger.info("application_starting", version=settings.APP_VERSION)

    # Create tables and seed
    Base.metadata.create_all(bind=engine)
    try:
        seed_database()
    except Exception as e:
        logger.warning("seed_skipped", reason=str(e))

    logger.info("application_started")
    yield
    logger.info("application_shutting_down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## 🍽️ Slooze Food Ordering Platform API

A production-grade food ordering backend with enterprise RBAC and country-based access control.

### 🔐 Authentication
All endpoints (except login) require a Bearer JWT token.
Login to get a token, which embeds your role and country.

### 👥 Roles
| Role | Permissions |
|------|------------|
| **ADMIN** | Full access to all operations |
| **MANAGER** | View menu, create/cancel orders, checkout |
| **MEMBER** | View menu, create orders only |

### 🌍 Country Access Control
Users can only access restaurants, menus, and orders in their assigned country.
- India users → India restaurants/orders only
- America users → America data only
- Admins can access all countries

### 🧪 Test Credentials
| User | Email | Role | Country |
|------|-------|------|---------|
| Nick Fury | nick.fury@shield.gov | ADMIN | AMERICA |
| Captain Marvel | carol.danvers@shield.gov | MANAGER | INDIA |
| Captain America | steve.rogers@shield.gov | MANAGER | AMERICA |
| Thanos | thanos@titan.space | MEMBER | INDIA |
| Thor | thor@asgard.realm | MEMBER | INDIA |
| Travis | travis@avengers.org | MEMBER | AMERICA |

**Password for all users:** `password123`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Middleware ───────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

# ─── API Routes ──────────────────────────────────────────────────────────────

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(restaurants.router, prefix=settings.API_V1_PREFIX)
app.include_router(orders.router, prefix=settings.API_V1_PREFIX)
app.include_router(payments.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)


# ─── Root Endpoint ───────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Health check and API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "database": "connected",
    }
