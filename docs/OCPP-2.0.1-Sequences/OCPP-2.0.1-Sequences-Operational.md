# OCPP 2.0.1 — Operational Message Flows

> **Purpose:** Step-by-step message flows for operational OCPP 2.0.1 scenarios: reservations, offline behavior, firmware updates, and report pagination. Optimized for AI agent consumption. Complements the [core flows](./OCPP-2.0.1-Sequences.md) document (boot, auth, transactions).

> **Last updated:** 2026-02-07

---

## How This Document Was Produced

This document covers operational OCPP 2.0.1 message flows: reservations, offline queueing and replay, firmware updates, and report pagination. Its dominant confidence tier is **spec-knowledge** — behavioral sequences from the OCPP 2.0.1 specification Part 2, known via AI training data. Firmware status enum values are **schema-derived** (cross-referenced against the [schema documentation](../OCPP-2.0.1-Schemas/) and [data types reference](../OCPP-2.0.1-DataTypes.md), mechanically extracted from the official OCA JSON schemas). The reconnection backoff formula (§2.3) is **spec-knowledge**.

This document contains **2 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [Core Flows](./OCPP-2.0.1-Sequences.md) — boot, authorization, transaction lifecycle
- [Reservation Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md) — ReserveNow, CancelReservation, ReservationStatusUpdate field-level details
- [Firmware Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md) — UpdateFirmware, FirmwareStatusNotification field-level details
- [Provisioning Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) — GetBaseReport, NotifyReport field-level details
- [Diagnostics Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md) — GetLog, LogStatusNotification, monitoring
- [Data Types Reference](../OCPP-2.0.1-DataTypes.md) — IdTokenType, IdTokenInfoType, EVSEType

---

## 1. Reservation → Transaction

Reservations hold an EVSE for a specific user within a time window. Requires `ReservationCtrlr.Enabled` = true.

