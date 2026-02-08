# OCPP 2.0.1 — Core Message Flows

> **Purpose:** Precise step-by-step message flows for boot, authorization, and transaction lifecycles. Optimized for AI agent consumption — uses structured sequences and explicit rules rather than visual diagrams.

> **Last updated:** 2026-02-07

---

## How This Document Was Produced

This document covers core OCPP 2.0.1 message flows: boot sequence, authorization (including local lists, caching, and offline decisions), and transaction lifecycle. Its dominant confidence tier is **spec-knowledge** — behavioral sequences from the OCPP 2.0.1 specification Part 2, known via AI training data. Field names, enum values, and type references are **schema-derived** (cross-referenced against the [schema documentation](../OCPP-2.0.1-Schemas/) and [data types reference](../OCPP-2.0.1-DataTypes.md), mechanically extracted from the official OCA JSON schemas). The pseudocode authorization decision logic in §2.3 is **interpretation** — synthesis of spec rules into executable logic.

This document contains **3 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [Operational Flows](./OCPP-2.0.1-Sequences-Operational.md) — reservations, offline queueing, firmware updates, report pagination
- [Provisioning Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) — BootNotification, Heartbeat, StatusNotification field-level details
- [Authorization Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md) — Authorize, SendLocalList, GetLocalListVersion field-level details
- [Transaction Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md) — TransactionEvent, RequestStartTransaction, RequestStopTransaction field-level details
- [Data Types Reference](../OCPP-2.0.1-DataTypes.md) — IdTokenType, IdTokenInfoType, MeterValueType, EVSEType

---

## 1. Boot Sequence

When a Charging Station powers on or resets, it must register with the CSMS before doing anything else.

