import { NextRequest, NextResponse } from "next/server";
import { loadEvents, saveEvents } from "@/lib/data";
import { v4 as uuidv4 } from "uuid";

export async function GET() {
  const events = loadEvents();
  return NextResponse.json(events);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const events = loadEvents();
  const newEvent = {
    id: body.id || `evt${uuidv4().replace(/-/g, "").slice(0, 6)}`,
    title: body.title || "",
    category: body.category || "Music",
    city: body.city || "Ashgabat",
    venue: body.venue || "",
    date_start: body.date_start || new Date().toISOString(),
    date_end: body.date_end || new Date().toISOString(),
    price: body.price ?? 0,
    popularity: body.popularity ?? 50,
    lat: body.lat ?? 37.9601,
    lon: body.lon ?? 58.3261,
    image: body.image || "images/event_default.jpg",
    description: body.description || "",
    icon: body.icon || "",
    ...(body.i18n ? { i18n: body.i18n } : {}),
  };
  events.push(newEvent);
  saveEvents(events);
  return NextResponse.json(newEvent, { status: 201 });
}

export async function DELETE() {
  saveEvents([]);
  return NextResponse.json({ ok: true });
}