For field schemas: [ReserveNow](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md#reservenow), [CancelReservation](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md#cancelreservation), [ReservationStatusUpdate](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md#reservationstatusupdate).

### 1.1 Making a Reservation

1. CSMS sends `ReserveNow` (CSMS→CS) with `id` (reservation ID), `expiryDateTime`, `idToken`, and optionally `evseId` and/or `connectorType`.
2. CS responds with `ReserveNowResponse`:
   - `Accepted` — reservation created.
   - `Occupied` — EVSE is currently in use.
   - `Faulted` — EVSE has a fault.
   - `Unavailable` — EVSE is set to inoperative.
   - `Rejected` — other reason (e.g., reservations not supported).
3. If Accepted, CS sends `StatusNotification` with `connectorStatus: Reserved` for the reserved EVSE.
4. If `evseId` is omitted but `connectorType` is provided, CS picks an EVSE with a matching connector.
5. If `groupIdToken` is provided in `ReserveNow`, any token in that group can use the reservation.

### 1.2 Using a Reservation (Reservation → Transaction)

1. User arrives and presents token at the reserved EVSE.
2. CS sends `Authorize` → CSMS responds `Accepted`.
3. CS matches the `idToken` (or `groupIdToken`) to the active reservation.
4. User plugs in cable.
5. CS sends `TransactionEvent(Started)` with `reservationId` field set to the reservation `id`. This links the transaction to the reservation.
6. Reservation is consumed — connector status transitions from `Reserved` to `Occupied`.
7. Transaction proceeds normally (see [Core Flows §3](./OCPP-2.0.1-Sequences.md#3-transaction-lifecycle)).

### 1.3 Reservation Expiry

If the user doesn't arrive before `expiryDateTime`:
1. CS sends `ReservationStatusUpdate` (CS→CSMS) with `reservationId` and `reservationUpdateStatus: Expired`.
2. CS sends `StatusNotification` with `connectorStatus: Available`.

`ReservationUpdateStatusEnumType` values: `Expired`, `Removed`.

### 1.4 Reservation Cancellation

1. CSMS sends `CancelReservation` (CSMS→CS) with `reservationId`.
2. CS responds `Accepted` or `Rejected` (`CancelReservationStatusEnumType`).
3. If Accepted, CS sends `StatusNotification` with `connectorStatus: Available`.

### 1.5 Reservation Configuration

| Component | Variable | Purpose |
|-----------|----------|---------|
| `ReservationCtrlr` | `Enabled` | Whether CS supports reservations |
| `ReservationCtrlr` | `NonEvseSpecific` | Whether reservations without `evseId` are supported |

---

## 2. Offline Queueing and Replay

When the WebSocket connection to the CSMS is lost, the CS continues operating and queues messages for delivery upon reconnection.

### 2.1 Offline Behavior Rules

**What the CS does when disconnected:**
- Continues charging active transactions (does not stop them).
- Authorizes new tokens using local resources (see §2.2).
- Queues all `TransactionEvent` messages locally with `offline: true`.
- Preserves `seqNo` ordering — numbers continue incrementing as if online.
- May also queue `StatusNotification`, `FirmwareStatusNotification`, and other CS→CSMS messages.

**What happens upon reconnection:**
1. CS re-establishes WebSocket connection (with backoff — see §2.3).
2. CS sends `BootNotification` → must get `Accepted` before anything else.
3. CS sends `StatusNotification` per connector (current state).
4. CS replays queued messages **in original order**, one at a time (standard single-outstanding-CALL rule).
5. Each queued `TransactionEvent` has `offline: true` so the CSMS knows it occurred during disconnection.
6. CSMS uses `seqNo` to detect gaps — if seqNo jumps (e.g., 3 → 6), the CSMS knows events 4 and 5 were lost.

> **ESCALATE: SPEC-SILENT** — What happens when the CSMS rejects a replayed `TransactionEvent`? (e.g., CSMS lost its data and doesn't recognize the `transactionId`). The spec defines replay order but not error recovery.
> An AI agent MUST NOT choose error recovery behavior without asking the developer:
> 1. Drop the rejected event and continue replaying remaining queued events
> 2. Stop replay and alert the operator immediately (safest, but blocks other queued events)
> 3. Re-queue the rejected event and retry later with backoff (risk of infinite loop if CSMS won't accept)

### 2.2 Offline Authorization Decision Logic

```
if AuthCacheCtrlr.Enabled AND token in cache AND not expired:
    → use cached status
elif AuthCtrlr.LocalAuthorizeOffline AND token in local list:
    → use local list status
elif AuthCtrlr.OfflineTxForUnknownIdEnabled:
    → accept (allow unknown tokens offline)
else:
    → reject
```

| Component | Variable | Purpose |
|-----------|----------|---------|
| `AuthCtrlr` | `LocalAuthorizeOffline` | Use local list when offline |
| `AuthCtrlr` | `OfflineTxForUnknownIdEnabled` | Allow unknown tokens offline |
| `AuthCacheCtrlr` | `Enabled` | Whether auth cache is active |

### 2.3 Reconnection Backoff

To prevent thundering herd when a CSMS restarts:

```
wait_time = RetryBackOffWaitMinimum + random(0, RetryBackOffRandomRange)
```

Repeat up to `RetryBackOffRepeatTimes` times.

| Variable | Purpose |
|----------|---------|
| `OCPPCommCtrlr.RetryBackOffWaitMinimum` | Minimum wait before reconnecting (seconds) |
| `OCPPCommCtrlr.RetryBackOffRandomRange` | Random range added (seconds) — prevents simultaneous reconnection |
| `OCPPCommCtrlr.RetryBackOffRepeatTimes` | Number of retry attempts |

### 2.4 GetTransactionStatus (CSMS Checking for Queued Messages)

After reconnection, the CSMS can query whether the CS has queued messages:

1. CSMS sends `GetTransactionStatus` (CSMS→CS) with optional `transactionId`.
2. CS responds with:
   - `messagesInQueue: true/false` — whether queued messages remain for this transaction.
   - `ongoingIndicator: true/false` — whether the transaction is still active.

This is optional — the CSMS can also simply wait for queued events to arrive.

---

## 3. Firmware Update

The CSMS instructs the CS to download and install new firmware. Progress is reported through `FirmwareStatusNotification` messages.

For field schemas: [UpdateFirmware](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md#updatefirmware), [FirmwareStatusNotification](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md#firmwarestatusnotification).

### 3.1 Update Flow Steps

1. CSMS sends `UpdateFirmware` (CSMS→CS) with `requestId`, `firmware` (location URL, retrieveDateTime, optional signature/signingCertificate, optional installDateTime), and optionally `retries` and `retryInterval`.
2. CS responds with `UpdateFirmwareResponse`:
   - `Accepted` — will proceed with update.
   - `Rejected` — cannot update now.
   - `AcceptedCanceled` — accepted but a previous update was canceled.
   - `InvalidCertificate` / `RevokedCertificate` — signing cert issue.
3. CS waits until `firmware.retrieveDateTime` (if in the future).
4. CS sends status notifications via `FirmwareStatusNotification` (CS→CSMS) with `requestId` to correlate to the original request.

### 3.2 Status Progression (Happy Path)

```
Downloading → Downloaded → [SignatureVerified] → Installing → Installed → [CS reboots] → BootNotification(reason: FirmwareUpdate)
```

`SignatureVerified` only appears if `firmware.signature` was provided. Without a signature: `Downloaded` → `Installing` directly.

### 3.3 Status Progression with Errors

**Download failure with retry:**
```
Downloading → DownloadFailed → [wait retryInterval] → Downloading → Downloaded → ...
```
CS retries up to `retries` times, waiting `retryInterval` seconds between attempts. If `retries` is omitted, CS decides its own policy.

**Signature verification failure:**
```
Downloaded → InvalidSignature → [may retry download]
```

**Installation failure:**
```
Installing → InstallationFailed
```
or:
```
Installing → InstallVerificationFailed
```

### 3.4 Deferred Installation

If `firmware.installDateTime` is set (future time) or there are active transactions:
```
Downloaded → InstallScheduled → [wait for installDateTime AND no active transactions] → Installing → Installed
```

The CS should not interrupt active transactions to install firmware.

> **ESCALATE: POLICY-DEPENDENT** — "Should not interrupt" active transactions is a soft recommendation. The concrete strategy is a policy decision.
> An AI agent MUST NOT choose firmware installation timing without asking the developer:
> 1. Wait indefinitely for all transactions to end (safest, but may never install if station is always busy)
> 2. Wait up to N hours then force-install, interrupting remaining transactions (set N based on site policy)
> 3. Schedule installation for a maintenance window (e.g., 2 AM) regardless of transaction state

### 3.5 FirmwareStatusEnumType — Complete Reference

| Status | Meaning |
|--------|---------|
| `Idle` | No firmware update in progress |
| `Downloading` | Download in progress |
| `Downloaded` | Download completed successfully |
| `DownloadScheduled` | Download will start at `retrieveDateTime` |
| `DownloadPaused` | Download paused |
| `DownloadFailed` | Download failed — may retry |
| `SignatureVerified` | Signature verified successfully |
| `InvalidSignature` | Signature verification failed — may retry |
| `Installing` | Installation in progress |
| `Installed` | Installation completed |
| `InstallRebooting` | Rebooting as part of installation |
| `InstallScheduled` | Install deferred to `installDateTime` |
| `InstallationFailed` | Installation failed |
| `InstallVerificationFailed` | Post-install verification failed |

**`UpdateFirmwareStatusEnumType` (initial response):** `Accepted`, `Rejected`, `AcceptedCanceled`, `InvalidCertificate`, `RevokedCertificate`.

### 3.6 After Reboot

After firmware installation and reboot, the CS sends `BootNotification` with `reason: FirmwareUpdate`. The CSMS can then verify the new firmware version from the `chargingStation` fields.

---

## 4. GetBaseReport → NotifyReport Pagination

When the CSMS requests a device model report, the CS sends it in paginated `NotifyReport` messages using the `seqNo` / `tbc` pattern.

For field schemas: [GetBaseReport](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md#getbasereport), [NotifyReport](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md#notifyreport).

### 4.1 Flow Steps

1. CSMS sends `GetBaseReport` (CSMS→CS) with `requestId` (integer) and `reportBase` (what to report).
2. CS responds with `GetBaseReportResponse` — `status: Accepted` or `Rejected`/`NotSupported`/`EmptyResultSet`.
3. CS sends one or more `NotifyReport` (CS→CSMS) messages, each containing:
   - `requestId` — must match the original request exactly.
   - `seqNo` — starts at 0, increments by 1 per message.
   - `tbc` — "to be continued": `true` if more messages follow, `false` (or omitted, default `false`) if this is the last one.
   - `generatedAt` — timestamp of report generation.
   - `reportData` — array of Component/Variable entries with attributes.
4. CSMS responds to each `NotifyReport` with `NotifyReportResponse` (empty, no required fields).
5. Report is complete when a `NotifyReport` arrives with `tbc: false` (or `tbc` omitted).

**`ReportBaseEnumType` values:**

| Value | What it reports |
|-------|-----------------|
| `ConfigurationInventory` | Only writable (configuration) variables |
| `FullInventory` | All variables |
| `SummaryInventory` | Summary of all variables (less detail) |

### 4.2 Same Pagination Pattern in Other Messages

The `requestId` + `seqNo` + `tbc` pattern is reused across the protocol:

| Request (CSMS→CS) | Paginated Response (CS→CSMS) | Schema file |
|---------|---------------------|-------------|
| `GetBaseReport` | `NotifyReport` | [Provisioning](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) |
| `GetReport` | `NotifyReport` | [Provisioning](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) |
| `GetChargingProfiles` | `ReportChargingProfiles` | [Smart Charging](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) |
| `GetMonitoringReport` | `NotifyMonitoringReport` | [Diagnostics](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md) |
| `GetDisplayMessages` | `NotifyDisplayMessages` | [Display](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Display.md) |
| `CustomerInformation` | `NotifyCustomerInformation` | [Diagnostics](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md) |

When implementing any of these, the same CSMS-side logic applies: correlate by `requestId`, order by `seqNo`, collect until `tbc: false`.

---

## 5. Diagnostics and Logging

### 5.1 Log Upload Flow

1. CSMS sends `GetLog` (CSMS→CS) with `logType` (`DiagnosticsLog` or `SecurityLog`), `requestId`, and `log` object (containing `remoteLocation` URL, optional timestamp filters).
2. CS responds `Accepted`, `Rejected`, `AcceptedCanceled`.
3. CS sends `LogStatusNotification` (CS→CSMS) with `status: Uploading` and `requestId`.
4. CS uploads log file to `log.remoteLocation` (typically HTTP PUT or FTP).
5. CS sends `LogStatusNotification` with `status: Uploaded` (or `UploadFailure`).

**LogStatusNotification states:** `BadMessage`, `Idle`, `NotSupportedOperation`, `PermissionDenied`, `Uploaded`, `UploadFailure`, `Uploading`, `AcceptedCanceled`.

For field schemas: [GetLog](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md#getlog).

---

## Related Documents

| Document | What it contains |
|----------|-----------------|
| [Core Flows](./OCPP-2.0.1-Sequences.md) | Boot, authorization, transaction lifecycle |
| [Reservation Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md) | ReserveNow, CancelReservation, ReservationStatusUpdate — field-level details |
| [Firmware Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md) | UpdateFirmware, FirmwareStatusNotification — field-level details |
| [Provisioning Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) | GetBaseReport, NotifyReport — field-level details |
| [Diagnostics Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md) | GetLog, LogStatusNotification, monitoring — field-level details |
| [Data Types Reference](../OCPP-2.0.1-DataTypes.md) | IdTokenType, IdTokenInfoType, EVSEType |
| [Smart Charging Deep-Dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) | Charging profiles and composite schedules |
| [Main OCPP Reference](../OCPP-2.0.1.md) | Protocol overview, all messages, config variables |
