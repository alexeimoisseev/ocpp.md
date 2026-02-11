# OCPP 1.6J — Smart Charging Deep-Dive

> **Purpose:** Practical reference for AI agents implementing or debugging OCPP 1.6J smart charging. Covers the charging profile model, profile purposes, stack levels, composite schedule calculation, schedule kinds, and common pitfalls.

> **Last updated:** 2026-02-11

---

## How This Document Was Produced

This document is an AI-authored deep-dive into OCPP 1.6 Edition 2 Smart Charging, derived from specification section 3.13 (pages 20-29) and related sections (5.7, 5.16, 7.9-7.14, 9.4). Its dominant confidence tier is **spec-knowledge** — behavioral rules from the OCPP 1.6 specification known via AI training data and cross-referenced against the extracted spec text. The "Common Pitfalls" section (SS7) is **interpretation** — guidance based on AI training data and field experience, not normative text.

This document contains **4 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

---

## 1. Overview

Smart Charging allows a Central System to influence the charging power or current of a specific EV, or the total allowed energy consumption on an entire Charge Point. The Central System does this by sending **Charging Profiles** — schedules that define power or current limits at specific points in time.

Three messages make up the Smart Charging functional block:

| Message | Direction | Purpose |
|---------|-----------|---------|
| `SetChargingProfile` | Central System -> Charge Point | Install or update a charging profile on a connector |
| `ClearChargingProfile` | Central System -> Charge Point | Remove one or more charging profiles |
| `GetCompositeSchedule` | Central System -> Charge Point | Request the effective merged schedule for a connector |

Smart Charging is part of the "Smart Charging" feature profile. A Charge Point that supports this profile SHALL implement all three messages and report its capabilities via the configuration keys listed in SS8.

---

## 2. Charging Profile Structure

A Charging Profile is the core data structure. It contains a schedule of power/current limits along with metadata that determines when and how the schedule applies.

```
ChargingProfile: chargingProfileId (int), stackLevel (int ≥ 0), chargingProfilePurpose (ChargePointMaxProfile|TxDefaultProfile|TxProfile), chargingProfileKind (Absolute|Recurring|Relative), recurrencyKind? (Daily|Weekly, Recurring only), validFrom? (dateTime), validTo? (dateTime), transactionId? (int, required for TxProfile)
  └─ chargingSchedule: chargingRateUnit (A|W), duration? (int, seconds), startSchedule? (dateTime, Absolute/Recurring), minChargingRate? (decimal)
       └─ chargingSchedulePeriod[]: startPeriod (int, seconds from schedule start), limit (decimal, W or A), numberPhases? (int, default 3)
```

**Key structural differences from OCPP 2.0.1:**
- Only ONE `chargingSchedule` per profile (2.0.1 allows up to 3).
- No `ChargingStationExternalConstraints` purpose (added in 2.0.1).
- No `ChargingStationMaxProfile` — the equivalent is `ChargePointMaxProfile`.
- The `transactionId` is an integer (2.0.1 uses a string).
- Profiles are set per `connectorId`, not per `evseId`.

---

## 3. The Three Profile Purposes

Each profile has a `chargingProfilePurpose` that determines its role, scope, and how it interacts with other profiles.

### 3.1 ChargePointMaxProfile

Sets the maximum power or current for the **entire Charge Point** (all connectors combined).

- Can ONLY be set on `connectorId=0`.
- Used for load balancing at the grid connection level.
- Acts as a hard ceiling — the combined energy flow of all connectors SHALL NOT exceed this limit.

**Example use case:** The Charge Point is connected to a 32A fuse. Set a `ChargePointMaxProfile` with `limit=32` (Amps) to ensure the total draw across all connectors never exceeds 32A.

### 3.2 TxDefaultProfile

Default charging schedule applied to **new transactions**.

