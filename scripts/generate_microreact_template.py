#!/usr/bin/env python3

import argparse
import json
from copy import deepcopy
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

TEMPLATE_FILES = {
    "csv-only": "csv-only.microreact.json",
    "csv-tree": "csv-tree.microreact.json",
    "csv-map": "csv-map.microreact.json",
    "csv-tree-map": "csv-tree-map.microreact.json",
    "csv-tree-map-timeline": "csv-tree-map-timeline.microreact.json",
}


def load_template(name: str) -> dict:
    template_path = SCRIPT_DIR / TEMPLATE_FILES[name]
    return json.loads(template_path.read_text())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill a Microreact starter template with project-specific values."
    )
    parser.add_argument("--template", choices=sorted(TEMPLATE_FILES), required=True)
    parser.add_argument("--name", required=True, help="Project name for meta.name")
    parser.add_argument("--data-url", required=True, help="CSV URL")
    parser.add_argument("--data-name", default="data.csv", help="CSV filename label")
    parser.add_argument("--tree-url", help="Tree URL for tree-enabled templates")
    parser.add_argument("--tree-name", default="tree.nwk", help="Tree filename label")
    parser.add_argument("--id-field", required=True, help="CSV identifier column")
    parser.add_argument(
        "--table-fields",
        required=True,
        help="Comma-separated CSV columns to expose in the metadata table",
    )
    parser.add_argument("--latitude-field", help="CSV latitude column for map templates")
    parser.add_argument("--longitude-field", help="CSV longitude column for map templates")
    parser.add_argument("--year-field", help="CSV year column for timeline templates")
    parser.add_argument("--month-field", help="CSV month column for timeline templates")
    parser.add_argument("--day-field", help="CSV day column for timeline templates")
    parser.add_argument(
        "--output",
        help="Output JSON path. Defaults to <template>.generated.microreact.json",
    )
    return parser.parse_args()


def require(args: argparse.Namespace, field_name: str, reason: str) -> str:
    value = getattr(args, field_name)
    if not value:
        raise SystemExit(f"--{field_name.replace('_', '-')} is required for {reason}")
    return value


def build_columns(fields_csv: str) -> list[dict]:
    fields = [field.strip() for field in fields_csv.split(",") if field.strip()]
    if not fields:
        raise SystemExit("--table-fields must contain at least one field")
    return [{"field": field} for field in fields]


def main() -> None:
    args = parse_args()
    payload = deepcopy(load_template(args.template))

    payload["meta"]["name"] = args.name
    payload["files"]["data-file-1"]["url"] = args.data_url
    payload["files"]["data-file-1"]["name"] = args.data_name
    payload["datasets"]["dataset-1"]["idFieldName"] = args.id_field
    payload["tables"]["table-1"]["columns"] = build_columns(args.table_fields)

    if "trees" in payload:
        payload["files"]["tree-file-1"]["url"] = require(
            args, "tree_url", "tree-enabled templates"
        )
        payload["files"]["tree-file-1"]["name"] = args.tree_name

    if "maps" in payload:
        payload["maps"]["map-1"]["latitudeField"] = require(
            args, "latitude_field", "map-enabled templates"
        )
        payload["maps"]["map-1"]["longitudeField"] = require(
            args, "longitude_field", "map-enabled templates"
        )

    if "timelines" in payload:
        payload["timelines"]["timeline-1"]["yearField"] = require(
            args, "year_field", "timeline-enabled templates"
        )
        payload["timelines"]["timeline-1"]["monthField"] = require(
            args, "month_field", "timeline-enabled templates"
        )
        payload["timelines"]["timeline-1"]["dayField"] = require(
            args, "day_field", "timeline-enabled templates"
        )

    output_path = Path(
        args.output or f"{args.template}.generated.microreact.json"
    ).resolve()
    output_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(output_path)


if __name__ == "__main__":
    main()
