# OCPP 1.6J — Core Message Flows

> **Purpose:** Step-by-step message sequences for boot, authorization, transaction lifecycle, status reporting, and offline behavior in OCPP 1.6J. Optimized for AI agent consumption and developer troubleshooting.

> **Last updated:** 2026-02-11

---

## How This Document Was Produced

This document covers core OCPP 1.6J message flows. Its dominant confidence tier is **spec-knowledge** — behavioral sequences from the OCPP 1.6 specification (edition 2, 2017-09-28), known via AI training data and cross-referenced against the spec PDF. Field names, enum values, and configuration key names are **schema-derived**. The errata note about StatusNotification during Pending state is sourced from published OCA errata.

This document contains **3 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

---

## 1. Boot Sequence

When a Charge Point (CP) powers on or reboots, it must register with the Central System (CS) before normal operation.

### 1.1 Boot Flow Steps

1. CP opens a WebSocket connection to `ws(s)://central-system.example.com/ocpp/{chargePointId}` (sub-protocol `ocpp1.6`).
2. CP sends `BootNotification.req` with `chargePointModel`, `chargePointVendor`, and optional fields (`chargePointSerialNumber`, `firmwareVersion`, `iccid`, `imsi`, `meterSerialNumber`, `meterType`).
3. CS responds with `BootNotification.conf` containing `status`, `interval`, and `currentTime`.
4. CP behavior depends on `status`:

**If `Accepted`:**
- CP syncs its internal clock to `currentTime`.
- CP adjusts its heartbeat interval to `interval` seconds.
- CP sends `StatusNotification.req` for **every connector** (connectorId 1..N), reporting current status.
- CP begins sending `Heartbeat.req` every `interval` seconds. CS responds with `currentTime` for ongoing clock sync.
- CP is now fully operational.

**If `Pending`:**
- CP waits `interval` seconds, then re-sends `BootNotification.req`. Loop until `Accepted`.
- **CRITICAL RULE:** CP **must not** send any request messages to the CS, except `BootNotification.req`. However, CS MAY send requests to CP (e.g., `GetConfiguration`, `ChangeConfiguration`) and CP SHOULD respond.
- Per errata: CP SHOULD send `StatusNotification.req` for its connectors even while Pending, so the CS knows connector state during provisioning.
- `RemoteStartTransaction.req` and `RemoteStopTransaction.req` are explicitly forbidden while Pending.
- If `interval` is 0, CP chooses its own retry interval to avoid flooding.

**If `Rejected`:**
- CP waits `interval` seconds, then re-sends `BootNotification.req`.
- CP **must not** send any OCPP messages until the retry interval expires.
- CP MAY close its communication channel or shut down communication hardware during the wait.
- CS SHOULD NOT initiate any messages while the CP is Rejected.

### 1.2 Boot Sequence Diagram

```
CP→CS: [WebSocket connect to wss://central-system/ocpp/{chargePointId}, sub-protocol ocpp1.6]
CP→CS: BootNotification.req(chargePointModel, chargePointVendor)
CS→CP: BootNotification.conf(status=Accepted, interval=300, currentTime)
CP→CS: StatusNotification.req(connectorId=0, status=Available, errorCode=NoError)
CS→CP: StatusNotification.conf()
CP→CS: StatusNotification.req(connectorId=1, status=Available, errorCode=NoError)
CS→CP: StatusNotification.conf()
CP→CS: StatusNotification.req(connectorId=2, status=Available, errorCode=NoError)
CS→CP: StatusNotification.conf()
[loop every 300s]
  CP→CS: Heartbeat.req()
  CS→CP: Heartbeat.conf(currentTime)
```

### 1.3 Pending Boot Sequence Diagram

```
CP→CS: BootNotification.req(chargePointModel, chargePointVendor)
CS→CP: BootNotification.conf(status=Pending, interval=30)
[CS may query/configure CP while Pending]
  CS→CP: GetConfiguration.req(key=["SupportedFeatureProfiles"])
  CP→CS: GetConfiguration.conf(configurationKey=[...])
[wait 30 seconds]
CP→CS: BootNotification.req(chargePointModel, chargePointVendor)
CS→CP: BootNotification.conf(status=Accepted, interval=300, currentTime)
CP→CS: StatusNotification.req(connectorId=N, ...) [for each connector]
CS→CP: StatusNotification.conf()
```

