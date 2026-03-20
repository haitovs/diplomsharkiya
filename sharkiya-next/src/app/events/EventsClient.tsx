"use client";

import { useState, useMemo } from "react";
import { Hero } from "@/components/ui/Hero";
import { FilterPanel } from "@/components/events/FilterPanel";
import { EventGrid } from "@/components/events/EventGrid";
import { PaymentDialog } from "@/components/payment/PaymentDialog";
import { useTranslation } from "@/i18n/config";
import { useFilterStore } from "@/store/useFilterStore";
import { usePaymentStore } from "@/store/usePaymentStore";
import { applyFilters, sortEvents } from "@/lib/filters";
import type { Event } from "@/types/event";

interface EventsClientProps {
  events: Event[];
}

export function EventsClient({ events }: EventsClientProps) {
  const { t } = useTranslation();
  const filters = useFilterStore();
  const { transactions } = usePaymentStore();
  const [paymentEvent, setPaymentEvent] = useState<Event | null>(null);

  const filteredEvents = useMemo(() => {
    const filtered = applyFilters(events, filters);
    return sortEvents(filtered, filters.sortBy);
  }, [events, filters]);

  return (
    <>
      <Hero
        title={t("events_page_title")}
        subtitle={t("events_page_subtitle")}
        icon="📋"
      />

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <aside className="lg:w-72 shrink-0">
          <div className="sticky top-20 card p-4">
            <FilterPanel />
          </div>

          {/* My Tickets */}
          {transactions.length > 0 && (
            <div className="card p-4 mt-4">
              <h4 className="font-semibold text-sm mb-3">🎫 {t("my_tickets")}</h4>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {transactions.slice().reverse().map((txn) => (
                  <div key={txn.id} className="bg-bg-primary rounded-lg p-2 text-xs">
                    <p className="font-semibold truncate">{txn.title}</p>
                    <p className="text-text-muted">{txn.id} · {txn.amount} TMT</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </aside>

        {/* Event list */}
        <div className="flex-1 min-w-0">
          <p className="text-sm text-text-secondary mb-4">
            {filteredEvents.length} {t("events_found")}
          </p>
          {filteredEvents.length === 0 ? (
            <div className="text-center py-16">
              <p className="text-5xl mb-4">🔍</p>
              <p className="text-text-secondary">{t("no_events_found")}</p>
            </div>
          ) : (
            <EventGrid events={filteredEvents} onBuyTicket={setPaymentEvent} />
          )}
        </div>
      </div>

      {paymentEvent && (
        <PaymentDialog event={paymentEvent} onClose={() => setPaymentEvent(null)} />
      )}
    </>
  );
}
