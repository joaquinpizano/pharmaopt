# PharmaOpt Web v1 verification — November 12, 2026

## Repository and preservation

Branch: `pharmaopt-v2-quality`. HEAD remains
`7e24cdcd0b9129178908a5c24394e0116ce87012`.
No commit, push, or deployment was performed.

The incoming launcher and complete web source were backed up before editing at
`C:\Users\jpiza\AppData\Local\Temp\pharmaopt-handoff-20261112-200500`.
Generated `node_modules/` and `.next/` were excluded. The original Streamlit app,
Python metrics/evaluation/validation scripts, notebooks, saved evaluation outputs,
and historical source datasets have no Git diff. A full pandas frame comparison
confirmed that the web gzip matches every row and column of the corrected source.

The only modified tracked file is `.github/workflows/ci.yml`, which adds a web
job (Node 22, clean install, type checks, lint, tests, build) alongside Python CI.
That remote CI job has not run; local checks used Node 26.13.1 and Python 3.15.

Untracked files are the root launcher, `scripts/launch_pharmaopt.ps1`, this report,
and all web source listed below. Generated dependencies/build output remain ignored.

```text
Launch PharmaOpt.bat
scripts/launch_pharmaopt.ps1
docs/web-v1-verification.md
web/.gitignore
web/README.md
web/data/pharmaopt_packages.csv.gz
web/eslint.config.mjs
web/next-env.d.ts
web/next.config.ts
web/package-lock.json
web/package.json
web/postcss.config.mjs
web/public/logo-mark.svg
web/public/logo.ico
web/public/logo.svg
web/src/app/api/health/route.ts
web/src/app/api/packages/route.test.ts
web/src/app/api/packages/route.ts
web/src/app/globals.css
web/src/app/icon.svg
web/src/app/layout.tsx
web/src/app/page.tsx
web/src/lib/evaluation.test.ts
web/src/lib/evaluation.ts
web/src/lib/types.ts
web/tsconfig.json
web/vitest.config.ts
```

## Functionality and fixes

All five sections are implemented: Overview, Budget Planner, Drug Explorer,
Model Evaluation, and Methodology. Model selection, hypothetical budget/cost/
capacity arithmetic, deterministic ranking, server-side search, historical filters,
pagination, details, retrospective metrics, and uncertainty displays are available.
Explorer searches the complete cohort; unlike Streamlit's selected-sample explorer,
it deliberately does not restrict results to the hypothetical planner budget.
Its copy identifies this scope.

Confirmed fixes:

- HTTP errors no longer enter the client as package data and crash rendering.
- Aborted/stale requests cannot replace newer model/search results.
- Reset retries failed requests even when filters already have their default values.
- Empty results display guidance; model changes clear stale package details.
- NaN, infinite, fractional, zero, and negative pagination use safe defaults;
  response pages are bounded to 50 rows.
- API errors no longer disclose filesystem paths to clients.
- Both model orderings share records rather than duplicating the whole cohort.
- NDC tie-breaking uses lexical ordering consistent with the Python implementation.
- Random expectation uses exact prevalence, fixing the displayed @500 value
  from 0.216 to 0.217.
- The study snapshot reflects the chosen model; branding stacks correctly;
  inline icons, chart spacing, long detail values, keyboard focus, mobile menu
  state, and pagination labels were improved.
- Type checks generate Next.js route definitions before invoking TypeScript.
- The cohort-cap test now actually exercises selection beyond the cohort size.
- Production dependency advisories were fixed with csv-parse 7.0.3 and a scoped
  PostCSS 8.5.32 override; Vitest 4.1.11 removes high/critical test-tool findings.

## Verification results

Passed:

- Clean `npm ci` with the parser/PostCSS patches; subsequent Vitest upgrade
  installed successfully and updated the lockfile.
- TypeScript (`next typegen && tsc --noEmit`), ESLint, production build.
- Vitest: 7 tests across planner/metrics and the real package API.
- Python unittest discovery: 10 tests, including existing Streamlit AppTest checks.
- Dataset validator: 221,667 rows, 96 flags (12 non-discontinuation, 84 discontinuation).
- Model timing safeguard validator.
- All six published capture budgets reproduce for both models:
  v0.4 `[1, 5, 10, 10, 11, 17]`; v0.5 `[0, 3, 7, 7, 14, 17]`.
