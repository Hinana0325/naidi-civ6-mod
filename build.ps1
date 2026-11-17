# 奶家（奶帝）模组构建脚本
# 用法：在 PowerShell 里执行 .\build.ps1
# 说明：没有安装 27GB 的 Development Assets，所以用一个最小 pantry 占位（fakeassets），
#       我们的贴图不依赖官方素材，打包器在无基础 pantry 模式下也能正常 cook。

$proj = Join-Path $PSScriptRoot "NaiwaCiv\NaiwaCiv.civ6proj"
$msb  = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
$sdk  = "C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization VI SDK"
$fake = Join-Path $PSScriptRoot "fakeassets"
$log  = Join-Path $PSScriptRoot "build_art.log"

& $msb $proj /t:ReBuild /nologo /v:m `
  "/p:Civ6_UserPath=C:\Users\jq200\Documents\My Games\Sid Meier's Civilization VI" `
  "/p:MSBuildLocalExtensionPath=$sdk\ModBuddy\Extensions\Application\" `
  "/p:Civ6_CookerPath=$sdk\AssetModTools\Cooker\Civ6AssetCooker_FinalRelease.exe" `
  "/p:Civ6_AssetsPath=$fake" *> $log

"退出码: $LASTEXITCODE"
Get-Content -LiteralPath $log -Tail 6
