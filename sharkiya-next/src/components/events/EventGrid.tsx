"use client";

import { EventCard } from "./EventCard";
import type { Event } from "@/types/event";

interface EventGridProps {
  events: Event[];
  onBuyTicket?: (event: Event) => void;
}

export function EventGrid({ events, onBuyTicket }: EventGridProps) {
  return (
    <div className="space-y-4">
      {events.map((event) => (
        <EventCard key={event.id} event={event} onBuyTicket={onBuyTicket} />
      ))}
    </div>
  );
}
