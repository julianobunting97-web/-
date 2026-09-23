$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$release = (Resolve-Path -LiteralPath (Join-Path $workspace '.sites-release')).Path
$mobile = (Resolve-Path -LiteralPath (Join-Path $workspace '.sites-mobile')).Path
$separator = [IO.Path]::DirectorySeparatorChar

if (-not $release.StartsWith($workspace + $separator, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'The release checkout must stay inside the workspace.'
}

$portfolio = (Resolve-Path -LiteralPath (Join-Path $release 'public\portfolio')).Path
if (-not $portfolio.StartsWith($release + $separator, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'The portfolio assets must stay inside the release checkout.'
}

$oldImages = Get-ChildItem -LiteralPath $portfolio -Recurse -File |
  Where-Object { $_.Extension -match '^\.(png|jpe?g)$' }
foreach ($file in $oldImages) {
  if (-not $file.FullName.StartsWith($portfolio + $separator, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Asset escaped the release checkout: $($file.FullName)"
  }
  Remove-Item -LiteralPath $file.FullName
}

$assetDirectory = (Resolve-Path -LiteralPath (Join-Path $release 'src\assets')).Path
$unusedAssets = Get-ChildItem -LiteralPath $assetDirectory -File |
  Where-Object { $_.Name -ne 'hero-background.mp4' }
foreach ($file in $unusedAssets) {
  if (-not $file.FullName.StartsWith($assetDirectory + $separator, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Source asset escaped the release checkout: $($file.FullName)"
  }
  Remove-Item -LiteralPath $file.FullName
}

$distTarget = Join-Path $release 'dist'
$expectedDist = Join-Path $workspace '.sites-release\dist'
if (-not [string]::Equals($distTarget, $expectedDist, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'Unexpected release build directory.'
}
if (Test-Path -LiteralPath $distTarget) {
  $resolvedDist = (Resolve-Path -LiteralPath $distTarget).Path
  if (-not $resolvedDist.StartsWith($release + $separator, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The build directory must stay inside the release checkout.'
  }
  Remove-Item -LiteralPath $resolvedDist -Recurse -Force
}
Copy-Item -LiteralPath (Join-Path $mobile 'dist') -Destination $distTarget -Recurse

Write-Output "Prepared release: removed $($oldImages.Count) original image files and $($unusedAssets.Count) unused source assets."
