import { loadEvents } from "@/lib/data";
import { MapClient } from "./MapClient";

export default function MapPage() {
  const events = loadEvents();
  return <MapClient events={events} />;
}
