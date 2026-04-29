import { loadEvents } from "@/lib/data";
import { AboutClient } from "./AboutClient";

export const dynamic = "force-dynamic";

export default function AboutPage() {
  const events = loadEvents();
  return <AboutClient events={events} />;
}
