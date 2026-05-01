# 🔐 RBAC Design

## Overview

The Slooze platform implements a dual-layer authorization system:

1. **Role-Based Access Control (RBAC)** — Action-level permissions tied to roles
2. **Relational Access Control (ReBAC)** — Country-based row-level data isolation

## Permission Model

### Actions

| Action | Description |
|--------|-------------|
| `view_restaurants` | View restaurant listings |
| `view_menu` | View menu items for a restaurant |
| `create_order` | Create a new order / add items to cart |
| `checkout` | Process payment and place order |
| `cancel_order` | Cancel an existing order |
| `add_payment_method` | Add a new payment method |
| `modify_payment_method` | Edit or delete payment methods |
| `view_own_orders` | View user's own orders |
| `view_all_orders` | View all orders (admin) |
| `manage_users` | View and manage user accounts |
| `view_dashboard` | Access dashboard statistics |
| `update_order_payment` | Change payment method on an order |

### Role-Permission Matrix

| Action | ADMIN | MANAGER | MEMBER |
|--------|:-----:|:-------:|:------:|
| view_restaurants | ✅ | ✅ | ✅ |
| view_menu | ✅ | ✅ | ✅ |
| create_order | ✅ | ✅ | ✅ |
| checkout | ✅ | ✅ | ❌ |
| cancel_order | ✅ | ✅ | ❌ |
| add_payment_method | ✅ | ❌ | ❌ |
| modify_payment_method | ✅ | ❌ | ❌ |
| view_own_orders | ✅ | ✅ | ✅ |
| view_all_orders | ✅ | ❌ | ❌ |
| manage_users | ✅ | ❌ | ❌ |
| view_dashboard | ✅ | ✅ | ❌ |
| update_order_payment | ✅ | ✅ | ❌ |

## Role Hierarchy

```
ADMIN (superuser — all permissions)
  └── MANAGER (operational — order lifecycle)
        └── MEMBER (basic — view + create only)
```

## Implementation

### 1. Permission Decorator (Dependency Injection)

```python
# Usage in API routes:
@router.post("/orders")
async def create_order(
    current_user: CurrentUser = Depends(require_permission(Action.CREATE_ORDER)),
):
    ...
```

The `require_permission()` factory returns a FastAPI dependency that:
1. Extracts the JWT token via `HTTPBearer`
2. Decodes and validates the token
3. Loads the user from the database
4. Checks the role-permission matrix
5. Returns a `CurrentUser` context object

### 2. Country Guard (Row-Level Access Control)

```python
class CountryGuard:
    @staticmethod
    def validate(user_country, resource_country):
        if user_country != resource_country:
            raise HTTP 403

    @staticmethod
    def filter_query(query, model_field, user_country):
        return query.filter(model_field == user_country)
```

### 3. JWT Token Structure

```json
{
  "sub": "user-id-uuid",
  "role": "MANAGER",
  "country": "INDIA",
  "email": "user@example.com",
  "exp": 1714567890
}
```

Role and country are embedded in the token, enabling zero-database-hit permission checks for action-level authorization. The user is still loaded from DB for data integrity validation.

## Policy Enforcement Points

| Layer | Enforcement |
|-------|-------------|
| **API Router** | `require_permission(Action)` dependency |
| **Service Layer** | `CountryGuard.validate()` before data access |
| **Repository Layer** | `CountryGuard.filter_query()` on list queries |
| **Frontend** | `hasPermission(role, action)` for UI visibility |

## Security Properties

- **No privilege escalation**: Permissions are checked server-side on every request
- **No cross-country data leakage**: Country guard applied at query level
- **Token integrity**: JWT signed with HS256, validated on every request
- **Defense in depth**: Multiple layers enforce the same policies
