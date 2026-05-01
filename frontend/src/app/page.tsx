'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/lib/store';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { ChefHat, Lock, Mail, ArrowRight, Sparkles, Globe, Shield } from 'lucide-react';

const TEST_USERS = [
  { name: 'Nick Fury', email: 'nick.fury@shield.gov', role: 'ADMIN', country: 'AMERICA', color: 'from-violet-500 to-purple-600' },
  { name: 'Captain Marvel', email: 'carol.danvers@shield.gov', role: 'MANAGER', country: 'INDIA', color: 'from-pink-500 to-rose-600' },
  { name: 'Captain America', email: 'steve.rogers@shield.gov', role: 'MANAGER', country: 'AMERICA', color: 'from-blue-500 to-cyan-600' },
  { name: 'Thanos', email: 'thanos@titan.space', role: 'MEMBER', country: 'INDIA', color: 'from-purple-500 to-indigo-600' },
  { name: 'Thor', email: 'thor@asgard.realm', role: 'MEMBER', country: 'INDIA', color: 'from-amber-500 to-yellow-600' },
  { name: 'Travis', email: 'travis@avengers.org', role: 'MEMBER', country: 'AMERICA', color: 'from-emerald-500 to-teal-600' },
];

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await login({ email, password });
      toast.success('Welcome back!');
      router.push('/dashboard');
    } catch (err: any) {
      toast.error(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const quickLogin = async (userEmail: string) => {
    setEmail(userEmail);
    setPassword('password123');
    setIsLoading(true);
    try {
      await login({ email: userEmail, password: 'password123' });
      toast.success('Welcome back!');
      router.push('/dashboard');
    } catch (err: any) {
      toast.error(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-600/20 rounded-full blur-[128px] animate-float" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/15 rounded-full blur-[128px] animate-float" style={{ animationDelay: '-3s' }} />
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-pink-600/10 rounded-full blur-[128px] animate-float" style={{ animationDelay: '-1.5s' }} />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-10 w-full max-w-5xl grid lg:grid-cols-2 gap-8"
      >
        {/* Left — Login Form */}
        <div className="glass-card p-8 lg:p-10">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            {/* Logo */}
            <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center">
                <ChefHat className="w-5 h-5 text-foreground" />
              </div>
              <span className="text-xl font-display font-bold gradient-text">Slooze</span>
            </div>

            <h1 className="text-3xl font-display font-bold text-foreground mb-2">Welcome back</h1>
            <p className="text-muted mb-8">Sign in to your premium food ordering experience</p>

            <form onSubmit={handleLogin} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-muted mb-2">Email</label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="input-field pl-11"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-muted mb-2">Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="input-field pl-11"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full flex items-center justify-center gap-2 py-3"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    Sign In
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            {/* Features */}
            <div className="mt-8 pt-6 border-t border-border grid grid-cols-3 gap-4 text-center">
              <div>
                <Shield className="w-5 h-5 text-brand-400 mx-auto mb-1" />
                <p className="text-xs text-muted">RBAC</p>
              </div>
              <div>
                <Globe className="w-5 h-5 text-purple-400 mx-auto mb-1" />
                <p className="text-xs text-muted">Country ACL</p>
              </div>
              <div>
                <Sparkles className="w-5 h-5 text-pink-400 mx-auto mb-1" />
                <p className="text-xs text-muted">Premium UX</p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Right — Quick Login */}
        <div className="space-y-4">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="text-lg font-semibold text-foreground mb-1">Quick Login</h2>
            <p className="text-sm text-muted mb-4">Select a test user to sign in instantly</p>
          </motion.div>

          <div className="space-y-3">
            {TEST_USERS.map((user, i) => (
              <motion.button
                key={user.email}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.08 }}
                onClick={() => quickLogin(user.email)}
                disabled={isLoading}
                className="w-full glass-card-hover p-4 text-left flex items-center gap-4 group"
              >
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${user.color} flex items-center justify-center flex-shrink-0`}>
                  <span className="text-sm font-bold text-foreground">{user.name[0]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-foreground text-sm">{user.name}</p>
                  <p className="text-xs text-muted truncate">{user.email}</p>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <span className={`badge ${
                    user.role === 'ADMIN' ? 'badge-purple' :
                    user.role === 'MANAGER' ? 'badge-info' : 'badge-success'
                  }`}>
                    {user.role}
                  </span>
                  <span className="badge bg-foreground/5 text-muted border border-border text-[10px]">
                    {user.country === 'INDIA' ? '🇮🇳' : '🇺🇸'}
                  </span>
                </div>
                <ArrowRight className="w-4 h-4 text-muted group-hover:text-foreground group-hover:translate-x-1 transition-all" />
              </motion.button>
            ))}
          </div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.9 }}
            className="text-xs text-muted text-center pt-2"
          >
            All test users use password: <code className="text-muted">password123</code>
          </motion.p>
        </div>
      </motion.div>
    </div>
  );
}
