# OCPP 2.1 — Smart Charging Deltas (vs 2.0.1)

> **Purpose:** Practical reference for AI agents implementing or debugging the OCPP **2.1** additions to smart charging. Covers ONLY what is new versus 2.0.1: dynamic charging profiles / dynamic schedules, priority charging, battery swap, and periodic event streams. Shared fundamentals (the charging-profile model, stack levels, composite schedule) are unchanged — this document cross-links the 2.0.1 deep-dive rather than repeating them.

> **Last updated:** 2026-06-11

---

## How This Document Was Produced

This document covers the OCPP **2.1** smart-charging additions relative to 2.0.1. Its dominant confidence tier is **spec-knowledge** — behavioral rules summarized in original wording from the OCPP 2.1 Edition 2 Part 2 specification (Smart Charging block K, especially use cases K15–K29). All message names, field names, and enum values are **schema-derived** — cross-referenced against the mechanically generated [SmartCharging schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md), [BatterySwap schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md), [Diagnostics schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md), and the [Data Types reference](../OCPP-2.1-DataTypes.md), all extracted from the official OCA artifacts. No spec prose is reproduced verbatim (the OCA specification is CC BY-ND licensed); all explanatory text is original.

This document contains **3 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer (or operator) to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the confidence and escalation model.

**Companion documents:**
- [OCPP 2.0.1 Smart Charging](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) — shared fundamentals: charging-profile model, purposes, stack levels, composite schedule, AC/DC differences. **Read this first** for anything not marked *(2.1)*.
- [OCPP 2.1 Sequences](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md) — full numbered-step message flows for the dynamic-schedule loop, battery swap, web-payment start, and periodic event stream lifecycle.
- [OCPP 2.1 Bidirectional / V2X](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) — operation modes, setpoints, discharge limits, V2X curves referenced by dynamic schedule periods.
- [OCPP 2.1 DER Control](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md) — DER controls configured alongside smart charging.
- [SmartCharging schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md) — complete field-level message schemas.
- [Data Types reference](../OCPP-2.1-DataTypes.md) — shared types including `ChargingProfileType`, `ChargingSchedulePeriodType`, `ChargingScheduleType`.

---

## 1. What Is New in 2.1

The 2.0.1 charging-profile model is carried forward unchanged: `SetChargingProfile`, `GetChargingProfiles`, `ClearChargingProfile`, `ReportChargingProfiles`, `GetCompositeSchedule`, `NotifyChargingLimit`, `ClearedChargingLimit`, `NotifyEVChargingNeeds`, `NotifyEVChargingSchedule` all behave as documented in the [2.0.1 deep-dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md). OCPP 2.1 adds the following on top:

| Area | New messages | Purpose |
|------|--------------|---------|
| Dynamic charging profiles | `UpdateDynamicSchedule` (CSMS → CS), `PullDynamicScheduleUpdate` (CS → CSMS) | Update the limits/setpoints of an existing dynamic profile without re-installing the whole profile. |
| Priority charging | `UsePriorityCharging` (CSMS → CS), `NotifyPriorityCharging` (CS → CSMS) | Temporarily charge one transaction at maximum priority (e.g. an EV that must leave soon). |
| Battery swap | `RequestBatterySwap` (CSMS → CS), `BatterySwap` (CS → CSMS) | Coordinate physical battery exchange at a swap station. |
| Periodic event streams | `OpenPeriodicEventStream`, `ClosePeriodicEventStream` (CS → CSMS), `GetPeriodicEventStream`, `AdjustPeriodicEventStream` (CSMS → CS), `NotifyPeriodicEventStream` (CS → CSMS, one-way) | Efficient high-rate telemetry without per-sample request/response overhead. |

New enum values added to the carried-over charging types:

| Type | New 2.1 value | Meaning |
|------|---------------|---------|
| [`ChargingProfileKindEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilekindenumtype) | `Dynamic` | The schedule periods carry live setpoints/limits that the CSMS (or the CS, by pull) updates over time. |
| [`ChargingProfilePurposeEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilepurposeenumtype) | `PriorityCharging` | Profile purpose dedicated to priority charging. |
| [`ChargingProfilePurposeEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilepurposeenumtype) | `LocalGeneration` | Profile representing locally generated capacity (e.g. on-site PV) rather than a limit. |

---

## 2. Dynamic Charging Profiles / Dynamic Schedules

### 2.1 Concept

A **dynamic** charging profile is a charging profile whose `chargingProfileKind` is the `Dynamic` value of [`ChargingProfileKindEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilekindenumtype). Unlike `Absolute` / `Recurring` / `Relative` profiles — whose schedule periods are fixed at install time — a dynamic profile's per-period limits and setpoints are expected to change during the transaction. The CSMS pushes new values, or the CS pulls them, without resending the full `SetChargingProfile` payload each time.

