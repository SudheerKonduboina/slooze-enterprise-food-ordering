# Slooze API Specification

This document provides a detailed overview of the RESTful API endpoints provided by the Slooze backend. All endpoints are prefixed with `/api/v1`.

## 🔐 Authentication

### `POST /auth/login`
Authenticates a user and returns a JWT access token.
- **Request Body:**
  - `email` (string, required)
  - `password` (string, required)
- **Response:**
  - `access_token` (string)
  - `token_type` (string: "bearer")

---

## 🍽️ Restaurants & Menus

### `GET /restaurants`
List all restaurants accessible to the user based on their country.
- **Access:** Admin, Manager, Member.
- **Filtering:** Automatically filtered by the user's `country` claim in JWT.

### `GET /restaurants/{restaurant_id}`
Retrieve detailed information about a specific restaurant, including its menu.
- **Access:** Admin, Manager, Member.

---

## 🛒 Orders

### `POST /orders`
Place a new food order.
- **Access:** Admin, Manager, Member.
- **Request Body:**
  - `restaurant_id` (string)
  - `items` (List of objects: `{ menu_item_id: string, quantity: int }`)
- **Note:** Relational access control ensures users can only order from restaurants in their assigned country.

### `GET /orders`
List orders placed by the user (Members/Managers) or all orders (Admin).
- **Access:** All.

### `POST /orders/{order_id}/cancel`
Cancel an existing order.
- **Access:** Admin, Manager.
- **Restriction:** Members cannot cancel orders.

---

## 💳 Payments

### `GET /payments/methods`
List available payment methods.
- **Access:** Admin.

### `POST /payments/methods`
Add a new payment method.
- **Access:** Admin.

---

## 🛡️ Admin & User Management

### `GET /admin/users`
List all users in the system.
- **Access:** Admin only.

### `GET /admin/dashboard`
Retrieve high-level analytics (Revenue, Total Orders, Active Users).
- **Access:** Admin, Manager.
- **Restriction:** Managers see stats filtered by their region.

---

## ⚠️ Error Responses

| Status Code | Description |
|:---:|:---|
| `401 Unauthorized` | Invalid or missing JWT token. |
| `403 Forbidden` | Insufficient RBAC permissions or Country Access mismatch. |
| `404 Not Found` | The requested resource (restaurant, order, user) does not exist. |
| `422 Unprocessable Entity` | Validation error (handled by Pydantic). |
| `500 Internal Server Error` | Unexpected backend failure. |