- Can be set on `connectorId=0` (applies to ALL connectors) or on a specific connector.
- If set on connector 0 AND a specific connector, the specific connector's profile overrides the connector-0 default **for that connector only**. Other connectors still use the connector-0 default.
- Persists across transactions — it is the "standing order" for how new sessions should charge.

**Example use case:** Prevent charging during daytime peak hours by setting a recurring TxDefaultProfile that limits power between 08:00 and 20:00.

### 3.3 TxProfile

Transaction-specific profile that overrides TxDefaultProfile for the **current transaction only**.

- Can ONLY be set on `connectorId > 0` (a specific connector with an active transaction).
- If there is no active transaction on the specified connector, the Charge Point SHALL discard the profile and return an error status in `SetChargingProfile.conf`.
- The profile SHOULD be deleted after the transaction ends.
- The Central System SHALL include the `transactionId` in the `SetChargingProfile.req` to prevent mismatch between transactions and profiles.

**Example use case:** The Central System receives a capacity forecast mid-transaction and needs to limit this specific EV to 16A for the next 2 hours.

### 3.4 SetChargingProfile Rejection Conditions

`SetChargingProfile.conf` returns one of: `Accepted`, `Rejected`, `NotSupported`.

The Charge Point SHALL reject a profile when:

| Condition | Reason |
|-----------|--------|
| `TxProfile` on a connector with no active transaction | No transaction to apply the profile to |
| `ChargePointMaxProfile` on `connectorId > 0` | This purpose is only valid on connectorId=0 |
| `TxProfile` on `connectorId=0` | TxProfile must target a specific connector |
| `stackLevel` exceeds `ChargeProfileMaxStackLevel` | Hardware limit exceeded |
| Schedule has more periods than `ChargingScheduleMaxPeriods` | Hardware limit exceeded |
| Total installed profiles would exceed `MaxChargingProfilesInstalled` | Storage limit exceeded (unless replacing an existing profile at the same stackLevel + purpose) |
| `transactionId` in profile does not match the active transaction on the connector | Transaction mismatch — prevents stale profiles from applying to a different session |

`NotSupported` is returned if the Charge Point does not support the Smart Charging feature profile.

---

## 4. Stack Levels

Multiple profiles of the **same purpose** can coexist on a Charge Point by using different `stackLevel` values. This allows building complex charging calendars from layered rules.

**Precedence rule:** At any point in time, the prevailing profile is the one with the **highest `stackLevel`** among profiles that are valid at that moment (as determined by `validFrom`/`validTo` and `duration`).

**Replacement rule:** Multiple profiles with the same `stackLevel` AND the same `chargingProfilePurpose` are not allowed. If the Charge Point receives a new profile matching an existing one on both fields, the new profile SHALL replace the old one.

**Example — layered TxDefaultProfiles:**

```
stackLevel=0: Weekly recurring profile, allows 32A on weekdays 23:00-06:00,
              full power on weekends, 16A at other times
stackLevel=1: Holiday override, valid Dec 24-26, allows 32A all day
```

When December 25 arrives, the stackLevel=1 profile is valid and takes precedence. On a normal Tuesday at 10:00, only stackLevel=0 is valid, so the 16A limit applies.

### Stack Level Warnings

> **WARNING:** If an updated profile (same stackLevel and purpose) is sent with a `validFrom` in the future, the Charge Point SHALL replace the installed profile immediately — but the new profile is not active until `validFrom`. This creates a **gap** where no profile of that purpose/stackLevel is active. The spec RECOMMENDS providing a `validFrom` in the past to prevent gaps.

> **WARNING:** If you use stacking without a `duration` on the highest stack level, the Charge Point will **never** fall back to a lower stack level profile, because the highest-level profile never expires.

---

## 5. Combining Profile Purposes (Composite Schedule)

The Composite Schedule is the effective charging limit at each point in time, computed by merging all active profiles across purposes.

### 5.1 Calculation

