# bootstrap.ps1 — DeepSeekHarness 记忆体一键引导（Windows）
#
# 原则：全部软件只从官方源安装；每步要不要人审批由 DSH 的审批模式决定——
#   · 不需要审批的（检测、克隆、切目录、验收）→ 自动跑
#   · 需要审批的（装 Git / Python 等系统软件）→ agent 先问用户，同意后执行
# 国内网络：GitHub 不可达时自动切换产品仓库到国内镜像
#   https://gitee.com/monetize/DeepSeekHarness（镜像与 GitHub 同源，由 owner 维护）
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1                              # 只检测并打印计划（默认，零改动）
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1 -Install -Yes                # 按计划执行（用户已审批后）
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1 -Install -TargetDir "D:\mem" -Yes
#   powershell -ExecutionPolicy Bypass -File bootstrap.ps1 -Install -Yes -Source gitee  # 强制走国内镜像
#   -Install -Yes 只在 DSH 已逐项征得用户同意后使用，脚本本身不替用户点头

param(
    [switch]$Install,
    [string]$TargetDir = "$env:USERPROFILE\dsh-memory",
    [switch]$Yes,
    [ValidateSet("auto", "github", "gitee")]
    [string]$Source = "auto"
)

$ErrorActionPreference = "Stop"

$GitHubUrl  = "https://github.com/adsorgcn/DeepSeekHarness.git"
$GiteeUrl   = "https://gitee.com/monetize/DeepSeekHarness.git"
$GitHubProbe = "https://github.com"

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

function Resolve-Cmd($cmd) {
    # 返回能真正执行该命令的绝对路径；找不到返回 $null（调用处失败报错，不再裸调）
    try {
        $null = & $cmd --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $found = Get-Command $cmd -ErrorAction SilentlyContinue
            if ($found) { return $found.Source }
        }
    } catch { }
    switch ($cmd) {
        "git" {
            foreach ($p in @("C:\Program Files\Git\cmd\git.exe", "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe")) {
                if (Test-Path $p) { return $p }
            }
        }
        "python" {
            foreach ($p in @("$env:LOCALAPPDATA\Programs\Python\Python312\python.exe", "C:\Python312\python.exe")) {
                if (Test-Path $p) { return $p }
            }
        }
    }
    return $null
}

function Test-DshInstalled($dir) {
    return (Test-Path (Join-Path $dir "AGENTS.md")) -and
           (Test-Path (Join-Path $dir "tools\brain.py")) -and
           (Test-Path (Join-Path $dir "CITATION.cff"))
}

function Test-GitHubReachable {
    if ($Source -eq "gitee")  { return $false }
    if ($Source -eq "github") { return $true }
    try {
        Invoke-WebRequest -UseBasicParsing -Uri $GitHubProbe -TimeoutSec 8 | Out-Null
        return $true
    } catch {
        return $false
    }
}

$gitOk    = Has git
$pyOk     = Has python
$wingetOk = Has winget

$productSource = "auto"
if ($Source -eq "gitee") { $productSource = "gitee" }
elseif ($Source -eq "github") { $productSource = "github" }
elseif (Test-GitHubReachable) { $productSource = "github" }
else { $productSource = "gitee" }
$cloneUrl = if ($productSource -eq "github") { $GitHubUrl } else { $GiteeUrl }

Write-Host "== DeepSeekHarness 记忆体引导 =="
Write-Host ("git     : " + $(if ($gitOk) { "已装" } else { "缺（需审批安装）" }))
Write-Host ("python  : " + $(if ($pyOk) { "已装" } else { "缺（需审批安装）" }))
Write-Host ("winget  : " + $(if ($wingetOk) { "可用（官方包管理器）" } else { "缺（将给官方下载链接，人类点一下）" }))
Write-Host ("目标仓库: " + $(if (Test-DshInstalled $TargetDir) { "已安装（完整） -> $TargetDir" } else { "待克隆 -> $TargetDir" }))
if ($Source -eq "auto") { Write-Host ("产品源  : 自动探测（GitHub 优先，不可达走国内镜像 gitee.com/monetize/DeepSeekHarness）——本轮: " + $productSource) }
elseif ($Source -eq "gitee") { Write-Host "产品源  : 国内镜像 gitee.com/monetize/DeepSeekHarness（强制）" }
else { Write-Host "产品源  : github.com/adsorgcn/DeepSeekHarness（强制）" }
Write-Host ""