For field schemas: [BootNotification](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md#bootnotification), [StatusNotification](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md#statusnotification), [Heartbeat](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md#heartbeat).

### 1.1 Boot Flow Steps

1. CS opens WebSocket to `wss://csms.example.com/ocpp/{cs_id}` (sub-protocol `ocpp2.0.1`).
2. CS sends `BootNotification` (CS→CSMS) with `reason` and `chargingStation` (model, vendorName).
3. CSMS responds with `BootNotificationResponse` containing `status`, `interval`, and `currentTime`.
4. CS behavior depends on `status`:

**If `Accepted`:**
- CS syncs clock to `currentTime`.
- CS sends `StatusNotification` (CS→CSMS) for **every connector** — reporting `connectorStatus` (`Available`, `Occupied`, `Faulted`, etc.).
- CS starts sending `Heartbeat` (CS→CSMS) every `interval` seconds. CSMS responds with `currentTime` for ongoing clock sync.
- CS is now fully operational and can send/receive all message types.

**If `Pending`:**
- CS waits `interval` seconds, then sends `BootNotification` again. Loop until `Accepted`.
- **CRITICAL RULE:** CS **must not** send any message other than `BootNotification` while in Pending state. No StatusNotification, no Heartbeat, no TransactionEvent — nothing.
- CSMS may change `interval` between retries.
- Typical reason: CSMS is provisioning the CS or awaiting operator approval.

**If `Rejected`:**
- Same behavior as Pending — wait `interval`, retry `BootNotification`, must not send other messages.
- Typically requires operator action (registering the CS in the CSMS) before it will be accepted.
- CS retries indefinitely at the given interval.

### 1.2 Boot Reason Values

`BootReasonEnumType`: `PowerUp`, `ApplicationReset`, `FirmwareUpdate`, `LocalReset`, `RemoteReset`, `ScheduledReset`, `Triggered`, `Unknown`, `Watchdog`.

### 1.3 Connector Status Values

`ConnectorStatusEnumType`: `Available`, `Occupied`, `Reserved`, `Unavailable`, `Faulted`.

### 1.4 Boot-Related Configuration Variables

| Component | Variable | Relevance |
|-----------|----------|-----------|
| `HeartbeatCtrlr` | `Interval` | Overridden by `interval` from `BootNotificationResponse` when Accepted |
| `OCPPCommCtrlr` | `RetryBackOffWaitMinimum` | Minimum wait before WebSocket reconnect after disconnect |
| `OCPPCommCtrlr` | `RetryBackOffRandomRange` | Random range added to reconnect wait (prevents thundering herd) |
| `OCPPCommCtrlr` | `RetryBackOffRepeatTimes` | Number of reconnect retries |
| `OCPPCommCtrlr` | `WebSocketPingInterval` | WebSocket ping interval to detect broken connections |

---

## 2. Authorization

Authorization determines whether an idToken (RFID, app, eMAID, etc.) is allowed to start a transaction. Three mechanisms exist: online CSMS authorization, local authorization list, and authorization cache.

For field schemas: [Authorize](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md#authorize), [IdTokenInfoType](../OCPP-2.0.1-DataTypes.md#idtokeninfotype).

### 2.1 Online Authorization

1. User presents token at CS.
2. CS sends `Authorize` (CS→CSMS) with `idToken` ({idToken: string, type: IdTokenEnumType}).
3. CSMS responds with `AuthorizeResponse` containing `idTokenInfo`.
4. `idTokenInfo.status` determines result:
   - `Accepted` — token is valid, transaction can proceed.
   - `Blocked`, `Invalid`, `Expired`, `NoCredit`, etc. — reject.
   - `ConcurrentTx` — token is valid but already in use in another transaction within the same group.
5. If `cacheExpiryDateTime` is present, CS caches the result for future offline/pre-auth use.
6. If `groupIdToken` is present, CS records the token's group membership.

**`AuthorizationStatusEnumType` values:** `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`.

### 2.2 GroupId (Parent Token)

`groupIdToken` in `AuthorizeResponse` links multiple physical tokens to the same account.

**Rules:**
- If CARD-A and CARD-B both have `groupIdToken: "GRP-01"`, they share an account.
- A user can stop a transaction started by CARD-A by presenting CARD-B (same group).
- `ConcurrentTx` status means the token is valid but another token in the same group already has an active transaction (and the system doesn't allow concurrent charging).
- `groupIdToken` also appears in `SendLocalList` entries to pre-populate group memberships for offline use.

### 2.3 Authorization Decision Logic

When a token is presented, the CS follows this logic (order depends on configuration):

**Online (WebSocket connected):**

If `AuthCtrlr.LocalPreAuthorize` = true:
1. Check local list and/or cache first.
2. If found and `Accepted`: immediately allow user to proceed (show accept, allow plug-in).
3. Simultaneously send `Authorize` to CSMS.
4. If CSMS responds with anything other than `Accepted`: **stop the transaction** that may have started during pre-auth.

If `AuthCtrlr.LocalPreAuthorize` = false (default):
1. Send `Authorize` to CSMS, wait for response.
2. Act on `idTokenInfo.status`.

**Offline (WebSocket disconnected):**

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

> **ESCALATE: POLICY-DEPENDENT** — Accepting unknown tokens when offline (`OfflineTxForUnknownIdEnabled=true`) has security and revenue implications.
> An AI agent MUST NOT enable this offline authorization path without asking the developer:
> 1. Reject unknown tokens offline (secure, but may strand drivers whose tokens haven't been cached)
> 2. Accept unknown tokens offline with a configurable energy/time cap (balanced approach)
> 3. Accept unknown tokens with no limit (trusts all tokens when offline — highest risk, highest convenience)

### 2.4 Local Authorization List Management

The CSMS pushes the list to the CS via `SendLocalList` (CSMS→CS):
- `updateType: Full` — replaces the entire list.
- `updateType: Differential` — adds, updates, or removes individual entries.
- Each entry contains `idToken` and optionally `idTokenInfo` (with status and groupIdToken).
- CSMS can query the current list version via `GetLocalListVersion` (CSMS→CS).
- `SendLocalListStatusEnumType` response values: `Accepted`, `Failed`, `VersionMismatch`.

### 2.5 Authorization Cache

Separate from the local list — automatically populated from responses:
- Populated from `AuthorizeResponse.idTokenInfo` and `TransactionEventResponse.idTokenInfo`.
- Entries expire at `cacheExpiryDateTime`.
- CSMS can clear the entire cache via `ClearCache` (CSMS→CS).
- Controlled by `AuthCacheCtrlr.Enabled`.

### 2.6 Authorization Configuration Variables

| Component | Variable | Purpose |
|-----------|----------|---------|
| `AuthCtrlr` | `Enabled` | Whether authorization is required at all |
| `AuthCtrlr` | `LocalAuthorizeOffline` | Use local list when offline |
| `AuthCtrlr` | `LocalPreAuthorize` | Check local list/cache before CSMS (reduces latency) |
| `AuthCtrlr` | `OfflineTxForUnknownIdEnabled` | Allow offline transactions for tokens not in list or cache |
| `AuthCacheCtrlr` | `Enabled` | Whether auth cache is active |
| `AuthCacheCtrlr` | `LifeTime` | Default cache entry lifetime if `cacheExpiryDateTime` not provided |

---

## 3. Transaction Lifecycle

OCPP 2.0.1 uses `TransactionEvent` (CS→CSMS) as the single message for the entire transaction lifecycle — replacing `StartTransaction`, `StopTransaction`, and `MeterValues` from OCPP 1.6.

For field schemas: [TransactionEvent](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md#transactionevent), [RequestStartTransaction](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md#requeststarttransaction), [RequestStopTransaction](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md#requeststoptransaction).

### 3.1 TransactionEvent Rules

- **First event** of a transaction: `eventType: Started` (exactly once).
- **Last event** of a transaction: `eventType: Ended` (exactly once).
- **All intermediate events**: `eventType: Updated`.
- `seqNo` starts at 0 and increments by 1 for each event in the same transaction. The CSMS uses this to detect gaps (e.g., from offline events).
- `transactionId` is assigned by the CS (string, max 36 chars) and stays the same for the entire transaction.
- `triggerReason` explains why this particular event was sent.
- `stoppedReason` is only present in the `Ended` event.
- `offline: true` flag indicates the event occurred while the CS was disconnected.

### 3.2 Auth-First Flow (Most Common)

1. User presents token → CS sends `Authorize` → CSMS responds `Accepted`.
2. User plugs in cable → EV detected on EVSE.
3. CS sends `TransactionEvent(Started, triggerReason: Authorized, seqNo: 0)` with `chargingState: Charging`, `idToken`, `evse`, and opening `meterValue` (context: `Transaction.Begin`).
4. CSMS responds with `TransactionEventResponse` (may include `idTokenInfo` to re-confirm or revoke).
5. Periodically (per `SampledDataCtrlr.TxUpdatedInterval`): CS sends `TransactionEvent(Updated, triggerReason: MeterValuePeriodic)` with meter readings.
6. User stops (presents token / presses button): CS sends `TransactionEvent(Ended, triggerReason: StopAuthorized, stoppedReason: Local)` with closing `meterValue` (context: `Transaction.End`).
7. CSMS responds with `TransactionEventResponse` (may include `totalCost`). `totalCost` is only meaningful for `Ended` events. `totalCost: 0.00` means free; omitted `totalCost` means NOT free (cost unknown or calculated later).

> **ESCALATE: SPEC-SILENT** — The semantic distinction between `totalCost: 0.00` (free) and omitted `totalCost` (cost unknown) could cause billing bugs. The spec's exact wording is ambiguous.
> An AI agent MUST NOT assume billing interpretation without asking the developer:
> 1. Follow the semantics stated here: `0.00` = free, omitted = cost unknown or calculated later
> 2. Treat omitted `totalCost` as free (some implementations do this — simpler but loses information)
> 3. Always wait for a separate billing calculation regardless of `totalCost` presence (billing system is authoritative)

### 3.3 Plug-First Flow (Cable Before Auth)

1. User plugs in cable → EV detected.
2. CS sends `TransactionEvent(Started, triggerReason: CablePluggedIn, seqNo: 0)` with `chargingState: EVConnected`, `evse`, **no** `idToken`.
3. Power is NOT flowing — `EVConnected` state means waiting for authorization.
4. User presents token → CS sends `Authorize` → CSMS responds `Accepted`.
5. CS sends `TransactionEvent(Updated, triggerReason: Authorized, seqNo: 1)` with `chargingState: Charging` and `idToken`.
6. Charging begins, continues with periodic Updated events, ends normally.

Config variable `TxCtrlr.EVConnectionTimeOut` controls how long the CS waits for authorization after cable plug-in before timing out.

> **ESCALATE: POLICY-DEPENDENT** — When `EVConnectionTimeOut` fires (user plugged in but didn't authorize), the spec says the transaction should end, but HOW it ends is a policy choice.
> An AI agent MUST NOT silently choose timeout behavior without asking the developer:
> 1. End the transaction silently (just release the connector)
> 2. End the transaction and send `TransactionEvent(Ended, triggerReason=EVConnectTimeout)` (explicit event for audit trail)
> 3. Keep waiting indefinitely (ignore the timeout)
> Additionally: should the connector be automatically unlocked to free the cable?

### 3.4 Remote Start (CSMS-Initiated)

1. CSMS sends `RequestStartTransaction` (CSMS→CS) with `idToken`, `remoteStartId`, and optionally `evseId` and `chargingProfile`.
2. CS responds `Accepted` or `Rejected` (rejected if EVSE unavailable/faulted/occupied).
3. If `evseId` omitted, CS picks an available EVSE.
4. CS prepares EVSE, waits for user to plug in cable.
5. CS sends `TransactionEvent(Started, triggerReason: RemoteStart)` with `transactionInfo.remoteStartId` matching the request — this is how the CSMS correlates the start request with the actual transaction.

### 3.5 Remote Stop (CSMS-Initiated)

1. CSMS sends `RequestStopTransaction` (CSMS→CS) with `transactionId`.
2. CS responds `Accepted` or `Rejected`.
3. CS stops energy delivery.
4. CS sends `TransactionEvent(Ended, triggerReason: RemoteStop, stoppedReason: Remote)`.

### 3.6 Charging State Transitions

`ChargingStateEnumType` tracks energy flow. Transitions trigger `TransactionEvent(Updated, triggerReason: ChargingStateChanged)`.

| State | Meaning | Transitions to |
|-------|---------|---------------|
| `Idle` | No cable / transaction ended | → `EVConnected` (cable plugged in) |
| `EVConnected` | Cable in, not charging (waiting for auth or EV not ready) | → `Charging` (authorized and EV ready) |
| `Charging` | Energy flowing EVSE→EV | → `SuspendedEV`, `SuspendedEVSE`, `Idle` (ended) |
| `SuspendedEV` | Paused by EV (e.g., battery management, target SoC reached) | → `Charging` (EV resumes), `Idle` (ended) |
| `SuspendedEVSE` | Paused by EVSE (e.g., smart charging limit = 0) | → `Charging` (limit raised), `Idle` (ended) |

### 3.7 Stopped Reasons

`ReasonEnumType` values for `transactionInfo.stoppedReason` (only in `Ended` events):

| Reason | Meaning |
|--------|---------|
| `Local` | User stopped at CS (RFID, button). May be omitted (default). |
| `Remote` | CSMS sent `RequestStopTransaction` |
| `DeAuthorized` | Token became invalid during transaction |
| `EVDisconnected` | User unplugged cable |
| `EmergencyStop` | Emergency stop pressed |
| `PowerLoss` | CS lost power |
| `Reboot` | CS rebooting |
| `EnergyLimitReached` | Charging profile energy limit hit |
| `TimeLimitReached` | Charging profile time limit hit |
| `SOCLimitReached` | EV reached target state of charge |
| `ImmediateReset` | CS received `Reset(Immediate)` |
| `Other` | None of the above |

Config variables that affect stop behavior:
- `TxCtrlr.StopTxOnEVSideDisconnect` — stop transaction when cable unplugged.
- `TxCtrlr.StopTxOnInvalidId` — stop transaction if token becomes invalid.

### 3.8 Trigger Reasons

`TriggerReasonEnumType` — why this `TransactionEvent` was sent:

| TriggerReason | When used |
|---------------|-----------|
| `Authorized` | Token was authorized (Started or Updated after auth) |
| `CablePluggedIn` | Cable plugged in (plug-first Started event) |
| `ChargingRateChanged` | Charging rate changed (from smart charging profile) |
| `ChargingStateChanged` | `chargingState` transitioned |
| `Deauthorized` | Token revoked during transaction |
| `EVCommunicationLost` | Communication with EV lost |
| `EVConnectTimeout` | EV didn't connect within `EVConnectionTimeOut` |
| `EVDeparted` | EV unplugged / departed |
| `EVDetected` | EV detected on connector |
| `MeterValueClock` | Clock-aligned meter reading |
| `MeterValuePeriodic` | Periodic meter reading |
| `RemoteStart` | Started by `RequestStartTransaction` |
| `RemoteStop` | Stopped by `RequestStopTransaction` |
| `StopAuthorized` | User authorized the stop (presented token/button) |
| `AbnormalCondition` | Fault or abnormal condition |
| `ResetCommand` | CS received `Reset` command |
| `SignedDataReceived` | Signed meter data received from EV |
| `Trigger` | Triggered by `TriggerMessage` |
| `EnergyLimitReached` | Energy limit from profile hit |
| `TimeLimitReached` | Time limit from profile hit |
| `UnlockCommand` | `UnlockConnector` command received |

### 3.9 Meter Values in Transactions

Meter values are embedded in `TransactionEvent` via the `meterValue` array (not sent as separate messages).

**Reading context** (`ReadingContextEnumType`):

| Context | When used | Typical event |
|---------|-----------|---------------|
| `Transaction.Begin` | Opening meter reading | `Started` event |
| `Sample.Periodic` | Regular interval reading | `Updated` event (per `SampledDataCtrlr.TxUpdatedInterval`) |
| `Sample.Clock` | Clock-aligned reading | `Updated` event (per `AlignedDataCtrlr.Interval`) |
| `Transaction.End` | Closing meter reading | `Ended` event |
| `Trigger` | On-demand reading | `Updated` event (from `TriggerMessage`) |

**Metering configuration:**

| Component | Variable | Purpose |
|-----------|----------|---------|
| `SampledDataCtrlr` | `TxUpdatedInterval` | Seconds between periodic meter values |
| `SampledDataCtrlr` | `TxUpdatedMeasurands` | Which measurands (e.g., `Energy.Active.Import.Register,Power.Active.Import,SoC`) |
| `AlignedDataCtrlr` | `Interval` | Seconds between clock-aligned readings |
| `AlignedDataCtrlr` | `Measurands` | Which measurands for clock-aligned readings |

---

## Related Documents

| Document | What it contains |
|----------|-----------------|
| [Operational Flows](./OCPP-2.0.1-Sequences-Operational.md) | Reservations, offline queueing, firmware updates, report pagination |
| [Provisioning Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) | BootNotification, Heartbeat, StatusNotification — field-level details |
| [Authorization Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md) | Authorize, SendLocalList, GetLocalListVersion — field-level details |
| [Transaction Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md) | TransactionEvent, RequestStartTransaction, RequestStopTransaction — field-level details |
| [Availability Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Availability.md) | StatusNotification, ChangeAvailability — field-level details |
| [Data Types Reference](../OCPP-2.0.1-DataTypes.md) | IdTokenType, IdTokenInfoType, EVSEType, MeterValueType |
| [Smart Charging Deep-Dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) | Charging profiles, composite schedules — affects transaction power limits |
| [Main OCPP Reference](../OCPP-2.0.1.md) | Protocol overview, all messages, config variables |
