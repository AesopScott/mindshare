Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$localClientRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$mindshareRoot = Split-Path -Parent $localClientRoot
$codeRoot = Split-Path -Parent $mindshareRoot
$mojoRoot = Join-Path $codeRoot "mojo"
$contentRoot = Join-Path $localClientRoot "app-content"

function Invoke-RoboCopy {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Source path not found: $Source"
    }

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    & robocopy $Source $Destination /E /R:1 /W:1 /XD ".git" "node_modules" "__pycache__" ".pytest_cache" ".mypy_cache" /XF "*.pyc" "*.pyo" "*.log" ".DS_Store" "Thumbs.db" | Out-Host
    if ($LASTEXITCODE -gt 7) {
        throw "robocopy failed from $Source to $Destination with exit code $LASTEXITCODE"
    }
}

New-Item -ItemType Directory -Force -Path $contentRoot | Out-Null

Invoke-RoboCopy -Source (Join-Path $mindshareRoot "public") -Destination (Join-Path $contentRoot "public")
Invoke-RoboCopy -Source (Join-Path $mindshareRoot "roles\autonomy-engineer") -Destination (Join-Path $contentRoot "mindshare\roles\autonomy-engineer")

Invoke-RoboCopy -Source (Join-Path $mojoRoot "roles\mojo-maps-engineer") -Destination (Join-Path $contentRoot "mojo\roles\mojo-maps-engineer")
Invoke-RoboCopy -Source (Join-Path $mojoRoot "assets\maps") -Destination (Join-Path $contentRoot "mojo\assets\maps")
Invoke-RoboCopy -Source (Join-Path $mojoRoot "agents") -Destination (Join-Path $contentRoot "mojo\agents")

$manifest = [ordered]@{
    generatedAt = (Get-Date).ToUniversalTime().ToString("o")
    contentRoot = $contentRoot
    sources = [ordered]@{
        public = (Join-Path $mindshareRoot "public")
        tessRole = (Join-Path $mindshareRoot "roles\autonomy-engineer")
        beaRole = (Join-Path $mojoRoot "roles\mojo-maps-engineer")
        mojoMaps = (Join-Path $mojoRoot "assets\maps")
        mojoAgents = (Join-Path $mojoRoot "agents")
    }
}

$manifestPath = Join-Path $contentRoot "manifest.json"
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Path $manifestPath -Encoding UTF8

Write-Output "MindShare Local app content synced to $contentRoot"
Write-Output "Manifest: $manifestPath"
