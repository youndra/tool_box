# 图片流程图转可编辑 PPTX

这个项目用于把流程图图片、结构图图片、论文模块图等内容，重建为可编辑的 PowerPoint 文件。

导出的 `.pptx` 不是简单把图片贴进幻灯片，而是尽量使用 PowerPoint 原生对象来表达，包括：

- 形状
- 文本框
- 连线
- 背景区块
- 表格式布局

这样导出后的文件可以继续在 PowerPoint 中手动修改。

## 项目目标

这个项目的核心目标不是做“完全自动识图”，而是提供一套稳定的半自动流程：

1. 从图片中理解结构
2. 用 JSON 描述图中的对象和布局
3. 根据 JSON 生成可编辑的 PPTX

相比直接重新手工画图，这种方式更适合复用、调整和持续迭代。

## 适用场景

这个项目适合以下类型的图片：

- 业务流程图
- 网络结构图
- 注意力模块图
- 论文中的模型示意图
- 希望后续继续修改的 PPT 图示

## 当前能力

当前生成器支持：

- 常见矩形和流程图形状
- 独立文本标注
- 背景色块
- 虚线边框
- 直线连接
- 通过普通矩形模拟表格布局

## 面向不同 AI 模型的说明

如果别人 `git clone` 这个项目，但使用的不是 GPT，而是其他支持看图的 AI，也仍然可以使用这套流程。

为了尽量减少不同模型之间的输出差异，仓库中补充了这几份说明：

- [JSON_SCHEMA.md](C:\Users\86183\Desktop\Codex\流程图转变成可编辑\JSON_SCHEMA.md)
- [PROMPT_TEMPLATE.md](C:\Users\86183\Desktop\Codex\流程图转变成可编辑\PROMPT_TEMPLATE.md)
- [AI使用说明.md](C:\Users\86183\Desktop\Codex\流程图转变成可编辑\AI使用说明.md)

建议任何模型在“图片 -> JSON”时，都参考这三份文件。

如果有 Codex 这类 agent，可以直接让 agent 看图并产出 JSON。

如果没有 agent，也可以直接把图片上传到网页 AI，再把 [PROMPT_TEMPLATE.md](C:\Users\86183\Desktop\Codex\流程图转变成可编辑\PROMPT_TEMPLATE.md) 里的提示词复制进去，让网页 AI 输出 JSON。

## 项目结构

```text
.
├─ scripts/
│  ├─ bootstrap_from_image.py
│  ├─ build_flowchart_pptx.py
│  └─ generate_pptx.py
├─ CA/
│  ├─ CA.png
│  ├─ CA.json
│  └─ CA.pptx
├─ EMA注意力/
│  ├─ EMA注意力.jpg
│  ├─ EMA注意力.json
│  └─ EMA注意力.pptx
├─ yolov8模块细节图/
│  ├─ yolov8模块细节图.png
│  ├─ yolov8模块细节图.json
│  └─ yolov8模块细节图.pptx
├─ README.md
├─ requirements.txt
├─ LICENSE
└─ 操作流程.md
```

## 安装方式

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 使用方式

### 1. 只给图片，先创建输出骨架

如果你手上只有图片，先运行：

```powershell
python .\scripts\bootstrap_from_image.py .\CA\CA.png --output-root .\outputs
```

这会自动创建：

```text
outputs/
└─ CA/
   ├─ CA.png
   └─ CA.json
```

其中：

- 文件夹名使用图片名
- 图片会复制进去
- 同时生成一个同名的 JSON 骨架文件

### 2. 编辑 JSON 规格

JSON 用来描述 PPT 里的元素，例如：

- `theme`：整体主题与尺寸
- `overlays`：背景块、装饰块
- `segments`：自由线段
- `nodes`：流程框、模块框
- `edges`：节点之间的连线
- `texts`：额外文字说明

### 3. 生成可编辑 PPTX

编辑好 JSON 后运行：

```powershell
python .\scripts\generate_pptx.py `
  --image .\CA\CA.png `
  --spec .\CA\CA.json `
  --output-root .\outputs `
  --copy-image
```

这会生成：

```text
outputs/
└─ CA/
   ├─ CA.png
   ├─ CA.json
   └─ CA.pptx
```

## 输出规则

后续统一遵循下面的输出规则：

- 每张图片对应一个同名文件夹
- 文件夹内保存同名 `.json`
- 文件夹内保存同名 `.pptx`
- 如果需要，也可以把原图一起复制进去

例如：

```text
outputs/
└─ yolov8模块细节图/
   ├─ yolov8模块细节图.png
   ├─ yolov8模块细节图.json
   └─ yolov8模块细节图.pptx
```

## 已包含示例

仓库中目前包含 3 个实际示例：

- `CA`
- `EMA注意力`
- `yolov8模块细节图`

每个示例目录都包含：

- 原图
- JSON 规格
- 可编辑 PPTX

## 当前限制

目前仍然存在这些限制：

- 图片到 JSON 这一步还不是全自动
- 弯折线和复杂箭头还原有限
- 特别密集的图仍然可能需要手工微调
- 当前优先目标是“可编辑”，不是“逐像素复刻”

## 后续可扩展方向

后续可以继续扩展：

- 自动识别图片中的框、箭头和文本
- 引入 OCR 提高文本提取效率
- 支持折线连接
- 支持更丰富的图形模板
- 逐步发展为更自动化的图转 PPT 工具
