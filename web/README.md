# PharmaOpt web application

This Next.js application is a presentation layer over the validated PharmaOpt
2025 cohort. It does not retrain models or change the Python analytics
pipeline.

## Local development

```powershell
cd web
npm ci
npm run dev
```

Open http://localhost:3000.

Windows users can also double-click [`Launch PharmaOpt.bat`](../Launch%20PharmaOpt.bat)
from the repository root. It finds Node.js, installs missing dependencies from the
lockfile, reuses a running PharmaOpt server, and selects another free port when
port 3000 belongs to another application. The PowerShell helper remembers the
selected port, serializes simultaneous launches, binds the server to localhost,
and saves startup logs in `%TEMP%/pharmaopt-<checkout hash>/`. It needs no
administrator permissions. Startup errors include the log location. For checks
without opening a browser, run `powershell -NoProfile -ExecutionPolicy Bypass
-File scripts/launch_pharmaopt.ps1 -NoBrowser` from the repository root.

## Validation

```powershell
npm run typecheck
npm run lint
npm test
npm run build
```

## Vercel deployment

1. Import the repository in Vercel.
2. Set the project **Root Directory** to `web`.
3. Use the default Next.js framework preset.
4. Build command: `npm run build`.
5. No environment variables are required for the public research prototype.
6. Confirm the server-only `web/data/pharmaopt_packages.csv.gz` export is
   included in the deployment and is not exposed as a static public asset.

The package API reads the compressed export only on the server and returns
bounded pages. It never sends the full cohort to the browser.

The API uses the Node.js runtime; do not configure static export or Edge runtime.
The export is included in the `/api/packages` server bundle through
`outputFileTracingIncludes`. It is approximately 6 MB compressed; the API
parses it lazily and caches the ranked records in process memory. This is
appropriate for a research prototype, but a production-scale deployment
should move querying to a database or precomputed index if cold starts,
memory, or serverless bundle limits become material. Both rankings share package
records; only their sort order is cached separately. API failures return a generic
message, with diagnostic details confined to server logs. Pages contain at most
50 records. The API is intentionally public: bounded pagination limits individual
responses, but does not prevent someone from collecting the public cohort over
multiple requests. No credentials or private patient records are required.

Local production verification on November 12, 2026 measured a 13,470,273-byte
traced package API bundle including the 6,146,760-byte gzip, about 353 MB process
working set after querying both models, a 1.3-second initial request, and roughly
10 ms warm unfiltered requests. A name search took 129 ms. These are local
measurements, not serverless guarantees. The gzip URL returns 404; paginated API
records remain public. Confirm cold start, peak memory, and concurrent search
latency in Vercel after deployment approval.

Vercel settings: root `web`, Next.js preset, install `npm ci`, build
`npm run build`, default Next.js output directory, no environment variables.
Keep `data/` out of `public/`. The compressed file is a traced runtime input;
its decompressed CSV occupies memory and is not a separate deployment asset.
The local traced bundle is well below the documented standard 250 MB function
bundle limit. Review the current [function limits](https://vercel.com/docs/functions/limitations)
and [Next.js tracing guidance](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)
when creating the Vercel project. No deployment was performed.

Dependency review: production audit reports zero vulnerabilities after updating
`csv-parse` to 7.0.3 and overriding Next.js's nested PostCSS to 8.5.32. Vitest
was updated to 4.1.11. The full audit still reports eight moderate development
dependency findings through minimatch and the lint/test dependency chain; there
are no remaining high or critical findings. Keep development/test servers local
and revisit these advisories during the next tooling upgrade. Normal usage runs
`vitest run`, not a publicly reachable test UI.

## Brand assets

- [`public/logo.svg`](./public/logo.svg) is the full wordmark.
- [`public/logo-mark.svg`](./public/logo-mark.svg) is the icon-only variation.
- [`src/app/icon.svg`](./src/app/icon.svg) supplies the browser favicon.
