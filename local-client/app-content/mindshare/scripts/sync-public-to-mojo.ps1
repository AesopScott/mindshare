param(
    [string]$MindshareRoot = "C:\Users\scott\Code\mindshare",
    [string]$MojoRoot = "C:\Users\scott\Code\mojo"
)

$ErrorActionPreference = "Stop"

# Mindshare public is the authored source. Mojo\MindShare is the deploy mirror.
# If a fix is made in Mojo first, pull it back into Mindshare\public before continuing.
$source = Join-Path $MindshareRoot "public"
$target = Join-Path $MojoRoot "MindShare"

if (-not (Test-Path -LiteralPath $source)) {
    throw "Mindshare public folder not found: $source"
}

New-Item -ItemType Directory -Force -Path $target | Out-Null

Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
    $destination = Join-Path $target $_.Name
    if (Test-Path -LiteralPath $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
}

Write-Output "Synced $source to $target"
