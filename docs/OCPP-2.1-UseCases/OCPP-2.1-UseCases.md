# OCPP 2.1 — Use-Case Catalog (Part 2)

> **Purpose:** A catalog of every OCPP 2.1 Part 2 use case across functional blocks A–S. For each use case it records its ID, purpose, the messages involved, and any escalation flags — a single index an AI agent can scan to find the right use case and jump to the relevant schema and deep-dive references.

> **Last updated:** 2026-06-11

---

## How This Document Was Produced

This document catalogs the use cases of the OCPP 2.1 Edition 2 Part 2 specification (functional blocks A–S). Each entry is an **original summary** — a short restatement of what the use case does in original wording, **not verbatim spec prose** (the OCA specification is CC BY-ND licensed). Its dominant confidence tier is **spec-knowledge** for the behavioral description of each use case; the **message names** referenced in each entry are **schema-derived**, cross-referenced against the per-block schema references listed below, all mechanically extracted from the official OCA artifacts.

This document will contain escalation points marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer (or relevant stakeholder) to make the decision. The escalation count will be finalized when the per-use-case summaries are authored. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

Each catalog entry below will list:
- **Purpose** — what the use case accomplishes.
- **Messages** — the OCPP messages involved, linked to the per-block schema references.
- **Escalation flags** — any decisions an AI agent must defer to a developer or stakeholder.

**Companion documents:**
- [Security Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Security.md)
- [Provisioning Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md)
- [Authorization Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md)
- [Local Authorization List Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md)
- [Transactions Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md)
- [Remote Control Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md)
- [Availability Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md)
- [Reservation Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md)
- [Tariff And Cost Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md)
- [Meter Values Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-MeterValues.md)
- [Smart Charging Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md)
- [Firmware Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md)
- [Certificates Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md)
- [Diagnostics Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md)
- [Display Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md)
- [Data Transfer Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DataTransfer.md)
- [Bidirectional Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md)
- [DER Control Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md)
- [Battery Swap Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md)
- [DER Control Deep-Dive](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md)
- [Bidirectional Power Transfer (V2X) Deep-Dive](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md)
- [Smart Charging Deep-Dive](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md)
- [Tariff And Cost Deep-Dive](../OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md)
- [Data Types Reference](../OCPP-2.1-DataTypes.md)
- [Enumerations Reference](../OCPP-2.1-Enumerations/)
- [Device Model Reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md)

---

## A. Security

### A01 — Update Charging Station Password for HTTP Basic Authentication

> **Deprecated in OCPP 2.1.** Use B09 (Setting a new NetworkConnectionProfile) instead to manage the `BasicAuthPassword`. This use case remains for backwards compatibility with OCPP 1.6 deployments using Security Profile 1 or 2.

The CSMS remotely rotates the HTTP Basic Authentication password stored in the `BasicAuthPassword` configuration variable on the Charging Station. The CSMS sends a `SetVariablesRequest` targeting `SecurityCtrlr.BasicAuthPassword`; on an `Accepted` response the Charging Station disconnects and reconnects using the new credential. If the Charging Station responds with any status other than `Accepted`, the old credentials remain active and the CSMS must continue accepting them.

> **ESCALATE: POLICY-DEPENDENT** — The CSO must decide the password rotation policy: frequency, entropy requirements, and whether to accept the old credential for a grace period after a rotation failure.

**Messages:** [SetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) (CSMS → CS)

### A02 — Update Charging Station Certificate by request of CSMS

The CSMS initiates a certificate renewal by sending a `TriggerMessageRequest` with `requestedMessage = SignChargingStationCertificate` (or `SignV2GCertificate` / `SignV2G20Certificate` for ISO 15118 certificates). The Charging Station responds by generating a new key pair, creating a Certificate Signing Request (CSR), and sending it to the CSMS via `SignCertificateRequest`. The CSMS (or a connected Certificate Authority) signs the certificate and delivers it back with `CertificateSignedRequest`. If the Charging Station has per-EVSE ISO15118Ctrlr components, the CSMS must trigger and process one CSR per EVSE.

