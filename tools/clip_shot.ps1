# clip_shot.ps1 — 把剪贴板里的截图存成 shots/<UTC 时间戳>.png，打印绝对路径（Windows）
# 用法: powershell -NoProfile -ExecutionPolicy Bypass -File tools/clip_shot.ps1
# 无图时打印 NO_IMAGE 并退出 2；成功打印绝对路径并退出 0。输出目录: <仓库根>/shots/
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$img = [System.Windows.Forms.Clipboard]::GetImage()
if ($null -eq $img) {
    Write-Output "NO_IMAGE"
    exit 2
}
$dir = Join-Path (Split-Path -Parent $PSScriptRoot) "shots"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
$out = Join-Path $dir ($stamp + ".png")
$img.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$img.Dispose()
Write-Output (Resolve-Path $out).Path
exit 0