The final effective limit is the **minimum** of:
1. The prevailing `ChargePointMaxProfile` limit (if any)
2. The prevailing `TxProfile` limit (if any), OR the prevailing `TxDefaultProfile` limit if no TxProfile is present

At any point in time, the available power or current SHALL be less than or equal to the lowest value across the merged schedules.

**For multi-connector Charge Points:** The `ChargePointMaxProfile` limit is the total for ALL connectors combined. The combined energy flow of all connectors SHALL NOT exceed it. This means the per-connector effective limit depends on what other connectors are drawing.

> **ESCALATE: SPEC-SILENT** — How a multi-connector Charge Point distributes the ChargePointMaxProfile limit across connectors is not specified.
> The spec says the combined flow SHALL NOT exceed the limit, but does not define the allocation algorithm (equal split, first-come-first-served, proportional, priority-based, etc.). An AI agent MUST NOT choose an allocation strategy. Ask the developer:
> 1. Does the target Charge Point perform local load balancing across connectors?
> 2. What allocation strategy does the CP firmware use?
> 3. Should the Central System pre-compute per-connector limits and send TxProfiles instead of relying on the CP's internal allocation?

### 5.2 GetCompositeSchedule

The Central System can request the computed composite schedule using `GetCompositeSchedule.req`:

- `connectorId` — which connector to compute for. When `connectorId=0`, the Charge Point SHALL report the **total expected power or current** it expects to consume from the grid.
- `duration` — how many seconds into the future to compute (from the moment the request is received).
- `chargingRateUnit` — optionally request the result in `A` (Amps) or `W` (Watts).

The response contains the merged schedule as a `ChargingSchedule` with the effective periods.

> **ESCALATE: VENDOR-DEPENDENT** — `GetCompositeSchedule` implementation varies significantly across Charge Point vendors.
> The spec defines what the result should represent but many CPs implement the calculation differently, especially around: profile boundary behavior, how multi-connector limits are divided when `connectorId=0`, and what happens when no profiles are active. An AI agent MUST NOT assume consistent behavior across vendors. Ask the developer:
> 1. Has `GetCompositeSchedule` been tested with the target CP hardware?
> 2. Does the CP return `Rejected` for `connectorId=0` or does it support station-level aggregation?
> 3. When no profiles are active, does the CP return the hardware maximum or an empty schedule?

### 5.3 ClearChargingProfile Filtering

`ClearChargingProfile.req` removes profiles by matching filters. All fields are optional:

| Field | Type | Effect |
|-------|------|--------|
| `id` | integer | Clear the specific profile with this `chargingProfileId` |
| `connectorId` | integer | Clear profiles on this connector |
| `chargingProfilePurpose` | enum | Clear profiles with this purpose |
| `stackLevel` | integer | Clear profiles at this stack level |

**Filtering logic:**

- If `id` is provided, clear that specific profile. The other fields are ignored.
- If `id` is omitted, clear all profiles matching the combination of the remaining fields. All provided fields must match (AND logic). Omitted fields are wildcards.
- If all fields are omitted (empty request), clear **all** profiles on the Charge Point.

**Examples:**

- `{id: 5}` — remove the profile with chargingProfileId=5
- `{connectorId: 1, chargingProfilePurpose: "TxProfile"}` — remove all TxProfiles on connector 1
- `{chargingProfilePurpose: "TxDefaultProfile"}` — remove all TxDefaultProfiles across all connectors
- `{connectorId: 0, stackLevel: 1}` — remove all stackLevel=1 profiles on connectorId=0
- `{}` — remove all profiles

**Response:** `Accepted` if one or more profiles were removed, `Unknown` if no profiles matched the filter.

---

## 6. Schedule Kinds

The `chargingProfileKind` determines how the schedule's time axis is interpreted.

### 6.1 Absolute

Schedule periods are offsets (in seconds) from a fixed point in time.

