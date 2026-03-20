import { loadEvents } from "@/lib/data";
import { AboutClient } from "./AboutClient";

export default function AboutPage() {
  const events = loadEvents();
  return <AboutClient events={events} />;
}
