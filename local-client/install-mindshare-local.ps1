param(
    [string]$ExtensionId = "fomlcadcldjpnlbapddpmlikinmdiiji"
)

$ErrorActionPreference = "Stop"

$localClientRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$nativeInstaller = Join-Path $localClientRoot "native-host\install-chrome-native-host.ps1"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js was not found on PATH. MindShare Local currently needs Node.js to run the native host."
}

if (-not (Test-Path -LiteralPath $nativeInstaller)) {
    throw "MindShare native-host installer not found: $nativeInstaller"
}

& powershell -ExecutionPolicy Bypass -File $nativeInstaller -ExtensionId $ExtensionId

Write-Output ""
Write-Output "MindShare Local native messaging is registered."
Write-Output "Extension ID: $ExtensionId"
Write-Output ""
Write-Output "Next step for persistent Chrome use:"
Write-Output "1. Open chrome://extensions"
Write-Output "2. Enable Developer mode"
Write-Output "3. Load unpacked: $localClientRoot\chrome-extension"
Write-Output ""
Write-Output "For a temporary test browser, run:"
Write-Output "powershell -ExecutionPolicy Bypass -File `"$localClientRoot\start-mindshare-test-chrome.ps1`""
