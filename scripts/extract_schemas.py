#!/usr/bin/env python3
"""
Extract OCPP 2.0.1 JSON schemas and generate markdown documentation.

Reads all *Request.json / *Response.json from the schema directory,
deduplicates shared types, and outputs:
  - OCPP-2.0.1-DataTypes.md
  - OCPP-2.0.1-Schemas-{Block}.md  (10 files)
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "OCPP-2.0.1_JSON_schemas"
REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_OUTPUT_DIR = REPO_ROOT / "OCPP-2.0.1-Schemas"  # block files go here
DATATYPES_OUTPUT_DIR = REPO_ROOT  # DataTypes.md stays at repo root

# Message → functional block mapping
BLOCK_MAP = {
    "Provisioning": [
        "BootNotification", "Heartbeat", "StatusNotification",
        "GetVariables", "SetVariables", "GetBaseReport", "GetReport",
        "NotifyReport", "Reset", "DataTransfer", "SetNetworkProfile",
    ],
    "Authorization": [
        "Authorize", "SendLocalList", "GetLocalListVersion", "ClearCache",
    ],
    "Transactions": [
        "TransactionEvent", "RequestStartTransaction", "RequestStopTransaction",
        "GetTransactionStatus", "MeterValues",
    ],
    "SmartCharging": [
        "SetChargingProfile", "GetChargingProfiles", "ClearChargingProfile",
        "ReportChargingProfiles", "GetCompositeSchedule",
        "ClearedChargingLimit", "NotifyChargingLimit",
        "NotifyEVChargingSchedule", "NotifyEVChargingNeeds",
    ],
    "Firmware": [
        "UpdateFirmware", "FirmwareStatusNotification",
        "PublishFirmware", "PublishFirmwareStatusNotification",
        "UnpublishFirmware",
    ],
    "Security": [
        "Get15118EVCertificate", "GetCertificateStatus",
        "SignCertificate", "CertificateSigned",
        "InstallCertificate", "DeleteCertificate",
        "GetInstalledCertificateIds", "SecurityEventNotification",
    ],
    "Diagnostics": [
        "GetLog", "LogStatusNotification", "NotifyEvent",
        "SetMonitoringBase", "SetVariableMonitoring", "SetMonitoringLevel",
        "GetMonitoringReport", "ClearVariableMonitoring",
        "NotifyMonitoringReport", "CustomerInformation",
        "NotifyCustomerInformation",
    ],
    "Availability": [
        "ChangeAvailability", "UnlockConnector", "TriggerMessage",
    ],
    "Reservation": [
        "ReserveNow", "CancelReservation", "ReservationStatusUpdate",
    ],
    "Display": [
        "SetDisplayMessage", "GetDisplayMessages", "ClearDisplayMessage",
        "NotifyDisplayMessages", "CostUpdated",
    ],
}

# Message direction: True = CS→CSMS, False = CSMS→CS, "Both" = bidirectional
DIRECTION_MAP = {
    # Provisioning
    "BootNotification": "CS → CSMS",
    "Heartbeat": "CS → CSMS",
    "StatusNotification": "CS → CSMS",
    "GetVariables": "CSMS → CS",
    "SetVariables": "CSMS → CS",
    "GetBaseReport": "CSMS → CS",
    "GetReport": "CSMS → CS",
    "NotifyReport": "CS → CSMS",
    "Reset": "CSMS → CS",
    "DataTransfer": "Both",
    "SetNetworkProfile": "CSMS → CS",
    # Authorization
    "Authorize": "CS → CSMS",
    "SendLocalList": "CSMS → CS",
    "GetLocalListVersion": "CSMS → CS",
    "ClearCache": "CSMS → CS",
    # Transactions
    "TransactionEvent": "CS → CSMS",
    "RequestStartTransaction": "CSMS → CS",
    "RequestStopTransaction": "CSMS → CS",
    "GetTransactionStatus": "CSMS → CS",
    "MeterValues": "CS → CSMS",
    # Smart Charging
    "SetChargingProfile": "CSMS → CS",
    "GetChargingProfiles": "CSMS → CS",
    "ClearChargingProfile": "CSMS → CS",
    "ReportChargingProfiles": "CS → CSMS",
    "GetCompositeSchedule": "CSMS → CS",
    "ClearedChargingLimit": "CS → CSMS",
    "NotifyChargingLimit": "CS → CSMS",
    "NotifyEVChargingSchedule": "CS → CSMS",
    "NotifyEVChargingNeeds": "CS → CSMS",
    # Firmware
    "UpdateFirmware": "CSMS → CS",
    "FirmwareStatusNotification": "CS → CSMS",
    "PublishFirmware": "CSMS → CS",
    "PublishFirmwareStatusNotification": "CS → CSMS",
    "UnpublishFirmware": "CSMS → CS",
    # Security
    "Get15118EVCertificate": "CS → CSMS",
    "GetCertificateStatus": "CS → CSMS",
    "SignCertificate": "CS → CSMS",
    "CertificateSigned": "CSMS → CS",
    "InstallCertificate": "CSMS → CS",
    "DeleteCertificate": "CSMS → CS",
    "GetInstalledCertificateIds": "CSMS → CS",
    "SecurityEventNotification": "CS → CSMS",
    # Diagnostics
    "GetLog": "CSMS → CS",
    "LogStatusNotification": "CS → CSMS",
    "NotifyEvent": "CS → CSMS",
    "SetMonitoringBase": "CSMS → CS",
    "SetVariableMonitoring": "CSMS → CS",
    "SetMonitoringLevel": "CSMS → CS",
    "GetMonitoringReport": "CSMS → CS",
    "ClearVariableMonitoring": "CSMS → CS",
    "NotifyMonitoringReport": "CS → CSMS",
    "CustomerInformation": "CSMS → CS",
    "NotifyCustomerInformation": "CS → CSMS",
    # Availability
    "ChangeAvailability": "CSMS → CS",
    "UnlockConnector": "CSMS → CS",
    "TriggerMessage": "CSMS → CS",
    # Reservation
    "ReserveNow": "CSMS → CS",
    "CancelReservation": "CSMS → CS",
    "ReservationStatusUpdate": "CS → CSMS",
    # Display
    "SetDisplayMessage": "CSMS → CS",
    "GetDisplayMessages": "CSMS → CS",
    "ClearDisplayMessage": "CSMS → CS",
    "NotifyDisplayMessages": "CS → CSMS",
    "CostUpdated": "CSMS → CS",
}

# Functional block letter codes
BLOCK_CODES = {
    "Provisioning": "B",
    "Authorization": "C",
    "Transactions": "D",
    "SmartCharging": "H",
    "Firmware": "I",
    "Security": "B/J",
    "Diagnostics": "K",
    "Availability": "E/F",
    "Reservation": "N",
    "Display": "L",
}

# Threshold: types appearing in >= this many files go into DataTypes.md
SHARED_TYPE_THRESHOLD = 3

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def load_schemas():
    """Load all schema JSON files, return dict keyed by filename stem."""
    schemas = {}
    for f in sorted(SCHEMA_DIR.glob("*.json")):
        with open(f) as fh:
            schemas[f.stem] = json.load(fh)
    return schemas


def clean_description(desc):
    """Clean up OCA schema descriptions for markdown."""
    if not desc:
        return ""
    # Strip \r
    desc = desc.replace("\r\n", "\n").replace("\r", "")
    # Convert HTML entities FIRST (so regexes can match << >> etc.)
    desc = desc.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    # Remove OCA URN lines like "urn:x-oca:ocpp:uid:1:569324" or "urn:x-enexis:ecdm:uid:1:569198"
    desc = re.sub(r'urn:x-[\w:-]+\n?', '', desc)
    # Remove spec-internal field/class path lines at the START of descriptions.
    # OCA descriptions follow the pattern:
    #   "Field_ Path. Sub. Name\n<URN removed>\nActual description.\n"
    # After URN removal, the first line is the field path. Match patterns like:
    #   "Sampled_ Value. Context. Reading_ Context_ Code\n"
    #   "ID_ Token. Status. Authorization_ Status\n"
    #   "Meter_ Value\n"
    #   "Transaction\n"
    # Only match at absolute string start to avoid stripping real description lines.
    # Match lines containing "_ " (underscore-space) or ". " (dot-space) patterns,
    # or short single-word type names (<=30 chars, no spaces except with underscore).
    desc = re.sub(
        r'\A[\w][\w_ ]*(\.\s*[\w][\w_ ]*)+\s*\n',  # dotted paths
        '', desc
    )
    desc = re.sub(
        r'\A[\w]+_\s[\w_ ]*\s*\n',  # underscore-space type names like "Meter_ Value"
        '', desc
    )
    desc = re.sub(
        r'\A[A-Z][\w]{0,29}\s*\n',  # short single-word type names like "Transaction"
        '', desc
    )
    # Convert spec cross-references <<ref-RFC5646,[RFC5646]>> → RFC 5646
    desc = re.sub(r'<<ref-([^,>]+),\[([^\]]+)\]>>', r'\2', desc)
    # Convert <<identifier,Display Text>> → Display Text
    desc = re.sub(r'<<[^,>]+,\s*([^>]+?)>>', r'\1', desc)
    # Remove any remaining << >> fragments
    desc = re.sub(r'<<[^>]*>>', '', desc)
    # Strip backtick formatting from cleaned references
    desc = desc.replace('`', '')
    # Collapse multiple newlines
    desc = re.sub(r'\n{2,}', ' ', desc)
    # Trim and collapse whitespace
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc


def extract_type_name_from_ref(ref):
    """Extract type name from $ref like '#/definitions/FooType'."""
    return ref.split("/")[-1]


# ---------------------------------------------------------------------------
# Type Registry
# ---------------------------------------------------------------------------

def build_type_registry(schemas):
    """
    Build a registry of all types across all schema files.
    Returns: { type_name: { "definition": {...}, "files": [filenames], "is_enum": bool } }
    """
    registry = {}

    for filename, schema in schemas.items():
        defs = schema.get("definitions", {})
        for type_name, type_def in defs.items():
            if type_name not in registry:
                registry[type_name] = {
                    "definition": type_def,
                    "files": [],
                    "is_enum": "enum" in type_def,
                }
            else:
                # Pick the definition with the longest description (most informative)
                existing_desc = registry[type_name]["definition"].get("description", "")
                new_desc = type_def.get("description", "")
                if len(new_desc) > len(existing_desc):
                    registry[type_name]["definition"] = type_def
            registry[type_name]["files"].append(filename)

    return registry


def build_message_registry(schemas):
    """
    Build a registry of all messages.
    Returns: { message_name: { "request": {...}, "response": {...} } }
    """
    messages = {}

    for filename, schema in schemas.items():
        if filename.endswith("Request"):
            msg_name = filename[:-len("Request")]
        elif filename.endswith("Response"):
            msg_name = filename[:-len("Response")]
        else:
            continue

        if msg_name not in messages:
            messages[msg_name] = {}

        side = "request" if filename.endswith("Request") else "response"
        messages[msg_name][side] = {
            "properties": schema.get("properties", {}),
            "required": schema.get("required", []),
            "definitions": schema.get("definitions", {}),
        }

    return messages


# ---------------------------------------------------------------------------
# Classify types: shared (DataTypes.md) vs local (inline in block file)
# ---------------------------------------------------------------------------

def classify_types(type_registry):
    """Split types into shared (for DataTypes.md) and local."""
    shared = {}
    local = {}
    for type_name, info in type_registry.items():
        if len(info["files"]) >= SHARED_TYPE_THRESHOLD:
            shared[type_name] = info
        else:
            local[type_name] = info
    return shared, local


# ---------------------------------------------------------------------------
# Resolve which messages use which types (for "Used in" annotations)
# ---------------------------------------------------------------------------

def build_type_usage_map(type_registry):
    """
    Map each type to the message names that use it.
    Returns: { type_name: sorted list of message names }
    """
    usage = defaultdict(set)
    for type_name, info in type_registry.items():
        for filename in info["files"]:
            # Extract message name from filename
            if filename.endswith("Request"):
                msg = filename[:-len("Request")]
            elif filename.endswith("Response"):
                msg = filename[:-len("Response")]
            else:
                msg = filename
            usage[type_name].add(msg)
    return {k: sorted(v) for k, v in usage.items()}


# ---------------------------------------------------------------------------
# Markdown generation helpers
# ---------------------------------------------------------------------------

def format_type_ref(prop_def, type_name, is_shared, is_array=False):
    """Format a type reference as a markdown link."""
    if is_shared:
        link = f"[{type_name}](../OCPP-2.0.1-DataTypes.md#{type_name.lower()})"
    else:
        link = f"[{type_name}](#{type_name.lower()})"
    if is_array:
        return f"\\[[{type_name}](../OCPP-2.0.1-DataTypes.md#{type_name.lower()})]" if is_shared else f"\\[[{type_name}](#{type_name.lower()})]"
    return link


def resolve_field_type(prop_def, shared_types):
    """
    Resolve a property definition to a display type string.
    Returns (type_string, constraints_string).
    """
    constraints = []

    if "$ref" in prop_def:
        type_name = extract_type_name_from_ref(prop_def["$ref"])
        is_shared = type_name in shared_types
        if is_shared:
            type_str = f"[{type_name}](../OCPP-2.0.1-DataTypes.md#{type_name.lower()})"
        else:
            type_str = f"[{type_name}](#{type_name.lower()})"
        return type_str, ""

    ptype = prop_def.get("type", "")

    if ptype == "array":
        items = prop_def.get("items", {})
        if "$ref" in items:
            type_name = extract_type_name_from_ref(items["$ref"])
            is_shared = type_name in shared_types
            if is_shared:
                inner = f"[{type_name}](../OCPP-2.0.1-DataTypes.md#{type_name.lower()})"
            else:
                inner = f"[{type_name}](#{type_name.lower()})"
        else:
            inner = items.get("type", "any")
        type_str = f"{inner}[]"

        if "minItems" in prop_def:
            constraints.append(f"minItems: {prop_def['minItems']}")
        if "maxItems" in prop_def:
            constraints.append(f"maxItems: {prop_def['maxItems']}")
        return type_str, ", ".join(constraints)

    if ptype == "string":
        type_str = "string"
        fmt = prop_def.get("format")
        if fmt:
            type_str = f"string ({fmt})"
        if "maxLength" in prop_def:
            constraints.append(f"maxLength: {prop_def['maxLength']}")
        if "minLength" in prop_def:
            constraints.append(f"minLength: {prop_def['minLength']}")
        return type_str, ", ".join(constraints)

    if ptype == "integer":
        type_str = "integer"
        if "minimum" in prop_def:
            constraints.append(f"min: {prop_def['minimum']}")
        if "maximum" in prop_def:
            constraints.append(f"max: {prop_def['maximum']}")
        return type_str, ", ".join(constraints)

    if ptype == "number":
        type_str = "number"
        if "minimum" in prop_def:
            constraints.append(f"min: {prop_def['minimum']}")
        if "maximum" in prop_def:
            constraints.append(f"max: {prop_def['maximum']}")
        return type_str, ", ".join(constraints)

    if ptype == "boolean":
        return "boolean", ""

    return ptype or "any", ", ".join(constraints)


def resolve_field_type_for_datatype(prop_def, all_shared_types):
    """Same as resolve_field_type but links within DataTypes use local anchors."""
    constraints = []

    if "$ref" in prop_def:
        type_name = extract_type_name_from_ref(prop_def["$ref"])
        type_str = f"[{type_name}](#{type_name.lower()})"
        return type_str, ""

    ptype = prop_def.get("type", "")

    if ptype == "array":
        items = prop_def.get("items", {})
        if "$ref" in items:
            type_name = extract_type_name_from_ref(items["$ref"])
            inner = f"[{type_name}](#{type_name.lower()})"
        else:
            inner = items.get("type", "any")
        type_str = f"{inner}[]"
        if "minItems" in prop_def:
            constraints.append(f"minItems: {prop_def['minItems']}")
        if "maxItems" in prop_def:
            constraints.append(f"maxItems: {prop_def['maxItems']}")
        return type_str, ", ".join(constraints)

    if ptype == "string":
        type_str = "string"
        fmt = prop_def.get("format")
        if fmt:
            type_str = f"string ({fmt})"
        if "maxLength" in prop_def:
            constraints.append(f"maxLength: {prop_def['maxLength']}")
        if "minLength" in prop_def:
            constraints.append(f"minLength: {prop_def['minLength']}")
        return type_str, ", ".join(constraints)

    if ptype == "integer":
        type_str = "integer"
        if "minimum" in prop_def:
            constraints.append(f"min: {prop_def['minimum']}")
        if "maximum" in prop_def:
            constraints.append(f"max: {prop_def['maximum']}")
        return type_str, ", ".join(constraints)

    if ptype == "number":
        type_str = "number"
        if "minimum" in prop_def:
            constraints.append(f"min: {prop_def['minimum']}")
        if "maximum" in prop_def:
            constraints.append(f"max: {prop_def['maximum']}")
        return type_str, ", ".join(constraints)

    if ptype == "boolean":
        return "boolean", ""

    return ptype or "any", ", ".join(constraints)


def generate_fields_table(properties, required_fields, shared_types, for_datatype=False):
    """Generate a markdown table of fields for a message or type."""
    if not properties:
        return "*No fields (empty object).*\n"

    lines = []
    lines.append("| Field | Type | Required | Constraints | Description |")
    lines.append("|-------|------|----------|-------------|-------------|")

    # Sort: required first, then optional; customData always last
    def sort_key(field_name):
        is_custom = field_name == "customData"
        is_required = field_name in required_fields
        return (is_custom, not is_required, field_name)

    for field_name in sorted(properties.keys(), key=sort_key):
        prop_def = properties[field_name]
        is_required = field_name in required_fields

        if for_datatype:
            type_str, constraint_str = resolve_field_type_for_datatype(prop_def, shared_types)
        else:
            type_str, constraint_str = resolve_field_type(prop_def, shared_types)

        desc = clean_description(prop_def.get("description", ""))

        # Add default value to description if present
        default = prop_def.get("default")
        if default is not None:
            desc_default = f"Default: `{default}`"
            if desc:
                desc = f"{desc} {desc_default}"
            else:
                desc = desc_default

        req_str = "**Yes**" if is_required else "No"

        lines.append(f"| `{field_name}` | {type_str} | {req_str} | {constraint_str} | {desc} |")

    return "\n".join(lines) + "\n"


def generate_example_payload(properties, required_fields, definitions, depth=0):
    """Generate a minimal valid JSON example with required fields only."""
    if depth > 3:
        return "{...}"

    obj = {}
    for field_name in sorted(required_fields):
        if field_name not in properties:
            continue
        prop_def = properties[field_name]
        obj[field_name] = _example_value(prop_def, definitions, depth)

    return json.dumps(obj, indent=2)


def _example_value(prop_def, definitions, depth):
    """Generate an example value for a property."""
    if "$ref" in prop_def:
        type_name = extract_type_name_from_ref(prop_def["$ref"])
        if type_name in definitions:
            sub_def = definitions[type_name]
            if "enum" in sub_def:
                return sub_def["enum"][0]
            sub_props = sub_def.get("properties", {})
            sub_req = sub_def.get("required", [])
            if depth < 2:
                sub_obj = {}
                for f in sub_req:
                    if f in sub_props:
                        sub_obj[f] = _example_value(sub_props[f], definitions, depth + 1)
                return sub_obj
            return "{...}"
        return "..."

    ptype = prop_def.get("type", "")

    if ptype == "string":
        fmt = prop_def.get("format")
        if fmt == "date-time":
            return "2024-01-15T10:30:00Z"
        enums = prop_def.get("enum")
        if enums:
            return enums[0]
        return "string"

    if ptype == "integer":
        return prop_def.get("default", 0)

    if ptype == "number":
        return prop_def.get("default", 0.0)

    if ptype == "boolean":
        return prop_def.get("default", False)

    if ptype == "array":
        items = prop_def.get("items", {})
        return [_example_value(items, definitions, depth + 1)]

    return "..."


# ---------------------------------------------------------------------------
# Markdown file generators
# ---------------------------------------------------------------------------

def generate_datatypes_md(shared_types, type_usage_map):
    """Generate OCPP-2.0.1-DataTypes.md."""
    lines = []

    # Header
    lines.append("# OCPP 2.0.1 — Data Types Reference")
    lines.append("")
    lines.append("> **Purpose:** Complete reference of all reusable data types and enumerations in OCPP 2.0.1.")
    lines.append("> Generated from the official OCA JSON schemas.")
    lines.append(">")
    lines.append("> **See also:** Message schemas by functional block:")
    for block_name in BLOCK_MAP:
        lines.append(f"> [Schemas — {block_name}](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-{block_name}.md) |")
    lines.append("")

    # Separate enums and composite types
    enums = {k: v for k, v in shared_types.items() if v["is_enum"]}
    composites = {k: v for k, v in shared_types.items() if not v["is_enum"]}

    lines.append(f"**{len(enums)} Enum Types** | **{len(composites)} Composite Types**")
    lines.append("")

    # Table of contents
    lines.append("---")
    lines.append("")
    lines.append("## Table of Contents")
    lines.append("")
    lines.append("### Enums")
    lines.append("")
    for name in sorted(enums.keys()):
        lines.append(f"- [{name}](#{name.lower()})")
    lines.append("")
    lines.append("### Composite Types")
    lines.append("")
    for name in sorted(composites.keys()):
        lines.append(f"- [{name}](#{name.lower()})")
    lines.append("")

    # Enums section
    lines.append("---")
    lines.append("")
    lines.append("## Enums")
    lines.append("")

    for name in sorted(enums.keys()):
        info = enums[name]
        defn = info["definition"]
        desc = clean_description(defn.get("description", ""))

        lines.append(f"### {name}")
        lines.append("")
        if desc:
            lines.append(f"{desc}")
            lines.append("")

        # Default value
        default = defn.get("default")
        if default is not None:
            lines.append(f"**Default:** `{default}`")
            lines.append("")

        lines.append("| Value |")
        lines.append("|-------|")
        for val in defn["enum"]:
            lines.append(f"| `{val}` |")
        lines.append("")

        # Used in
        if name in type_usage_map:
            msgs = type_usage_map[name]
            lines.append(f"**Used in:** {', '.join(msgs)}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Composite types section
    lines.append("## Composite Types")
    lines.append("")

    for name in sorted(composites.keys()):
        info = composites[name]
        defn = info["definition"]
        desc = clean_description(defn.get("description", ""))
        props = defn.get("properties", {})
        required = defn.get("required", [])

        lines.append(f"### {name}")
        lines.append("")
        if desc:
            lines.append(f"{desc}")
            lines.append("")

        lines.append(generate_fields_table(props, required, shared_types, for_datatype=True))
        lines.append("")

        # Used in
        if name in type_usage_map:
            msgs = type_usage_map[name]
            lines.append(f"**Used in:** {', '.join(msgs)}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_block_md(block_name, messages_in_block, message_registry, shared_types, local_types, type_usage_map):
    """Generate one OCPP-2.0.1-Schemas-{Block}.md file."""
    lines = []

    block_code = BLOCK_CODES.get(block_name, "")

    # Header
    lines.append(f"# OCPP 2.0.1 Schemas — {block_name}")
    lines.append("")
    lines.append(f"> **Functional Block:** {block_code}")
    lines.append(f">")
    lines.append(f"> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).")
    lines.append(f"> Types used only within this block are documented [inline below](#local-types).")
    lines.append("")

    # Table of contents
    lines.append("## Messages")
    lines.append("")
    for msg_name in messages_in_block:
        direction = DIRECTION_MAP.get(msg_name, "?")
        lines.append(f"- [{msg_name}](#{msg_name.lower()}) ({direction})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Collect local types for this block
    block_local_types = {}
    for msg_name in messages_in_block:
        msg = message_registry.get(msg_name, {})
        for side in ["request", "response"]:
            side_data = msg.get(side, {})
            for type_name in side_data.get("definitions", {}).keys():
                if type_name not in shared_types and type_name in local_types:
                    block_local_types[type_name] = local_types[type_name]

    # Messages
    for msg_name in messages_in_block:
        msg = message_registry.get(msg_name, {})
        direction = DIRECTION_MAP.get(msg_name, "?")

        lines.append(f"## {msg_name}")
        lines.append("")
        lines.append(f"**Direction:** {direction}")
        lines.append("")

        # Request
        req = msg.get("request", {})
        if req:
            lines.append(f"### {msg_name}Request")
            lines.append("")

            props = {k: v for k, v in req["properties"].items()}
            required = req["required"]

            lines.append(generate_fields_table(props, required, shared_types))
            lines.append("")

            # Example
            if required:
                example = generate_example_payload(
                    req["properties"], required, req.get("definitions", {}))
                lines.append("<details>")
                lines.append(f"<summary>Example {msg_name}Request</summary>")
                lines.append("")
                lines.append("```json")
                lines.append(example)
                lines.append("```")
                lines.append("")
                lines.append("</details>")
                lines.append("")

        # Response
        resp = msg.get("response", {})
        if resp:
            lines.append(f"### {msg_name}Response")
            lines.append("")

            props = {k: v for k, v in resp["properties"].items()}
            required = resp["required"]

            if not props or (len(props) == 1 and "customData" in props and not required):
                lines.append("*No required fields. An empty `{}` is a valid response.*")
                lines.append("")
            else:
                lines.append(generate_fields_table(props, required, shared_types))
                lines.append("")

                if not required:
                    lines.append("*No fields are required. An empty `{}` is a valid response.*")
                    lines.append("")

        lines.append("---")
        lines.append("")

    # Local types section
    if block_local_types:
        lines.append("## Local Types")
        lines.append("")
        lines.append("*Types used only within this block's messages.*")
        lines.append("")

        local_enums = {k: v for k, v in block_local_types.items() if v["is_enum"]}
        local_composites = {k: v for k, v in block_local_types.items() if not v["is_enum"]}

        for name in sorted(local_enums.keys()):
            info = local_enums[name]
            defn = info["definition"]
            desc = clean_description(defn.get("description", ""))

            lines.append(f"### {name}")
            lines.append("")
            if desc:
                lines.append(f"{desc}")
                lines.append("")

            default = defn.get("default")
            if default is not None:
                lines.append(f"**Default:** `{default}`")
                lines.append("")

            lines.append("| Value |")
            lines.append("|-------|")
            for val in defn["enum"]:
                lines.append(f"| `{val}` |")
            lines.append("")

            if name in type_usage_map:
                msgs = type_usage_map[name]
                lines.append(f"**Used in:** {', '.join(msgs)}")
                lines.append("")

            lines.append("---")
            lines.append("")

        for name in sorted(local_composites.keys()):
            info = local_composites[name]
            defn = info["definition"]
            desc = clean_description(defn.get("description", ""))
            props = defn.get("properties", {})
            required = defn.get("required", [])

            lines.append(f"### {name}")
            lines.append("")
            if desc:
                lines.append(f"{desc}")
                lines.append("")

            lines.append(generate_fields_table(props, required, shared_types, for_datatype=False))
            lines.append("")

            if name in type_usage_map:
                msgs = type_usage_map[name]
                lines.append(f"**Used in:** {', '.join(msgs)}")
                lines.append("")

            lines.append("---")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading schemas...")
    schemas = load_schemas()
    print(f"  Loaded {len(schemas)} schema files")

    print("Building type registry...")
    type_registry = build_type_registry(schemas)
    print(f"  Found {len(type_registry)} unique types")

    print("Building message registry...")
    message_registry = build_message_registry(schemas)
    print(f"  Found {len(message_registry)} messages")

    # Verify all messages in BLOCK_MAP exist
    all_block_messages = set()
    for msgs in BLOCK_MAP.values():
        all_block_messages.update(msgs)

    missing_from_blocks = set(message_registry.keys()) - all_block_messages
    missing_from_schemas = all_block_messages - set(message_registry.keys())

    if missing_from_blocks:
        print(f"  WARNING: Messages in schemas but not in BLOCK_MAP: {missing_from_blocks}", file=sys.stderr)
    if missing_from_schemas:
        print(f"  WARNING: Messages in BLOCK_MAP but not in schemas: {missing_from_schemas}", file=sys.stderr)

    print("Classifying types...")
    shared_types, local_types = classify_types(type_registry)
    print(f"  Shared (≥{SHARED_TYPE_THRESHOLD} files): {len(shared_types)}")
    print(f"  Local (<{SHARED_TYPE_THRESHOLD} files): {len(local_types)}")

    type_usage_map = build_type_usage_map(type_registry)

    # Generate DataTypes.md (at repo root)
    print("Generating OCPP-2.0.1-DataTypes.md...")
    datatypes_content = generate_datatypes_md(shared_types, type_usage_map)
    output_path = DATATYPES_OUTPUT_DIR / "OCPP-2.0.1-DataTypes.md"
    with open(output_path, "w") as f:
        f.write(datatypes_content)
    print(f"  Written to {output_path}")

    # Generate block files (in OCPP-2.0.1-Schemas/ subdirectory)
    SCHEMAS_OUTPUT_DIR.mkdir(exist_ok=True)
    for block_name, messages_in_block in BLOCK_MAP.items():
        print(f"Generating OCPP-2.0.1-Schemas-{block_name}.md...")
        content = generate_block_md(
            block_name, messages_in_block, message_registry,
            shared_types, local_types, type_usage_map)
        output_path = SCHEMAS_OUTPUT_DIR / f"OCPP-2.0.1-Schemas-{block_name}.md"
        with open(output_path, "w") as f:
            f.write(content)
        print(f"  Written to {output_path}")

    # Summary
    enum_count = sum(1 for v in shared_types.values() if v["is_enum"])
    composite_count = sum(1 for v in shared_types.values() if not v["is_enum"])
    print(f"\nDone! Generated 11 files:")
    print(f"  - OCPP-2.0.1-DataTypes.md ({enum_count} enums, {composite_count} composite types)")
    for block_name, msgs in BLOCK_MAP.items():
        print(f"  - OCPP-2.0.1-Schemas-{block_name}.md ({len(msgs)} messages)")


if __name__ == "__main__":
    main()