### 1.4 Boot-Related Configuration Keys

| Key | Type | Purpose |
|-----|------|---------|
| `HeartbeatInterval` | int (seconds) | Heartbeat interval; overridden by `interval` from `BootNotification.conf` when Accepted |
| `WebSocketPingInterval` | int (seconds) | WebSocket ping interval to detect broken connections (0 = disabled) |

---

## 2. Authorization Flow

Authorization determines whether an idTag (typically an RFID card UID) is allowed to start or stop a transaction.

### 2.1 Online Authorization

1. User presents token at CP.
2. CP sends `Authorize.req(idTag)` to CS.
3. CS responds with `Authorize.conf(idTagInfo)`.
4. `idTagInfo.status` determines the result:
   - `Accepted` — token is valid, transaction may proceed.
   - `Blocked` — token is blocked (e.g., reported lost).
   - `Expired` — token authorization has expired.
   - `Invalid` — token is unknown or blacklisted.
   - `ConcurrentTx` — token is valid but already in use in another transaction (within the same group).
5. If `idTagInfo.expiryDate` is present, CP uses it to determine cache entry validity.
6. If `idTagInfo.parentIdTag` is present, CP records the group membership.

### 2.2 Parent idTag (Group Authorization)

`parentIdTag` in `idTagInfo` links multiple physical tokens to the same account.

**Rules:**
- If CARD-A and CARD-B both have `parentIdTag: "GROUP-01"`, they share an account.
- A user can stop a transaction started by CARD-A by presenting CARD-B (same group).
- `ConcurrentTx` status means the token is valid but another token in the same group already has an active transaction.
- `parentIdTag` also appears in `SendLocalList.req` entries (`AuthorizationData`) to pre-populate group memberships for offline use.
- The `parentIdTag` value MAY not be a real token UID — it can be an account number. CP SHOULD NOT use it for comparison against presented tokens.

### 2.3 Authorization Decision Logic

When a token is presented, the CP follows this logic:

**Online (WebSocket connected):**

If `LocalPreAuthorize` = true:
1. Check local authorization list and/or authorization cache first.
2. If found and `Accepted`: immediately allow user to proceed (reduces perceived latency).
3. Simultaneously send `Authorize.req` to CS.
4. If CS responds with anything other than `Accepted`: revoke the pre-authorization.

If `LocalPreAuthorize` = false (default):
1. Send `Authorize.req` to CS, wait for response.
2. Act on `idTagInfo.status`.

**Offline (WebSocket disconnected):**

```
if LocalAuthorizeOffline AND token in local authorization list:
    -> use local list status
elif AuthorizationCacheEnabled AND token in cache AND not expired:
    -> use cached status
elif AllowOfflineTxForUnknownId:
    -> accept (allow unknown tokens offline)
else:
    -> reject
```

> **ESCALATE: POLICY-DEPENDENT** — Accepting unknown tokens when offline (`AllowOfflineTxForUnknownId=true`) has security and revenue implications.
> An AI agent MUST NOT enable this without asking the developer:
> 1. Reject unknown tokens offline (secure, but may strand drivers)
> 2. Accept unknown tokens offline with energy cap via `MaxEnergyOnInvalidId` (balanced)
> 3. Accept unknown tokens with no limit (highest risk)

### 2.4 Local Authorization List Management

The CS pushes the list to the CP via `SendLocalList.req`:
- `updateType: Full` — replaces the entire list.
- `updateType: Differential` — adds, updates, or removes individual entries.
- Each entry (`AuthorizationData`) contains `idTag` and optionally `idTagInfo` (with status and parentIdTag).
- CS can query the current list version via `GetLocalListVersion.req`.
- Response statuses: `Accepted`, `Failed`, `VersionMismatch`.
- The CP MUST NOT modify the list by any means other than receiving a `SendLocalList.req`.
- Local list entries have priority over authorization cache entries for the same idTag.

### 2.5 Authorization Cache

Separate from the local list — automatically populated from responses:
- Updated from `idTagInfo` in `Authorize.conf`, `StartTransaction.conf`, and `StopTransaction.conf`.
- Cache contains both valid and invalid entries (the latest received status).
- When an entry expires, it is changed to `Expired` in the cache.
- When the cache is full and a new entry arrives: remove invalid entries first, then oldest valid entries.
- Cache SHOULD persist across reboots (non-volatile storage).
- CS can clear the entire cache via `ClearCache.req`.
- Controlled by `AuthorizationCacheEnabled` configuration key.

