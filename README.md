# OCPP 2.0.1 — AI-Friendly Implementation Reference

This repository contains **non-normative, developer-oriented documentation** for **OCPP 2.0.1**, designed primarily to help **AI coding agents and developers** implement, debug, and reason about OCPP behavior correctly.

The focus is on:
- Clear structural references derived from official OCA JSON schemas
- Practical implementation guidance where the specification is complex
- Explicit identification of **spec-silent and implementation-dependent areas**
- Guardrails to prevent incorrect assumptions by automated coding tools

This repository is **not** a replacement for the official OCPP specification.

---

## Scope & Goals

**What this repository is:**
- A structured, AI-friendly reference for OCPP 2.0.1
- A bridge between formal schemas and real-world implementations
- An explicit guide to where developer decisions are required
- Suitable for humans *and* autonomous coding agents

**What this repository is not:**
- Not an official OCPP specification
- Not normative or authoritative
- Not affiliated with the Open Charge Alliance (OCA)
- Not a complete legal or compliance reference

For authoritative definitions, always refer to the official OCPP 2.0.1 documents published by the Open Charge Alliance.

---

## Repository Structure

### 1. Data Types Reference

#### `OCPP-2.0.1-DataTypes.md`

Complete reference of all reusable OCPP 2.0.1 data types, including:
- 16 enums
- 18 composite types

Examples:
- `IdTokenType`
- `ChargingProfileType`
- `MeterValueType`
- `StatusInfoType`
- `EVSEType`

This document is **generated from official OCA JSON schemas** and reorganized into a human- and AI-readable format.

---

### 2. Message Schemas (Field-Level)

#### `OCPP-2.0.1-Schemas/`

Field-level schemas for **all 64 OCPP 2.0.1 messages**, split by functional block:

- Provisioning  
- Authorization  
- Transactions  
- Smart Charging  
- Firmware  
- Security  
- Diagnostics  
- Availability  
- Reservation  
- Display  

Each message documents:
- All fields
- Types
- Required vs optional status
- Constraints

These files are **generated from official OCA JSON schemas** and are intended as a **developer convenience reference**.

---

### 3. Smart Charging Deep-Dive

#### `OCPP-2.0.1-SmartCharging/`

AI-authored documentation focusing on the most complex part of OCPP.

- `OCPP-2.0.1-SmartCharging.md`  
  Charging profiles, purposes, stack levels, validity windows, composite schedule concepts, AC vs DC differences, external constraints, and common pitfalls.

- `OCPP-2.0.1-SmartCharging-Examples.md`  
  Worked composite schedule walkthroughs, realistic CALL / CALLRESULT payloads, ASCII sequence diagrams.

- `OCPP-2.0.1-SmartCharging-ISO15118.md`  
  EV charging needs, EV-proposed schedules, AC/DC parameters, and sales tariffs.

These documents explicitly distinguish between:
- **Spec-defined behavior**
- **Spec-silent behavior**
- **Vendor-dependent behavior**
- **Policy-dependent behavior**

---

### 4. Multi-Message Sequences

#### `OCPP-2.0.1-Sequences/`

AI-authored sequence diagrams covering real-world flows:

- `OCPP-2.0.1-Sequences.md`  
  Boot process, authorization flows, transaction lifecycle, meter values, state machines.

- `OCPP-2.0.1-Sequences-Operational.md`  
  Offline queueing and replay, reconnection backoff, firmware updates, diagnostics upload, pagination flows.

---

### 5. AI Agent Guardrails

This repository includes explicit **AI agent guardrails** that define:
- Where automated implementation is safe
- Where escalation to a human developer is mandatory
- How agents should pause and request clarification in ambiguous cases

These guardrails are intentional and critical to correctness.

---

## Intended Audience

- Developers implementing OCPP 2.0.1 CSMS or Charging Station software
- Engineers debugging interoperability issues
- Teams building tooling, simulators, or emulators
- AI coding agents working under developer supervision

---

## Using with AI Coding Agents

This repository is available as a **Claude Code plugin**:

```
/plugin marketplace add https://github.com/alexeimoisseev/ocpp.md
/plugin install ocpp-md@ocpp-md
```

See the [AI Agent Setup guide](https://ocpp.md/ai-agent-setup/) for configuration options and usage details.

---

## License

This repository is licensed under the **Apache License, Version 2.0**.

The license applies to the **original documentation, structure, diagrams, and explanations** contained here.

This repository:
- Does **not** redistribute the official OCPP specification
- Does **not** relicense OCPP or OCA intellectual property

OCPP® is a trademark of the Open Charge Alliance.  
This project is **not affiliated with or endorsed by the OCA**.

See the `LICENSE` file for details.

---

## Disclaimer

This is **non-normative documentation**.

While care has been taken to ensure accuracy, implementation details may vary by:
- Charging Station hardware
- Firmware capabilities
- Local grid and regulatory requirements
- Business and operational policy

Always verify behavior against:
- The official OCPP 2.0.1 specification
- The Open Charge Alliance Compliance Testing Tool (OCTT)
- Vendor documentation

---

## Contributions

Contributions are welcome if they:
- Improve clarity
- Fix factual errors
- Add examples
- Better distinguish spec-defined vs implementation-dependent behavior

All contributions must remain **non-normative** and **original**.

---

## Final Note

This repository exists to reduce ambiguity — not to hide it.

Where the OCPP specification is silent, this documentation makes that silence explicit
and requires human decisions rather than assumptions.

That is a feature, not a limitation.
