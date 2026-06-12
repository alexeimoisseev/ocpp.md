# OCPP.md — Open Charge Point Protocol Reference

> A structured OCPP reference for AI agents and developers building EV charging infrastructure. Covers **OCPP 2.1**, **OCPP 2.0.1** and **OCPP 1.6J** with field-level message schemas, sequence diagrams, smart charging deep-dives, and explicit markers for every place the spec leaves a decision to you.
>
> Source on [GitHub](https://github.com/alexeimoisseev/ocpp.md).

---

## Why This Exists

OCPP specifications are hundreds of pages long and full of deliberate gaps — places where behavior depends on your hardware vendor, your business rules, or your grid operator's requirements. AI coding agents that rely on training data alone tend to fill those gaps with plausible-sounding defaults. Sometimes they're right. Often they're not, and you don't find out until production.

OCPP.md gives AI agents (and human developers) a structured reference that distinguishes between what the spec defines, what it intentionally leaves open, and what depends on your specific deployment. Every ambiguous area is marked with an **escalation marker** — the agent stops and asks you instead of guessing.

---

## Using with AI Agents

### Claude Code

Install as a plugin:

```
/plugin marketplace add https://github.com/alexeimoisseev/ocpp.md
/plugin install ocpp@ocpp
```

Then use `/ocpp <topic>` to load specific reference material, or just ask OCPP-related questions — the plugin activates automatically when it detects OCPP keywords in your code or prompts.

### Other Agents (Cursor, Windsurf, Copilot, etc.)

Clone the repository and point your agent at the `docs/` directory. See the [AI Agent Setup Guide](./ai-agent-setup/) for detailed instructions.

---

## OCPP 2.0.1

The current specification, recommended for all new deployments. 64 messages organized by Functional Block.

**Reference docs:**

- [OCPP 2.0.1 Overview & Architecture](./ocpp-2.0.1/) — Roles, device model, transport, message frame, all 64 messages
- [Shared Data Types](./ocpp-2.0.1/data-types/) — 34 enums and composite types used across messages

**Schemas (field-level, generated from OCA JSON schemas):**

- [Provisioning](./ocpp-2.0.1/schemas/provisioning/) — BootNotification, GetVariables, SetVariables, Reset, etc.
- [Authorization](./ocpp-2.0.1/schemas/authorization/) — Authorize, SendLocalList, ClearCache
- [Transactions](./ocpp-2.0.1/schemas/transactions/) — TransactionEvent, RequestStartTransaction, MeterValues
- [Smart Charging](./ocpp-2.0.1/schemas/smart-charging/) — SetChargingProfile, GetCompositeSchedule, etc.
- [Firmware](./ocpp-2.0.1/schemas/firmware/) — UpdateFirmware, FirmwareStatusNotification
- [Security](./ocpp-2.0.1/schemas/security/) — CertificateSigned, InstallCertificate, SecurityEventNotification
- [Diagnostics](./ocpp-2.0.1/schemas/diagnostics/) — GetLog, NotifyEvent, SetVariableMonitoring
- [Availability](./ocpp-2.0.1/schemas/availability/) — ChangeAvailability, StatusNotification, Heartbeat
- [Reservation](./ocpp-2.0.1/schemas/reservation/) — ReserveNow, CancelReservation
- [Display](./ocpp-2.0.1/schemas/display/) — SetDisplayMessage, CostUpdated

**Behavioral docs:**

- [Sequences](./ocpp-2.0.1/sequences/) — Boot, authorization, transaction lifecycle, offline replay
- [Sequences (Operational)](./ocpp-2.0.1/sequences/operational/) — Firmware updates, diagnostics, reset
- [Smart Charging Deep-Dive](./ocpp-2.0.1/smart-charging/) — Profile model, composite schedules, AC/DC differences
- [Smart Charging Examples](./ocpp-2.0.1/smart-charging/examples/) — Worked examples with full JSON payloads
- [Smart Charging & ISO 15118](./ocpp-2.0.1/smart-charging/iso15118/) — EV-side schedules, Plug & Charge integration
- [Charging Profile Generator](./ocpp-2.0.1/smart-charging/generator/) — Interactive tool to build SetChargingProfileRequest payloads

---

## OCPP 2.1

The latest specification (Edition 2, 2025). A structural superset of 2.0.1 — all 64 of its messages are retained plus 27 new ones, for **91 messages** across **19 functional blocks (A–S)**. Adds DER control, bidirectional power transfer (V2X), a first-class tariff & cost model, battery swapping, dynamic charging profiles, periodic event streams, and ISO 15118-20 support.

**Reference docs:**

- [OCPP 2.1 Overview & Migration](./ocpp-2.1/) — Roles, device model, all 91 messages by block, and the 2.0.1 → 2.1 migration guide
- [Shared Data Types](./ocpp-2.1/data-types/) — Enums and composite types used across messages
- [Device Model Reference](./ocpp-2.1/device-model/) — Standardized components and variables (82 components, 240 variables)
- [Standardized Enumerations](./ocpp-2.1/enumerations/) — Connector types, units, security events, reason codes, payment brands, etc.

**Schemas (field-level, generated from OCA JSON schemas):**

- [Security](./ocpp-2.1/schemas/security/) — SecurityEventNotification
- [Provisioning](./ocpp-2.1/schemas/provisioning/) — BootNotification, GetVariables, SetVariables, Reset
- [Authorization](./ocpp-2.1/schemas/authorization/) — Authorize, ClearCache
- [Local Auth List](./ocpp-2.1/schemas/local-auth-list/) — SendLocalList, GetLocalListVersion
- [Transactions](./ocpp-2.1/schemas/transactions/) — TransactionEvent, GetTransactionStatus
- [Remote Control](./ocpp-2.1/schemas/remote-control/) — RequestStartTransaction, UnlockConnector, TriggerMessage
- [Availability](./ocpp-2.1/schemas/availability/) — ChangeAvailability, StatusNotification
- [Reservation](./ocpp-2.1/schemas/reservation/) — ReserveNow, CancelReservation
- [Tariff & Cost](./ocpp-2.1/schemas/tariff-and-cost/) — GetTariffs, SetDefaultTariff, CostUpdated, NotifySettlement *(new in 2.1)*
- [Meter Values](./ocpp-2.1/schemas/meter-values/) — MeterValues
- [Smart Charging](./ocpp-2.1/schemas/smart-charging/) — SetChargingProfile, UpdateDynamicSchedule, UsePriorityCharging
- [Firmware](./ocpp-2.1/schemas/firmware/) — UpdateFirmware, PublishFirmware
- [Certificates](./ocpp-2.1/schemas/certificates/) — InstallCertificate, GetCertificateChainStatus
- [Diagnostics](./ocpp-2.1/schemas/diagnostics/) — NotifyEvent, GetLog, periodic event streams
- [Display](./ocpp-2.1/schemas/display/) — SetDisplayMessage
- [Data Transfer](./ocpp-2.1/schemas/data-transfer/) — DataTransfer
- [Bidirectional / V2X](./ocpp-2.1/schemas/bidirectional/) — NotifyAllowedEnergyTransfer, AFRRSignal *(new in 2.1)*
- [DER Control](./ocpp-2.1/schemas/der-control/) — SetDERControl, ReportDERControl, NotifyDERAlarm *(new in 2.1)*
- [Battery Swap](./ocpp-2.1/schemas/battery-swap/) — BatterySwap, RequestBatterySwap *(new in 2.1)*

**Behavioral & feature docs:**

- [DER Control Deep-Dive](./ocpp-2.1/der-control/) — Control types, curves/setpoints, Get/Set/Clear/Report flow, alarms
- [Bidirectional Power Transfer / V2X](./ocpp-2.1/bidirectional/) — Operation modes, setpoints, frequency support (AFRR), allowed energy transfer
- [Tariff, Cost & Payment](./ocpp-2.1/tariff-cost/) — Tariff structure, cost calculation, settlement, ad-hoc/web payment, VAT
- [Smart Charging Deltas](./ocpp-2.1/smart-charging/) — Dynamic schedules, priority charging, battery swap, periodic event streams
- [Sequences](./ocpp-2.1/sequences/) — DER setup, dynamic schedule loop, battery swap, web-payment, periodic event stream lifecycle
- [Use-Case Catalog](./ocpp-2.1/use-cases/) — All 177 Part 2 use cases (A–S) with messages and escalation flags
- [Certification Profiles](./ocpp-2.1/certification/) — Profile × functional-block matrix (non-normative summary)

---

## OCPP 1.6J

The most widely deployed version. 28 messages organized by Feature Profile. Uses JSON over WebSocket transport (the "J" suffix).

**Reference docs:**

- [OCPP 1.6J Overview & Architecture](./ocpp-1.6j/) — Roles, connector model, transport, all 28 messages, config keys, differences from 2.0.1

**Schemas (field-level, generated from OCA JSON schemas):**

- [Core](./ocpp-1.6j/schemas/core/) — BootNotification, Authorize, StartTransaction, StopTransaction, StatusNotification, etc. (16 messages)
- [Smart Charging](./ocpp-1.6j/schemas/smart-charging/) — SetChargingProfile, ClearChargingProfile, GetCompositeSchedule
- [Firmware](./ocpp-1.6j/schemas/firmware/) — UpdateFirmware, GetDiagnostics, status notifications
- [Local Auth List](./ocpp-1.6j/schemas/local-auth-list/) — SendLocalList, GetLocalListVersion
- [Reservation](./ocpp-1.6j/schemas/reservation/) — ReserveNow, CancelReservation
- [Remote Trigger](./ocpp-1.6j/schemas/remote-trigger/) — TriggerMessage

**Behavioral docs:**

- [Sequences](./ocpp-1.6j/sequences/) — Boot, authorization, transaction lifecycle, status reporting, offline behavior
- [Smart Charging Deep-Dive](./ocpp-1.6j/smart-charging/) — Profile purposes, stack levels, composite schedule, common pitfalls
- [Charging Profile Generator](./ocpp-1.6j/smart-charging/generator/) — Interactive tool to build SetChargingProfile.req payloads

---

## The Escalation Model

This is the core idea behind OCPP.md. Both OCPP specifications have areas where behavior is intentionally left to the implementer. Most AI agents treat these like any other requirement and quietly make something up. OCPP.md marks every such area so the agent knows to ask:

- **SPEC-SILENT** — The specification doesn't define this. You need to make a decision.
- **VENDOR-DEPENDENT** — Behavior varies by charging station hardware or firmware. Ask which hardware you're targeting.
- **POLICY-DEPENDENT** — Depends on business rules, site configuration, or grid operator requirements.

By default, the agent stops and asks. If you want it to pick reasonable defaults during prototyping, add this to your project configuration (e.g., `CLAUDE.md`):

```
For OCPP: use pragmatic escalation mode.
```

---

## About This Project

- **Source:** [github.com/alexeimoisseev/ocpp.md](https://github.com/alexeimoisseev/ocpp.md)
- **Methodology:** All schemas are mechanically extracted from official OCA JSON schemas. Behavioral docs are AI-authored with explicit confidence tiers. See [Methodology](./methodology/).
- **License:** Apache 2.0. Does not redistribute the official OCPP specification.
- **Disclaimer:** Non-normative documentation. Always verify against the official specification and your vendor's documentation. OCPP is a trademark of the Open Charge Alliance. This project is not affiliated with or endorsed by the OCA.
