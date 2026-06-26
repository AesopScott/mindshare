param(
    [string]$Url = "https://mojoaistudio.com/MindShare/departments/?division=technology-and-data"
)

$ErrorActionPreference = "Stop"

$localClientRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$extensionRoot = Join-Path $localClientRoot "chrome-extension"
$profileRoot = Join-Path $env:TEMP "mindshare-chrome-test-profile"

if (-not (Test-Path -LiteralPath $extensionRoot)) {
    throw "MindShare Chrome extension folder not found: $extensionRoot"
}

$chromeCandidates = @(@(
    (Join-Path ${env:ProgramFiles} "Google\Chrome\Application\chrome.exe"),
    (Join-Path ${env:ProgramFiles(x86)} "Google\Chrome\Application\chrome.exe"),
    (Join-Path $env:LOCALAPPDATA "Google\Chrome\Application\chrome.exe")
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) })

if (-not $chromeCandidates.Count) {
    throw "Chrome was not found in the standard install locations."
}

$chrome = $chromeCandidates[0]
New-Item -ItemType Directory -Force -Path $profileRoot | Out-Null

$arguments = @(
    "--user-data-dir=$profileRoot",
    "--load-extension=$extensionRoot",
    "--no-first-run",
    "--no-default-browser-check",
    "--new-window",
    $Url
)

Start-Process -FilePath $chrome -ArgumentList $arguments

Write-Output "Started Chrome test profile with MindShare extension loaded."
Write-Output "URL: $Url"
