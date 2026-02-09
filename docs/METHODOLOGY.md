# How the Documentation Was Produced

This document explains how the OCPP 2.0.1 reference files were produced, what guarantees they carry, and where they might fall short. There are two categories of documentation with **different trust models**:

1. **Mechanically generated** — schema reference files extracted from OCA JSON schemas by a Python script. High confidence, verifiable.
2. **AI-authored** — deep-dive documents written by an AI model (Claude, Anthropic) from training data knowledge. Contains verifiable schema-derived facts alongside spec-knowledge that should be verified against the official specification.

---

# Part 1: Schema Documentation (Mechanically Generated)

## Source Material

The sole input is the **official OCA JSON Schema files** for OCPP 2.0.1 FINAL — 128 files (64 request/response pairs) published by the Open Charge Alliance alongside the specification. These are the same schemas that vendors use for message validation in production OCPP implementations.

**The schema files are not bundled with this repository.** To regenerate or verify the documentation, download the official OCPP 2.0.1 JSON schemas from the [Open Charge Alliance](https://openchargealliance.org) (free registration required) and place them in `OCPP-2.0.1_JSON_schemas/`.

## Generation Process

A Python script (`scripts/extract_schemas.py`) performs a deterministic, fully automated extraction:

1. **Parse** — Every `.json` schema file is loaded and parsed.
2. **Deduplicate types** — OCA schemas are self-contained: each file embeds all types it uses in a local `definitions` section. The same type (e.g., `IdTokenType`) appears identically in 10+ files. The script collects all 143 unique type definitions, groups them by name, and verifies identity across files.
3. **Classify** — Types appearing in 3 or more schema files are placed in `OCPP-2.0.1-DataTypes.md` as shared types. Types appearing in only 1-2 files are documented inline in the relevant functional block file as "Local Types."
4. **Extract message schemas** — For each of the 64 messages, the script extracts the top-level `properties` and `required` arrays from both the Request and Response schemas.
5. **Clean descriptions** — OCA schema descriptions contain internal metadata (URN identifiers, field-path prefixes, HTML entities, spec cross-references like `<<ref-RFC5646,[RFC5646]>>`). The script strips these to produce clean, readable text.
6. **Generate markdown** — Tables, cross-reference links, and example payloads are generated programmatically.

**No manual editing** is applied to the generated files. Every field name, type, required/optional status, enum value, and constraint comes directly from the JSON schema files.

## What Was Verified

- **All 64 messages** are accounted for — no message is missing, no message appears in more than one block file.
- **Type identity** — All 143 types were compared across every file where they appear. 12 types have minor description differences between files (contextual wording); all enum values are identical everywhere. The script picks the longest (most informative) description.
- **Field completeness** — Spot-checked against raw JSON schemas for TransactionEvent, SetChargingProfile, BootNotification, Authorize, GetVariables, NotifyReport, and others. All fields, required markings, and constraints match.
- **Cross-references** — All markdown links between DataTypes and block files resolve to valid anchors.

## What Is Accurate (High Confidence)

These elements are extracted mechanically from the JSON schemas with no interpretation:

- **Field names** — Exact match to schema `properties` keys.
- **Data types** — `string`, `integer`, `number`, `boolean`, `array`, `object` — taken directly from schema `type` fields.
- **Required vs. optional** — Taken directly from schema `required` arrays. If a field is not in the array, it's optional.
- **Enum values** — Taken directly from schema `enum` arrays. Complete and in original order.
- **String constraints** — `maxLength`, `minLength` taken directly from schema fields.
- **Array constraints** — `minItems`, `maxItems` taken directly from schema fields.
- **Numeric constraints** — `minimum`, `maximum` taken directly from schema fields.
- **Default values** — Taken from schema `default` fields where present.
- **Date-time format** — Indicated where schema specifies `"format": "date-time"`.

## What Is NOT Covered

These aspects of OCPP 2.0.1 are defined in the prose specification (Part 2), not in the JSON schemas, and are therefore **not present** in the generated documentation:

- **Semantic validation rules** — For example, "evseId SHALL be > 0" or "SHALL only be included if ChargingProfilePurpose is set to TxProfile" appear in description text but are not enforced by the JSON schema structure. Some of these survive in the cleaned descriptions, but not all.
- **Cross-field dependencies** — Conditional requirements like "field X is required when field Y has value Z" are not expressible in JSON Schema draft-06. The schemas only define unconditional required/optional status.
- **Message sequencing rules** — Which messages must come before others, retry behavior, timing constraints.
- **Business logic** — How composite schedules are calculated, how stack levels interact, offline authorization rules.
- **Errata and implementation notes** — The OCA publishes errata and implementation guides separately.

## Known Limitations

### Description cleanup may be imperfect

The OCA schema descriptions embed internal metadata in a semi-structured format. The cleanup regexes handle all patterns observed in the current schema set, but an OCA schema update could introduce new patterns that aren't caught. Symptoms would be stray URN identifiers or field-path prefixes in description text.

### Descriptions contain original typos from the OCA schemas

Where the OCA schema has a typo (e.g., "This inludes" instead of "This includes"), the generated documentation preserves it. This is intentional — the output faithfully represents the source.

### The ≥3 file threshold for shared types is a heuristic

Types appearing in 3+ schema files go to DataTypes.md; fewer go inline. This is a readability tradeoff, not an OCA distinction. A type like `ConnectorEnumType` (used only by `ReserveNow`) is documented inline in the Reservation block file rather than in DataTypes. If you're looking for a type and don't find it in DataTypes.md, check the Local Types section of the relevant block file.

### Message direction and functional block assignment are manually mapped

The JSON schemas do not encode whether a message is CS-to-CSMS or CSMS-to-CS, nor which functional block it belongs to. These are hardcoded in the script based on the OCPP 2.0.1 specification tables. An error here would mean a message shows the wrong direction label, but would not affect any field/type data.

### Example payloads are minimal, not realistic

The auto-generated examples include only required fields with placeholder values. They are syntactically valid against the schema but don't represent realistic charging scenarios. Use them as structural templates, not as test fixtures.

### OCPP 2.0.1 errata are not reflected

If the OCA has published errata that correct the JSON schemas, those corrections are only reflected here if the schema files in `OCPP-2.0.1_JSON_schemas/` are updated and the script is re-run.

### CustomDataType is documented but not useful for most agents

Every message and every type includes an optional `customData` field for vendor extensions. It's always the same structure (`vendorId: string, maxLength 255`). It's listed last in every table to minimize noise.

## How to Regenerate

1. Download the official OCPP 2.0.1 JSON schemas from [openchargealliance.org](https://openchargealliance.org) (free registration required).
2. Place all `*Request.json` and `*Response.json` files in `OCPP-2.0.1_JSON_schemas/`.
3. Run:

```
python3 scripts/extract_schemas.py
```

This overwrites `OCPP-2.0.1-DataTypes.md` and all files in `OCPP-2.0.1-Schemas/`. The script is idempotent — running it twice on the same input produces identical output.

## Relationship to Official OCA Documents

| This project | Official OCA |
|---|---|
| `OCPP-2.0.1_JSON_schemas/*.json` | Not bundled — download from OCA and place here to regenerate |
| `OCPP-2.0.1-DataTypes.md` | Mechanically extracted from the above |
| `OCPP-2.0.1-Schemas/*.md` | Mechanically extracted from the above |
| `OCPP-2.0.1.md` | Community summary — accurate but not exhaustive |
| Field names, types, enums, constraints | Exact match to OCA schemas |
| Descriptions | Cleaned version of OCA schema descriptions (metadata stripped) |
| Message direction, block assignments | From the spec, manually mapped |
| Semantic rules, sequencing, business logic | NOT included — read the spec for these |

The generated documentation is a **faithful reformatting** of the official schemas into a readable reference. It does not add, remove, or alter any structural information. Where the OCA schema is the single source of truth, this documentation matches it exactly.

---

# Part 2: AI-Authored Reference Documents

The following documents were authored by an AI model (Claude, Anthropic) to provide semantic understanding that goes beyond what the JSON schemas encode — algorithms, behavioral rules, implementation guidance, and worked examples.

## Files

| File | Purpose |
|------|---------|
| `OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md` | Smart charging concepts: profile model, composite schedules, AC/DC differences, grid integration, pitfalls |
| `OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-Examples.md` | Worked composite schedule calculations, realistic JSON payloads, message flow sequences |
| `OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-ISO15118.md` | ISO 15118 EV charging needs, EV-proposed schedules, sales tariffs |
| `OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences.md` | Core message sequences: boot, authorization, transaction lifecycle |
| `OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences-Operational.md` | Operational sequences: reservations, offline queueing, firmware updates, report pagination |

## How These Were Produced

These documents were written by Claude (Anthropic) in a collaborative session with the repository maintainer. The AI model used its training data knowledge of the OCPP 2.0.1 specification to author the content. **No automated extraction from schema files was involved** — the content is editorial, not mechanical.

## Information Tiers

Every claim in the AI-authored documents falls into one of four confidence tiers:

| Tier | Source | Confidence | How to verify |
|------|--------|------------|---------------|
| **Schema-derived** | Field names, types, enum values, constraints taken from JSON schemas | **High** — verifiable against `OCPP-2.0.1-Schemas/*.md` and `OCPP-2.0.1-DataTypes.md` | Compare against the mechanically generated schema docs in this repo |
| **Schema-described** | Behavioral rules quoted from OCA schema description fields (e.g., "Higher values have precedence") | **High** — directly from OCA text | Check the schema description in the relevant schema file |
| **Spec-knowledge** | Rules from the OCPP 2.0.1 specification Part 2, known to the AI model from training data | **Medium** — likely correct but not verifiable from this repo | Verify against the official OCPP 2.0.1 specification (available from [OCA](https://openchargealliance.org)) |
| **Interpretation** | Synthesis, worked examples, "common pitfalls," sequence diagrams | **Lower** — could contain errors | Treat as guidance, not as normative. Test against your implementation |

Each document has a "How This Document Was Produced" section at the top that identifies which tiers it primarily contains.

## Escalation Points

Some areas of the OCPP specification are ambiguous, silent, vendor-dependent, or policy-dependent. AI coding agents must not silently pick defaults in these areas — doing so produces bugs that are hard to detect and hard to trace back to the assumption.

The AI-authored documents use **inline escalation markers** to flag these areas. The format is:

```
> **ESCALATE: CATEGORY** — [What is ambiguous or unspecified].
> An AI agent MUST NOT choose a default here. Ask the developer:
> 1. Option A
> 2. Option B
> 3. Option C
```

Three escalation categories are used:

| Category | When used | Agent action |
|----------|-----------|-------------|
| **SPEC-SILENT** | The OCPP specification does not define behavior for this case | Agent MUST ask the developer to specify the desired behavior |
| **VENDOR-DEPENDENT** | Behavior depends on the Charging Station hardware or firmware | Agent MUST ask which hardware/firmware is targeted |
| **POLICY-DEPENDENT** | Behavior depends on business rules, site configuration, or grid operator requirements | Agent MUST ask about the business/operational requirements |

Content that is **SPEC-DEFINED** (the specification clearly mandates the behavior) needs no escalation marker — the agent can implement it directly.

The rationale for this escalation model is documented in [HUMAN_INTERVENTION.md](./HUMAN_INTERVENTION.md).

## What Is Accurate

- **All enum values, field names, type names, and constraints** match the mechanically generated schema documentation. These were cross-referenced during authoring.
- **Behavioral rules quoted from schema descriptions** (e.g., stackLevel precedence, validFrom/validTo semantics, evseId=0 behavior per purpose) are taken directly from OCA schema description text.

## What May Contain Errors

- **The composite schedule calculation approach** — the general principles (purpose hierarchy as ceilings, higher stackLevel wins within same purpose, min() across purposes) are widely accepted, but the exact normative algorithm is defined in Part 2 of the specification. Edge cases (gaps between profiles, duration behavior at boundaries, rate unit conversion with varying voltage) may differ from the description.
- **Worked examples** — the JSON payloads use correct field structures, but the calculated composite schedule results represent the AI's understanding of the merging algorithm, which may not match the normative algorithm in all edge cases.
- **Sequence diagrams** — show typical message flows, not every possible variation or error path.
- **"Common pitfalls" lists** — based on the AI model's training data. May miss real-world issues or include issues that are not universal.
- **Configuration variable names** — taken from the specification via AI training data. Variable availability depends on the CS implementation and firmware version.

## What Is NOT Covered

- **The exact normative algorithm text** from Part 2 of the specification. The documents describe the general approach, not the step-by-step normative text.
- **OCPP 2.0.1 errata** that may have been published after the AI model's training data cutoff.
- **Vendor-specific behavior** — different CS vendors may interpret specification ambiguities differently.
- **ISO 15118 protocol details** — the documents cover how ISO 15118 data flows through OCPP messages, not the ISO 15118 protocol itself.
- **OCTT compliance test cases** — for certification testing, consult the OCA directly.

## Relationship to Official Documents

| This project (AI-authored) | Official source |
|---|---|
| Profile model, composite schedule approach | OCPP 2.0.1 Part 2 (from OCA) |
| Enum values, field names used in text | OCA JSON schemas (verified against mechanically generated docs in this repo) |
| Behavioral rules quoted from descriptions | OCA JSON schema description fields |
| ISO 15118 interaction descriptions | OCPP 2.0.1 Part 2 + ISO 15118-2 |
| Worked examples and pitfalls | AI-generated guidance (not from any official source) |

**The official OCA specification is the authoritative source for all OCPP behavior.** These AI-authored documents are a practical reference to accelerate understanding, not a replacement for the specification.
