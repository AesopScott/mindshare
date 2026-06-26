param(
    [Parameter(Mandatory = $true)]
    [string]$ExtensionId
)

$ErrorActionPreference = "Stop"

$hostName = "com.mindshare.local_client"
$hostRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifestPath = Join-Path $hostRoot "$hostName.json"
$runnerPath = Join-Path $hostRoot "run-native-host.cmd"

if (-not (Test-Path -LiteralPath $runnerPath)) {
    throw "Native host runner not found: $runnerPath"
}

$manifest = [ordered]@{
    name = $hostName
    description = "MindShare Local Client Native Host"
    path = $runnerPath
    type = "stdio"
    allowed_origins = @("chrome-extension://$ExtensionId/")
}

$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$registryPath = "HKCU:\Software\Google\Chrome\NativeMessagingHosts\$hostName"
New-Item -Path $registryPath -Force | Out-Null
Set-Item -Path $registryPath -Value $manifestPath

Write-Output "Registered $hostName for Chrome."
Write-Output "Manifest: $manifestPath"
Write-Output "Allowed extension: chrome-extension://$ExtensionId/"
