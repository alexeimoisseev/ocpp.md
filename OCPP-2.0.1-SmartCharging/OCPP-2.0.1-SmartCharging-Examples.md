# OCPP 2.0.1 — Smart Charging Examples

> **Purpose:** Worked examples, realistic JSON payloads, and message flow sequences for OCPP 2.0.1 smart charging. Companion to the [Smart Charging Deep-Dive](./OCPP-2.0.1-SmartCharging.md).

> **Last updated:** 2026-02-07

---

## How This Document Was Produced

This document contains worked examples, JSON payloads, and message flow sequences for smart charging. Its dominant confidence tier is **interpretation** — these are illustrative examples, not normative. JSON payload structures and enum values are **schema-derived** (cross-referenced against the [schema documentation](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) and [data types reference](../OCPP-2.0.1-DataTypes.md)). Composite schedule calculation results represent an AI interpretation of the merging algorithm — the exact normative algorithm is in Part 2. Numeric values (voltages, currents, powers) are realistic but not prescriptive.

This document contains **1 escalation point** marked with `> **ESCALATE:**`. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

---

## 1. Composite Schedule Walkthroughs

### Example 1: Stack Level Resolution (Same Purpose)

**Scenario:** An office building CSMS sets two `TxDefaultProfile` profiles on EVSE 1 — a base limit and a peak-hours override.

**Profile A** — Base limit (low priority):
```json
{
  "id": 100,
  "stackLevel": 0,
  "chargingProfilePurpose": "TxDefaultProfile",
  "chargingProfileKind": "Recurring",
  "recurrencyKind": "Daily",
  "chargingSchedule": [{
    "id": 1,
    "chargingRateUnit": "A",
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 32.0 }
    ]
  }]
}
```

**Profile B** — Peak hours override (higher priority):
```json
{
  "id": 101,
  "stackLevel": 1,
  "chargingProfilePurpose": "TxDefaultProfile",
  "chargingProfileKind": "Recurring",
  "recurrencyKind": "Daily",
  "chargingSchedule": [{
    "id": 2,
    "chargingRateUnit": "A",
    "startSchedule": "2026-02-07T08:00:00Z",
    "duration": 36000,
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 16.0 }
    ]
  }]
}
```

**Resolution:**

Both profiles have the same purpose (`TxDefaultProfile`). Profile B has a higher `stackLevel` (1 > 0), so **Profile B takes precedence** during the hours it is active.

