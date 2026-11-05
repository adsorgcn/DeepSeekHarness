# bootstrap.ps1 — DeepSeekHarness 记忆体一键引导（Windows）
#
# 原则：全部软件只从官方源安装；每步要不要人审批由 DSH 的审批模式决定——
#   · 不需要审批的（检测、克隆、切目录、验收）→ 自动跑
#   · 需要审批的（装 Git / Python 等系统软件）→ agent 先问用户，同意后执行
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1             # 只检测并打印计划（默认，零改动）
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1 -Install -Yes   # 按计划执行（用户已审批后）
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1 -Install -TargetDir "D:\mem" -Yes

param(
    [switch]$Install,
    [string]$TargetDir = "$env:USERPROFILE\dsh-memory",
    [switch]$Yes
)

$ErrorActionPreference = "Stop"
function Has($cmd) {
    # 1) 真跑一下版本命令（防止把微软商店的 python 占位 stub 当成本地已装）
    try {
        $null = & $cmd --version 2>$null
        if ($LASTEXITCODE -eq 0) { return $true }
    } catch { }
    # 2) 再看 PATH 之外的常见官方安装位置（防止“装好了但当前终端 PATH 没刷新”的误报）
    switch ($cmd) {
        "git"    { return (Test-Path "C:\Program Files\Git\cmd\git.exe") -or (Test-Path "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe") }
        "python" { return (Test-Path "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe") -or (Test-Path "C:\Python312\python.exe") }
        default  { return $false }
    }
}

$gitOk    = Has git
$pyOk     = Has python
$wingetOk = Has winget
$repoOk   = Test-Path (Join-Path $TargetDir "AGENTS.md")

Write-Host "== DeepSeekHarness 记忆体引导 =="
Write-Host ("git     : " + $(if ($gitOk) { "已装" } else { "缺（需审批安装）" }))
Write-Host ("python  : " + $(if ($pyOk) { "已装" } else { "缺（需审批安装）" }))
Write-Host ("winget  : " + $(if ($wingetOk) { "可用（官方包管理器）" } else { "缺（将给官方下载链接，人类点一下）" }))
Write-Host ("目标仓库: " + $(if ($repoOk) { "已存在 -> $TargetDir" } else { "待克隆 -> $TargetDir" }))
Write-Host ""

$plan = @()
if (-not $gitOk)    { $plan += "安装 Git —— 官方源：winget id=Git.Git（git-scm.org 官方版）" }
if (-not $pyOk)     { $plan += "安装 Python 3.12 —— 官方源：winget id=Python.Python.3.12（python.org 官方版）" }
if (-not $repoOk)   { $plan += "克隆 https://github.com/adsorgcn/DeepSeekHarness -> $TargetDir" }
$plan += "切目录 $TargetDir 并跑 python tools\brain.py check 验收"

Write-Host "计划："
$plan | ForEach-Object { Write-Host ("  - " + $_) }
Write-Host ""

if (-not $Install) {
    Write-Host "（默认只出计划，不做任何改动。确认后：agent 逐项征得你同意，再以 -Install -Yes 执行。）"
    exit 0
}

function Approved($what) {
    if ($Yes) { return $true }
    $r = Read-Host ("  需要安装系统软件: " + $what + " [y/N]")
    return ($r -eq "y")
}

# 1) Git（官方源）
if (-not $gitOk) {
    if (-not (Approved "Git（git-scm.org 官方版）")) {
        Write-Host "跳过 Git（后续克隆仓库需要它）"
    } elseif ($wingetOk) {
        winget install --id Git.Git --source winget -e --silent --accept-source-agreements --accept-package-agreements
        Write-Host "Git 安装完成。注意：新装的 git 需要新开终端（或重启 DSH）才进 PATH。"
    } else {
        Write-Host "winget 不可用。请从官方下载并安装：https://git-scm.com/download/win"
        Write-Host "装好后重跑本脚本。"
        exit 1
    }
}

# 2) Python 3.12（官方源）
if (-not $pyOk) {
    if (-not (Approved "Python 3.12（python.org 官方版）")) {
        Write-Host "跳过 Python（brain.py check 需要它）"
    } elseif ($wingetOk) {
        winget install --id Python.Python.3.12 --source winget -e --silent --accept-source-agreements --accept-package-agreements
        Write-Host "Python 安装完成。注意：新装的 python 需要新开终端（或重启 DSH）才进 PATH。"
    } else {
        Write-Host "winget 不可用。请从官方下载并安装：https://www.python.org/downloads/windows/"
        Write-Host "装好后重跑本脚本。"
        exit 1
    }
}

# 3) 克隆仓库（无需审批）
if (-not $repoOk) {
    Write-Host "克隆仓库..."
    if (-not (Has git)) {
        Write-Host "git 仍不可用：请新开终端后重跑本脚本。"
        exit 1
    }
    git clone https://github.com/adsorgcn/DeepSeekHarness.git $TargetDir
}

# 4) 验收（无需审批）
Set-Location $TargetDir
if (Has python) {
    python -X utf8 tools\brain.py check
} elseif (Has py) {
    py -X utf8 tools\brain.py check
} else {
    Write-Host "Python 仍不可用：请新开终端后重跑本脚本。"
    exit 1
}

Write-Host ""
Write-Host "完成。在 DSH 里把 $TargetDir 选为工作区（或说一句话让 agent 切进去），记忆体即上线。"


