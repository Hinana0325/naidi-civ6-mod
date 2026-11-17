# Civ6 奶帝领袖模组（奶家）

把网络梗「奶蛙称帝」做成《文明 VI》里一个可玩的文明：领袖只有一个 **奶帝**，奶家其他成员
（奶狗 / 奶蛋 / 奶鸡）作为特色兵种。

## 内容

- 文明：奶家（`CIVILIZATION_NAIWA`），领袖：奶帝（`LEADER_NAIDI`）
- 领袖特性「奶魂觉醒」：所有城市 +1 生产力
- 文明特性「万物皆可奶」：所有城市 +1 食物
- 特色兵种：奶狗（侦察系）、奶蛋（近战系）、奶鸡（建造者系）
- 首都「奶蛙大学」，城市名池 8 个奶家成员
- 领袖立绘、加载页背景 / 前景、外交静态图、文明与领袖图标

## 目录

```
NaiwaCiv/                 ModBuddy 工程（源文件）
  Data/                   领袖、文明、兵种、文本键值定义
  Text/                   本地化文本
  Icons/                  文明 / 领袖图标（10 档、7 档 atlas）
  Textures/               .dds + .tex（UI 贴图与贴图元数据）
  XLPs/                   UILeaders / LeaderFallbacks 打包定义
  ArtDefs/                FallbackLeaders.artdef
  Art/                    美术源图（4K 母版、抠像立绘、裁切稿）
  NaiwaCiv.Art.xml        美术 consumer / library 声明
build.ps1                 MSBuild + Civ6 打包器一键构建
bmp_to_dds.py             BMP → 未压缩 32bpp DDS
png_to_dds.py             PNG → 带 alpha 的未压缩 DDS
fakeassets/               最小 pantry 占位（未安装 27GB 官方素材包时用）
```

## 构建

前置：Steam 版《文明 VI》+ Civilization VI SDK（ModBuddy）。必须先关闭游戏，否则产物被占用。

```powershell
.\build.ps1
```

脚本内部调用 `MSBuild.exe NaiwaCiv\NaiwaCiv.civ6proj /t:ReBuild`，并传入四个路径参数：

| 参数 | 指向 |
| --- | --- |
| `Civ6_UserPath` | `%USERPROFILE%\Documents\My Games\Sid Meier's Civilization VI` |
| `MSBuildLocalExtensionPath` | `<游戏目录>\Sid Meier's Civilization VI SDK\ModBuddy\Extensions\Application\` |
| `Civ6_CookerPath` | `<SDK>\AssetModTools\Cooker\Civ6AssetCooker_FinalRelease.exe` |
| `Civ6_AssetsPath` | 仓库内 `fakeassets`（没有官方 Development Assets 时的占位 pantry） |

构建产物自动落到 `Documents\My Games\Sid Meier's Civilization VI\Mods\NaiwaCiv`，
进游戏「额外内容」里启用即可。

## 美术管线说明

游戏 UI 贴图是**按贴图原始像素居中显示、不缩放**的（`LoadScreen.xml` 里 `StretchMode="Auto"`），
所以：

- 加载页背景必须 ≥ 屏幕分辨率（本工程按 2560×1440 出图）；
- 领袖立绘是**带透明通道的抠像**，落在背景右侧，不是同图裁切；
- DDS 通道顺序在 BMP 与 PNG 两条路径上相反：BMP 走 `bmp_to_dds.py`（交换 R/B），
  PNG 走 `png_to_dds.py`（保持 RGBA 直写）。写反了画面会整体发蓝，这是踩过的坑。

## 素材来源与声明

- 梗依据：`奶蛙称帝` 形象母题（抖音《奶帝登基》）、`奶魂大陆` 修仙设定（「奶魂觉醒」→ +1 生产力 的出处）。
- 领袖立绘母版来自 Wallpaper Engine 工坊壁纸《奶龙皇帝》（id 3808246035）的作者画面，
  抠像由 MediaKit 背景移除完成；本仓库仅作个人学习/自用，不作商用。
- 「奶龙」为第三方 IP，官方对恶搞二创态度不友好；若公开分发请注意版权与下架风险。
