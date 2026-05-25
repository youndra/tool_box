# PROMPT_TEMPLATE

这个文件用于解决一个很实际的问题：

如果用户本地没有 Codex 这类可识别图片并可操作仓库的 agent，也仍然可以借助网页上的 AI，把图片先转换成 JSON，再回到本项目里生成可编辑 PPTX。

## 两种使用模式

### 模式 A：有 agent

如果用户使用的是 Codex 这类 agent：

- agent 直接看图
- agent 按本项目规范输出 JSON
- agent 调用脚本生成 PPTX

### 模式 B：没有 agent，只有网页 AI

如果用户没有类似 Codex 的 agent，可以这样做：

1. 打开任意支持看图的网页 AI
2. 上传目标图片
3. 把本文件中的提示词发给它
4. 让它只输出 JSON
5. 把 JSON 保存为同名 `.json`
6. 回到本项目中运行脚本生成 PPTX

适合的网页 AI 包括但不限于：

- ChatGPT 网页版
- Claude 网页版
- Gemini 网页版
- Kimi
- 通义
- 豆包
- 其他支持图片输入的模型

## 网页 AI 通用提示词

把下面这段完整复制给网页 AI，并附上图片：

```text
你要把这张图片中的流程图、结构图或模块图，转换成一个 JSON 对象。

严格要求：
1. 只输出 JSON，不要输出解释，不要输出 Markdown 代码块。
2. 顶层字段必须固定包含：
   - title
   - theme
   - overlays
   - segments
   - nodes
   - edges
   - texts
3. 所有坐标和尺寸统一使用英寸。
4. 所有颜色统一使用 #RRGGBB。
5. 保持图中的主要结构、模块层级、连接方向和文本标签。
6. 可以适度简化细小装饰，但不能破坏主流程和主结构。
7. 所有 nodes 的 id 必须唯一。
8. 背景块、虚线框、灰色区域放到 overlays。
9. 主要流程框、模块框、算子框放到 nodes。
10. 与节点无关的尺寸标注、标题、公式说明放到 texts。
11. 无法直接挂靠节点的自由直线放到 segments。
12. 节点之间的连接关系放到 edges。

补充要求：
- 如果图中有表格，可以用多个 rect 节点模拟单元格。
- 如果图特别复杂，优先保留主结构、主连线和主文字。
- 不要求像素级复刻，但要求结构逻辑正确。
- theme 默认使用白底，字体默认使用 Microsoft YaHei 或 Arial。

请直接输出最终 JSON，不要输出任何多余内容。
```

## 更强约束版本

如果某些网页 AI 容易输出解释、漏字段或格式不稳定，可以使用下面这版：

```text
任务：读取图片中的结构图，并输出一个合法 JSON，用于后续生成可编辑 PowerPoint。

输出规则：
- 只输出一个 JSON 对象
- 不要输出任何解释
- 不要输出 ```json
- 不要省略顶层字段
- 即使数组为空，也必须保留

顶层结构固定为：
{
  "title": "",
  "theme": {},
  "overlays": [],
  "segments": [],
  "nodes": [],
  "edges": [],
  "texts": []
}

字段要求：
- nodes 中每个对象必须至少包含：id, shape, text, x, y, w, h
- edges 中每个对象必须至少包含：from, to
- texts 中每个对象必须至少包含：text, x, y
- 所有数字字段必须输出为数字
- 所有颜色必须输出为 #RRGGBB

建模顺序：
1. 先识别大区域
2. 再识别主要节点
3. 再识别连接关系
4. 最后补充文本标注和自由线段

输出目标：
- 结构正确
- JSON 可编辑
- 能直接用于后续 PPT 生成

现在只输出最终 JSON。
```

## 推荐附加材料

如果网页 AI 支持同时参考多个文件，建议一起提供：

- 当前图片
- `JSON_SCHEMA.md`
- 一个现有示例 JSON

这样能明显提升不同模型之间的输出一致性。

## 网页 AI 使用后的落地方式

当网页 AI 输出 JSON 后：

1. 把内容保存成同名 `.json`
2. 放到对应图片文件夹中，或者输出目录中
3. 执行本项目脚本生成 PPTX

示例：

```powershell
python .\scripts\generate_pptx.py `
  --image .\CA\CA.png `
  --spec .\CA\CA.json `
  --output-root .\outputs `
  --copy-image
```

## 结论

这个项目不是强绑定某一个 AI。

只要某个模型满足下面条件，就能接入这套流程：

- 能看图
- 能理解结构
- 能稳定输出 JSON

所以：

- 有 agent 时，直接 agent 处理更顺滑
- 没有 agent 时，网页 AI + 本提示词也能工作
