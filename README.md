# nikke-rapi — 拉毗·小红帽 AI 桌宠素材库

用 AI 图像生成 + 自动化质检流水线制作的《胜利女神：妮姬》拉毗（小红帽皮肤）Q 版桌宠精灵图完整工作库：包含两个版本的全部素材、生成提示词、帧序列与质检报告。

![全状态预览](outputs/rapi-v2/all-states.gif)

## 这是什么

一套二头身动漫贴纸风格的桌面宠物（pets plugin）精灵图集，从角色研究、动作设计、逐帧生成到成品校验全程留痕：

- **9 个动作状态**：待机、左右跑、打招呼、（v2：地面偷笑）、失败、等待、工作、审阅
- **16 方向视线机制**：躯干和双脚固定朝前，由颈部转动/俯仰带动鼻尖、眼睛与帽子，头部自然遮挡，不整体转身也不只移瞳孔
- **两个版本**：v1 偏冷静认真可靠；v2 按用户反馈修订为后期更活泼的性格——半眯眼坏笑、掩嘴偷笑、脸红、咬牙等表情，并**移除了跳跃**，替换为双脚基线不动的地面掩嘴偷笑（同一宠物 ID 更新，非新建）

## 版本对照

| | v1 `rapi-red-hood` | v2 `rapi-red-hood-v2` |
|---|---|---|
| 性格基调 | 冷静、认真、可靠 | 温暖、促狭、微得意，仍保持专业 |
| jumping 行 | 短跳 5 帧 | 地面掩嘴偷笑 5 帧（脚底基线校验 ≤3px 差） |
| 修订范围 | 全套制作 | idle / waving / failed / waiting / running / review 重制，跑动与视线沿用 v1 已验收像素 |
| 交付物 | `outputs/rapi/` | `outputs/rapi-v2/` |

## 状态与帧数

| 状态 | 帧数 | 说明 |
|---|---|---|
| idle | 6 | 待机呼吸眨眼 |
| running-right | 8 | 向右小跑 |
| running-left | 8 | 向左小跑 |
| waving | 4 | 扶帽敬礼式招呼 |
| jumping / grounded-chuckle | 5 | v1 短跳；v2 掩嘴偷笑 |
| failed | 8 | 失落低头后振作 |
| waiting | 6 | 摊手等候指示 |
| running | 6 | 专注检查既有装备 |
| review | 6 | 手托下巴审阅 |

## 图集规格

- 单元格 192 × 208 px，背景色键 `#00FFFF`
- 基础图集 `spritesheet.png`：1536 × 1872（8 列 × 9 行）
- 扩展图集 `spritesheet-extended.png`：1536 × 2288，附加第 9 / 10 行的 16 方向视线条带
- 成品同时输出 PNG 与 WebP，边缘做过 despill 消色键处理

## 目录结构

```
work/
  pet_pipeline.py            # 标准流水线编排（抽取帧→检查→拼图→预览）
  pet_revision_pipeline.py   # v2 修订编排（复用验收资产+重制表情+质检）
  Pets/
    rapi-red-hood/           # v1：decoded 原始条带 / frames 帧 / final 图集 / prompts / qa / references
    rapi-red-hood-v2/        # v2：同结构，含修订说明与复用记录
outputs/
  rapi/                      # v1 交付：全状态 GIF/MP4、单状态 GIF、质检报告
  rapi-v2/                   # v2 交付：含表情静帧、视线循环、no-jump 校验
```

`work/python-deps/`（含 ffmpeg 二进制）与两个交付 zip 未入库，见 `.gitignore`。

## 流水线说明

两个 Python 脚本是**编排器**，调用的是 Codex work-pets 技能自带的工具链（`extract_strip_frames → inspect_frames → compose_atlas → assemble_extended_atlas → despill_chroma_edges → validate_atlas → make_direction_blind_qa_sheet → validate_pet_quality` 等）。上游工具脚本位于技能安装目录，不包含在本仓库中——本仓库保存的是全部素材、提示词、QA 报告与编排逻辑，可完整复现工作过程与质检结论。

质检要点：

- **方向盲测**：QA 人员不看注册表直接判读视线方向，与 answer key 比对
- **连续性测量**：16 方向逐格量化视线衔接
- **no-jump 校验**：逐帧检测 v2 偷笑行脚底基线，最大差 ≤3px 才放行
- **validate_pet_quality** 汇总图集校验、色键报告、帧审、方向语义与连续性

## 来源与致谢

- 角色原型：拉毗·小红帽（NIKKE），性格与动作参考了活动剧情与社区整理的后期性格变化
- 图集结构参考：[zili-codex-pet](https://github.com/2846182283/zili-codex-pet)（仅参考紧凑轮廓与九状态十六视线布局）
- 动作与表情均为原创设计，未复现游戏内动作

## 版权声明

拉毗（Rapi: Red Hood）及相关角色版权归 **SHIFT UP** 所有。本仓库为 AI 生成的同人衍生素材（built-in imagegen 制作，非官方），仅供个人学习与非商业用途，请勿用于商业用途。如有侵权请联系删除。
