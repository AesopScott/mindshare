$ErrorActionPreference = "Stop"

$localClientRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$server = Join-Path $localClientRoot "mindshare-local-bridge-server.js"

if (-not (Test-Path -LiteralPath $server)) {
    throw "MindShare local bridge server not found: $server"
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js was not found on PATH. MindShare Local Bridge needs Node.js."
}

node $server
