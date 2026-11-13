param([switch]$NoBrowser, [int]$TimeoutSeconds = 120)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$web = Join-Path $root 'web'

function Test-PharmaOpt([int]$Port) {
    try {
        $health = Invoke-RestMethod "http://localhost:$Port/api/health" -TimeoutSec 2
        return $health.application -eq 'pharmaopt-web' -and $health.status -eq 'ok'
    } catch { return $false }
}

try {
    if (!(Test-Path -LiteralPath (Join-Path $web 'package.json'))) { throw "Web application missing at $web" }
    $hash = [Security.Cryptography.SHA256]::Create()
    $key = [BitConverter]::ToString($hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($root))).Replace('-', '').Substring(0, 16)
    $state = Join-Path ([IO.Path]::GetTempPath()) "pharmaopt-$key"
    New-Item -ItemType Directory -Path $state -Force | Out-Null
    $mutex = New-Object Threading.Mutex($false, "Local\PharmaOpt-$key")
    if (!$mutex.WaitOne(150000)) { throw 'Another PharmaOpt launcher is still starting. Please try again shortly.' }
    try {
        $portFile = Join-Path $state 'port.txt'
        $candidates = @(3000)
        if (Test-Path -LiteralPath $portFile) {
            $saved = 0
            if ([int]::TryParse((Get-Content -LiteralPath $portFile -Raw).Trim(), [ref]$saved) -and $saved -ge 3000 -and $saved -le 65535) { $candidates = @($saved, 3000) | Select-Object -Unique }
        }
        $port = $null
        foreach ($candidate in $candidates) {
            if (Test-PharmaOpt $candidate) { $port = $candidate; break }
        }
        if (!$port) {
            $node = (Get-Command node.exe -ErrorAction SilentlyContinue).Source
            if (!$node -and (Test-Path -LiteralPath "$env:ProgramFiles\nodejs\node.exe")) { $node = "$env:ProgramFiles\nodejs\node.exe" }
            if (!$node -and (Test-Path -LiteralPath "$env:LOCALAPPDATA\Programs\nodejs\node.exe")) { $node = "$env:LOCALAPPDATA\Programs\nodejs\node.exe" }
            if (!$node) { throw 'Node.js is missing. Install Node.js LTS from https://nodejs.org/ and try again.' }
            $env:PATH = "$(Split-Path $node);$env:PATH"
            $next = Join-Path $web 'node_modules\next\dist\bin\next'
            if (!(Test-Path -LiteralPath $next)) {
                Push-Location $web
                try {
                    & (Join-Path (Split-Path $node) 'npm.cmd') ci --no-audit --no-fund
                    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Check your connection and npm output.' }
                } finally { Pop-Location }
            }
            $port = 3000
            while ($port -le 65535) {
                $listener = New-Object Net.Sockets.TcpListener([Net.IPAddress]::IPv6Any, $port)
                $listener.Server.DualMode = $true
                try { $listener.Start(); break } catch { $port++ } finally { $listener.Stop() }
            }
            if ($port -gt 65535) { throw 'No free local port was found.' }
            $stdout = Join-Path $state 'server.log'
            $stderr = Join-Path $state 'server-error.log'
            Write-Host "[PharmaOpt] Starting http://localhost:$port ..."
            $server = Start-Process -FilePath $node -ArgumentList @("`"$next`"", 'dev', '-H', 'localhost', '-p', $port) -WorkingDirectory $web -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
            $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
            while (!(Test-PharmaOpt $port)) {
                if ($server.HasExited) { throw "Server exited. See $stderr and $stdout" }
                if ((Get-Date) -ge $deadline) { throw "Server startup timed out. See $stderr and $stdout" }
                Start-Sleep -Milliseconds 500
            }
        }
        Set-Content -LiteralPath $portFile -Value $port
        Write-Host "[PharmaOpt] Ready at http://localhost:$port"
        if (!$NoBrowser) { Start-Process "http://localhost:$port" }
    } finally { $mutex.ReleaseMutex(); $mutex.Dispose() }
} catch {
    Write-Host "[PharmaOpt] $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