- Planner formula and tiers match the existing Streamlit implementation.
- Chrome automation against both development and production servers: five sections,
  model selection, filters, page changes, details, empty search, simulated HTTP 500,
  recovery, mobile menu, and no horizontal document overflow at 320px and 390px.
- Production browser slider checks: a $10,000 budget at $1,000 selects 10 packages;
  changing the per-package cost to $5,000 selects 2.
- Screenshots reviewed at desktop and mobile widths; no browser page errors.
- Logo, Windows icon, favicon, and health endpoint return HTTP 200;
  `/data/pharmaopt_packages.csv.gz` returns 404.
- Production npm audit: zero reported vulnerabilities. Full audit: eight moderate,
  zero high, zero critical findings, all in the development lint/test chain.

Initial command failures were environment issues: Node was absent from PATH,
the Python 3.13 interpreter lacked project dependencies, and the filesystem sandbox
prevented esbuild from traversing a parent directory. Explicit executable paths,
the existing Python 3.15 environment, and an approved unsandboxed test run resolved
them. No final application test fails.

Nonfatal warnings: Next.js does not detect the custom ESLint plugin configuration
during build, although explicit ESLint passes; some existing dependencies are
deprecated. Eight moderate tooling advisories remain for a future compatible
lint/test dependency update. No remote CI run or hosted load test was performed.

## Windows launcher and shortcut

The batch entry point delegates to `scripts/launch_pharmaopt.ps1` and preserves
its exit status. The helper locates Node, installs missing dependencies, checks
application identity at `/api/health`, remembers the chosen port, and serializes
simultaneous launches with a mutex. Startup uses a hidden, localhost-bound server
with stdout/stderr logs under `%TEMP%/pharmaopt-<checkout hash>/`.

Verified fresh startup on 3000 and repeat reuse. With an unrelated HTTP server on
3000, the launcher chose 3001; a repeat invocation reused 3001. The unrelated
process was not terminated by the launcher. Errors include a useful message and,
for startup failures, log paths. No elevation is requested by launcher code.
Automated launches used `-NoBrowser`; browser opening uses the Windows default URL
association, but a physical desktop double-click was not manually observed.

The existing OneDrive Desktop shortcut had an empty target. It was repaired and
read back outside the sandbox: target is
`C:\Users\jpiza\PharmaOpt-v2-work\Launch PharmaOpt.bat`, working directory is the
repository, and icon is `web\public\logo.ico,0`. Local test servers are stopped
after verification; the launcher can start a new one on demand.

## Vercel readiness and remaining work

Ready for an approved preview deployment using root `web`, the Next.js preset,
install `npm ci`, build `npm run build`, and the default output directory.
No environment variables are needed. Use the Node.js runtime, not static export
or Edge. Tracing includes the runtime dataset. The final local package API trace
totals 13,470,273 bytes, including the 6,146,760-byte gzip. This is below Vercel's
documented standard 250 MB function limit. See
[Vercel function limits](https://vercel.com/docs/functions/limitations) and
[Next.js output tracing](https://nextjs.org/docs/app/api-reference/config/next-config-js/output).

Local production measurements: approximately 1.3 seconds for first package load,
331 ms to initialize the second model, 129 ms for a name search, 10 ms for warm
unfiltered requests, and 353 MB process working set after both rankings. These
are local observations, not serverless or peak-concurrency guarantees. CSV parsing
is synchronous and each search scans the cached cohort; a database/index is the
next scaling step if hosted concurrency or cold starts become material.

The export is outside public assets, but its paginated records are intentionally
public and can be collected through repeated API calls. It contains the existing
public research data; it is not a private-data access boundary. No new secrets or
environment files are required.

Remaining items: review the uncommitted source, approve a commit/push separately,
run the new CI job on GitHub, then approve a Vercel preview. On that preview,
measure cold starts, peak memory, and concurrent searches. Moderate tooling
advisories should be addressed in the next dependency maintenance pass. No
deployment has been attempted, and hosted behavior remains unverified.
