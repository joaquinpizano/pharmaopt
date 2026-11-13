import { NextResponse } from "next/server";

export function GET() {
  return NextResponse.json({ application: "pharmaopt-web", status: "ok" });
}
