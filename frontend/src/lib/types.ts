/* ─── User & Auth Types ─────────────────────────────────────────────────── */

export type Role = 'ADMIN' | 'MANAGER' | 'MEMBER';
export type Country = 'INDIA' | 'AMERICA';
export type OrderStatus = 'CART' | 'PLACED' | 'CONFIRMED' | 'PREPARING' | 'DELIVERED' | 'CANCELLED';
export type PaymentMethodType = 'CREDIT_CARD' | 'DEBIT_CARD' | 'UPI' | 'NET_BANKING' | 'WALLET';
export type PaymentStatus = 'PENDING' | 'COMPLETED' | 'FAILED' | 'REFUNDED';

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  role: Role;
  country: Country;
  is_active: boolean;
  avatar_url?: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

/* ─── Restaurant & Menu Types ───────────────────────────────────────────── */

export interface Restaurant {
  id: string;
  name: string;
  description?: string;
  cuisine_type: string;
  country: string;
  address?: string;
  rating: number;
  image_url?: string;
  opening_hours: string;
  delivery_time_mins: number;
  is_active: boolean;
  created_at: string;
  menu_item_count?: number;
}

export interface MenuItem {
  id: string;
  restaurant_id: string;
  name: string;
  description?: string;
  price: number;
  category: string;
  image_url?: string;
  is_vegetarian: boolean;
  is_available: boolean;
  preparation_time_mins: number;
  created_at: string;
}

/* ─── Order Types ───────────────────────────────────────────────────────── */

export interface OrderItem {
  id: string;
  menu_item_id: string;
  menu_item_name?: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  special_instructions?: string;
}

export interface Payment {
  id: string;
  order_id: string;
  payment_method_id?: string;
  amount: number;
  status: PaymentStatus;
  transaction_id?: string;
  paid_at?: string;
  created_at: string;
}

export interface Order {
  id: string;
  user_id: string;
  restaurant_id: string;
  restaurant_name?: string;
  country: string;
  status: OrderStatus;
  total_amount: number;
  notes?: string;
  items: OrderItem[];
  payment?: Payment;
  created_at: string;
  updated_at: string;
}

/* ─── Payment Method Types ──────────────────────────────────────────────── */

export interface PaymentMethod {
  id: string;
  user_id: string;
  method_type: PaymentMethodType;
  label: string;
  details?: string;
  is_default: boolean;
  created_at: string;
}

/* ─── Dashboard Types ───────────────────────────────────────────────────── */

export interface DashboardStats {
  total_orders: number;
  total_revenue: number;
  total_restaurants: number;
  total_users: number;
  recent_orders: Order[];
  orders_by_status: Record<string, number>;
}

/* ─── Paginated Response Types ──────────────────────────────────────────── */

export interface PaginatedResponse<T> {
  total: number;
  page: number;
  page_size: number;
}

export interface RestaurantListResponse extends PaginatedResponse<Restaurant> {
  restaurants: Restaurant[];
}

export interface MenuItemListResponse extends PaginatedResponse<MenuItem> {
  menu_items: MenuItem[];
}

export interface OrderListResponse extends PaginatedResponse<Order> {
  orders: Order[];
}

export interface UserListResponse extends PaginatedResponse<User> {
  users: User[];
}

/* ─── Permission Types ──────────────────────────────────────────────────── */

export const ROLE_PERMISSIONS: Record<Role, string[]> = {
  ADMIN: [
    'view_restaurants', 'view_menu', 'create_order', 'checkout',
    'cancel_order', 'add_payment_method', 'modify_payment_method',
    'view_all_orders', 'manage_users', 'view_dashboard', 'view_own_orders',
    'update_order_payment',
  ],
  MANAGER: [
    'view_restaurants', 'view_menu', 'create_order', 'checkout',
    'cancel_order', 'view_own_orders', 'view_dashboard', 'update_order_payment',
  ],
  MEMBER: [
    'view_restaurants', 'view_menu', 'create_order', 'view_own_orders',
  ],
};

export function hasPermission(role: Role, action: string): boolean {
  return ROLE_PERMISSIONS[role]?.includes(action) ?? false;
}
