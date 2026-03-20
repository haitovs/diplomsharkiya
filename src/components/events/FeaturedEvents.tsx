"use client";

import { EventCard } from "./EventCard";
import type { Event } from "@/types/event";

interface FeaturedEventsProps {
  events: Event[];
  onBuyTicket?: (event: Event) => void;
}

export function FeaturedEvents({ events, onBuyTicket }: FeaturedEventsProps) {
  const featured = [...events]
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, 5);

  if (featured.length === 0) return null;

  return (
    <div className="space-y-4">
      {featured.map((event) => (
        <EventCard key={event.id} event={event} onBuyTicket={onBuyTicket} />
      ))}
    </div>
  );
}
