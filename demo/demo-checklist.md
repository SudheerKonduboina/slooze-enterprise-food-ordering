# Slooze Food Ordering Platform - Demo Checklist

Use this checklist during your live or recorded demonstration to ensure all critical backend and frontend features are verified and showcased.

## 1. Initial Load & Design System
- [ ] Application loads at `http://localhost:3000` with floating gradient animations.
- [ ] Quick Login cards display properly with CSS variables.
- [ ] Click Theme Toggle in top right (Dropdown opens smoothly).
- [ ] Select **Light Mode**. 
  - *Expected Outcome: Instant transition to white/gray background, shadows adapt properly.*
- [ ] Perform a browser refresh (F5).
  - *Expected Outcome: Light mode persists with ZERO white flashing or hydration errors.*
- [ ] Switch Theme back to **System** or **Dark**.

## 2. Authentication & Admin Context (Nick Fury)
- [ ] Click Quick Login for **Nick Fury (Admin / US)**.
  - *Expected Outcome: Redirects to Dashboard. Admin metrics (Revenue, Total Orders) are visible.*
- [ ] Look at the Sidebar.
  - *Expected Outcome: ALL navigation items are visible (Dashboard, Restaurants, My Orders, Payments, Users, Cart).*

## 3. Core Ordering Flow
- [ ] Navigate to **Restaurants**.
  - *Expected Outcome: US Restaurants are displayed (Liberty Grill, Smoky BBQ).*
- [ ] Click **View Menu** on a restaurant.
- [ ] Add 2 different items to the cart.
- [ ] Navigate to **Cart**.
  - *Expected Outcome: Items are listed, total price is accurate.*
- [ ] Click **Proceed to Checkout**. Select a payment method and submit.
  - *Expected Outcome: Success toast appears. Redirected to Orders page.*
- [ ] View **My Orders**.
  - *Expected Outcome: New order appears at the top with a `PLACED` badge.*
- [ ] Cancel an order using the Cancel button.
  - *Expected Outcome: Badge updates to `CANCELLED` (Admin has permission).*

## 4. Admin Management Powers
- [ ] Navigate to **Payments**.
  - *Expected Outcome: Payment methods are visible and manageable.*
- [ ] Navigate to **Users**.
  - *Expected Outcome: User table loads. Nick Fury can view all system users.*
- [ ] Click **Sign Out**.

## 5. Row-Level Country Isolation (Captain Marvel)
- [ ] Click Quick Login for **Captain Marvel (Manager / India)**.
- [ ] Navigate to **Restaurants**.
  - *Expected Outcome: ONLY Indian restaurants are visible (Taj Mahal Kitchen, Spice Garden). No US restaurants.*
- [ ] Navigate to **My Orders**.
  - *Expected Outcome: ONLY orders placed in India by this user are visible.*

## 6. RBAC UI Hardening (Manager limitations)
- [ ] Look at the Sidebar.
  - *Expected Outcome: "Users" and "Payments" tabs are completely hidden from the UI.*
- [ ] Click **Sign Out**.

## 7. The Member Experience (Thanos)
- [ ] Click Quick Login for **Thanos (Member / India)**.
- [ ] Look at the Sidebar.
  - *Expected Outcome: Highly restricted. Only Dashboard, Restaurants, My Orders, Cart.*
- [ ] Look at the Dashboard.
  - *Expected Outcome: High-level financial metrics (Total Revenue) are hidden or zeroed out depending on member policies.*
- [ ] Click **Sign Out**.

## Final Verification
- [ ] Console is clear of errors.
- [ ] No hydration mismatches occurred.
- [ ] API responses were consistently fast.
