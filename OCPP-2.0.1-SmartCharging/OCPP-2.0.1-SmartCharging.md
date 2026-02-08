# OCPP 2.0.1 — Smart Charging Deep-Dive

> **Purpose:** Practical reference for AI agents implementing or debugging OCPP 2.0.1 smart charging. Covers the charging profile model, composite schedule calculation, AC/DC differences, grid integration, and common pitfalls.

> **Last updated:** 2026-02-07

---

## How This Document Was Produced

This document covers the OCPP 2.0.1 smart charging profile model, composite schedule calculation, AC/DC differences, grid integration, and common pitfalls. Its dominant confidence tier is **spec-knowledge** — behavioral rules from the OCPP 2.0.1 specification known via AI training data. Field names, enum values, and structural constraints are **schema-derived** (cross-referenced against the [schema documentation](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) and [data types reference](../OCPP-2.0.1-DataTypes.md), mechanically extracted from the official OCA JSON schemas). Paragraphs marked `> **Schema source**` quote directly from OCA schema description text (**schema-described** tier). The "Common pitfalls" section (§6) is **interpretation** — guidance based on AI training data, not normative.

This document contains **6 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [Smart Charging Examples](./OCPP-2.0.1-SmartCharging-Examples.md) — worked composite schedule calculations, realistic JSON payloads, message flow sequences
- [Smart Charging & ISO 15118](./OCPP-2.0.1-SmartCharging-ISO15118.md) — EV charging needs, EV-proposed schedules, sales tariffs
- [Smart Charging Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) — complete field-level message schemas (mechanically generated, high confidence)
- [Data Types Reference](../OCPP-2.0.1-DataTypes.md) — all shared types including `ChargingProfileType`, `ChargingScheduleType`, `ChargingSchedulePeriodType`

---

## 1. What Smart Charging Solves

Smart charging allows a CSMS to dynamically control how much power each Charging Station or EVSE delivers. Without it, every EV charges at maximum capacity, which can:

- **Overload the grid connection** — a building with 10 EVSEs at 22 kW each would need 220 kW, but the grid connection may only support 100 kW.
- **Cause peak demand charges** — utility billing often includes demand charges based on the highest 15-minute power draw.
- **Miss renewable energy windows** — shifting charging to midday (solar) or nighttime (wind/low-demand) reduces cost and carbon.
- **Conflict with building loads** — HVAC, lighting, and other building systems compete for the same grid connection.

Smart charging addresses these through **charging profiles** — schedules that define power or current limits over time, layered by purpose and priority.

### Messages

Nine messages make up the smart charging functional block (Block H). For complete field-level schemas, see the [schema reference](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md).

| Message | Direction | Purpose |
|---------|-----------|---------|
| `SetChargingProfile` | CSMS → CS | Install or update a charging profile |
| `GetChargingProfiles` | CSMS → CS | Request installed profiles matching criteria |
| `ClearChargingProfile` | CSMS → CS | Remove profiles by ID or criteria |
| `ReportChargingProfiles` | CS → CSMS | Return profiles in response to `GetChargingProfiles` |
| `GetCompositeSchedule` | CSMS → CS | Request the effective merged schedule |
| `ClearedChargingLimit` | CS → CSMS | Notify that an external limit was removed |
| `NotifyChargingLimit` | CS → CSMS | Report current limits from an external source |
| `NotifyEVChargingSchedule` | CS → CSMS | Report the EV's proposed schedule (ISO 15118) |
| `NotifyEVChargingNeeds` | CS → CSMS | Report the EV's charging requirements (ISO 15118) |

---

## 2. Charging Profile Model

A charging profile defines power/current limits over time. Profiles are layered: multiple profiles can be active simultaneously, and a well-defined priority system determines the effective limit at any moment.

### 2.1 Profile Structure Overview

