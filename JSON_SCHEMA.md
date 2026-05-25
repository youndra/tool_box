# JSON_SCHEMA

这个文件说明本项目使用的 JSON 中间格式。

目标是让不同的 AI 模型在“看图 -> 输出 JSON”这一步时，尽量产出一致、可复用的结构。

## 总体原则

- 坐标单位统一使用英寸
- 原点默认在幻灯片左上角
- `x` 表示左边距
- `y` 表示上边距
- `w` 表示宽度
- `h` 表示高度
- 所有颜色使用 `#RRGGBB`

## 顶层结构

```json
{
  "title": "",
  "theme": {},
  "overlays": [],
  "segments": [],
  "nodes": [],
  "edges": [],
  "texts": []
}
```

## 1. title

类型：

```json
"title": "可选标题"
```

说明：

- 可为空字符串
- 如果希望在页面顶部显示标题，可以填写

## 2. theme

类型示例：

```json
"theme": {
  "slide_width": 13.333,
  "slide_height": 7.5,
  "background_color": "#FFFFFF",
  "font_name": "Microsoft YaHei",
  "font_color": "#111111",
  "line_color": "#333333",
  "line_width": 1.0,
  "box_fill": "#FFFFFF",
  "box_line": "#333333",
  "decision_fill": "#FFFFFF",
  "terminator_fill": "#FFFFFF"
}
```

说明：

- `slide_width` 和 `slide_height` 控制页面大小
- `font_name` 是默认字体
- 其余字段是默认样式，可被局部覆盖

## 3. overlays

用途：

- 背景区块
- 虚线框
- 灰色区域
- 装饰性矩形或圆形

示例：

```json
{
  "shape": "rect",
  "x": 1.0,
  "y": 1.0,
  "w": 4.0,
  "h": 2.0,
  "fill_color": "#EEEEEE",
  "line_color": "#666666",
  "line_width": 0.8,
  "line_dash": "dash"
}
```

支持字段：

- `shape`：`rect`、`oval`
- `x`、`y`、`w`、`h`
- `fill_color`
- `line_color`
- `line_width`
- `line_dash`
- `text`
- `font_size`
- `font_color`
- `bold`

## 4. segments

用途：

- 自由直线
- 辅助线
- 不依附节点的连接线

示例：

```json
{
  "x1": 1.0,
  "y1": 1.0,
  "x2": 5.0,
  "y2": 1.0,
  "line_color": "#333333",
  "line_width": 0.8
}
```

支持字段：

- `x1`
- `y1`
- `x2`
- `y2`
- `line_color`
- `line_width`
- `dash`

## 5. nodes

用途：

- 主要流程框
- 模块框
- 算子框
- 表格中的单元格

示例：

```json
{
  "id": "conv_1",
  "shape": "process",
  "text": "Conv",
  "x": 2.0,
  "y": 1.5,
  "w": 2.2,
  "h": 0.8,
  "font_size": 16,
  "fill_color": "#7FDBFF"
}
```

必填字段：

- `id`
- `shape`
- `text`
- `x`
- `y`
- `w`
- `h`

常用可选字段：

- `font_size`
- `font_name`
- `font_color`
- `fill_color`
- `line_color`
- `line_width`
- `line_dash`
- `bold`

支持的 `shape`：

- `process`
- `start`
- `end`
- `terminator`
- `decision`
- `data`
- `document`
- `subprocess`
- `rect`
- `oval`

## 6. edges

用途：

- 节点之间的连接关系

示例：

```json
{
  "from": "conv_1",
  "to": "bn_1",
  "from_side": "bottom",
  "to_side": "top"
}
```

支持字段：

- `from`
- `to`
- `from_side`
- `to_side`
- `line_color`
- `line_width`
- `dash`
- `label`

其中锚点方向可选：

- `top`
- `right`
- `bottom`
- `left`

## 7. texts

用途：

- 尺寸标注
- 公式说明
- 模块标题
- 与节点无关的自由文字

示例：

```json
{
  "text": "C x H x W",
  "x": 3.0,
  "y": 1.2,
  "w": 1.5,
  "h": 0.2,
  "font_size": 14,
  "align": "left"
}
```

支持字段：

- `text`
- `x`
- `y`
- `w`
- `h`
- `font_size`
- `font_name`
- `font_color`
- `bold`
- `align`
- `word_wrap`

`align` 可选：

- `left`
- `center`
- `right`

## 推荐建模顺序

建议让 AI 按下面顺序产出 JSON：

1. 先确定整张图分成几个大区域
2. 先写 `theme`
3. 再写 `overlays`
4. 再写主要 `nodes`
5. 再写 `edges`
6. 最后补 `texts` 和 `segments`

## 建议约束

为了让不同模型输出更稳定，建议提示词里明确要求：

- 只输出 JSON
- 不要附加解释
- 所有节点 `id` 必须唯一
- 坐标尽量保留相对布局关系
- 优先保留结构逻辑，不强求像素级复刻

## 最小可用示例

```json
{
  "title": "",
  "theme": {
    "slide_width": 13.333,
    "slide_height": 7.5,
    "background_color": "#FFFFFF",
    "font_name": "Microsoft YaHei",
    "font_color": "#111111",
    "line_color": "#333333",
    "line_width": 1.0,
    "box_fill": "#FFFFFF",
    "box_line": "#333333",
    "decision_fill": "#FFFFFF",
    "terminator_fill": "#FFFFFF"
  },
  "overlays": [],
  "segments": [],
  "nodes": [
    {
      "id": "start",
      "shape": "start",
      "text": "Start",
      "x": 5.0,
      "y": 1.0,
      "w": 2.0,
      "h": 0.7
    },
    {
      "id": "step_1",
      "shape": "process",
      "text": "Process",
      "x": 5.0,
      "y": 2.2,
      "w": 2.0,
      "h": 0.8
    }
  ],
  "edges": [
    {
      "from": "start",
      "to": "step_1",
      "from_side": "bottom",
      "to_side": "top"
    }
  ],
  "texts": []
}
```
