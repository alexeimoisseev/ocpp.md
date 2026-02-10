---
name: ocpp
description: >
  OCPP 2.0.1 protocol reference for EV charging infrastructure development.
  Use when working with OCPP messages, charging station code, CSMS backends,
  smart charging, transaction handling, or EV charging protocols. Activates on
  keywords: OCPP, charging station, CSMS, EVSE, charging profile, BootNotification,
  TransactionEvent, SetChargingProfile, or any OCPP message name.
user-invocable: true
argument-hint: "[topic: smart-charging | authorize | transactions | schemas | sequences | ...]"
---

# OCPP 2.0.1 — AI Agent Reference

You are assisting a developer working on EV charging infrastructure using OCPP 2.0.1.
This skill gives you structured knowledge of the protocol. Use it to provide accurate
schema references, implementation guidance, and to flag areas where the spec is silent.

## Quick Reference

**What is OCPP:** Open Charge Point Protocol — communication between EV Charging Stations (CS) and a Charging Station Management System (CSMS) over WebSocket + JSON. The CS initiates the connection. Both sides can send messages. OCPP 2.0.1 is the current recommended version.

**Device Model:** Charging Station → EVSE(s) → Connector(s). `evseId` and `connectorId` are 1-indexed. `evseId=0` means the whole station.

**Message Frame:** JSON-RPC-like. Three types:
- `CALL` — `[2, messageId, action, payload]`
- `CALLRESULT` — `[3, messageId, payload]`
- `CALLERROR` — `[4, messageId, errorCode, errorDescription, errorDetails]`

## All 64 OCPP 2.0.1 Messages

### Provisioning & Lifecycle
- `BootNotification` (CS→CSMS) — Station registers on connect
- `Heartbeat` (CS→CSMS) — Keepalive
- `StatusNotification` (CS→CSMS) — Connector/EVSE status changes
- `GetVariables` (CSMS→CS) — Read configuration
- `SetVariables` (CSMS→CS) — Write configuration
- `GetBaseReport` (CSMS→CS) — Request full variable inventory
- `NotifyReport` (CS→CSMS) — Variable inventory response (paginated)
- `SetNetworkProfile` (CSMS→CS) — Configure network connection profiles
- `Reset` (CSMS→CS) — Reboot station

### Authorization
- `Authorize` (CS→CSMS) — Validate ID token
- `ClearCache` (CSMS→CS) — Clear authorization cache
- `SendLocalList` (CSMS→CS) — Push local auth list
- `GetLocalListVersion` (CSMS→CS) — Query local auth list version

### Transactions
- `TransactionEvent` (CS→CSMS) — Started/Updated/Ended events
- `RequestStartTransaction` (CSMS→CS) — Remote start
- `RequestStopTransaction` (CSMS→CS) — Remote stop
- `GetTransactionStatus` (CSMS→CS) — Query outstanding transaction messages
- `MeterValues` (CS→CSMS) — Send meter values outside transaction context

### Remote Control
- `TriggerMessage` (CSMS→CS) — Request CS to send a specific message
- `UnlockConnector` (CSMS→CS) — Physically unlock connector
- `ChangeAvailability` (CSMS→CS) — Set EVSE operative/inoperative

### Smart Charging
- `SetChargingProfile` (CSMS→CS) — Install charging profile
- `GetChargingProfiles` (CSMS→CS) — Query installed profiles
- `ClearChargingProfile` (CSMS→CS) — Remove profiles
- `ClearedChargingLimit` (CS→CSMS) — External limit cleared
- `NotifyChargingLimit` (CS→CSMS) — External limit notification
- `ReportChargingProfiles` (CS→CSMS) — Profile query response
- `GetCompositeSchedule` (CSMS→CS) — Calculate effective schedule
- `NotifyEVChargingSchedule` (CS→CSMS) — EV-proposed schedule (ISO 15118)
- `NotifyEVChargingNeeds` (CS→CSMS) — Report EV charging needs (ISO 15118)

