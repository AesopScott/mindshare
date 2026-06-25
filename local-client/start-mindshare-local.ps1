Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$localClientRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Push-Location $localClientRoot
try {
    if (-not (Test-Path -LiteralPath (Join-Path $localClientRoot "node_modules"))) {
        npm install
    }

    npm start
}
finally {
    Pop-Location
}
