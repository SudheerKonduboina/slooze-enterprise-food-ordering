'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import Cookies from 'js-cookie';
import { api } from './api';
import type { User, Role, Country, LoginRequest, MenuItem } from './types';

/* ─── Auth Context ──────────────────────────────────────────────────────── */

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  isLoading: true,
  login: async () => {},
  logout: () => {},
  isAuthenticated: false,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const savedToken = Cookies.get('slooze_token');
    const savedUser = Cookies.get('slooze_user');
    if (savedToken && savedUser) {
      try {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
      } catch {
        Cookies.remove('slooze_token');
        Cookies.remove('slooze_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (data: LoginRequest) => {
    const response = await api.login(data);
    setToken(response.access_token);
    setUser(response.user);
    Cookies.set('slooze_token', response.access_token, { expires: 1 });
    Cookies.set('slooze_user', JSON.stringify(response.user), { expires: 1 });
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    Cookies.remove('slooze_token');
    Cookies.remove('slooze_user');
  };

  return (
    <AuthContext.Provider
      value={{ user, token, isLoading, login, logout, isAuthenticated: !!token }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

/* ─── Cart Context ──────────────────────────────────────────────────────── */

export interface CartItem {
  menuItem: MenuItem;
  quantity: number;
  specialInstructions?: string;
}

interface CartContextType {
  items: CartItem[];
  restaurantId: string | null;
  restaurantName: string | null;
  addItem: (item: MenuItem, quantity?: number) => void;
  removeItem: (menuItemId: string) => void;
  updateQuantity: (menuItemId: string, quantity: number) => void;
  clearCart: () => void;
  total: number;
  itemCount: number;
}

const CartContext = createContext<CartContextType>({
  items: [],
  restaurantId: null,
  restaurantName: null,
  addItem: () => {},
  removeItem: () => {},
  updateQuantity: () => {},
  clearCart: () => {},
  total: 0,
  itemCount: 0,
});

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [restaurantId, setRestaurantId] = useState<string | null>(null);
  const [restaurantName, setRestaurantName] = useState<string | null>(null);

  const addItem = useCallback((menuItem: MenuItem, quantity = 1) => {
    setItems((prev) => {
      // If different restaurant, clear cart
      if (restaurantId && menuItem.restaurant_id !== restaurantId) {
        setRestaurantId(menuItem.restaurant_id);
        return [{ menuItem, quantity }];
      }

      setRestaurantId(menuItem.restaurant_id);

      const existing = prev.find((i) => i.menuItem.id === menuItem.id);
      if (existing) {
        return prev.map((i) =>
          i.menuItem.id === menuItem.id
            ? { ...i, quantity: i.quantity + quantity }
            : i
        );
      }
      return [...prev, { menuItem, quantity }];
    });
  }, [restaurantId]);

  const removeItem = useCallback((menuItemId: string) => {
    setItems((prev) => {
      const filtered = prev.filter((i) => i.menuItem.id !== menuItemId);
      if (filtered.length === 0) {
        setRestaurantId(null);
        setRestaurantName(null);
      }
      return filtered;
    });
  }, []);

  const updateQuantity = useCallback((menuItemId: string, quantity: number) => {
    if (quantity <= 0) {
      removeItem(menuItemId);
      return;
    }
    setItems((prev) =>
      prev.map((i) =>
        i.menuItem.id === menuItemId ? { ...i, quantity } : i
      )
    );
  }, [removeItem]);

  const clearCart = useCallback(() => {
    setItems([]);
    setRestaurantId(null);
    setRestaurantName(null);
  }, []);

  const total = items.reduce((sum, i) => sum + i.menuItem.price * i.quantity, 0);
  const itemCount = items.reduce((sum, i) => sum + i.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        items,
        restaurantId,
        restaurantName,
        addItem,
        removeItem,
        updateQuantity,
        clearCart,
        total,
        itemCount,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => useContext(CartContext);