This is the OCPP-level mechanism behind ISO 15118-20 dynamic control mode (see [`ControlModeEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#controlmodeenumtype) `DynamicControl` reported in `NotifyEVChargingNeeds`) and behind V2X setpoint following (cross-link the [Bidirectional / V2X doc](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md)).

### 2.2 Dynamic fields on a charging schedule period

These *(2.1)* fields on [`ChargingSchedulePeriodType`](../OCPP-2.1-DataTypes.md#chargingscheduleperiodtype) make dynamic operation possible. They are also the fields the update messages (§2.3) can change.

| Field | Meaning |
|-------|---------|
| `setpoint` | Target the EV should follow as closely as possible (negative = discharge). `setpoint_L2`, `setpoint_L3` for per-phase. |
| `setpointReactive` | Reactive-power/current target (positive = inductive, negative = capacitive). `setpointReactive_L2`, `setpointReactive_L3` per phase. |
| `dischargeLimit` | Maximum the EV may discharge (a negative value; `max: 0.0`). `dischargeLimit_L2`, `dischargeLimit_L3` per phase. |
| `limit` / `limit_L2` / `limit_L3` | Charging-rate ceiling (carried over, now optional depending on operation mode). |
| `v2xBaseline` | Baseline power onto which the V2X curves are added. |
| `v2xFreqWattCurve` | [`V2XFreqWattPointType`](../OCPP-2.1-DataTypes.md#v2xfreqwattpointtype)[] — frequency→watt response curve. See [V2X doc](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md). |
| `v2xSignalWattCurve` | [`V2XSignalWattPointType`](../OCPP-2.1-DataTypes.md#v2xsignalwattpointtype)[] — signal→watt response curve. See [V2X doc](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md). |

Two *(2.1)* fields on [`ChargingProfileType`](../OCPP-2.1-DataTypes.md#chargingprofiletype) coordinate the update cadence:

| Field | Meaning |
|-------|---------|
| `dynUpdateInterval` | Seconds after the last update at which the CS should request a fresh one via `PullDynamicScheduleUpdate`. `0` or absent = no pull interval. Only relevant for a dynamic profile. |
| `dynUpdateTime` | Timestamp at which the limits/setpoints were last updated (by a pull, a push, or an external actor). Only relevant for a dynamic profile. |

### 2.3 The two update messages

Both messages address an existing profile by `chargingProfileId` and carry a [`ChargingScheduleUpdateType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#chargingscheduleupdatetype) — a subset of the period containing only the changeable fields (`limit*`, `setpoint*`, `setpointReactive*`, `dischargeLimit*`). They do not install or replace a profile.

| Message | Direction | Request key fields | Response | Notes |
|---------|-----------|--------------------|----------|-------|
| [`UpdateDynamicSchedule`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule) | CSMS → CS | `chargingProfileId`, `scheduleUpdate` (required) | `status`: [`ChargingProfileStatusEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilestatusenumtype) (`Accepted` / `Rejected`) | CSMS pushes new setpoints/limits into the live dynamic profile. |
| [`PullDynamicScheduleUpdate`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate) | CS → CSMS | `chargingProfileId` | `status`: [`ChargingProfileStatusEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilestatusenumtype); optional `scheduleUpdate` | CS asks the CSMS for the latest values (e.g. when offline-buffered or on `dynUpdateInterval`). The CSMS returns the update in the response. |

The full establish-then-update loop is in the [Sequences doc §2](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md#2-dynamic-schedule-update-loop).

> **ESCALATE: POLICY-DEPENDENT** — Whether your CSMS drives a dynamic profile by **push** (`UpdateDynamicSchedule` on the CSMS's own cadence) or relies on the CS to **pull** (`dynUpdateInterval` + `PullDynamicScheduleUpdate`), and how often, depends on your control strategy, the EV/charger capability, and grid-signal latency. Confirm the intended mode with the operator.

---

## 3. Priority Charging

### 3.1 Concept

Priority charging lets the CSMS (or a local action relayed by the CS) temporarily promote one transaction to charge at maximum allowed rate, overriding the normal smart-charging limits applied to it. Typical uses: a driver who pays for or requests a "boost", or an operational need to free a bay quickly. The dedicated `PriorityCharging` value of [`ChargingProfilePurposeEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilepurposeenumtype) marks the profile that backs it.

### 3.2 Messages

| Message | Direction | Request key fields | Response | Notes |
|---------|-----------|--------------------|----------|-------|
| [`UsePriorityCharging`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#useprioritycharging) | CSMS → CS | `activate` (boolean), `transactionId` | `status`: [`PriorityChargingStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#prioritychargingstatusenumtype) (`Accepted` / `Rejected` / `NoProfile`) | CSMS requests starting (`true`) or stopping (`false`) priority charging for a transaction. `NoProfile` means no priority-charging profile is configured. |
| [`NotifyPriorityCharging`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyprioritycharging) | CS → CSMS | `activated` (boolean), `transactionId` | empty `{}` | CS reports that priority charging actually started (`true`) or stopped (`false`) for the transaction — e.g. after a local trigger or when the priority profile ends. |

> **ESCALATE: POLICY-DEPENDENT** — Eligibility for priority charging (who may invoke it, pricing, and the rate it grants relative to grid/site ceilings) is an operator business decision. Do not hard-code an answer.

---

## 4. Battery Swap

OCPP 2.1 adds coordination for battery-swap stations, where a depleted pack is physically exchanged rather than charged in place (block S, use cases S01–S04).

| Message | Direction | Request key fields | Response | Notes |
|---------|-----------|--------------------|----------|-------|
| [`RequestBatterySwap`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#requestbatteryswap) | CSMS → CS | `idToken`, `requestId` | `status`: [`GenericStatusEnumType`](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | CSMS asks the station to begin a swap for an authorized token. |
| [`BatterySwap`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap) | CS → CSMS | `batteryData[]`, `eventType`, `idToken`, `requestId` | empty `{}` | CS notifies battery in/out events. `eventType` is [`BatterySwapEventEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswapeventenumtype): `BatteryIn` / `BatteryOut` / `BatteryOutTimeout`. `requestId` correlates the events (and the optional `RequestBatterySwap`). |

The full flow is in the [Sequences doc §3](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md#3-battery-swap).

---

## 5. Periodic Event Streams

### 5.1 Concept

A periodic event stream is an efficient transport for high-rate telemetry. Instead of one request/response pair per sample (as with polled `GetVariables` or per-event `NotifyEvent`), the CS opens a stream tied to a monitor and then pushes batches of timestamped values in one-way `NotifyPeriodicEventStream` messages. This removes per-sample round-trip overhead (block N, use cases N11–N15).

A stream is bound to a `variableMonitoringId` via [`ConstantStreamDataType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#constantstreamdatatype) and paced by [`PeriodicEventStreamParamsType`](../OCPP-2.1-DataTypes.md#periodiceventstreamparamstype) (`interval` seconds, `values` items per send).

### 5.2 The five messages (N11–N15)

| Message | Direction | Purpose |
|---------|-----------|---------|
| [`OpenPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#openperiodiceventstream) | CS → CSMS | CS opens a stream (`constantStreamData`); CSMS replies `Accepted`/`Rejected`. |
| [`NotifyPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream) | CS → CSMS (**one-way SEND**) | CS pushes a batch: `basetime`, `data[]` ([`StreamDataElementType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#streamdataelementtype) with offset `t` + value `v`), stream `id`, and `pending` count. No response. |
| [`AdjustPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#adjustperiodiceventstream) | CSMS → CS | CSMS re-paces an existing stream (`id`, `params`). |
| [`GetPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getperiodiceventstream) | CSMS → CS | CSMS requests the list of currently configured streams. |
| [`ClosePeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#closeperiodiceventstream) | CS → CSMS | CS closes a stream by `id`. |

> **ESCALATE: POLICY-DEPENDENT** — Stream rate (`interval` / `values`) and which variables warrant streaming versus polling are a bandwidth/cost trade-off specific to the deployment and back-end ingestion capacity. Confirm targets with the operator.

The full lifecycle is in the [Sequences doc §5](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md#5-periodic-event-stream-lifecycle).
