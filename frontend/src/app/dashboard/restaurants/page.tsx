'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { api } from '@/lib/api';
import type { Restaurant } from '@/lib/types';
import { Star, Clock, MapPin, ChevronRight, Search, UtensilsCrossed } from 'lucide-react';

export default function RestaurantsPage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    api.getRestaurants()
      .then((res) => setRestaurants(res.restaurants))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = restaurants.filter(
    (r) =>
      r.name.toLowerCase().includes(search.toLowerCase()) ||
      r.cuisine_type.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground mb-1">Restaurants</h1>
          <p className="text-muted">Discover amazing food from your region</p>
        </div>
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
          <input
            type="text"
            placeholder="Search restaurants..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field pl-11 py-2.5 text-sm"
          />
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="skeleton h-80 rounded-2xl" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <UtensilsCrossed className="w-12 h-12 text-muted mx-auto mb-4" />
          <h2 className="text-lg font-semibold text-foreground mb-2">No restaurants found</h2>
          <p className="text-muted">Try adjusting your search or check back later.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((restaurant, i) => (
            <motion.div
              key={restaurant.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Link href={`/dashboard/restaurants/${restaurant.id}`}>
                <div className="glass-card-hover overflow-hidden group cursor-pointer">
                  {/* Image */}
                  <div className="relative h-48 overflow-hidden">
                    <div
                      className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-110"
                      style={{
                        backgroundImage: restaurant.image_url
                          ? `url(${restaurant.image_url})`
                          : 'linear-gradient(135deg, #1e293b, #334155)',
                      }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-surface-950 via-surface-950/40 to-transparent" />

                    {/* Country Badge */}
                    <div className="absolute top-3 right-3">
                      <span className="badge bg-black/40 backdrop-blur-sm text-foreground border-border text-xs">
                        {restaurant.country === 'INDIA' ? '🇮🇳 India' : '🇺🇸 USA'}
                      </span>
                    </div>

                    {/* Rating */}
                    <div className="absolute bottom-3 left-3 flex items-center gap-1.5">
                      <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-500/20 backdrop-blur-sm border border-amber-500/30">
                        <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                        <span className="text-xs font-semibold text-amber-300">{restaurant.rating}</span>
                      </div>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-5">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-foreground group-hover:text-brand-400 transition-colors line-clamp-1">
                        {restaurant.name}
                      </h3>
                      <ChevronRight className="w-4 h-4 text-muted group-hover:text-brand-400 group-hover:translate-x-1 transition-all flex-shrink-0 mt-1" />
                    </div>

                    <p className="text-sm text-muted line-clamp-2 mb-4">
                      {restaurant.description}
                    </p>

                    <div className="flex items-center gap-4 text-xs text-muted">
                      <div className="flex items-center gap-1">
                        <UtensilsCrossed className="w-3 h-3" />
                        {restaurant.cuisine_type}
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {restaurant.delivery_time_mins} min
                      </div>
                      {restaurant.menu_item_count && restaurant.menu_item_count > 0 && (
                        <div className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {restaurant.menu_item_count} items
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
