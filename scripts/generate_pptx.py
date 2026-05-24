#!/usr/bin/env python
"""Generate an editable PPTX from a JSON spec and store outputs by image name."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_flowchart_pptx import build_presentation
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an editable PPTX from a JSON spec into an image-named output folder."
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Source image path. Only used to determine the output folder name.",
    )
    parser.add_argument(
        "--spec",
        required=True,
        help="JSON spec path.",
    )
    parser.add_argument(
        "--output-root",
        default="outputs",
        help="Root directory for generated folders. Default: outputs",
    )
    parser.add_argument(
        "--copy-image",
        action="store_true",
        help="Copy the source image into the output folder.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = Path(args.image).resolve()
    spec_path = Path(args.spec).resolve()
    output_root = Path(args.output_root).resolve()

    folder_name = image_path.stem
    output_dir = output_root / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_output = output_dir / f"{folder_name}.json"
    pptx_output = output_dir / f"{folder_name}.pptx"

    shutil.copy2(spec_path, spec_output)
    if args.copy_image:
        shutil.copy2(image_path, output_dir / image_path.name)

    with spec_path.open("r", encoding="utf-8") as fh:
        spec = json.load(fh)

    build_presentation(spec, pptx_output)
    print(output_dir)


if __name__ == "__main__":
    main()
