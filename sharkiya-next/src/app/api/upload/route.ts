import { NextRequest, NextResponse } from "next/server";
import { writeFile, mkdir } from "fs/promises";
import path from "path";

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const file = formData.get("file") as File;
  const eventId = formData.get("eventId") as string;

  if (!file) return NextResponse.json({ error: "No file" }, { status: 400 });

  const imgDir = path.join(process.cwd(), "public", "images");
  await mkdir(imgDir, { recursive: true });

  const ext = file.name.split(".").pop() || "jpg";
  const filename = `${eventId || "upload"}.${ext}`;
  const buffer = Buffer.from(await file.arrayBuffer());
  await writeFile(path.join(imgDir, filename), buffer);

  return NextResponse.json({ image: `images/${filename}` });
}
