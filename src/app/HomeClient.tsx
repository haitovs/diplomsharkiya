"use client";

import { useState } from "react";
import { Hero } from "@/components/ui/Hero";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { StatCard } from "@/components/ui/StatCard";
import { NavCard } from "@/components/ui/NavCard";
import { FeaturedEvents } from "@/components/events/FeaturedEvents";
import { PaymentDialog } from "@/components/payment/PaymentDialog";
import { useTranslation } from "@/i18n/config";
import type { Event } from "@/types/event";

interface HomeClientProps {
  events: Event[];
}

export function HomeClient({ events }: HomeClientProps) {
  const { t } = useTranslation();
  const [paymentEvent, setPaymentEvent] = useState<Event | null>(null);

  const cityCount = new Set(events.map((e) => e.city)).size;

  return (
    <>
      <Hero
        title={t("app_title")}
        subtitle={t("app_subtitle")}
        badge={t("event_discovery_platform")}
      />

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <StatCard icon="🎉" value={events.length} label={t("upcoming_events")} delta={t("live_now")} />
        <StatCard icon="🏙️" value={cityCount} label={t("cities_covered")} />
        <StatCard icon="👥" value={t("community")} label={t("growing")} />
      </div>

      {/* Quick Navigation */}
      <SectionHeader title={`🧭 ${t("quick_navigation")}`} subtitle={t("jump_to_section")} />
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <NavCard
          href="/events"
          icon="📋"
          title={t("browse_events")}
          description={t("browse_events_desc")}
          linkText={t("go_to_events")}
        />
        <NavCard
          href="/map"
          icon="🗺️"
          title={t("interactive_map")}
          description={t("interactive_map_desc")}
          linkText={t("open_map")}
        />
        <NavCard
          href="/saved"
          icon="⭐"
          title={t("saved_events")}
          description={t("saved_events_desc")}
          linkText={t("view_saved")}
        />
      </div>

      {/* Featured Events */}
      <SectionHeader title={`🔥 ${t("featured_events")}`} subtitle={t("featured_events_desc")} />
      <FeaturedEvents events={events} onBuyTicket={setPaymentEvent} />

      {paymentEvent && (
        <PaymentDialog event={paymentEvent} onClose={() => setPaymentEvent(null)} />
      )}
    </>
  );
}