### Firmware
- `UpdateFirmware` (CSMS→CS) — Trigger firmware update
- `FirmwareStatusNotification` (CS→CSMS) — Update progress
- `PublishFirmware` (CSMS→CS) — Make firmware available to local network
- `PublishFirmwareStatusNotification` (CS→CSMS) — Publish progress
- `UnpublishFirmware` (CSMS→CS) — Remove published firmware

### Security & Certificates
- `Get15118EVCertificate` (CS→CSMS) — EV certificate request
- `GetCertificateStatus` (CS→CSMS) — OCSP status check
- `SignCertificate` (CS→CSMS) — CSR for station certificate
- `CertificateSigned` (CSMS→CS) — Signed certificate delivery
- `InstallCertificate` (CSMS→CS) — Install CA certificate
- `DeleteCertificate` (CSMS→CS) — Remove certificate
- `GetInstalledCertificateIds` (CSMS→CS) — List installed certs
- `SecurityEventNotification` (CS→CSMS) — Report security-related event

### Diagnostics & Monitoring
- `GetLog` (CSMS→CS) — Request log upload
- `LogStatusNotification` (CS→CSMS) — Log upload progress
- `NotifyEvent` (CS→CSMS) — Component/variable events
- `SetMonitoringBase` (CSMS→CS) — Set monitoring baseline
- `SetVariableMonitoring` (CSMS→CS) — Configure variable monitors
- `SetMonitoringLevel` (CSMS→CS) — Set monitoring severity level
- `GetMonitoringReport` (CSMS→CS) — Query active monitors
- `ClearVariableMonitoring` (CSMS→CS) — Remove monitors
- `NotifyMonitoringReport` (CS→CSMS) — Monitor query response
- `CustomerInformation` (CSMS→CS) — Request customer data
- `NotifyCustomerInformation` (CS→CSMS) — Customer data response

### Display Messages
- `CostUpdated` (CSMS→CS) — Update displayed cost
- `SetDisplayMessage` (CSMS→CS) — Show message on display
- `GetDisplayMessages` (CSMS→CS) — Query displayed messages
- `ClearDisplayMessage` (CSMS→CS) — Remove displayed message
- `NotifyDisplayMessages` (CS→CSMS) — Display message query response

### Reservation
- `ReserveNow` (CSMS→CS) — Create reservation
- `CancelReservation` (CSMS→CS) — Cancel reservation
- `ReservationStatusUpdate` (CS→CSMS) — Reservation expired/removed

### Data Transfer
- `DataTransfer` (CS↔CSMS) — Bidirectional vendor extension

## Key Data Types

- **IdTokenType** — User identification (eMAID, RFID, etc.) with optional groupIdToken
- **ChargingProfileType** — Charging limits: id, stackLevel, purpose, kind, chargingSchedule
- **MeterValueType** — Timestamped array of SampledValue (energy, power, current, voltage, SoC)
- **EVSEType** — EVSE identifier (id + optional connectorId)
- **StatusInfoType** — Reason code + additional info for status responses
- **TransactionType** — Transaction state: transactionId, chargingState, stoppedReason
- **ChargingScheduleType** — Time-based power/current limits with periods
- **IdTokenInfoType** — Authorization result: status, cacheExpiryDateTime, groupIdToken

## Escalation Model

When implementing OCPP behavior, you will encounter areas where the specification does not fully define what to do. These are categorized as:

### SPEC-SILENT
The OCPP specification does not define behavior for this case. You MUST flag this to the developer. Do NOT silently pick a default.

### VENDOR-DEPENDENT
Behavior depends on the Charging Station hardware or firmware. Ask which hardware/firmware is targeted.

### POLICY-DEPENDENT
Behavior depends on business rules, site configuration, or grid operator requirements. Ask about the business/operational context.

### Escalation Strictness

