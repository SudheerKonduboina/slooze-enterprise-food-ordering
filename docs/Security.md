# 🛡️ Security

## Authentication

### JWT Token-Based Authentication

- **Algorithm**: HS256 (HMAC-SHA256)
- **Token Lifetime**: 60 minutes (configurable)
- **Token Contents**: User ID, role, country, email, expiration
- **Password Hashing**: bcrypt with automatic salt generation

### Authentication Flow

```
1. POST /api/v1/auth/login { email, password }
2. Server validates credentials against bcrypt hash
3. Server generates JWT with user context embedded
4. Client stores token (httpOnly cookie recommended for production)
5. Subsequent requests include: Authorization: Bearer <token>
6. Server validates JWT signature and expiration on every request
```

## Access Isolation

### Role-Based Access Control (RBAC)

Every API endpoint is protected by a `require_permission(Action)` dependency that:

1. Extracts and validates the JWT token
2. Loads the user from the database
3. Checks the role-permission matrix
4. Raises HTTP 403 if the permission check fails

### Country-Based Data Isolation

Row-level access control ensures users only see data from their assigned country:

```python
# Every query filters by country
restaurants = db.query(Restaurant).filter(
    Restaurant.country == current_user.country
)

orders = db.query(Order).filter(
    Order.country == current_user.country,
    Order.user_id == current_user.id
)
```

**Key principle**: Country is denormalized onto orders at creation time, so changing a user's country doesn't retroactively change order visibility.

## Injection Protection

### SQL Injection
- **ORM-based queries**: All database access uses SQLAlchemy's parameterized queries
- **No raw SQL**: The application never constructs SQL strings from user input
- **Input validation**: Pydantic schemas validate all request bodies

### XSS Prevention
- **Content Security Policy** headers via Nginx
- **React's built-in escaping**: JSX automatically escapes rendered values
- **No dangerouslySetInnerHTML**: Application does not use unsafe React APIs

### CSRF Protection
- **Token-based auth**: JWT tokens in Authorization headers are not vulnerable to CSRF
- **SameSite cookies**: When using cookies, SameSite=Strict is recommended

## Security Headers

Set by Nginx reverse proxy:

```
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

## API Security

### Rate Limiting (Recommended for Production)
```python
# Future: Using slowapi or custom middleware
@app.middleware("http")
async def rate_limit(request, call_next):
    # Check Redis for request count
    # Enforce rate limits per API key/IP
```

### Input Validation
- All request bodies validated by Pydantic schemas
- Strict type checking on all fields
- Field constraints (min_length, gt=0, etc.)
- Enum validation for roles, countries, order statuses

### Error Handling
- Custom exception hierarchy prevents information leakage
- Production errors return generic messages
- Debug mode (controlled by env) provides detailed errors only in development

## Secrets Management

| Secret | Storage | Notes |
|--------|---------|-------|
| JWT_SECRET_KEY | Environment variable | Must be rotated regularly |
| DATABASE_URL | Environment variable | Contains credentials |
| REDIS_URL | Environment variable | Network-scoped access |

### Production Recommendations

1. Use a secrets manager (AWS Secrets Manager, HashiCorp Vault)
2. Rotate JWT secrets periodically
3. Use TLS for all database connections
4. Enable PostgreSQL SSL mode
5. Run containers as non-root users
6. Implement API rate limiting
7. Add request size limits
8. Enable audit logging for sensitive operations