### 2.6 Authorization Configuration Keys

| Key | Type | Purpose |
|-----|------|---------|
| `LocalAuthorizeOffline` | boolean | Use local list / cache when offline |
| `LocalPreAuthorize` | boolean | Check local list / cache before CS (reduces latency) |
| `AuthorizationCacheEnabled` | boolean | Whether the authorization cache is active |
| `AllowOfflineTxForUnknownId` | boolean | Allow offline transactions for unknown tokens |
| `AuthorizeRemoteTxRequests` | boolean | Whether remote start requires authorization flow |
| `LocalAuthListEnabled` | boolean | Whether the local authorization list is active |
| `LocalAuthListMaxLength` | int | Maximum entries in the local authorization list |
| `MaxEnergyOnInvalidId` | int (Wh) | Max energy delivered when idTag becomes invalid mid-transaction |

---

## 3. Transaction Lifecycle

OCPP 1.6 uses separate messages for each phase: `StartTransaction.req`, `MeterValues.req`, and `StopTransaction.req`.

### 3.1 Normal Transaction Flow (Auth-First)

1. User presents idTag at CP.
2. CP authorizes (locally or via `Authorize.req` to CS).
3. User plugs in cable, EV connects.
4. CP sends `StartTransaction.req(connectorId, idTag, meterStart, timestamp)` to CS.
5. CS responds with `StartTransaction.conf(transactionId, idTagInfo)`.
6. CP uses the returned `transactionId` for all subsequent messages in this transaction.
7. If `idTagInfo.status` is not `Accepted`, CP should handle per `StopTransactionOnInvalidId` config.
8. During charging: CP sends `MeterValues.req(connectorId, meterValue, transactionId)` at `MeterValueSampleInterval` and/or `ClockAlignedDataInterval`.
9. User stops (presents idTag / presses button / unplugs).
10. CP sends `StopTransaction.req(transactionId, meterStop, timestamp, reason, [idTag], [transactionData])`.
11. CS responds with `StopTransaction.conf([idTagInfo])`.

### 3.2 Normal Transaction Sequence Diagram

```
[User presents idTag]
CP→CS: Authorize.req(idTag)
CS→CP: Authorize.conf(idTagInfo: status=Accepted)
[User plugs in, EV connects]
CP→CS: StatusNotification.req(connectorId=1, status=Preparing)
CS→CP: StatusNotification.conf()
CP→CS: StartTransaction.req(connectorId=1, idTag, meterStart=0, timestamp)
CS→CP: StartTransaction.conf(transactionId=12345, idTagInfo.status=Accepted)
CP→CS: StatusNotification.req(connectorId=1, status=Charging)
CS→CP: StatusNotification.conf()
[loop every MeterValueSampleInterval seconds]
  CP→CS: MeterValues.req(connectorId=1, transactionId=12345, meterValue=[...])
  CS→CP: MeterValues.conf()
[User presents idTag to stop]
CP→CS: StopTransaction.req(transactionId=12345, meterStop=15000, reason=Local)
CS→CP: StopTransaction.conf(idTagInfo)
CP→CS: StatusNotification.req(connectorId=1, status=Finishing)
CS→CP: StatusNotification.conf()
[User unplugs cable]
CP→CS: StatusNotification.req(connectorId=1, status=Available)
CS→CP: StatusNotification.conf()
```

### 3.3 Remote Start Transaction

1. CS sends `RemoteStartTransaction.req(idTag, [connectorId], [chargingProfile])` to CP.
2. CP responds with `RemoteStartTransaction.conf(status)` — `Accepted` or `Rejected`.
3. If `AuthorizeRemoteTxRequests` is true: CP authorizes the idTag first (local list, cache, or `Authorize.req`).
4. If `AuthorizeRemoteTxRequests` is false: CP starts the transaction immediately.
5. If `connectorId` is omitted, CP selects a connector. CP MAY reject requests without a connectorId.
6. CP proceeds with normal `StartTransaction.req` flow.
7. Optional `chargingProfile` (purpose must be `TxProfile`) is applied to this transaction.

