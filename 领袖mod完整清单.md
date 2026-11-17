# 一个「完整」的文明 6 领袖模组，到底要有哪些东西

调查时间：2026-11-17　｜　依据：本机游戏文件（schema + 官方 DLC 数据）+ 社区领袖美术教程

---

## 一句话结论

Civ6 的「一个领袖」不是一条数据，是**五层东西叠起来**：

```
数据层（XML）  →  图标层（ICON_LEADER_*）  →  2D 图像层（立绘/加载页/外交静态图）
                                                  →  3D 场景层（模型+动画，即「雕像」）
                                                  →  音频层（开场语音/台词）
```

缺哪一层，游戏就退化成什么样，下面一层一层拆。

---

## 第一层：数据层（XML，缺了会崩或功能缺失）

| 表 | 作用 | 我们有没有 | 缺了会怎样 |
| --- | --- | --- | --- |
| `Types` | 注册 KIND_LEADER / KIND_TRAIT | ✅ | 全部失效 |
| `Leaders` | 领袖本体：LeaderType / Name / **SceneLayers** / Sex | ⚠️ 有，但 **SceneLayers 没写 4** | 0 层场景 → 外交界面空 |
| `LeaderTraits` | 把特性挂到领袖上 | ✅ | 特性不生效 |
| `CivilizationLeaders` | 把领袖挂到文明上，指定首都 | ✅ | 选不到这个领袖 |
| `Traits` / `TraitModifiers` / `Modifiers` / `ModifierArguments` | 领袖特性本体 | ✅ | 没特性 |
| `Agendas` / `AgendaTraits` / `HistoricalAgendas` | AI 性格与外交态度 | ❌ **缺** | AI 没有自己的脾气，只会通用行为 |
| `FavoredReligions` | AI 偏好宗教 | ❌ 缺 | 小事，AI 随便信 |
| `LeaderQuotes`（Quote + QuoteAudio） | 见面/胜利的领袖引言 | ❌ 缺 | 没有台词，界面少一块 |
| `LeaderInfo`（Header / Caption） | 选领袖界面的头衔小字 | ❌ 缺 | 列表里没有副标题 |
| `LoadingInfo`（前景图/背景图/leader 文本/开场语音） | **开局加载页** | ❌ **缺** | 就是你刚看到的——加载时没有奶帝的图 |
| `CivilopediaPageChapterParagraphs` | 百科词条正文 | ✅（文字有，段落索引要核对） | 百科空白 |
| `PlayerItems` | 选文明界面列出特色兵种 | ✅ | 看不出独特单位 |
| `CityNames` | 城市名池 | ✅ 8 个 | 只能用通用名 |

### 官方原样（可以直接照抄的两个文件）

- 表结构：`...\Base\Assets\Gameplay\Data\Schema\01_GameplaySchema.sql`
- 加载页官方写法：`...\DLC\Expansion1\Data\Expansion1_LoadingInfo.xml`

```xml
<LoadingInfo>
  <Row LeaderType="LEADER_CHANDRAGUPTA"
       ForegroundImage="LEADER_CHANDRAGUPTA_NEUTRAL"
       BackgroundImage="LEADER_CHANDRAGUPTA_BACKGROUND"/>
</LoadingInfo>
```

- 完整的「第二领袖」样例（含加载页、引言、百科、AI）：`...\DLC\CatherineDeMedici\Data\CatherineDeMedici_Leaders.xml`

```xml
<Leaders>
  <Row LeaderType="LEADER_CATHERINE_DE_MEDICI_ALT"
       Name="LOC_LEADER_..."
       InheritFrom="LEADER_DEFAULT" SceneLayers="4"/>
</Leaders>
<LeaderQuotes>
  <Row LeaderType="LEADER_..." Quote="LOC_PEDIA_..."
       QuoteAudio="Play_FRAN_CA_VICTORY_CULTURE_B"/>
</LeaderQuotes>
<LoadingInfo>
  <Row LeaderType="LEADER_..."
       ForegroundImage="LEADER_CATHERINE_DE_MEDICI_ALT_NEUTRAL"
       BackgroundImage="LEADER_CATHERINE_DE_MEDICI_ALT_BACKGROUND"
       LeaderText="LOC_LOADING_INFO_LEADER_CATHERINE_DE_MEDICI"
       DawnOfManLeaderId="LEADER_CATHERINE_DE_MEDICI"/>
</LoadingInfo>
```

注意 `SceneLayers="4"`——官方每个有脸有动作的领袖都是 4 层。我们的是 0。

---

## 第二层：图标（已经有，17 张 dds）

- 领袖图标 7 档：32 / 45 / 50 / 55 / 64 / 80 / 256
- 这些是**小图标**，只用在列表、旗帜、UI 角标上，不负责「脸」。

---

## 第三层：2D 图像（决定「有没有脸」的一层）

这是你最直观感受到的缺口，也是**最值得做**的一层。完整的话要三张：

| 用途 | 建议尺寸 | 文件名习惯 | 说明 |
| --- | --- | --- | --- |
| 选文明界面立绘 | 768 × 1024（dds） | `PORTRAIT_<领袖>.dds` | 选文明时右边那张大图，构图要偏左 |
| 加载页前景 | 约 1024 高（dds） | `LEADER_<领袖>_NEUTRAL.dds` | 就是你刚吐槽「加载没图」的那张 |
| 加载页背景 | 1280 × 1000（dds） | `LEADER_<领袖>_BACKGROUND.dds` | 前景后面那层氛围图 |
| 外交界面静态图（备用） | 1600 × 900（dds） | `FALLBACK_NEUTRAL_<领袖>.dds` | 关掉 3D 领袖时用的那张 |

