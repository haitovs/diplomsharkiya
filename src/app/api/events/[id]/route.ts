import { NextRequest, NextResponse } from "next/server";
import { loadEvents, saveEvents } from "@/lib/data";

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  const body = await request.json();
  const events = loadEvents();
  const idx = events.findIndex(e => e.id === params.id);
  if (idx === -1) return NextResponse.json({ error: "Not found" }, { status: 404 });
  const merged: Record<string, unknown> = { ...events[idx], ...body, id: params.id };
  for (const [k, v] of Object.entries(merged)) {
    if (v === null) delete merged[k];
  }
  events[idx] = merged as unknown as typeof events[number];
  saveEvents(events);
  return NextResponse.json(events[idx]);
}

export async function DELETE(_request: NextRequest, { params }: { params: { id: string } }) {
  const events = loadEvents();
  const filtered = events.filter(e => e.id !== params.id);
  saveEvents(filtered);
  return NextResponse.json({ ok: true });
}
