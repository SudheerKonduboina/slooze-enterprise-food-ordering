'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '@/lib/api';
import type { User } from '@/lib/types';
import { Users, Shield, Globe } from 'lucide-react';

const ROLE_COLORS: Record<string, string> = {
  ADMIN: 'badge-purple',
  MANAGER: 'badge-info',
  MEMBER: 'badge-success',
};

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getUsers()
      .then((res) => setUsers(res.users))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-display font-bold text-foreground mb-1">User Management</h1>
        <p className="text-muted">View and manage all platform users</p>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-16 rounded-2xl" />
          ))}
        </div>
      ) : (
        <div className="glass-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left px-6 py-4 text-xs font-medium text-muted uppercase tracking-wider">User</th>
                  <th className="text-left px-6 py-4 text-xs font-medium text-muted uppercase tracking-wider">Email</th>
                  <th className="text-left px-6 py-4 text-xs font-medium text-muted uppercase tracking-wider">Role</th>
                  <th className="text-left px-6 py-4 text-xs font-medium text-muted uppercase tracking-wider">Country</th>
                  <th className="text-left px-6 py-4 text-xs font-medium text-muted uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user, i) => (
                  <motion.tr
                    key={user.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: i * 0.05 }}
                    className="border-b border-border hover:bg-white/[0.02] transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center">
                          <span className="text-xs font-bold text-foreground">{user.full_name[0]}</span>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-foreground">{user.full_name}</p>
                          <p className="text-xs text-muted">@{user.username}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-muted">{user.email}</td>
                    <td className="px-6 py-4">
                      <span className={ROLE_COLORS[user.role] || 'badge-info'}>{user.role}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-muted">
                        {user.country === 'INDIA' ? '🇮🇳 India' : '🇺🇸 America'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={user.is_active ? 'badge-success' : 'badge-danger'}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
