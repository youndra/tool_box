# Flowchart Image To Editable PPTX

Convert a flowchart image or architecture diagram into an editable PowerPoint file made from native PowerPoint shapes, text boxes, and connectors.

This repository is designed for cases where a screenshot, paper figure, or diagram image needs to become a `.pptx` that can be manually edited later.

## What This Project Does

- Rebuilds diagrams as editable PowerPoint objects
- Stores each result in a folder named after the source image
- Keeps the intermediate JSON spec for later adjustment
- Works well for flowcharts, module diagrams, and model-structure figures

## Current Workflow

This project currently uses a semi-automatic workflow:

1. Inspect the source image
2. Create a JSON layout spec
3. Generate the editable PPTX from the JSON spec

The JSON step is the editable bridge between image understanding and PowerPoint output.

## Project Structure

```text
.
├─ scripts/
│  ├─ build_flowchart_pptx.py
│  └─ generate_pptx.py
├─ CA/
│  ├─ CA.json
│  └─ CA.pptx
├─ EMA注意力/
│  ├─ EMA注意力.json
│  └─ EMA注意力.pptx
├─ yolov8模块细节图/
│  ├─ yolov8模块细节图.json
│  └─ yolov8模块细节图.pptx
├─ CA.png
├─ EMA注意力.jpg
├─ yolov8模块细节图.png
├─ README.md
├─ requirements.txt
└─ 操作流程.md
```

## Installation

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Step 1: Bootstrap a new image workspace

If you only have an image and want to start fast, run:

```powershell
python .\scripts\bootstrap_from_image.py .\examples\new-diagram.png
```

This creates:

```text
outputs/
└─ new-diagram/
   ├─ new-diagram.png
   └─ new-diagram.json
```

Then edit the JSON spec and generate the PPTX.

### Step 2: Generate the editable PPTX

Prepare a JSON spec first, then run:

```powershell
python .\scripts\generate_pptx.py `
  --image .\CA\CA.png `
  --spec .\CA\CA.json `
  --output-root .\outputs `
  --copy-image
```

This creates:

```text
outputs/
└─ CA/
   ├─ CA.png
   ├─ CA.json
   └─ CA.pptx
```

The output folder name is always the source image name without its extension.

## JSON Capabilities

The generator supports:

- Rounded rectangles and common flowchart shapes
- Free text labels
- Background panels
- Solid and dashed lines
- Straight connectors between blocks
- Table-like layouts built from regular rectangles

## Best Use Cases

- Research paper module diagrams
- Model architecture illustrations
- Process flowcharts
- Attention-module diagrams
- Diagrams that need later manual editing in PowerPoint

## Limitations

- The image-to-JSON step is not fully automatic yet
- Curved arrows are approximated with straight editable lines
- Very dense diagrams may need manual cleanup after export
- Pixel-perfect reproduction is not the goal; editability is

## Example Outputs

Current examples included in this repository:

- `CA`
- `EMA注意力`
- `yolov8模块细节图`

Each example folder contains the editable `.pptx` and the corresponding `.json`.

## Next Improvements

- Add image-to-JSON automation
- Add OCR-assisted text extraction
- Add support for elbow connectors
- Add template export styles for cleaner visual consistency
