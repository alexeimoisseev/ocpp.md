# OCPP 2.1 — Bidirectional Power Transfer (V2X) Deep-Dive

> **Purpose:** Practical reference for AI agents implementing or debugging OCPP 2.1 bidirectional power transfer (V2X). Covers what V2X is, the operation-mode model, setpoints and charge/discharge limits, mode switching and entry/exit flows, frequency support (FCR / aFRR), allowed-energy-transfer negotiation, and offline behavior. Functional Block Q.

> **Last updated:** 2026-06-09

---

## How This Document Was Produced

This document covers OCPP 2.1 Functional Block Q (Bidirectional Power Transfer / V2X). Its dominant confidence tier is **spec-knowledge** — behavioral rules summarized from the OCPP 2.1 Edition 2 Part 2 specification, section Q (use cases Q01–Q12). All message names, field names, and enum values are **schema-derived**: cross-referenced against the mechanically generated [Bidirectional schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md), the [SmartCharging schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md), and the [Data Types reference](../OCPP-2.1-DataTypes.md). Where a behavior depends on grid-operator, market, or vendor policy, it is marked as an escalation point rather than asserted.

This document contains **5 escalation points** marked with `> **ESCALATE: POLICY-DEPENDENT**`. When an AI agent encounters one, it MUST stop and ask the developer/operator to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [Bidirectional Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md) — field-level schemas for the two Block Q messages (`NotifyAllowedEnergyTransfer`, `AFRRSignal`)
- [Smart Charging Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md) — `SetChargingProfile`, `UpdateDynamicSchedule`, `PullDynamicScheduleUpdate`, `NotifyEVChargingNeeds`, and the charging-profile model V2X builds on (Block K)
- [Data Types Reference](../OCPP-2.1-DataTypes.md) — `OperationModeEnumType`, `EnergyTransferModeEnumType`, `ChargingSchedulePeriodType`, `V2XFreqWattPointType`, `V2XSignalWattPointType`

---

## 1. What V2X Is and Why 2.1 Adds It

**Bidirectional power transfer** lets an EV not only draw power from the grid but also export power back. OCPP 2.1 introduces this as Functional Block Q. The spec uses the umbrella term **V2X** ("vehicle-to-anything") rather than V2G, to avoid colliding with ISO 15118's own use of "V2G" for the EV↔Charging-Station link.

V2X variants (all handled identically in OCPP — only the destination of the exported power differs):

| Term | Meaning |
|------|---------|
| V2G | Vehicle-to-grid: export power to the electricity grid |
| V2H | Vehicle-to-home: power a home, e.g. during a grid outage or to avoid grid draw |
| V2B | Vehicle-to-building: power a building, same idea at building scale |
| V2L | Vehicle-to-load: power an appliance directly — **out of scope for OCPP**, no CSMS involvement |

Why it was added: a parked EV is a large battery. Letting it discharge enables grid balancing services (frequency reserves), local load balancing against on-site generation (e.g. solar), backup power, and energy arbitrage — turning charging infrastructure into a flexible grid resource.

### Relationship to ISO 15118-20

V2X over OCPP requires a bidirectional-capable EV-to-station protocol. The spec defines Block Q for use when the EV↔station link is **ISO 15118-20** or **CHAdeMO**. ISO 15118-20 carries the service negotiation (the EV and station agree on a bidirectional energy-transfer service); OCPP carries the authorization of that service and the control loop (setpoints/limits) between station and CSMS. Prerequisite control variables: `ISO15118Ctrlr.Enabled = true` and `V2XChargingCtrlr.Enabled = true`.

### Block Q Messages

Only two messages are unique to Block Q. V2X control itself reuses the Smart Charging (Block K) machinery.

