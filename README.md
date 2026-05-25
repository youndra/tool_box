# 图片转可编辑 PPTX

这个项目用于把流程图图片、结构图图片、论文模块图等内容，转换成可编辑的 PowerPoint 文件。

这里的“可编辑”指的是：

- 方框可改
- 文字可改
- 连线可改
- 区块可改
- 布局可继续调整

## 项目现状

当前流程分成两段：

1. `图片 -> JSON`
2. `JSON -> PPTX`

其中：

- `JSON -> PPTX` 已经由脚本自动完成
- `图片 -> JSON` 目前依赖 AI 辅助理解图片结构

所以这个项目支持两种使用方式：

1. 有 Codex 这类 agent
2. 没有 agent，只使用网页 AI

## 安装

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 用法一：有 agent

适合使用 Codex 这类可以看图、理解结构、并操作仓库的 agent。

流程如下：

1. 把图片放进项目目录
2. 让 agent 参考 `JSON_SCHEMA.md` 和示例文件理解输出格式
3. 让 agent 直接生成同名 `.json`
4. 运行脚本生成可编辑 PPTX

生成命令：

```powershell
python .\scripts\generate_pptx.py `
  --image .\CA\CA.png `
  --spec .\CA\CA.json `
  --output-root .\outputs `
  --copy-image
```

生成结果：

```text
outputs/
└─ CA/
   ├─ CA.png
   ├─ CA.json
   └─ CA.pptx
```

## 用法二：没有 agent，只有网页 AI

如果没有 Codex 这类 agent，也可以完成整套流程。

### 第 1 步：准备图片

例如图片路径是：

```text
CA/CA.png
```

### 第 2 步：把图片上传到网页 AI

把图片上传到任意支持看图的网页 AI，例如：

- ChatGPT
- Claude
- Gemini
- Kimi
- 通义
- 豆包

### 第 3 步：把提示词发给网页 AI

把 [PROMPT_TEMPLATE.md](C:\Users\86183\Desktop\Codex\流程图转变成可编辑\PROMPT_TEMPLATE.md) 里的提示词完整复制给网页 AI。

目标是让网页 AI 只输出 JSON。

### 第 4 步：保存网页 AI 返回的 JSON

网页 AI 输出 JSON 后，手动把结果保存成同名文件。

例如图片是 `CA.png`，那就保存为：

```text
CA/CA.json
```

或者也可以保存到你刚创建的输出骨架里：

```text
outputs/CA/CA.json
```

核心要求只有一个：

- `.json` 文件内容必须是合法 JSON
- 字段结构符合 `JSON_SCHEMA.md`

### 第 5 步：生成 PPTX

如果你把 JSON 保存在：

```text
CA/CA.json
```

就运行：

```powershell
python .\scripts\generate_pptx.py `
  --image .\CA\CA.png `
  --spec .\CA\CA.json `
  --output-root .\outputs `
  --copy-image
```

如果你把 JSON 保存在：

```text
outputs/CA/CA.json
```

就运行：

```powershell
python .\scripts\generate_pptx.py `
  --image .\CA\CA.png `
  --spec .\outputs\CA\CA.json `
  --output-root .\outputs `
  --copy-image
```

### 第 6 步：检查结果

脚本执行后会生成：

```text
outputs/
└─ CA/
   ├─ CA.png
   ├─ CA.json
   └─ CA.pptx
```

然后直接打开 `CA.pptx` 检查：

- 方框是否能单独选中
- 文字是否能直接编辑
- 连线是否合理
- 标注是否有遮挡

## 骨架命令

如果你想先自动创建输出文件夹和空白 JSON，可以先运行：

```powershell
python .\scripts\bootstrap_from_image.py .\CA\CA.png --output-root .\outputs
```

这会创建：

```text
outputs/
└─ CA/
   ├─ CA.png
   └─ CA.json
```

## 关键文件

- `scripts/build_flowchart_pptx.py`
  负责把 JSON 转换成可编辑 PPTX

- `scripts/generate_pptx.py`
  负责按图片名输出到对应文件夹

- `scripts/bootstrap_from_image.py`
  负责创建输出骨架

- `JSON_SCHEMA.md`
  说明 JSON 字段结构

- `PROMPT_TEMPLATE.md`
  提供给网页 AI 的提示词

- `操作流程.md`
  提供更细的实际操作步骤
