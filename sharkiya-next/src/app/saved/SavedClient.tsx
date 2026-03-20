"use client";

import { useState } from "react";
import { Hero } from "@/components/ui/Hero";
import { EventCard } from "@/components/events/EventCard";
import { PaymentDialog } from "@/components/payment/PaymentDialog";
import { useTranslation } from "@/i18n/config";
import { useUIStore } from "@/store/useUIStore";
import type { Event } from "@/types/event";

interface SavedClientProps {
  events: Event[];
}

export function SavedClient({ events }: SavedClientProps) {
  const { t } = useTranslation();
  const { savedEvents, clearSaved } = useUIStore();
  const [paymentEvent, setPaymentEvent] = useState<Event | null>(null);

  const savedEventsList = events.filter(e => savedEvents.includes(e.id));

  return (
    <>
      <Hero title={t("saved_page_title")} subtitle={t("saved_page_subtitle")} icon="⭐" />

      {savedEventsList.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-7xl mb-6">🤍</p>
          <p className="text-xl text-text-secondary">{t("no_saved_events")}</p>
          <p className="text-sm text-text-muted mt-2">{t("visit_events_to_buy")}</p>
        </div>
      ) : (
        <>
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-text-secondary">
              {savedEventsList.length} {t("saved_events")}
            </p>
            <button onClick={clearSaved} className="btn-ghost text-sm">
              🗑️ {t("clear_saved")}
            </button>
          </div>
          <div className="space-y-4">
            {savedEventsList.map(event => (
              <EventCard key={event.id} event={event} onBuyTicket={setPaymentEvent} />
            ))}
          </div>
        </>
      )}

      {paymentEvent && (
        <PaymentDialog event={paymentEvent} onClose={() => setPaymentEvent(null)} />
      )}
    </>
  );
}
