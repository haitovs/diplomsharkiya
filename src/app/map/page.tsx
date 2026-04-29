import { loadEvents } from "@/lib/data";
import { MapClient } from "./MapClient";

export const dynamic = "force-dynamic";

export default function MapPage() {
  const events = loadEvents();
  return <MapClient events={events} />;
}
