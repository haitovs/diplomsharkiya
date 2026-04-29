import { loadEvents } from "@/lib/data";
import { SavedClient } from "./SavedClient";

export const dynamic = "force-dynamic";

export default function SavedPage() {
  const events = loadEvents();
  return <SavedClient events={events} />;
}
