$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$release = (Resolve-Path -LiteralPath (Join-Path $workspace '.sites-release')).Path
$build = (Resolve-Path -LiteralPath (Join-Path $release 'dist')).Path
$temporary = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd([IO.Path]::DirectorySeparatorChar)
$separator = [IO.Path]::DirectorySeparatorChar
$stage = Join-Path $temporary ('caoshuo-sites-stage-' + [guid]::NewGuid().ToString('N'))
$archive = Join-Path $temporary ('caoshuo-mobile-site-' + [guid]::NewGuid().ToString('N') + '.tar.gz')

if (-not $release.StartsWith($workspace + $separator, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'The release checkout must stay inside the workspace.'
}
if (-not $build.StartsWith($release + $separator, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'The build must stay inside the release checkout.'
}
if (-not $stage.StartsWith($temporary + $separator, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'The packaging stage must stay inside the temp directory.'
}

New-Item -ItemType Directory -Path $stage | Out-Null
Copy-Item -LiteralPath $build -Destination (Join-Path $stage 'dist') -Recurse
$manifestDirectory = Join-Path $stage 'dist\.openai'
New-Item -ItemType Directory -Path $manifestDirectory -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $release '.openai\hosting.json') -Destination (Join-Path $manifestDirectory 'hosting.json')

& tar.exe -czf $archive -C $stage dist
if ($LASTEXITCODE -ne 0) { throw 'Could not create the Sites archive.' }
$entries = & tar.exe -tzf $archive
if ($LASTEXITCODE -ne 0 -or $entries -notcontains 'dist/.openai/hosting.json' -or $entries -notcontains 'dist/index.html') {
  throw 'The Sites archive is missing its manifest or index.'
}
$resolvedStage = (Resolve-Path -LiteralPath $stage).Path
if (-not $resolvedStage.StartsWith($temporary + $separator, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'Refusing to remove a packaging stage outside the temp directory.'
}
Remove-Item -LiteralPath $resolvedStage -Recurse -Force
$archiveInfo = Get-Item -LiteralPath $archive
Write-Output "ARCHIVE=$($archiveInfo.FullName)"
Write-Output "BYTES=$($archiveInfo.Length)"
Write-Output "ENTRIES=$($entries.Count)"
