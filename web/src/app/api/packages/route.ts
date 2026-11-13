import { gunzipSync } from "node:zlib";
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";
import { NextRequest, NextResponse } from "next/server";
import type { PackageRecord } from "@/lib/types";

type RawRow = Record<string, string>;
type Model = "v04" | "v05";

export const runtime = "nodejs";

function positiveInteger(value: string | null, fallback: number, maximum: number) {
  const parsed = value === null ? fallback : Number(value);
  return Number.isSafeInteger(parsed) && parsed > 0 ? Math.min(parsed, maximum) : fallback;
}

let cache: PackageRecord[] | null = null;
let sortedCache: Record<Model, PackageRecord[]> | null = null;

function loadRows(): PackageRecord[] {
  if (cache) return cache;
  const file = path.join(process.cwd(), "data", "pharmaopt_packages.csv.gz");
  const content = gunzipSync(readFileSync(file)).toString("utf8");
  const rawRows = parse(content, { columns: true, skip_empty_lines: true }) as RawRow[];
  cache = rawRows.map((row) => ({
    package_ndc: row.package_ndc,
    generic_name: row.generic_name || "Not available",
    brand_name: row.brand_name || "Not available",
    labeler_name: row.labeler_name || "Not available",
    dosage_form: row.dosage_form || "Not available",
    marketing_category: row.marketing_category || "Not available",
    package_description: row.package_description || "Not available",
    risk_score_v04: Number(row.risk_score_v04),
    risk_score_v05: Number(row.risk_score_v05),
    fda_event_any: Number(row.fda_event_any),
    non_discontinuation_event_candidate: Number(row.non_discontinuation_event_candidate),
    discontinuation_notice_candidate: Number(row.discontinuation_notice_candidate),
    risk_rank: 0,
  }));
  sortedCache = null;
  return cache;
}

function ranked(model: Model): PackageRecord[] {
  loadRows();
  if (!sortedCache) sortedCache = { v04: [], v05: [] };
  if (sortedCache[model].length) return sortedCache[model];
  const score = model === "v04" ? "risk_score_v04" : "risk_score_v05";
  sortedCache[model] = [...cache!]
    .sort((a, b) => b[score] - a[score] || (a.package_ndc < b.package_ndc ? -1 : a.package_ndc > b.package_ndc ? 1 : 0));
  return sortedCache[model];
}

export async function GET(request: NextRequest) {
  try {
    const params = request.nextUrl.searchParams;
    const model = params.get("model") === "v05" ? "v05" : "v04";
    const query = (params.get("q") || "").trim().toLowerCase();
    const eventOnly = params.get("eventOnly") === "true";
    const page = positiveInteger(params.get("page"), 1, 221667);
    const pageSize = positiveInteger(params.get("pageSize"), 12, 50);
    const rankedRows = ranked(model);
    const start = (page - 1) * pageSize;
    const rows: PackageRecord[] = [];
    let total = 0;
    rankedRows.forEach((row, index) => {
      if (eventOnly && row.fda_event_any !== 1) return;
      const matches = !query || [row.package_ndc, row.generic_name, row.brand_name, row.labeler_name]
        .join(" ").toLowerCase().includes(query);
      if (!matches) return;
      if (total >= start && rows.length < pageSize) rows.push({ ...row, risk_rank: index + 1 });
      total++;
    });
    return NextResponse.json({
      rows,
      total,
      page,
      pageSize,
      model,
    });
  } catch (error) {
    console.error("Package query failed", error);
    return NextResponse.json(
      { error: "Unable to query package data. Please try again later." },
      { status: 500 },
    );
  }
}
