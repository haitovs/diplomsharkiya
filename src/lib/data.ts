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
  // Atomic write: tempfile + rename. Rename needs directory-write perm only,
  // so this still works if events.json is owned by a different user than the
  // process (e.g. someone restored it via `git checkout` as root).
  const tmp = `${DATA_PATH}.${process.pid}.${Date.now()}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(events, null, 2), "utf-8");
  fs.renameSync(tmp, DATA_PATH);
}
