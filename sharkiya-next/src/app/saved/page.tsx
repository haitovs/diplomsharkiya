import { loadEvents } from "@/lib/data";
import { SavedClient } from "./SavedClient";

export default function SavedPage() {
  const events = loadEvents();
  return <SavedClient events={events} />;
}
