'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/store';
import type { PaymentMethod, PaymentMethodType } from '@/lib/types';
import { toast } from 'sonner';
import {
  CreditCard, Plus, Trash2, Star, Wallet
} from 'lucide-react';

const METHOD_ICONS: Record<string, string> = {
  CREDIT_CARD: '💳',
  DEBIT_CARD: '💳',
  UPI: '📱',
  NET_BANKING: '🏦',
  WALLET: '👛',
};

export default function PaymentsPage() {
  const { user } = useAuth();
  const [methods, setMethods] = useState<PaymentMethod[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    method_type: 'CREDIT_CARD' as string,
    label: '',
    details: '',
    is_default: false,
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.getPaymentMethods()
      .then(setMethods)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const newMethod = await api.createPaymentMethod(formData);
      setMethods((prev) => [...prev, newMethod]);
      setShowForm(false);
      setFormData({ method_type: 'CREDIT_CARD', label: '', details: '', is_default: false });
      toast.success('Payment method added');
    } catch (err: any) {
      toast.error(err.message || 'Failed to add payment method');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.deletePaymentMethod(id);
      setMethods((prev) => prev.filter((m) => m.id !== id));
      toast.success('Payment method deleted');
    } catch (err: any) {
      toast.error(err.message || 'Failed to delete payment method');
    }
  };

  return (
    <div className="max-w-3xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground mb-1">Payment Methods</h1>
          <p className="text-muted">Manage your payment methods</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Add Method
        </button>
      </div>

      {/* Add Form */}
      {showForm && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="glass-card p-6 mb-6"
        >
          <h2 className="text-lg font-semibold text-foreground mb-4">Add Payment Method</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-muted mb-2">Type</label>
                <select
                  value={formData.method_type}
                  onChange={(e) => setFormData((p) => ({ ...p, method_type: e.target.value }))}
                  className="input-field"
                >
                  <option value="CREDIT_CARD" className="bg-card">Credit Card</option>
                  <option value="DEBIT_CARD" className="bg-card">Debit Card</option>
                  <option value="UPI" className="bg-card">UPI</option>
                  <option value="NET_BANKING" className="bg-card">Net Banking</option>
                  <option value="WALLET" className="bg-card">Wallet</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-muted mb-2">Label</label>
                <input
                  type="text"
                  value={formData.label}
                  onChange={(e) => setFormData((p) => ({ ...p, label: e.target.value }))}
                  placeholder="e.g., Personal Visa"
                  className="input-field"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-muted mb-2">Details</label>
              <input
                type="text"
                value={formData.details}
                onChange={(e) => setFormData((p) => ({ ...p, details: e.target.value }))}
                placeholder="e.g., **** **** **** 1234"
                className="input-field"
              />
            </div>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="is_default"
                checked={formData.is_default}
                onChange={(e) => setFormData((p) => ({ ...p, is_default: e.target.checked }))}
                className="w-4 h-4 rounded"
              />
              <label htmlFor="is_default" className="text-sm text-muted">Set as default</label>
            </div>
            <div className="flex justify-end gap-3">
              <button type="button" onClick={() => setShowForm(false)} className="btn-ghost">Cancel</button>
              <button type="submit" disabled={submitting} className="btn-primary">
                {submitting ? 'Adding...' : 'Add Method'}
              </button>
            </div>
          </form>
        </motion.div>
      )}

      {/* Methods List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2].map((i) => <div key={i} className="skeleton h-20 rounded-2xl" />)}
        </div>
      ) : methods.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <Wallet className="w-12 h-12 text-muted mx-auto mb-4" />
          <h2 className="text-lg font-semibold text-foreground mb-2">No payment methods</h2>
          <p className="text-muted">Add a payment method to checkout orders.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {methods.map((method, i) => (
            <motion.div
              key={method.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card p-4 flex items-center gap-4"
            >
              <div className="w-12 h-12 rounded-xl bg-foreground/5 flex items-center justify-center text-2xl">
                {METHOD_ICONS[method.method_type] || '💳'}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-foreground">{method.label}</h3>
                  {method.is_default && (
                    <span className="badge-info text-[10px]">
                      <Star className="w-2.5 h-2.5 mr-0.5" /> Default
                    </span>
                  )}
                </div>
                <p className="text-xs text-muted mt-0.5">
                  {method.method_type.replace('_', ' ')} · {method.details || 'No details'}
                </p>
              </div>
              <button
                onClick={() => handleDelete(method.id)}
                className="w-8 h-8 rounded-lg bg-red-500/10 hover:bg-red-500/20 flex items-center justify-center transition-colors"
              >
                <Trash2 className="w-4 h-4 text-red-400" />
              </button>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
