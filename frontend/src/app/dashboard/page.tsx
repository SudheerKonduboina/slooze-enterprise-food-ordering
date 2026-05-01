'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/store';
import { hasPermission } from '@/lib/types';
import type { DashboardStats, Order } from '@/lib/types';
import {
  TrendingUp, ShoppingBag, UtensilsCrossed, Users,
  DollarSign, ArrowUpRight, Package
} from 'lucide-react';

const STATUS_COLORS: Record<string, string> = {
  CART: 'badge-warning',
  PLACED: 'badge-info',
  CONFIRMED: 'badge-info',
  PREPARING: 'badge-purple',
  DELIVERED: 'badge-success',
  CANCELLED: 'badge-danger',
};

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && hasPermission(user.role as any, 'view_dashboard')) {
      api.getDashboard()
        .then(setStats)
        .catch(console.error)
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [user]);

  if (!user) return null;

  const canViewDashboard = hasPermission(user.role as any, 'view_dashboard');

  if (!canViewDashboard) {
    return (
      <div>
        <h1 className="text-2xl font-display font-bold text-foreground mb-2">Welcome, {user.full_name}</h1>
        <p className="text-muted mb-8">Browse restaurants and place orders from your region.</p>

        <div className="glass-card p-8 text-center">
          <Package className="w-12 h-12 text-muted mx-auto mb-4" />
          <h2 className="text-lg font-semibold text-foreground mb-2">Start Ordering</h2>
          <p className="text-muted mb-6">Explore restaurants in {user.country === 'INDIA' ? '🇮🇳 India' : '🇺🇸 America'} and add items to your cart.</p>
          <a href="/dashboard/restaurants" className="btn-primary inline-flex items-center gap-2">
            Browse Restaurants <ArrowUpRight className="w-4 h-4" />
          </a>
        </div>
      </div>
    );
  }

  const statCards = stats ? [
    {
      label: 'Total Orders',
      value: stats.total_orders,
      icon: ShoppingBag,
      gradient: 'from-blue-500 to-cyan-500',
    },
    {
      label: 'Revenue',
      value: user.country === 'INDIA'
        ? `₹${stats.total_revenue.toLocaleString()}`
        : `$${stats.total_revenue.toLocaleString()}`,
      icon: DollarSign,
      gradient: 'from-emerald-500 to-teal-500',
    },
    {
      label: 'Restaurants',
      value: stats.total_restaurants,
      icon: UtensilsCrossed,
      gradient: 'from-purple-500 to-pink-500',
    },
    {
      label: 'Users',
      value: stats.total_users,
      icon: Users,
      gradient: 'from-amber-500 to-orange-500',
    },
  ] : [];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-display font-bold text-foreground mb-1">Dashboard</h1>
        <p className="text-muted">
          Welcome back, {user.full_name} — {user.country === 'INDIA' ? '🇮🇳 India' : '🇺🇸 America'} Region
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-32 rounded-2xl" />
          ))}
        </div>
      ) : stats ? (
        <>
          {/* Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {statCards.map((stat, i) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="glass-card p-6 group hover:border-border transition-all duration-300"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${stat.gradient} flex items-center justify-center`}>
                      <Icon className="w-5 h-5 text-foreground" />
                    </div>
                    <TrendingUp className="w-4 h-4 text-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <p className="text-2xl font-display font-bold text-foreground">{stat.value}</p>
                  <p className="text-sm text-muted mt-1">{stat.label}</p>
                </motion.div>
              );
            })}
          </div>

          {/* Orders by Status + Recent Orders */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Order Status Distribution */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="glass-card p-6"
            >
              <h2 className="text-lg font-semibold text-foreground mb-4">Order Distribution</h2>
              <div className="space-y-3">
                {Object.entries(stats.orders_by_status).map(([status, count]) => {
                  const total = Object.values(stats.orders_by_status).reduce((a, b) => a + b, 0);
                  const pct = total > 0 ? (count / total) * 100 : 0;
                  return (
                    <div key={status} className="flex items-center gap-3">
                      <span className={`${STATUS_COLORS[status] || 'badge-info'} w-24 text-center text-[10px]`}>
                        {status}
                      </span>
                      <div className="flex-1 h-2 bg-foreground/5 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 1, delay: 0.5 }}
                          className="h-full bg-gradient-to-r from-brand-500 to-purple-500 rounded-full"
                        />
                      </div>
                      <span className="text-sm text-muted w-8 text-right">{count}</span>
                    </div>
                  );
                })}
              </div>
            </motion.div>

            {/* Recent Orders */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="glass-card p-6"
            >
              <h2 className="text-lg font-semibold text-foreground mb-4">Recent Orders</h2>
              <div className="space-y-3">
                {stats.recent_orders.length === 0 ? (
                  <p className="text-muted text-sm text-center py-4">No orders yet</p>
                ) : (
                  stats.recent_orders.map((order) => (
                    <div key={order.id} className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
                      <div>
                        <p className="text-sm font-medium text-foreground">{order.restaurant_name || 'Order'}</p>
                        <p className="text-xs text-muted">
                          {new Date(order.created_at).toLocaleDateString()} · {order.items.length} item(s)
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-semibold text-foreground">
                          {order.country === 'INDIA' ? '₹' : '$'}{order.total_amount.toFixed(2)}
                        </p>
                        <span className={`${STATUS_COLORS[order.status]} text-[10px]`}>
                          {order.status}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </motion.div>
          </div>
        </>
      ) : null}
    </div>
  );
}
