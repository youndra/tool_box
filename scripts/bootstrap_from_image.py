#!/usr/bin/env python
"""Create a per-image workspace folder with a starter JSON spec."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


STARTER_SPEC = {
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
        "terminator_fill": "#FFFFFF",
    },
    "overlays": [],
    "segments": [],
    "nodes": [],
    "edges": [],
    "texts": [],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an image-named output folder and starter JSON spec."
    )
    parser.add_argument(
        "image",
        help="Path to the source image.",
    )
    parser.add_argument(
        "--output-root",
        default="outputs",
        help="Root folder for generated workspaces. Default: outputs",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing copied image and JSON skeleton if they already exist.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = Path(args.image).resolve()
    output_root = Path(args.output_root).resolve()

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    folder_name = image_path.stem
    output_dir = output_root / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    image_target = output_dir / image_path.name
    spec_target = output_dir / f"{folder_name}.json"

    if image_target.exists() and not args.force:
        pass
    else:
        shutil.copy2(image_path, image_target)

    if spec_target.exists() and not args.force:
        pass
    else:
        with spec_target.open("w", encoding="utf-8") as fh:
            json.dump(STARTER_SPEC, fh, ensure_ascii=False, indent=2)

    print(output_dir)


if __name__ == "__main__":
    main()