```
ChargingProfileType
├── id                        (integer, unique identifier)
├── stackLevel                (integer ≥ 0, priority within same purpose)
├── chargingProfilePurpose    (see §2.2)
├── chargingProfileKind       (see §2.4)
├── chargingSchedule[]        (1-3 schedules, see §2.5)
├── recurrencyKind            (Daily or Weekly, for Recurring profiles)
├── transactionId             (required for TxProfile, links to active transaction)
├── validFrom / validTo       (validity window, see §2.3)
└── customData
```

> **Schema source (schema-described):** All field names and constraints above come from [`ChargingProfileType`](../OCPP-2.0.1-DataTypes.md#chargingprofiletype) in the data types reference.

### 2.2 Profile Purposes

Each profile has a `chargingProfilePurpose` that determines its role and priority.

| Purpose | Who typically sets it | Scope | Priority |
|---------|----------------------|-------|----------|
| `ChargingStationExternalConstraints` | Grid operator, building EMS, demand response aggregator — via the CS's local interfaces or via CSMS | Entire station (`evseId=0`) or per EVSE | **Highest** — acts as a hard ceiling |
| `ChargingStationMaxProfile` | CSMS (fleet operator, site operator) | Entire station (`evseId=0`) or per EVSE | **High** — caps total station draw |
| `TxDefaultProfile` | CSMS | Per EVSE (or `evseId=0` to apply to all EVSEs) | **Medium** — default for any transaction on the EVSE |
| `TxProfile` | CSMS | Per active transaction | **Lowest purpose** — but can raise limits up to the ceilings above |

> **Schema source (schema-described):** Enum values from [`ChargingProfilePurposeEnumType`](../OCPP-2.0.1-DataTypes.md#chargingprofilepurposeenumtype). Priority order is per the specification.

**Key rules:**

- Higher-priority purposes act as **ceilings**. A `TxProfile` cannot exceed the limit set by `ChargingStationMaxProfile` or `ChargingStationExternalConstraints`.
- `TxProfile` **requires** an active `transactionId`. The schema description states: *"SHALL only be included if ChargingProfilePurpose is set to TxProfile."*
- `TxDefaultProfile` with `evseId=0` applies as the default to **each individual EVSE**, not as a station-wide aggregate. The schema description for `SetChargingProfile.evseId` states: *"For TxDefaultProfile an evseId=0 applies the profile to each individual evse."*
- `ChargingStationMaxProfile` and `ChargingStationExternalConstraints` with `evseId=0` set an **overall limit for the whole Charging Station**.

### 2.3 Stack Levels

When multiple profiles exist at the **same purpose**, `stackLevel` determines which one takes precedence.

> **Schema source (schema-described):** `ChargingProfileType.stackLevel` description: *"Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0."*

- `stackLevel` is an integer ≥ 0.
- **Higher values win** within the same purpose.
- Different purposes use their own stack level spaces independently — a `TxDefaultProfile` at `stackLevel=5` does not override a `ChargingStationMaxProfile` at `stackLevel=0`.

**Example:** Two `TxDefaultProfile` profiles on the same EVSE:
- Profile A: `stackLevel=0`, limit 32 A
- Profile B: `stackLevel=1`, limit 16 A
- **Effective:** Profile B wins (higher stack level) → 16 A

### 2.4 Profile Kinds

The `chargingProfileKind` determines how the schedule's time axis is interpreted.

| Kind | Schedule start point | Use case |
|------|---------------------|----------|
| `Absolute` | `startSchedule` field (a specific date-time) | One-time schedules: "from 14:00 today, limit to 16 A" |
| `Recurring` | Repeats daily or weekly (set via `recurrencyKind`) | Time-of-use patterns: "every day, 08:00-18:00 at 16 A, overnight at 32 A" |
| `Relative` | Relative to the start of the transaction | Per-session ramps: "for the first 30 min charge at 32 A, then drop to 16 A" |

> **Schema source (schema-described):** Enum values from [`ChargingProfileKindEnumType`](../OCPP-2.0.1-DataTypes.md#chargingprofilekindenumtype). `startSchedule` description: *"Starting point of an absolute schedule. If absent the schedule will be relative to start of charging."*

**Notes on `Recurring`:**
- `recurrencyKind` can be `Daily` or `Weekly`.
- A recurring schedule defines one cycle (24 hours for daily, 7 days for weekly). The CS repeats it.
- Per the specification, a recurring schedule needs a `startSchedule` to anchor the first occurrence (e.g., "starting Monday at 00:00" for weekly).

### 2.5 Schedule Structure

Each profile contains 1 to 3 `chargingSchedule` entries. Each schedule defines:

| Field | Description |
|-------|-------------|
| `chargingRateUnit` | `W` (watts) or `A` (amperes) — the unit for all `limit` values in this schedule |
| `chargingSchedulePeriod[]` | Array of time periods, each with a `startPeriod` (seconds from schedule start) and a `limit` |
| `duration` | Schedule length in seconds. If omitted, the last period continues indefinitely (or until end of transaction for `TxProfile`) |
| `startSchedule` | Absolute start time (for `Absolute` kind). If absent, relative to start of charging |
| `minChargingRate` | Minimum rate the EV can usefully accept. Hint for local optimization — see §4 |
| `salesTariff` | Pricing information for ISO 15118 — see [ISO 15118 doc](./OCPP-2.0.1-SmartCharging-ISO15118.md) |

> **Schema source (schema-described):** All fields from [`ChargingScheduleType`](../OCPP-2.0.1-DataTypes.md#chargingscheduletype) and [`ChargingSchedulePeriodType`](../OCPP-2.0.1-DataTypes.md#chargingscheduleperiodtype).

**Period structure:**

Each `ChargingSchedulePeriodType` contains:
- `startPeriod` — seconds from the start of the schedule. First period typically starts at 0.
- `limit` — the power/current limit in the schedule's `chargingRateUnit`.
- `numberPhases` — number of AC phases (defaults to 3 if omitted). See §4.
- `phaseToUse` — which specific phase (1, 2, or 3) when `numberPhases=1` and AC phase switching is supported.

**Important:** The schema description for `startPeriod` states: *"The value of StartPeriod also defines the stop time of the previous period."* Periods are contiguous — there are no gaps within a schedule.

**Why up to 3 schedules?** The `chargingSchedule` array allows `maxItems: 3`. Per the specification, this enables providing the same profile in multiple rate units (e.g., one schedule in amperes, one in watts) or for different phases. The Charging Station selects the applicable schedule.

### 2.6 Validity Windows

- `validFrom` — when the profile becomes active. If absent, active immediately upon receipt.
- `validTo` — when the profile expires. If absent, active until replaced.

> **Schema source (schema-described):** `ChargingProfileType.validFrom` description: *"Point in time at which the profile starts to be valid. If absent, the profile is valid as soon as it is received by the Charging Station."* `validTo`: *"Point in time at which the profile stops to be valid. If absent, the profile is valid until it is replaced by another profile."*

---

## 3. Composite Schedule Calculation

The **composite schedule** is the effective charging limit at each point in time, after merging all active profiles. This is the most complex part of smart charging and the most common source of implementation bugs.

> **ESCALATE: SPEC-SILENT** — The exact normative composite schedule algorithm is defined in Part 2 of the OCPP 2.0.1 specification. The general approach below (stack level resolution + purpose hierarchy as ceilings) is widely accepted, but edge cases — gap behavior between profiles, boundary conditions when durations expire, rounding — are not fully specified in the JSON schemas and may differ between implementations.
> An AI agent MUST NOT implement composite schedule calculation from this description alone. Ask the developer:
> 1. Whether to follow the Part 2 normative algorithm (requires access to the official spec)
> 2. Which CS vendor's interpretation to target (vendors differ on edge cases)
> 3. Whether to use `GetCompositeSchedule` to let the CS compute it instead of reimplementing in the CSMS

### 3.1 General Approach

The composite schedule is computed in two steps:

**Step 1 — Resolve stack levels within each purpose:**
For each purpose that has active profiles, select the profile with the highest `stackLevel`. This gives at most one effective schedule per purpose.

**Step 2 — Apply purpose hierarchy as ceilings:**
Layer the per-purpose schedules from highest priority to lowest:
1. Start with `ChargingStationExternalConstraints` (if any) — this is the outermost ceiling.
2. Apply `ChargingStationMaxProfile` — the effective limit is `min(ExternalConstraints, StationMax)`.
3. Apply `TxDefaultProfile` — the effective limit is `min(above, TxDefault)`.
4. Apply `TxProfile` — the effective limit is `min(above, TxProfile)`.

The final result at each point in time is the **minimum** of all applicable limits from active purposes.

### 3.2 `GetCompositeSchedule`

The CSMS can request the computed composite schedule using `GetCompositeSchedule`.

- `evseId` — which EVSE to compute for. When `evseId=0`, the CS calculates the expected consumption for the **entire grid connection** (aggregate of all EVSEs).
- `duration` — how many seconds into the future to compute.
- `chargingRateUnit` — optionally request the result in `W` or `A`.

The response contains a [`CompositeScheduleType`](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#compositescheduletype) with the merged periods.

### 3.3 Rate Unit Conversion

Profiles may use different rate units (`W` vs `A`). To compare or merge them, conversion is needed:

**For AC charging:**
```
Power (W) = Current (A) × Voltage (V) × numberPhases
```

**For DC charging:**
```
Power (W) = Current (A) × Voltage (V)
```

The Charging Station must know the actual voltage to perform this conversion. When the CSMS requests a composite schedule in a specific rate unit, the CS performs the conversion.

> **ESCALATE: VENDOR-DEPENDENT** — Voltage assumptions for W↔A conversion.
> The conversion requires knowing the actual line voltage, which varies by installation (230V in Europe, 120/208/240V in North America, other values elsewhere). An AI agent MUST NOT hardcode a voltage assumption. Ask the developer:
> 1. What is the nominal voltage for the target installation?
> 2. Should voltage be read dynamically from meter values (`Voltage` measurand) or configured as a constant?
> 3. When profiles use mixed units (some in `A`, some in `W`), does the target CS support conversion, or should the CSMS normalize units before sending?

### 3.4 What Happens in Gaps

If no profile of a particular purpose is active at a given time (e.g., the `TxDefaultProfile` has expired and no replacement was sent), the behavior for that purpose layer is as if no limit is set — the ceiling from that layer does not apply.

> **ESCALATE: SPEC-SILENT** — Behavior when no profile is active at any purpose level (all profiles expired or none set).
> The OCPP 2.0.1 specification does not mandate a single default behavior for this case. An AI agent MUST NOT choose a default. Ask the developer:
> 1. Allow full hardware capacity (no limit) — the CS charges at its maximum rate
> 2. Apply a configured default limit — a site-specific safety cap
> 3. Block charging until a profile is set — strictest interpretation, prevents uncontrolled charging

---

## 4. AC vs DC Charging Differences

Smart charging behaves differently depending on whether the EVSE delivers AC or DC power.

### 4.1 AC Charging

AC charging passes alternating current to the EV's onboard charger. The EVSE controls the maximum current via the control pilot signal (IEC 61851).

**Key characteristics:**
- The `limit` in a charging schedule typically represents **current per phase** when `chargingRateUnit` is `A`.
- `numberPhases` determines how many phases are used (1 or 3 for most installations; 2 is rare).
- If `numberPhases` is omitted, **3 is assumed** (schema description: *"If a number of phases is needed, numberPhases=3 will be assumed unless another number is given."*).
- **Total power** = limit (A) × voltage (V) × numberPhases.

**Phase switching (`phaseToUse`):**
Some EVSEs can switch which physical phase is connected to a single-phase EV. The schema description states: *"Values: 1..3, Used if numberPhases=1 and if the EVSE is capable of switching the phase connected to the EV, i.e. ACPhaseSwitchingSupported is defined and true."*

This is useful for load balancing across phases in a building — the CSMS can direct different single-phase EVs to different phases.

### 4.2 DC Charging

DC charging converts AC to DC inside the EVSE and delivers DC power directly to the EV battery. The EVSE has full control over voltage and current.

**Key characteristics:**
- `numberPhases` and `phaseToUse` are not relevant (the DC output is not phased).
- The `limit` typically represents **total power** when `chargingRateUnit` is `W`, or **DC current** when `A`.
- DC chargers can adjust power more precisely and quickly than AC (no pilot signal rounding).

### 4.3 Rate Unit Conventions

| Charging type | Common rate unit | Why |
|--------------|-----------------|-----|
| AC | `A` (amperes) | The control pilot signal specifies current. EVSE hardware limits are in amperes. |
| DC | `W` (watts) | DC chargers control power output directly. Power is the more meaningful metric. |

Both units are valid for both types — the convention above is a practical default, not a requirement.

### 4.4 `minChargingRate`

The `minChargingRate` field in `ChargingScheduleType` indicates the minimum rate at which the EV can usefully charge. Below this rate, charging becomes inefficient (the EV's onboard charger may draw power but convert very little to stored energy).

> **Schema source (schema-described):** *"Minimum charging rate supported by the EV. This parameter is intended to be used by a local smart charging algorithm to optimize the power allocation for in the case a charging process is inefficient at lower charging rates. Accepts at most one digit fraction (e.g. 8.1)"*

A local smart charging algorithm on the CS can use this to avoid allocating tiny power slices that waste energy. If the available capacity is below `minChargingRate`, it may be better to allocate zero to that EVSE and give the capacity to another.

---

## 5. External Constraints & Grid Integration

External constraints represent limits imposed by entities outside the CSMS — grid operators, building energy management systems (EMS), demand response aggregators.

### 5.1 How External Constraints Arrive

External constraints are set via `SetChargingProfile` with `chargingProfilePurpose` = `ChargingStationExternalConstraints`. They can arrive:

- **From the CSMS** — the CSMS has received a signal from a grid operator or demand response program and forwards it as a profile.
- **From a local interface on the CS** — some Charging Stations have direct connections to building EMS systems (e.g., via Modbus, EEBUS, or OCPI). In this case, the CS installs the profile locally and **notifies** the CSMS via `NotifyChargingLimit`.

### 5.2 `NotifyChargingLimit` and `ClearedChargingLimit`

These CS → CSMS messages inform the CSMS about limits that the CS has received from external sources:

- `NotifyChargingLimit` — the CS reports that an external source has imposed a limit. Includes a `ChargingLimitType` with the source and optionally the schedule.
- `ClearedChargingLimit` — the CS reports that a previously-imposed external limit has been removed.

**`ChargingLimitSourceEnumType`** identifies the source:

| Value | Meaning |
|-------|---------|
| `EMS` | Building Energy Management System |
| `SO` | System Operator (grid/distribution operator) |
| `CSO` | Charging Station Operator |
| `Other` | Other external source |

> **Schema source (schema-described):** Enum values from [`ChargingLimitSourceEnumType`](../OCPP-2.0.1-DataTypes.md#charginglimitsourceenumtype).

### 5.3 `isGridCritical`

The `ChargingLimitType` (used in `NotifyChargingLimit`) includes an `isGridCritical` boolean flag.

> **Schema source (schema-described):** *"Indicates whether the charging limit is critical for the grid."*

Per the specification, when `isGridCritical` is true, the limit **must** be respected — it is a hard constraint from the grid operator, not a soft request. The CS should apply it immediately, even if it means interrupting or reducing active charging sessions.

> **ESCALATE: POLICY-DEPENDENT** — Reaction timing and behavior for `isGridCritical=true`.
> The specification requires that grid-critical limits be respected, but the implementation details are policy decisions. An AI agent MUST NOT choose defaults for these. Ask the developer:
> 1. How fast must the CS react? (immediately / within N seconds / at next control interval)
> 2. Should active transactions be interrupted mid-charge, or should the limit apply only to new sessions?
> 3. Should the CSMS be notified before or after the limit is applied?
> 4. What happens if the grid-critical limit conflicts with minimum charging rates (`minChargingRate`) — stop charging entirely, or charge at the minimum?

### 5.4 Mid-Transaction Limit Changes

When an external constraint changes during an active transaction (e.g., the grid operator reduces the allowed power):

1. The CS receives the new `ChargingStationExternalConstraints` profile.
2. The CS recomputes the composite schedule.
3. If the new effective limit is lower than the current charging rate, the CS must reduce the rate.
4. The CS reports the change via `TransactionEvent` with `triggerReason=ChargingRateChanged`.

---

## 6. Common Implementation Pitfalls

> **Confidence: interpretation.** This section is based on common smart charging implementation issues known from AI training data. Not exhaustive or authoritative — use as guidance for code review and testing.

### 6.1 Confusing Purpose Priority with Stack Level

Stack levels only resolve priority **within the same purpose**. A `TxProfile` at `stackLevel=99` cannot exceed the ceiling set by a `ChargingStationExternalConstraints` at `stackLevel=0`. The purpose hierarchy always applies first.

### 6.2 Ignoring External Constraints as Hard Ceilings

`ChargingStationExternalConstraints` is the **highest priority** purpose. Implementations must ensure that the composite schedule never exceeds this limit, regardless of what other profiles request.

### 6.3 Rate Unit Mismatch

When merging profiles in different rate units (one in `A`, another in `W`), the CS must convert to a common unit before applying `min()`. Getting the voltage or phase count wrong in this conversion leads to incorrect limits.

> **ESCALATE: VENDOR-DEPENDENT** — Behavior when profiles at different purposes use incompatible rate units.
> If `ChargingStationMaxProfile` is in `W` and `TxDefaultProfile` is in `A`, the CS must convert before computing `min()`. This requires a voltage value. An AI agent MUST NOT assume the conversion is handled automatically. Ask the developer:
> 1. Does the target CS support mixed rate units across profiles?
> 2. What voltage does the CS use for conversion — a configured constant, or measured from the meter?
> 3. Should the CSMS normalize all profiles to the same rate unit before sending to avoid CS-side conversion?

### 6.4 `Recurring` Profiles Crossing Midnight

A `Daily` recurring schedule with `startSchedule` at 06:00 and `duration` of 86400 seconds (24 hours) is straightforward. But if `duration` is only 43200 seconds (12 hours), the schedule is only active from 06:00-18:00 each day. Outside that window, this profile does not contribute to the composite schedule.

### 6.5 `Relative` Profile Start Time

`Relative` profiles start when the **transaction** starts, not when the profile is received. If the CSMS sends a `Relative` profile before the transaction begins, the schedule timeline starts at transaction start.

### 6.6 `evseId=0` Semantics Differ by Purpose

- For `TxDefaultProfile`: `evseId=0` means the profile applies to **each EVSE individually** (each EVSE gets this as its default).
- For `ChargingStationMaxProfile` and `ChargingStationExternalConstraints`: `evseId=0` means the profile applies to the **whole station** (aggregate limit).
- For `GetCompositeSchedule`: `evseId=0` requests the expected consumption for the **grid connection** (total across all EVSEs).

> **ESCALATE: VENDOR-DEPENDENT** — `GetCompositeSchedule` with `evseId=0` aggregation logic.
> When `evseId=0`, the CS must compute the total expected consumption across all EVSEs. How the CS aggregates individual EVSE schedules into a station-wide composite is not fully specified. An AI agent MUST NOT assume a specific aggregation method. Ask the developer:
> 1. Does the target CS support `evseId=0` for `GetCompositeSchedule`? (not all do)
> 2. Does it sum individual EVSE composites, or does it apply the station-level profile directly?
> 3. How does it handle EVSEs with different rate units or phase configurations?

### 6.7 `TxProfile` Without Active Transaction

`TxProfile` requires a `transactionId` field linking it to an active transaction. Sending a `TxProfile` without a valid `transactionId`, or for a transaction that has ended, should be rejected by the CS.

### 6.8 Phase-Related Bugs on AC

- A 3-phase profile with `limit=32` means 32 A per phase = 22 kW (at 230 V). A 1-phase profile with `limit=32` means 32 A on one phase = 7.4 kW. Confusing the two off by a factor of 3.
- When `numberPhases` is omitted, **3 is assumed**. If the EV is actually single-phase, the actual power draw will be 1/3 of what the profile allows.

### 6.9 `ChargingProfileStatus: Accepted` Does Not Mean Applied

The schema description for `ChargingProfileStatusEnumType` states: *"This does not guarantee the schedule will be followed to the letter. There might be other constraints the Charging Station may need to take into account."*

`Accepted` means the CS has received and stored the profile, not that the CS is currently charging at the specified rate. Hardware limits, EV capabilities, and other profiles may result in a different effective rate.

---

## 7. Key Configuration Variables

The following `SmartChargingCtrlr` component variables control smart charging behavior on the Charging Station.

> **Note:** Variable names below are per the specification. They are set/queried via `SetVariables` / `GetVariables` using `component.name = "SmartChargingCtrlr"`.

| Variable | Description |
|----------|-------------|
| `Enabled` | Whether smart charging is supported and active |
| `ACPhaseSwitchingSupported` | Whether the EVSE supports switching the connected AC phase |
| `ProfileMaxStackLevel` | Maximum `stackLevel` the CS supports |
| `ChargingScheduleMaxPeriods` | Maximum number of periods per schedule |
| `ChargingScheduleChargingRateUnit` | Which rate units the CS supports (`A`, `W`, or both) |
| `PeriodsPerSchedule` | Maximum periods the CS can handle per schedule |
| `ChargingProfileMaxStackLevel` | Maximum stack level value the CS accepts |
| `EntriesChargingProfiles` | Maximum number of charging profiles the CS can store |

> **Note:** Exact variable names and availability depend on the CS implementation and firmware. Use `GetBaseReport` to discover which variables are supported.

---

## 8. What This Document Does NOT Cover

- **The exact normative composite schedule algorithm** from Part 2 of the specification — this document describes the general approach, not the step-by-step normative text.
- **OCPP 2.0.1 errata** — if the OCA has published corrections to the smart charging sections, they are not reflected here.
- **Vendor-specific extensions** — `customData` fields allow vendor extensions; these are not documented.
- **OCTT compliance test cases** — for compliance testing details, consult the OCA's OCPP Compliance Testing Tool documentation.
- **ISO 15118 EV charging needs and sales tariffs** — see the [companion ISO 15118 document](./OCPP-2.0.1-SmartCharging-ISO15118.md).
- **Worked examples and sequence diagrams** — see the [companion examples document](./OCPP-2.0.1-SmartCharging-Examples.md).

---

## 9. Related Documents

| Document | What it contains |
|----------|-----------------|
| [Smart Charging Examples](./OCPP-2.0.1-SmartCharging-Examples.md) | Composite schedule walkthroughs, realistic JSON payloads, message flow sequences |
| [Smart Charging & ISO 15118](./OCPP-2.0.1-SmartCharging-ISO15118.md) | EV charging needs, EV schedules, sales tariffs |
| [Smart Charging Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) | Field-level message schemas (mechanically generated from OCA JSON schemas) |
| [Data Types Reference](../OCPP-2.0.1-DataTypes.md) | All shared types: `ChargingProfileType`, `ChargingScheduleType`, `ChargingSchedulePeriodType`, enums |
| [OCPP 2.0.1 Overview](../OCPP-2.0.1.md) | Protocol overview including smart charging summary in §4.5 |

---

*This document is a community reference for AI agents. It is not affiliated with or endorsed by the Open Charge Alliance. For the authoritative specification, refer to the official OCPP 2.0.1 documents from OCA.*
