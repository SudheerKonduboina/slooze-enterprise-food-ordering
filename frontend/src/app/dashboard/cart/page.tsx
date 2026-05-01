'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { useCart, useAuth } from '@/lib/store';
import { api } from '@/lib/api';
import { hasPermission } from '@/lib/types';
import type { PaymentMethod } from '@/lib/types';
import { toast } from 'sonner';
import {
  Minus, Plus, Trash2, ShoppingBag, CreditCard,
  ArrowRight, ShoppingCart, ArrowLeft, Sparkles
} from 'lucide-react';
import Link from 'next/link';

export default function CartPage() {
  const { items, updateQuantity, removeItem, clearCart, total, itemCount, restaurantId } = useCart();
  const { user } = useAuth();
  const router = useRouter();
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState<string>('');
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const [loadingPayments, setLoadingPayments] = useState(true);

  const canCheckout = user ? hasPermission(user.role as any, 'checkout') : false;
  const currencySymbol = user?.country === 'INDIA' ? '₹' : '$';

  useEffect(() => {
    api.getPaymentMethods()
      .then((methods) => {
        setPaymentMethods(methods);
        const defaultMethod = methods.find((m) => m.is_default);
        if (defaultMethod) setSelectedPaymentMethod(defaultMethod.id);
        else if (methods.length > 0) setSelectedPaymentMethod(methods[0].id);
      })
      .catch(console.error)
      .finally(() => setLoadingPayments(false));
  }, []);

  const handleCheckout = async () => {
    if (!restaurantId || items.length === 0) return;
    if (!selectedPaymentMethod) {
      toast.error('Please select a payment method');
      return;
    }

    setIsCheckingOut(true);
    try {
      // Create order
      const order = await api.createOrder(
        restaurantId,
        items.map((i) => ({
          menu_item_id: i.menuItem.id,
          quantity: i.quantity,
        }))
      );

      // Checkout
      await api.checkoutOrder(order.id, selectedPaymentMethod);

      clearCart();
      toast.success('Order placed successfully! 🎉');
      router.push('/dashboard/orders');
    } catch (err: any) {
      toast.error(err.message || 'Checkout failed');
    } finally {
      setIsCheckingOut(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="max-w-2xl mx-auto text-center py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <ShoppingCart className="w-16 h-16 text-muted mx-auto mb-6" />
          <h1 className="text-2xl font-display font-bold text-foreground mb-3">Your cart is empty</h1>
          <p className="text-muted mb-8">Browse our restaurants and add delicious items to your cart.</p>
          <Link href="/dashboard/restaurants" className="btn-primary inline-flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" /> Browse Restaurants
          </Link>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-display font-bold text-foreground mb-1">Your Cart</h1>
        <p className="text-muted">{itemCount} item(s) · {currencySymbol}{total.toFixed(2)}</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-3">
          {items.map((item, i) => (
            <motion.div
              key={item.menuItem.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card p-4 flex gap-4"
            >
              <div className="w-20 h-20 rounded-xl overflow-hidden flex-shrink-0">
                <div
                  className="w-full h-full bg-cover bg-center"
                  style={{
                    backgroundImage: item.menuItem.image_url
                      ? `url(${item.menuItem.image_url})`
                      : 'linear-gradient(135deg, #1e293b, #334155)',
                  }}
                />
              </div>

              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-semibold text-foreground">{item.menuItem.name}</h3>
                <p className="text-xs text-muted mt-0.5">{currencySymbol}{item.menuItem.price} each</p>

                <div className="flex items-center justify-between mt-3">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => updateQuantity(item.menuItem.id, item.quantity - 1)}
                      className="w-7 h-7 rounded-lg bg-foreground/5 hover:bg-foreground/10 flex items-center justify-center transition-colors"
                    >
                      <Minus className="w-3 h-3 text-muted" />
                    </button>
                    <span className="w-8 text-center text-sm font-medium text-foreground">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.menuItem.id, item.quantity + 1)}
                      className="w-7 h-7 rounded-lg bg-foreground/5 hover:bg-foreground/10 flex items-center justify-center transition-colors"
                    >
                      <Plus className="w-3 h-3 text-muted" />
                    </button>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-bold text-foreground">
                      {currencySymbol}{(item.menuItem.price * item.quantity).toFixed(2)}
                    </span>
                    <button
                      onClick={() => removeItem(item.menuItem.id)}
                      className="w-7 h-7 rounded-lg bg-red-500/10 hover:bg-red-500/20 flex items-center justify-center transition-colors"
                    >
                      <Trash2 className="w-3 h-3 text-red-400" />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}

          <button
            onClick={clearCart}
            className="text-sm text-muted hover:text-red-400 transition-colors flex items-center gap-1.5"
          >
            <Trash2 className="w-3 h-3" /> Clear cart
          </button>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card p-6 sticky top-24"
          >
            <h2 className="text-lg font-semibold text-foreground mb-4">Order Summary</h2>

            <div className="space-y-3 mb-6">
              <div className="flex justify-between text-sm">
                <span className="text-muted">Subtotal</span>
                <span className="text-foreground">{currencySymbol}{total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted">Delivery</span>
                <span className="text-emerald-400">Free</span>
              </div>
              <div className="border-t border-border pt-3 flex justify-between">
                <span className="font-semibold text-foreground">Total</span>
                <span className="font-bold text-lg text-foreground">{currencySymbol}{total.toFixed(2)}</span>
              </div>
            </div>

            {canCheckout ? (
              <>
                {/* Payment Method Selection */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-muted mb-2">
                    <CreditCard className="w-4 h-4 inline mr-1.5" />
                    Payment Method
                  </label>
                  {loadingPayments ? (
                    <div className="skeleton h-10 rounded-xl" />
                  ) : paymentMethods.length === 0 ? (
                    <div className="text-xs text-muted p-3 glass-card text-center">
                      No payment methods. Ask an Admin to add one.
                    </div>
                  ) : (
                    <select
                      value={selectedPaymentMethod}
                      onChange={(e) => setSelectedPaymentMethod(e.target.value)}
                      className="input-field py-2.5 text-sm"
                    >
                      {paymentMethods.map((m) => (
                        <option key={m.id} value={m.id} className="bg-card">
                          {m.label} ({m.method_type})
                        </option>
                      ))}
                    </select>
                  )}
                </div>

                <button
                  onClick={handleCheckout}
                  disabled={isCheckingOut || !selectedPaymentMethod}
                  className="btn-primary w-full flex items-center justify-center gap-2 py-3"
                >
                  {isCheckingOut ? (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      Place Order · {currencySymbol}{total.toFixed(2)}
                    </>
                  )}
                </button>
              </>
            ) : (
              <div className="text-center text-sm text-muted p-4 glass-card">
                <ShoppingBag className="w-8 h-8 text-muted mx-auto mb-2" />
                <p>As a <strong>{user?.role}</strong>, you can create orders but checkout requires a Manager or Admin.</p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
