'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/store';
import { hasPermission } from '@/lib/types';
import type { Order } from '@/lib/types';
import { toast } from 'sonner';
import {
  ShoppingBag, Package, Clock, CheckCircle, XCircle,
  ChefHat, Truck, AlertCircle, CreditCard
} from 'lucide-react';

const STATUS_CONFIG: Record<string, { label: string; color: string; icon: any; badge: string }> = {
  CART: { label: 'In Cart', color: 'text-amber-400', icon: ShoppingBag, badge: 'badge-warning' },
  PLACED: { label: 'Placed', color: 'text-blue-400', icon: Package, badge: 'badge-info' },
  CONFIRMED: { label: 'Confirmed', color: 'text-cyan-400', icon: CheckCircle, badge: 'badge-info' },
  PREPARING: { label: 'Preparing', color: 'text-purple-400', icon: ChefHat, badge: 'badge-purple' },
  DELIVERED: { label: 'Delivered', color: 'text-emerald-400', icon: Truck, badge: 'badge-success' },
  CANCELLED: { label: 'Cancelled', color: 'text-red-400', icon: XCircle, badge: 'badge-danger' },
};

export default function OrdersPage() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState<string | null>(null);

  const canCancel = user ? hasPermission(user.role as any, 'cancel_order') : false;
  const currencySymbol = user?.country === 'INDIA' ? '₹' : '$';

  useEffect(() => {
    api.getOrders()
      .then((res) => setOrders(res.orders))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleCancel = async (orderId: string) => {
    setCancellingId(orderId);
    try {
      const updated = await api.cancelOrder(orderId);
      setOrders((prev) => prev.map((o) => (o.id === orderId ? updated : o)));
      toast.success('Order cancelled successfully');
    } catch (err: any) {
      toast.error(err.message || 'Failed to cancel order');
    } finally {
      setCancellingId(null);
    }
  };

  if (loading) {
    return (
      <div>
        <h1 className="text-2xl font-display font-bold text-foreground mb-6">My Orders</h1>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton h-40 rounded-2xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-display font-bold text-foreground mb-1">My Orders</h1>
        <p className="text-muted">Track and manage your food orders</p>
      </div>

      {orders.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <Package className="w-12 h-12 text-muted mx-auto mb-4" />
          <h2 className="text-lg font-semibold text-foreground mb-2">No orders yet</h2>
          <p className="text-muted mb-6">Start by browsing restaurants and placing your first order!</p>
          <a href="/dashboard/restaurants" className="btn-primary inline-flex items-center gap-2">
            Browse Restaurants
          </a>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order, i) => {
            const statusConfig = STATUS_CONFIG[order.status] || STATUS_CONFIG.CART;
            const StatusIcon = statusConfig.icon;
            const canCancelThis = canCancel &&
              ['CART', 'PLACED', 'CONFIRMED'].includes(order.status);

            return (
              <motion.div
                key={order.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="glass-card p-5"
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <div className={`w-9 h-9 rounded-xl bg-foreground/5 flex items-center justify-center ${statusConfig.color}`}>
                        <StatusIcon className="w-4 h-4" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-foreground">{order.restaurant_name || 'Order'}</h3>
                        <p className="text-xs text-muted">
                          {new Date(order.created_at).toLocaleString()} · ID: {order.id.slice(0, 8)}
                        </p>
                      </div>
                      <span className={statusConfig.badge}>{statusConfig.label}</span>
                    </div>

                    {/* Items */}
                    <div className="pl-12 space-y-1.5">
                      {order.items.map((item) => (
                        <div key={item.id} className="flex justify-between text-sm">
                          <span className="text-muted">
                            {item.quantity}× {item.menu_item_name || 'Item'}
                          </span>
                          <span className="text-muted">{currencySymbol}{item.subtotal.toFixed(2)}</span>
                        </div>
                      ))}
                    </div>

                    {/* Payment Info */}
                    {order.payment && (
                      <div className="pl-12 mt-3 flex items-center gap-2 text-xs text-muted">
                        <CreditCard className="w-3 h-3" />
                        Payment: {order.payment.status}
                        {order.payment.transaction_id && ` · ${order.payment.transaction_id}`}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col items-end gap-2">
                    <p className="text-lg font-bold text-foreground">{currencySymbol}{order.total_amount.toFixed(2)}</p>
                    {canCancelThis && (
                      <button
                        onClick={() => handleCancel(order.id)}
                        disabled={cancellingId === order.id}
                        className="text-xs text-red-400 hover:text-red-300 flex items-center gap-1 transition-colors"
                      >
                        {cancellingId === order.id ? (
                          <div className="w-3 h-3 border border-red-400/30 border-t-red-400 rounded-full animate-spin" />
                        ) : (
                          <XCircle className="w-3 h-3" />
                        )}
                        Cancel Order
                      </button>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
