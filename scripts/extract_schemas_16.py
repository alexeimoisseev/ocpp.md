#!/usr/bin/env python3
"""
Extract OCPP 1.6J JSON schemas and generate markdown documentation.

Reads all *.json from the schema directory (28 request/response pairs),
groups by Feature Profile, and outputs:
  - OCPP-1.6J-Schemas-{Profile}.md  (6 files)

Unlike OCPP 2.0.1 schemas, 1.6J schemas have no shared $ref definitions.
Types are defined inline, so there is no separate DataTypes file.
Nested objects (ChargingProfile, MeterValue, etc.) are documented as
sub-tables under the field where they appear.
"""

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "OCPP_1.6_documentation" / "schemas" / "json"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "OCPP-1.6J-Schemas"

# Message → Feature Profile mapping (from OCPP 1.6 spec section 3.3)
PROFILE_MAP = {
    "Core": [
        "Authorize", "BootNotification", "ChangeAvailability",
        "ChangeConfiguration", "ClearCache", "DataTransfer",
        "GetConfiguration", "Heartbeat", "MeterValues",
        "RemoteStartTransaction", "RemoteStopTransaction",
        "Reset", "StartTransaction", "StatusNotification",
        "StopTransaction", "UnlockConnector",
    ],
    "SmartCharging": [
        "SetChargingProfile", "ClearChargingProfile",
        "GetCompositeSchedule",
    ],
    "Firmware": [
        "GetDiagnostics", "DiagnosticsStatusNotification",
        "UpdateFirmware", "FirmwareStatusNotification",
    ],
    "LocalAuthList": [
        "SendLocalList", "GetLocalListVersion",
    ],
    "Reservation": [
        "ReserveNow", "CancelReservation",
    ],
    "RemoteTrigger": [
        "TriggerMessage",
    ],
}

# Message direction
DIRECTION_MAP = {
    # Core
    "Authorize": "CP → CS",
    "BootNotification": "CP → CS",
    "ChangeAvailability": "CS → CP",
    "ChangeConfiguration": "CS → CP",
    "ClearCache": "CS → CP",
    "DataTransfer": "CP ↔ CS",
    "GetConfiguration": "CS → CP",
    "Heartbeat": "CP → CS",
    "MeterValues": "CP → CS",
    "RemoteStartTransaction": "CS → CP",
    "RemoteStopTransaction": "CS → CP",
    "Reset": "CS → CP",
    "StartTransaction": "CP → CS",
    "StatusNotification": "CP → CS",
    "StopTransaction": "CP → CS",
    "UnlockConnector": "CS → CP",
    # Smart Charging
    "SetChargingProfile": "CS → CP",
    "ClearChargingProfile": "CS → CP",
    "GetCompositeSchedule": "CS → CP",
    # Firmware
    "GetDiagnostics": "CS → CP",
    "DiagnosticsStatusNotification": "CP → CS",
    "UpdateFirmware": "CS → CP",
    "FirmwareStatusNotification": "CP → CS",
    # Local Auth List
    "SendLocalList": "CS → CP",
    "GetLocalListVersion": "CS → CP",
    # Reservation
    "ReserveNow": "CS → CP",
    "CancelReservation": "CS → CP",
    # Remote Trigger
    "TriggerMessage": "CS → CP",
}

