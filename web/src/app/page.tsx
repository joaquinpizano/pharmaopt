"use client";

import { useEffect, useState } from "react";
import { ArrowDownRight, ArrowUpRight, ChevronLeft, ChevronRight, CircleAlert, FlaskConical, Menu, Search, ShieldCheck } from "lucide-react";
import { bootstrapMetrics, budgetMetrics, budgets, calculateReviewPlan, productMetrics } from "@/lib/evaluation";
import type { PackageRecord, PackageResponse } from "@/lib/types";

const totalPackages = 221667;

function money(value: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

function modelName(model: "v04" | "v05") {
  return model === "v04" ? "v0.4" : "v0.5";
}

function App() {
  const [model, setModel] = useState<"v04" | "v05">("v04");
  const [budget, setBudget] = useState(500000);
  const [reviewCost, setReviewCost] = useState(1000);
  const [capacity, setCapacity] = useState(500);
  const [explorerQuery, setExplorerQuery] = useState("");
  const [eventOnly, setEventOnly] = useState(false);
  const [selectedPackage, setSelectedPackage] = useState<PackageRecord | null>(null);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [explorer, setExplorer] = useState<PackageResponse | null>(null);
  const [explorerPage, setExplorerPage] = useState(1);
  const [loadingExplorer, setLoadingExplorer] = useState(false);
  const [apiError, setApiError] = useState("");
  const [reload, setReload] = useState(0);

  const { selectedCount, cost, remaining } = calculateReviewPlan(budget, reviewCost, capacity, totalPackages);
  const tierCounts = [Math.min(selectedCount, 100), Math.max(0, Math.min(selectedCount - 100, 150)), Math.max(0, selectedCount - 250)];

  useEffect(() => {
    const controller = new AbortController();
    setLoadingExplorer(true);
    setApiError("");
    const timer = setTimeout(() => {
      fetch(`/api/packages?model=${model}&page=${explorerPage}&pageSize=12&q=${encodeURIComponent(explorerQuery)}&eventOnly=${eventOnly}`, { signal: controller.signal })
        .then((response) => {
          if (!response.ok) throw new Error("Package request failed");
          return response.json();
        })
        .then((data: PackageResponse) => {
          if (controller.signal.aborted) return;
          setExplorer(data);
          setLoadingExplorer(false);
        })
        .catch(() => {
          if (controller.signal.aborted) return;
          setExplorer(null);
          setApiError("Explorer results could not be loaded. Try Reset to reload the package data.");
          setLoadingExplorer(false);
        });
    }, 180);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [model, explorerQuery, explorerPage, eventOnly, reload]);

  function scrollTo(id: string) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
    setMobileMenu(false);
  }

  function changeModel(next: "v04" | "v05") {
    setModel(next);
    setExplorerPage(1);
    setSelectedPackage(null);
  }

  const explorerRows = explorer?.rows ?? [];
  const maxTier = Math.max(...tierCounts, 1);

  return (
    <div className="shell">
      <header className="topbar">
        <button className="brand" onClick={() => scrollTo("overview")} aria-label="Go to overview">
          <span className="brand-mark" aria-hidden="true"><svg viewBox="0 0 72 72"><path d="M17 17h18a12 12 0 0 1 0 24H17V17Z" fill="white" /><path d="M17 29h18" stroke="#087f78" strokeWidth="4" strokeLinecap="round" /><path d="M14 52c7-8 12-8 18 0s11 8 18 0" fill="none" stroke="#70d2c2" strokeWidth="4" strokeLinecap="round" /></svg></span>
          <span className="brand-copy"><span className="brand-name">PharmaOpt</span><span className="brand-sub">Research intelligence</span></span>
        </button>
        <button className="menu" onClick={() => setMobileMenu((open) => !open)} aria-label="Toggle navigation" aria-expanded={mobileMenu}><Menu size={21} /></button>
        <nav className={mobileMenu ? "nav mobile-open" : "nav"} aria-label="Primary navigation">
          {["overview", "planner", "explorer", "evaluation", "methodology"].map((item) => (
            <button key={item} onClick={() => scrollTo(item)}>{item === "planner" ? "Budget Planner" : item[0].toUpperCase() + item.slice(1)}</button>
          ))}
          <button className="nav-cta" onClick={() => scrollTo("explorer")}>Explore packages <ArrowDownRight size={14} /></button>
        </nav>
      </header>

      <main>
        <section className="hero" id="overview">
          <div>
            <div className="eyebrow">Pharmaceutical review intelligence / 2025 retrospective</div>
            <h1>Make the first<br /><em>review</em> more thoughtful.</h1>
            <p>PharmaOpt organizes a large pharmaceutical package universe into a transparent, research-based review list — so teams can explore limited capacity without confusing a ranking with a shortage forecast.</p>
            <div className="hero-actions">
              <button className="button button-primary" onClick={() => scrollTo("planner")}>Plan a review sample <ArrowDownRight size={16} /></button>
              <button className="button button-ghost" onClick={() => scrollTo("methodology")}>Read the methodology</button>
            </div>
          </div>
          <div className="hero-panel" aria-label="Historical study snapshot">
            <div className="hero-panel-top"><span>Study snapshot</span><span>2025 / {modelName(model)}</span></div>
            <div className="signal"><div className="signal-label">packages organized for review</div><div className="signal-value">221,667</div><div className="signal-bar"><span /></div><div className="panel-foot"><span>96 historical event flags</span><span>0.043% base rate</span></div></div>
            <div className="notice">A research interface, not a live monitoring service. Historical FDA-linked indicators are not verified active shortages.</div>
          </div>
        </section>

        <div className="main">
          {apiError && <div className="notice error" role="alert"><CircleAlert size={16} /> {apiError}</div>}
          <section className="section">
            <div className="section-heading"><div><div className="eyebrow">01 / At a glance</div><h2>A clearer starting point.</h2></div><p>Explore the same core ideas as the Streamlit prototype in a calmer, more approachable workspace. The numbers below are fixed to the validated 2025 research artifact.</p></div>
            <div className="kpi-grid">
              <div className="card"><div className="kpi-label">Packages in study</div><div className="kpi-value">221,667</div><div className="kpi-note">2025 package cohort</div></div>
              <div className="card"><div className="kpi-label">FDA-linked event flags</div><div className="kpi-value">96</div><div className="kpi-note">Historical indicators</div></div>
              <div className="card"><div className="kpi-label">v0.4 capture @500</div><div className="kpi-value">10 / 96</div><div className="kpi-note">2.00% precision</div></div>
              <div className="card"><div className="kpi-label">v0.5 capture @500</div><div className="kpi-value">7 / 96</div><div className="kpi-note">1.40% precision</div></div>
            </div>
          </section>

          <section className="section steps">
            <div className="section-heading"><div><div className="eyebrow">A practical workflow</div><h2>Analyze. Prioritize. Review.</h2></div><p>The interface keeps the review question visible while making assumptions easy to inspect.</p></div>
            <div className="grid-3">
              <div className="card"><div className="step-num">STEP 01</div><h3>Analyze</h3><p>Combine FDA package context with historical event and utilization signals in a package-year research panel.</p></div>
              <div className="card"><div className="step-num">STEP 02</div><h3>Prioritize</h3><p>Use an experimental ranking to decide which packages appear first in a hypothetical review queue.</p></div>
              <div className="card"><div className="step-num">STEP 03</div><h3>Interrogate</h3><p>Open the evidence, compare models, and keep the distinction between an indicator and a confirmed shortage.</p></div>
            </div>
          </section>

          <section className="section" id="planner">
            <div className="section-heading"><div><div className="eyebrow">02 / Budget planner</div><h2>Make capacity visible.</h2></div><p>Change the assumptions and see how many packages would enter a hypothetical review queue. These are planning assumptions, not actual expenditures.</p></div>
            <div className="planner">
              <div className="card control">
                <label>Ranking model<select value={model} onChange={(event) => changeModel(event.target.value as "v04" | "v05")}><option value="v04">v0.4 — recommended comparison</option><option value="v05">v0.5 — experimental alternative</option></select></label>
                <label>Available review budget <span className="control-value">{money(budget)}</span><input type="range" min="10000" max="2000000" step="10000" value={budget} onChange={(event) => setBudget(Number(event.target.value))} /></label>
                <label>Assumed review cost per package <span className="control-value">{money(reviewCost)}</span><input type="range" min="100" max="5000" step="100" value={reviewCost} onChange={(event) => setReviewCost(Number(event.target.value))} /></label>
                <label>Team capacity <span className="control-value">{capacity.toLocaleString()} packages</span><input type="range" min="100" max="5000" step="100" value={capacity} onChange={(event) => setCapacity(Number(event.target.value))} /></label>
                <div className="notice"><ShieldCheck size={16} /> This planner selects by saved score order. It does not place orders, spend money, or create a shortage probability.</div>
              </div>
              <div className="planner-result">
                <div className="big-result"><small>Packages selected for hypothetical review</small><strong>{selectedCount.toLocaleString()}</strong><span>using {modelName(model)} and deterministic rank order</span></div>
                <div className="mini-grid"><div className="card"><div className="kpi-label">Assumed cost</div><strong>{money(cost)}</strong></div><div className="card"><div className="kpi-label">Budget remaining</div><strong>{money(remaining)}</strong></div><div className="card"><div className="kpi-label">Share of cohort</div><strong>{(selectedCount / totalPackages * 100).toFixed(2)}%</strong></div></div>
                <div className="card"><div className="chart-title">Priority tiers</div><p className="chart-sub">Organizing buckets, not clinically validated risk categories.</p><div className="tier-list">{["Tier 1 · ranks 1–100", "Tier 2 · ranks 101–250", "Tier 3 · remaining"].map((tier, index) => <div className="tier-row" key={tier}><span>{tier.split(" · ")[0]}</span><div className="tier-track"><div className="tier-fill" style={{ width: `${tierCounts[index] / maxTier * 100}%` }} /></div><strong>{tierCounts[index]}</strong></div>)}</div></div>
              </div>
            </div>
          </section>

          <section className="section" id="explorer">
            <div className="section-heading"><div><div className="eyebrow">03 / Drug explorer</div><h2>Inspect the queue.</h2></div><p>Search the server-side package index by NDC, generic name, brand, or FDA labeler. Only the current page is sent to the browser.</p></div>
            <div className="card">
              <div className="table-tools"><div className="search" style={{ display: "flex", gap: 8, alignItems: "center" }}><Search size={16} color="#647777" /><input aria-label="Search packages" value={explorerQuery} onChange={(event) => { setExplorerQuery(event.target.value); setExplorerPage(1); }} placeholder="Search package, drug, brand, or labeler" style={{ border: 0, outline: 0, width: "100%", background: "transparent" }} /></div><button className={eventOnly ? "button button-primary" : "button button-ghost"} onClick={() => { setEventOnly((value) => !value); setExplorerPage(1); }}>Historical flags only</button><button className="button button-ghost" onClick={() => { setExplorerQuery(""); setEventOnly(false); setExplorerPage(1); setReload((value) => value + 1); }}>Reset</button></div>
              {loadingExplorer ? <div className="notice">Loading the next server-side page…</div> : <>{!apiError && explorer?.total === 0 && <div className="notice" role="status">No packages match these filters. Try another search or Reset.</div>}<div className="table-wrap"><table><thead><tr><th>Rank</th><th>Package NDC</th><th>Generic name</th><th>FDA labeler</th><th>Score</th><th>Event</th><th>Details</th></tr></thead><tbody>{explorerRows.map((row) => <tr key={row.package_ndc}><td className="highlight">#{row.risk_rank.toLocaleString()}</td><td>{row.package_ndc}</td><td>{row.generic_name}</td><td>{row.labeler_name}</td><td>{row[model === "v04" ? "risk_score_v04" : "risk_score_v05"].toFixed(4)}</td><td>{row.fda_event_any ? <span className="pill">Flagged</span> : "—"}</td><td><button className="button button-ghost" style={{ padding: "7px 10px", fontSize: 12 }} onClick={() => setSelectedPackage(row)}>Open</button></td></tr>)}</tbody></table></div><div className="pager"><span>{explorer ? `${explorer.total.toLocaleString()} matching packages` : "Loading"} · page {explorerPage}</span><div><button onClick={() => setExplorerPage((page) => Math.max(1, page - 1))} disabled={explorerPage === 1}><ChevronLeft size={15} aria-label="Previous page" /></button> <button onClick={() => setExplorerPage((page) => page + 1)} disabled={!explorer || explorerPage * 12 >= explorer.total}><ChevronRight size={15} aria-label="Next page" /></button></div></div></>}
              {selectedPackage && <div className="detail card"><div className="section-heading"><div><div className="eyebrow">Package detail</div><h3>{selectedPackage.generic_name}</h3></div><button className="button button-ghost" onClick={() => setSelectedPackage(null)}>Close</button></div><div className="detail-grid"><div className="detail-item"><small>Package NDC</small><strong>{selectedPackage.package_ndc}</strong></div><div className="detail-item"><small>Brand</small><strong>{selectedPackage.brand_name}</strong></div><div className="detail-item"><small>Dosage form</small><strong>{selectedPackage.dosage_form}</strong></div><div className="detail-item"><small>Historical indicator</small><strong>{selectedPackage.fda_event_any ? "FDA-linked flag" : "No flag in cohort"}</strong></div><div className="detail-item"><small>v0.4 score</small><strong>{selectedPackage.risk_score_v04.toFixed(6)}</strong></div><div className="detail-item"><small>v0.5 score</small><strong>{selectedPackage.risk_score_v05.toFixed(6)}</strong></div><div className="detail-item"><small>Discontinuation candidate</small><strong>{selectedPackage.discontinuation_notice_candidate ? "Yes" : "No"}</strong></div><div className="detail-item"><small>Non-discontinuation candidate</small><strong>{selectedPackage.non_discontinuation_event_candidate ? "Yes" : "No"}</strong></div></div></div>}
            </div>
          </section>

          <section className="section" id="evaluation">
            <div className="section-heading"><div><div className="eyebrow">04 / Model evaluation</div><h2>Compare, don’t overclaim.</h2></div><p>Evaluation v2 compares saved rankings against the same 96 historical FDA-linked flags. The result is a retrospective ranking diagnostic, not prospective validation.</p></div>
            <div className="callout"><CircleAlert size={17} /> At a 500-package budget, v0.4 captures 10 flags and v0.5 captures 7. Both rankings are far above the expected random count, but absolute precision remains low.</div>
            <div className="grid-2" style={{ marginTop: 16 }}><div className="card chart-card"><h3 className="chart-title">Event capture by review budget</h3><p className="chart-sub">Higher bars mean more recorded event flags found, not more likely shortages.</p><div className="bar-chart">{budgets.map((k) => { const a = budgetMetrics.find((row) => row.model === "risk_score_v04" && row.review_budget === k)!; const b = budgetMetrics.find((row) => row.model === "risk_score_v05" && row.review_budget === k)!; return <div key={k} style={{ display: "flex", gap: 4, alignItems: "end", flex: 1, height: "100%" }}><div className="bar" style={{ height: `${Math.max(4, a.captured / 17 * 100)}%` }}><span>{a.captured}</span></div><div className="bar" style={{ height: `${Math.max(4, b.captured / 17 * 100)}%`, background: "linear-gradient(180deg,#7c9fcd,#315e91)" }}><span>{b.captured}</span></div></div> })}</div><div className="bar-labels">{budgets.map((k) => <span key={k}>{k.toLocaleString()}</span>)}</div><div style={{ display: "flex", gap: 12, color: "#647777", fontSize: 12 }}><span><i style={{ display: "inline-block", width: 9, height: 9, background: "#087f78", borderRadius: 3 }} /> v0.4</span><span><i style={{ display: "inline-block", width: 9, height: 9, background: "#315e91", borderRadius: 3 }} /> v0.5</span></div></div><div className="card chart-card"><h3 className="chart-title">Ranking quality</h3><p className="chart-sub">Average precision and ROC-AUC across the saved 2025 cohort.</p><div className="kpi-grid" style={{ gridTemplateColumns: "1fr 1fr" }}><div><div className="kpi-label">v0.4 AP</div><div className="kpi-value" style={{ fontSize: 25 }}>0.003897</div><div className="kpi-note">ROC-AUC 0.7751</div></div><div><div className="kpi-label">v0.5 AP</div><div className="kpi-value" style={{ fontSize: 25 }}>0.002858</div><div className="kpi-note">ROC-AUC 0.7493</div></div></div><div className="notice" style={{ marginTop: 24 }}><FlaskConical size={16} /> Scores are ranks, not calibrated probabilities.</div></div></div>
            <div className="card" style={{ marginTop: 16 }}><h3 className="chart-title">Budget comparison</h3><div className="eval-table"><table><thead><tr><th>K</th><th>v0.4 capture</th><th>v0.4 precision</th><th>v0.4 recall</th><th>v0.5 capture</th><th>v0.5 precision</th><th>v0.5 recall</th><th>Random expected</th></tr></thead><tbody>{budgets.map((k) => { const a = budgetMetrics.find((row) => row.model === "risk_score_v04" && row.review_budget === k)!; const b = budgetMetrics.find((row) => row.model === "risk_score_v05" && row.review_budget === k)!; return <tr key={k}><td>{k.toLocaleString()}</td><td className="highlight">{a.captured}/96</td><td>{(a.precision * 100).toFixed(2)}%</td><td>{(a.recall * 100).toFixed(2)}%</td><td className="highlight">{b.captured}/96</td><td>{(b.precision * 100).toFixed(2)}%</td><td>{(b.recall * 100).toFixed(2)}%</td><td>{a.random_expected.toFixed(3)}</td></tr> })}</tbody></table></div></div>
            <div className="grid-2" style={{ marginTop: 16 }}><div className="card"><h3 className="chart-title">Product-level review</h3><p className="chart-sub">Max package score per derived product; K is a product budget.</p><div className="mini-grid"><div><div className="kpi-label">v0.4 flagged products</div><strong>{productMetrics.risk_score_v04.flaggedProducts}</strong></div><div><div className="kpi-label">v0.5 flagged products</div><strong>{productMetrics.risk_score_v05.flaggedProducts}</strong></div><div><div className="kpi-label">Derived products</div><strong>112,966</strong></div></div><p className="chart-sub" style={{ marginTop: 16 }}>96 package flags map to 83 derived products. One malformed package NDC is excluded from product aggregates.</p></div><div className="card"><h3 className="chart-title">Product-cluster uncertainty</h3><p className="chart-sub">1,000 seeded replicates; products are resampled as clusters while observed package order is held fixed.</p><div className="detail-grid"><div className="detail-item"><small>v0.4 Recall@500</small><strong>{bootstrapMetrics.risk_score_v04.recall}</strong></div><div className="detail-item"><small>v0.5 Recall@500</small><strong>{bootstrapMetrics.risk_score_v05.recall}</strong></div><div className="detail-item"><small>v0.4 AP interval</small><strong>{bootstrapMetrics.risk_score_v04.ap}</strong></div><div className="detail-item"><small>v0.5 AP interval</small><strong>{bootstrapMetrics.risk_score_v05.ap}</strong></div></div></div></div>
          </section>

          <section className="section" id="methodology">
            <div className="section-heading"><div><div className="eyebrow">05 / Methodology</div><h2>Useful, with edges visible.</h2></div><p>PharmaOpt is designed to make assumptions inspectable. Read the methodology before treating any ranking as operational evidence.</p></div>
            <div className="grid-2"><div className="card"><h3 className="chart-title">Data and modeling</h3><ul className="method-list"><li>2025 cohort: 221,667 unique package NDC records.</li><li>Sources include FDA NDC, shortage and recall records plus lagged CMS Part D features in the underlying pipeline.</li><li>v0.4 is the simpler saved ranking; v0.5 adds recall-language-derived features.</li><li>Evaluation uses deterministic descending scores with package NDC tie-breaking.</li><li>Historical labels are FDA-linked event indicators, not verified future shortages.</li></ul></div><div className="card"><h3 className="chart-title">What this does not mean</h3><ul className="method-list"><li>A high score is not a probability, diagnosis, procurement recommendation, or clinical signal.</li><li>2025 was inspected during development and is not an untouched prospective test.</li><li>Package and product-level metrics answer different review questions.</li><li>Product identifiers are derived from NDC structure in the web artifact; the canonical pipeline uses FDA relationships.</li><li>Do not use this prototype for live shortage monitoring or purchasing decisions.</li></ul></div></div>
            <div className="card" style={{ marginTop: 16, display: "flex", justifyContent: "space-between", gap: 20, alignItems: "center", flexWrap: "wrap" }}><div><div className="eyebrow">Open research</div><h3 style={{ margin: "8px 0 0" }}>Read the source and evaluation artifacts.</h3></div><a className="button button-primary" href="https://github.com/joaquinpizano/pharmaopt" target="_blank" rel="noreferrer">View GitHub <ArrowUpRight size={15} /></a></div>
          </section>
        </div>
      </main>
      <footer className="footer"><span>PharmaOpt / independent research prototype</span><span>Historical data · transparent assumptions · no live shortage predictions</span></footer>
    </div>
  );
}

export default App;
