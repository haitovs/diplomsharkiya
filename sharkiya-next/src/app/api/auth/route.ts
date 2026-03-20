import { NextRequest, NextResponse } from "next/server";
import { ADMIN_USERNAME, ADMIN_PASSWORD } from "@/config/constants";

export async function POST(request: NextRequest) {
  const { username, password } = await request.json();
  if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
    return NextResponse.json({ ok: true, username });
  }
  return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });
}