# Brief descriptions for each message (from spec sections 4 and 5)
MESSAGE_DESC = {
    "Authorize": "Validate an idTag before or during a transaction.",
    "BootNotification": "Charge Point registers with the Central System after (re)boot.",
    "ChangeAvailability": "Change a connector or the entire Charge Point to operative/inoperative.",
    "ChangeConfiguration": "Set a configuration key on the Charge Point.",
    "ClearCache": "Clear the Charge Point's authorization cache.",
    "DataTransfer": "Vendor-specific data exchange (bidirectional).",
    "GetConfiguration": "Read one or more configuration keys from the Charge Point.",
    "Heartbeat": "Keepalive — Charge Point signals it is still connected.",
    "MeterValues": "Send periodic or clock-aligned meter readings.",
    "RemoteStartTransaction": "Central System requests the Charge Point to start a transaction.",
    "RemoteStopTransaction": "Central System requests the Charge Point to stop a transaction.",
    "Reset": "Reboot the Charge Point (Hard or Soft).",
    "StartTransaction": "Charge Point reports that a transaction has started.",
    "StatusNotification": "Charge Point reports a connector status or error change.",
    "StopTransaction": "Charge Point reports that a transaction has ended.",
    "UnlockConnector": "Remotely unlock a connector (for cable removal).",
    "SetChargingProfile": "Install or update a charging profile on a connector.",
    "ClearChargingProfile": "Remove one or more charging profiles.",
    "GetCompositeSchedule": "Request the combined effective charging schedule.",
    "GetDiagnostics": "Request the Charge Point to upload diagnostic logs.",
    "DiagnosticsStatusNotification": "Charge Point reports diagnostic upload progress.",
    "UpdateFirmware": "Request the Charge Point to download and install firmware.",
    "FirmwareStatusNotification": "Charge Point reports firmware update progress.",
    "SendLocalList": "Push a local authorization list to the Charge Point.",
    "GetLocalListVersion": "Query the version of the local authorization list.",
    "ReserveNow": "Reserve a connector for a specific idTag.",
    "CancelReservation": "Cancel an existing reservation.",
    "TriggerMessage": "Request the Charge Point to send a specific message now.",
}


# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------

def load_schemas():
    """Load all schema JSON files, return dict keyed by filename stem."""
    schemas = {}
    for f in sorted(SCHEMA_DIR.glob("*.json")):
        with open(f) as fh:
            schemas[f.stem] = json.load(fh)
    return schemas


def build_message_registry(schemas):
    """
    Build a registry of all messages.
    Returns: { message_name: { "request": schema_dict, "response": schema_dict } }
    """
    messages = {}

    for filename, schema in schemas.items():
        if filename.endswith("Response"):
            msg_name = filename[:-len("Response")]
            side = "response"
        else:
            msg_name = filename
            side = "request"

        if msg_name not in messages:
            messages[msg_name] = {}
        messages[msg_name][side] = schema

    return messages


# ---------------------------------------------------------------------------
# Field rendering
# ---------------------------------------------------------------------------

def resolve_field_type(prop_def):
    """
    Resolve a property to (type_string, constraints_list).
    For inline enums, type_string includes the enum name contextually.
    For inline objects, returns "object" (caller handles sub-table).
    """
    constraints = []
    ptype = prop_def.get("type", "any")

    if ptype == "string":
        fmt = prop_def.get("format")
        if "enum" in prop_def:
            return "string (enum)", constraints
        if fmt:
            return f"string ({fmt})", constraints
        if "maxLength" in prop_def:
            constraints.append(f"maxLength: {prop_def['maxLength']}")
        if "minLength" in prop_def:
            constraints.append(f"minLength: {prop_def['minLength']}")
        return "string", constraints

    if ptype == "integer":
        if "minimum" in prop_def:
            constraints.append(f"min: {prop_def['minimum']}")
        if "maximum" in prop_def:
            constraints.append(f"max: {prop_def['maximum']}")
        return "integer", constraints

    if ptype == "number":
        if "multipleOf" in prop_def:
            constraints.append(f"multipleOf: {prop_def['multipleOf']}")
        if "minimum" in prop_def:
            constraints.append(f"min: {prop_def['minimum']}")
        if "maximum" in prop_def:
            constraints.append(f"max: {prop_def['maximum']}")
        return "number", constraints

    if ptype == "boolean":
        return "boolean", constraints

    if ptype == "array":
        items = prop_def.get("items", {})
        if items.get("type") == "object":
            return "object[]", constraints
        inner_type, _ = resolve_field_type(items)
        if "minItems" in prop_def:
            constraints.append(f"minItems: {prop_def['minItems']}")
        if "maxItems" in prop_def:
            constraints.append(f"maxItems: {prop_def['maxItems']}")
        return f"{inner_type}[]", constraints

    if ptype == "object":
        return "object", constraints

    return ptype, constraints