| Message | Direction | Purpose |
|---------|-----------|---------|
| [`NotifyAllowedEnergyTransfer`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer) | CSMS → CS | Tell the CS which energy-transfer modes are allowed for a transaction (see §6) |
| [`AFRRSignal`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#afrrsignal) | CSMS → CS | Push an aFRR activation signal value to the CS (see §5) |

V2X **control** is expressed through charging profiles delivered by [`SetChargingProfile`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile) and updated by [`UpdateDynamicSchedule`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule) / [`PullDynamicScheduleUpdate`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate). The allowed transfer modes are negotiated via [`NotifyEVChargingNeeds`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds). This document cross-links those rather than duplicating their schemas.

---

## 2. V2X Operation Modes

The mode of operation for each schedule interval is set by the `operationMode` field of [`ChargingSchedulePeriodType`](../OCPP-2.1-DataTypes.md#chargingscheduleperiodtype). The enum is [`OperationModeEnumType`](../OCPP-2.1-DataTypes.md#operationmodeenumtype). When `operationMode` is absent it defaults to `ChargingOnly`.

The eight values (the first four are shared with regular smart charging; the others are V2X-specific):

| `operationMode` value | Who determines the control value | Bidirectional? | Notes |
|-----------------------|----------------------------------|----------------|-------|
| `ChargingOnly` | CS follows `limit` only | No | Default. Charge-only; used as a safe starting mode before V2X is authorized. `setpoint`/`dischargeLimit` not used. |
| `ExternalSetpoint` | External actor (e.g. EMS) sets the setpoint | Yes (setpoint may be negative) | CSMS may still bound it with `limit` and `dischargeLimit`. |
| `ExternalLimits` | External actor sets `limit` and `dischargeLimit` | Yes | Like `ExternalSetpoint` but the limits, not the setpoint, are externally driven. |
| `CentralSetpoint` | CSMS sets `setpoint` in the schedule period | Yes (negative = discharge) | With `chargingProfileKind = Dynamic`, CSMS updates `setpoint` via `UpdateDynamicSchedule` without resending the profile. `limit`/`dischargeLimit` not used. |
| `CentralFrequency` | CSMS computes setpoint from centrally measured frequency | Yes | For calibrated frequency metering done centrally. Requires `chargingProfileKind = Dynamic`; CSMS pushes new setpoints continually. If no update arrives in time, the profile terminates and the CS falls back to a lower stack level. |
| `LocalFrequency` | CS computes setpoint locally from a frequency-watt curve | Yes | FCR / aFRR participation. Requires `chargingRateUnit = W`. Uses `v2xFreqWattCurve` (FCR) and/or `v2xSignalWattCurve` + `AFRRSignal` (aFRR). See §5. |
| `LocalLoadBalancing` | CS computes setpoint locally from a metered building load | Yes | EV compensates building load (e.g. against solar). Controlled by configuration keys `UpperThreshold`, `LowerThreshold`, `UpperOffset`, `LowerOffset` (require `UpperThreshold > LowerThreshold`). |
| `Idle` | Neither charge nor discharge | No (suspended) | EV refrains from charging/discharging for the interval. `limit`, `dischargeLimit`, `setpoint`, `setpointReactive` MUST be absent. Optional battery preconditioning (`preconditioningRequest`) and EVSE sleep (`evseSleep`) — see §7. |

> **ESCALATE: POLICY-DEPENDENT** — Which operation modes to enable for a given site or EV is an operator/market decision. Discharging modes may require third-party (eMSP / aggregator / grid-operator) authorization, contracts, or grid-code compliance. Do not enable `*Setpoint`, `*Frequency`, or `LocalLoadBalancing` modes by default; confirm the operator's V2X service policy first.

---

## 3. Setpoints and Charge/Discharge Limits

V2X reuses the charging-profile model but extends [`ChargingSchedulePeriodType`](../OCPP-2.1-DataTypes.md#chargingscheduleperiodtype) with bidirectional fields. All values are in the schedule's `chargingRateUnit` (Watts or Amperes).

| Field | Sign convention | Meaning |
|-------|-----------------|---------|
| `setpoint` | Positive = charge, negative = discharge | Target rate the EV should follow as closely as possible. |
| `limit` | Positive only | Maximum allowed **charging** rate. |
| `dischargeLimit` | Negative only (schema constraint `max: 0.0`) | Maximum allowed **discharging** rate (a floor, since it is negative). |
| `setpointReactive` | Positive = inductive, negative = capacitive | Reactive-power (or current) setpoint. |

Phase-specific variants exist for AC: `setpoint_L2` / `setpoint_L3`, `limit_L2` / `limit_L3`, `dischargeLimit_L2` / `dischargeLimit_L3`, `setpointReactive_L2` / `setpointReactive_L3`. When the L2/L3 fields are present, the un-suffixed field represents L1; otherwise it represents the sum of all phases.

When a `setpoint` is given together with `limit` and/or `dischargeLimit`, any overshoot while tracking the setpoint must stay within those bounds. Which fields are required vs. ignored depends on `operationMode` (see the per-mode notes in §2).

Frequency-support curve fields (used by the frequency modes, §5):

| Field | Type | Meaning |
|-------|------|---------|
| `v2xFreqWattCurve` | [`V2XFreqWattPointType`](../OCPP-2.1-DataTypes.md#v2xfreqwattpointtype)[] (1–20 points) | Power/frequency (FCR) curve: each point is `{frequency` (Hz)`, power` (W; +charge / −discharge)`}`. Values between points are linearly interpolated. |
| `v2xSignalWattCurve` | [`V2XSignalWattPointType`](../OCPP-2.1-DataTypes.md#v2xsignalwattpointtype)[] (1–20 points) | Signal/watt (aFRR) curve: each point is `{signal` (integer)`, power` (W)`}`. Maps an `AFRRSignal.signal` value to a power level. |
| `v2xBaseline` | number | Baseline power on top of which `v2xFreqWattCurve` / `v2xSignalWattCurve` outputs are added. |

For the full charging-profile structure, stack-level priority, and `chargingProfileKind` (`Absolute` / `Recurring` / `Relative` / `Dynamic`), see the [SmartCharging schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md). V2X does not change those mechanics; it only adds the fields above and the V2X `operationMode` values.

> **ESCALATE: POLICY-DEPENDENT** — Concrete discharge-limit values (`dischargeLimit`) and the maximum export power for a site depend on the grid connection capacity, the EV/battery warranty terms, and any local export agreement. These must come from the operator/grid configuration, not be inferred.

---

## 4. Switching Modes / Entering and Leaving V2X

### 4.1 Authorizing and entering V2X (Q01)

Because a V2X energy service often needs third-party authorization that may not complete within the EV's ISO 15118-20 timeout, the recommended pattern is to **start in `ChargingOnly`** and renegotiate to V2X once the allowed transfer modes are known (see §4.2). Direct entry (Q01) when V2X is pre-authorized:

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CS → CSMS | `Authorize` | EV plugged in; CS includes the ISO 15118 EVCCID in `idToken.additionalInfo`. |
| 2 | CSMS → CS | `Authorize` (response) | `idTokenInfo.status = Accepted`, plus the `allowedEnergyTransfer` list for this EV. |
| 3 | CS → CSMS | `TransactionEvent` (`eventType = Started`) | Transaction begins. |
| 4 | — | (ISO 15118-20 service negotiation) | EV and CS agree on an energy-transfer method. |
| 5 | CS → CSMS | [`NotifyEVChargingNeeds`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds) | Carries the chosen `requestedEnergyTransfer` (and optional `availableEnergyTransfer` list), `departureTime`, and control mode. |
| 6 | CSMS → CS | `NotifyEVChargingNeeds` (response) | `status = Accepted` (a `SetChargingProfile` will follow) or `NoChargingProfile` (CS should use its `TxDefaultProfile`). |
| 7 | CSMS → CS | [`SetChargingProfile`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile) | Profile whose schedule has a V2X `operationMode` (anything other than `ChargingOnly`). Skipped if step 6 returned `NoChargingProfile`. |
| 8 | — | (CS → EV) | CS relays charge/discharge parameters to EV; EV requests V2X power transfer; CS accepts. V2X operation active. |

**Error handling (Q01):** if the CSMS does not accept the `requestedEnergyTransfer`, it responds to `NotifyEVChargingNeeds` with `status = Rejected` and the CS stops the transaction.

### 4.2 Safe-start then enable V2X (Q02)

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `SetChargingProfile` | Schedule with `operationMode = ChargingOnly` — transaction starts charge-only while V2X authorization is pending. |
| 2 | CSMS → CS | [`NotifyAllowedEnergyTransfer`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer) | Once a V2X mode is authorized, CSMS updates the allowed list for the EVSE/transaction (includes a V2X `EnergyTransferModeEnumType`, e.g. `DC_BPT`). |
| 3 | CS → CSMS | `NotifyAllowedEnergyTransfer` (response) | `status = Accepted`. |
| 4 | — | (ISO 15118-20 service renegotiation) | EV/CS renegotiate to the V2X service. |
| 5 | CSMS → CS | `SetChargingProfile` | New/updated profile with a V2X `operationMode`; bidirectional operation begins. |

### 4.3 Leaving / falling back

A mode change is just a new schedule period or a higher-priority profile expiring. Two key fallbacks:
- **Dynamic timeout** (`CentralSetpoint` / `CentralFrequency`): if no `UpdateDynamicSchedule` arrives within `chargingSchedule.duration`, the schedule ends and the CS falls back to the next valid (lower stack-level) profile. For `CentralFrequency` this may be a `LocalFrequency` profile, so frequency support continues locally (Q08) until central updates resume.
- **Offline**: see §7.

---

## 5. Frequency Support — FCR and aFRR

Two grid-balancing products are supported, both through frequency-related operation modes. Both require `chargingRateUnit = W`.

### 5.1 FCR (Frequency Containment Reserve), via `LocalFrequency`

FCR (primary control reserve) reacts automatically within seconds to grid frequency deviations. In OCPP the CS reads grid frequency locally and derives the power setpoint from a power/frequency curve carried in `v2xFreqWattCurve`. Power for frequencies between curve points is computed by linear interpolation. No per-tick OCPP message is needed once the curve is installed — control is fully local.

### 5.2 aFRR (automatic Frequency Restoration Reserve)

aFRR is the secondary reserve; it gradually replaces FCR after ~30 s, must be fully available within 15 minutes once activated, and must track a new setpoint every few seconds. Activation comes from the TSO to the operator (CSO), which forwards it to affected stations as an [`AFRRSignal`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#afrrsignal).

`AFRRSignal` (CSMS → CS):

| Field | Type | Meaning |
|-------|------|---------|
| `signal` | integer | A signal value; the CS maps it to a power level via the `v2xSignalWattCurve` in the active schedule period. |
| `timestamp` | date-time | The moment the signal becomes active. |

Response uses [`GenericStatusEnumType`](../OCPP-2.1-DataTypes.md#genericstatusenumtype) (`Accepted` / `Rejected`). The amount of upward/downward aFRR offered by a station is encoded in `v2xSignalWattCurve` ([`V2XSignalWattPointType`](../OCPP-2.1-DataTypes.md#v2xsignalwattpointtype)[]): each point maps a `signal` integer to a `power` value.

**Q07 vs Q08:** `CentralFrequency` (Q07) has the CSMS compute and push the setpoint via `UpdateDynamicSchedule` (used when calibrated central metering is required); `LocalFrequency` (Q08) has the CS compute it locally from its curves. Note these V2X frequency modes are distinct from the frequency-droop / frequency-Watt features in **Block R (DER Control)** — in Block Q frequency support is the profile's primary goal, whereas in Block R it exists to satisfy grid-code requirements.

> **ESCALATE: POLICY-DEPENDENT** — Participation in FCR/aFRR markets, the prequalified power offered, and the contents of `v2xFreqWattCurve` / `v2xSignalWattCurve` are commercial/grid-operator decisions (TSO contracts, prequalification). Do not synthesize curve values or enable frequency modes without the operator's market configuration.

---

## 6. Allowed Energy Transfer

`NotifyAllowedEnergyTransfer` (CSMS → CS) tells the CS which energy-transfer modes are permitted for a specific transaction. It is sent when the set of allowed modes changes — typically after V2X authorization completes, or whenever an external/aggregating actor updates what this EV may do (the safe-start flow in §4.2).

Request fields:

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `allowedEnergyTransfer` | [`EnergyTransferModeEnumType`](../OCPP-2.1-DataTypes.md#energytransfermodeenumtype)[] (minItems 1) | Yes | The modes the CSMS accepts for this transaction. |
| `transactionId` | string (≤36) | Yes | The transaction the allowance applies to. |

Response uses [`NotifyAllowedEnergyTransferStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransferstatusenumtype) (`Accepted` / `Rejected`).

[`EnergyTransferModeEnumType`](../OCPP-2.1-DataTypes.md#energytransfermodeenumtype) values (the `_BPT` suffix denotes Bidirectional Power Transfer; `_DER` denotes DER-capable; `_ACDP` is automatic connection device / pantograph):

| Value | Bidirectional? | Notes |
|-------|----------------|-------|
| `AC_single_phase` | No | Unidirectional AC, 1-phase |
| `AC_two_phase` | No | Unidirectional AC, 2-phase |
| `AC_three_phase` | No | Unidirectional AC, 3-phase |
| `DC` | No | Unidirectional DC |
| `AC_BPT` | Yes | Bidirectional AC |
| `AC_BPT_DER` | Yes | Bidirectional AC with DER capability |
| `AC_DER` | No (DER) | AC with DER capability |
| `DC_BPT` | Yes | Bidirectional DC |
| `DC_ACDP` | No | DC via automatic connection device (pantograph) |
| `DC_ACDP_BPT` | Yes | Bidirectional DC via automatic connection device |
| `WPT` | No | Wireless power transfer |

The same enum also appears in `Authorize` (the `allowedEnergyTransfer` returned to the CS) and in `NotifyEVChargingNeeds` (`requestedEnergyTransfer` / `availableEnergyTransfer`), tying authorization, EV negotiation, and the standalone notify message together.

> **ESCALATE: POLICY-DEPENDENT** — Which `EnergyTransferModeEnumType` values to place in `allowedEnergyTransfer` for a given EV/transaction is an authorization/market decision (per-EV contracts, aggregator rules, eMSP approval). Do not default to including `_BPT` modes; obtain the operator's allow-list logic.

---

## 7. Idle Mode, Preconditioning, and EVSE Sleep (Q10)

`operationMode = Idle` requests the EV to neither charge nor discharge for the interval. The fields `limit`, `dischargeLimit`, `setpoint`, and `setpointReactive` (and their L2/L3 variants) MUST be absent; a `SetChargingProfile` that includes them with `Idle` is rejected with `status = Rejected`, `statusInfo.reasonCode = "InvalidSchedule"`.

Two optional refinements on `ChargingSchedulePeriodType` during Idle:

| Field | Effect |
|-------|--------|
| `preconditioningRequest` | If true, EV keeps the battery preconditioned (optimal temperature) for the interval — may draw some power. |
| `evseSleep` | If true (and `SmartChargingCtrlr.SupportsEvseSleep` is true), the EVSE turns off the power electronics/modules for this transaction until an event requires reactivation (e.g. next period's mode change, a new profile including one with 0 W limits, or transaction stop). While sleeping, the CS reports `evseSleep = true` in `TransactionEvent`; any charging command — including a 0 W limit/setpoint — wakes it. If `evseSleep` is unsupported, the CS ignores it and reports `evseSleep = false`/absent. |

---

## 8. Offline V2X Behavior (Q11 / Q12)

Whether a V2X operation may continue while the CS is offline is governed by two fields on the profile ([`ChargingProfileType`](../OCPP-2.1-DataTypes.md#chargingprofiletype) in Block K), not by anything Block-Q-specific:

| Field | Meaning |
|-------|---------|
| `maxOfflineDuration` | How long (seconds) the profile stays valid after the CS detects it is offline. The countdown starts at the moment the CS detects the offline condition (expected within ~30 s). |
| `invalidAfterOfflineDuration` | If true, once `maxOfflineDuration` has elapsed the profile is permanently invalid and is NOT reactivated when the CS comes back online. |

### 8.1 Going offline (Q11)

| Step | Actor | Behavior |
|------|-------|----------|
| 1 | CS | V2X operation active; CS loses connection to CSMS. |
| 2 | CS | Detects offline; starts the `maxOfflineDuration` countdown. |
| 3 | CS | While `t ≤ maxOfflineDuration`: continue the active V2X profile. |
| 4 | CS | When `t > maxOfflineDuration`: profile becomes invalid; fall back to the next valid (lower stack-level) profile — which may itself be a V2X profile if its own `maxOfflineDuration` has not elapsed. |
| 5 | CS | If there is no profile to fall back to, continue charging without a profile (charge-only, no limits). |
| 6 | CSMS | On detecting the offline situation, assume the CS has reverted; do **not** try to compute the exact switch moment from `maxOfflineDuration` (CS and CSMS detect offline at different instants). |

### 8.2 Resuming after offline (Q12)

On reconnection the CS re-evaluates its profiles:

| Case | Condition | Result on reconnect |
|------|-----------|---------------------|
| 1 | `t ≤ maxOfflineDuration` | V2X profile stayed active throughout; nothing changes. |
| 2 | `t > maxOfflineDuration`, `invalidAfterOfflineDuration = false` | CS had fallen back to the lower (charge-only) profile while offline; on reconnect it re-selects the higher V2X profile and resumes V2X. |
| 3 | `t > maxOfflineDuration`, `invalidAfterOfflineDuration = true` | The V2X profile is permanently ineligible; CS continues with the lower charge-only profile. |

> **ESCALATE: POLICY-DEPENDENT** — `maxOfflineDuration` and `invalidAfterOfflineDuration` for V2X profiles are risk/operational decisions: how long an EV may keep discharging without CSMS supervision, and whether stale V2X authorization may resume. Set these per the operator's offline-risk policy; do not pick defaults that allow unbounded offline discharge.

---

## 9. Common Pitfalls (interpretation)

- **Wrong sign**: `setpoint` and `dischargeLimit` are negative for discharging; `limit` is positive-only. Sending a positive `dischargeLimit` violates the schema (`max: 0.0`).
- **`Idle` with values**: including `limit`/`setpoint`/etc. with `operationMode = Idle` is rejected (`InvalidSchedule`).
- **Frequency modes need Watts**: `LocalFrequency` / `CentralFrequency` require `chargingRateUnit = W`.
- **Dynamic modes need updates**: `CentralSetpoint` and `CentralFrequency` rely on `chargingProfileKind = Dynamic` and timely `UpdateDynamicSchedule`; without them the schedule expires and the CS falls back.
- **Don't treat Block R as Block Q frequency support**: DER Control (Block R) frequency-Watt/droop is for grid-code compliance, not V2X market participation.
