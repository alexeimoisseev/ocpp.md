# OCPP 2.1 — DER Control Deep-Dive

> **Purpose:** Practical reference for AI agents implementing or debugging OCPP 2.1 DER (Distributed Energy Resource) control — functional block R. Covers what DER control is, the control/curve model, the Get / Set / Clear / Report message flow, alarms and start/stop notifications, prioritization and superseding, and offline behavior.

> **Last updated:** 2026-06-09

---

## How This Document Was Produced

This document covers OCPP 2.1 DER control (functional block R, use cases R01–R05 of the Part 2 specification). Its dominant confidence tier is **spec-knowledge** — behavioral rules summarized in original wording from the OCPP 2.1 Edition 2 Part 2 specification. Message names, field names, enum values, and structural constraints are **schema-derived** — cross-referenced against the [DER Control schema reference](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md), the [data types reference](../OCPP-2.1-DataTypes.md), and the [device model reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md), all mechanically extracted from the official OCA artifacts. No spec prose is reproduced verbatim (the OCA specification is CC BY-ND licensed); all explanatory text is original.

This document contains **4 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer (or grid/utility stakeholder) to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [DER Control Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md) — complete field-level message and local-type schemas (mechanically generated, high confidence)
- [Data Types Reference](../OCPP-2.1-DataTypes.md) — shared types including [`DERControlEnumType`](../OCPP-2.1-DataTypes.md#dercontrolenumtype) and [`DERControlStatusEnumType`](../OCPP-2.1-DataTypes.md#dercontrolstatusenumtype)
- [Device Model Reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md) — the `ACDERCtrlr` and `DCDERCtrlr` components and their variables
- [Smart Charging Deep-Dive (2.0.1)](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) — charging profiles, which DER control reuses for active/reactive power setpoints

---

## 1. What DER Control Is and Why OCPP 2.1 Adds It

When a charging station (or a fleet of them) charges and discharges bidirectionally, the utility treats it as a **Distributed Energy Resource (DER)** — a grid-connected inverter that must obey local grid codes. Grid codes define how an inverter reacts to abnormal grid conditions: ride through a voltage sag, trip off on over-frequency, absorb or inject reactive power to support voltage, ramp slowly back into service, and so on. OCPP 2.1 adds functional block R so a CSMS can configure and observe this grid-code behavior on a charging station.

DER control also applies to **charging-only** stations: a utility may require frequency support (curtailing import when frequency drops) even from stations that never discharge. Throughout block R, "DER control" covers both bidirectional and charging-only cases.

### 1.1 The aggregator model

OCPP does **not** connect a utility directly to a charging station or an EV. The flow is layered:

| Step | Sender → Receiver | Interface | Notes |
|------|-------------------|-----------|-------|
| 1 | Utility → CSMS | IEC 61850 / IEEE 2030.5 / DNP3 / Modbus (out of OCPP scope) | Utility sends grid-code settings, often a schedule of timed events with priorities |
| 2 | CSMS → CS | OCPP block R messages | CSMS, acting as the CSO/aggregator, schedules and prioritizes, then forwards the appropriate controls |
| 3 | CS → EV | ISO 15118-20 (or CHAdeMO) | If the inverter is in the EV, the station relays settings/targets to the EV |

The CSMS carries most of the scheduling and prioritization burden. OCPP block R is the CSMS↔CS interface only.

### 1.2 Relationship to ISO 15118-20 inverter architectures

Where the inverter physically lives determines who enforces the grid code. From the OCPP point of view this is irrelevant — the CSMS always sends DER controls to the **charging station**, which decides how to apply them.

| Architecture | Inverter location | Who enforces grid code | OCPP role |
|--------------|-------------------|------------------------|-----------|
| DC bidirectional (ISO 15118-20 DC_BPT, CHAdeMO) | In the EVSE (charging station) | The EVSE inverter directly | CS applies DER controls to its own inverter |
| ISO 15118-20 V2G-AC (`AC_BPT_DER`) | In the EV | The EV's smart inverter | CS forwards all required settings to the EV during ISO 15118-20 parameter discovery |
| ISO 15118-20 V2G-Split (`AC_BPT_DER`) | Split EV + EVSE | EV does what it supports; EVSE emulates the rest via `ChargeLoop` targets | CS splits controls: EV-supported ones go to the EV, the remainder the EVSE emulates |

The station reports which control modes it can emulate/enforce in the device-model variable `ModesSupported` (see [§9](#9-device-model-acderctrlr--dcderctrlr)). Active/reactive power **setpoints and limits** are not block-R messages — they are expressed as OCPP charging profiles (see [Smart Charging](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md)); block R covers the grid-code *behavior* (curves and parameter settings) on top of those profiles.

---

## 2. The DER Control Model

A **DER control** is one configured grid-code behavior. Every control has:

- a **`controlId`** — a unique id (e.g. a UUID, max 36 chars) the CSMS assigns;
- a **`controlType`** — one value of [`DERControlEnumType`](../OCPP-2.1-DataTypes.md#dercontrolenumtype), which dictates *which* control-specific object is allowed;
- an **`isDefault`** flag — default vs scheduled (see [§2.4](#24-default-vs-scheduled-controls));
- a **`priority`** integer inside the control-specific object (0 = highest priority);
- exactly **one control-specific object** matching the `controlType` (see [§2.3](#23-controltype--payload-field-mapping)).

### 2.1 Control types

The 22 values of [`DERControlEnumType`](../OCPP-2.1-DataTypes.md#dercontrolenumtype), grouped by what they configure:

| Group | `controlType` values | What it does |
|-------|----------------------|--------------|
| Enter service | `EnterService` | Voltage/frequency window and delay/ramp for (re)connecting to the grid |
| Frequency droop | `FreqDroop`, `FreqWatt` | Adjust active power as a function of frequency to stabilize the grid |
| Frequency trip / ride-through | `HFMustTrip`, `HFMayTrip`, `LFMustTrip` | High/low-frequency disconnect (`MustTrip`) and ride-through (`MayTrip`) curves |
| Voltage trip / ride-through / momentary cessation | `HVMustTrip`, `HVMayTrip`, `HVMomCess`, `LVMustTrip`, `LVMayTrip`, `LVMomCess` | High/low-voltage disconnect, ride-through, and momentary-cessation curves |
| Reactive power | `FixedVar`, `VoltVar`, `WattVar`, `FixedPFAbsorb`, `FixedPFInject`, `WattPF` | Fixed or curve-based reactive-power / power-factor behavior |
| Active power vs voltage | `VoltWatt` | Reduce/increase active power as a function of voltage |
| Discharge / power limits | `LimitMaxDischarge`, `PowerMonitoringMustTrip` | Cap discharge power; trip on a power-monitoring threshold |
| Ramp rates | `Gradients` | Default and soft-start ramp rates |

> **ESCALATE: POLICY-DEPENDENT** — Which control types are enabled, and the actual curve points / setpoints / thresholds inside them, are grid-code and utility-policy decisions (often per IEEE 1547, EN 50549, VDE-AR-N 4105, or a local regulator). Do not invent curve values; obtain them from the utility/CSO.

### 2.2 Curves vs parameter settings

Two structural forms exist:

| Form | Carried in | Used by | Shape |
|------|-----------|---------|-------|
| **Curve** | [`DERCurveType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#dercurvetype) | All trip/ride-through and `Volt*`/`Watt*`/`FreqWatt` types | 1–10 `(x, y)` points ([`DERCurvePointsType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#dercurvepointstype)), a `priority`, and a `yUnit` ([`DERUnitEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#derunitenumtype)); the x-axis is frequency/voltage/power depending on type |
| **Parameter setting** | type-specific object (e.g. [`FreqDroopType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#freqdrooptype), [`FixedPFType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#fixedpftype), [`FixedVarType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#fixedvartype), [`EnterServiceType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#enterservicetype), [`GradientType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#gradienttype), [`LimitMaxDischargeType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#limitmaxdischargetype)) | `FreqDroop`, `FixedVar`, `FixedPFAbsorb`, `FixedPFInject`, `EnterService`, `Gradients`, `LimitMaxDischarge` | Named scalar parameters plus a `priority` |

A frequency-droop is conceptually a parameterized Freq-Watt curve (slope + dead-band) rather than explicit points, which is why it has its own [`FreqDroopType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#freqdrooptype) object.

Curves may also carry optional refinements: [`HysteresisType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#hysteresistype) (return-to-normal behavior after an event), [`VoltageParamsType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#voltageparamstype) (e.g. 10-minute mean over-voltage monitoring, momentary cessation via [`PowerDuringCessationEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#powerduringcessationenumtype)), and [`ReactivePowerParamsType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reactivepowerparamstype) (VoltVar `vRef` / autonomous adjustment).

### 2.3 `controlType` → payload field mapping

`SetDERControlRequest` carries the control-specific object in exactly one field, selected by `controlType`. Sending the wrong field, or more than one control, must be rejected (see [§4](#4-set-flow)).

| `controlType` value(s) | Required field in `SetDERControlRequest` |
|------------------------|------------------------------------------|
| `FixedPFAbsorb` | `fixedPFAbsorb` |
| `FixedPFInject` | `fixedPFInject` |
| `FixedVar` | `fixedVar` |
| `LimitMaxDischarge` | `limitMaxDischarge` |
| `FreqDroop` | `freqDroop` |
| `EnterService` | `enterService` |
| `Gradients` | `gradient` |
| all other types (trip, ride-through, `VoltVar`, `VoltWatt`, `WattVar`, `WattPF`, `FreqWatt`, `PowerMonitoringMustTrip`) | `curve` |

### 2.4 Default vs scheduled controls

- **Default control** (`isDefault = true`): always-on baseline for its `controlType`. It is active whenever no scheduled control of the same type is active. A default control **must not** carry `startTime` or `duration` — sending those is rejected.
- **Scheduled control** (`isDefault = false`): time-bounded by `startTime` and `duration` (seconds). It becomes active at `startTime`, overriding the default of the same type, and is automatically deleted by the station once `startTime + duration` has elapsed. When it ends, the system falls back to the default (if any).

Two `controlType`s are default-only — `EnterService` and `Gradients`. The CSMS must not send them with `isDefault = false`; the station rejects such a request.

Controls persist across reboots/power-cycles — the station stores them durably.

---

## 3. Messages and Direction

Six messages make up block R. Full field-level schemas: [DER Control schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md).

| Message | Direction | Purpose |
|---------|-----------|---------|
| [`GetDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#getdercontrol) | CSMS → CS | Request installed controls matching criteria |
| [`SetDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol) | CSMS → CS | Install or update one DER control |
| [`ClearDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#cleardercontrol) | CSMS → CS | Remove controls by id / type / default flag |
| [`ReportDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reportdercontrol) | CS → CSMS | Return controls in response to `GetDERControl` |
| [`NotifyDERAlarm`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm) | CS → CSMS | Report that a control is overriding normal behavior |
| [`NotifyDERStartStop`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop) | CS → CSMS | Report that a scheduled control started or stopped |

All four CSMS→CS responses (`Get`/`Set`/`Clear`) carry a [`DERControlStatusEnumType`](../OCPP-2.1-DataTypes.md#dercontrolstatusenumtype) `status`: `Accepted`, `Rejected`, `NotSupported`, or `NotFound`.

---

## 4. Set Flow

`SetDERControl` installs or updates a single control. The control-specific field must match `controlType` ([§2.3](#23-controltype--payload-field-mapping)); the station rejects a request that carries multiple controls or a mismatched field.

### 4.1 Setting a default control (e.g. frequency droop)

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | Utility → CSMS | (out of OCPP scope) | New frequency-droop parameters arrive |
| 2 | CSMS → CS | `SetDERControlRequest` | `isDefault = true`, `controlType = FreqDroop`, `freqDroop = { overFreq, underFreq, overDroop, underDroop, responseTime }`, no `startTime`/`duration` |
| 3 | CS → CSMS | `SetDERControlResponse` | `status = Accepted` |
| 4 | CS (internal) | — | Default droop becomes active immediately |

### 4.2 Setting a scheduled control (e.g. VoltVar Q(U) curve)

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `SetDERControlRequest` | `isDefault = false`, `controlType = VoltVar`, `curve = { curveData[], priority, yUnit, startTime, duration }` |
| 2 | CS → CSMS | `SetDERControlResponse` | `status = Accepted` |
| 3 | CS → CSMS | `NotifyDERStartStopRequest` | At `startTime`: `controlId`, `started = true` |
| 4 | CS (internal) | — | For `duration` seconds, station adjusts reactive power per the curve |
| 5 | CS → CSMS | `NotifyDERStartStopRequest` | At `startTime + duration`: `controlId`, `started = false`; control then deleted |

### 4.3 Response rules (`SetDERControlResponse`)

| Condition | `status` | Extra |
|-----------|----------|-------|
| `controlType` not supported by the station | `NotSupported` | — |
| Default (`isDefault=true`) sent with `startTime` and/or `duration` | `Rejected` | — |
| `EnterService` or `Gradients` sent with `isDefault=false` | `Rejected` | — |
| Multiple controls, or control object not matching `controlType` | `Rejected` | — |
| Valid; no existing control of this type | `Accepted` | — |
| Valid; supersedes existing control(s) of same type | `Accepted` | `supersededIds[]` lists the superseded `controlId`s |

The `supersededIds` array (1–24 ids) appears whenever installing this control causes others of the same type to be superseded — see [§6](#6-prioritization-and-superseding).

---

## 5. Get / Report and Clear Flows

### 5.1 Get / Report

`GetDERControl` carries a `requestId` and optional filters (`controlId`, `controlType`, `isDefault`). A missing filter matches any value. The station answers the **request** synchronously with a `GetDERControlResponse` status, then streams the matching controls in one or more asynchronous `ReportDERControlRequest` messages (CS→CSMS), each echoing the original `requestId`.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `GetDERControlRequest` | `requestId` + optional `controlId` / `controlType` / `isDefault` |
| 2 | CS → CSMS | `GetDERControlResponse` | `status = Accepted` if matches exist; see table below |
| 3 | CS → CSMS | `ReportDERControlRequest` (1..n) | Same `requestId`; `tbc = true` on every message except the last |
| 4 | CSMS → CS | `ReportDERControlResponse` | Empty `{}` ack for each report |

`GetDERControlResponse` status:

| Condition | `status` |
|-----------|----------|
| No controls match the given `isDefault` / `controlType` / `controlId` | `NotFound` |
| `controlType` is one the station does not support | `NotSupported` |
| One or more controls match | `Accepted` (reports follow) |

`ReportDERControlRequest` groups returned controls by type into arrays of "Get" wrapper types — [`DERCurveGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#dercurvegettype), [`FreqDroopGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#freqdroopgettype), [`FixedPFGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#fixedpfgettype), [`FixedVarGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#fixedvargettype), [`EnterServiceGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#enterservicegettype), [`GradientGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#gradientgettype), [`LimitMaxDischargeGetType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#limitmaxdischargegettype). Each wrapper adds the `id` (the original `controlId`), `isDefault`, and an **`isSuperseded`** flag, so the CSMS can see which installed controls are currently shadowed by a higher-priority one.

### 5.2 Clear

`ClearDERControl` removes controls. `isDefault` is **required** (clear defaults vs scheduled); `controlId` and `controlType` are optional filters.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `ClearDERControlRequest` | `isDefault` required; optional `controlId` / `controlType` |
| 2 | CS → CSMS | `ClearDERControlResponse` | status per table below |

| Condition | `status` |
|-----------|----------|
| `controlType` set + not supported by station | `NotSupported` |
| `controlType` given but never set for that `isDefault` | `NotFound` |
| `controlId` given but never set for that `isDefault` | `NotFound` |
| No `controlType`/`controlId` → clear all controls matching `isDefault` | `Accepted` |
| `controlType` matches set controls → clear them for that `isDefault` | `Accepted` |
| `controlId` matches a set control → clear it for that `isDefault` | `Accepted` |

---

## 6. Prioritization and Superseding

Two mechanisms decide which control of a given type is active. **Type** here means a specific control parameter or curve type (e.g. `FreqDroop`, `HFMustTrip`).

1. **Default vs scheduled.** A scheduled control of a type, while active, overrides the default of that type. Outside any scheduled window, the default applies.
2. **`priority` value.** Only one control of a type can be active at a time. When multiple exist, the one with the **lowest** `priority` value wins (0 = highest priority). This applies independently within defaults and within scheduled controls.

### 6.1 Superseding rules

Prioritization happens **when the message is received**, not at start time. Key rules:

| Situation | Behavior |
|-----------|----------|
| New control of a type has a lower `priority` value than an existing one **not yet started** | Existing control is superseded immediately (`isSuperseded = true`), even if the new control starts much later |
| New higher-priority control arrives while a lower-priority control of the same type is **already active** (past `startTime`) | Active control keeps running until the new control's `startTime`, then is superseded |
| New control has a **higher** `priority` value than an already-active control of the same type | New control is accepted but immediately superseded; the existing one keeps running. Its `controlId` is returned in `supersededIds`. (The CSMS should avoid sending lower-priority controls in the first place.) |
| Any control with `isSuperseded = true` | Never executed |
| Any control past `startTime + duration` | Automatically deleted by the station |

When no scheduled control of a type is active, the station executes the default control of that type that has `isSuperseded = false`.

This matches the prioritization process in the IEEE 2030.5 / CSIP profile, so a CSMS can map utility events to OCPP controls predictably. Ideally the CSMS resolves priority itself and sends only the winning control, but because network latency makes "send exactly at start time" unreliable, the station must also handle overlapping controls of differing priority.

> **ESCALATE: POLICY-DEPENDENT** — Assigning `priority` values across overlapping utility events (which event group outranks another) is a CSO/utility scheduling decision. Confirm the priority scheme with the operator before relying on superseding behavior.

---

## 7. Alarms and Start/Stop Notifications

### 7.1 `NotifyDERAlarm` — a control overrides normal behavior

When a station starts deviating from normal (dis)charging because a DER curve or setting forced it to — for example an over-frequency causing an `HFMustTrip` curve to cut export — it raises a [`NotifyDERAlarm`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm) so the CSO is aware.

| Field | Use |
|-------|-----|
| `controlType` | Which control took over (e.g. `HFMustTrip`, `LimitMaxDischarge`, `VoltVar`) |
| `timestamp` | When the event started (or ended) |
| `alarmEnded` | Absent/`false` when the alarm starts; `true` on the follow-up message when the condition clears |
| `gridEventFault` | Optional cause, one of [`GridEventFaultEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#grideventfaultenumtype) (e.g. `OverFrequency`, `UnderVoltage`, `OverCurrent`, `LocalEmergency`) |
| `extraInfo` | Optional free text (max 200), e.g. forwarded from the EV |

The station sends the alarm again with `alarmEnded = true` when the event ends. A purely reactive-power curve (e.g. `VoltVar`) typically does **not** raise an alarm, because it does not disturb the active-power profile — unless the active charging profile also specifies reactive-power behavior.

### 7.2 `NotifyDERStartStop` — scheduled control activation

When a **scheduled** control (`isDefault = false`, `isSuperseded = false`) reaches its `startTime` or its `startTime + duration`, the station reports the transition with [`NotifyDERStartStop`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop).

| Field | Use |
|-------|-----|
| `controlId` | The control that started/stopped (matches the `SetDERControlRequest` id) |
| `started` | `true` at `startTime`, `false` at `startTime + duration` |
| `timestamp` | Current time of the transition |
| `supersededIds` | If starting this control supersedes others of the same type, their ids (1–24) |

| Trigger | Message contents |
|---------|------------------|
| Scheduled control reaches `startTime` | `started = true`, `controlId` |
| ...and it supersedes an active control B | `started = true`, `controlId = A`, `supersededIds = [B]` |
| Scheduled control reaches `startTime + duration` | `started = false`, `controlId` |

`NotifyDERAlarm` and `NotifyDERStartStop` are distinct: start/stop reports the *schedule lifecycle* of a control; alarm reports that a control is *actively overriding* charging because of a grid event.

---

## 8. Offline Behavior

Block R has no offline-specific messages. DER controls are stored **persistently** on the station, so a reboot or connectivity loss does not erase them — defaults and scheduled controls keep applying on their own timelines, and the station continues enforcing grid-code behavior autonomously (that is the point of curves: autonomous reaction without a round-trip to the CSMS).

Active/reactive **power setpoints**, by contrast, ride on OCPP charging profiles, whose offline lifetime is governed by `maxOfflineDuration` / `invalidAfterOfflineDuration` in `ChargingProfileType` (V2X use cases Q11/Q12, outside block R). See the [Smart Charging](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) deep-dive for that mechanism.

> **ESCALATE: SPEC-SILENT** — The Part 2 DER chapter does not define a block-R-specific reconciliation procedure for what the CSMS should re-`Get` or re-`Set` after a station reconnects following a long outage (e.g. whether scheduled controls that elapsed while offline are reported as deleted). Confirm the expected reconciliation with the integration team.

---

## 9. Device Model: `ACDERCtrlr` & `DCDERCtrlr`

DER capabilities and the set of supported control modes live in two device-model components (see the [Device Model reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md)). Both sit at the EVSE level.

| Component | Represents | Key variables |
|-----------|-----------|---------------|
| `DCDERCtrlr` | DER capabilities ("nameplate") of the EVSE's own DC inverter | `Enabled`, `ModesSupported`, ratings (`MaxW`, `MaxVA`, `MaxVar`, `MaxVarNeg`, `MaxChargeRateW`, over/under-excited W and PF), voltage ratings (`VNom`, `MaxV`, `MinV`), inverter identity (`InverterManufacturer`/`Model`/`SerialNumber`/`SwVersion`/`HwVersion`), `IslandingDetectionMethod`, `ReactiveSusceptance` |
| `ACDERCtrlr` | DER modes the EVSE can emulate via ISO 15118-20 `ChargeLoop` to control the EV's inverter | `ModesSupported` |

`ModesSupported` (a `MemberList`) is the contract for `SetDERControl`/`GetDERControl`: the CSMS should not send (and the station will answer `NotSupported` for) a `controlType` absent from `ModesSupported` of the relevant controller. For a DC station the supported modes are the EVSE inverter's; for an AC station they are the modes the EVSE can emulate (the rest must be handled by the EV's inverter, per the V2G-AC / V2G-Split split in [§1.2](#12-relationship-to-iso-15118-20-inverter-architectures)).

> **ESCALATE: POLICY-DEPENDENT** — `Enabled` and the contents of `ModesSupported`, plus all nameplate ratings, reflect hardware capability and regulatory registration of the inverter. Treat them as configuration provided by the station vendor / CSO, not values to set arbitrarily.

---

## 10. Use Case Index

The block-R use cases (R01–R05) in the Part 2 specification map to this document as:

| Use case | Topic | Section(s) |
|----------|-------|-----------|
| R01 | Start V2X session with DER control in the EVSE (DC / AC emulation) | [§1.2](#12-relationship-to-iso-15118-20-inverter-architectures), [§7](#7-alarms-and-startstop-notifications) |
| R02 | Start V2X session with DER control in the EV (ISO 15118-20 `AC_BPT_DER`) | [§1.2](#12-relationship-to-iso-15118-20-inverter-architectures) |
| R03 | Hybrid DER control split across EV and EVSE | [§1.2](#12-relationship-to-iso-15118-20-inverter-architectures) |
| R04 | Configure DER control settings (Set / Get / Report / Clear, start/stop) | [§4](#4-set-flow), [§5](#5-get--report-and-clear-flows), [§6](#6-prioritization-and-superseding), [§7](#7-alarms-and-startstop-notifications) |
| R05 / device model | Reporting DER capabilities | [§9](#9-device-model-acderctrlr--dcderctrlr) |