Check the developer's project for escalation configuration. Look for this in CLAUDE.md or project config:

```
ocpp:
  escalation: strict | pragmatic
```

- **strict (default):** Stop and ask the developer before proceeding. Present specific options. Do not write code for the ambiguous area until answered.
- **pragmatic:** Flag the ambiguity but pick a reasonable default. Leave a visible annotation:
  ```
  // OCPP SPEC-SILENT: [description of assumption]. Verify this matches your requirements.
  ```

If no configuration is found, default to **strict**.

## Documentation File Map

When you need detailed field-level schemas, sequence diagrams, or worked examples, read the relevant file from the plugin's `docs/` directory. Use `${CLAUDE_PLUGIN_ROOT}` to resolve the path.

| Topic | File to read |
|-------|-------------|
| **All shared data types (enums + composites)** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-DataTypes.md` |
| **Authorization schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md` |
| **Availability schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Availability.md` |
| **Diagnostics schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md` |
| **Display schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Display.md` |
| **Firmware schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md` |
| **Provisioning schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md` |
| **Reservation schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md` |
| **Security schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Security.md` |
| **Smart Charging schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md` |
| **Transaction schemas** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md` |
| **Boot, auth, transaction sequences** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences.md` |
| **Offline, firmware, diagnostics sequences** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences-Operational.md` |
| **Smart Charging deep-dive** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md` |
| **Smart Charging worked examples** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-Examples.md` |
| **ISO 15118 + Smart Charging** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-ISO15118.md` |
| **OCPP overview + migration guide** | `${CLAUDE_PLUGIN_ROOT}/docs/OCPP-2.0.1.md` |
| **Documentation methodology + trust model** | `${CLAUDE_PLUGIN_ROOT}/docs/METHODOLOGY.md` |

### How to use the file map

1. Identify the topic from the developer's question
2. Read the relevant file(s) using the Read tool
3. Cite specific fields, constraints, and enum values from the docs
4. Flag any ESCALATE markers you encounter in the docs

### Topic argument routing

If invoked with `/ocpp <topic>`, immediately read the relevant files:

- `/ocpp smart-charging` → read all 3 SmartCharging files
- `/ocpp authorize` or `/ocpp authorization` → read Authorization schemas
- `/ocpp transactions` → read Transaction schemas + Sequences
- `/ocpp provisioning` or `/ocpp boot` → read Provisioning schemas + Sequences
- `/ocpp schemas` → read all Schema files
- `/ocpp sequences` → read both Sequence files
- `/ocpp types` or `/ocpp data-types` → read DataTypes
- `/ocpp firmware` → read Firmware schemas + Operational sequences
- `/ocpp diagnostics` → read Diagnostics schemas + Operational sequences
- `/ocpp reservation` → read Reservation schemas
- `/ocpp display` → read Display schemas
- `/ocpp security` or `/ocpp certificates` → read Security schemas
- `/ocpp availability` → read Availability schemas
- Any other topic → search across all docs using grep

## Behavioral Guidelines

1. **Always cite the source.** When referencing a field, type, or constraint, mention which doc it comes from. Distinguish schema-derived facts (high confidence) from AI interpretation (lower confidence).

2. **Respect the escalation model.** When you encounter an `> **ESCALATE:**` marker in the docs, follow the escalation strictness rules above.

3. **Assume 2.0.1 unless told otherwise.** If the developer doesn't specify an OCPP version, assume 2.0.1. If their code uses 1.6-style messages (e.g. `StartTransaction` instead of `TransactionEvent`), note the version mismatch and ask.

4. **Don't invent protocol behavior.** If you're unsure whether something is spec-defined, check the docs first. If the docs don't cover it, say so explicitly rather than guessing.

5. **Use the schemas for validation.** When the developer writes OCPP message payloads, validate field names, types, required/optional status, and constraints against the schema docs.
