// @vitest-environment node
import { describe, expect, it } from "vitest";
import { NextRequest } from "next/server";
import { GET } from "./route";

async function query(params: string) {
  const response = await GET(new NextRequest(`http://localhost/api/packages?${params}`));
  expect(response.status).toBe(200);
  return response.json();
}

describe("package API against the published cohort", () => {
  it("bounds malformed and excessive pagination inputs", async () => {
    const invalid = await query("page=NaN&pageSize=Infinity");
    expect(invalid.page).toBe(1);
    expect(invalid.pageSize).toBe(12);
    expect(invalid.rows).toHaveLength(12);
    expect(invalid.total).toBe(221667);
    const capped = await query("pageSize=999999");
    expect(capped.rows).toHaveLength(50);
  });

  it("preserves global ranks and all 96 flags with either ranking", async () => {
    for (const model of ["v04", "v05"]) {
      const data = await query(`model=${model}&eventOnly=true&pageSize=50`);
      expect(data.total).toBe(96);
      expect(data.rows.every((row: { fda_event_any: number }) => row.fda_event_any === 1)).toBe(true);
      expect(data.rows.filter((row: { risk_rank: number }) => row.risk_rank <= 500)).toHaveLength(model === "v04" ? 10 : 7);
    }
  });

  it("searches NDCs and returns an empty result for unknown terms", async () => {
    const first = await query("pageSize=1");
    const match = await query(`q=${encodeURIComponent(first.rows[0].package_ndc)}`);
    expect(match.rows[0].package_ndc).toBe(first.rows[0].package_ndc);
    expect(match.rows[0].risk_rank).toBe(1);
    expect((await query("q=__no_such_package__")).total).toBe(0);
    const second = await query("page=2&pageSize=1");
    expect(second.rows[0].risk_rank).toBe(2);
    expect(second.rows[0].package_ndc).not.toBe(first.rows[0].package_ndc);
  });
});