> **ESCALATE: POLICY-DEPENDENT** — The CSO must decide which Certificate Authority signs the certificate, the certificate validity period, and whether to require an immediate reconnect after installation to validate the new credential.

**Messages:** [TriggerMessage](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#triggermessage) (CSMS → CS), [SignCertificate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#signcertificate) (CS → CSMS), [CertificateSigned](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#certificatesigned) (CSMS → CS)

### A03 — Update Charging Station Certificate initiated by the Charging Station

The Charging Station autonomously detects that its certificate is approaching expiry and self-initiates the renewal flow without waiting for a CSMS trigger. It generates a new key pair, constructs a CSR, and sends `SignCertificateRequest` to the CSMS. The CSMS (or its CA) signs and returns the certificate via `CertificateSignedRequest`. This use case differs from A02 only in who starts the flow: the Charging Station acts proactively rather than reactively.

> **ESCALATE: POLICY-DEPENDENT** — The CSO must decide the threshold (days before expiry) at which the Charging Station should self-trigger renewal, and whether an expired-certificate connection should be accepted in Pending state to allow certificate refresh.

**Messages:** [SignCertificate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#signcertificate) (CS → CSMS), [CertificateSigned](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#certificatesigned) (CSMS → CS)

### A04 — Security Event Notification

When the Charging Station detects a security-relevant condition — such as an invalid TLS certificate, a tamper attempt, an invalid firmware signature, or a connection attempt using an unknown security profile — it sends a `SecurityEventNotificationRequest` to the CSMS. The notification carries the event type (a well-known string from the security events list) and an optional `techInfo` field for additional diagnostic detail. The CSMS acknowledges with an empty response. Critical events (such as `InvalidTLSVersion`) that occur before a connection is established must be queued locally and sent once connectivity is restored.

**Messages:** [SecurityEventNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Security.md#securityeventnotification) (CS → CSMS)

### A05 — Upgrade Charging Station Security Profile

The CSMS upgrades a Charging Station from a lower security profile to a higher one (e.g. Profile 1 to Profile 2, or Profile 2 to Profile 3) without interrupting normal operation. The process involves writing the new network credentials or certificates via `SetVariablesRequest`, then triggering a `ResetRequest` so the Charging Station reconnects using the new security profile. On reconnect, the Charging Station sends `BootNotificationRequest` and the CSMS verifies the new profile is active. Downgrade to a lower profile is rejected unless `AllowSecurityProfileDowngrade` is explicitly set to `true`.

> **ESCALATE: POLICY-DEPENDENT** — The CSO must decide whether to allow security profile downgrade (`AllowSecurityProfileDowngrade`), the reset type (Immediate vs. OnIdle), and whether to place the Charging Station in Pending state during the transition.

**Messages:** [SetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) (CSMS → CS), [Reset](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#reset) (CSMS → CS), [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS)

---

## B. Provisioning

### B01 — Cold Boot Charging Station

When a Charging Station powers on and has no reason to believe the CSMS is withholding acceptance, it sends `BootNotificationRequest` and expects an `Accepted` response containing the current time and the heartbeat interval. The Charging Station then sends a `Heartbeat` on the configured interval to keep the connection alive and synchronize its clock. If the offline period before reconnect exceeded the `OfflineThreshold` configuration variable, the Charging Station also sends `NotifyEventRequest` with `variable.name = AvailabilityState` for every connector; otherwise it only sends `NotifyEvent` for connectors whose state changed while offline.

**Messages:** [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS), [Heartbeat](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

### B02 — Cold Boot Charging Station - Pending

The CSMS responds to `BootNotificationRequest` with status `Pending` when it needs to perform provisioning steps — such as pushing configuration variables or a new certificate — before the Charging Station is allowed to serve drivers. The Charging Station must continue sending `BootNotificationRequest` at the retry interval provided in the response. While in `Pending` state the CSMS may exchange `GetVariables`, `SetVariables`, and other provisioning messages. Once the CSMS completes provisioning it replies to a subsequent `BootNotificationRequest` with `Accepted`.

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide which provisioning steps (configuration push, certificate update, firmware check) are mandatory before moving from Pending to Accepted.

**Messages:** [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS), [GetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getvariables) (CSMS → CS), [SetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) (CSMS → CS)

### B03 — Cold Boot Charging Station - Rejected

The CSMS responds to `BootNotificationRequest` with status `Rejected` when it does not recognize the Charging Station or its credentials are invalid. The response includes a retry interval; the Charging Station must wait at least that interval before attempting another `BootNotificationRequest`. The Charging Station is not authorized to perform any charging operations while in the rejected state.

> **ESCALATE: POLICY-DEPENDENT** — The operator must define the conditions under which a boot is rejected (unknown serial number, invalid certificate, provisioning not yet complete) and whether an alert should be raised for persistent rejection.

**Messages:** [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS)

### B04 — Offline Behavior Idle Charging Station

When CSMS connectivity is lost, the Charging Station continues to operate stand-alone. On reconnection, if the offline period exceeded the `OfflineThreshold` configuration variable, the Charging Station sends `NotifyEventRequest` with `variable.name = AvailabilityState` for every connector to allow the CSMS to reconstruct the full state. If the offline period was shorter than the threshold, only connectors whose `AvailabilityState` changed during the offline period are reported. The Charging Station then resumes sending `Heartbeat` messages as normal.

**Messages:** [Heartbeat](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

### B05 — Set Variables

The CSMS writes one or more Device Model variable values to the Charging Station in a single `SetVariablesRequest`. Each element specifies a `component`, `variable`, optional `attributeType` (defaulting to `Actual`), and the new value. The Charging Station evaluates each element independently and returns a `SetVariablesResponse` with one `SetVariableResult` per element, using status codes `Accepted`, `Rejected`, `UnknownComponent`, `UnknownVariable`, or `NotSupportedAttributeType`. The CSMS must not exceed the `ItemsPerMessageSetVariables` limit per request.

**Messages:** [SetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) (CSMS → CS)

### B06 — Get Variables

The CSMS retrieves the current value of one or more Device Model variables from the Charging Station. The `GetVariablesRequest` carries a list of `GetVariableData` elements, each identifying a component, variable, and optional `attributeType`. The Charging Station returns a `GetVariablesResponse` with one `GetVariableResult` per requested element. Variables with status `WriteOnly` are returned with status `Rejected` and no value. The CSMS must not request more elements in a single call than the `ItemsPerMessageGetVariables` limit allows.

**Messages:** [GetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getvariables) (CSMS → CS)

### B07 — Get Base Report

The CSMS requests a predefined report from the Charging Station by sending `GetBaseReportRequest` with a `reportBase` type: `ConfigurationInventory` (all operator-settable variables and their characteristics), `FullInventory` (all component-variables including characteristics), or `SummaryInventory` (availability and problem state of the station, EVSEs, and connectors). The Charging Station acknowledges immediately with `GetBaseReportResponse` and then asynchronously streams the results in one or more `NotifyReportRequest` messages, each acknowledged by the CSMS with `NotifyReportResponse`. The `tbc` (to be continued) flag is `true` in all but the last part.

**Messages:** [GetBaseReport](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getbasereport) (CSMS → CS), [NotifyReport](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#notifyreport) (CS → CSMS)

### B08 — Get Custom Report

The CSMS requests a filtered report by sending `GetReportRequest` with optional `componentCriteria` (a list of criteria from: `Active`, `Available`, `Enabled`, `Problem`) and/or a list of specific `componentVariables`. The Charging Station returns only components matching at least one criterion (logical OR). The results are streamed asynchronously as `NotifyReportRequest` messages. If the filter combination yields an empty result set, the Charging Station responds with `status = EmptyResultSet`. Multiple criteria are OR-combined, not AND-combined.

**Messages:** [GetReport](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#getreport) (CSMS → CS), [NotifyReport](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#notifyreport) (CS → CSMS)

### B09 — Setting a new NetworkConnectionProfile

> **Updated in OCPP 2.1.** The `SetNetworkProfileRequest` method is deprecated and may be removed in a future release. The preferred OCPP 2.1 method is to write `NetworkConfiguration` component variables directly via `SetVariablesRequest`.

The CSMS updates the network connection parameters for a specific configuration slot on the Charging Station. The slot number must appear in the `valuesList` of the `NetworkConfigurationPriority` variable. In the legacy flow, the CSMS sends `SetNetworkProfileRequest` and the Charging Station stores the new profile and replies `Accepted`. In the new Device Model flow, the CSMS first removes the target slot from `NetworkConfigurationPriority` via `SetVariablesRequest`, then writes individual `NetworkConfiguration` component variables (instance = slot number), ensuring the station cannot attempt to connect using an incomplete configuration.

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide: which configuration slot to write, whether to use the deprecated `SetNetworkProfile` or the new `SetVariables` path, and whether to immediately trigger a reconnect after updating the active profile.

**Messages:** [SetNetworkProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setnetworkprofile) (CSMS → CS, deprecated), [SetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) (CSMS → CS, preferred)

### B10 — Migrate to new CSMS

The CSMS pushes a new network connection profile (using B09) pointing to the new CSMS endpoint, then resets the Charging Station so it reconnects to the new CSMS. The Charging Station reconnects using the newly configured profile, sends `BootNotificationRequest` to the new CSMS, and completes the transition. If the new CSMS rejects the connection, the Charging Station falls back to the next slot in `NetworkConfigurationPriority`, which should still point to the original CSMS. Errors during the B09 step are non-destructive to the current active connection because the slot being written must not be in the active priority list.

> **ESCALATE: POLICY-DEPENDENT** — The operator must coordinate the cutover timing between old and new CSMS, decide the fallback slot configuration, and confirm the new CSMS is ready to accept the station's `BootNotification` before triggering the reset.

**Messages:** [SetNetworkProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setnetworkprofile) (CSMS → CS) or [SetVariables](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#setvariables) (CSMS → CS), [Reset](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#reset) (CSMS → CS), [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → new CSMS)

### B11 — Reset - Without Ongoing Transaction

The CSMS instructs the Charging Station to restart when no transaction is in progress. The `ResetRequest` carries a `type` of `Immediate` (restart as soon as possible) or `OnIdle` (wait until all connectors are idle). The Charging Station acknowledges with `ResetResponse` (status `Accepted` or `Rejected`), performs the restart, and sends `BootNotificationRequest` on reconnection. An `Immediate` reset must be acted upon without waiting for a user to unplug.

> **ESCALATE: POLICY-DEPENDENT** — The operator must choose the reset type (`Immediate` vs. `OnIdle`) and whether to apply the reset to a specific EVSE or the entire Charging Station.

**Messages:** [Reset](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#reset) (CSMS → CS), [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS)

### B12 — Reset - With Ongoing Transaction

The CSMS issues a `ResetRequest` while one or more transactions are active. For an `Immediate` reset, the Charging Station stops active transactions, sends the final transaction-related messages, then restarts. For an `OnIdle` reset, the Charging Station marks itself as unavailable for new transactions and waits until all current transactions end before restarting. The Charging Station must not start new transactions once an `OnIdle` reset has been accepted. After restart it sends `BootNotificationRequest`.

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide whether to accept the risk of abruptly ending transactions (Immediate) or delay the reset until idle (OnIdle), and how to handle EV drivers who are mid-session.

**Messages:** [Reset](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#reset) (CSMS → CS), [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS)

### B13 — Reset - With Ongoing Transaction - Resuming Transaction

A variant of B12 in which the Charging Station is configured to resume interrupted transactions after reboot (the `ResumeTransaction` capability is supported). When the reset occurs mid-transaction, the Charging Station stores enough state to reconstruct the session. After restarting and sending `BootNotificationRequest`, if the EV is still connected, the Charging Station resumes the transaction without requiring a new authorization. The CSMS receives the continuation as part of the same transaction ID.

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide whether transaction resumption is enabled, what the maximum allowed interruption duration is before the transaction is treated as ended, and whether the driver needs to re-authorize after a reboot.

**Messages:** [Reset](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#reset) (CSMS → CS), [BootNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#bootnotification) (CS → CSMS)

---

## C. Authorization

### C01 — EV Driver Authorization using RFID
_(summary pending)_

### C02 — Authorization using a start button
_(summary pending)_

### C03 — Authorization using credit/debit card
_(summary pending)_

### C04 — Authorization using PIN-code
_(summary pending)_

### C05 — Authorization for CSMS initiated transactions
_(summary pending)_

### C06 — Authorization using local id type
_(summary pending)_

### C07 — Authorization using Contract Certificates
_(summary pending)_

### C08 — Authorization at EVSE using ISO 15118 External Identification Means (EIM)
_(summary pending)_

### C09 — Authorization by GroupId
_(summary pending)_

### C10 — Store Authorization Data in the Authorization Cache
_(summary pending)_

### C11 — Clear Authorization Data in Authorization Cache
_(summary pending)_

### C12 — Start Transaction - Cached Id
_(summary pending)_

### C13 — Offline Authorization through Local Authorization List
_(summary pending)_

### C14 — Online Authorization through Local Authorization List
_(summary pending)_

### C15 — Offline Authorization of unknown Id
_(summary pending)_

### C16 — Stop Transaction with a Master Pass
_(summary pending)_

### C17 — Authorization with prepaid card
_(summary pending)_

### C18 — Authorization using locally connected payment terminal
_(summary pending)_

### C19 — Cancellation prior to transaction
_(summary pending)_

### C20 — Cancellation after start of transaction
_(summary pending)_

### C21 — Settlement at end of transaction
_(summary pending)_

### C22 — Settlement is rejected or fails
_(summary pending)_

### C23 — Increasing authorization amount
_(summary pending)_

### C24 — Ad hoc payment via stand-alone payment terminal
_(summary pending)_

### C25 — Ad hoc payment via a QR code
_(summary pending)_

---

## D. Local Authorization List Management

### D01 — Send Local Authorization List
_(summary pending)_

### D02 — Get Local List Version
_(summary pending)_

---

## E. Transactions

### E01 — Start Transaction options
_(summary pending)_

### E02 — Start Transaction - Cable Plugin First
_(summary pending)_

### E03 — Start Transaction - IdToken First
_(summary pending)_

### E04 — Transaction started while Charging Station is offline
_(summary pending)_

### E05 — Start Transaction - Id not Accepted
_(summary pending)_

### E06 — Stop Transaction options
_(summary pending)_

### E07 — Transaction locally stopped by IdToken
_(summary pending)_

### E08 — Transaction stopped while Charging Station is offline
_(summary pending)_

### E09 — When cable disconnected on EV-side: Stop Transaction
_(summary pending)_

### E10 — When cable disconnected on EV-side: Suspend Transaction
_(summary pending)_

### E11 — Connection Loss During Transaction
_(summary pending)_

### E12 — Inform CSMS of an Offline Occurred Transaction
_(summary pending)_

### E13 — Transaction-related message not accepted by CSMS
_(summary pending)_

### E14 — Check transaction status
_(summary pending)_

### E15 — End of charging process
_(summary pending)_

### E16 — Transactions with fixed cost, energy, SoC or time
_(summary pending)_

### E17 — Resuming transaction after forced reboot
_(summary pending)_

---

## F. Remote Control

### F01 — Remote Start Transaction - Cable Plugin First
_(summary pending)_

### F02 — Remote Start Transaction - Remote Start First
_(summary pending)_

### F03 — Remote Stop Transaction
_(summary pending)_

### F04 — Remote Stop ISO 15118 Charging from CSMS
_(summary pending)_

### F05 — Remotely Unlock Connector
_(summary pending)_

### F06 — Trigger Message
_(summary pending)_

### F07 — Remote start with fixed cost, energy, SoC or time
_(summary pending)_

---

## G. Availability

### G01 — Report connector AvailabilityState
_(summary pending)_

### G02 — Heartbeat
_(summary pending)_

### G03 — Change Availability EVSE/Connector
_(summary pending)_

### G04 — Change Availability Charging Station
_(summary pending)_

### G05 — Lock Failure
_(summary pending)_

---

## H. Reservation

### H01 — Reservation
_(summary pending)_

### H02 — Cancel Reservation
_(summary pending)_

### H03 — Use a reserved EVSE
_(summary pending)_

### H04 — Reservation Ended, not used
_(summary pending)_

---

## I. Tariff And Cost

### I01 — Show EV Driver-specific Tariff Information
_(summary pending)_

### I02 — Show EV Driver Running Total Cost During Charging
_(summary pending)_

### I03 — Show EV Driver Final Total Cost After Charging
_(summary pending)_

### I04 — Show Fallback Tariff Information
_(summary pending)_

### I05 — Show Fallback Total Cost Message
_(summary pending)_

### I06 — Update Tariff Information During Transaction
_(summary pending)_

### I07 — Local Cost Calculation - Set Default Tariff
_(summary pending)_

### I08 — Local Cost Calculation - Receive Driver Tariff
_(summary pending)_

### I09 — Local Cost Calculation - Get Tariffs
_(summary pending)_

### I10 — Local Cost Calculation - Clear Tariffs
_(summary pending)_

### I11 — Local Cost Calculation - Change transaction tariff
_(summary pending)_

### I12 — Local Cost Calculation - Cost Details of Transaction
_(summary pending)_

---

## J. Meter Values

### J01 — Sending Meter Values not related to a transaction
_(summary pending)_

### J02 — Sending transaction related Meter Values
_(summary pending)_

### J03 — Charging Loop with metering information exchange
_(summary pending)_

---

## K. Smart Charging

### K01 — SetChargingProfile
_(summary pending)_

### K02 — Central Smart Charging
_(summary pending)_

### K03 — Local Smart Charging
_(summary pending)_

### K04 — Internal Load Balancing
_(summary pending)_

### K05 — Remote Start Transaction with Charging Profile
_(summary pending)_

### K06 — Offline Behavior Smart Charging During Transaction
_(summary pending)_

### K07 — Offline Behavior Smart Charging at Start of Transaction
_(summary pending)_

### K08 — Get Composite Schedule
_(summary pending)_

### K09 — Get Charging Profiles
_(summary pending)_

### K10 — Clear Charging Profile
_(summary pending)_

### K11 — Set / Update External Charging Limit With Ongoing Transaction
_(summary pending)_

### K12 — Set / Update External Charging Limit Without Ongoing Transaction
_(summary pending)_

### K13 — Reset / Release External Charging Limit
_(summary pending)_

### K14 — External Charging Limit with Local Controller
_(summary pending)_

### K15 — ISO 15118-2 Charging with load leveling
_(summary pending)_

### K16 — Renegotiation initiated by CSMS
_(summary pending)_

### K17 — Renegotiation initiated by EV
_(summary pending)_

### K18 — ISO 15118-20 Scheduled Control Mode
_(summary pending)_

### K19 — ISO 15118-20 Dynamic Control Mode
_(summary pending)_

### K20 — ISO 15118-20 Adjusting charging schedule when energy needs change
_(summary pending)_

### K21 — Requesting priority charging remotely
_(summary pending)_

### K22 — Requesting priority charging locally
_(summary pending)_

### K23 — Smart Charging with EMS connected to Charging Stations
_(summary pending)_

### K24 — Smart Charging with EMS connected to Local Controller
_(summary pending)_

### K25 — Smart Charging with EMS acting as a Local Controller
_(summary pending)_

### K26 — Smart Charging with Hybrid Local & Cloud EMS
_(summary pending)_

### K27 — Smart Charging with EMS and LocalGeneration
_(summary pending)_

### K28 — Dynamic charging profiles from CSMS
_(summary pending)_

### K29 — Dynamic charging profiles from external system
_(summary pending)_

---

## L. Firmware Management

### L01 — Secure Firmware Update
_(summary pending)_

### L02 — Non-Secure Firmware Update
_(summary pending)_

### L03 — Publish Firmware file on Local Controller
_(summary pending)_

### L04 — Unpublish Firmware file on Local Controller
_(summary pending)_

---

## M. Certificate Management

### M01 — Certificate installation EV
_(summary pending)_

### M02 — Certificate Update EV
_(summary pending)_

### M03 — Retrieve list of available certificates from a Charging Station
_(summary pending)_

### M04 — Delete a specific certificate from a Charging Station
_(summary pending)_

### M05 — Install CA certificate in a Charging Station
_(summary pending)_

### M06 — Get V2G Charging Station Certificate status
_(summary pending)_

### M07 — Get Vehicle Certificate Chain Revocation Status
_(summary pending)_

---

## N. Diagnostics

### N01 — Retrieve Log Information
_(summary pending)_

### N02 — Get Monitoring report
_(summary pending)_

### N03 — Set Monitoring Base
_(summary pending)_

### N04 — Set Variable Monitoring
_(summary pending)_

### N05 — Set Monitoring Level
_(summary pending)_

### N06 — Clear / Remove Monitoring
_(summary pending)_

### N07 — Alert Event
_(summary pending)_

### N08 — Periodic Event
_(summary pending)_

### N09 — Get Customer Information
_(summary pending)_

### N10 — Clear Customer Information
_(summary pending)_

### N11 — Set Frequent Periodic Variable Monitoring
_(summary pending)_

### N12 — Get Periodic Event Streams
_(summary pending)_

### N13 — Close Periodic Event Streams
_(summary pending)_

### N14 — Adjust Periodic Event Streams
_(summary pending)_

### N15 — Periodic Event Streams
_(summary pending)_

---

## O. Display Message

### O01 — Set DisplayMessage
_(summary pending)_

### O02 — Set DisplayMessage for Transaction
_(summary pending)_

### O03 — Get All DisplayMessages
_(summary pending)_

### O04 — Get Specific DisplayMessages
_(summary pending)_

### O05 — Clear a DisplayMessage
_(summary pending)_

### O06 — Replace DisplayMessage
_(summary pending)_

---

## P. Data Transfer

### P01 — Data Transfer to the Charging Station
_(summary pending)_

### P02 — Data Transfer to the CSMS
_(summary pending)_

---

## Q. Bidirectional Power Transfer (V2X)

### Q01 — V2X Authorization
_(summary pending)_

### Q02 — Starting in operationMode ChargingOnly before enabling V2X
_(summary pending)_

### Q03 — Central V2X control with charging schedule
_(summary pending)_

### Q04 — Central V2X control with dynamic CSMS setpoint
_(summary pending)_

### Q05 — External V2X setpoint control with a charging profile from CSMS
_(summary pending)_

### Q06 — External V2X control with a charging profile from an External System
_(summary pending)_

### Q07 — Central V2X control for frequency support
_(summary pending)_

### Q08 — Local V2X control for frequency support
_(summary pending)_

### Q09 — Local V2X control for load balancing
_(summary pending)_

### Q10 — Idle, minimizing energy consumption
_(summary pending)_

### Q11 — Going offline during V2X operation
_(summary pending)_

### Q12 — Resuming a V2X operation after an offline period
_(summary pending)_

---

## R. DER Control

### R01 — Starting a V2X session with DER control in EVSE
_(summary pending)_

### R02 — Starting a V2X session with DER control in EV
_(summary pending)_

### R03 — Starting a V2X session with hybrid DER control in both EV and EVSE
_(summary pending)_

### R04 — Configure DER control settings at Charging Station
_(summary pending)_

### R05 — Charging station reporting a DER event
_(summary pending)_

---

## S. Battery Swapping

### S01 — Battery Swap Local Authorization
_(summary pending)_

### S02 — Battery Swap Remote Start
_(summary pending)_

### S03 — Battery Swap In/Out
_(summary pending)_

### S04 — Battery Swap Charging
_(summary pending)_
