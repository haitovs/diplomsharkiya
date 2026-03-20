import { Event } from "@/types/event";
import fs from "fs";
import path from "path";

const DATA_PATH = path.join(process.cwd(), "data", "events.json");

export function loadEvents(): Event[] {
  try {
    const raw = fs.readFileSync(DATA_PATH, "utf-8");
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

export function saveEvents(events: Event[]): void {
  fs.writeFileSync(DATA_PATH, JSON.stringify(events, null, 2), "utf-8");
}