**关键点**：这四张原始 dds **不能直接丢进 mod** 就完事——Civ6 走的是「美术资源必须打包」的路子：

1. 在 ModBuddy → Tools → **Asset Editor** 里新建 Texture
   - 普通界面图：类型选 `UserInterface`
   - 外交静态图：类型选 `Leader_Fallback`
2. Asset Editor 会生成配套的 `.tex` 与 `.artdef`（类 `FallbackLeaders` / `Leaders`）
3. 在 ModBuddy 里把这些文件设为 **Import to VFS = True**（注意：**不要**加 UpdateDatabase 条目）
4. 然后 `LoadingInfo` 里的 `ForegroundImage` / `BackgroundImage` 填 art 名（如 `LEADER_NAIDI_NEUTRAL`），不是文件路径

> 注意：没有 AssetEditor 打包这一步，光把 dds 放进 `Icons/` 并改 `LoadingInfo`，游戏找不到 art 名，加载页依然是空的。

---

## 第四层：3D 场景（你说的「奶帝雕像」）

这是「真·完整」的门槛：

- `Leaders.SceneLayers = 4`
- 需要一个 ArtDef 类 `Leaders` 的 `.ast` 资产（模型 + 材质 + 动画，cook 成 `.fgx` / `.tsr`）
- 工具链：**Development Assets**（约 27 GB 下载、解压 38.9 GB）+ AssetEditor + Blender 绑骨
- 社区现状：**绝大多数领袖 mod 不做 3D**，直接做 2D 静态立绘（`FALLBACK_NEUTRAL`）。做了 3D 的通常是「拿现成领袖模型换皮」，因为从零建模+绑骨+动画的成本以天计。

结论：雕像可以做，但要单开一个工期，而且必须在这台 Windows 上装 Development Assets。

---

## 第五层：音频

| 项 | 字段 | 缺了会怎样 |
| --- | --- | --- |
| 开场（Dawn of Man）语音 | `LoadingInfo.PlayDawnOfManAudio` / `DawnOfManLeaderId` | 加载页没有配音，无伤大雅 |
| 领袖引言配音 | `LeaderQuotes.QuoteAudio` | 静默，可空 |

奶帝这里其实有现成素材——「齁齁齁齁」的笑声，但要转成游戏认的音频格式，属于可选项。

---

## 我们现在的差距（对照表）

| 项 | 状态 |
| --- | --- |
| 数据行（领袖/特性/文明/城市/兵种/图标注册） | ✅ 已进游戏库验证 |
| 图标 7 档 + 文明 10 档 | ✅ |
| `SceneLayers=4` | ❌ 缺 |
| 选文明界面立绘 768×1024 | ❌ 缺 |
| 加载页前景/背景 | ❌ 缺（就是你看到的空加载页） |
| 外交界面静态图 | ❌ 缺（进外交大概率灰屏） |
| 3D 雕像场景 | ❌ 缺（也不会自己出现） |
| `LoadingInfo` 数据行 | ❌ 缺 |
| `LeaderQuotes` / `LeaderInfo` | ❌ 缺 |
| `Agendas` / `FavoredReligions`（AI 性格） | ❌ 缺 |

---

## 三条路线，选一条

### A. 最小可用（几十行 XML，不碰美术）
补 `LeaderInfo`、`LeaderQuotes`、`Agendas`、`FavoredReligions`。
**结果**：功能和 AI 完整，但**依然没有脸**，加载页空、外交灰屏。
→ 只适合自己玩、不在乎观感。

### B. 2D 立绘（推荐，性价比最高）
我做图 → 你（或我用命令行）在 AssetEditor 里打包 → 补 `LoadingInfo` + `SceneLayers=4`。
产出四张图：选领袖立绘、加载页前景、加载页背景、外交静态图。
**结果**：选文明有奶帝、开局加载页有奶帝、外交界面有奶帝立绘（不是 3D，是高清静态）。
成本：我这边出图 1 小时；打包需要在这台 Windows 上操作一次 AssetEditor。

### C. 3D 雕像（完整但重）
在 B 的基础上，再做 3D 模型 + 材质 + 待机动画 + cook。
成本：先装 Development Assets（27 GB / 38.9 GB），再建模绑骨，以天计。
**不建议现在做**，除非你确定要把它当成长期项目。

---

## 下一步（如果走 B）

1. 我按上面四张图的尺寸出图（沿用你现在那张奶帝的构图：冕旒 + 龙袍 + 玉玺）
2. 转 4 张 dds
3. 在这台机器上打开 AssetEditor 打包成 tex/artdef
4. 补 `NaiwaCiv_Leaders.xml` 的 `SceneLayers="4"` 与新的 `LoadingInfo` XML
5. 重新构建 → 进游戏验证加载页与外交界面

---

## 参考来源

- 本机 `01_GameplaySchema.sql`（Leaders / LoadingInfo / LeaderQuotes / LeaderInfo 字段）
- 本机 `DLC\Expansion1\Data\Expansion1_LoadingInfo.xml`（加载页图像名规则）
- 本机 `DLC\CatherineDeMedici\Data\CatherineDeMedici_Leaders.xml`（完整第二领袖范例）
- CivFanatics《Example mods that only change leader art》（ArtDef 类 FallbackLeaders / Leaders 的替换原理）
- CivFanatics《Step by step tutorial for leader art》（Asset Editor 的 Texture 类型与 Leader_Fallback）
- civ6wiki《MOD/作成方法/新文明・指导者/ローディング画面・リザルト》（三张 tex 的尺寸与 .tex 字段）
