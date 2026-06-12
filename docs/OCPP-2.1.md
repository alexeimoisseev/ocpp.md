# OCPP 2.1 — Overview and 2.0.1 → 2.1 Migration Guide

> **Purpose:** Top-level reference for AI agents working with OCPP 2.1. Provides the protocol overview, the full message catalogue grouped by functional block, the new capability areas (DER control, bidirectional/V2X, tariff & cost, periodic event streams, battery swap, dynamic/priority charging, ISO 15118-20), and a structured migration guide from OCPP 2.0.1. It is not a replacement for the official OCA specification but a practical grounding reference.

> **Last updated:** 2026-06-08
> **Primary spec covered:** OCPP 2.1 Edition 2 (2025) — Part 1 Architecture & Topology, Part 2 Specification, Part 4 OCPP-J
>
> Source on [Github](https://github.com/alexeimoisseev/ocpp.md).

---

## How This Document Was Produced

This document is an overview and migration guide for OCPP 2.1. It mixes two confidence tiers. Mechanical facts — exact message names, which functional block a message belongs to, and message direction — are **schema-derived**: every message named here is cross-referenced to a `## <MessageName>` section in the mechanically generated schema docs under [OCPP-2.1-Schemas/](./OCPP-2.1-Schemas/), which were extracted directly from the official OCA OCPP 2.1 JSON schemas. The behavioral and migration narrative (what each capability area is for, how 2.1 differs from 2.0.1, backward-compatibility notes) is **spec-knowledge** — drawn from the OCPP 2.1 Edition 2 specification known via AI training data and the Part 1/2/4 source PDFs. Original wording is used throughout; the OCA specification is licensed CC BY-ND, so no spec prose is reproduced verbatim.

This document contains **1 escalation point** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer to make the decision. See [METHODOLOGY.md](./METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**

Mechanically generated (schema-derived, high confidence):
- [Message Schemas](./OCPP-2.1-Schemas/) — field-level request/response schemas for all 91 messages, one file per functional block (linked individually in [§4](#4-message-catalogue-by-functional-block)).
- [Data Types Reference](./OCPP-2.1-DataTypes.md) — shared composite types used across blocks.
- [Device Model Reference](./OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md) — components, variables, and the standardized device model.
- [Enumerations Reference](./OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md) — all enumeration types and their allowed values.

AI-authored deep-dives (spec-knowledge; some are forward-references not yet written — see note):
- [DER Control Deep-Dive](./OCPP-2.1-DERControl/OCPP-2.1-DERControl.md) — distributed energy resource control (Block R).
- [Bidirectional / V2X Deep-Dive](./OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) — vehicle-to-grid energy transfer (Block Q).
- [Tariff & Cost Deep-Dive](./OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md) — tariffs, settlement, and cost (Block I).
- [Smart Charging Deep-Dive](./OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md) — charging profiles, dynamic and priority charging (Block K).
- [Message Sequences](./OCPP-2.1-Sequences/OCPP-2.1-Sequences.md) — boot, transaction, and operational flows.

> **Note:** The five AI-authored deep-dive documents above are **forward-references** to documents not yet created at the time of writing. The link paths are the correct final locations.

---

## 1. What is OCPP?

OCPP (Open Charge Point Protocol) is an open application-level protocol for communication between **EV Charging Stations** (CS, also called Charge Points) and a **Charging Station Management System** (CSMS, historically "Central System"). It is developed and maintained by the **Open Charge Alliance (OCA)**.

OCPP enables interoperability: a charging station from one vendor can be managed by a CSMS from another, as long as both implement the protocol correctly.

### 1.1 Version History

| Version | Status | Transport | Subprotocol | Notes |
|---------|--------|-----------|-------------|-------|
| OCPP 1.2 | Legacy | SOAP/HTTP | — | First widely adopted version |
| OCPP 1.5 | Legacy | SOAP/HTTP | — | Added smart charging basics |
| OCPP 1.6 | Widely deployed | SOAP or WebSocket + JSON | `ocpp1.6` | Most common version in the field today |
| OCPP 2.0 | Superseded | WebSocket + JSON | `ocpp2.0` | Major rewrite; never widely deployed |
| OCPP 2.0.1 | Widely deployed | WebSocket + JSON | `ocpp2.0.1` | Bugfix/clarification release of 2.0; current baseline for many deployments |
| OCPP 2.1 | **Published (Edition 2, 2025)** | WebSocket + JSON | `ocpp2.1` | Superset of 2.0.1. Adds DER control, bidirectional/V2X, tariff & cost, battery swap, periodic event streams, dynamic/priority charging, and ISO 15118-20 |

OCPP 2.1 is a **published standard**, not a work in progress. It is a functional superset of 2.0.1: all 64 of 2.0.1's messages are retained unchanged, and 27 net-new messages are added, for a total of **91 messages**. See [§6 Migration](#6-ocpp-201--21-migration) for the compatibility model.

### 1.2 Transport

- **WebSocket** (RFC 6455), normally over TLS (`wss://`).
- WebSocket subprotocol identifier: **`ocpp2.1`** (per OCPP-J, Part 4).
- The same JSON-RPC-style message framing as 2.0.1 (CALL / CALLRESULT / CALLERROR — see [§3](#3-message-framing-rpc)). OCPP 2.1 adds **CALLRESULTERROR** (5) for unprocessable CALLRESULT responses and the one-way **SEND** (6) for periodic event streams (see [§3](#3-message-framing-rpc)).
- The Charging Station opens the connection to the CSMS, typically at a URL like `wss://csms.example.com/ocpp/<charging_station_id>`.

---

## 2. Architecture & Roles

### 2.1 Roles

- **Charging Station (CS):** the physical device that charges EVs; contains one or more EVSEs.
- **CSMS (Charging Station Management System):** the backend that manages charging stations remotely.

The Charging Station always initiates the connection. Once established, the connection is bidirectional: either side may send a request.

### 2.2 Device Model

OCPP 2.1 keeps the hierarchical device model introduced in 2.0.1. Rather than an ASCII tree, the hierarchy is described here as a table.

| Level | Entity | Cardinality | `id` semantics | Role |
|-------|--------|-------------|----------------|------|
| 0 | Charging Station | exactly 1 | `evseId = 0` addresses the whole station | Top-level entity; single connection to the CSMS |
| 1 | EVSE | 1..N per station | `evseId` is a 1-indexed integer | A separately controllable charging spot; charges one EV at a time |
| 2 | Connector | 1..N per EVSE | `connectorId` is a 1-indexed integer within its EVSE | A physical socket/plug; only one connector per EVSE is active at a time |

Beyond the physical EVSE/connector hierarchy, OCPP 2.1 (like 2.0.1) models configuration through a **Component / Variable** abstraction. A `Component` (optionally scoped to an EVSE) holds `Variable`s that are read with `GetVariables`/`GetReport` and written with `SetVariables`. The full standardized component/variable catalogue is in the [Device Model Reference](./OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md).

### 2.3 What is New Conceptually in 2.1

| Area | Summary |
|------|---------|
| Grid services (DER) | The station can act as a managed Distributed Energy Resource: the CSMS configures volt-watt, frequency-watt, power-factor and similar curves (Block R). |
| Bidirectional / V2X | Explicit support for energy flowing from the EV back to the grid, including AFRR (automatic frequency restoration reserve) signalling (Block Q). |
| Tariff & cost | A first-class tariff model (default tariffs, per-transaction tariff changes, settlement, VAT) replacing ad-hoc cost messaging (Block I). |
| Battery swap | Workflow for battery-swap stations that exchange a depleted pack for a charged one (Block S). |
| Periodic event streams | A one-way, high-frequency telemetry channel using the SEND message type, layered into Diagnostics (Block N). |
| Dynamic & priority charging | Pull/push schedule updates and priority-charging signalling on top of the existing profile model (Block K). |
| ISO 15118-20 | Updated Plug & Charge and bidirectional power-transfer support aligned with ISO 15118-20. |

### 2.4 Security Profiles

OCPP 2.1 retains the three security profiles from 2.0.1.

| Profile | Authentication | Encryption |
|---------|----------------|------------|
| 1 | HTTP Basic Auth | TLS (server cert only) |
| 2 | TLS client certificate | TLS (mutual) |
| 3 | TLS client certificate + Plug & Charge | TLS (mutual) + ISO 15118 PKI |

---

## 3. Message Framing (RPC)

OCPP 2.1 uses the same JSON-array RPC framing as 2.0.1, plus a new one-way message type.

| MessageTypeId | Name | Frame | Purpose |
|---------------|------|-------|---------|
| 2 | CALL | `[2, "<messageId>", "<action>", {payload}]` | Request; expects a matching CALLRESULT or CALLERROR |
| 3 | CALLRESULT | `[3, "<messageId>", {payload}]` | Success response, correlated by `messageId` |
| 4 | CALLERROR | `[4, "<messageId>", "<errorCode>", "<errorDescription>", {details}]` | Error response |
| 5 | CALLRESULTERROR | `[5, "<messageId>", "<errorCode>", "<errorDescription>", {errorDetails}]` | New in OCPP 2.1 (Part 4). Sent when a received CALLRESULT cannot be processed by the recipient. |
| 6 | SEND | `[6, "<messageId>", "<action>", {payload}]` | **New in 2.1.** One-way fire-and-forget message; no response is sent. Used by `NotifyPeriodicEventStream` for high-rate telemetry |

Flow rules (unchanged from 2.0.1): at most one CALL may be outstanding per direction at a time; both sides may initiate CALLs independently. SEND messages are not subject to the request/response correlation rule because they carry no response.

---

## 4. Message Catalogue by Functional Block

OCPP 2.1 organizes its **91 messages** into **19 functional blocks (A–S)**. The tables below are schema-derived: message names, block membership, and directions come directly from the `## Messages` list at the top of each generated schema file. Each block header links to its schema file; each message links to its `## <MessageName>` section within that file.

Messages new in 2.1 are flagged **(new)**.

### Block A — Security · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Security.md)

| Message | Direction |
|---------|-----------|
| [SecurityEventNotification](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Security.md#securityeventnotification) | CS → CSMS |

### Block B — Provisioning · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md)

| Message | Direction |
|---------|-----------|
| [BootNotification](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) | CS → CSMS |
| [Heartbeat](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat) | CS → CSMS |
| [GetBaseReport](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getbasereport) | CSMS → CS |
| [GetReport](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getreport) | CSMS → CS |
| [NotifyReport](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#notifyreport) | CS → CSMS |
| [GetVariables](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getvariables) | CSMS → CS |
| [SetVariables](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) | CSMS → CS |
| [SetNetworkProfile](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setnetworkprofile) | CSMS → CS |
| [Reset](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#reset) | CSMS → CS |

### Block C — Authorization · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md)

| Message | Direction |
|---------|-----------|
| [Authorize](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) | CS → CSMS |
| [ClearCache](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#clearcache) | CSMS → CS |

### Block D — LocalAuthList · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md)

| Message | Direction |
|---------|-----------|
| [SendLocalList](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#sendlocallist) | CSMS → CS |
| [GetLocalListVersion](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#getlocallistversion) | CSMS → CS |

### Block E — Transactions · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md)

| Message | Direction |
|---------|-----------|
| [TransactionEvent](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) | CS → CSMS |
| [GetTransactionStatus](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#gettransactionstatus) | CSMS → CS |

### Block F — RemoteControl · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md)

| Message | Direction |
|---------|-----------|
| [RequestStartTransaction](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction) | CSMS → CS |
| [RequestStopTransaction](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststoptransaction) | CSMS → CS |
| [UnlockConnector](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#unlockconnector) | CSMS → CS |
| [TriggerMessage](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#triggermessage) | CSMS → CS |

### Block G — Availability · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md)

| Message | Direction |
|---------|-----------|
| [ChangeAvailability](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#changeavailability) | CSMS → CS |
| [StatusNotification](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification) | CS → CSMS |

### Block H — Reservation · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md)

| Message | Direction |
|---------|-----------|
| [ReserveNow](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#reservenow) | CSMS → CS |
| [CancelReservation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#cancelreservation) | CSMS → CS |
| [ReservationStatusUpdate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#reservationstatusupdate) | CS → CSMS |

### Block I — TariffAndCost (new in 2.1) · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md)

| Message | Direction | New |
|---------|-----------|-----|
| [CostUpdated](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#costupdated) | CSMS → CS | reassigned from Block O (Display) in 2.0.1 |
| [GetTariffs](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#gettariffs) | CSMS → CS | **(new)** |
| [SetDefaultTariff](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#setdefaulttariff) | CSMS → CS | **(new)** |
| [ChangeTransactionTariff](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#changetransactiontariff) | CSMS → CS | **(new)** |
| [ClearTariffs](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#cleartariffs) | CSMS → CS | **(new)** |
| [NotifySettlement](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) | CS → CSMS | **(new)** |
| [NotifyWebPaymentStarted](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifywebpaymentstarted) | CSMS → CS | **(new)** |
| [VatNumberValidation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#vatnumbervalidation) | CS → CSMS | **(new)** |

### Block J — MeterValues · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-MeterValues.md)

| Message | Direction |
|---------|-----------|
| [MeterValues](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-MeterValues.md#metervalues) | CS → CSMS |

### Block K — SmartCharging · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md)

| Message | Direction | New |
|---------|-----------|-----|
| [SetChargingProfile](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile) | CSMS → CS | |
| [GetChargingProfiles](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#getchargingprofiles) | CSMS → CS | |
| [ClearChargingProfile](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearchargingprofile) | CSMS → CS | |
| [ReportChargingProfiles](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#reportchargingprofiles) | CS → CSMS | |
| [GetCompositeSchedule](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#getcompositeschedule) | CSMS → CS | |
| [ClearedChargingLimit](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearedcharginglimit) | CS → CSMS | |
| [NotifyChargingLimit](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit) | CS → CSMS | |
| [NotifyEVChargingSchedule](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingschedule) | CS → CSMS | |
| [NotifyEVChargingNeeds](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds) | CS → CSMS | |
| [PullDynamicScheduleUpdate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate) | CS → CSMS | **(new)** |
| [UpdateDynamicSchedule](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule) | CSMS → CS | **(new)** |
| [NotifyPriorityCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyprioritycharging) | CS → CSMS | **(new)** |
| [UsePriorityCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#useprioritycharging) | CSMS → CS | **(new)** |

### Block L — Firmware · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md)

| Message | Direction |
|---------|-----------|
| [UpdateFirmware](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#updatefirmware) | CSMS → CS |
| [FirmwareStatusNotification](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#firmwarestatusnotification) | CS → CSMS |
| [PublishFirmware](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#publishfirmware) | CSMS → CS |
| [PublishFirmwareStatusNotification](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#publishfirmwarestatusnotification) | CS → CSMS |
| [UnpublishFirmware](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#unpublishfirmware) | CSMS → CS |

### Block M — Certificates · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md)

| Message | Direction | New |
|---------|-----------|-----|
| [Get15118EVCertificate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#get15118evcertificate) | CS → CSMS | |
| [GetCertificateStatus](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getcertificatestatus) | CS → CSMS | |
| [GetCertificateChainStatus](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getcertificatechainstatus) | CS → CSMS | **(new)** |
| [SignCertificate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#signcertificate) | CS → CSMS | |
| [CertificateSigned](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#certificatesigned) | CSMS → CS | |
| [InstallCertificate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#installcertificate) | CSMS → CS | |
| [DeleteCertificate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#deletecertificate) | CSMS → CS | |
| [GetInstalledCertificateIds](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getinstalledcertificateids) | CSMS → CS | |

### Block N — Diagnostics · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md)

| Message | Direction | New |
|---------|-----------|-----|
| [GetLog](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getlog) | CSMS → CS | |
| [LogStatusNotification](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#logstatusnotification) | CS → CSMS | |
| [NotifyEvent](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) | CS → CSMS | |
| [SetMonitoringBase](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setmonitoringbase) | CSMS → CS | |
| [SetVariableMonitoring](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setvariablemonitoring) | CSMS → CS | |
| [SetMonitoringLevel](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setmonitoringlevel) | CSMS → CS | |
| [GetMonitoringReport](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getmonitoringreport) | CSMS → CS | |
| [ClearVariableMonitoring](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#clearvariablemonitoring) | CSMS → CS | |
| [NotifyMonitoringReport](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifymonitoringreport) | CS → CSMS | |
| [CustomerInformation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#customerinformation) | CSMS → CS | |
| [NotifyCustomerInformation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifycustomerinformation) | CS → CSMS | |
| [OpenPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#openperiodiceventstream) | CS → CSMS | **(new)** |
| [ClosePeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#closeperiodiceventstream) | CS → CSMS | **(new)** |
| [GetPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getperiodiceventstream) | CSMS → CS | **(new)** |
| [AdjustPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#adjustperiodiceventstream) | CSMS → CS | **(new)** |
| [NotifyPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream) | CS → CSMS (one-way SEND) | **(new)** |

### Block O — Display · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md)

| Message | Direction |
|---------|-----------|
| [SetDisplayMessage](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#setdisplaymessage) | CSMS → CS |
| [GetDisplayMessages](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#getdisplaymessages) | CSMS → CS |
| [ClearDisplayMessage](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#cleardisplaymessage) | CSMS → CS |
| [NotifyDisplayMessages](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#notifydisplaymessages) | CS → CSMS |

> **Note:** In 2.0.1 the `CostUpdated` message lived in the Display block. In 2.1 it is reassigned to Block I (TariffAndCost). See [§6.3](#63-costupdated-reassignment).

### Block P — DataTransfer · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DataTransfer.md)

| Message | Direction |
|---------|-----------|
| [DataTransfer](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DataTransfer.md#datatransfer) | Both |

### Block Q — Bidirectional / V2X (new in 2.1) · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md)

| Message | Direction | New |
|---------|-----------|-----|
| [NotifyAllowedEnergyTransfer](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer) | CSMS → CS | **(new)** |
| [AFRRSignal](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#afrrsignal) | CSMS → CS | **(new)** |

### Block R — DERControl (new in 2.1) · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md)

| Message | Direction | New |
|---------|-----------|-----|
| [GetDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#getdercontrol) | CSMS → CS | **(new)** |
| [SetDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol) | CSMS → CS | **(new)** |
| [ClearDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#cleardercontrol) | CSMS → CS | **(new)** |
| [ReportDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reportdercontrol) | CS → CSMS | **(new)** |
| [NotifyDERAlarm](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm) | CS → CSMS | **(new)** |
| [NotifyDERStartStop](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop) | CS → CSMS | **(new)** |

### Block S — BatterySwap (new in 2.1) · [schemas](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md)

| Message | Direction | New |
|---------|-----------|-----|
| [BatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap) | CS → CSMS | **(new)** |
| [RequestBatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#requestbatteryswap) | CSMS → CS | **(new)** |

---

## 5. New Capability Areas

Short orientation for each new area. Deep behavioral coverage lives in the linked Phase C deep-dives (forward-references where noted in the header).

### 5.1 DER Control (Block R)

OCPP 2.1 lets the CSMS treat a charging station as a managed **Distributed Energy Resource**. The CSMS installs DER control settings — characteristic curves and setpoints such as volt-watt, volt-var, frequency-watt, fixed power factor, and reactive-power control — with [SetDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol), reads them back with [GetDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#getdercontrol) (answered by [ReportDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reportdercontrol)), and removes them with [ClearDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#cleardercontrol). The station reports grid-protection trips and curtailments through [NotifyDERAlarm](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm) and start/stop of DER functions through [NotifyDERStartStop](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop). See the [DER Control Deep-Dive](./OCPP-2.1-DERControl/OCPP-2.1-DERControl.md).

### 5.2 Bidirectional / V2X (Block Q)

Block Q makes vehicle-to-grid energy flow explicit. The CSMS authorizes the direction and amount of energy transfer with [NotifyAllowedEnergyTransfer](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer) and drives fast grid-balancing with [AFRRSignal](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#afrrsignal) (Automatic Frequency Restoration Reserve). Discharging is also coordinated with the DER controls in Block R and the dynamic schedules in Block K. See the [Bidirectional / V2X Deep-Dive](./OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md).

### 5.3 Tariff & Cost (Block I)

OCPP 2.1 introduces a first-class tariff model. The CSMS pushes a default tariff per EVSE with [SetDefaultTariff](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#setdefaulttariff), swaps the tariff of a running transaction with [ChangeTransactionTariff](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#changetransactiontariff), inspects installed tariffs with [GetTariffs](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#gettariffs), and removes them with [ClearTariffs](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#cleartariffs). Settlement/clearing data flows back with [NotifySettlement](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement); web-payment kiosks signal start with [NotifyWebPaymentStarted](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifywebpaymentstarted); and VAT identifiers are checked with [VatNumberValidation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#vatnumbervalidation). Running/final cost still reaches the display via [CostUpdated](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#costupdated), which now lives in this block. See the [Tariff & Cost Deep-Dive](./OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md).

### 5.4 Periodic Event Streams (Block N, N11–N15)

The Diagnostics block gains a streaming telemetry channel. The station offers a stream with [OpenPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#openperiodiceventstream) and tears it down with [ClosePeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#closeperiodiceventstream); the CSMS enumerates active streams with [GetPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getperiodiceventstream) and retunes their rate with [AdjustPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#adjustperiodiceventstream). The actual high-frequency data is pushed with [NotifyPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream), which is a **one-way SEND** message (MessageTypeId 6) and therefore generates no response — this keeps high-rate telemetry from consuming the single-outstanding-CALL slot.

### 5.5 Battery Swap (Block S)

For battery-swap stations, the CSMS asks for a swap with [RequestBatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#requestbatteryswap) and the station reports swap events (battery insertion/removal, identifiers, state of health) with [BatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap).

### 5.6 Dynamic & Priority Charging (Block K)

On top of the existing profile model, 2.1 adds dynamic schedules and priority charging. The station pulls an updated schedule setpoint with [PullDynamicScheduleUpdate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate) and the CSMS pushes one with [UpdateDynamicSchedule](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule). Priority charging (e.g. a driver-requested boost) is requested by the CSMS with [UsePriorityCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#useprioritycharging) and reported by the station with [NotifyPriorityCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyprioritycharging). See the [Smart Charging Deep-Dive](./OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md).

### 5.7 ISO 15118-20

OCPP 2.1 aligns Plug & Charge and bidirectional power transfer with **ISO 15118-20**, layered onto the existing 15118-2 support. This underpins V2X (Block Q) and updates the certificate/EV-schedule exchange used by Plug & Charge. Certificate handling adds [GetCertificateChainStatus](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getcertificatechainstatus) for validating full chains.

---

## 6. OCPP 2.0.1 → 2.1 Migration

OCPP 2.1 is a **structural superset** of 2.0.1. An existing 2.0.1 implementation remains valid: the same draft-06 JSON Schema framing is used, the `customData` extension pattern is unchanged, and all 64 of 2.0.1's messages are retained with the same names and directions. Migration is therefore additive — implement the new blocks/messages you need, and negotiate the `ocpp2.1` subprotocol.

### 6.1 The 27 New Messages

The 27 net-new messages added in 2.1 (64 retained + 27 new = 91 total). All names below resolve to a `## <MessageName>` section in the linked schema files.

| Message | Block | Direction | Purpose |
|---------|-------|-----------|---------|
| [AFRRSignal](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#afrrsignal) | Q | CSMS → CS | Send an automatic frequency restoration reserve setpoint for fast grid balancing. |
| [AdjustPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#adjustperiodiceventstream) | N | CSMS → CS | Change the sampling/reporting parameters of an active event stream. |
| [BatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap) | S | CS → CSMS | Report a battery-swap event (insertion/removal, battery identity and state). |
| [ChangeTransactionTariff](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#changetransactiontariff) | I | CSMS → CS | Replace the tariff applied to an in-progress transaction. |
| [ClearDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#cleardercontrol) | R | CSMS → CS | Remove one or more installed DER control settings. |
| [ClearTariffs](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#cleartariffs) | I | CSMS → CS | Remove installed tariffs from the station. |
| [ClosePeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#closeperiodiceventstream) | N | CS → CSMS | Close a previously opened periodic event stream. |
| [GetCertificateChainStatus](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getcertificatechainstatus) | M | CS → CSMS | Query the revocation/validity status of a certificate chain. |
| [GetDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#getdercontrol) | R | CSMS → CS | Request the station's current DER control settings (answered by ReportDERControl). |
| [GetPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getperiodiceventstream) | N | CSMS → CS | Enumerate the station's active periodic event streams. |
| [GetTariffs](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#gettariffs) | I | CSMS → CS | Retrieve the tariffs currently installed on the station. |
| [NotifyAllowedEnergyTransfer](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer) | Q | CSMS → CS | Tell the station which energy-transfer modes/directions are permitted. |
| [NotifyDERAlarm](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm) | R | CS → CSMS | Report a DER grid-protection alarm or curtailment event. |
| [NotifyDERStartStop](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop) | R | CS → CSMS | Report that a DER control function started or stopped. |
| [NotifyPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream) | N | CS → CSMS (one-way SEND) | Push high-frequency streamed telemetry; no response. |
| [NotifyPriorityCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyprioritycharging) | K | CS → CSMS | Report the priority-charging state for a transaction. |
| [NotifySettlement](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) | I | CS → CSMS | Report payment/settlement (clearing) data for a transaction. |
| [NotifyWebPaymentStarted](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifywebpaymentstarted) | I | CSMS → CS | Inform the station that a web/QR payment session has started. |
| [OpenPeriodicEventStream](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#openperiodiceventstream) | N | CS → CSMS | Open a new periodic event stream with the CSMS. |
| [PullDynamicScheduleUpdate](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate) | K | CS → CSMS | Request an updated setpoint for a dynamic charging schedule. |
| [ReportDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reportdercontrol) | R | CS → CSMS | Return DER control settings in response to GetDERControl. |
| [RequestBatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#requestbatteryswap) | S | CSMS → CS | Request the station to perform a battery swap. |
| [SetDefaultTariff](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#setdefaulttariff) | I | CSMS → CS | Install the default tariff for an EVSE. |
| [SetDERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol) | R | CSMS → CS | Install or update a DER control setting (curve/setpoint). |
| [UpdateDynamicSchedule](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule) | K | CSMS → CS | Push an updated dynamic charging schedule setpoint. |
| [UsePriorityCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#useprioritycharging) | K | CSMS → CS | Request that priority charging be applied to a transaction. |
| [VatNumberValidation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#vatnumbervalidation) | I | CS → CSMS | Validate a customer VAT number for invoicing. |

### 6.2 The 4 New Functional Blocks

OCPP 2.0.1 defined 15 functional blocks (A–P, with letter I unassigned). OCPP 2.1 fills letter I with the new TariffAndCost block and appends Q, R, S — 19 blocks total.

| Block | Letter | Theme | Messages |
|-------|--------|-------|----------|
| TariffAndCost | I | Tariff model, settlement, VAT, cost-to-display | 8 (incl. the reassigned `CostUpdated`) |
| Bidirectional | Q | Vehicle-to-grid / V2X, AFRR | 2 |
| DERControl | R | Distributed energy resource grid services | 6 |
| BatterySwap | S | Battery-swap station workflow | 2 |

### 6.3 CostUpdated Reassignment

`CostUpdated` (CSMS → CS) existed in 2.0.1 as part of the **Display** block (O). In 2.1 it is **reassigned to the TariffAndCost block (I)**, alongside the new tariff and settlement messages. The message itself is otherwise carried forward; only its block membership changes. Implementations that grouped handlers by block should move `CostUpdated` accordingly.

### 6.4 OCPP-J Version Negotiation

Version is negotiated through the WebSocket `Sec-WebSocket-Protocol` header (OCPP-J, Part 4). A station that supports 2.1 and wants backward compatibility offers, in preference order:

```
Sec-WebSocket-Protocol: ocpp2.1, ocpp2.0.1, ocpp1.6
```

The CSMS echoes the single subprotocol it selects, e.g. `Sec-WebSocket-Protocol: ocpp2.1`. The selected subprotocol fixes the message set and framing for the connection. Because all 64 of 2.0.1's messages are retained unchanged in 2.1, a CSMS can fall back to `ocpp2.0.1` for older stations without code divergence on the shared messages.

### 6.5 Backward Compatibility Summary

| Aspect | 2.0.1 | 2.1 | Migration impact |
|--------|-------|-----|------------------|
| JSON Schema framing | draft-06 | draft-06 | None — same validation tooling |
| `customData` extension | supported | supported (unchanged pattern) | None |
| Retained messages | 64 | 64 (identical) | None — existing handlers keep working |
| New messages | — | 27 | Additive — implement only what you need |
| Functional blocks | A–P (15) | A–S (19) | 4 new blocks; `CostUpdated` moves O → I |
| Subprotocol | `ocpp2.0.1` | `ocpp2.1` | Negotiate via `Sec-WebSocket-Protocol` |
| Message types | CALL / CALLRESULT / CALLERROR | + CALLRESULTERROR (5) and SEND (6, one-way) | Add handling for CALLRESULTERROR and SEND (periodic event streams) |

> **ESCALATE:** The brief instructs treating message direction and block membership as PDF-verified and schema-derived, but it does not confirm whether your target CSMS/CS deployment must *also* keep negotiating `ocpp2.0.1`/`ocpp1.6` for a mixed fleet, or move to `ocpp2.1`-only. This is a deployment-policy decision (fleet composition, certification scope) the AI agent cannot infer from the spec. Stop and ask the developer which subprotocols to advertise/accept before changing negotiation code.

---

*This document is a community reference for AI agents. It is not affiliated with or endorsed by the Open Charge Alliance. For the authoritative specification, refer to the official OCPP 2.1 documents from OCA.*
