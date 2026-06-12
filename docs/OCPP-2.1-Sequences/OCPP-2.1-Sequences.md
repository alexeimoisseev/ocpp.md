# OCPP 2.1 — Sequence Flows (new / changed)

> **Purpose:** Practical reference for AI agents implementing or debugging the message flows that are new or changed in OCPP **2.1**. Each flow is a numbered step table (`Step | Sender → Receiver | Message | Trigger/Notes`). Concepts and field-level schemas live in the linked companion docs; this document is the flow ordering.

> **Last updated:** 2026-06-11

---

## How This Document Was Produced

This document covers the OCPP **2.1** sequence flows that are new or changed versus 2.0.1. Its dominant confidence tier is **spec-knowledge** — message ordering and triggers summarized in original wording from the OCPP 2.1 Edition 2 Part 2 specification (blocks K Smart Charging, R DER Control, Q Bidirectional, S Battery Swap, N Diagnostics). All message names, field names, and enum values are **schema-derived** — cross-referenced against the mechanically generated [SmartCharging](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md), [DERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md), [BatterySwap](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md), [TariffAndCost](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md), [RemoteControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md), and [Diagnostics](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md) schema docs, plus the [Data Types reference](../OCPP-2.1-DataTypes.md). No spec prose is reproduced verbatim (OCA is CC BY-ND); all text is original.

This document contains **0 escalation points**; the policy decisions touching these flows (e.g. push vs. pull dynamic-schedule updates) are flagged with `> **ESCALATE:**` markers in the companion SmartCharging and DER docs and only cross-referenced here. See [METHODOLOGY.md](../METHODOLOGY.md) for the confidence and escalation model.

**Companion documents:**
- [OCPP 2.1 Smart Charging deltas](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md) — concepts for dynamic schedules, priority charging, battery swap, periodic event streams.
- [OCPP 2.1 DER Control](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md) — DER control/curve model used in §1.
- [OCPP 2.1 Bidirectional / V2X](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) — operation modes and setpoints used in §2.
- [OCPP 2.1 Tariff & Cost](../OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md) — web-payment and tariff context for §4.
- Schema docs linked inline for every message.

---

## 1. DER Control Setup

The CSMS configures Distributed Energy Resource (DER) controls on the CS and reads back the result. Full control/curve model and enum values are in the [DER Control deep-dive](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md).

| Step | Sender → Receiver | Message | Trigger/Notes |
|------|-------------------|---------|---------------|
| 1 | CSMS → CS | [`GetDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#getdercontrol) | (Optional) CSMS reads which DER controls/curves the CS currently has, to plan changes. |
| 2 | CS → CSMS | [`ReportDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reportdercontrol) | CS reports the requested DER control settings (may be multiple, paginated by request id). |
| 3 | CSMS → CS | [`SetDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol) | CSMS installs or updates a DER control (e.g. a volt-watt or freq-watt curve). CS replies with the set status. |
| 4 | CSMS → CS | [`ClearDERControl`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#cleardercontrol) | (Optional) CSMS removes DER controls by id/type when no longer needed. |
| 5 | CS → CSMS | [`NotifyDERAlarm`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm) | (Async, if applicable) CS reports a DER-related alarm condition. |
| 6 | CS → CSMS | [`NotifyDERStartStop`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop) | (Async, if applicable) CS reports that a DER control started or stopped acting. |

---

## 2. Dynamic Schedule Update Loop

A dynamic charging profile is installed once, then its setpoints/limits are updated repeatedly without re-installing. Concept and fields are in the [Smart Charging deltas §2](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md#2-dynamic-charging-profiles--dynamic-schedules); operation-mode/setpoint semantics in the [V2X doc](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md).

| Step | Sender → Receiver | Message | Trigger/Notes |
|------|-------------------|---------|---------------|
| 1 | CSMS → CS | [`SetChargingProfile`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile) | CSMS installs a profile with `chargingProfileKind` = `Dynamic` ([`ChargingProfileKindEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilekindenumtype)). May set `dynUpdateInterval` to request CS pulls. |
| 2 | — | (charging proceeds) | CS follows the current `setpoint` / `limit` / `dischargeLimit` of the dynamic schedule periods. |
| 3a | CSMS → CS | [`UpdateDynamicSchedule`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule) | **Push path.** CSMS sends `chargingProfileId` + `scheduleUpdate` ([`ChargingScheduleUpdateType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#chargingscheduleupdatetype)) with new setpoints/limits. CS replies `status` = [`ChargingProfileStatusEnumType`](../OCPP-2.1-DataTypes.md#chargingprofilestatusenumtype). |
| 3b | CS → CSMS | [`PullDynamicScheduleUpdate`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate) | **Pull path.** On `dynUpdateInterval` (or its own logic) the CS sends `chargingProfileId`; CSMS returns `status` and optional `scheduleUpdate` in the response. |
| 4 | — | (apply update) | CS applies the new values; `dynUpdateTime` on the profile reflects the moment of update. Loop returns to step 2. |
| 5 | CSMS → CS | [`GetCompositeSchedule`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#getcompositeschedule) | (Optional) CSMS verifies the effective merged schedule after updates. |

> Steps 3a and 3b are alternatives selected per deployment, not both required. Which is used is a policy decision — see the ESCALATE note in [Smart Charging deltas §2.3](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md#23-the-two-update-messages).

---

## 3. Battery Swap

Coordinates a physical battery exchange. Concept and fields are in the [Smart Charging deltas §4](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md#4-battery-swap) and the [BatterySwap schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md).

| Step | Sender → Receiver | Message | Trigger/Notes |
|------|-------------------|---------|---------------|
| 1 | CSMS → CS | [`RequestBatterySwap`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#requestbatteryswap) | (Optional initiator) CSMS asks the station to begin a swap for `idToken`, assigning a `requestId`. CS replies `status` = [`GenericStatusEnumType`](../OCPP-2.1-DataTypes.md#genericstatusenumtype). |
| 2 | CS → CSMS | [`BatterySwap`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap) | `eventType` = `BatteryIn` ([`BatterySwapEventEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswapeventenumtype)): the driver's depleted pack has been inserted **into** the station slot. `batteryData[]` carries `evseId` (slot), `serialNumber`, `soC`, `soH`; CS assigns the `requestId`. Event names are from the station-slot perspective; default swap order is In-Out. |
| 3 | — | (charged pack offered) | Station presents/charges a charged pack for the driver to collect from the slot. |
| 4 | CS → CSMS | [`BatterySwap`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap) | `eventType` = `BatteryOut`: the charged pack has been taken **out** of the station slot by the driver. `batteryData[]` (incl. `serialNumber`, `soC`, `soH`) describes the collected pack; same `requestId` as the `BatteryIn`. |
| 5 | CS → CSMS | [`BatterySwap`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap) | (Error path) If the charged pack offered after `BatteryIn` is **not collected** within `BatterySwapOutTimeout`, CS reports `eventType` = `BatteryOutTimeout` with the same `requestId` (otherwise CSMS is left with an orphan `BatteryIn`). |