def render_fields_table(properties, required_fields, indent_prefix=""):
    """
    Render a markdown fields table. For inline objects and arrays of objects,
    recursively renders sub-tables.
    Returns list of markdown lines.
    """
    if not properties:
        return ["*No fields (empty object).*", ""]

    lines = []
    lines.append(f"{indent_prefix}| Field | Type | Required | Constraints | Description |")
    lines.append(f"{indent_prefix}|-------|------|----------|-------------|-------------|")

    # Sort: required first, then alphabetical
    def sort_key(name):
        return (name not in required_fields, name)

    for field_name in sorted(properties.keys(), key=sort_key):
        prop_def = properties[field_name]
        is_required = field_name in required_fields
        type_str, constraints = resolve_field_type(prop_def)
        constraint_str = ", ".join(constraints)
        req_str = "**Yes**" if is_required else "No"

        # For enum fields, show values in description
        desc = ""
        if "enum" in prop_def:
            vals = ", ".join(f"`{v}`" for v in prop_def["enum"])
            desc = f"Values: {vals}"

        lines.append(f"{indent_prefix}| `{field_name}` | {type_str} | {req_str} | {constraint_str} | {desc} |")

        # Render sub-table for inline objects
        if prop_def.get("type") == "object" and "properties" in prop_def:
            lines.append("")
            sub_props = prop_def["properties"]
            sub_required = prop_def.get("required", [])
            lines.append(f"{indent_prefix}**`{field_name}` object:**")
            lines.append("")
            lines.extend(render_fields_table(sub_props, sub_required, indent_prefix))

        # Render sub-table for arrays of inline objects
        if prop_def.get("type") == "array":
            items = prop_def.get("items", {})
            if items.get("type") == "object" and "properties" in items:
                lines.append("")
                sub_props = items["properties"]
                sub_required = items.get("required", [])
                lines.append(f"{indent_prefix}**`{field_name}[]` items:**")
                lines.append("")
                lines.extend(render_fields_table(sub_props, sub_required, indent_prefix))

    return lines


# ---------------------------------------------------------------------------
# Example payloads
# ---------------------------------------------------------------------------

def generate_example(properties, required_fields, depth=0):
    """Generate a minimal valid JSON example with required fields only."""
    if depth > 4:
        return {}

    obj = {}
    for field_name in sorted(required_fields):
        if field_name not in properties:
            continue
        obj[field_name] = _example_value(properties[field_name], depth)
    return obj


def _example_value(prop_def, depth):
    """Generate an example value for a property."""
    ptype = prop_def.get("type", "")

    if ptype == "string":
        if "enum" in prop_def:
            return prop_def["enum"][0]
        fmt = prop_def.get("format")
        if fmt == "date-time":
            return "2024-01-15T10:30:00Z"
        max_len = prop_def.get("maxLength", 0)
        if max_len == 20:
            return "ABCDEF1234"
        return "string"

    if ptype == "integer":
        return 0

    if ptype == "number":
        return 0.0

    if ptype == "boolean":
        return False

    if ptype == "object" and "properties" in prop_def:
        return generate_example(
            prop_def["properties"],
            prop_def.get("required", []),
            depth + 1,
        )

    if ptype == "array":
        items = prop_def.get("items", {})
        if items.get("type") == "object" and "properties" in items:
            return [generate_example(
                items["properties"],
                items.get("required", []),
                depth + 1,
            )]
        return [_example_value(items, depth + 1)]

    return "..."


# ---------------------------------------------------------------------------
# Markdown file generators
# ---------------------------------------------------------------------------

