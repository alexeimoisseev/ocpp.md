#!/usr/bin/env python3
"""
Generate OCPP 2.1 device-model and open-enumeration reference from appendix CSVs.

Reads:  OCPP-2.1_appendices_csv/*.csv (components, variables, dm_components_vars, + 11 enum files)
Writes: docs/OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md
        docs/OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "OCPP-2.1_appendices_csv"
DM_OUT = ROOT / "docs" / "OCPP-2.1-DeviceModel" / "OCPP-2.1-DeviceModel.md"
ENUM_OUT = ROOT / "docs" / "OCPP-2.1-Enumerations" / "OCPP-2.1-Enumerations.md"

ENUM_FILES = [
    ("connectorenumtype.csv",         "Connector Types",             "Backs the free-form `connectorType` field."),
    ("units_of_measure.csv",          "Units of Measure",            "Backs the `unit` field in MeterValues/measurands."),
    ("security_events.csv",           "Security Events",             "Backs `SecurityEventNotification.type`."),
    ("reason_codes.csv",              "Status Reason Codes",         "Standardized `StatusInfo.reasonCode` values."),
    ("signingmethod.csv",             "Signing Methods",             "Backs `signingMethod` in signed meter values."),
    ("charginglimitsourceenumtype.csv", "Charging Limit Sources",    "Backs `chargingLimitSource`."),
    ("idtokenenumtype.csv",           "IdToken Types",               "Standardized `idToken.type` values."),
    ("additional_info_types.csv",     "Additional Info Types",       "Backs `additionalInfo.type`."),
    ("additional_info_types_adhoc.csv", "Additional Info Types (Ad-hoc)", "Ad-hoc payment additionalInfo types."),
    ("paymentbrand.csv",              "Payment Brands",              "Standardized payment brand values."),
    ("paymentrecognition.csv",        "Payment Recognition",         "Payment recognition method values."),
]


def read_csv(name):
    with open(CSV_DIR / name, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f, delimiter=";"))
    header = [c.strip() for c in rows[0]]
    return header, [[c.strip() for c in r] for r in rows[1:] if any(c.strip() for c in r)]


def md_cell(value):
    """Make a CSV value safe inside a Markdown table cell: escape the column
    pipe and flatten newlines. Kept HTML-free — see render_matrix for how
    tag-like literals such as `<generic>` are handled (backticks, not entities).
    """
    return (value or "").replace("|", "\\|").replace("\n", " ")


def md_table(header, rows):
    out = ["| " + " | ".join(md_cell(h) for h in header) + " |",
           "| " + " | ".join("---" for _ in header) + " |"]
    for r in rows:
        cells = [md_cell(c) for c in r]
        cells = cells[:len(header)] + [""] * max(0, len(header) - len(cells))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


GENERIC = "<generic>"


def slug(text):
    """Heading slug matching python-markdown's toc extension (lowercase,
    drop non-word chars, spaces -> hyphens). Component names are single tokens,
    so this is essentially `text.lower()`."""
    s = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s]+", "-", s)


def _variable_block(cell, row):
    """One variable entry: bold name + compact metadata line, then description.
    The owning component is omitted (it's the section heading)."""
    var = cell(row, "Variable")
    inst = cell(row, "Instance")
    req = cell(row, "Required?")
    dtype = cell(row, "DataType")
    unit = cell(row, "Unit")
    desc = cell(row, "Description")

    meta = []
    if req:
        meta.append(f"Required: {req}")
    if dtype:
        meta.append(f"Type: {dtype}")
    if unit:
        meta.append(f"Unit: {unit}")
    if inst:
        meta.append(f"Instance: `{inst}`")

    heading = f"**`{var}`**" if var else "**(unnamed variable)**"
    block = [f"{heading} — " + "  ·  ".join(meta) if meta else heading]
    if desc:
        block += ["", desc]
    return "\n".join(block)


def matrix_components(header, rows):
    """Sorted set of named components that own at least one matrix variable."""
    i = header.index("Specific Component")
    named = {r[i].strip() for r in rows if i < len(r) and r[i].strip() and r[i].strip() != GENERIC}
    return sorted(named, key=str.lower)


def render_variables_by_component(header, rows):
    """Group the matrix into one `### <Component>` section per component (plus a
    Generic section), each listing its variables as per-variable blocks. The
    blocks stay plain Markdown; the website cards them for visual separation.
    """
    idx = {h: i for i, h in enumerate(header)}

    def cell(row, name):
        i = idx.get(name)
        return row[i].strip() if i is not None and i < len(row) else ""

    groups = {}
    for row in rows:
        comp = cell(row, "Specific Component") or GENERIC
        groups.setdefault(comp, []).append(row)

    named = sorted((c for c in groups if c != GENERIC), key=str.lower)
    order = named + ([GENERIC] if GENERIC in groups else [])

    out = []
    for comp in order:
        if comp == GENERIC:
            out += ["### Generic variables", "",
                    "Variables that apply generically to any component, "
                    "not bound to one specific component.", ""]
        else:
            out += [f"### {comp}", ""]
        blocks = [_variable_block(cell, row) for row in groups[comp]]
        out.append("\n\n".join(blocks))
        out.append("")
    return "\n".join(out).rstrip()


def generate_enums():
    ENUM_OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# OCPP 2.1 — Standardized Open Enumerations", "",
        "> **Source:** OCA OCPP 2.1 appendix CSVs. These are **open enumerations**: the JSON "
        "schemas type these fields as free-form strings and point here for the standardized "
        "values. Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md).", ""]
    for fname, title, note in ENUM_FILES:
        if not (CSV_DIR / fname).exists():
            print(f"  WARN missing {fname}")
            continue
        h, r = read_csv(fname)
        lines += [f"## {title} ({len(r)})", "", f"> {note}", "", md_table(h, r), ""]
    ENUM_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {ENUM_OUT}")