```
CS→CP: RemoteStartTransaction.req(idTag, connectorId=1)
CP→CS: RemoteStartTransaction.conf(status=Accepted)
CP→CS: StartTransaction.req(connectorId=1, idTag, meterStart=0, timestamp)
CS→CP: StartTransaction.conf(transactionId=12346, idTagInfo.status=Accepted)
CP→CS: StatusNotification.req(connectorId=1, status=Charging)
CS→CP: StatusNotification.conf()
[charging continues...]
```

### 3.4 Remote Stop Transaction

1. CS sends `RemoteStopTransaction.req(transactionId)` to CP.
2. CP responds with `RemoteStopTransaction.conf(status)` — `Accepted` if the transaction is ongoing, `Rejected` otherwise.
3. CP stops energy delivery and unlocks the connector (if applicable).
4. CP sends `StopTransaction.req` with `reason=Remote`.

```
CS→CP: RemoteStopTransaction.req(transactionId=12345)
CP→CS: RemoteStopTransaction.conf(status=Accepted)
CP→CS: StopTransaction.req(transactionId=12345, meterStop=15000, reason=Remote)
CS→CP: StopTransaction.conf()
CP→CS: StatusNotification.req(connectorId=1, status=Finishing)
CS→CP: StatusNotification.conf()
```

### 3.5 StopTransaction Reasons

`Reason` values for `StopTransaction.req`:

| Reason | Meaning |
|--------|---------|
| `Local` | User stopped at CP (RFID, button). Default if omitted. |
| `Remote` | CS sent `RemoteStopTransaction.req` |
| `DeAuthorized` | Token became invalid during transaction (e.g., rejected by `StartTransaction.conf` after offline start) |
| `EmergencyStop` | Emergency stop button pressed |
| `EVDisconnected` | EV unplugged (when `StopTransactionOnEVSideDisconnect=true`) |
| `HardReset` | CS sent `Reset.req` with type `Hard` |
| `SoftReset` | CS sent `Reset.req` with type `Soft` |
| `Reboot` | CP is rebooting |
| `PowerLoss` | CP lost power |
| `UnlockCommand` | CS sent `UnlockConnector.req` |
| `Other` | None of the above |

### 3.6 Meter Values During Transactions

Meter values are sent as separate `MeterValues.req` messages during a transaction.

**Sampled (periodic) meter values:**
- Sent every `MeterValueSampleInterval` seconds (0 = disabled).
- Measurands configured via `MeterValuesSampledData` (comma-separated list, e.g., `Energy.Active.Import.Register,Power.Active.Import`).

**Clock-aligned meter values:**
- Sent at intervals aligned to midnight, every `ClockAlignedDataInterval` seconds (e.g., 900 = every 15 min).
- Measurands configured via `MeterValuesAlignedData`.

**Transaction data in StopTransaction:**
- `transactionData` field in `StopTransaction.req` can include additional meter values.
- Sampled measurands for stop: `StopTxnSampledData`.
- Clock-aligned measurands for stop: `StopTxnAlignedData`.
- When both `StopTxnAlignedData` and `StopTxnSampledData` are empty strings, CP sends no meter values in `StopTransaction.req`.

> **ESCALATE: SPEC-SILENT** — The spec does not define whether `MeterValues.req` messages sent during a transaction should include the opening meter reading (context `Transaction.Begin`) or only periodic/clock-aligned samples.
> An AI agent MUST NOT assume meter value context without asking the developer:
> 1. Only send periodic/clock-aligned samples in `MeterValues.req` (most common interpretation)
> 2. Also include a `Transaction.Begin` reading in the first `MeterValues.req`
> 3. Rely solely on `meterStart` in `StartTransaction.req` for the opening reading

### 3.7 Transaction Configuration Keys

