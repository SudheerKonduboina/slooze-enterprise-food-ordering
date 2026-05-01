'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '@/lib/api';
import { useCart, useAuth } from '@/lib/store';
import type { Restaurant, MenuItem } from '@/lib/types';
import { toast } from 'sonner';
import {
  Star, Clock, ArrowLeft, Plus, Minus, ShoppingCart,
  Leaf, ChefHat, Check
} from 'lucide-react';
import Link from 'next/link';

export default function RestaurantDetailPage() {
  const params = useParams();
  const restaurantId = params.id as string;
  const { user } = useAuth();
  const { addItem, items: cartItems, itemCount, total } = useCart();

  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [addedItems, setAddedItems] = useState<Set<string>>(new Set());

  useEffect(() => {
    Promise.all([
      api.getRestaurant(restaurantId),
      api.getMenu(restaurantId),
    ])
      .then(([rest, menu]) => {
        setRestaurant(rest);
        setMenuItems(menu.menu_items);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [restaurantId]);

  const categories = Array.from(new Set(menuItems.map((item) => item.category)));
  const filteredItems = selectedCategory
    ? menuItems.filter((item) => item.category === selectedCategory)
    : menuItems;

  const handleAddToCart = (item: MenuItem) => {
    addItem(item, 1);
    setAddedItems((prev) => new Set(prev).add(item.id));
    toast.success(`${item.name} added to cart`);
    setTimeout(() => {
      setAddedItems((prev) => {
        const next = new Set(prev);
        next.delete(item.id);
        return next;
      });
    }, 1500);
  };

  const currencySymbol = user?.country === 'INDIA' ? '₹' : '$';

  if (loading) {
    return (
      <div>
        <div className="skeleton h-64 rounded-2xl mb-6" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-40 rounded-2xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!restaurant) {
    return (
      <div className="text-center py-20">
        <p className="text-muted">Restaurant not found</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="relative h-64 rounded-2xl overflow-hidden mb-8">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: restaurant.image_url
              ? `url(${restaurant.image_url})`
              : 'linear-gradient(135deg, #1e293b, #334155)',
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-surface-950 via-surface-950/60 to-transparent" />

        <div className="absolute bottom-0 left-0 right-0 p-6">
          <Link href="/dashboard/restaurants" className="inline-flex items-center gap-2 text-muted hover:text-foreground text-sm mb-4 transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to restaurants
          </Link>
          <h1 className="text-3xl font-display font-bold text-foreground mb-2">{restaurant.name}</h1>
          <div className="flex items-center gap-4 text-sm text-muted">
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
              {restaurant.rating}
            </div>
            <span>·</span>
            <span>{restaurant.cuisine_type}</span>
            <span>·</span>
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {restaurant.delivery_time_mins} min delivery
            </div>
            <span>·</span>
            <span>{restaurant.country === 'INDIA' ? '🇮🇳 India' : '🇺🇸 USA'}</span>
          </div>
        </div>
      </div>

      {/* Category Tabs */}
      {categories.length > 0 && (
        <div className="flex items-center gap-2 mb-6 overflow-x-auto pb-2 scrollbar-none">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all whitespace-nowrap ${
              !selectedCategory
                ? 'bg-brand-500/10 text-brand-400 border border-brand-500/20'
                : 'text-muted hover:text-foreground hover:bg-foreground/5 border border-transparent'
            }`}
          >
            All ({menuItems.length})
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all whitespace-nowrap ${
                selectedCategory === cat
                  ? 'bg-brand-500/10 text-brand-400 border border-brand-500/20'
                  : 'text-muted hover:text-foreground hover:bg-foreground/5 border border-transparent'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}

      {/* Menu Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AnimatePresence mode="popLayout">
          {filteredItems.map((item, i) => {
            const isAdded = addedItems.has(item.id);
            const cartItem = cartItems.find((ci) => ci.menuItem.id === item.id);
            return (
              <motion.div
                key={item.id}
                layout
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ delay: i * 0.03 }}
                className="glass-card-hover p-4 flex gap-4"
              >
                {/* Image */}
                <div className="w-28 h-28 rounded-xl overflow-hidden flex-shrink-0 relative">
                  <div
                    className="absolute inset-0 bg-cover bg-center"
                    style={{
                      backgroundImage: item.image_url
                        ? `url(${item.image_url})`
                        : 'linear-gradient(135deg, #1e293b, #334155)',
                    }}
                  />
                  {item.is_vegetarian && (
                    <div className="absolute top-1 left-1 w-5 h-5 rounded-md bg-emerald-500/80 flex items-center justify-center">
                      <Leaf className="w-3 h-3 text-foreground" />
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0 flex flex-col">
                  <h3 className="text-sm font-semibold text-foreground mb-1 line-clamp-1">{item.name}</h3>
                  <p className="text-xs text-muted line-clamp-2 mb-auto">{item.description}</p>

                  <div className="flex items-center justify-between mt-3">
                    <div>
                      <span className="text-lg font-bold text-foreground">{currencySymbol}{item.price}</span>
                      <div className="flex items-center gap-1 text-[10px] text-muted mt-0.5">
                        <Clock className="w-2.5 h-2.5" />
                        {item.preparation_time_mins} min
                      </div>
                    </div>

                    {cartItem ? (
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-muted bg-foreground/5 px-2 py-1 rounded-lg">
                          {cartItem.quantity} in cart
                        </span>
                        <button
                          onClick={() => handleAddToCart(item)}
                          className="w-8 h-8 rounded-lg bg-brand-500/10 text-brand-400 flex items-center justify-center hover:bg-brand-500/20 transition-colors"
                        >
                          <Plus className="w-4 h-4" />
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => handleAddToCart(item)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-300 ${
                          isAdded
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : 'bg-brand-500/10 text-brand-400 border border-brand-500/20 hover:bg-brand-500/20'
                        }`}
                      >
                        {isAdded ? (
                          <><Check className="w-3 h-3" /> Added</>
                        ) : (
                          <><Plus className="w-3 h-3" /> Add</>
                        )}
                      </button>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Floating Cart Bar */}
      <AnimatePresence>
        {itemCount > 0 && (
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50"
          >
            <Link href="/dashboard/cart">
              <div className="glass-card gradient-border px-6 py-3 flex items-center gap-4 cursor-pointer hover:scale-[1.02] transition-transform">
                <div className="w-10 h-10 rounded-xl bg-brand-500 flex items-center justify-center">
                  <ShoppingCart className="w-5 h-5 text-foreground" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-foreground">{itemCount} item(s) in cart</p>
                  <p className="text-xs text-muted">{currencySymbol}{total.toFixed(2)}</p>
                </div>
                <div className="btn-primary py-2 px-4 text-sm">View Cart</div>
              </div>
            </Link>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
