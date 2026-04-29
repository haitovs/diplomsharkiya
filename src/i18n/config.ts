"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import en from "./en.json";
import ru from "./ru.json";
import tk from "./tk.json";
import type { Event, Locale } from "@/types/event";

const messages: Record<Locale, Record<string, string>> = { en, ru, tk };

export const LANGUAGES: Record<Locale, string> = {
  en: "English",
  ru: "Русский",
  tk: "Türkmen",
};

interface I18nStore {
  locale: Locale;
  setLocale: (locale: Locale) => void;
}

export const useI18nStore = create<I18nStore>()(
  persist(
    (set) => ({
      locale: "tk",
      setLocale: (locale) => set({ locale }),
    }),
    { name: "sharkiya-locale" }
  )
);

export function useTranslation() {
  const { locale, setLocale } = useI18nStore();

  function t(key: string, params?: Record<string, string | number>): string {
    let text = messages[locale]?.[key] || messages.en[key] || key;
    if (params) {
      Object.entries(params).forEach(([k, v]) => {
        text = text.replace(`{${k}}`, String(v));
      });
    }
    return text;
  }

  function tCat(category: string): string {
    return t(`cat_${category}`) || category;
  }

  function tCity(city: string): string {
    const key = `city_${city}`;
    const translated = messages[locale]?.[key];
    return translated || city;
  }

  function tEvent(event: Event, field: "title" | "description" | "venue"): string {
    const localized = event.i18n?.[locale]?.[field];
    if (localized && localized.trim().length > 0) return localized;
    return event[field] || "";
  }

  return { t, tCat, tCity, tEvent, locale, setLocale };
}