def generate_profile_md(profile_name, messages_in_profile, message_registry):
    """Generate one OCPP-1.6J-Schemas-{Profile}.md file."""
    lines = []

    # Header
    lines.append(f"# OCPP 1.6J Schemas — {profile_name}")
    lines.append("")
    lines.append(f"> **Feature Profile:** {profile_name}")
    lines.append(f">")
    lines.append(f"> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.")
    lines.append(f"> Field names, types, required status, enum values, and constraints are")
    lines.append(f"> extracted mechanically. No manual editing applied.")
    lines.append("")

    # Table of contents
    lines.append("## Messages")
    lines.append("")
    for msg_name in messages_in_profile:
        direction = DIRECTION_MAP.get(msg_name, "?")
        lines.append(f"- [{msg_name}](#{msg_name.lower()}) ({direction})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Each message
    for msg_name in messages_in_profile:
        msg = message_registry.get(msg_name, {})
        direction = DIRECTION_MAP.get(msg_name, "?")
        desc = MESSAGE_DESC.get(msg_name, "")

        lines.append(f"## {msg_name}")
        lines.append("")
        lines.append(f"**Direction:** {direction}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")

        # Request
        req = msg.get("request")
        if req:
            props = req.get("properties", {})
            required = req.get("required", [])

            lines.append(f"### {msg_name}.req")
            lines.append("")

            if not props:
                lines.append("*No fields (empty object `{}`).*")
                lines.append("")
            else:
                lines.extend(render_fields_table(props, required))
                lines.append("")

            # Example
            example = generate_example(props, required)
            lines.append("<details>")
            lines.append(f"<summary>Example {msg_name}.req</summary>")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(example, indent=2))
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

        # Response
        resp = msg.get("response")
        if resp:
            props = resp.get("properties", {})
            required = resp.get("required", [])

            lines.append(f"### {msg_name}.conf")
            lines.append("")

            if not props:
                lines.append("*No fields (empty object `{}`).*")
                lines.append("")
            else:
                lines.extend(render_fields_table(props, required))
                lines.append("")

            # Example
            example = generate_example(props, required)
            lines.append("<details>")
            lines.append(f"<summary>Example {msg_name}.conf</summary>")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(example, indent=2))
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not SCHEMA_DIR.exists():
        print(f"ERROR: Schema directory not found: {SCHEMA_DIR}", file=sys.stderr)
        print("Download the OCPP 1.6 JSON schemas from OCA and place them in", file=sys.stderr)
        print(f"  {SCHEMA_DIR}", file=sys.stderr)
        sys.exit(1)

    print("Loading schemas...")
    schemas = load_schemas()
    print(f"  Loaded {len(schemas)} schema files")

    print("Building message registry...")
    message_registry = build_message_registry(schemas)
    print(f"  Found {len(message_registry)} messages")

    # Verify all messages in PROFILE_MAP exist in schemas
    all_profile_messages = set()
    for msgs in PROFILE_MAP.values():
        all_profile_messages.update(msgs)

    missing_from_profiles = set(message_registry.keys()) - all_profile_messages
    missing_from_schemas = all_profile_messages - set(message_registry.keys())

    if missing_from_profiles:
        print(f"  WARNING: Messages in schemas but not in PROFILE_MAP: {missing_from_profiles}", file=sys.stderr)
    if missing_from_schemas:
        print(f"  WARNING: Messages in PROFILE_MAP but not in schemas: {missing_from_schemas}", file=sys.stderr)

    # Generate profile files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for profile_name, messages_in_profile in PROFILE_MAP.items():
        print(f"Generating OCPP-1.6J-Schemas-{profile_name}.md...")
        content = generate_profile_md(profile_name, messages_in_profile, message_registry)
        output_path = OUTPUT_DIR / f"OCPP-1.6J-Schemas-{profile_name}.md"
        with open(output_path, "w") as f:
            f.write(content)
        print(f"  Written to {output_path}")

    # Summary
    print(f"\nDone! Generated {len(PROFILE_MAP)} files:")
    for profile_name, msgs in PROFILE_MAP.items():
        print(f"  - OCPP-1.6J-Schemas-{profile_name}.md ({len(msgs)} messages)")


if __name__ == "__main__":
    main()