| Key | Type | Purpose |
|-----|------|---------|
| `MeterValueSampleInterval` | int (seconds) | Interval for sampled meter values (0 = disabled) |
| `ClockAlignedDataInterval` | int (seconds) | Interval for clock-aligned meter values (0 = disabled) |
| `MeterValuesSampledData` | CSL | Measurands for periodic samples |
| `MeterValuesAlignedData` | CSL | Measurands for clock-aligned samples |
| `StopTxnSampledData` | CSL | Sampled measurands included in `StopTransaction.req` |
| `StopTxnAlignedData` | CSL | Clock-aligned measurands included in `StopTransaction.req` |
| `StopTransactionOnEVSideDisconnect` | boolean | Stop transaction when cable disconnected at EV side |
| `StopTransactionOnInvalidId` | boolean | Stop transaction if idTag becomes invalid |
| `UnlockConnectorOnEVSideDisconnect` | boolean | Unlock connector when cable disconnected at EV side |
| `ConnectionTimeOut` | int (seconds) | Timeout for user to present idTag after plugging in (Preparing state) |
| `AuthorizeRemoteTxRequests` | boolean | Whether remote start requires authorization |

---

## 4. Status Notification

`StatusNotification.req` reports connector status changes and error conditions to the CS.

### 4.1 Message Fields

`StatusNotification.req(connectorId, errorCode, status, [timestamp], [info], [vendorId], [vendorErrorCode])`

- `connectorId=0` refers to the Charge Point main controller itself. Only `Available`, `Unavailable`, and `Faulted` are valid for connectorId 0.
- `connectorId > 0` refers to individual connectors.

### 4.2 Connector Statuses (ChargePointStatus)

| Status | Meaning |
|--------|---------|
| `Available` | Connector is ready for a new user |
| `Preparing` | Cable plugged in or idTag presented, waiting for remaining preconditions |
| `Charging` | Energy is being transferred to the EV |
| `SuspendedEV` | EV has paused charging (e.g., battery management, target SoC reached) |
| `SuspendedEVSE` | EVSE has paused charging (e.g., smart charging limit = 0) |
| `Finishing` | Transaction stopped, waiting for user action (e.g., unplug cable) |
| `Reserved` | Connector is reserved for a specific idTag |
| `Unavailable` | Connector is not available for charging (e.g., maintenance, firmware update) |
| `Faulted` | Connector has a fault preventing charging |

**Precedence rule:** If charging is suspended by both EV and EVSE simultaneously, `SuspendedEVSE` takes precedence.

### 4.3 Typical Charging Session Status Flow

```
Normal flow: Available → Preparing → Charging → Finishing → Available
Suspend variations: Charging ↔ SuspendedEV, Charging ↔ SuspendedEVSE
Reservation: Available → Reserved → Preparing → ...
Faulted: any state → Faulted (on error), Faulted → previous state (on recovery)
```

Full status transition for a normal session:
1. `Available` — connector idle, ready for use.
2. `Preparing` — user plugs in cable or presents idTag. Timeout controlled by `ConnectionTimeOut`.
3. `Charging` — all preconditions met, energy flowing.
4. `SuspendedEV` / `SuspendedEVSE` — charging paused (may alternate).
5. `Finishing` — transaction ended, user needs to unplug.
6. `Available` — user unplugs, connector ready again.

### 4.4 Error Codes (ChargePointErrorCode)

| ErrorCode | Meaning |
|-----------|---------|
| `NoError` | No error (normal status change report) |
| `ConnectorLockFailure` | Failure to lock or unlock connector |
| `EVCommunicationError` | Communication failure with EV (warning only; use with Preparing, SuspendedEV, SuspendedEVSE, Finishing) |
| `GroundFailure` | Ground fault detected |
| `HighTemperature` | Temperature too high |
| `InternalError` | Internal error in the Charge Point |
| `LocalListConflict` | Conflict between local authorization list and CS authorization response |
| `OtherError` | Other error not covered above |
| `OverCurrentFailure` | Over-current detected |
| `OverVoltage` | Over-voltage detected |
| `PowerMeterFailure` | Power meter failure |
| `PowerSwitchFailure` | Power switch failure |
| `ReaderFailure` | RFID reader failure |
| `ResetFailure` | Unable to perform reset |
| `UnderVoltage` | Under-voltage detected |
| `WeakSignal` | Weak cellular/network signal |

### 4.5 MinimumStatusDuration

The optional `MinimumStatusDuration` configuration key (int, seconds) sets the minimum time a status must remain active before the CP sends a `StatusNotification.req`. This prevents flooding the CS with rapid transitions (e.g., Preparing -> Charging within 2 seconds).

- Setting it to 0 does NOT override any manufacturer-built-in minimum delay.
- Setting it too high will delay ALL status notifications, not just rapid transitions.

