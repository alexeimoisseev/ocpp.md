# OCPP.md — Open Charge Point Protocol Reference for AI Agents

> **Purpose:** This file provides structured context about the OCPP protocol for AI agents working on EV charging infrastructure. It is not a replacement for the official specification but a practical reference to ground AI-assisted development, integration, and troubleshooting.

> **Last updated:** 2026-02-08
> **Primary spec covered:** OCPP 2.0.1 (Part 1: Architecture & Topology, Part 2: Specification)
>
> Source on [Github](https://github.com/alexeimoisseev/ocpp.md).

---

## 1. What is OCPP?

OCPP (Open Charge Point Protocol) is an open application-level protocol for communication between **Electric Vehicle (EV) Charging Stations** (also called Charge Points) and a **Charging Station Management System** (CSMS, formerly called Central System). It is developed and maintained by the **Open Charge Alliance (OCA)**.

OCPP enables interoperability: a charge point from vendor A can be managed by a CSMS from vendor B, as long as both implement OCPP correctly.

### Version History

| Version | Status | Transport | Notes |
|---------|--------|-----------|-------|
| OCPP 1.2 | Legacy | SOAP/HTTP | First widely adopted version |
| OCPP 1.5 | Legacy | SOAP/HTTP | Added smart charging basics |
| OCPP 1.6 | Widely deployed | SOAP or WebSocket + JSON | Most common version in the field today |
| OCPP 2.0 | Superseded | WebSocket + JSON | Major rewrite; never widely deployed |
| OCPP 2.0.1 | **Current** | WebSocket + JSON | Bugfix/clarification release of 2.0; recommended for new deployments |
| OCPP 2.1 | In development | WebSocket + JSON | Adds ISO 15118-20, improved tariff support, and more |

### Companion Documents

This reference is part of a larger documentation set:

- **[Smart Charging Deep-Dive](./OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md)** — Profile model, composite schedule calculation, AC/DC differences, grid integration, common pitfalls. Includes [Examples](./OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-Examples.md) and [ISO 15118 integration](./OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-ISO15118.md).
- **[Message Sequences](./OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences.md)** — Boot sequence, authorization flows, transaction lifecycle. Includes [Operational Sequences](./OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences-Operational.md) (reservation, offline behavior, firmware, diagnostics).
- **[Data Types Reference](./OCPP-2.0.1-DataTypes.md)** — All reusable composite types and enumerations, plus [field-level schemas](#detailed-schema-reference) for all 64 messages.
- **[Methodology](./METHODOLOGY.md)** — How these documents were produced, provenance tiers, and trust model.
- **[AI Agent Setup](./AI-AGENT-SETUP.md)** — Full configuration guide for using this reference as a Claude Code plugin.

---

## 2. Architecture Overview (OCPP 2.0.1)

### 2.1 Roles

- **Charging Station (CS):** The physical device that charges EVs. Contains one or more EVSEs.
- **CSMS (Charging Station Management System):** The backend/server that manages charging stations remotely.

Communication is **initiated by the Charging Station**, which opens a persistent **WebSocket** connection to the CSMS. Both sides can then send messages over this connection.

### 2.2 Device Model

OCPP 2.0.1 introduced a hierarchical device model:

```
Charging Station
├── EVSE 1 (Electric Vehicle Supply Equipment)
│   ├── Connector 1 (e.g., CCS)
│   └── Connector 2 (e.g., CHAdeMO)
├── EVSE 2
│   └── Connector 1 (e.g., Type 2)
└── ...
```

- **Charging Station** is the top-level entity. It has a single connection to the CSMS.
- **EVSE** represents a separately controllable charging spot. Each EVSE can charge one EV at a time.
- **Connector** is a physical socket/plug. An EVSE may have multiple connectors, but only one can be active at a time.

**Important:** In OCPP 2.0.1, `evseId` and `connectorId` are 1-indexed integers. `evseId=0` refers to the Charging Station as a whole (used in certain messages like status notifications).

### 2.3 Transport

- **WebSocket** (RFC 6455) over TLS (wss://)
- Sub-protocol: `ocpp2.0.1`
- The Charging Station connects to the CSMS at a URL like: `wss://csms.example.com/ocpp/<charging_station_id>`
- The Charging Station ID is typically included in the WebSocket URL path.
- JSON-RPC-like message framing (see Section 3).

### 2.4 Security Profiles

OCPP 2.0.1 defines three security profiles:

| Profile | Authentication | Encryption |
|---------|---------------|------------|
| **1** | Basic Auth (HTTP) | TLS (server cert only) |
| **2** | TLS client-side certificates | TLS (mutual) |
| **3** | TLS client-side certificates + Plug & Charge | TLS (mutual) + ISO 15118 PKI |

---

## 3. Message Structure (RPC Framework)

OCPP uses a JSON-based RPC framework over WebSocket. There are three message types:

### 3.1 CALL (Request)

```json
[2, "<messageId>", "<action>", {<payload>}]
```

- `2` — MessageTypeId for CALL
- `messageId` — Unique string identifier for this request (used to correlate response)
- `action` — The name of the operation (e.g., `"BootNotification"`, `"Authorize"`)
- `payload` — JSON object with the request parameters

### 3.2 CALLRESULT (Response)

```json
[3, "<messageId>", {<payload>}]
```

- `3` — MessageTypeId for CALLRESULT
- `messageId` — Must match the CALL it responds to
- `payload` — JSON object with the response data

### 3.3 CALLERROR (Error Response)

```json
[4, "<messageId>", "<errorCode>", "<errorDescription>", {<errorDetails>}]
```

- `4` — MessageTypeId for CALLERROR
- Standard error codes include: `NotImplemented`, `NotSupported`, `InternalError`, `ProtocolError`, `SecurityError`, `FormatViolationError`, `PropertyConstraintViolation`, `OccurrenceConstraintViolation`, `TypeConstraintViolation`, `GenericError`

### 3.4 Message Flow Rules

- Only **one CALL can be outstanding** at a time per direction (CS→CSMS or CSMS→CS). A new CALL must not be sent until a CALLRESULT or CALLERROR is received for the previous one.
- Both sides can initiate CALLs independently since the connection is bidirectional.
- Messages initiated by the CS are called **CS→CSMS** messages; messages initiated by the CSMS are **CSMS→CS** messages.

---

## 4. Key Messages (OCPP 2.0.1)

### 4.1 Provisioning & Lifecycle

| Message | Direction | Purpose |
|---------|-----------|---------|
| `BootNotification` | CS→CSMS | Sent when CS boots up. Contains vendor, model, serial number, firmware version. CSMS responds with `Accepted`, `Pending`, or `Rejected` and a heartbeat interval. |
| `Heartbeat` | CS→CSMS | Periodic keepalive. CSMS responds with current time for clock sync. |
| `StatusNotification` | CS→CSMS | Reports the status of a Connector (Available, Occupied, Reserved, Unavailable, Faulted). |
| `GetVariables` | CSMS→CS | Read configuration variables from the CS. |
| `SetVariables` | CSMS→CS | Write configuration variables on the CS. |
| `GetBaseReport` | CSMS→CS | Request a full or summary report of all variables. CS responds with `NotifyReport` messages. |
| `NotifyReport` | CS→CSMS | Sends variable data in response to `GetBaseReport`. May be sent in multiple parts (seq/tbc). |
| `Reset` | CSMS→CS | Restart the CS (Immediate or OnIdle). |

### 4.2 Authorization

| Message | Direction | Purpose |
|---------|-----------|---------|
| `Authorize` | CS→CSMS | Validate an idToken (RFID, app, etc.) before starting a transaction. |
| `SendLocalList` | CSMS→CS | Push a local authorization list to the CS for offline auth. |
| `GetLocalListVersion` | CSMS→CS | Query current version of the local auth list. |

**idToken types:** `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`

**AuthorizationStatus values:** `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`

### 4.3 Transactions

OCPP 2.0.1 uses a simplified transaction model compared to 1.6.

| Message | Direction | Purpose |
|---------|-----------|---------|
| `TransactionEvent` | CS→CSMS | **The core transaction message.** Reports transaction lifecycle events. |
| `RequestStartTransaction` | CSMS→CS | Remotely start a transaction. |
| `RequestStopTransaction` | CSMS→CS | Remotely stop a transaction. |

#### TransactionEvent Details

`TransactionEvent` replaces the old `StartTransaction`, `StopTransaction`, and `MeterValues` from OCPP 1.6. It carries:

- **eventType**: `Started`, `Updated`, `Ended`
- **triggerReason**: `Authorized`, `CablePluggedIn`, `ChargingRateChanged`, `ChargingStateChanged`, `Deauthorized`, `EnergyLimitReached`, `EVCommunicationLost`, `EVConnectTimeout`, `MeterValueClock`, `MeterValuePeriodic`, `TimeLimitReached`, `Trigger`, `UnlockCommand`, `StopAuthorized`, `EVDeparted`, `EVDetected`, `RemoteStart`, `RemoteStop`, `AbnormalCondition`, `SignedDataReceived`, `ResetCommand`
- **transactionInfo**: Contains `transactionId` (string, assigned by CS), `chargingState` (`Charging`, `EVConnected`, `SuspendedEV`, `SuspendedEVSE`, `Idle`), and optionally `stoppedReason` and `remoteStartId`.
- **meterValue**: Array of sampled meter values (energy, power, current, voltage, SoC, etc.)
- **idToken**: The token used for authorization.
- **evse**: Which EVSE the transaction is on.

#### Transaction Lifecycle (typical flow)

1. User presents RFID → CS sends `Authorize`
2. CSMS responds `Accepted`
3. User plugs in cable
4. CS sends `TransactionEvent(Started, triggerReason=Authorized)`
5. Charging begins → periodic `TransactionEvent(Updated, triggerReason=MeterValuePeriodic)`
6. User stops → `TransactionEvent(Ended, triggerReason=StopAuthorized)`

### 4.4 Metering

Meter values are embedded within `TransactionEvent` messages (not sent as separate `MeterValues` messages as in 1.6).

A **MeterValue** contains a `timestamp` and an array of `sampledValue` entries, each with:

- **value** — decimal number
- **measurand** — `Energy.Active.Import.Register` (Wh, cumulative), `Power.Active.Import` (W), `Current.Import` (A), `Voltage` (V), `SoC` (%), `Frequency` (Hz), and more
- **phase** — `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1` (optional)
- **context** — `Transaction.Begin`, `Sample.Periodic`, `Sample.Clock`, `Transaction.End`, `Trigger`, `Interruption.Begin`, `Interruption.End`
- **location** — `Body`, `Cable`, `EV`, `Inlet`, `Outlet`
- **unitOfMeasure** — e.g., `{ unit: "Wh", multiplier: 0 }`

### 4.5 Smart Charging

> **Deep-dive:** For comprehensive coverage of smart charging — profile model, composite schedule calculation, AC/DC differences, grid integration, and common pitfalls — see the [Smart Charging Deep-Dive](./OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md), [Examples](./OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-Examples.md), and [ISO 15118 integration](./OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging-ISO15118.md).

Smart charging allows the CSMS to control how much power/current a CS delivers.

| Message | Direction | Purpose |
|---------|-----------|---------|
| `SetChargingProfile` | CSMS→CS | Set a charging profile (schedule of limits). |
| `GetChargingProfiles` | CSMS→CS | Retrieve active charging profiles. |
| `ClearChargingProfile` | CSMS→CS | Remove charging profiles. |
| `ClearedChargingLimit` | CS→CSMS | Notify that an external limit was cleared. |
| `NotifyChargingLimit` | CS→CSMS | Report current charging limits (from external source or grid). |
| `ReportChargingProfiles` | CS→CSMS | Response to `GetChargingProfiles`. |
| `GetCompositeSchedule` | CSMS→CS | Get the combined/effective charging schedule. |
| `NotifyEVChargingSchedule` | CS→CSMS | Report the EV's desired charging schedule (ISO 15118). |

#### Charging Profile Structure

```json
{
  "id": 1,
  "stackLevel": 0,
  "chargingProfilePurpose": "TxDefaultProfile",
  "chargingProfileKind": "Recurring",
  "recurrencyKind": "Daily",
  "chargingSchedule": [{
    "id": 1,
    "chargingRateUnit": "A",
    "chargingSchedulePeriod": [
      { "startPeriod": 0, "limit": 32.0 },
      { "startPeriod": 28800, "limit": 16.0 },
      { "startPeriod": 72000, "limit": 32.0 }
    ]
  }]
}
```

**Profile purposes (stack priority, highest first):**
1. `ChargingStationExternalConstraints` — Grid operator / external limits
2. `ChargingStationMaxProfile` — Max power for entire station
3. `TxDefaultProfile` — Default for transactions on an EVSE
4. `TxProfile` — Specific to an active transaction

Profiles at the same purpose level use `stackLevel` to determine priority (higher wins).

### 4.6 Firmware Management

| Message | Direction | Purpose |
|---------|-----------|---------|
| `UpdateFirmware` | CSMS→CS | Instruct CS to download and install firmware. |
| `FirmwareStatusNotification` | CS→CSMS | Report firmware update progress. |
| `PublishFirmware` | CSMS→CS | Ask a CS to publish firmware for local distribution. |
| `PublishFirmwareStatusNotification` | CS→CSMS | Report publish firmware status. |
| `UnpublishFirmware` | CSMS→CS | Stop publishing firmware. |

### 4.7 Diagnostics & Logging

| Message | Direction | Purpose |
|---------|-----------|---------|
| `GetLog` | CSMS→CS | Request diagnostic or security logs. |
| `LogStatusNotification` | CS→CSMS | Report log upload status. |
| `NotifyEvent` | CS→CSMS | Report events/alerts from monitored variables. |
| `SetMonitoringBase` | CSMS→CS | Set monitoring level for all variables. |
| `SetVariableMonitoring` | CSMS→CS | Configure monitoring on specific variables. |
| `SetMonitoringLevel` | CSMS→CS | Set the severity threshold for reporting. |
| `GetMonitoringReport` | CSMS→CS | Request a monitoring report. |
| `ClearVariableMonitoring` | CSMS→CS | Remove variable monitors. |
| `NotifyMonitoringReport` | CS→CSMS | Report monitoring configuration. |
| `CustomerInformation` | CSMS→CS | Request or clear customer data (GDPR). |
| `NotifyCustomerInformation` | CS→CSMS | Return customer data. |

### 4.8 Reservation

| Message | Direction | Purpose |
|---------|-----------|---------|
| `ReserveNow` | CSMS→CS | Reserve an EVSE for a specific idToken. |
| `CancelReservation` | CSMS→CS | Cancel a reservation. |
| `ReservationStatusUpdate` | CS→CSMS | Notify reservation expired or removed. |

### 4.9 Remote Triggers

| Message | Direction | Purpose |
|---------|-----------|---------|
| `TriggerMessage` | CSMS→CS | Ask CS to send a specific message (e.g., `BootNotification`, `StatusNotification`, `Heartbeat`, `MeterValues`, `FirmwareStatusNotification`). |

### 4.10 Certificate Management

| Message | Direction | Purpose |
|---------|-----------|---------|
| `Get15118EVCertificate` | CS→CSMS | Request an EV certificate (Plug & Charge). |
| `GetCertificateStatus` | CS→CSMS | Check OCSP status of a certificate. |
| `SignCertificate` | CS→CSMS | Request CSMS to sign a CSR. |
| `CertificateSigned` | CSMS→CS | Return a signed certificate. |
| `InstallCertificate` | CSMS→CS | Install a CA certificate. |
| `DeleteCertificate` | CSMS→CS | Delete a certificate. |
| `GetInstalledCertificateIds` | CSMS→CS | List installed certificates. |

### 4.11 Local Auth & Display

| Message | Direction | Purpose |
|---------|-----------|---------|
| `CostUpdated` | CSMS→CS | Push running/final cost to CS display. |
| `SetDisplayMessage` | CSMS→CS | Set a message on the CS display. |
| `GetDisplayMessages` | CSMS→CS | Retrieve display messages. |
| `ClearDisplayMessage` | CSMS→CS | Remove a display message. |
| `NotifyDisplayMessages` | CS→CSMS | Report configured display messages. |
| `UnlockConnector` | CSMS→CS | Remotely unlock a connector (to free a cable). |
| `ChangeAvailability` | CSMS→CS | Set an EVSE to operative or inoperative. |

### 4.12 Data Transfer

| Message | Direction | Purpose |
|---------|-----------|---------|
| `DataTransfer` | **Both** | Vendor-specific or custom data exchange. Can be sent by either side. Uses `vendorId` and optional `messageId` to identify the payload. |

---

## 5. Functional Blocks

OCPP 2.0.1 organizes features into **Functional Blocks** that can be independently supported:

| Block | Letter | Key Features |
|-------|--------|--------------|
| Security | B | Certificates, security events, signed firmware |
| Provisioning | B | Boot, variables, reset, base reports |
| Authorization | C | Authorize, local list, auth cache |
| Transactions | D | TransactionEvent, remote start/stop |
| Remote Control | E | Trigger, unlock, change availability |
| Availability | F | Status notifications, heartbeat |
| Metering | G | Meter values in transaction events |
| Smart Charging | H | Charging profiles, composite schedules |
| Firmware Management | I | Update, publish firmware |
| ISO 15118 Certificate Mgmt | J | Plug & Charge certificates |
| Diagnostics | K | Logs, monitoring, events |
| Display Message | L | Display and cost messages |
| Data Transfer | P | Vendor-specific extensions |
| Reservation | N | Reserve EVSE |

---

## 6. Key Configuration Variables

OCPP 2.0.1 uses a **Component/Variable** model for configuration. Some important ones:

| Component | Variable | Description |
|-----------|----------|-------------|
| `AlignedDataCtrlr` | `Interval` | Interval (s) for clock-aligned meter data |
| `AuthCtrlr` | `Enabled` | Whether authorization is required |
| `AuthCtrlr` | `OfflineTxForUnknownIdEnabled` | Allow offline transactions for unknown tokens |
| `AuthCtrlr` | `LocalAuthorizeOffline` | Use local list when offline |
| `AuthCtrlr` | `LocalPreAuthorize` | Pre-authorize from local list before checking CSMS |
| `HeartbeatCtrlr` | `Interval` | Heartbeat interval in seconds |
| `SampledDataCtrlr` | `TxUpdatedInterval` | Interval (s) for periodic meter values during tx |
| `SampledDataCtrlr` | `TxUpdatedMeasurands` | Which measurands to sample |
| `TxCtrlr` | `EVConnectionTimeOut` | Timeout (s) waiting for EV to connect after auth |
| `TxCtrlr` | `StopTxOnEVSideDisconnect` | Stop transaction when EV disconnects cable |
| `TxCtrlr` | `StopTxOnInvalidId` | Stop transaction if idToken becomes invalid |
| `OCPPCommCtrlr` | `RetryBackOffRepeatTimes` | Reconnect retry count |
| `OCPPCommCtrlr` | `RetryBackOffRandomRange` | Random reconnect backoff range (s) |
| `OCPPCommCtrlr` | `RetryBackOffWaitMinimum` | Minimum reconnect wait (s) |
| `OCPPCommCtrlr` | `WebSocketPingInterval` | WebSocket ping interval (s) |
| `SmartChargingCtrlr` | `Enabled` | Whether smart charging is supported |
| `ReservationCtrlr` | `Enabled` | Whether reservations are supported |

---

## 7. OCPP 1.6 vs 2.0.1 — Key Differences

This section is useful for agents working on migrations or systems that support both versions.

| Aspect | OCPP 1.6 | OCPP 2.0.1 |
|--------|----------|------------|
| Transport | SOAP or WebSocket+JSON | WebSocket+JSON only |
| Device model | Flat (ChargePoint → Connectors) | Hierarchical (Station → EVSE → Connector) |
| Transactions | `StartTransaction` / `StopTransaction` / `MeterValues` | Unified `TransactionEvent` |
| Configuration | Key-value (`GetConfiguration`/`ChangeConfiguration`) | Component/Variable model (`GetVariables`/`SetVariables`) |
| Smart Charging | Basic profiles | Enhanced with external constraints, EV schedules |
| Security | Minimal (basic auth) | Three security profiles, certificate management |
| ISO 15118 | Not supported | Plug & Charge support |
| Display messages | Not supported | `SetDisplayMessage`, `CostUpdated` |
| Monitoring | Not supported | Variable monitoring and event notifications |

### 1.6 Message → 2.0.1 Mapping

| OCPP 1.6 | OCPP 2.0.1 Equivalent |
|-----------|----------------------|
| `StartTransaction` | `TransactionEvent (eventType=Started)` |
| `StopTransaction` | `TransactionEvent (eventType=Ended)` |
| `MeterValues` | `TransactionEvent (eventType=Updated)` |
| `GetConfiguration` | `GetVariables` / `GetBaseReport` |
| `ChangeConfiguration` | `SetVariables` |
| `RemoteStartTransaction` | `RequestStartTransaction` |
| `RemoteStopTransaction` | `RequestStopTransaction` |
| `ChangeAvailability` | `ChangeAvailability` (now targets EVSE) |
| `DiagnosticsStatusNotification` | `LogStatusNotification` |
| `GetDiagnostics` | `GetLog` |

---

## 8. Common Implementation Patterns

> **Deep-dive:** For detailed sequence diagrams covering boot loops (Pending/Rejected), authorization with groupId/parent tokens, full transaction lifecycle, reservations, offline queueing, and firmware updates — see the [Message Sequences](./OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences.md) and [Operational Sequences](./OCPP-2.0.1-Sequences/OCPP-2.0.1-Sequences-Operational.md).

### 8.1 Boot Sequence

```
CS                                  CSMS
 |                                    |
 |--- WebSocket Connect ------------->|
 |--- BootNotification --------------->|
 |<-- BootNotificationResponse --------|  (status: Accepted/Pending/Rejected)
 |                                    |
 |--- StatusNotification (per conn) -->|  (report connector statuses)
 |                                    |
 |--- Heartbeat ---------------------->|  (periodic, per interval from boot response)
```

If `BootNotificationResponse.status` is `Pending`, the CS should retry after the `interval` and must not send any other messages except `BootNotification` until `Accepted`. If `Rejected`, the CS should retry but at the given interval.

### 8.2 Offline Behavior

When the CS loses connection to the CSMS:
- It should queue `TransactionEvent` messages and replay them in order upon reconnection.
- It can use the **Local Authorization List** or **Authorization Cache** for offline authorization.
- Configuration variable `OfflineTxForUnknownIdEnabled` controls whether unknown tokens can start transactions offline.

### 8.3 Reconnection Strategy

The CS should implement exponential backoff when reconnecting:
- Wait at least `RetryBackOffWaitMinimum` seconds
- Add a random value between 0 and `RetryBackOffRandomRange`
- Repeat up to `RetryBackOffRepeatTimes` times
- This prevents thundering herd when a CSMS restarts and many stations reconnect simultaneously.

---

## 9. JSON Schema Validation

All OCPP 2.0.1 messages have **JSON Schemas** published by OCA. Implementations should validate incoming messages against these schemas. The schemas define:
- Required vs optional fields
- Data types and formats (e.g., `dateTime` in RFC 3339 format)
- String length constraints
- Enum values
- Nested object structures

Schemas are available from the OCA website and are typically named like `BootNotificationRequest.json`, `BootNotificationResponse.json`, etc.

### Detailed Schema Reference

Complete field-level documentation for all 64 messages (request + response) is available in these companion files:

- **[Data Types Reference](./OCPP-2.0.1-DataTypes.md)** — All reusable composite types and enumerations
- **[Provisioning](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md)** — BootNotification, Heartbeat, GetVariables, SetVariables, Reset, DataTransfer, etc.
- **[Authorization](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md)** — Authorize, SendLocalList, GetLocalListVersion, ClearCache
- **[Transactions](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md)** — TransactionEvent, RequestStartTransaction, RequestStopTransaction, MeterValues
- **[Smart Charging](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md)** — SetChargingProfile, GetChargingProfiles, GetCompositeSchedule, etc.
- **[Firmware](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md)** — UpdateFirmware, PublishFirmware, FirmwareStatusNotification
- **[Security](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Security.md)** — Certificates, CSR signing, ISO 15118
- **[Diagnostics](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md)** — GetLog, NotifyEvent, variable monitoring
- **[Availability](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Availability.md)** — ChangeAvailability, UnlockConnector, TriggerMessage
- **[Reservation](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md)** — ReserveNow, CancelReservation
- **[Display](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Display.md)** — SetDisplayMessage, CostUpdated, etc.

---

## 10. Testing & Compliance

- **OCA Compliance Testing** — The Open Charge Alliance provides a compliance testing tool and test cases.
- **OCTT (OCPP Compliance Testing Tool)** — Official tool for validating OCPP implementations.
- Common test scenarios include: boot sequence, authorization flows, transaction lifecycle, offline behavior, smart charging profile application, firmware update, and security profile negotiation.

---

## 11. Useful Resources

- **OCA Official Site:** https://openchargealliance.org
- **OCPP 2.0.1 Specification:** Available for download from OCA (requires free registration)
- **OCPP 2.0.1 JSON Schemas:** Published alongside the specification
- **OCA GitHub:** Example implementations and schemas

---

## 12. Using with AI Coding Agents

This reference is available as a **Claude Code plugin**. Install it once and your AI assistant gets structured OCPP 2.0.1 knowledge in every project.

### Quick Setup

```
/plugin marketplace add https://github.com/alexeimoisseev/ocpp.md
/plugin install ocpp@ocpp
```

Once installed, the plugin activates automatically when working with OCPP code. You can also invoke it directly:

```
/ocpp                    # General OCPP assistance
/ocpp smart-charging     # Smart charging deep-dive
/ocpp transactions       # Transaction handling
/ocpp authorize          # Authorization flow
```

### What the Agent Gets

The plugin provides a hybrid reference: a compact inline summary (all 64 messages, key types, escalation model) is always available, while detailed schemas, sequence diagrams, and worked examples are loaded on demand when needed.

### Escalation Handling

The OCPP spec has areas that are silent, vendor-dependent, or policy-dependent. The plugin prevents the agent from silently guessing in these areas. By default it uses **strict** mode (stops and asks). To switch to pragmatic mode, add to your `CLAUDE.md`:

```
For OCPP: use pragmatic escalation mode.
```

- **strict** (default) — agent stops and asks before making assumptions
- **pragmatic** — agent flags ambiguity with a code comment but picks a reasonable default

See the full [AI Agent Setup guide](./AI-AGENT-SETUP.md) for manual installation and detailed configuration.

---

## 13. Glossary

| Term | Definition |
|------|-----------|
| **CSMS** | Charging Station Management System (the backend server) |
| **CS** | Charging Station (the physical charger) |
| **EVSE** | Electric Vehicle Supply Equipment — a single charging spot |
| **Connector** | Physical plug/socket on an EVSE |
| **idToken** | An identifier used for authorization (RFID UID, eMAID, etc.) |
| **eMAID** | e-Mobility Account Identifier (used in Plug & Charge) |
| **SoC** | State of Charge (battery percentage) |
| **Plug & Charge** | ISO 15118-based automatic auth via EV certificate |
| **Measurand** | A type of meter measurement (energy, power, current, voltage, etc.) |
| **Charging Profile** | A schedule defining power/current limits over time |
| **Composite Schedule** | The effective schedule after combining all active profiles |
| **Local List** | A list of pre-authorized idTokens stored on the CS |
| **OCTT** | OCPP Compliance Testing Tool |
| **OCA** | Open Charge Alliance — the standards body for OCPP |

---

*This document is a community reference for AI agents. It is not affiliated with or endorsed by the Open Charge Alliance. For the authoritative specification, refer to the official OCPP 2.0.1 documents from OCA.*
