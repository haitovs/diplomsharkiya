"use client";

import { useState, useMemo } from "react";
import dynamic from "next/dynamic";
import { Hero } from "@/components/ui/Hero";
import { PaymentDialog } from "@/components/payment/PaymentDialog";
import { useTranslation } from "@/i18n/config";
import { CATEGORY_NAMES } from "@/config/categories";
import { CITY_NAMES } from "@/config/cities";
import type { Event } from "@/types/event";

const EventMap = dynamic(() => import("@/components/map/EventMap").then(m => m.EventMap), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] bg-bg-card rounded-xl flex items-center justify-center">
      <p className="text-text-secondary">Loading map...</p>
    </div>
  ),
});

interface MapClientProps {
  events: Event[];
}

export function MapClient({ events }: MapClientProps) {
  const { t, tCat } = useTranslation();
  const [city, setCity] = useState("All Cities");
  const [categories, setCategories] = useState<string[]>([]);
  const [paymentEvent, setPaymentEvent] = useState<Event | null>(null);

  const filtered = useMemo(() => {
    let result = events;
    if (city !== "All Cities") result = result.filter(e => e.city === city);
    if (categories.length > 0) result = result.filter(e => categories.includes(e.category));
    return result;
  }, [events, city, categories]);

  function toggleCategory(cat: string) {
    setCategories(prev =>
      prev.includes(cat) ? prev.filter(c => c !== cat) : [...prev, cat]
    );
  }

  return (
    <>
      <Hero title={t("map_page_title")} subtitle={t("map_page_subtitle")} icon="🗺️" />

      <div className="flex flex-col lg:flex-row gap-4 mb-4">
        <select value={city} onChange={(e) => setCity(e.target.value)} className="select max-w-xs">
          <option value="All Cities">{t("all_cities")}</option>
          {CITY_NAMES.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <div className="flex flex-wrap gap-1.5">
          {CATEGORY_NAMES.map(cat => (
            <button
              key={cat}
              onClick={() => toggleCategory(cat)}
              className={`text-xs px-2.5 py-1 rounded-full font-medium transition-colors ${
                categories.includes(cat)
                  ? "bg-accent-primary/20 text-accent-primary border border-accent-primary/40"
                  : "bg-bg-card text-text-secondary border border-border-subtle hover:border-accent-primary/30"
              }`}
            >
              {tCat(cat)}
            </button>
          ))}
        </div>
      </div>

      <p className="text-sm text-text-secondary mb-3">
        {t("showing_events")}: {filtered.length}
      </p>

      <EventMap events={filtered} onBuyTicket={setPaymentEvent} />

      <p className="text-xs text-text-muted mt-3">{t("map_note")}</p>

      {paymentEvent && (
        <PaymentDialog event={paymentEvent} onClose={() => setPaymentEvent(null)} />
      )}
    </>
  );
}
