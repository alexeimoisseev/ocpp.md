# OCPP 1.6J — Open Charge Point Protocol 1.6 (JSON over WebSocket)

> **Purpose:** This file provides structured context about OCPP 1.6J for AI agents working on EV charging infrastructure. It is not a replacement for the official specification but a practical reference to ground AI-assisted development, integration, and troubleshooting.

> **Last updated:** 2026-02-11
> **Spec covered:** OCPP 1.6 Edition 2 (2017-09-28), JSON over WebSocket transport
>
> Source on [Github](https://github.com/alexeimoisseev/ocpp.md).

---

## 1. What is OCPP 1.6J?

OCPP 1.6 is the most widely deployed version of the Open Charge Point Protocol. It defines communication between a **Charge Point** and a **Central System** for managing EV charging infrastructure.

The **"J" suffix** denotes the JSON-over-WebSocket transport binding (as opposed to the SOAP/HTTP binding). JSON is the dominant transport for OCPP 1.6 in practice.

**Edition 2** (published 2017-09-28) is the current revision. It clarified ambiguities from Edition 1 and is the edition referenced throughout this document.

The specification is maintained by the **Open Charge Alliance (OCA)**.

---

## 2. Architecture

### 2.1 Roles

- **Charge Point (CP):** The physical device that charges EVs. Initiates the WebSocket connection.
- **Central System (CS):** The backend server that manages Charge Points remotely.

**Important terminology note:** OCPP 1.6 uses "Charge Point" and "Central System." The terms "Charging Station" and "CSMS" are OCPP 2.0.1 terms and do not apply to 1.6.

### 2.2 Connector Model

```
Charge Point → Connector 1 (e.g., Type 2), Connector 2 (e.g., CCS), ...
```

- A Charge Point has one or more **Connectors**, each identified by a `connectorId` (1-indexed integer).
- `connectorId=0` refers to the **Charge Point as a whole** (used in messages like `ChangeAvailability`, `StatusNotification`, and `MeterValues`).
- There is **no EVSE concept** in 1.6. The EVSE abstraction layer was introduced in OCPP 2.0.1.

### 2.3 Transport

- **WebSocket** (RFC 6455), typically over TLS (`wss://`)
- Sub-protocol: `ocpp1.6`
- The Charge Point connects to the Central System at a URL like: `wss://cs.example.com/ocpp/<charge_point_id>`
- The Charge Point ID is included in the WebSocket URL path.

### 2.4 Message Frame

OCPP 1.6J uses a JSON-RPC-like message framing. There are three message types:

**CALL (Request):**
```json
[2, "<messageId>", "<action>", {<payload>}]
```

**CALLRESULT (Response):**
```json
[3, "<messageId>", {<payload>}]
```

**CALLERROR (Error Response):**
```json
[4, "<messageId>", "<errorCode>", "<errorDescription>", {<errorDetails>}]
```

- `messageId` is a unique string that correlates a CALL with its CALLRESULT or CALLERROR.
- Only **one CALL can be outstanding** at a time per direction (CP->CS or CS->CP).
- Both sides can initiate CALLs independently since the connection is bidirectional.
- Standard error codes: `NotImplemented`, `NotSupported`, `InternalError`, `ProtocolError`, `SecurityError`, `FormationViolation`, `PropertyConstraintViolation`, `OccurenceConstraintViolation`, `TypeConstraintViolation`, `GenericError`.

---

## 3. Feature Profiles

OCPP 1.6 organizes its 28 messages into **6 Feature Profiles**. The Core profile is required; all others are optional. A Charge Point advertises its supported profiles via the `SupportedFeatureProfiles` configuration key.

| Profile | Required | Messages |
|---------|----------|----------|
| **Core** | Yes | Authorize, BootNotification, ChangeAvailability, ChangeConfiguration, ClearCache, DataTransfer, GetConfiguration, Heartbeat, MeterValues, RemoteStartTransaction, RemoteStopTransaction, Reset, StartTransaction, StatusNotification, StopTransaction, UnlockConnector |
| **Firmware Management** | No | GetDiagnostics, DiagnosticsStatusNotification, UpdateFirmware, FirmwareStatusNotification |
| **Local Auth List Management** | No | SendLocalList, GetLocalListVersion |
| **Reservation** | No | ReserveNow, CancelReservation |
| **Smart Charging** | No | SetChargingProfile, ClearChargingProfile, GetCompositeSchedule |
| **Remote Trigger** | No | TriggerMessage |

---

## 4. All 28 Messages

### 4.1 Core (16 messages)

| Message | Direction | Purpose |
|---------|-----------|---------|
| `Authorize` | CP->CS | Validate an idTag before starting a transaction. |
| `BootNotification` | CP->CS | Sent on boot. Contains vendor, model, serial, firmware version. CS responds with `Accepted`, `Pending`, or `Rejected` and a heartbeat interval. |
| `ChangeAvailability` | CS->CP | Set a Connector (or entire CP) to Operative or Inoperative. |
| `ChangeConfiguration` | CS->CP | Write a configuration key on the CP. |
| `ClearCache` | CS->CP | Clear the authorization cache. |
| `DataTransfer` | **Both** | Vendor-specific data exchange. Can be sent by either side. Uses `vendorId` and optional `messageId`. |
| `GetConfiguration` | CS->CP | Read configuration key(s) from the CP. |
| `Heartbeat` | CP->CS | Periodic keepalive. CS responds with current time for clock sync. |
| `MeterValues` | CP->CS | Send meter data for a Connector (outside or during a transaction). |
| `RemoteStartTransaction` | CS->CP | Remotely start a transaction on a Connector. |
| `RemoteStopTransaction` | CS->CP | Remotely stop a transaction by transactionId. |
| `Reset` | CS->CP | Restart the CP. Type: `Hard` or `Soft`. |
| `StartTransaction` | CP->CS | Notify CS that a transaction has started. Includes connectorId, idTag, meterStart, timestamp. CS returns transactionId. |
| `StatusNotification` | CP->CS | Report the status of a Connector (or CP as a whole). |
| `StopTransaction` | CP->CS | Notify CS that a transaction has ended. Includes transactionId, meterStop, timestamp, reason, and optional transaction data (meter values). |
| `UnlockConnector` | CS->CP | Remotely unlock a Connector. |

### 4.2 Firmware Management (4 messages)

| Message | Direction | Purpose |
|---------|-----------|---------|
| `GetDiagnostics` | CS->CP | Request CP to upload diagnostics file to a given URL. |
| `DiagnosticsStatusNotification` | CP->CS | Report diagnostics upload status (`Idle`, `Uploading`, `Uploaded`, `UploadFailed`). |
| `UpdateFirmware` | CS->CP | Instruct CP to download and install firmware from a given URL. |
| `FirmwareStatusNotification` | CP->CS | Report firmware update progress (`Downloaded`, `DownloadFailed`, `Downloading`, `Idle`, `InstallationFailed`, `Installing`, `Installed`). |

### 4.3 Local Auth List Management (2 messages)

| Message | Direction | Purpose |
|---------|-----------|---------|
| `SendLocalList` | CS->CP | Push a local authorization list (full or differential update). |
| `GetLocalListVersion` | CS->CP | Query the current version number of the local auth list. |

### 4.4 Reservation (2 messages)

| Message | Direction | Purpose |
|---------|-----------|---------|
| `ReserveNow` | CS->CP | Reserve a Connector for a specific idTag until an expiry time. |
| `CancelReservation` | CS->CP | Cancel an existing reservation by reservationId. |

### 4.5 Smart Charging (3 messages)

| Message | Direction | Purpose |
|---------|-----------|---------|
| `SetChargingProfile` | CS->CP | Set a charging profile (schedule of power/current limits) on a Connector. |
| `ClearChargingProfile` | CS->CP | Remove charging profiles by id, Connector, purpose, or stack level. |
| `GetCompositeSchedule` | CS->CP | Request the effective combined charging schedule for a Connector. |

### 4.6 Remote Trigger (1 message)

| Message | Direction | Purpose |
|---------|-----------|---------|
| `TriggerMessage` | CS->CP | Ask CP to send a specific message (e.g., `BootNotification`, `StatusNotification`, `Heartbeat`, `MeterValues`, `DiagnosticsStatusNotification`, `FirmwareStatusNotification`). |

### 4.7 Common Patterns

#### Boot Sequence

```
CP→CS: [WebSocket connect]
CP→CS: BootNotification.req(chargePointModel, chargePointVendor)
CS→CP: BootNotification.conf(status=Accepted|Pending|Rejected, interval, currentTime)
CP→CS: StatusNotification.req(connectorId=N, status, errorCode) [for each connector]
CP→CS: Heartbeat.req() [every interval seconds]
```

If `BootNotification.conf` returns `Pending`, the CP must retry after the given `interval` and must not send any messages other than `BootNotification` until it receives `Accepted`. If `Rejected`, the CP should retry at the given interval.

#### Transaction Lifecycle (typical flow)

1. User presents RFID -> CP sends `Authorize.req` with `idTag`
2. CS responds `Authorize.conf` with `idTagInfo.status=Accepted`
3. User plugs in cable -> CP sends `StatusNotification` (Preparing)
4. CP sends `StartTransaction.req` (connectorId, idTag, meterStart, timestamp)
5. CS responds `StartTransaction.conf` with `transactionId` and `idTagInfo`
6. CP sends `StatusNotification` (Charging)
7. During charging -> periodic `MeterValues.req` (every `MeterValueSampleInterval` seconds)
8. User stops -> CP sends `StopTransaction.req` (transactionId, meterStop, timestamp, reason)
9. CP sends `StatusNotification` (Finishing -> Available)

**StopTransaction reasons:** `EmergencyStop`, `EVDisconnected`, `HardReset`, `Local`, `Other`, `PowerLoss`, `Reboot`, `Remote`, `SoftReset`, `UnlockCommand`, `DeAuthorized`.

#### Smart Charging Profile Structure

```json
{
  "connectorId": 1,
  "csChargingProfiles": {
    "chargingProfileId": 1,
    "stackLevel": 0,
    "chargingProfilePurpose": "TxDefaultProfile",
    "chargingProfileKind": "Recurring",
    "recurrencyKind": "Daily",
    "chargingSchedule": {
      "chargingRateUnit": "A",
      "chargingSchedulePeriod": [
        { "startPeriod": 0, "limit": 32.0 },
        { "startPeriod": 28800, "limit": 16.0 },
        { "startPeriod": 72000, "limit": 32.0 }
      ]
    }
  }
}
```

**Profile purposes (stack priority, highest first):**
1. `ChargePointMaxProfile` — Max power for the entire Charge Point (connectorId=0 only).
2. `TxDefaultProfile` — Default for transactions on a Connector.
3. `TxProfile` — Specific to an active transaction.

Profiles at the same purpose level use `stackLevel` to determine priority (higher wins).

#### Offline Behavior

When the CP loses connection to the CS:
- It should queue transaction-related messages (`StartTransaction`, `StopTransaction`, `MeterValues`) and replay them in order upon reconnection.
- `TransactionMessageAttempts` and `TransactionMessageRetryInterval` control retry behavior.
- It can use the **Local Authorization List** or **Authorization Cache** for offline authorization.
- `LocalAuthorizeOffline` enables transaction start for locally-known IDs.
- `AllowOfflineTxForUnknownId` (when supported) enables transaction start for unknown IDs while offline.

---

## 5. Connector Status Model

The status of a Connector is reported via `StatusNotification`. OCPP 1.6 defines **9 statuses**:

| Status | Description |
|--------|-------------|
| `Available` | Connector is available for a new user. |
| `Preparing` | Connector is occupied but not yet charging (e.g., user authenticated, waiting for cable). |
| `Charging` | EV is connected and energy is actively being transferred. |
| `SuspendedEV` | EV is connected, but the EV has suspended charging (e.g., battery management). |
| `SuspendedEVSE` | EV is connected, but the EVSE (Charge Point) has suspended charging (e.g., smart charging limit). |
| `Finishing` | Transaction has stopped, but Connector is not yet available (e.g., cable still plugged in). |
| `Reserved` | Connector is reserved for a specific idTag. |
| `Unavailable` | Connector is not available for charging (set via `ChangeAvailability` to Inoperative). |
| `Faulted` | Connector is in an error state. A `ChargePointErrorCode` provides the specific error. |

**Historical note:** OCPP 1.5 used a single `Occupied` status. In OCPP 1.6, this was split into the five statuses `Preparing`, `Charging`, `SuspendedEV`, `SuspendedEVSE`, and `Finishing` to provide more granular visibility into the charging session lifecycle.

### Typical Status Flow

```
Normal flow: Available → Preparing → Charging → Finishing → Available
Suspend variations: Charging ↔ SuspendedEV, Charging ↔ SuspendedEVSE
```

A `StatusNotification` also carries a `ChargePointErrorCode` field. When the status is not `Faulted`, this is set to `NoError`. Error codes include: `ConnectorLockFailure`, `EVCommunicationError`, `GroundFailure`, `HighTemperature`, `InternalError`, `LocalListConflict`, `OtherError`, `OverCurrentFailure`, `OverVoltage`, `PowerMeterFailure`, `PowerSwitchFailure`, `ReaderFailure`, `ResetFailure`, `UnderVoltage`, `WeakSignal`.

---

## 6. Configuration Keys Reference

OCPP 1.6 uses a flat key-value configuration model accessed via `GetConfiguration` and `ChangeConfiguration`. Keys are grouped by Feature Profile.

### 6.1 Core Profile

| Key | Type | R/RW | Required | Description |
|-----|------|------|----------|-------------|
| `AllowOfflineTxForUnknownId` | boolean | RW | No | Enable Unknown Offline Authorization. |
| `AuthorizationCacheEnabled` | boolean | RW | No | Enable the authorization cache. |
| `AuthorizeRemoteTxRequests` | boolean | R/RW | Yes | Whether RemoteStartTransaction should be authorized first. |
| `BlinkRepeat` | integer | RW | No | Number of times to blink CP lighting when signalling. |
| `ClockAlignedDataInterval` | integer (s) | RW | Yes | Interval for clock-aligned meter data. 0 = disabled. |
| `ConnectionTimeOut` | integer (s) | RW | Yes | Timeout from Preparing status until transaction is cancelled. |
| `ConnectorPhaseRotation` | CSL | RW | Yes | Phase rotation per connector (e.g., `0.RST, 1.RST, 2.RTS`). |
| `ConnectorPhaseRotationMaxLength` | integer | R | No | Max items in ConnectorPhaseRotation. |
| `GetConfigurationMaxKeys` | integer | R | Yes | Max keys in a GetConfiguration request. |
| `HeartbeatInterval` | integer (s) | RW | Yes | Inactivity interval before sending Heartbeat. |
| `LightIntensity` | integer (%) | RW | No | CP lighting intensity percentage. |
| `LocalAuthorizeOffline` | boolean | RW | Yes | Start transactions for locally-authorized IDs when offline. |
| `LocalPreAuthorize` | boolean | RW | Yes | Start transactions for locally-authorized IDs without waiting for CS response. |
| `MaxEnergyOnInvalidId` | integer (Wh) | RW | No | Max energy delivered after idTag is invalidated mid-transaction. |
| `MeterValuesAlignedData` | CSL | RW | Yes | Clock-aligned measurands for MeterValues. |
| `MeterValuesAlignedDataMaxLength` | integer | R | No | Max items in MeterValuesAlignedData. |
| `MeterValuesSampledData` | CSL | RW | Yes | Sampled measurands for MeterValues. Default: `Energy.Active.Import.Register`. |
| `MeterValuesSampledDataMaxLength` | integer | R | No | Max items in MeterValuesSampledData. |
| `MeterValueSampleInterval` | integer (s) | RW | Yes | Interval between sampled meter values. 0 = disabled. |
| `MinimumStatusDuration` | integer (s) | RW | No | Min stable duration before sending StatusNotification. |
| `NumberOfConnectors` | integer | R | Yes | Number of physical connectors on this CP. |
| `ResetRetries` | integer | RW | Yes | Number of times to retry an unsuccessful reset. |
| `StopTransactionOnEVSideDisconnect` | boolean | RW | Yes | Stop transaction when cable is unplugged from EV. |
| `StopTransactionOnInvalidId` | boolean | RW | Yes | Stop transaction on non-Accepted StartTransaction.conf. |
| `StopTxnAlignedData` | CSL | RW | Yes | Clock-aligned measurands for StopTransaction.req transaction data. |
| `StopTxnAlignedDataMaxLength` | integer | R | No | Max items in StopTxnAlignedData. |
| `StopTxnSampledData` | CSL | RW | Yes | Sampled measurands for StopTransaction.req transaction data. |
| `StopTxnSampledDataMaxLength` | integer | R | No | Max items in StopTxnSampledData. |
| `SupportedFeatureProfiles` | CSL | R | Yes | Supported profiles (Core, FirmwareManagement, LocalAuthListManagement, Reservation, SmartCharging, RemoteTrigger). |
| `SupportedFeatureProfilesMaxLength` | integer | R | No | Max items in SupportedFeatureProfiles. |
| `TransactionMessageAttempts` | integer | RW | Yes | Retry count for transaction-related messages. |
| `TransactionMessageRetryInterval` | integer (s) | RW | Yes | Wait time between retries of transaction-related messages. |
| `UnlockConnectorOnEVSideDisconnect` | boolean | RW | Yes | Unlock cable on CP side when EV unplugs. |
| `WebSocketPingInterval` | integer (s) | RW | No | WebSocket ping interval. 0 = disabled (server initiates). |

### 6.2 Local Auth List Management Profile

| Key | Type | R/RW | Required | Description |
|-----|------|------|----------|-------------|
| `LocalAuthListEnabled` | boolean | RW | Yes | Whether the Local Authorization List is enabled. |
| `LocalAuthListMaxLength` | integer | R | Yes | Max identifications in the Local Authorization List. |
| `SendLocalListMaxLength` | integer | R | Yes | Max identifications in a single SendLocalList.req. |

### 6.3 Reservation Profile

| Key | Type | R/RW | Required | Description |
|-----|------|------|----------|-------------|
| `ReserveConnectorZeroSupported` | boolean | R | No | Whether reservations on connectorId=0 are supported. |

### 6.4 Smart Charging Profile

| Key | Type | R/RW | Required | Description |
|-----|------|------|----------|-------------|
| `ChargeProfileMaxStackLevel` | integer | R | Yes | Max stackLevel of a ChargingProfile. |
| `ChargingScheduleAllowedChargingRateUnit` | CSL | R | Yes | Supported rate units: `Current`, `Power`. |
| `ChargingScheduleMaxPeriods` | integer | R | Yes | Max periods per ChargingSchedule. |
| `ConnectorSwitch3to1PhaseSupported` | boolean | R | No | Whether 3-to-1 phase switching during a transaction is supported. |
| `MaxChargingProfilesInstalled` | integer | R | Yes | Max number of installed charging profiles. |

---

## 7. Key Differences from OCPP 2.0.1

### 7.1 Terminology Mapping

| OCPP 1.6 | OCPP 2.0.1 |
|----------|------------|
| Charge Point | Charging Station |
| Central System | CSMS (Charging Station Management System) |
| Connector (`connectorId`) | EVSE + Connector (`evseId` + `connectorId`) |
| `connectorId=0` (whole Charge Point) | `evseId=0` (whole Charging Station) |
| `idTag` (CiString20Type, max 20 chars) | `IdTokenType` (object with `idToken` + `type`) |
| `StartTransaction` / `StopTransaction` | `TransactionEvent` (eventType: Started/Updated/Ended) |
| `MeterValues` (separate message) | `TransactionEvent` (meter values embedded) |
| Feature Profile | Functional Block |
| `.req` / `.conf` (message suffixes) | `Request` / `Response` |
| `GetConfiguration` / `ChangeConfiguration` | `GetVariables` / `SetVariables` |
| `RemoteStartTransaction` | `RequestStartTransaction` |
| `RemoteStopTransaction` | `RequestStopTransaction` |
| `GetDiagnostics` | `GetLog` |
| `DiagnosticsStatusNotification` | `LogStatusNotification` |

### 7.2 Structural Differences

| Aspect | OCPP 1.6 | OCPP 2.0.1 |
|--------|----------|------------|
| Transport | SOAP or WebSocket + JSON | WebSocket + JSON only |
| Device model | Flat (Charge Point -> Connectors) | Hierarchical (Station -> EVSE -> Connector) |
| Transaction model | `StartTransaction` + `MeterValues` + `StopTransaction` | Unified `TransactionEvent` |
| Configuration | Flat key-value (`GetConfiguration` / `ChangeConfiguration`) | Component/Variable model (`GetVariables` / `SetVariables`) |
| Smart Charging | 3 profile purposes, basic profiles | 4 purposes (adds external constraints), EV schedules |
| Security | Basic Auth only, no certificate management | Three security profiles, certificate management, Plug & Charge |
| ISO 15118 | Not supported | Plug & Charge support |
| Display messages | Not supported | `SetDisplayMessage`, `CostUpdated` |
| Variable monitoring | Not supported | `SetVariableMonitoring`, `NotifyEvent` |
| Message count | 28 messages | 64 messages |

---

## 8. Companion Documents

This reference is part of a larger documentation set for OCPP 1.6J:

**Schemas (field-level documentation per profile):**
- [Schemas — Core](./OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-Core.md)
- [Schemas — Smart Charging](./OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-SmartCharging.md)
- [Schemas — Local Auth List](./OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-LocalAuthList.md)
- [Schemas — Firmware Management](./OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-Firmware.md)
- [Schemas — Reservation](./OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-Reservation.md)
- [Schemas — Remote Trigger](./OCPP-1.6J-Schemas/OCPP-1.6J-Schemas-RemoteTrigger.md)

**Other references:**
- [Message Sequences](./OCPP-1.6J-Sequences/OCPP-1.6J-Sequences.md) — Boot, authorization, transaction lifecycle, offline behavior
- [Smart Charging Deep-Dive](./OCPP-1.6J-SmartCharging/OCPP-1.6J-SmartCharging.md) — Profile model, composite schedule, stack levels
- [Methodology](./METHODOLOGY.md) — How these documents were produced, provenance tiers, trust model

---

*This document is a community reference for AI agents. It is not affiliated with or endorsed by the Open Charge Alliance. For the authoritative specification, refer to the official OCPP 1.6 documents from OCA.*
