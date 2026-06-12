#!/usr/bin/env python3
"""
Generate OCPP 2.1 device-model and open-enumeration reference from appendix CSVs.

Reads:  OCPP-2.1_appendices_csv/*.csv (components, variables, dm_components_vars, + 11 enum files)
Writes: docs/OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md
        docs/OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md
"""
import csv
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


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "| " + " | ".join("---" for _ in header) + " |"]
    for r in rows:
        cells = [(c or "").replace("|", "\\|").replace("\n", " ") for c in r]
        cells = cells[:len(header)] + [""] * max(0, len(header) - len(cells))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


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
    for name in ("components.csv", "variables.csv", "dm_components_vars.csv"):
        if not (CSV_DIR / name).exists():
            sys.exit(f"ERROR: required appendix CSV missing: {CSV_DIR / name}")
    DM_OUT.parent.mkdir(parents=True, exist_ok=True)
    comp_h, comp_r = read_csv("components.csv")
    var_h, var_r = read_csv("variables.csv")
    cv_h, cv_r = read_csv("dm_components_vars.csv")
    lines = [
        "# OCPP 2.1 — Device Model Reference",
        "",
        "> **Source:** OCA OCPP 2.1 appendix CSVs (`components.csv`, `variables.csv`, "
        "`dm_components_vars.csv`). Mechanically generated — see "
        "[METHODOLOGY](../METHODOLOGY.md). These are the **standardized** component and "
        "variable names referenced by free-form `name` fields in `GetVariables`/`SetVariables`/"
        "`GetReport`. Vendors may extend with optional custom components/variables.",
        "",
        f"## Components ({len(comp_r)})", "", md_table(comp_h, comp_r), "",
        f"## Component × Variable Matrix ({len(cv_r)})", "",
        "> `<generic>` in the Component column means the variable applies generically, "
        "not to one specific component.", "",
        md_table(cv_h, cv_r), "",
        f"## Variables ({len(var_r)})", "", md_table(var_h, var_r), "",
    ]
    DM_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {DM_OUT} — {len(comp_r)} components, {len(var_r)} variables, {len(cv_r)} matrix rows")

    generate_enums()


if __name__ == "__main__":
    main()
