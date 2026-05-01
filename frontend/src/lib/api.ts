import Cookies from 'js-cookie';
import type {
  TokenResponse, LoginRequest, RestaurantListResponse,
  MenuItemListResponse, Order, OrderListResponse,
  PaymentMethod, DashboardStats, UserListResponse, Restaurant
} from './types';

const API_BASE = '/api/v1';

class ApiClient {
  private getToken(): string | undefined {
    return Cookies.get('slooze_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // ─── Auth ────────────────────────────────────────────────────────────
  async login(data: LoginRequest): Promise<TokenResponse> {
    return this.request<TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // ─── Restaurants ─────────────────────────────────────────────────────
  async getRestaurants(page = 1, pageSize = 20): Promise<RestaurantListResponse> {
    return this.request<RestaurantListResponse>(
      `/restaurants?page=${page}&page_size=${pageSize}`
    );
  }

  async getRestaurant(id: string): Promise<Restaurant> {
    return this.request<Restaurant>(`/restaurants/${id}`);
  }

  async getMenu(restaurantId: string, page = 1, pageSize = 50, category?: string): Promise<MenuItemListResponse> {
    let url = `/restaurants/${restaurantId}/menu?page=${page}&page_size=${pageSize}`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    return this.request<MenuItemListResponse>(url);
  }

  // ─── Orders ──────────────────────────────────────────────────────────
  async createOrder(restaurantId: string, items: { menu_item_id: string; quantity: number }[], notes?: string): Promise<Order> {
    return this.request<Order>('/orders', {
      method: 'POST',
      body: JSON.stringify({ restaurant_id: restaurantId, items, notes }),
    });
  }

  async getOrders(page = 1, pageSize = 20, status?: string): Promise<OrderListResponse> {
    let url = `/orders?page=${page}&page_size=${pageSize}`;
    if (status) url += `&status=${status}`;
    return this.request<OrderListResponse>(url);
  }

  async getOrder(id: string): Promise<Order> {
    return this.request<Order>(`/orders/${id}`);
  }

  async checkoutOrder(orderId: string, paymentMethodId: string): Promise<Order> {
    return this.request<Order>(`/orders/${orderId}/checkout`, {
      method: 'POST',
      body: JSON.stringify({ payment_method_id: paymentMethodId }),
    });
  }

  async cancelOrder(orderId: string): Promise<Order> {
    return this.request<Order>(`/orders/${orderId}/cancel`, {
      method: 'POST',
    });
  }

  async updateOrderPaymentMethod(orderId: string, paymentMethodId: string): Promise<Order> {
    return this.request<Order>(`/orders/${orderId}/payment-method`, {
      method: 'PUT',
      body: JSON.stringify({ payment_method_id: paymentMethodId }),
    });
  }

  // ─── Payment Methods ─────────────────────────────────────────────────
  async getPaymentMethods(): Promise<PaymentMethod[]> {
    return this.request<PaymentMethod[]>('/payment-methods');
  }

  async createPaymentMethod(data: {
    method_type: string; label: string; details?: string; is_default?: boolean;
  }): Promise<PaymentMethod> {
    return this.request<PaymentMethod>('/payment-methods', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async deletePaymentMethod(id: string): Promise<void> {
    await this.request(`/payment-methods/${id}`, { method: 'DELETE' });
  }

  // ─── Admin ───────────────────────────────────────────────────────────
  async getDashboard(): Promise<DashboardStats> {
    return this.request<DashboardStats>('/admin/dashboard');
  }

  async getUsers(page = 1, pageSize = 20): Promise<UserListResponse> {
    return this.request<UserListResponse>(`/admin/users?page=${page}&page_size=${pageSize}`);
  }
}

export const api = new ApiClient();
