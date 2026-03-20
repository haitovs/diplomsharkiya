import { loadEvents } from "@/lib/data";
import { HomeClient } from "./HomeClient";

export default function HomePage() {
  const events = loadEvents();
  return <HomeClient events={events} />;
}
