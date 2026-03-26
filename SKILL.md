---
name: microreact-project-template
description: Create or adapt Microreact `.microreact` JSON payloads for API project creation. Use when the user wants starter payloads, wants to transform CSV/tree/map/timeline inputs into a valid Microreact project document, or wants a reusable template for `POST /api/projects/create/`.
---

# Microreact Project Template

## Overview

Use this skill when the task is to generate or adapt a Microreact `.microreact`
payload for the documented API create flow. This skill provides ready-made
starter templates and a script that fills them with project-specific URLs and
column names.

## Workflow

1. Decide which starter shape matches the request:
   - `csv-only`
   - `csv-tree`
   - `csv-map`
   - `csv-tree-map`
   - `csv-tree-map-timeline`
2. If the user only wants a starter, use the matching file from
   `assets/templates/`.
3. If the user has concrete URLs and field names, run
   `scripts/generate_microreact_template.py`.
4. Return the generated file path and call out any required placeholders that
   still need real values.

## Required Inputs

- For every template:
  - project name
  - CSV URL
  - CSV record ID field
  - CSV table fields to expose
- For tree templates:
  - tree URL
- For map templates:
  - latitude field
  - longitude field
- For timeline templates:
  - year field
  - month field
  - day field

If the user has not provided these, either keep placeholders in the starter
template or infer only when the correct values are obvious from local context.

## Resources

### Starter templates

These live in `assets/templates/`:

- `csv-only.microreact.json`
- `csv-tree.microreact.json`
- `csv-map.microreact.json`
- `csv-tree-map.microreact.json`
- `csv-tree-map-timeline.microreact.json`

### Generator script

Use:

```bash
python3 scripts/generate_microreact_template.py --help
```

Typical invocation:

```bash
python3 scripts/generate_microreact_template.py \
  --template csv-tree-map \
  --name "Example Project" \
  --data-url "https://example.org/data.csv" \
  --tree-url "https://example.org/tree.nwk" \
  --id-field sample_id \
  --table-fields "sample_id,country,__latitude,__longitude" \
  --latitude-field __latitude \
  --longitude-field __longitude \
  --output example.microreact.json
```

## Constraints

- Keep `schema` as `https://microreact.org/schema/v1.json`
- Keep file references stable: dataset points to the CSV file entry; tree points
  to the Newick file entry
- `datasets.dataset-1.idFieldName` must match the CSV identifier column
- `tables.table-1.columns` should only reference real CSV fields
- Map and timeline field names must match CSV column names exactly

## Output Expectations

When generating a payload, return:

- the output path
- the chosen template shape
- any remaining placeholders or assumptions

When only supplying a starter template, point to the relevant file in
`assets/templates/`.
