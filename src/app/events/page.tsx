import { loadEvents } from "@/lib/data";
import { EventsClient } from "./EventsClient";

export const dynamic = "force-dynamic";

export default function EventsPage() {
  const events = loadEvents();
  return <EventsClient events={events} />;
}
