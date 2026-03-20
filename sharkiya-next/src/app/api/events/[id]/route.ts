import { NextRequest, NextResponse } from "next/server";
import { loadEvents, saveEvents } from "@/lib/data";

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  const body = await request.json();
  const events = loadEvents();
  const idx = events.findIndex(e => e.id === params.id);
  if (idx === -1) return NextResponse.json({ error: "Not found" }, { status: 404 });
  events[idx] = { ...events[idx], ...body, id: params.id };
  saveEvents(events);
  return NextResponse.json(events[idx]);
}

export async function DELETE(_request: NextRequest, { params }: { params: { id: string } }) {
  const events = loadEvents();
  const filtered = events.filter(e => e.id !== params.id);
  saveEvents(filtered);
  return NextResponse.json({ ok: true });
}