def main():
    for name in ("components.csv", "dm_components_vars.csv"):
        if not (CSV_DIR / name).exists():
            sys.exit(f"ERROR: required appendix CSV missing: {CSV_DIR / name}")
    DM_OUT.parent.mkdir(parents=True, exist_ok=True)
    comp_h, comp_r = read_csv("components.csv")
    cv_h, cv_r = read_csv("dm_components_vars.csv")

    # Link each Components-table row to its variable section (if it has one).
    # The first CSV column is the component name.
    linked = set(matrix_components(cv_h, cv_r))
    comp_rows = [
        ([f"[{r[0]}](#{slug(r[0])})" if r and r[0] in linked else (r[0] if r else "")] + list(r[1:]))
        for r in comp_r
    ]

    lines = [
        "# OCPP 2.1 — Device Model Reference",
        "",
        "> **Source:** OCA OCPP 2.1 appendix CSVs (`components.csv`, `dm_components_vars.csv`). "
        "Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md). These are the "
        "**standardized** component and variable names referenced by free-form `name` fields "
        "in `GetVariables`/`SetVariables`/`GetReport`. Vendors may extend with optional custom "
        "components/variables.",
        "",
        f"## Components ({len(comp_r)})", "",
        "> Component names link to their variables in "
        "[Variables by Component](#variables-by-component) below "
        "(components with no component-specific variables use only generic variables).", "",
        md_table(comp_h, comp_rows), "",
        "## Variables by Component", "",
        f"> All {len(cv_r)} component/variable pairings, grouped by the component they "
        "belong to. **Generic** variables apply to any component. Each variable lists its "
        "required flag, datatype, unit, and instance where applicable.", "",
        "> ⚠️ **Suspected OCA source defects (flag, not authoritative).** The OCA's "
        "component×variable appendix table (the source for the groups below) disagrees with "
        "its separate standardized-variable definitions list in ways that look like errors in "
        "the source data. None are listed in the OCPP 2.1 errata (2026-04), so they appear "
        "**unreported** (spec checked: Edition 2, 2025-12-03 — published, not draft). "
        "Device-model variable names are **case-sensitive on the wire**, so verify against the "
        "official spec before relying on a spelling:", "",
        "> - **Casing:** the groups below use `TargetSoC` (BatterySwapCtrlr) and `VehicleID` "
        "(ConnectedEV), but the Part 2 prose / Appendix 3.2.13 and the standardized-variable "
        "list use `TargetSoc` and `VehicleId` — the spellings below are the **deviant ones**.",
        "> - **Name mismatch (same concept, different name):** `NotificationDelay` below "
        "(ISO15118Ctrlr) is `NotificationMaxDelay` in the variable-definitions list; "
        "`SupportedIdTokenType` below (AuthCtrlr) is `SupportedIdTokenTypes` there.",
        "> - **Defined but absent here:** `EnergyCapacity` and `Present` exist in the OCA "
        "variable-definitions list but are mapped to no component, so they do not appear "
        "below; both read like generic variables (cf. `Available`/`Enabled`).", "",
        render_variables_by_component(cv_h, cv_r), "",
    ]
    DM_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {DM_OUT} — {len(comp_r)} components, {len(cv_r)} component/variable pairings")

    generate_enums()


if __name__ == "__main__":
    main()
