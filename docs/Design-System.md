# Enterprise Design System Documentation

Slooze uses a token-based Design System that ensures visual consistency, accessibility, and high performance across its Light and Dark themes.

## 🎨 Token Architecture

All design tokens are defined as CSS variables in `src/app/globals.css`. These variables are consumed by Tailwind CSS in `tailwind.config.js`.

### Color Palette (HSL)
- **Primary:** `hsl(var(--primary))` - High-intent action color (Blue/Indigo).
- **Background:** `hsl(var(--background))` - Core canvas color.
- **Surface:** `hsl(var(--card))` - Elevation layer for cards and menus.
- **Border:** `hsl(var(--border))` - Subtle containment lines.

### Layout & Shape
- **Radius:** `--radius` (1rem) - Consistent rounding for all containers.
- **Shadows:** 
  - `--shadow-sm`: Subtle elevation.
  - `--shadow-md`: Standard card elevation.
  - `--shadow-lg`: Floating menus and dropdowns.

---

## 🌓 Theming System

Powered by `next-themes` and a critical blocking script in `layout.tsx`.

### FOUC Prevention
To prevent the "Flash of Unstyled Content", a raw script is injected into the `<head>` of the application. This script reads the `localStorage` theme preference and applies the `.dark` class to the `<html>` tag before React hydration begins.

### System Auto-Sync
If the user selects **System** mode, the application uses `matchMedia` event listeners to respond instantly to changes in the operating system's appearance settings without a page reload.

---

## 🏗️ Core Components

### 1. Glassmorphism Card
- **Styles:** `bg-glass`, `backdrop-blur-xl`, `border-glass`.
- **Usage:** Used for the Login container and Dashboard summary cards to provide a cinematic, premium feel.

### 2. Theme Toggle (Radix UI)
- **Implementation:** Uses `@radix-ui/react-dropdown-menu`.
- **Animations:** Powered by `tailwindcss-animate` for scale-in effects and `framer-motion` for SVG icon transitions.

---

## ♿ Accessibility (WCAG)

The Design System is built with a "Privacy and Access First" mindset:
- **Focus States:** Every interactive element has a visible `ring-2` focus state using the `--ring` token.
- **Contrast:** Colors are audited to ensure a minimum 4.5:1 contrast ratio for normal text.
- **ARIA:** All theme-switching and navigation components utilize semantic HTML and ARIA roles.
