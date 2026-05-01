import type { Metadata } from 'next';
import './globals.css';
import { Toaster } from 'sonner';
import Providers from '@/components/Providers';

export const metadata: Metadata = {
  title: 'Slooze — Premium Food Ordering Platform',
  description: 'A luxury food ordering experience with role-based access control and country-based authorization.',
  keywords: ['food ordering', 'restaurant', 'RBAC', 'Slooze'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="noise-bg min-h-screen">
        <Providers>
        {children}
        </Providers>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: 'rgba(15, 23, 42, 0.9)',
              border: '1px solid rgba(255,255,255,0.08)',
              color: '#f1f5f9',
              backdropFilter: 'blur(20px)',
            },
          }}
        />
      </body>
    </html>
  );
}
