Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$localClientRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$mindshareRoot = Split-Path -Parent $localClientRoot
$codeRoot = Split-Path -Parent $mindshareRoot
$mojoRoot = Join-Path $codeRoot "mojo"
$watchRoot = Join-Path $codeRoot "watch"
$mindshareDriveRoot = "G:\My Drive\Mindshare"
$contentRoot = Join-Path $localClientRoot "app-content"

function Clear-AppContent {
    $resolvedLocalClientRoot = [System.IO.Path]::GetFullPath($localClientRoot)
    $resolvedContentRoot = [System.IO.Path]::GetFullPath($contentRoot)

    if (-not $resolvedContentRoot.StartsWith($resolvedLocalClientRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to clear content outside local client root: $resolvedContentRoot"
    }

    if (Test-Path -LiteralPath $resolvedContentRoot) {
        Remove-Item -LiteralPath $resolvedContentRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $resolvedContentRoot | Out-Null
}

function Invoke-RoboCopy {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Source path not found: $Source"
    }

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    & robocopy $Source $Destination /E /R:1 /W:1 `
        /XD ".git" ".claude" ".codex" ".obsidian" ".pytest_cache" ".mypy_cache" ".wrangler" "__pycache__" "node_modules" "tmp" `
        /XF ".DS_Store" ".env" ".env.*" "*.key" "*.pem" "*.pfx" "*.pyc" "*.pyo" "*.log" "Thumbs.db" | Out-Host
    if ($LASTEXITCODE -gt 7) {
        throw "robocopy failed from $Source to $Destination with exit code $LASTEXITCODE"
    }
}

function Copy-DirectoryIfPresent {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination,
        [System.Collections.ArrayList]$CopiedSources,
        [System.Collections.ArrayList]$MissingSources
    )

    if (Test-Path -LiteralPath $Source) {
        Invoke-RoboCopy -Source $Source -Destination $Destination
        [void]$CopiedSources.Add([ordered]@{
            source = $Source
            destination = $Destination
            type = "directory"
        })
    } else {
        [void]$MissingSources.Add($Source)
    }
}

function Copy-FileIfPresent {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination,
        [System.Collections.ArrayList]$CopiedSources,
        [System.Collections.ArrayList]$MissingSources
    )

    if (Test-Path -LiteralPath $Source) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
        [void]$CopiedSources.Add([ordered]@{
            source = $Source
            destination = $Destination
            type = "file"
        })
    } else {
        [void]$MissingSources.Add($Source)
    }
}

function Convert-ToPortableSource {
    param([Parameter(Mandatory = $true)][string]$Source)

    $resolvedSource = [System.IO.Path]::GetFullPath($Source)
    $roots = @(
        @{ Prefix = "mindshare"; Path = [System.IO.Path]::GetFullPath($mindshareRoot) },
        @{ Prefix = "mojo"; Path = [System.IO.Path]::GetFullPath($mojoRoot) },
        @{ Prefix = "watch"; Path = [System.IO.Path]::GetFullPath($watchRoot) },
        @{ Prefix = "mindshare-drive"; Path = [System.IO.Path]::GetFullPath($mindshareDriveRoot) }
    )

    foreach ($root in $roots) {
        if ($resolvedSource.StartsWith($root.Path, [System.StringComparison]::OrdinalIgnoreCase)) {
            $relative = $resolvedSource.Substring($root.Path.Length).TrimStart("\", "/")
            if ([string]::IsNullOrWhiteSpace($relative)) {
                return $root.Prefix
            }
            return ($root.Prefix + "/" + ($relative -replace "\\", "/"))
        }
    }

    return (Split-Path -Leaf $Source)
}

function Convert-ToPortableDestination {
    param([Parameter(Mandatory = $true)][string]$Destination)

    $resolvedDestination = [System.IO.Path]::GetFullPath($Destination)
    $resolvedContentRoot = [System.IO.Path]::GetFullPath($contentRoot)
    if ($resolvedDestination.StartsWith($resolvedContentRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return ($resolvedDestination.Substring($resolvedContentRoot.Length).TrimStart("\", "/") -replace "\\", "/")
    }
    return (Split-Path -Leaf $Destination)
}

function Convert-CopyRecords {
    param([Parameter(Mandatory = $true)][System.Collections.ArrayList]$Records)

    return @($Records | ForEach-Object {
        [ordered]@{
            source = Convert-ToPortableSource -Source $_.source
            destination = Convert-ToPortableDestination -Destination $_.destination
            type = $_.type
        }
    })
}

$copiedSources = [System.Collections.ArrayList]::new()
$missingSources = [System.Collections.ArrayList]::new()

Clear-AppContent

Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "public") -Destination (Join-Path $contentRoot "mindshare\public") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "roles") -Destination (Join-Path $contentRoot "mindshare\roles") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "agents") -Destination (Join-Path $contentRoot "mindshare\agents") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "catalogs") -Destination (Join-Path $contentRoot "mindshare\catalogs") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "docs") -Destination (Join-Path $contentRoot "mindshare\docs") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "phases") -Destination (Join-Path $contentRoot "mindshare\phases") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "rooms") -Destination (Join-Path $contentRoot "mindshare\rooms") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "scripts") -Destination (Join-Path $contentRoot "mindshare\scripts") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "skills") -Destination (Join-Path $contentRoot "mindshare\skills") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mindshareRoot "templates") -Destination (Join-Path $contentRoot "mindshare\templates") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-FileIfPresent -Source (Join-Path $mindshareRoot "AGENTS.md") -Destination (Join-Path $contentRoot "mindshare\AGENTS.md") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-FileIfPresent -Source (Join-Path $mindshareRoot "project-foundation.md") -Destination (Join-Path $contentRoot "mindshare\project-foundation.md") -CopiedSources $copiedSources -MissingSources $missingSources

Copy-FileIfPresent -Source (Join-Path $mindshareDriveRoot "roles.md") -Destination (Join-Path $contentRoot "mindshare\global\roles.md") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-FileIfPresent -Source (Join-Path $mindshareDriveRoot "role-artifacts.md") -Destination (Join-Path $contentRoot "mindshare\global\role-artifacts.md") -CopiedSources $copiedSources -MissingSources $missingSources

Copy-DirectoryIfPresent -Source (Join-Path $mojoRoot "agents") -Destination (Join-Path $contentRoot "mojo\agents") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mojoRoot "assets\maps") -Destination (Join-Path $contentRoot "mojo\assets\maps") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mojoRoot "maps") -Destination (Join-Path $contentRoot "mojo\maps") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $mojoRoot "roles") -Destination (Join-Path $contentRoot "mojo\roles") -CopiedSources $copiedSources -MissingSources $missingSources

Copy-DirectoryIfPresent -Source (Join-Path $watchRoot "agents") -Destination (Join-Path $contentRoot "watch\agents") -CopiedSources $copiedSources -MissingSources $missingSources
Copy-DirectoryIfPresent -Source (Join-Path $watchRoot "roles") -Destination (Join-Path $contentRoot "watch\roles") -CopiedSources $copiedSources -MissingSources $missingSources

$manifest = [ordered]@{
    generatedAt = (Get-Date).ToUniversalTime().ToString("o")
    contentRoot = "."
    copiedSources = Convert-CopyRecords -Records $copiedSources
    missingSources = @($missingSources | ForEach-Object { Convert-ToPortableSource -Source $_ })
}

$manifestPath = Join-Path $contentRoot "manifest.json"
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Path $manifestPath -Encoding UTF8

Write-Output "MindShare Local app content synced to $contentRoot"
Write-Output "Manifest: $manifestPath"