- `startSchedule` defines the anchor date-time.
- Each `chargingSchedulePeriod.startPeriod` is the number of seconds from `startSchedule`.
- If `startSchedule` is absent, the schedule starts at the beginning of the profile's validity (`validFrom`) or at "now" if `validFrom` is also absent.

**Example — limit to 16A from 14:00 to 18:00 today, then 32A after:**

```json
{
  "connectorId": 1,
  "csChargingProfiles": {
    "chargingProfileId": 1,
    "stackLevel": 0,
    "chargingProfilePurpose": "TxDefaultProfile",
    "chargingProfileKind": "Absolute",
    "chargingSchedule": {
      "chargingRateUnit": "A",
      "startSchedule": "2026-02-11T14:00:00Z",
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 16.0, "numberPhases": 3 },
        { "startPeriod": 14400, "limit": 32.0, "numberPhases": 3 }
      ]
    }
  }
}
```

### 6.2 Recurring

The schedule repeats on a daily or weekly cycle.

- `recurrencyKind` must be set to `Daily` or `Weekly`.
- `startSchedule` defines the reference start time (anchors the first occurrence).
- Schedule repeats every 24 hours (Daily) or 168 hours (Weekly).
- `duration` defines how long each recurrence lasts. If `duration` is shorter than the recurrence period, the Charge Point SHALL fall back to default behavior after the schedule ends (lower stackLevel profile, or no limit if none available).
- If `duration` is omitted, the schedule fills the entire recurrence period.

**Example — off-peak charging only (23:00 to 07:00 daily, reduced power otherwise):**

```json
{
  "connectorId": 0,
  "csChargingProfiles": {
    "chargingProfileId": 100,
    "stackLevel": 0,
    "chargingProfilePurpose": "TxDefaultProfile",
    "chargingProfileKind": "Recurring",
    "recurrencyKind": "Daily",
    "chargingSchedule": {
      "chargingRateUnit": "W",
      "duration": 86400,
      "startSchedule": "2013-01-01T00:00:00Z",
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 11000.0, "numberPhases": 3 },
        { "startPeriod": 28800, "limit": 6000.0, "numberPhases": 3 },
        { "startPeriod": 72000, "limit": 11000.0, "numberPhases": 3 }
      ]
    }
  }
}
```

