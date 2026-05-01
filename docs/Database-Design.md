# 🗄️ Database Design

## Entity-Relationship Diagram

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│    users     │     │  restaurants  │     │  menu_items   │
├─────────────┤     ├──────────────┤     ├──────────────┤
│ id (PK)      │     │ id (PK)       │     │ id (PK)       │
│ email        │     │ name          │     │ restaurant_id  │──→ restaurants.id
│ username     │     │ description   │     │ name          │
│ full_name    │     │ cuisine_type  │     │ description   │
│ hashed_pwd   │     │ country ──────┼─┐   │ price         │
│ role ────────┼─┐   │ address       │ │   │ category      │
│ country ─────┼─┤   │ rating        │ │   │ image_url     │
│ is_active    │ │   │ image_url     │ │   │ is_vegetarian │
│ avatar_url   │ │   │ is_active     │ │   │ is_available  │
│ created_at   │ │   │ opening_hours │ │   │ prep_time_mins│
│ updated_at   │ │   │ delivery_mins │ │   │ created_at    │
└──────┬───────┘ │   │ created_at    │ │   └──────────────┘
       │         │   │ updated_at    │ │
       │         │   └──────────────┘ │
       │         │                     │
       │    ┌────┴────────────────┐   │    Country-based isolation:
       │    │  ENUM: RoleEnum     │   │    Users and restaurants
       │    │  ADMIN | MANAGER    │   │    have a country field.
       │    │  MEMBER             │   │    Queries are filtered
       │    └─────────────────────┘   │    by user.country.
       │    ┌─────────────────────┐   │
       │    │  ENUM: CountryEnum  │───┘
       │    │  INDIA | AMERICA    │
       │    └─────────────────────┘
       │
       ▼
┌─────────────────┐     ┌───────────────┐     ┌──────────────┐
│    orders        │     │  order_items   │     │  payments     │
├─────────────────┤     ├───────────────┤     ├──────────────┤
│ id (PK)          │     │ id (PK)        │     │ id (PK)       │
│ user_id ─────────┼──→  │ order_id ──────┼──→  │ order_id ─────┼──→ orders.id
│ restaurant_id ───┼──→  │ menu_item_id ──┼──→  │ pm_id ────────┼──→ payment_methods.id
│ country          │     │ quantity       │     │ amount        │
│ status           │     │ unit_price     │     │ status        │
│ total_amount     │     │ subtotal       │     │ transaction_id│
│ notes            │     │ special_instr  │     │ paid_at       │
│ created_at       │     │ created_at     │     │ created_at    │
│ updated_at       │     └───────────────┘     │ updated_at    │
└─────────────────┘                             └──────────────┘
       │
       ▼
┌──────────────────┐
│ payment_methods   │
├──────────────────┤
│ id (PK)           │
│ user_id ──────────┼──→ users.id
│ method_type       │
│ label             │
│ details           │
│ is_default        │
│ created_at        │
│ updated_at        │
└──────────────────┘
```

## Tables

### `users`
Stores all user accounts. Each user has exactly one `role` and one `country`.

### `restaurants`
Restaurants are scoped to a `country`. Users can only see restaurants in their country.

### `menu_items`
Food items belonging to a restaurant. Inherit the country scope from their parent restaurant.

### `orders`
Orders are created by users and scoped to a country (copied from the restaurant's country at creation time). This ensures country-level data isolation even if relationships change.

### `order_items`
Individual line items within an order. References both the order and the menu item.

### `payment_methods`
User-managed payment methods (credit card, UPI, etc.). Only ADMIN can create/modify these.

### `payments`
Payment records for orders. Created during checkout, linked to a payment method.

## Key Design Decisions

1. **Country on Orders**: The `country` field is denormalized onto orders for efficient row-level filtering without joins.

2. **UUID Primary Keys**: All tables use UUID strings for globally unique, non-sequential identifiers.

3. **Soft State**: Restaurants and menu items have `is_active` / `is_available` flags instead of hard deletes.

4. **Order Status Machine**: Orders follow a state machine: `CART → PLACED → CONFIRMED → PREPARING → DELIVERED` with `CANCELLED` as a terminal state.

5. **Payment Separation**: Payment methods and payment records are separate entities, allowing method reuse across orders.

## Indexes

- `users.email` — UNIQUE index for login lookups
- `users.username` — UNIQUE index
- `restaurants.country` — Index for country-based filtering
- `menu_items.restaurant_id` — Index for restaurant menu lookups
- `orders.user_id` — Index for user order history
- `orders.country` — Index for country-based filtering
- `orders.restaurant_id` — Index for restaurant order tracking
- `order_items.order_id` — Index for order item retrieval
- `payment_methods.user_id` — Index for user payment methods
- `payments.order_id` — UNIQUE index (one payment per order)
