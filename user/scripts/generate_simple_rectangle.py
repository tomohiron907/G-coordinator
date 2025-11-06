#!/usr/bin/env python3
"""
Generate the tutorial Simple Rectangle path, export deterministic G-code, and
emit reproducibility metadata. The implementation follows:
https://gcoordinator.readthedocs.io/ja/latest/tutorials/tutorial_1.html
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from gcoordinator import gcode_generator, path_generator, settings


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "user" / "configs" / "printer" / "basic_cartesian.json"
DEFAULT_PRESET = REPO_ROOT / "user" / "presets" / "simple_rectangle.json"
DEFAULT_START_GCODE = REPO_ROOT / "user" / "configs" / "printer" / "start_basic.gcode"
DEFAULT_END_GCODE = REPO_ROOT / "user" / "configs" / "printer" / "end_basic.gcode"
DEFAULT_GCODE_OUT = REPO_ROOT / "user" / "artifacts" / "simple_rectangle.gcode"
DEFAULT_META_OUT = REPO_ROOT / "user" / "artifacts" / "simple_rectangle.meta.json"
TUTORIAL_URL = "https://gcoordinator.readthedocs.io/ja/latest/tutorials/tutorial_1.html"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the tutorial Simple Rectangle path and export G-code deterministically."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Printer configuration JSON.")
    parser.add_argument("--preset", type=Path, default=DEFAULT_PRESET, help="Geometry preset JSON.")
    parser.add_argument("--start-gcode", type=Path, default=DEFAULT_START_GCODE, help="Start G-code snippet.")
    parser.add_argument("--end-gcode", type=Path, default=DEFAULT_END_GCODE, help="End G-code snippet.")
    parser.add_argument("--gcode-out", type=Path, default=DEFAULT_GCODE_OUT, help="Output G-code path.")
    parser.add_argument("--meta-out", type=Path, default=DEFAULT_META_OUT, help="Metadata JSON path.")
    return parser.parse_args()


def load_preset(preset_path: Path) -> Dict[str, Any]:
    with preset_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def build_path(points: np.ndarray) -> path_generator.Path:
    x_coords, y_coords, z_coords = points.T
    return path_generator.Path(x_coords, y_coords, z_coords)


def compute_stats(points: np.ndarray) -> Dict[str, Any]:
    deltas = np.diff(points, axis=0)
    segment_lengths = np.linalg.norm(deltas, axis=1)
    bbox_min = points.min(axis=0)
    bbox_max = points.max(axis=0)
    return {
        "num_points": int(points.shape[0]),
        "num_segments": int(segment_lengths.shape[0]),
        "total_path_length_mm": round(float(segment_lengths.sum()), 6),
        "bounding_box_min": [round(float(v), 6) for v in bbox_min.tolist()],
        "bounding_box_max": [round(float(v), 6) for v in bbox_max.tolist()],
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def sha256_file(file_path: Path) -> str:
    digest = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_meta(meta_path: Path, payload: Dict[str, Any]) -> None:
    ensure_parent(meta_path)
    with meta_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")


def run(
    config_path: Path,
    preset_path: Path,
    start_gcode: Path,
    end_gcode: Path,
    gcode_out: Path,
    meta_out: Path,
) -> Dict[str, Any]:
    settings.load_settings(str(config_path))

    preset_payload = load_preset(preset_path)
    points = np.array(preset_payload["points"], dtype=float)
    rectangle_path = build_path(points)
    full_object: List[path_generator.Path] = [rectangle_path]

    exporter = gcode_generator.GCode(full_object)
    exporter.start_gcode(str(start_gcode))
    exporter.end_gcode(str(end_gcode))

    ensure_parent(gcode_out)
    exporter.save(str(gcode_out))

    stats = compute_stats(points)
    gcode_hash = sha256_file(gcode_out)
    metadata: Dict[str, Any] = {
        "tutorial": TUTORIAL_URL,
        "preset": str(preset_path),
        "config": str(config_path),
        "start_gcode": str(start_gcode),
        "end_gcode": str(end_gcode),
        "gcode_out": str(gcode_out),
        "meta_out": str(meta_out),
        "gcode_sha256": gcode_hash,
        "path_stats": stats,
        "closed_loop": bool(preset_payload.get("closed", False)),
    }
    write_meta(meta_out, metadata)
    return metadata


def main() -> None:
    args = parse_args()
    meta = run(
        config_path=args.config,
        preset_path=args.preset,
        start_gcode=args.start_gcode,
        end_gcode=args.end_gcode,
        gcode_out=args.gcode_out,
        meta_out=args.meta_out,
    )
    print(json.dumps(meta, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