This profile (taken from the spec's example in section 3.13.7) limits power to 6 kW between 08:00 and 20:00, and allows 11 kW otherwise. The `startSchedule` date does not matter for recurring profiles — only the time-of-day (and day-of-week for Weekly) is significant. The date anchors the cycle.

**Notes on recurring schedules:**
- On days when DST goes into or out of effect, a special profile might be needed.
- If `chargingSchedulePeriod` and/or `duration` is longer than the recurrence period, the remainder periods SHALL NOT be executed.

### 6.3 Relative

Schedule periods are relative to the start of the transaction.

- `startPeriod=0` corresponds to the moment the transaction begins.
- No `startSchedule` is needed (it would be meaningless).
- Only meaningful for `TxProfile` and `TxDefaultProfile` purposes.

**Example — ramp down: full power for first 30 minutes, then reduce:**

```json
{
  "connectorId": 1,
  "csChargingProfiles": {
    "chargingProfileId": 50,
    "stackLevel": 0,
    "chargingProfilePurpose": "TxProfile",
    "chargingProfileKind": "Relative",
    "transactionId": 12345,
    "chargingSchedule": {
      "chargingRateUnit": "A",
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 32.0, "numberPhases": 3 },
        { "startPeriod": 1800, "limit": 16.0, "numberPhases": 3 }
      ]
    }
  }
}
```

**Schedule duration behavior:**
- If `duration` is left empty, the last period continues indefinitely or until the end of the transaction (when `startSchedule` is absent).
- If `chargingSchedulePeriod` is longer than `duration`, the remainder periods SHALL NOT be executed.
- If `duration` is longer than the `chargingSchedulePeriod`, the Charge Point SHALL keep the value of the last period until `duration` has ended.

---

## 7. Common Pitfalls

> **Confidence: interpretation.** This section is based on common smart charging implementation issues. Not exhaustive or authoritative — use as guidance for code review and testing.

### 7.1 TxProfile Without Active Transaction

If you send a `SetChargingProfile.req` with `chargingProfilePurpose=TxProfile` and there is no active transaction on the specified connector, the Charge Point SHALL discard it and return an error. Always verify the transaction state before sending a TxProfile. If you need to pre-set limits for a future transaction, use `TxDefaultProfile` instead, or include the profile in `RemoteStartTransaction.req`.

### 7.2 Stack Level Gaps When Updating

Replacing a profile (same stackLevel + purpose) with a new profile that has `validFrom` in the future removes the old profile immediately but the new one is not active yet. This creates a gap with no profile at that stack level. **Fix:** Set `validFrom` to a time in the past to ensure continuous coverage. The Charge Point SHALL continue executing the existing profile until the new one is installed, but once replaced, the old profile is gone.

### 7.3 Highest Stack Level Without Duration

If you install a profile at the highest stack level without setting a `duration`, the Charge Point will never fall back to a lower stack level profile — the highest-level profile runs indefinitely. **Fix:** Always set `duration` on higher stack level profiles, or ensure you have a fallback strategy (e.g., explicitly clearing the profile when it should no longer apply).

### 7.4 connectorId=0 for TxDefaultProfile

Setting a `TxDefaultProfile` on `connectorId=0` applies to ALL connectors. If you then send a profile for connector 1 only, the connector-0 default is overridden only for connector 1. Other connectors still use the connector-0 default. This is often the desired behavior, but can be surprising if you expect the connector-1 profile to be independent of the connector-0 default.

### 7.5 ChargePointMaxProfile Is Per-CP, Not Per-Connector

The `ChargePointMaxProfile` limit is the **total** for the whole Charge Point. Two connectors sharing a 32A `ChargePointMaxProfile` means 32A total, not 32A each. If connector 1 is drawing 20A, connector 2 can draw at most 12A (assuming the CP performs internal load balancing).

### 7.6 chargingRateUnit Mismatch

If the Charge Point only supports Amps and you send a profile in Watts (or vice versa), behavior is vendor-dependent. Check the `ChargingScheduleAllowedChargingRateUnit` configuration key before sending profiles to ensure you use a supported unit.

> **ESCALATE: VENDOR-DEPENDENT** — Rate unit conversion behavior when profiles use unsupported units.
> The spec does not define what a Charge Point should do when it receives a profile in a `chargingRateUnit` it does not support. Some CPs reject the profile, others silently convert, others accept but ignore the limit. An AI agent MUST NOT assume any specific behavior. Ask the developer:
> 1. What does the `ChargingScheduleAllowedChargingRateUnit` config key return for the target CP?
> 2. Should the Central System always normalize to the CP's supported unit before sending?

### 7.7 GetCompositeSchedule Vendor Divergence

The spec defines what the Composite Schedule represents but many Charge Points implement the calculation differently. Edge cases where vendors diverge include: what happens at profile boundaries, how multi-connector limits are divided, the schedule returned when no profiles are active, and whether `connectorId=0` is supported at all. Always test `GetCompositeSchedule` with your specific hardware.

### 7.8 minChargingRate Misunderstanding

The `minChargingRate` field is an informational hint, not a hard constraint. It tells the Charge Point (or Local Controller) that charging below this rate is inefficient, allowing it to optimize power distribution — for example, by giving all available capacity to one connector rather than splitting it below the minimum for both. Not all Charge Points use this field. It does NOT mean the Charge Point will refuse to charge below this rate.

### 7.9 Accepted Does Not Mean Applied

A `SetChargingProfile.conf` with status `Accepted` means the Charge Point has received and stored the profile. It does NOT mean the CP is currently charging at the specified rate. Hardware limits, EV capabilities, the control pilot signal, and other profiles may result in a different effective rate. Use `GetCompositeSchedule` (with caveats from SS7.7) or meter values to verify actual charging behavior.

### 7.10 Offline Behavior

If a Charge Point goes offline:
- **With an active TxProfile:** It SHALL continue using that profile for the duration of the transaction.
- **Without a TxProfile but with other profiles:** It SHALL use whatever `ChargePointMaxProfile` and/or `TxDefaultProfile` profiles are available and combine them per the normal rules.
- **With no profiles at all:** It SHALL allow charging as if no constraints apply (full hardware capacity).

> **ESCALATE: SPEC-SILENT** — Default charging behavior when no profiles are installed and the CP is online.
> The spec defines offline behavior explicitly (charge without constraints if no profiles exist), but does not state whether the same applies when the CP is online with no profiles. Most implementations treat this the same way (no limit), but some site operators expect a "deny by default" posture. An AI agent MUST NOT assume either behavior. Ask the developer:
> 1. Should the CP charge at full capacity when no profiles are installed?
> 2. Is there a site-level default limit that should always be present as a fallback ChargePointMaxProfile?

---

## 8. Configuration Keys for Smart Charging

These configuration keys are read via `GetConfiguration.req` and define the Charge Point's smart charging capabilities. A Smart Charging-enabled Charge Point SHALL implement and support reporting all required keys.

| Key | Required | Type | Description |
|-----|----------|------|-------------|
| `ChargeProfileMaxStackLevel` | Required | integer | Maximum `stackLevel` value the CP accepts. Also indicates the max allowed number of installed charging schedules per Charging Profile Purpose. |
| `ChargingScheduleAllowedChargingRateUnit` | Required | CSL | Comma-separated list of supported rate units. Allowed values: `Current` (for Amps) and `Power` (for Watts). |
| `ChargingScheduleMaxPeriods` | Required | integer | Maximum number of `ChargingSchedulePeriod` entries allowed per `ChargingSchedule`. |
| `MaxChargingProfilesInstalled` | Required | integer | Maximum number of Charging Profiles that can be installed on the CP at any one time. |
| `ConnectorSwitch3to1PhaseSupported` | Optional | boolean | If defined and `true`, the Charge Point supports switching from 3-phase to 1-phase charging during a transaction. Use with care — some EVs do not support phase switching mid-session and it may cause physical damage. |

**Usage:** Before sending profiles, query these keys to understand the CP's limits. For example, if `ChargingScheduleMaxPeriods` is 5, do not send a schedule with 10 periods. If `ChargingScheduleAllowedChargingRateUnit` is `Current`, send profiles in Amps only.

---

## 9. What This Document Does NOT Cover

- **The full SetChargingProfile / ClearChargingProfile / GetCompositeSchedule message schemas** — for field-level detail, see the OCPP 1.6 specification sections 6.13-6.14, 6.21-6.22, 6.43-6.44.
- **Local Smart Charging and Local Controller topology** — section 3.13.4 of the spec describes this use case in detail. The protocol messages are the same; the difference is architectural (a Local Controller proxies OCPP messages).
- **RemoteStartTransaction with ChargingProfile** — a `TxProfile` can be included in `RemoteStartTransaction.req`. The CP applies it to the new transaction. This is covered in spec section 5.16.2.
- **OCPP 2.0.1 differences** — for the 2.0.1 smart charging model (which adds `ChargingStationExternalConstraints`, multiple schedules per profile, and grid integration messages), see [OCPP 2.0.1 Smart Charging](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md).
- **Vendor-specific extensions** — implementations may extend smart charging behavior beyond what the spec defines.

---

*This document is a community reference for AI agents. It is not affiliated with or endorsed by the Open Charge Alliance. For the authoritative specification, refer to the official OCPP 1.6 Edition 2 documents from OCA.*