Event names follow the station-slot perspective: `BatteryIn` = a battery placed into a slot, `BatteryOut` = a battery removed from a slot. The spec default order is In-Out (depleted battery in first, charged battery out second); a station using the reverse order reports `BatterySwapCtrlr.SwapOrder` = `Out-In`. A CS-initiated swap (no `RequestBatterySwap`) simply starts at step 2; the `requestId` then correlates the `BatteryIn`/`BatteryOut` pair.

---

## 4. Web-Payment Start

A driver pays via a web flow (e.g. scanning a QR code) and the transaction is started remotely. Tariff/cost context is in the [Tariff & Cost doc](../OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md).

| Step | Sender → Receiver | Message | Trigger/Notes |
|------|-------------------|---------|---------------|
| 1 | CSMS → CS | [`NotifyWebPaymentStarted`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifywebpaymentstarted) | CSMS tells the CS a web-payment flow has begun for `evseId`, with a `timeout` (seconds) after which no result is expected. CS may display "payment in progress". |
| 2 | — | (driver completes payment) | Web/QR payment authorized out-of-band; CSMS receives confirmation from the payment back-end. |
| 3 | CSMS → CS | [`RequestStartTransaction`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction) | On successful payment within `timeout`, CSMS remotely starts the transaction on that EVSE. CS replies with the start status. |
| 4 | CS → CSMS | [`TransactionEvent`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) | CS reports the transaction `Started` event as usual. |
| — | — | (timeout path) | If no payment confirmation arrives before `timeout`, the CSMS does not send `RequestStartTransaction`; the CS clears the "payment in progress" state. |

---

## 5. Periodic Event Stream Lifecycle

Efficient high-rate telemetry. Concept and the five messages are in the [Smart Charging deltas §5](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md#5-periodic-event-streams) and the [Diagnostics schema doc](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md).

| Step | Sender → Receiver | Message | Trigger/Notes |
|------|-------------------|---------|---------------|
| 1 | CS → CSMS | [`OpenPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#openperiodiceventstream) | CS opens a stream with `constantStreamData` ([`ConstantStreamDataType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#constantstreamdatatype)): stream `id`, `variableMonitoringId`, and `params` ([`PeriodicEventStreamParamsType`](../OCPP-2.1-DataTypes.md#periodiceventstreamparamstype): `interval`, `values`). CSMS replies `Accepted`/`Rejected`. |
| 2 | CS → CSMS | [`NotifyPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream) | **One-way SEND, repeated.** CS pushes a batch: `basetime`, `data[]` ([`StreamDataElementType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#streamdataelementtype): offset `t`, value `v`), stream `id`, `pending` count. No response. |
| 3 | CSMS → CS | [`GetPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getperiodiceventstream) | (Optional) CSMS asks the CS for the list of configured streams (`constantStreamData[]`). |
| 4 | CSMS → CS | [`AdjustPeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#adjustperiodiceventstream) | (Optional) CSMS re-paces a stream by `id` with new `params`. CS replies `Accepted`/`Rejected`; subsequent batches follow the new rate. |
| 5 | CS → CSMS | [`ClosePeriodicEventStream`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#closeperiodiceventstream) | CS closes the stream by `id` when the monitored situation ends. No further `NotifyPeriodicEventStream` for that `id`. |