| Time | Active profile | Effective limit | Reasoning |
|------|---------------|----------------|-----------|
| 00:00–08:00 | A only (B not yet active for the day) | 32 A | Only Profile A covers this window |
| 08:00–18:00 | B (higher stackLevel wins) | 16 A | Profile B at stackLevel=1 overrides Profile A at stackLevel=0 |
| 18:00–00:00 | A only (B's duration expired) | 32 A | Profile B's 36000s duration ends at 18:00 |

> **ESCALATE: SPEC-SILENT** — Behavior when a higher-stackLevel profile's duration expires.
> This walkthrough assumes that when a higher-stackLevel profile's duration expires, the next-highest stackLevel profile takes effect. The specification does not make this fallback behavior fully explicit. An AI agent MUST NOT assume this behavior without confirmation. Ask the developer:
> 1. Does the target CS fall back to the next-highest stackLevel when a profile's duration expires?
> 2. Or does the expired profile leave a gap (no limit from that purpose) until a new profile is set?
> 3. Should the CSMS proactively send a replacement profile before the high-priority profile expires?

---

### Example 2: Purpose Hierarchy (Ceiling Effect)

**Scenario:** A depot with 150 kW grid connection has two active profiles on EVSE 1.

**Profile C** — Station-wide power cap:
```json
{
  "id": 200,
  "stackLevel": 0,
  "chargingProfilePurpose": "ChargingStationMaxProfile",
  "chargingProfileKind": "Absolute",
  "chargingSchedule": [{
    "id": 3,
    "chargingRateUnit": "W",
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 22000.0 }
    ]
  }]
}
```

**Profile D** — Transaction default:
```json
{
  "id": 201,
  "stackLevel": 0,
  "chargingProfilePurpose": "TxDefaultProfile",
  "chargingProfileKind": "Absolute",
  "chargingSchedule": [{
    "id": 4,
    "chargingRateUnit": "W",
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 50000.0 }
    ]
  }]
}
```

**Resolution:**

`ChargingStationMaxProfile` has higher priority than `TxDefaultProfile` and acts as a ceiling.

| Purpose | Limit | Role |
|---------|-------|------|
| `ChargingStationMaxProfile` (Profile C) | 22,000 W | Ceiling |
| `TxDefaultProfile` (Profile D) | 50,000 W | Requested |
| **Effective** | **22,000 W** | min(22000, 50000) |

The `TxDefaultProfile` requests 50 kW, but the station-wide cap limits it to 22 kW. The composite schedule shows 22,000 W.

---

### Example 3: External Constraint Mid-Transaction

**Scenario:** An EV is charging at EVSE 1 with a `TxProfile` of 32 A. The grid operator sends a constraint reducing the station to 20 A.

**Active profiles before the constraint:**

| Profile | Purpose | stackLevel | Limit |
|---------|---------|------------|-------|
| E | `TxProfile` | 0 | 32 A |

No `ChargingStationExternalConstraints` or `ChargingStationMaxProfile` active → effective limit is 32 A.

**Grid operator sends constraint (via CSMS):**
```json
{
  "id": 300,
  "stackLevel": 0,
  "chargingProfilePurpose": "ChargingStationExternalConstraints",
  "chargingProfileKind": "Absolute",
  "chargingSchedule": [{
    "id": 5,
    "chargingRateUnit": "A",
    "startSchedule": "2026-02-07T14:00:00Z",
    "duration": 7200,
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 20.0 }
    ]
  }]
}
```

**After the constraint is applied (14:00–16:00):**

| Purpose | Limit |
|---------|-------|
| `ChargingStationExternalConstraints` (Profile F) | 20 A |
| `TxProfile` (Profile E) | 32 A |
| **Effective** | **20 A** — min(20, 32) |

**After 16:00 (constraint expires):**

| Purpose | Limit |
|---------|-------|
| `TxProfile` (Profile E) | 32 A |
| **Effective** | **32 A** — no ceiling active |

The CS reduces the charging rate to 20 A at 14:00 and restores it to 32 A at 16:00 when the external constraint's duration expires.

---

## 2. Realistic JSON Payloads

### 2.1 SetChargingProfile — Daily Recurring TxDefaultProfile

An office building limits EV charging to 16 A during business hours and allows 32 A overnight.

```json
[2, "msg-001", "SetChargingProfile", {
  "evseId": 0,
  "chargingProfile": {
    "id": 1,
    "stackLevel": 0,
    "chargingProfilePurpose": "TxDefaultProfile",
    "chargingProfileKind": "Recurring",
    "recurrencyKind": "Daily",
    "chargingSchedule": [{
      "id": 1,
      "chargingRateUnit": "A",
      "startSchedule": "2026-02-07T00:00:00Z",
      "duration": 86400,
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 32.0, "numberPhases": 3 },
        { "startPeriod": 28800, "limit": 16.0, "numberPhases": 3 },
        { "startPeriod": 64800, "limit": 32.0, "numberPhases": 3 }
      ]
    }]
  }
}]
```

Breakdown of periods:
- 00:00–08:00 (0–28800s): 32 A × 3 phases × 230 V = 22.1 kW
- 08:00–18:00 (28800–64800s): 16 A × 3 phases × 230 V = 11.0 kW
- 18:00–00:00 (64800–86400s): 32 A × 3 phases × 230 V = 22.1 kW

**Response:**
```json
[3, "msg-001", {
  "status": "Accepted"
}]
```

Note: `evseId=0` with `TxDefaultProfile` applies this schedule to **each individual EVSE**.

### 2.2 SetChargingProfile — External Constraint from Grid Operator

A demand response event requires the station to reduce total draw to 50 kW for 2 hours.

```json
[2, "msg-002", "SetChargingProfile", {
  "evseId": 0,
  "chargingProfile": {
    "id": 50,
    "stackLevel": 0,
    "chargingProfilePurpose": "ChargingStationExternalConstraints",
    "chargingProfileKind": "Absolute",
    "chargingSchedule": [{
      "id": 50,
      "chargingRateUnit": "W",
      "startSchedule": "2026-02-07T14:00:00Z",
      "duration": 7200,
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 50000.0 }
      ]
    }]
  }
}]
```

Note: `evseId=0` with `ChargingStationExternalConstraints` sets an **overall station-wide limit**.

### 2.3 GetCompositeSchedule — Request and Response

CSMS asks EVSE 1 for its effective schedule for the next hour:

**Request:**
```json
[2, "msg-003", "GetCompositeSchedule", {
  "evseId": 1,
  "duration": 3600,
  "chargingRateUnit": "A"
}]
```

**Response** (with a profile change at the 1800-second mark):
```json
[3, "msg-003", {
  "status": "Accepted",
  "schedule": {
    "evseId": 1,
    "duration": 3600,
    "scheduleStart": "2026-02-07T14:00:00Z",
    "chargingRateUnit": "A",
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 16.0, "numberPhases": 3 },
      { "startPeriod": 1800, "limit": 32.0, "numberPhases": 3 }
    ]
  }
}]
```

This tells the CSMS: "For the next 30 minutes, EVSE 1 will charge at max 16 A/phase. After that, it will charge at max 32 A/phase for the remaining 30 minutes."

### 2.4 GetChargingProfiles and ReportChargingProfiles

CSMS queries all installed profiles on EVSE 1:

**Request:**
```json
[2, "msg-004", "GetChargingProfiles", {
  "requestId": 42,
  "evseId": 1,
  "chargingProfile": {}
}]
```

**Response (acknowledgment):**
```json
[3, "msg-004", {
  "status": "Accepted"
}]
```

**CS then sends profiles asynchronously** (one or more `ReportChargingProfiles` messages):

```json
[2, "msg-005", "ReportChargingProfiles", {
  "requestId": 42,
  "evseId": 1,
  "chargingLimitSource": "CSO",
  "tbc": false,
  "chargingProfile": [
    {
      "id": 1,
      "stackLevel": 0,
      "chargingProfilePurpose": "TxDefaultProfile",
      "chargingProfileKind": "Recurring",
      "recurrencyKind": "Daily",
      "chargingSchedule": [{
        "id": 1,
        "chargingRateUnit": "A",
        "startSchedule": "2026-02-07T00:00:00Z",
        "duration": 86400,
        "chargingSchedulePeriod": [
          { "startPeriod": 0, "limit": 32.0, "numberPhases": 3 },
          { "startPeriod": 28800, "limit": 16.0, "numberPhases": 3 },
          { "startPeriod": 64800, "limit": 32.0, "numberPhases": 3 }
        ]
      }]
    }
  ]
}]
```

When `tbc` (To Be Continued) is `false`, this is the last message in the report. If the CS has many profiles, it may send multiple `ReportChargingProfiles` messages with `tbc=true` for all but the last.

---

## 3. Message Flow Sequences

### 3.1 Profile Lifecycle: Set Default, Start Transaction, Override with TxProfile

1. CSMS sends `SetChargingProfile` to CS — `TxDefaultProfile`: 32A on EVSE 1.
2. CS responds `SetChargingProfileResponse` — status: `Accepted`.
3. User plugs in EV and authorizes.
4. CS sends `TransactionEvent(Started)` to CSMS — transaction T1 begins, charging at 32A.
5. CSMS sends `SetChargingProfile` to CS — `TxProfile` for T1: 16A (demand response override).
6. CS responds `SetChargingProfileResponse` — status: `Accepted`.
7. CS sends `TransactionEvent(Updated, triggerReason=ChargingRateChanged)` to CSMS — CS now charging at 16A.
8. CSMS sends `ClearChargingProfile` to CS — remove the TxProfile.
9. CS responds `ClearChargingProfileResponse` — status: `Accepted`.
10. CS reverts to TxDefault: 32A.
11. CS sends `TransactionEvent(Updated, triggerReason=ChargingRateChanged)` to CSMS — back to 32A.

### 3.2 Grid Constraint Mid-Transaction

Three actors: CSMS, CS, and Grid/EMS (building energy management system).

1. CS sends `TransactionEvent(Started)` to CSMS — charging at 32A.
2. [Grid/EMS] sends external limit to CS — 20A via local EMS interface (e.g., Modbus, EEBUS).
3. CS installs `ChargingStationExternalConstraints` profile locally.
4. CS recomputes composite schedule: min(32, 20) = 20A.
5. CS sends `NotifyChargingLimit` to CSMS — source=`EMS`, `isGridCritical=true`.
6. CS sends `TransactionEvent(Updated, triggerReason=ChargingRateChanged)` to CSMS — now 20A.
7. [Later] Grid/EMS clears the constraint.
8. CS removes the `ExternalConstraints` profile.
9. CS sends `ClearedChargingLimit` to CSMS — source=`EMS`.
10. CS sends `TransactionEvent(Updated, triggerReason=ChargingRateChanged)` to CSMS — back to 32A.

### 3.3 GetCompositeSchedule Usage

1. CSMS sends `SetChargingProfile` to CS — `TxDefaultProfile`: 32A.
2. CS responds `SetChargingProfileResponse` — status: `Accepted`.
3. CSMS sends `SetChargingProfile` to CS — `ChargingStationMaxProfile`: 22kW.
4. CS responds `SetChargingProfileResponse` — status: `Accepted`.
5. CSMS sends `GetCompositeSchedule` to CS — `evseId=1`, `duration=3600`, `chargingRateUnit=W`.
6. CS computes the merged schedule (applying purpose hierarchy: min of StationMax and TxDefault).
7. CS responds `GetCompositeScheduleResponse` — status: `Accepted`, with the merged schedule periods.
8. CSMS inspects the composite to verify the effective limits are as expected.

### 3.4 GetChargingProfiles with Pagination

1. CSMS sends `GetChargingProfiles` to CS — `requestId=42`, `evseId` omitted (query all EVSEs).
2. CS responds `GetChargingProfilesResponse` — status: `Accepted` (profiles will follow asynchronously).
3. CS sends `ReportChargingProfiles` to CSMS — `requestId=42`, `tbc=true` (more batches coming).
4. CSMS responds `ReportChargingProfilesResponse`.
5. CS sends `ReportChargingProfiles` to CSMS — `requestId=42`, `tbc=true`.
6. CSMS responds `ReportChargingProfilesResponse`.
7. CS sends `ReportChargingProfiles` to CSMS — `requestId=42`, `tbc=false` (last batch).
8. CSMS responds `ReportChargingProfilesResponse`.

The `tbc` (To Be Continued) field defaults to `false`. When `true`, the CSMS should expect more messages with the same `requestId`.

---

*This document is a community reference for AI agents. Examples are illustrative and may not cover all edge cases. For the authoritative specification, refer to the official OCPP 2.0.1 documents from OCA.*