> **ESCALATE: SPEC-SILENT** — The spec does not define whether `MinimumStatusDuration` should suppress intermediate statuses entirely or merely delay their sending.
> An AI agent MUST NOT assume suppression behavior without asking the developer:
> 1. Suppress intermediate statuses (only send the final stable status after the duration elapses)
> 2. Delay all status notifications by the configured duration (queue and send them all, but later)
> 3. Only apply the minimum duration to specific transitions (e.g., Preparing->Charging)

---

## 5. Offline Behavior

When the WebSocket connection to the CS is lost, the CP operates autonomously.

### 5.1 Transaction Message Queuing

CP queues transaction-related messages when offline. Transaction-related messages are:
- `StartTransaction.req`
- `StopTransaction.req`
- `MeterValues.req` (periodic and clock-aligned, during a transaction)

**Queuing rules:**
- Transaction-related messages MUST be delivered in chronological order (FIFO).
- Non-transaction messages (e.g., `Authorize.req`, `StatusNotification.req`) MAY be sent immediately, bypassing the queue.
- New transaction-related messages wait until the queue is fully drained before being sent.
- CP SHOULD store queued messages in non-volatile memory to survive reboots.

### 5.2 Retry Configuration

| Key | Type | Purpose |
|-----|------|---------|
| `TransactionMessageAttempts` | int | Number of times to retry a failed transaction-related message |
| `TransactionMessageRetryInterval` | int (seconds) | Base wait between retries (multiplied by attempt number) |

**Retry backoff example** (attempts=3, interval=60):
1. First failure: wait 60 seconds, retry.
2. Second failure: wait 120 seconds, retry.
3. Third failure: discard the message, move to the next queued message.

### 5.3 Offline Authorization

When offline, CP uses local authorization if configured:

1. If `LocalAuthorizeOffline=true`: check local authorization list and authorization cache.
2. If the idTag is not found locally and `AllowOfflineTxForUnknownId=true`: accept the token.
3. Identifiers present in the local list with a status other than `Accepted` MUST be rejected, even offline.
4. Expired identifiers (per `expiryDate`) MUST also be rejected.

### 5.4 Reconnection Behavior

When the CP reconnects to the CS:

1. CP sends `BootNotification.req` (if the connection was fully lost and re-established).
2. CP drains its transaction-related message queue in chronological order.
3. CP sends `StatusNotification.req` with current connector statuses if they changed while offline.
4. CP SHOULD NOT send historical `StatusNotification.req` messages for intermediate states that occurred while offline — only current status and any error conditions.
5. If a transaction was started offline with an unknown idTag, the CS may reject the idTag in `StartTransaction.conf`. The CP then handles per `StopTransactionOnInvalidId`:
   - If `true`: stop the transaction, set `reason=DeAuthorized`, keep cable locked until owner presents their idTag.
   - If `false`: stop energy delivery but do not end the transaction.

### 5.5 Offline Reconnection Sequence Diagram

```
[connection lost]
[User starts transaction offline, authorized via local list]
[User stops transaction offline]
[connection restored]
CP→CS: [WebSocket reconnect]
CP→CS: BootNotification.req(chargePointModel, chargePointVendor)
CS→CP: BootNotification.conf(status=Accepted)
CP→CS: StatusNotification.req(connectorId=1, status=Available) [current status only]
CS→CP: StatusNotification.conf()
[drain transaction queue — FIFO, chronological order]
  CP→CS: StartTransaction.req(connectorId=1, idTag, meterStart, timestamp=<past>)
  CS→CP: StartTransaction.conf(transactionId=12347)
  CP→CS: MeterValues.req(transactionId=12347, meterValue=[...]) [queued values]
  CS→CP: MeterValues.conf()
  CP→CS: StopTransaction.req(transactionId=12347, meterStop, timestamp=<past>)
  CS→CP: StopTransaction.conf()
[queue drained, normal operations resume]
```

---

## Related Documents

| Document | What it contains |
|----------|-----------------|
| [OCPP 2.0.1 Sequences](../OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences.md) | Equivalent flows for OCPP 2.0.1 (TransactionEvent-based) |
| [METHODOLOGY.md](../METHODOLOGY.md) | Confidence tiers and escalation model |
