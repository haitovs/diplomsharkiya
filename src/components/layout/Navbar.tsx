"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { useTranslation } from "@/i18n/config";
import { LanguageSelector } from "./LanguageSelector";

const NAV_ITEMS = [
  { href: "/", key: "nav_home", icon: "🏠" },
  { href: "/events", key: "nav_events", icon: "📋" },
  { href: "/map", key: "nav_map", icon: "🗺️" },
  { href: "/saved", key: "nav_saved", icon: "⭐" },
  { href: "/about", key: "nav_about", icon: "ℹ️" },
  { href: "/admin", key: "nav_admin", icon: "🔧" },
];

export function Navbar() {
  const { t } = useTranslation();
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-border-subtle shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <span className="text-2xl">🎟️</span>
            <span className="text-xl font-bold gradient-text hidden sm:inline">EventHub</span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-accent-primary/15 text-accent-primary"
                      : "text-text-secondary hover:text-text-primary hover:bg-slate-100"
                  }`}
                >
                  {item.icon} {t(item.key)}
                </Link>
              );
            })}
          </div>

          <div className="flex items-center gap-3">
            <LanguageSelector />
            <button
              className="md:hidden p-2 text-text-secondary hover:text-text-primary"
              onClick={() => setMobileOpen(!mobileOpen)}
            >
              {mobileOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile nav */}
      {mobileOpen && (
        <div className="md:hidden border-t border-border-subtle bg-white pb-4">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className={`block px-6 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-accent-primary/10 text-accent-primary"
                    : "text-text-secondary hover:text-text-primary hover:bg-slate-100"
                }`}
              >
                {item.icon} {t(item.key)}
              </Link>
            );
          })}
        </div>
      )}
    </nav>
  );
}