$plan = @()
if (-not $gitOk)    { $plan += "安装 Git —— 官方源：winget id=Git.Git（git-scm.org 官方版）" }
if (-not $pyOk)     { $plan += "安装 Python 3.12 —— 官方源：winget id=Python.Python.3.12（python.org 官方版）" }
if (-not (Test-DshInstalled $TargetDir)) { $plan += "克隆 $cloneUrl -> $TargetDir" }
$plan += "切目录 $TargetDir 并跑 python tools\brain.py check 验收（失败即停）"
$plan += "安装记忆推送保护钩子（私人记忆不确认不得推送）"

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
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Git 安装失败（winget 退出码 $LASTEXITCODE）。请从官方下载并安装：https://git-scm.com/download/win ，装好后重跑本脚本。"
            exit 1
        }
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
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Python 安装失败（winget 退出码 $LASTEXITCODE）。请从官方下载并安装：https://www.python.org/downloads/windows/ ，装好后重跑本脚本。"
            exit 1
        }
        Write-Host "Python 安装完成。注意：新装的 python 需要新开终端（或重启 DSH）才进 PATH。"
    } else {
        Write-Host "winget 不可用。请从官方下载并安装：https://www.python.org/downloads/windows/"
        Write-Host "装好后重跑本脚本。"
        exit 1
    }
}

# 3) 克隆仓库（无需审批，但失败即停）
if (-not (Test-DshInstalled $TargetDir)) {
    if (Test-Path $TargetDir) {
        Write-Host "目标目录已存在但检测不到完整安装（缺 AGENTS.md / tools\brain.py / CITATION.cff）。为避免覆盖你已有的文件，已停止。请换一个 -TargetDir。"
        exit 1
    }
    Write-Host ("克隆仓库（" + $productSource + "）...")
    $git = Resolve-Cmd git
    if (-not $git) {
        Write-Host "git 仍不可用：请新开终端后重跑本脚本。"
        exit 1
    }
    & $git clone $cloneUrl $TargetDir
    if ($LASTEXITCODE -ne 0) {
        if (($productSource -eq "github") -and ($Source -eq "auto")) {
            Write-Host "GitHub 克隆失败，自动改用国内镜像重试..."
            if (Test-Path $TargetDir) { Remove-Item -Recurse -Force $TargetDir }
            $productSource = "gitee"
            $cloneUrl = $GiteeUrl
            & $git clone $cloneUrl $TargetDir
            if ($LASTEXITCODE -ne 0) {
                Write-Host "克隆失败（$cloneUrl）。已试过 GitHub 与 Gitee，请检查网络后重跑。"
                exit 1
            }
        } else {
            Write-Host "克隆失败（$cloneUrl）。请检查网络，或改用 -Source gitee 后重跑。"
            exit 1
        }
    }
    # 本机模式：关掉模板的推送地址，公开仓库在机制上永远不是推送目标
    & $git -C $TargetDir remote set-url --push origin DISABLED
    if ($LASTEXITCODE -ne 0) { Write-Host "设置本机模式失败，已停止。"; exit 1 }
    & $git -C $TargetDir config dsh.mode local
    if ($LASTEXITCODE -ne 0) { Write-Host "设置本机模式失败，已停止。"; exit 1 }
    & $git -C $TargetDir config dsh.source $productSource
    if ($LASTEXITCODE -ne 0) { Write-Host "记录产品源失败，已停止。"; exit 1 }
}

# 4) 验收（失败即停，不报完成）
Set-Location $TargetDir
$py = Resolve-Cmd python
if (-not $py) { $py = Resolve-Cmd py }
if (-not $py) {
    Write-Host "Python 仍不可用：请新开终端后重跑本脚本。"
    exit 1
}
& $py -X utf8 tools\brain.py check
if ($LASTEXITCODE -ne 0) {
    Write-Host "验收失败：brain.py check 未通过（退出码 $LASTEXITCODE），已停止（请按上面 ERROR/WARN 修复）。"
    exit 1
}

# 5) 记忆推送保护钩子
$hookSrc = Join-Path $TargetDir "tools\guard-pre-push.sh"
$hookDst = Join-Path $TargetDir ".git\hooks\pre-push"
if ((Test-Path $hookSrc) -and (Test-Path (Join-Path $TargetDir ".git"))) {
    Copy-Item $hookSrc $hookDst -Force
    Write-Host "已安装记忆推送保护钩子（推私人记忆前需显式确认 DSH_ALLOW_MEMORY_PUSH=1）。"
} else {
    Write-Host "（本次克隆的版本不含推送保护钩子；更新到新版本后重跑即可自动安装。）"
}

Write-Host ""
Write-Host ("完成。关掉这个窗口重开一个，把 " + $TargetDir + " 选为工作区，它第一句应该汇报上次做到哪；没看到就把屏幕上的内容贴给你的 DSH。")
