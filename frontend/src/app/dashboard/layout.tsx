'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useAuth, useCart } from '@/lib/store';
import { hasPermission } from '@/lib/types';
import {
  LayoutDashboard, UtensilsCrossed, ShoppingBag, CreditCard,
  Users, LogOut, ChefHat, ShoppingCart, Menu, X, Globe, Shield
} from 'lucide-react';
import { useState } from 'react';

import { ThemeToggle } from '@/components/theme-toggle';

const NAV_ITEMS = [
  { label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard, permission: 'view_dashboard' },
  { label: 'Restaurants', href: '/dashboard/restaurants', icon: UtensilsCrossed, permission: 'view_restaurants' },
  { label: 'My Orders', href: '/dashboard/orders', icon: ShoppingBag, permission: 'view_own_orders' },
  { label: 'Payments', href: '/dashboard/payments', icon: CreditCard, permission: 'add_payment_method' },
  { label: 'Users', href: '/dashboard/users', icon: Users, permission: 'manage_users' },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, logout, isAuthenticated, isLoading } = useAuth();
  const { itemCount } = useCart();
  const router = useRouter();
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin" />
      </div>
    );
  }

  const visibleNavItems = NAV_ITEMS.filter(
    (item) => hasPermission(user.role as any, item.permission)
  );

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <div className="min-h-screen flex bg-background text-foreground transition-colors duration-300">
      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-72 bg-card/80 backdrop-blur-xl border-r border-border
        transform transition-transform duration-300 lg:translate-x-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 flex items-center justify-between">
            <Link href="/dashboard" className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center">
                <ChefHat className="w-5 h-5 text-foreground" />
              </div>
              <span className="text-lg font-display font-bold gradient-text">Slooze</span>
            </Link>
            <button onClick={() => setSidebarOpen(false)} className="lg:hidden text-muted hover:text-foreground">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* User Info */}
          <div className="mx-4 mb-6 p-4 glass-card">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center">
                <span className="text-sm font-bold text-foreground">{user.full_name[0]}</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-dynamic truncate">{user.full_name}</p>
                <div className="flex items-center gap-1.5 mt-0.5">
                  <span className={`badge text-[10px] ${
                    user.role === 'ADMIN' ? 'badge-purple' :
                    user.role === 'MANAGER' ? 'badge-info' : 'badge-success'
                  }`}>{user.role}</span>
                  <span className="text-xs text-muted">
                    {user.country === 'INDIA' ? '🇮🇳' : '🇺🇸'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 space-y-1">
            {visibleNavItems.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setSidebarOpen(false)}
                  className={`
                    flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium
                    transition-all duration-200 group
                    ${isActive
                      ? 'bg-brand-500/10 text-brand-500 border border-brand-500/20'
                      : 'text-muted hover:text-foreground hover:bg-foreground/5'
                    }
                  `}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-brand-500' : 'text-muted group-hover:text-foreground'}`} />
                  {item.label}
                </Link>
              );
            })}

            {/* Cart Link */}
            <Link
              href="/dashboard/cart"
              onClick={() => setSidebarOpen(false)}
              className={`
                flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium
                transition-all duration-200 group relative
                ${pathname === '/dashboard/cart'
                  ? 'bg-brand-500/10 text-brand-500 border border-brand-500/20'
                  : 'text-muted hover:text-foreground hover:bg-foreground/5'
                }
              `}
            >
              <ShoppingCart className="w-4 h-4" />
              Cart
              {itemCount > 0 && (
                <span className="absolute right-3 w-5 h-5 rounded-full bg-brand-500 text-white text-[10px] font-bold flex items-center justify-center">
                  {itemCount}
                </span>
              )}
            </Link>
          </nav>

          {/* Logout */}
          <div className="p-4 mt-auto">
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium
                         text-muted hover:text-red-500 hover:bg-red-500/10 transition-all duration-200"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        </div>
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="flex-1 min-w-0">
        {/* Top Bar */}
        <header className="sticky top-0 z-30 h-16 flex items-center justify-between px-6
                           bg-card/60 backdrop-blur-xl border-b border-border">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden text-muted hover:text-foreground"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="hidden lg:flex items-center gap-2 text-sm text-muted">
            <Globe className="w-4 h-4" />
            <span>{user.country === 'INDIA' ? 'India Region' : 'America Region'}</span>
            <span className="mx-2 text-muted">·</span>
            <Shield className="w-4 h-4" />
            <span>{user.role}</span>
          </div>

          <div className="flex items-center gap-4 ml-auto lg:ml-0">
            <ThemeToggle />
            <Link href="/dashboard/cart" className="relative btn-ghost p-2">
              <ShoppingCart className="w-5 h-5" />
              {itemCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-brand-500 text-white text-[10px] font-bold flex items-center justify-center animate-scale-in">
                  {itemCount}
                </span>
              )}
            </Link>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6 lg:p-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={pathname}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.3 }}
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
