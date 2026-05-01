'use client';

import * as React from 'react';
import { useTheme } from 'next-themes';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, Monitor } from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

export function ThemeToggle() {
  const { theme, setTheme, systemTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="w-10 h-10 skeleton rounded-full" />;
  }

  const currentTheme = theme === 'system' ? systemTheme : theme;
  const isDark = currentTheme === 'dark';

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button
          className="relative flex items-center justify-center w-10 h-10 rounded-full bg-foreground/5 hover:bg-foreground/10 border border-border transition-colors overflow-hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-label="Toggle theme"
        >
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={isDark ? 'dark' : 'light'}
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 20, opacity: 0 }}
              transition={{ duration: 0.15 }}
            >
              {isDark ? <Moon className="w-5 h-5 text-foreground" /> : <Sun className="w-5 h-5 text-foreground" />}
            </motion.div>
          </AnimatePresence>
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="end"
          sideOffset={8}
          className="z-50 min-w-[8rem] overflow-hidden rounded-xl border border-border bg-card p-1 shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2"
        >
          <DropdownMenu.Item
            onClick={() => setTheme('light')}
            className={`relative flex cursor-pointer select-none items-center rounded-lg px-2 py-2 text-sm outline-none transition-colors hover:bg-foreground/5 focus:bg-foreground/5 focus:text-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 ${theme === 'light' ? 'bg-foreground/5 text-primary' : 'text-muted'}`}
          >
            <Sun className="mr-2 h-4 w-4" />
            <span>Light</span>
          </DropdownMenu.Item>
          <DropdownMenu.Item
            onClick={() => setTheme('dark')}
            className={`relative flex cursor-pointer select-none items-center rounded-lg px-2 py-2 text-sm outline-none transition-colors hover:bg-foreground/5 focus:bg-foreground/5 focus:text-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 ${theme === 'dark' ? 'bg-foreground/5 text-primary' : 'text-muted'}`}
          >
            <Moon className="mr-2 h-4 w-4" />
            <span>Dark</span>
          </DropdownMenu.Item>
          <DropdownMenu.Item
            onClick={() => setTheme('system')}
            className={`relative flex cursor-pointer select-none items-center rounded-lg px-2 py-2 text-sm outline-none transition-colors hover:bg-foreground/5 focus:bg-foreground/5 focus:text-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 ${theme === 'system' ? 'bg-foreground/5 text-primary' : 'text-muted'}`}
          >
            <Monitor className="mr-2 h-4 w-4" />
            <span>System</span>
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
