# Slooze Platform: Demo Script & Runbook

**Target Length:** 5–7 Minutes
**Tone:** Startup Product Launch (Polished, Fast-Paced, Value-Driven)
**Presenter:** Product Demo Engineer

---

## Part 1: The First Impression & Enterprise Theming (1:00)

**Goal:** Showcase the premium UI and flawless Enterprise Design System.

1. **Start on Login Page:**
   - Leave the mouse still for 3 seconds so the background animations (floating gradients) are visible.
   - Point out the clean Glassmorphism aesthetic.
2. **Quick Login as Nick Fury (Admin):**
   - Click the "Nick Fury" quick login card.
   - Wait for the dashboard to load.
3. **Showcase Theming:**
   - Move cursor to the top-right `Theme Toggle`.
   - Click to open the ShadCN dropdown.
   - Select **Light Mode**.
   - Watch the UI instantly transition to the Apple/Stripe-like white aesthetic.
   - Hit **F5 (Refresh)** to prove no FOUC (Flash of Unstyled Content) occurs.
   - Switch back to **Dark Mode**.

## Part 2: The Core Product — Food Ordering & Cart (1:30)

**Goal:** Demonstrate the core product loop (Restaurants -> Menu -> Cart -> Checkout).

1. **Navigate to Restaurants:**
   - Click "Restaurants" in the sidebar.
   - Point out the data loading (skeleton loaders).
2. **Interact with a Menu:**
   - Click "View Menu" on `Liberty Grill & Steakhouse` (US Restaurant).
   - Add two items to the cart (e.g., Classic Cheeseburger, Truffle Fries).
3. **Cart & Checkout:**
   - Click "Cart" in the sidebar.
   - Show the total calculation.
   - Click "Proceed to Checkout".
   - Select a payment method and place the order.
4. **Order Tracking:**
   - Navigate to "My Orders".
   - Show the newly placed order in `PLACED` state.

## Part 3: Enterprise RBAC & Admin Powers (1:30)

**Goal:** Prove that the Admin role has full control.

1. **Admin Capabilities:**
   - In "My Orders", show the ability to cancel orders.
   - Navigate to "Payments" in the sidebar. Show that Admins can view/manage payment methods.
   - Navigate to "Users" in the sidebar. Emphasize that only Admins can see this screen.
2. **Sign Out:**
   - Click "Sign Out" in the bottom left.

## Part 4: Country Isolation & Manager Role (1:00)

**Goal:** Demonstrate row-level country isolation and restricted Manager capabilities.

1. **Login as Captain Marvel (Manager - India):**
   - Click "Captain Marvel" on the Quick Login screen.
2. **Prove Country Isolation:**
   - Navigate to "Restaurants".
   - **Crucial step:** Show that Captain Marvel ONLY sees Indian restaurants (e.g., Taj Mahal Kitchen, Spice Garden), whereas Nick Fury saw US restaurants.
3. **Prove RBAC Limitations:**
   - Notice that the "Users" and "Payments" tabs are completely missing from the sidebar.
   - Navigate to "Dashboard". Point out that Managers can still see high-level statistics, unlike normal members.
4. **Sign Out:**
   - Click "Sign Out".

## Part 5: The Member Experience (1:00)

**Goal:** Show the most restricted, consumer-facing role.

1. **Login as Thanos (Member - India):**
   - Click "Thanos" on the Quick Login screen.
2. **Prove RBAC Limitations:**
   - Notice the sidebar is completely stripped down. Only "Dashboard", "Restaurants", "My Orders", and "Cart" remain.
   - Navigate to "My Orders".
   - Select an order and try to cancel it (if the button exists, it should be disabled or throw an unauthorized toast).
3. **Conclusion:**
   - Return to the Dashboard.
   - Deliver the closing statement.

---

### Expected Outcomes per Step:
- **Theme Switch:** Instant, <16ms, no layout jumps.
- **Cart checkout:** Success toast appears, redirects to Orders.
- **Admin Users Page:** Table loads all users.
- **Manager Restaurants:** List is strictly filtered to `country: INDIA`.
- **Member Sidebar:** Navigation items are conditionally hidden based on JWT role claims.
