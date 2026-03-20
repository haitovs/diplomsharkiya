"use client";

import { useTranslation } from "@/i18n/config";
import { LANGUAGES } from "@/i18n/config";
import type { Locale } from "@/types/event";

export function LanguageSelector() {
  const { locale, setLocale } = useTranslation();

  return (
    <select
      value={locale}
      onChange={(e) => setLocale(e.target.value as Locale)}
      className="bg-bg-secondary border border-border-subtle rounded-lg px-2 py-1.5 text-sm text-text-primary outline-none cursor-pointer focus:border-accent-primary"
    >
      {(Object.entries(LANGUAGES) as [Locale, string][]).map(([code, label]) => (
        <option key={code} value={code}>
          {code === "en" ? "🇬🇧" : code === "ru" ? "🇷🇺" : "🇹🇲"} {label}
        </option>
      ))}
    </select>
  );
}
