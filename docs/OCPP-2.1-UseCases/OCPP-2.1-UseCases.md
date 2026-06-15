# OCPP 2.1 — Use-Case Catalog (Part 2)

> **Purpose:** A catalog of every OCPP 2.1 Part 2 use case across functional blocks A–S. For each use case it records its ID, purpose, the messages involved, and any escalation flags — a single index an AI agent can scan to find the right use case and jump to the relevant schema and deep-dive references.

> **Last updated:** 2026-06-11

---

## How This Document Was Produced

This document catalogs the use cases of the OCPP 2.1 Edition 2 Part 2 specification (functional blocks A–S). Each entry is an **original summary** — a short restatement of what the use case does in original wording, **not verbatim spec prose** (the OCA specification is CC BY-ND licensed). Its dominant confidence tier is **spec-knowledge** for the behavioral description of each use case; the **message names** referenced in each entry are **schema-derived**, cross-referenced against the per-block schema references listed below, all mechanically extracted from the official OCA artifacts.

This catalog contains **102 escalation points** marked with `> **ESCALATE:**` — each flags a decision the spec leaves to the operator, vendor, or grid/market context. When an AI agent encounters one, it MUST stop and ask the developer (or relevant stakeholder) to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

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
- [Enumerations Reference](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md)
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

The baseline authorization flow: a driver presents an RFID card and the Charging Station forwards the token to the CSMS for validation before offering energy. The CSMS replies with an authorization status (and, optionally, the set of EVSEs the token is valid for and an associated group token), so the station only allows charging when the token is accepted and applicable to that EVSE. The same token that started a session can always end it locally without re-contacting the CSMS, and driver-facing messages should be shown in the configured language(s).

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS)

### C02 — Authorization using a start button

For simple stations without an RFID reader, charging can be triggered by a physical start button (or mechanical key, or simply by plugging in). No `Authorize` message is sent; instead the Charging Station opens a transaction and reports it with a `TransactionEventRequest` carrying an `idToken` of type `NoAuthorization`, which the CSMS cannot reject and must accept. Tokens of this type are never stored in the Authorization Cache.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide whether button-started (unauthenticated) charging is acceptable at a given site and how the resulting energy is accounted for or billed, since no driver identity is captured.

### C03 — Authorization using credit/debit card

This use case has been retired as a stand-alone authorization case in OCPP 2.1. Its objective — starting a transaction by paying with a credit or debit card — is now covered by the dedicated ad-hoc payment use cases, principally [C24](#c24--ad-hoc-payment-via-stand-alone-payment-terminal) (stand-alone terminal) and the locally connected terminal flows ([C18](#c18--authorization-using-locally-connected-payment-terminal) and following). Refer to those entries for the current behavior.

**Messages:** No dedicated message.

### C04 — Authorization using PIN-code

A station with a keypad lets the driver type a PIN (or similar key entry such as a licence-plate number) instead of presenting a card. The entered code is sent to the CSMS in an `Authorize` request with the token type set to `KeyCode`, and the CSMS responds accepting or rejecting it. PIN codes must never appear in logs, and stations are encouraged to apply brute-force protection such as increasing back-off after failed attempts.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator/vendor must define PIN length and brute-force countermeasures (lockout/back-off thresholds), which the spec only recommends rather than prescribes.

### C05 — Authorization for CSMS initiated transactions

When a transaction is started remotely (for example from a mobile app) for a driver who has no RFID, the CSMS supplies the identifier itself. It sends a `RequestStartTransaction` with a server-generated token (type `Central`) — which may be a single-use virtual code or a contract identifier such as an eMAID. Because the CSMS already knows this token, the Charging Station does not send an `Authorize` request and does not cache it; it accepts the remote start and reports the started session via `TransactionEvent`, echoing the token and the remote start id.

**Messages:** [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction) (CSMS → CS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

### C06 — Authorization using local id type

This case demonstrates the `Local` token type, used when a station generates or accepts an identifier produced by a locally integrated system rather than the CSMS — the canonical example being a parking-garage ticket that doubles as the charging credential. The Charging Station forwards the locally typed token to the CSMS in an `Authorize` request for validation, and a separate payment kiosk later triggers the stop via the CSMS. The interface between the local payment/parking system and the CSMS is outside OCPP scope.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: VENDOR-INTEGRATION** — The protocol and semantics between the local identifier source (e.g. parking kiosk/barrier) and the CSMS are not defined by OCPP and must be agreed between the site integrator and the CSMS operator.

### C07 — Authorization using Contract Certificates

ISO 15118 Plug & Charge authorization: the EV presents a contract certificate and eMAID, and the Charging Station passes the eMAID together with the certificate hash data (and, when it cannot validate the chain itself, the full PEM chain) to the CSMS in an `Authorize` request. The CSMS verifies the certificate chain via real-time or cached OCSP and returns both an authorization status for the eMAID and a certificate status, so the response distinguishes "certificate revoked/expired" from "identity not allowed." When offline, the station falls back to local validation (Local Authorization List, Authorization Cache, or unknown-id handling) depending on its configuration.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must set offline contract-validation behavior (`ContractValidationOffline`, `CentralContractValidationAllowed`, `LocalAuthorizeOffline`, `OfflineTxForUnknownIdEnabled`) and the OCSP strategy (real-time vs. cached), which together determine whether Plug & Charge works while disconnected.

### C08 — Authorization at EVSE using ISO 15118 External Identification Means (EIM)

In an ISO 15118 session where the driver authorizes by external means (EIM) rather than a contract certificate — for instance an RFID card, app, or PIN applied at the EVSE — the Charging Station sends the resulting identifier to the CSMS in an `Authorize` request and the CSMS responds. The mechanics are identical to the other C-block identification means; the only distinguishing factor is that 15118 communication is present. Identification may happen before plugging in or shortly after (with a bounded time-out for the latter).

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS)

### C09 — Authorization by GroupId

GroupId lets two drivers with different tokens act on the same session — for example a couple sharing one car, each with their own RFID card. When the CSMS authorizes a token it returns the associated `groupIdToken`, which the Charging Station stores alongside the token's authorization info. A second token that resolves to the same group is then allowed to stop (or otherwise act on) a transaction the first token started. The mechanism also works against the Authorization Cache, since the group id is cached too.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

### C10 — Store Authorization Data in the Authorization Cache

The Charging Station autonomously caches the `IdTokenInfo` of every identifier the CSMS has responded to — whether the data arrived in an `Authorize` response, a `TransactionEvent` response, or a `ReserveNow` request — so that subsequent presentations can be resolved faster or while offline. Cache entries should survive reboots (non-volatile storage), expire according to `AuthCacheLifeTime` or the token's `cacheExpiryDateTime`, and the cache is enabled/disabled by `AuthCacheEnabled`. Personal data should be stored securely, e.g. by hashing tokens, and the `additionalInfo` field is not cached.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must set cache lifetime (`AuthCacheLifeTime`) and decide on secure storage of personal data (e.g. hashing tokens), balancing offline availability against privacy/data-retention requirements.

### C11 — Clear Authorization Data in Authorization Cache

The CSMS can purge a station's Authorization Cache by sending a `ClearCache` request; the station attempts to clear all cached identifiers and reports the outcome. It returns `Accepted` on success and `Rejected` if it could not clear the cache or if the cache is disabled (`AuthCacheEnabled` is false).

**Messages:** [ClearCache](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#clearcache) (CSMS → CS)

### C12 — Start Transaction - Cached Id

While online, a station with `LocalPreAuthorize` and `AuthCacheEnabled` set can start a transaction immediately for a token it finds cached as `Accepted`, skipping the `Authorize` round-trip for faster response. It opens the session and reports it via `TransactionEvent`; because that response also carries current `IdTokenInfo`, the station learns if the token has since become invalid and may, per `MaxEnergyOnInvalidId`/`StopTxOnInvalidId`, stop the energy offer or the transaction. Tokens belonging to the `MasterPassGroupId` are never allowed to start a transaction.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must configure how a now-invalid cached token is handled mid-session (`MaxEnergyOnInvalidId`, `StopTxOnInvalidId`), trading faster local start against the risk of delivering energy to a token the CSMS would reject.

### C13 — Offline Authorization through Local Authorization List

When the station cannot reach the CSMS, it can still authorize a presented token by consulting the Local Authorization List — a CSMS-synchronized list of identifiers and their authorization status. If the token is present with status `Accepted`, charging is allowed offline. Where both a Local Authorization List and an Authorization Cache exist, list entries take priority over cache entries for the same identifier. Expiry handling depends on whether the list supports `cacheExpiryDateTime` and on `OfflineTxForUnknownIdEnabled`.

**Messages:** [SendLocalList](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#sendlocallist) (CSMS → CS), [GetLocalListVersion](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#getlocallistversion) (CSMS → CS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide which identifiers populate the Local Authorization List and the offline policy (`LocalAuthListEnabled`, `OfflineTxForUnknownIdEnabled`), which governs who can charge when connectivity is lost.

### C14 — Online Authorization through Local Authorization List

Even while online, a station with `LocalPreAuthorize` enabled can authorize a token directly from the Local Authorization List without sending an `Authorize` request, provided the token is present with status `Accepted` (and any `cacheExpiryDateTime` has not passed). If the token is unknown or not `Accepted`, the station falls back to sending an `Authorize` request to the CSMS. As in the offline case, list entries take priority over cache entries for the same identifier.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [SendLocalList](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#sendlocallist) (CSMS → CS), [GetLocalListVersion](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#getlocallistversion) (CSMS → CS)

### C15 — Offline Authorization of unknown Id

This covers presenting a token the offline station has never seen — absent from both the Local Authorization List and the Authorization Cache. If `OfflineTxForUnknownIdEnabled` is `true` the station accepts the unknown token and starts charging; if `false` it rejects it. When connectivity returns, the station reports any such offline-authorized transaction to the CSMS, which may then confirm or reject it; on rejection the station's later behavior (continue, cap energy via `MaxEnergyOnInvalidId`, or stop and deauthorize) depends on `StopTxOnInvalidId` and the configured `TxStopPoint`. It applies to all identifier types, including eMAIDs from ISO 15118 contract certificates.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide, via `OfflineTxForUnknownIdEnabled` (and `StopTxOnInvalidId`/`MaxEnergyOnInvalidId`), whether to grant energy to wholly unknown tokens during outages, accepting the revenue/fraud risk if the CSMS later rejects them.

### C16 — Stop Transaction with a Master Pass

A Master Pass lets an authorized holder — typically law-enforcement or emergency personnel — stop ongoing transactions and release the cable. The holder presents a token whose group equals the configured `MasterPassGroupId`; the station validates it with the CSMS via `Authorize`, and the response's group id confirms Master Pass status. If the station has a UI, the holder selects which transactions to stop; otherwise all ongoing transactions are stopped. Each stopped session is reported with a `TransactionEvent` (`Ended`, stop reason `MasterPass`). Master Pass tokens may never start a transaction.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must define and provision the `MasterPassGroupId` and decide who is issued Master Pass tokens, since these grant the power to terminate any driver's session.

### C17 — Authorization with prepaid card

A variant of RFID authorization (C01) for accounts carrying a prepaid balance. The station always sends an `Authorize` request (prepaid tokens must not be cached, so the CSMS can check the live balance) and the CSMS returns `Accepted` with a positive balance, `NoCredit` when the balance is zero/negative, or `Invalid`; in all cases `cacheExpiryDateTime` is set to now so the token does not persist in the cache. When the transaction starts, the CSMS returns a `transactionLimit.maxCost` equal to the remaining credit in the `TransactionEvent` response, and the station enforces that ceiling so no more energy is delivered than the balance covers.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The CSMS operator must support prepaid accounts and define how the remaining balance maps to `transactionLimit.maxCost`, including any reserve/margin applied to avoid overdraw.

### C18 — Authorization using locally connected payment terminal

A driver pays with a bank card at a payment terminal built into the Charging Station. The terminal asks the Payment Service Provider (PSP) to authorize a hold for the amount in `PaymentCtrlr.AuthorizationAmount`, and the PSP returns an approval plus a unique reference (the `PspRef`). The station uses that `PspRef` as an `idToken` of type `DirectPayment`, with card details (card BIN, last four digits, etc.) carried in `additionalInfo`. If `PaymentCtrlr.AuthorizeDirectPayment` is false the station authorizes locally against a default ad-hoc tariff; if true it sends an `Authorize` request so the CSMS can accept (optionally supplying a tariff) or reject. The started transaction is reported via `TransactionEvent` with `transactionLimit.maxCost` set to the authorized hold. A VAT number entered by the driver can optionally be validated with `VatNumberValidation` before settlement.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [VatNumberValidation](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#vatnumbervalidation) (CS → CSMS)

> **ESCALATE: PSP-INTEGRATION** — The protocol between the integrated payment terminal and the PSP, and between the terminal and the Charging Station, is out of OCPP scope and must be defined by the terminal/station vendor and the chosen PSP.

> **ESCALATE: PRICING-POLICY** — The operator must set the pre-authorization hold amount (`PaymentCtrlr.AuthorizationAmount`), the default ad-hoc tariff, and whether CSMS-side authorization (`AuthorizeDirectPayment`) is used to apply non-default tariffs or reject cards.

> **ESCALATE: REGULATORY** — VAT-number handling on receipts (whether collected, validated, and printed) depends on local tax legislation and operator policy.

### C19 — Cancellation prior to transaction

After an ad-hoc payment card has been authorized but before any OCPP transaction starts — the driver cancels, or never plugs in and the EV-connection timeout fires — the held amount must be released. The payment terminal asks the PSP to release the authorization reservation, and the station ends the `DirectPayment` token's authorization. If `PaymentCtrlr.AuthorizeDirectPayment` is true (so the CSMS knew about the token), the station sends a `NotifySettlement` with the `PspRef` and status `Canceled` so the CSMS knows the token will not be charged; if false, the CSMS was never told about the token and receives no notification.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize) (CS → CSMS), [NotifySettlement](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) (CS → CSMS)

> **ESCALATE: PSP-INTEGRATION** — Releasing the authorization hold is performed via the terminal/PSP interface, which is outside OCPP scope.

### C20 — Cancellation after start of transaction

Like C19 but the OCPP transaction has already started, though no energy was delivered and no other cost (e.g. reservation fee) was incurred. The driver cancels (or the EV-connection timeout fires); the station ends the transaction with a `TransactionEvent` (`Ended`, trigger `StopAuthorized` or `EVConnectTimeout`) reporting `totalCost` = 0, instructs the terminal to release the hold via the PSP, and sends a `NotifySettlement` with the transaction id, the `DirectPayment` `PspRef`, and status `Canceled`. When local cost calculation is used, the ending `TransactionEvent` also carries cost details showing zero cost/usage.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifySettlement](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) (CS → CSMS)

> **ESCALATE: PSP-INTEGRATION** — Releasing the authorization hold via the terminal/PSP is outside OCPP scope.

### C21 — Settlement at end of transaction

When an ad-hoc transaction ends, the final cost is settled against the held card amount and a receipt is produced. The station ends the transaction with a `TransactionEvent` carrying cost details, then either: (a) instructs the integrated terminal to settle the actual cost with the PSP and sends a `NotifySettlement` (`Settled`, with settlement amount/time, transaction id and `PspRef`, optionally VAT number/company) — the receipt URL coming back either from the CSMS in the `NotifySettlement` response (`ReceiptByCSMS` true) or from the terminal; or (b) when `SettlementByCSMS` is true, the CSMS settles directly with the PSP, bypassing the terminal and providing the receipt out of band. Showing a receipt is problematic when `TxStopPoint` is `ParkingBayOccupancy`, since the driver may have already left.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifySettlement](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) (CS → CSMS)

> **ESCALATE: SETTLEMENT-CHANNEL** — The operator must choose where settlement happens (terminal-to-PSP vs. CSMS-to-PSP via `PaymentCtrlr.SettlementByCSMS`) and who generates the receipt (`ReceiptByCSMS`), since these determine the money flow and reconciliation path.

> **ESCALATE: REGULATORY** — Receipt content and delivery, including VAT number/company details and how a driver who has already left retrieves a receipt, depend on tax law and operator policy.

### C22 — Settlement is rejected or fails

Settlement of an ad-hoc payment can be declined by the PSP (`Rejected`) or fail for technical reasons such as a communication breakdown (`Failed`). In either case the station notifies the CSMS with a `NotifySettlement` carrying the transaction id, the `DirectPayment` token, settlement amount and time, the appropriate status, and optional error detail in `statusInfo` — but no receipt information. On failure the operator can later attempt to capture the amount by contacting the PSP directly using the `PspRef` (the value of the `idToken`).

**Messages:** [NotifySettlement](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) (CS → CSMS)

> **ESCALATE: SETTLEMENT-CHANNEL** — The operator must define the recovery process for rejected/failed settlements (e.g. manual capture with the PSP via the `PspRef`), which OCPP only reports but does not resolve.

### C23 — Increasing authorization amount

For long or expensive ad-hoc sessions, the initial card hold (`PaymentCtrlr.AuthorizationAmount`) may be insufficient. If incremental authorization is supported — `PaymentCtrlr.IncrementalAuthorizationAmount` is greater than zero — the station monitors accrued cost and, once it approaches the current hold minus `PaymentCtrlr.IncrementalAuthorizationThreshold`, instructs the terminal to extend the hold by the incremental amount and raises the transaction's `transactionLimit.maxCost` accordingly, reporting the change in a `TransactionEvent` (trigger `LimitChanged`/`LimitSet`). If the incremental amount is zero or absent, energy flow halts when `maxCost` is reached.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: PRICING-POLICY** — The operator must set the incremental hold amount and threshold (`PaymentCtrlr.IncrementalAuthorizationAmount`, `IncrementalAuthorizationThreshold`), balancing uninterrupted charging against the size of the card pre-authorization.

> **ESCALATE: PSP-INTEGRATION** — Extending the authorization hold is performed via the terminal/PSP interface, which is outside OCPP scope.

### C24 — Ad hoc payment via stand-alone payment terminal

Here the payment terminal/kiosk is a separate unit serving several Charging Stations, with no direct connection to any individual station. The driver pays at the kiosk, the kiosk gets PSP approval and a `PspRef`, and the kiosk forwards station/EVSE identity and card details to the CSMS. The CSMS then remotely starts the session with a `RequestStartTransaction` using an `idToken` of value `<PspRef>` and type `DirectPayment`, and the flow continues like a remote start with cost limit (F07). At the end, cost is settled — locally or centrally — and settled with the PSP either via the kiosk or directly by the CSMS, with the receipt optionally surfaced to the driver via a display message. The kiosk-to-CSMS interface is out of OCPP scope.

**Messages:** [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction) (CSMS → CS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: PSP-INTEGRATION** — The protocol between the stand-alone kiosk and both the PSP and the CSMS is not specified by OCPP and must be defined by the kiosk/CSMS vendors.

> **ESCALATE: SETTLEMENT-CHANNEL** — The operator must choose whether final cost is calculated locally or centrally and whether settlement with the PSP is done by the kiosk or directly by the CSMS.

### C25 — Ad hoc payment via a QR code

For stations with no payment terminal at all, ad-hoc payment can be offered through a QR code linking to a payment web page. A dynamic QR code embeds a time-based one-time password and the station/EVSE identity in a URL template (`WebPaymentsCtrlr.URLTemplate`); the driver scans it, the CSMS validates the one-time password, optionally sends a `NotifyWebPaymentStarted` so the station can block a local start during the web-payment window, then redirects the driver to the PSP. After approval the PSP returns a `PspRef`, and the CSMS remotely starts the session with a `RequestStartTransaction` using `idToken` `<PspRef>` of type `DirectPayment`, continuing as a remote start with cost limit. A static QR code (a sticker) works similarly but is vulnerable to a fraudulent sticker being pasted over it, so dynamic codes are recommended. Final cost is settled with the PSP by the CSMS, and a receipt URL can be pushed to the station display.

**Messages:** [NotifyWebPaymentStarted](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifywebpaymentstarted) (CSMS → CS), [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction) (CSMS → CS), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: PSP-INTEGRATION** — The payment web page, its URL format, the CSMS-to-PSP communication, and receipt delivery are out of OCPP scope and chosen by the operator (CSO), optionally involving an EMSP.

> **ESCALATE: SECURITY-POLICY** — The operator must decide between static and dynamic QR codes; static stickers are susceptible to spoofing, so dynamic codes with a time-based one-time password are recommended.

---

## D. Local Authorization List Management

### D01 — Send Local Authorization List

The CSMS pushes a Local Authorization List to the station so that idTokens can be authorized locally — both while offline and, with pre-authorization enabled, faster while online. The `SendLocalList` message carries a `versionNumber` plus an `updateType` of either `Full` (replace the entire list) or `Differential` (add, update, or delete individual entries: an `AuthorizationData` element with `idTokenInfo` adds or updates it, one without removes it). The station applies the change, stores the new version number, and replies `Accepted`, `Failed`, or `VersionMismatch`; it rejects a differential update whose version is not strictly greater than the stored one. Each request is size-bounded by `ItemsPerMessageSendLocalList`/`BytesPerMessageSendLocalList`, so a large list is sent as an initial `Full` followed by `Differential` chunks, and the list should be held in non-volatile memory across reboots.

**Messages:** [SendLocalList](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#sendlocallist) (CSMS → CS)

> **ESCALATE: POLICY-DEPENDENT** — The operator decides which idTokens populate the list, how often it is synchronized, and whether differential or full updates are used; OCPP defines the transport but not the membership policy.

### D02 — Get Local List Version

To keep the station and CSMS lists in sync without retransmitting the whole list, the CSMS can query the station's current list version with `GetLocalListVersion`; the station replies with the `versionNumber` it currently holds. A returned value of `0` is reserved to mean "no Local Authorization List" — either because `LocalAuthListEnabled` is false or because the CSMS has never sent an update — whereas a list that was deliberately emptied (a `SendLocalList` carrying an empty list) still reports its assigned version greater than `0`. The CSMS typically compares the reported version against its own and issues a `SendLocalList` only when they differ.

**Messages:** [GetLocalListVersion](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md#getlocallistversion) (CSMS → CS)

---

## E. Transactions

### E01 — Start Transaction options

OCPP 2.1 decouples the "transaction" the CSMS records for billing from the physical charging session, and the `TxStartPoint` configuration variable determines the exact moment the station emits its first `TransactionEvent` (eventType `Started`). Possible start points include `ParkingBayOccupancy` (an occupancy detector sees the EV, trigger `EVDetected`), `EVConnected` (cable plugged in, trigger `CablePluggedIn`), `Authorized` (driver authorized), `DataSigned` (a signed meter reading is taken before energy flows), `PowerPathClosed` (authorized and connected, ready to deliver), and `EnergyTransfer` (energy actually starts flowing). The operator picks the start point to match what is billed — connection time, time of use, or charging time — and not all combinations of start and stop point are sensible.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must set `TxStartPoint` (and the matching `TxStopPoint`) to reflect the billing model; a poor pairing (e.g. start on `ParkingBayOccupancy`, stop on `EVConnected`) can leave a transaction that never closes.

### E02 — Start Transaction - Cable Plugin First

In the most common public-charging flow the driver plugs in before authorizing. With `TxStartPoint` = `EVConnected`, the station first reports the connector as `Occupied` via a `NotifyEvent`, then opens the transaction with a `TransactionEvent` (`Started`, trigger `CablePluggedIn`) even though the driver is not yet known. Once the driver authorizes (locally or via the CSMS), the station sends a `TransactionEvent` (`Updated`, trigger `Authorized`) carrying the idToken, locks the connector if the cable is not captive, starts the energy offer, and reports the move to `Charging` with a further `Updated` event. The station keeps the cache entry updated from the response, and continues to send `Updated` events through the session.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

### E03 — Start Transaction - IdToken First

The mirror of E02: the driver authorizes first, then plugs in. With `TxStartPoint` = `Authorized`, a successful authorization opens the transaction with a `TransactionEvent` (`Started`, trigger `Authorized`) before any cable is connected. When the driver plugs in within the connection timeout, the station reports the connector `Occupied` via `NotifyEvent`, sends an `Updated` event (`EVConnected`/`CablePluggedIn`), locks the connector, starts the energy offer, and reports `Charging`. If the cable is not plugged in within the timeout, the station ends the transaction with a `TransactionEvent` (`Ended`, trigger `EVConnectTimeout`, stop reason `Timeout`). The CSMS must always answer with a `TransactionEvent` response regardless of any sanity-check outcome.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

### E04 — Transaction started while Charging Station is offline

When the station is offline but can authorize a driver locally (Local Authorization List or Authorization Cache), it starts the transaction immediately, locks the connector, and begins the energy offer. The corresponding `TransactionEvent` (`Started`) is stored in a local queue with the `offline` flag set true. Once connectivity is restored — which may be minutes or days later — the station resumes communication (typically a `Heartbeat` first) and replays the queued events to the CSMS, which acknowledges and the messages leave the queue. The transaction is not tied to any particular `TxStartPoint`.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [Heartbeat](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat) (CS → CSMS)

### E05 — Start Transaction - Id not Accepted

Because a station may have authorized a token locally on stale data, the CSMS re-validates the idToken in every `TransactionEvent` that carries one. If the response's `idTokenInfo.status` is not `Accepted` (e.g. `Blocked`, `Invalid`, `Expired`, `Unknown`), the station suspends or stops the energy offer according to policy. With `StopTxOnInvalidId` false it keeps the transaction open but suspends energy (an `Updated` event with `SuspendedEVSE`), optionally allowing a small top-up bounded by `MaxEnergyOnInvalidId`. With `StopTxOnInvalidId` true it deauthorizes — emitting an `Updated` or `Ended` event with trigger `Deauthorized` depending on `TxStopPoint`. The cable typically remains locked even when energy is cut.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must set `StopTxOnInvalidId` and `MaxEnergyOnInvalidId`, deciding whether a token the CSMS rejects mid-start merely suspends energy (allowing a capped amount) or terminates the transaction.

### E06 — Stop Transaction options

The counterpart to E01: `TxStopPoint` determines when the station closes the transaction with a `TransactionEvent` (eventType `Ended`). Stop points mirror the start options — `ParkingBayOccupancy` (the EV leaves the bay, trigger `EVDeparted`), `EVConnected` (cable unplugged / EV communication lost, trigger `EVCommunicationLost`, stop reason `EVDisconnected`), `Authorized` (driver no longer authorized), and `PowerPathClosed`/`EnergyTransfer`. The chosen stop point must form a coherent pair with the start point so every started transaction can eventually end.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must set `TxStopPoint` consistently with `TxStartPoint` and the billing model; an ill-matched pair risks transactions that never stop.

### E07 — Transaction locally stopped by IdToken

A driver ends a session by presenting the same (or a group-validated) idToken a second time. With `TxStopPoint` = `Authorized` or `PowerPathClosed`, the station stops the energy transfer, unlocks the cable if it is not captive, and reports a `TransactionEvent` (`Ended`, trigger `StopAuthorized`, stop reason `Local`). With other stop points the station instead first sends an `Updated` event (trigger `StopAuthorized`) and ends the transaction only when the configured stop condition is later met. The CSMS cannot veto a stop — it can only acknowledge it.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

### E08 — Transaction stopped while Charging Station is offline

The offline analogue of E07. While offline with a transaction ongoing, the driver presents an idToken; if the station can validate it locally — the same token that started the session, or a matching `groupId` found in the Local Authorization List or Authorization Cache — it stops the energy offer, unlocks a non-captive cable, and queues a `TransactionEvent` (`Ended`, `offline` = true). When connectivity returns, the station replays the queued stop event (typically after a `Heartbeat`) and the CSMS acknowledges it.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [Heartbeat](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat) (CS → CSMS)

### E09 — When cable disconnected on EV-side: Stop Transaction

When `StopTxOnEVSideDisconnect` is true and the driver unplugs the cable at the vehicle, the station detects the loss, suspends the energy offer, and ends the transaction with a `TransactionEvent` (`Ended`, trigger `EVCommunicationLost`, stop reason `EVDisconnected`). The station-side connector behaves per `UnlockOnEVSideDisconnect`: if false it stays locked until the driver returns and authorizes; if true it unlocks immediately. Once the cable is fully removed, the station reports the connector `Available` via `NotifyEvent`. Plugging the cable back in does not resume the (already-ended) transaction.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must choose `StopTxOnEVSideDisconnect` (stop vs. suspend on EV-side unplug, see E10) and `UnlockOnEVSideDisconnect`, balancing convenience against the risk of an unattended live or unlocked connector.

### E10 — When cable disconnected on EV-side: Suspend Transaction

When `StopTxOnEVSideDisconnect` is false, an EV-side unplug suspends the energy offer for safety but keeps the transaction open. If the driver plugs back in, charging resumes and the station reports a `TransactionEvent` (`Updated`, trigger `CablePluggedIn`). For a non-captive cable the driver must re-authorize to unlock and end the session (trigger `StopAuthorized`), after which removal triggers a `NotifyEvent` reporting the connector `Available`. For a captive cable, if it is not reconnected within a vendor-defined timeout the station ends the transaction (trigger `EVCommunicationLost`, stop reason `EVDisconnected`). Combining this with `UnlockOnEVSideDisconnect` = true is discouraged, as it can leave an authorized transaction with an unlocked connector.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent) (CS → CSMS)

> **ESCALATE: VENDOR-DEFINED** — The reconnection timeout for a captive cable before the suspended transaction is ended is not specified by OCPP and is left to the Charging Station implementer.

### E11 — Connection Loss During Transaction

A transaction continues normally even when the station loses its CSMS link mid-session. While offline the station queues all the `TransactionEvent` messages it would otherwise have sent, and replays them with the `offline` flag set once the connection is restored, then resumes normal communication. If memory runs low the station may drop intermediate `Updated` events — never the first or last — and may split bulky meter data across multiple `Updated` events sharing a timestamp; signed meter values are still captured when `SampledDataSignReadings` is true.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

### E12 — Inform CSMS of an Offline Occurred Transaction

This covers a transaction that both started and stopped while the station was offline. After reconnecting (and sending a `Heartbeat`), the station replays the full queued sequence for that transaction in order — `Started`, any `Updated`, and `Ended` — each with the `offline` flag true, and the CSMS acknowledges each so it can reconstruct and bill the entire session that happened during the outage.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [Heartbeat](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat) (CS → CSMS)

### E13 — Transaction-related message not accepted by CSMS

This defines retry behavior when the CSMS, while online, rejects a transaction message or fails to answer within the message timeout (distinct from being fully offline). The station resends the same message, waiting before each retry for an interval equal to `MessageAttemptIntervalTransactionEvent` multiplied by the number of prior attempts, up to `MessageAttemptsTransactionEvent` total attempts. If the final attempt still fails, the station discards that message and proceeds to the next queued transaction message. For example, with three attempts and a 60-second base interval, the waits are 60s then 120s before the message is dropped.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must tune `MessageAttemptsTransactionEvent` and `MessageAttemptIntervalTransactionEvent`, trading delivery persistence against the risk of permanently losing transaction data after the attempt budget is exhausted.

### E14 — Check transaction status

The CSMS can ask whether a transaction is still running and whether the station still has undelivered messages for it, using `GetTransactionStatus`. With a `transactionId` the response reports `ongoingIndicator` (transaction still active) and `messagesInQueue` (pending messages for that transaction); without one, only `messagesInQueue` is returned for the queue as a whole. This is useful when the CSMS receives an `Ended` event but notices a gap in sequence numbers and wants to decide whether to wait or bill immediately. A response with both indicators false means either the transaction is finished with nothing pending, or the station no longer knows the transaction.

**Messages:** [GetTransactionStatus](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#gettransactionstatus) (CSMS → CS)

### E15 — End of charging process

This aligns OCPP with the ISO 15118 end-of-charging flow (ISO 15118-1 H1). When the EV signals it is done — e.g. a `SessionStopReq(Terminate)` — and the charging session closes, the station reports the transaction to the CSMS. Depending on `TxStopPoint`, if it has not already sent a `StopAuthorized` trigger it emits either a `TransactionEvent` (`Ended`, trigger `StopAuthorized`, stop reason `StoppedByEV`) for stop points like `Authorized`/`PowerPathClosed`/`EnergyTransfer`, or an `Updated` event (trigger `StopAuthorized`) for others. Configured meter measurands are attached to the `Ended` event; under memory pressure intermediate values may be dropped but never the start and end readings.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS)

### E16 — Transactions with fixed cost, energy, SoC or time

New in OCPP 2.1: a driver or the CSMS can cap a transaction by cost, energy, state of charge, or time, and the limit may be changed mid-session more than once. A driver-set limit (e.g. an energy ceiling entered at the UI) is reported in `transactionInfo.transactionLimit` on the next `TransactionEvent` (trigger `LimitChanged`); a CSMS-set limit (e.g. a prepaid balance or direct-payment hold as `maxCost`) is delivered in a `TransactionEvent` response and echoed back by the station as confirmation. When a limit is reached the station suspends energy and reports it with trigger `EnergyLimitReached` or `CostLimitReached` and `chargingState` `SuspendedEVSE`; raising the limit resumes transfer. Note it is the energy transfer, not the transaction duration, that is limited — the transaction still ends per `TxStopPoint`. If the station cannot calculate cost locally it relies on cost updates from the CSMS (in the `TransactionEvent` response or a `CostUpdated`) to know when to stop. Supported limits are advertised in `TxCtrlr.SupportedLimits`, and if several limits are set the first one reached ends the transfer.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [CostUpdated](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#costupdated) (CSMS → CS)

> **ESCALATE: POLICY-DEPENDENT** — The operator/CSMS must decide which limit types to set and their values, and whether cost is calculated locally (precise cut-off) or driven by CSMS cost updates (which stop at or near the limit).

### E17 — Resuming transaction after forced reboot

New in OCPP 2.1: a transaction can survive an unexpected reboot — power loss, watchdog event, maintenance mode, or software fault. If `TxResumptionTimeout` is greater than zero and the interruption was no longer than that timeout, the station restores each affected transaction to its pre-reboot charging state on restart and reports a `TransactionEvent` (`Updated`, trigger `TxResumed`). If `TxAllowEnergyTransferResumption` is false, energy transfer is not automatically resumed (a previously `Charging` state returns as `SuspendedEVSE`), guarding against a different EV having been plugged in during the outage. If the interruption exceeded the timeout, the station ends the transaction with a `TransactionEvent` (`Ended`, trigger `AbnormalCondition`, stop reason `PowerLoss` or `Reboot`). Because `TxProfile` charging profiles need not persist, the CSMS may re-send any applicable profile with `SetChargingProfile` after resumption.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent) (CS → CSMS), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile) (CSMS → CS)

> **ESCALATE: POLICY-DEPENDENT** — The operator must set `TxResumptionTimeout` and `TxAllowEnergyTransferResumption`, trading transaction continuity across outages against the safety risk of auto-resuming energy when the vehicle at the plug may have changed.

---

## F. Remote Control

### F01 — Remote Start Transaction - Cable Plugin First

When an EV driver plugs the cable first and the charging station has already started a transaction (triggerReason `CablePluggedIn` or `EVConnectTimedOut`), the CSMS can subsequently send a `RequestStartTransaction` to associate that session with a specific user identity. The charging station returns the already-running `transactionId` in the response so the CSMS can link the two. If `AuthorizeRemoteStart` is set to `true`, the charging station additionally performs an authorization check before enabling energy flow. Energy transfer begins and the charging station reports progress via `TransactionEvent` with `triggerReason = RemoteStart`.

**Messages:** [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: POLICY-DEPENDENT** — The operator must decide whether `AuthorizeRemoteStart` is enabled, determining if a backend-initiated start still requires the charging station to perform a local authorization round-trip before energy flows.

### F02 — Remote Start Transaction - Remote Start First

The CSMS initiates a session before the EV driver connects by sending `RequestStartTransaction` with an `idToken` and optionally an `evseId`. The charging station responds `Accepted` and begins waiting for the cable to be plugged in; a new transaction is started immediately with `triggerReason = RemoteStart`. If the cable is not connected within the `ConnectionTimeOut` interval, the charging station ends the transaction with `triggerReason = EVConnectTimeout`. Once connected, energy transfer starts and subsequent state changes are reported as `TransactionEvent` updates.

**Messages:** [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: OPERATOR-CONFIG** — The operator must configure `ConnectionTimeOut` to balance usability (giving drivers time to plug) against EVSE lock-up when a driver never arrives; the default value may not suit all deployment contexts.

### F03 — Remote Stop Transaction

The CSMS sends `RequestStopTransaction` carrying the `transactionId` it wishes to end. The charging station stops energy transfer, optionally unlocks the cable-retention lock, and emits a `TransactionEvent` with `triggerReason = RemoteStop` followed by an `Ended` event once the cable is unplugged. The charging station responds `Accepted` if the transaction exists and is active, or `Rejected` if the `transactionId` is unknown.

**Messages:** [RequestStopTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststoptransaction), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: OPERATOR-CONFIG** — The operator must configure `StopTxOnEVSideDisconnect` and `UnlockConnectorOnEVSideDisconnect` to specify whether a remote stop automatically unlocks the connector; some deployments keep the connector locked until the driver physically requests release.

### F04 — Remote Stop ISO 15118 Charging from CSMS

This use case mirrors F03 but targets sessions conducted over ISO 15118-2 or ISO 15118-20. After receiving `RequestStopTransaction`, the charging station stops energy transfer and additionally sends the appropriate ISO 15118 control signal to the vehicle: `EVSENotification = StopCharging` for ISO 15118-2 sessions or a `Terminate` message for ISO 15118-20. The transaction is then closed in OCPP in the same way as a regular remote stop.

**Messages:** [RequestStopTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststoptransaction), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-DEFINED** — The vendor must implement the correct ISO 15118 session-termination signal path; the OCPP spec delegates the EV-side signaling mechanism entirely to the charging station implementation.

### F05 — Remotely Unlock Connector

When an EV driver cannot unplug a cable because the cable-retention lock is stuck, the CSO can trigger a remote unlock by sending `UnlockConnector` with the target `evseId` and `connectorId`. The charging station attempts to release the lock and returns one of `Unlocked`, `UnlockFailed`, `UnknownConnector`, or `OngoingAuthorizedTransaction`. This message targets only the cable-retention lock, not an access-door lock; if the connector has no motorized lock the charging station should respond with a CALLERROR: NotSupported.

**Messages:** [UnlockConnector](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#unlockconnector)

> **ESCALATE: OPERATOR-POLICY** — The operator must define the procedure for notifying the driver and dispatching field service when `UnlockFailed` is returned, as the protocol provides no automatic escalation path beyond the single response status.

### F06 — Trigger Message

The CSMS can demand that a charging station send a specific CS-initiated message on demand by issuing `TriggerMessage` with a `requestedMessage` value and an optional `evse` scope. The charging station first replies with `Accepted`, `Rejected`, or `NotImplemented`, and then — if accepted — sends the requested message with current data (e.g. a `TransactionEvent` with `triggerReason = Trigger`, a `MeterValues` snapshot, or a `StatusNotification`). OCPP 2.1 adds `CustomTrigger` support, allowing the CSMS to request vendor-specific message types declared in the charging station's `CustomizationCtrlr.CustomTriggers` variable.

**Messages:** [TriggerMessage](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#triggermessage)

> **ESCALATE: VENDOR-DEFINED** — Custom trigger identifiers are vendor-defined; the CSMS must know which custom trigger strings a given charging station model supports, which requires out-of-band coordination between vendor and operator.

### F07 — Remote start with fixed cost, energy, SoC or time

This use case (new in OCPP 2.1) lets the CSMS cap a remotely started session by delivering a `transactionLimit` in the first `TransactionEventResponse` after the session `eventType = Started` is received. The limit can specify one or more of `maxCost`, `maxEnergy`, `maxTime`, or `maxSoC`. The charging station echoes the limit back in the next `TransactionEventRequest` and enforces it by suspending energy delivery (`SuspendedEVSE`) once the threshold is reached. The initial `RequestStartTransaction` follows F01 or F02 flow normally.

**Messages:** [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: POLICY-DEPENDENT** — The CSMS must determine which limit dimension(s) to apply and how to source the values (e.g. from a tariff engine, a driver preference, or a grid contract); the protocol does not prescribe how the limit is calculated or communicated to the driver before the session starts.

---

## G. Availability

### G01 — Report connector AvailabilityState

Whenever a connector's availability state changes — because a cable was plugged in, unplugged, or a `ChangeAvailability` command was processed — the charging station reports the new state to the CSMS. The preferred method in OCPP 2.1 is a `NotifyEvent` with `component.name = "Connector"`, `variable = "AvailabilityState"`, `actualValue` set to the new state string, and `trigger = Delta`; the older `StatusNotification` is an accepted alternative but is deprecated and will be removed in a future release. An `Unavailable` state set by a `ChangeAvailability` command persists across reboots. When a cable is plugged into one connector on a multi-connector EVSE, the charging station must not report a state change for the other connectors on that EVSE.

**Messages:** [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [StatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification)

> **ESCALATE: OPERATOR-CONFIG** — The operator must configure the CSMS to handle both `NotifyEvent` (preferred) and `StatusNotification` (legacy) reports for connector status, since the spec allows charging stations to choose either path during the transition period.

### G02 — Heartbeat

A charging station sends a `Heartbeat` to the CSMS at regular intervals configured by `HeartbeatInterval` to confirm it is still online; the interval is set from the `BootNotificationResponse` after a successful registration. The `HeartbeatResponse` carries the CSMS's `currentTime`, which the charging station may use to synchronize its internal clock. Over WebSocket, the heartbeat is not needed to keep the connection alive, but if it is used for clock synchronization it should be sent at least once every 24 hours even when other messages are flowing continuously.

**Messages:** [Heartbeat](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md#heartbeat)

> **ESCALATE: OPERATOR-CONFIG** — The operator must decide the `HeartbeatInterval` value and whether clock synchronization via heartbeat is required; setting the interval too high wastes bandwidth, while too low a value may mask connectivity problems.

### G03 — Change Availability EVSE/Connector

The CSMS can set a specific EVSE or connector to `Operative` or `Inoperative` by sending `ChangeAvailability` with an `evse` object identifying the target and the desired `operationalStatus`. If a transaction is in progress on the targeted EVSE, the charging station responds `Scheduled` and applies the change after the transaction ends; otherwise it responds `Accepted` immediately. After the state change takes effect, the charging station reports the new status for each affected connector (and EVSE) via `NotifyEvent` or `StatusNotification`. EVSEs and connectors have independent states, and the set availability persists across reboots.

**Messages:** [ChangeAvailability](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#changeavailability), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [StatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification)

> **ESCALATE: OPERATOR-POLICY** — The operator must define how the CSMS handles `Scheduled` responses — i.e., whether to track pending availability changes, set a timeout, or alert staff — as the protocol does not mandate any follow-up mechanism after the response is received.

### G04 — Change Availability Charging Station

This is a station-level variant of G03: omitting the `evse` field in `ChangeAvailability` instructs the charging station to change the availability of the entire unit. When set to `Inoperative`, all operative EVSEs and connectors (those not already `Faulted`) become `Unavailable`; when restored to `Operative`, the charging station reverts all EVSEs and connectors to their individual pre-change states. If any transaction is in progress, the response is `Scheduled` and the change is deferred. The availability state set this way persists across power loss or reboot.

**Messages:** [ChangeAvailability](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#changeavailability), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [StatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification)

> **ESCALATE: OPERATOR-POLICY** — The operator must decide the maintenance workflow: whether to wait for in-flight transactions to conclude before sending the station-wide `Inoperative` command, and how long to wait before escalating to a forced stop.

### G05 — Lock Failure

After an EV driver is authorized and plugs in, if the charging station's cable-retention lock fails to engage, the station must not start energy transfer and must report the hardware fault. The charging station sends a `NotifyEvent` for the `ConnectorPlugRetentionLock` component with `variable = Problem` and `value = True`. The CSMS may optionally surface an alert to the driver (e.g. "cable cannot be locked") through external channels; the charging station itself may show a local notification. A lock failure can also be triggered when unlocking a connector (F05) fails.

**Messages:** [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent)

> **ESCALATE: OPERATOR-POLICY** — The operator must decide how a lock-failure event is handled operationally: whether to automatically set the connector `Inoperative`, dispatch a technician, or notify the driver through a separate channel, as OCPP defines only the fault-reporting step.

---

## H. Reservation

### H01 — Reservation

The CSMS reserves an EVSE for a specific EV driver by sending `ReserveNow` with an `idToken`, an `expiryDateTime`, and optionally an `evseId` or a `connectorType`. If `evseId` is omitted, the charging station reserves any available EVSE on the station; if `evseId` is provided, only that specific EVSE is reserved. On success the charging station responds `Accepted` and reports the connector status change to `Reserved` via `NotifyEvent` (or the legacy `StatusNotification`). Only available EVSEs can be reserved; the spec acknowledges that reserving a currently occupied EVSE is possible if the CSMS delays sending the message until the EVSE becomes free.

**Messages:** [ReserveNow](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#reservenow), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [StatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification)

> **ESCALATE: POLICY-DEPENDENT** — The operator must define the maximum reservation window, how to handle a reservation that outlasts the expiry without being used, and whether to charge a no-show fee — none of which are specified by the protocol.

### H02 — Cancel Reservation

The CSMS can withdraw an active reservation before its expiry time by sending `CancelReservation` with the `reservationId` originally assigned in H01. If the reservation is found and removed, the charging station responds `Accepted` and the EVSE returns to `Available`; if the `reservationId` is unknown, it responds `Rejected`. A connector state update (`NotifyEvent` or `StatusNotification`) is sent to reflect the availability change.

**Messages:** [CancelReservation](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#cancelreservation), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [StatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification)

> **ESCALATE: OPERATOR-POLICY** — The operator must decide whether a driver-requested cancellation is routed through the CSMS to the charging station or handled locally, and whether any cancellation penalty is applied at the CSMS layer.

### H03 — Use a reserved EVSE

When the driver whose `idToken` (or `groupIdToken`) matches the reservation presents their credential at the reserved EVSE, the charging station clears the reservation and begins the authorization and transaction flow as normal. The charging station sends `ReservationStatusUpdate` with `reservationUpdateStatus = Removed` to inform the CSMS that the reservation was consumed. If a different driver's token is presented, the charging station rejects it (or handles it according to the authorization result) and the reservation remains active.

**Messages:** [ReservationStatusUpdate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#reservationstatusupdate), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: OPERATOR-POLICY** — The operator must configure what happens when a third-party driver attempts to use a reserved EVSE: whether to reject silently, show an error, or allow charging if capacity permits; the spec does not prescribe behavior beyond keeping the reservation intact.

### H04 — Reservation Ended, not used

If the reservation expires before the reserved driver shows up, the charging station automatically releases the EVSE and informs the CSMS by sending `ReservationStatusUpdate` with `reservationUpdateStatus = Expired`. Similarly, if the reservation is cleared for any other reason without a transaction being started, the status `NoTransaction` is used. After the reservation ends, the connector reverts to `Available` and the CSMS is responsible for any downstream actions such as charging a no-show fee.

**Messages:** [ReservationStatusUpdate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md#reservationstatusupdate), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [StatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md#statusnotification)

> **ESCALATE: OPERATOR-POLICY** — The operator must define the business logic that executes when a reservation expires unused: whether to notify the driver, levy a penalty, re-open the slot to walk-up users, or trigger a new reservation offer — all of which lie outside the OCPP protocol boundary.

---

## I. Tariff And Cost

### I01 — Show EV Driver-specific Tariff Information
Before a transaction starts, the EV Driver presents an identification token and the Charging Station authorizes it with the CSMS. When the CSMS recognizes the driver it can attach a human-readable, driver-specific tariff description to the authorization result, which the Charging Station then displays so the driver knows the price before committing to charge. This use case only covers showing a textual representation of the tariff; it does not require the Charging Station to support the structured `TariffType` used for local cost calculation. See [Tariff And Cost deep-dive](../OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md) for how this fits the central- versus local-calculation split.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize)

> **ESCALATE: OPERATOR-POLICY** — The wording, language(s), currency formatting and level of detail of the driver-facing tariff text, and whether the same message is shown to every token, are commercial/UX decisions the operator must define; the protocol only carries the free-text personal message.

### I02 — Show EV Driver Running Total Cost During Charging
While a transaction is in progress, the driver wants to see the accumulating cost. With central cost calculation the CSMS owns the running total and pushes periodic updates to the Charging Station via CostUpdated, or returns the running cost in the response to a transaction event the station already sends. The Charging Station then renders that figure on its display. The update frequency is a trade-off: more frequent updates give a smoother display but generate more traffic and mobile-data cost.

**Messages:** [CostUpdated](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#costupdated), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: OPERATOR-POLICY** — How often the CSMS recomputes and pushes the running total (the update interval) balances display freshness against messaging cost and is an operator deployment decision, not fixed by the protocol.

### I03 — Show EV Driver Final Total Cost After Charging
When the driver stops the transaction, the Charging Station reports the end event to the CSMS, which returns the final total cost in its response. The Charging Station displays that figure so the driver sees the final price before leaving. A free transaction is signalled by a total cost of exactly 0.00 — omitting the cost does not mean free. If the station was offline at stop time, or the stop model requires the driver to physically leave (parking-bay occupancy) before the transaction ends, there may be no display opportunity; see [I05 — Show Fallback Total Cost Message](#i05--show-fallback-total-cost-message).

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: OPERATOR-POLICY** — Whether and how the final cost is surfaced (on-station display, app, email receipt), and the settlement/refund handling for the figure shown, are operator commercial decisions; OCPP only delivers the computed total.

### I04 — Show Fallback Tariff Information
When the Charging Station cannot obtain a driver-specific tariff before charging — for example it is offline, or the CSMS returns no tariff for the token — it falls back to a generic message configured locally in `TariffFallbackMessage`. This gives the driver at least some price indication instead of nothing. The fallback text can be set or updated by the CSMS through that configuration variable. This is the degraded-mode counterpart to [I01 — Show EV Driver-specific Tariff Information](#i01--show-ev-driver-specific-tariff-information).

**Messages:** No dedicated message.

> **ESCALATE: OPERATOR-POLICY** — The content of the fallback tariff message (and whether a generic price is even advertised when the real tariff is unknown) is a commercial/regulatory decision; advertising a price the operator cannot guarantee may carry consumer-protection implications.

### I05 — Show Fallback Total Cost Message
When a transaction is stopped while the Charging Station is offline, the station cannot retrieve the final total cost from the CSMS. Instead of leaving the driver with no information it shows a pre-configured fallback message from `TotalCostFallbackMessage`. This is the offline counterpart to [I03 — Show EV Driver Final Total Cost After Charging](#i03--show-ev-driver-final-total-cost-after-charging). The fallback text can be configured by the CSMS via that configuration variable.

**Messages:** No dedicated message.

> **ESCALATE: OPERATOR-POLICY** — The wording of the offline total-cost fallback message, and how the driver later obtains the actual billed amount once the station reconnects, are operator decisions outside the protocol.

### I06 — Update Tariff Information During Transaction
Some tariffs vary during a session — for example DC fast charging priced against a moving day-ahead energy price, often quoted as a range with a current value. As the Charging Station sends its periodic transaction-event updates, the CSMS checks whether newer tariff text is available and returns it in the response (in the personal-message fields, optionally in several languages), which the station then displays. Note that local regulation or contract terms may forbid changing the advertised tariff mid-session, in which case no update should be sent.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: REGULATORY** — Whether the tariff communicated at session start may change during the transaction, and under what disclosure conditions, is governed by local consumer-protection law and the operator's contract terms, not by OCPP.

### I07 — Local Cost Calculation - Set Default Tariff
New in OCPP 2.1: the CSMS installs a structured tariff on the Charging Station so the station can calculate cost locally. SetDefaultTariff with `evseId = 0` installs the tariff on every EVSE; a non-zero `evseId` targets one EVSE and overrides the station-wide default there. Each tariff carries a unique `tariffId`, so updating a default means installing a new tariff (optionally with a future `validFrom` so it activates at a scheduled time and replaces the prior default). Only one tariff structure fits per message because tariffs can be large. See the [Tariff And Cost deep-dive](../OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md) for the tariff structure and the `validFrom` activation rules.

**Messages:** [SetDefaultTariff](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#setdefaulttariff)

> **ESCALATE: OPERATOR-POLICY** — The actual prices, currency, tax rates, time-of-day conditions and fixed/idle fees in the default tariff are commercial and tax-jurisdiction values the operator must supply; the protocol only transports the structure.

### I08 — Local Cost Calculation - Receive Driver Tariff
New in OCPP 2.1: instead of (or on top of) the default tariff, the CSMS can return a driver-specific tariff inside the authorization result, which the Charging Station then uses for local cost calculation of that driver's transaction. The driver-specific tariff is "in use" from when it is received until the transaction for that token ends. If the driver does not accept the tariff the station deauthorizes; if the station receives a tariff it cannot process, the configured `HandleFailedTariff` strategy decides whether to refuse charging, fall back to the default tariff, or defer to central calculation by the CSMS. A driver-specific tariff may also arrive via [I11 — Local Cost Calculation - Change transaction tariff](#i11--local-cost-calculation---change-transaction-tariff).

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: OPERATOR-POLICY** — The `HandleFailedTariff` behaviour (deauthorize, use default, or central cost) and whether implicit tariff acceptance (e.g. plugging in the cable) is treated as consent are operator/regulatory choices the deployment must set.

### I09 — Local Cost Calculation - Get Tariffs
New in OCPP 2.1: the CSMS queries which tariffs are currently present on a Charging Station. GetTariffs with `evseId = 0` returns the tariffs across all EVSEs; a non-zero `evseId` scopes the result to one EVSE. The response lists tariff assignments per EVSE, distinguishing default tariffs (installed on every EVSE) from driver-specific tariffs (tied to a token, and reported with the EVSE where a transaction is active). If nothing matches, the station replies with status `NoTariff`.

**Messages:** [GetTariffs](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#gettariffs)

### I10 — Local Cost Calculation - Clear Tariffs
New in OCPP 2.1: the CSMS removes one or more default tariffs from a Charging Station. ClearTariffs can target specific `tariffIds`, a specific `evseId`, both, or neither (clear all). Driver-specific tariffs are not cleared by this message — they are removed automatically when no longer in use. A default tariff that is currently in use by an active transaction is reported as cleared but continues to be applied until that transaction ends, so running sessions are never disrupted.

**Messages:** [ClearTariffs](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#cleartariffs)

### I11 — Local Cost Calculation - Change transaction tariff
New in OCPP 2.1: the CSMS swaps the tariff associated with an ongoing transaction, for example to handle an unexpected price change. ChangeTransactionTariff targets a `transactionId` (the change is bound to the transaction, not the driver, since the same driver may have other sessions that should not change). The station validates the new tariff and may reject with reasons such as `TooManyElements`, `ConditionNotSupported`, `NoCurrencyChange` (currency cannot switch mid-transaction) or `TxNotFound`. On acceptance the new tariff applies from that moment forward with no retroactive recalculation, and the station emits a transaction event marking the change.

**Messages:** [ChangeTransactionTariff](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#changetransactiontariff), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: REGULATORY** — Whether a tariff may be changed during an active transaction at all, and whether explicit customer agreement is required first, depends on local legislation and contract terms outside OCPP.

### I12 — Local Cost Calculation - Cost Details of Transaction
New in OCPP 2.1: when local cost calculation is active, the Charging Station produces a detailed cost breakdown and returns it to the CSMS so the CSMS can generate invoices or Charge Detail Records. During the session the station may send running cost updates (without per-period detail, to limit data); when the transaction ends it includes a full breakdown in the end event — a list of charging periods (one per pricing change), per-dimension totals for fixed fee, energy, charging time, idle time and reservation, and the overall total with tax handling (stacked tax rates, optional min/max cost capping). If the station cannot compute the cost it flags the failure rather than reporting a wrong figure. See the [Tariff And Cost deep-dive](../OCPP-2.1-TariffCost/OCPP-2.1-TariffCost.md) for the CostDetails structure and the tax-stacking and min/max rules.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: REGULATORY** — Tax-rate stacking (e.g. energy tax then VAT), invoice/CDR formatting and the legal validity of the locally calculated breakdown for billing are jurisdiction-specific decisions the operator and its tax advisor must make; OCPP only carries the numbers.

---

## J. Meter Values

### J01 — Sending Meter Values not related to a transaction
The Charging Station samples its energy meter or other sensors and sends those readings to the CSMS outside of any transaction, using the dedicated MeterValues message. Clock-aligned readings (taken at fixed wall-clock intervals such as every quarter hour, configured via `AlignedDataCtrlr`) and standalone diagnostic samples both travel this way. Each reading carries a timestamp and one or more sampled values, optionally tagged with measurand, context, location and phase; signed meter values can be included for fiscally certified meters. When an EVSE is in a transaction its clock-aligned values are sent inside transaction events instead, and `AlignedDataSendDuringIdle` can restrict aligned values to idle periods only.

**Messages:** [MeterValues](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-MeterValues.md#metervalues)

> **ESCALATE: VENDOR-CONFIG** — Which measurands are sampled, at what interval, at which locations/phases, and whether upstream (potentially privacy-sensitive) measurands are reported are deployment configuration choices; upstream measurands may require an explicit agreement due to data-protection and liability implications.

### J02 — Sending transaction related Meter Values
During an ongoing transaction the Charging Station samples metering data and offloads it to the CSMS inside transaction-event updates rather than standalone MeterValues messages. The measurands and sampling interval are configured through `SampledDataCtrlr` (`TxUpdatedMeasurands` / `TxUpdatedInterval`). All meter values reported must relate to the EVSE on which the transaction runs, and register values must increase monotonically and be read directly from the meter (not re-based to zero per transaction) so the CSMS can audit for missing energy between sessions. If the station is offline it queues these messages; if it is offline and low on memory it may drop intermediate updates first, never breaking the queue order. Signed meter values can be attached when supported.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-CONFIG** — The set of transaction measurands and the sampling interval, plus the behaviour when memory is constrained, are deployment configuration decisions; the fiscal-meter register values themselves may carry billing/legal-metrology obligations.

### J03 — Charging Loop with metering information exchange
This use case maps the ISO 15118 metering loop onto OCPP. During AC or DC charging the EV requests metering status from the Charging Station, which returns fiscal-meter readings (with a signed meter reading where required), and the EV acknowledges receipt with a MeteringReceipt message. The Charging Station does not forward that ISO 15118 receipt to the CSMS directly; instead it reports the signed meter values to the CSMS as ordinary transaction-related meter values exactly as in [J02 — Sending transaction related Meter Values](#j02--sending-transaction-related-meter-values). A station may, as an implementation choice, require an EV MeteringReceipt to acknowledge each fiscal reading before it is forwarded.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-CONFIG** — Whether the Charging Station mandates an ISO 15118 MeteringReceipt acknowledgement from the EV before forwarding each fiscal meter value is a vendor/operator implementation decision, not fixed by OCPP.

---

## K. Smart Charging

### K01 — SetChargingProfile
The base smart-charging operation: the CSMS sends a charging profile to an EVSE (or to EVSE 0 for the whole station) to cap the power or current an EV may draw over a period of time, staying within whatever limits an external system imposes. A profile carries a purpose (`TxProfile`, `TxDefaultProfile`, `ChargingStationMaxProfile`, `ChargingStationExternalConstraints`, `PriorityCharging`, `LocalGeneration`), a stack level and a validity window; the station re-evaluates its active profiles whenever a new one is set. A `TxProfile` must reference a `transactionId` and is only applied if that transaction is known; the CSMS must not reuse the same stackLevel/purpose/evseId combination across overlapping profiles, and it must never set `ChargingStationExternalConstraints` itself (that purpose is reserved for externally imposed limits). See the [OCPP 2.0.1 Smart Charging deep-dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) for profile-purpose stacking and composite-schedule fundamentals.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

### K02 — Central Smart Charging
The CSMS holds the load-management intelligence centrally. After authorization the EVSE first applies whatever default profile it already holds (limiting the Control Pilot signal so the EV cannot draw full power before the CSMS reacts), and once the transaction starts the CSMS may respond to the transaction event by pushing a per-transaction `TxProfile` that overrules the `TxDefaultProfile` for the life of that session and is deleted when it ends. The station continuously adapts current/power to the merged active profiles. It is recommended to omit the schedule `duration` so the `TxProfile` lasts the whole transaction; if it expires early the station falls back to the lowest limit of the active `TxDefaultProfile` and `ChargingStationMaxProfile`, then to the local hardware limit. The CSMS should check the `offline` flag on a transaction event before sending a profile, since the event may have been cached.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-CONFIG** — How the CSMS calculates per-transaction constraints (the central load-balancing algorithm) is not specified by OCPP; it is an operator/vendor backend decision.

### K03 — Local Smart Charging
An illustrative (non-prescriptive) example of load-balancing performed by a Local Controller rather than the CSMS. The Local Controller is given a total cluster limit — via a `ChargingStationMaxProfile` from the CSMS or a `ChargingStationExternalConstraints` profile from an EMS — and divides that budget across active transactions. Charging stations carry a low `TxDefaultProfile` (e.g. 6 A) so a vehicle cannot pull full power before the controller intervenes; when a transaction starts or stops, the Local Controller re-issues `TxProfile`s to the remaining sessions to redistribute the available current. The Local Controller sits in the OCPP path between stations and CSMS, registering transaction IDs as it forwards transaction events. See the [OCPP 2.0.1 Smart Charging deep-dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) for the Local Controller topology.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-CONFIG** — The local load-balancing strategy (how the cluster budget is split, whether departure time or state-of-charge is considered) is an implementation choice; OCPP only carries the resulting profiles.

### K04 — Internal Load Balancing
Here the Charging Station itself balances current/power between its own EVSEs, rather than relying on the CSMS or a Local Controller. The station is configured with a fixed ceiling (typically the grid-connection limit) — expressed as a `ChargingStationMaxProfile`, which may only be set at EVSE 0 (the whole station) — and controls each EVSE's schedule so the combined draw stays within it. The optional `minChargingRate` field tells the station that charging below a certain rate is inefficient, letting it choose a smarter balancing strategy. New in 2.1: when a `LocalGeneration` profile is active, the combined energy flow may go up to `ChargingStationMaxProfile + LocalGeneration` (see [K27](#k27--smart-charging-with-ems-and-localgeneration)).

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

> **ESCALATE: VENDOR-CONFIG** — The internal per-EVSE power-distribution algorithm is left to the Charging Station vendor; OCPP only sets the overall ceiling.

### K05 — Remote Start Transaction with Charging Profile
The CSMS embeds a charging profile directly in the remote-start request so the transaction is governed by the right schedule from the very first moment — important because, for example, the choice between three-phase and single-phase charging cannot always be changed once charging has begun, and because the station may go offline right after receiving the request. The included profile must have purpose `TxProfile` and cannot carry a `transactionId` (none exists yet); the station uses it when computing its composite schedule. A station that supports smart charging but receives an invalid profile rejects the start with `InvalidProfile` or `InvalidSchedule`; a station without smart-charging support simply ignores the profile.

**Messages:** [RequestStartTransaction](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md#requeststarttransaction), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

### K06 — Offline Behavior Smart Charging During Transaction
Defines what a station does with smart charging when it loses CSMS connectivity mid-transaction. If it had already received a `TxProfile` for the active transaction, it keeps applying that profile until the transaction ends or the profile expires, whichever comes first, operating stand-alone with no need for the backend. If it holds no charging profiles at all when it goes offline, it runs the transaction as though no constraints apply. No dedicated message is exchanged while offline — this use case is about local fallback behaviour.

**Messages:** No dedicated message.

### K07 — Offline Behavior Smart Charging at Start of Transaction
Covers a transaction that both starts and runs while the station is offline. By installing a `TxDefaultProfile` ahead of time, the CSMS guarantees that any transaction begun during a connectivity outage is governed by a sensible schedule. The station authorizes the driver locally (Local Authorization List, Authorization Cache, or `OfflineTxForUnknownIdEnabled`), starts the transaction as usual, and continuously adapts current/power to the already-installed default profile. See [K01](#k01--setchargingprofile) and the [OCPP 2.0.1 Smart Charging deep-dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md) for how profile purposes combine.

**Messages:** No dedicated message.

### K08 — Get Composite Schedule
The CSMS asks the station to report its composite schedule — the single effective schedule that results from merging all active charging profiles of the different purposes plus any local limits, taking the most restrictive value in each time interval. The report shows the power or current the station expects to draw from the grid for the requested EVSE over the requested duration; requesting EVSE 0 yields the total grid-connection forecast. The result is only indicative for that instant, since local balancing or an EVSE becoming free can change it later. New in 2.1: when no transaction is active the station computes the schedule as if a `TxDefaultProfile`-driven transaction were running (with `randomizedDelay = 0`); V2X-aware merging caps `setpoint` between `dischargeLimit` and `limit`, reports per-phase `limit_L2`/`limit_L3` values, and adds `LocalGeneration` capacity on top of the merged limit. See the [V2X bidirectional deep-dive](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) for setpoint/dischargeLimit sign conventions.

**Messages:** [GetCompositeSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#getcompositeschedule)

### K09 — Get Charging Profiles
The CSMS retrieves the charging profiles currently installed in a station — all of them or a filtered subset — for automatic control logic or operator debugging. The request filters either by a list of `chargingProfileId`s, or by some combination of `stackLevel`, `chargingLimitSource` and `chargingProfilePurpose`, optionally scoped to a specific `evseId` (EVSE 0 returns only the station-level profiles such as `ChargingStationMaxProfile` and `ChargingStationExternalConstraints`). The station acknowledges with `Accepted` or `NoProfiles` if nothing matches, then streams the matching profiles back in one or more report messages, each carrying the original `requestId` and a `tbc` (to-be-continued) flag set on every report except the last.

**Messages:** [GetChargingProfiles](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#getchargingprofiles), [ReportChargingProfiles](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#reportchargingprofiles)

### K10 — Clear Charging Profile
The CSMS removes some or all previously installed charging profiles. The request can target a specific profile `id`, or filter by `evseId`, `chargingProfilePurpose` and `stackLevel`; the station clears every profile matching the supplied criteria and reports whether anything matched. If no installed profile matches, the station responds `Unknown` rather than treating it as an error.

**Messages:** [ClearChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearchargingprofile)

### K11 — Set / Update External Charging Limit With Ongoing Transaction
An External Control System — a DSO, smart meter, or home energy-management system — imposes a limit or schedule on the station over a non-OCPP interface (IEC 61850, OpenADR, or any protocol the station supports), and the station honours it for ongoing transactions while keeping the CSMS informed. The station never charges faster than the external limit (unless `ExternalConstraintsProfileDisallowed` is set), represents the limit internally as a `ChargingStationExternalConstraints` profile, and when the limit changes by more than `LimitChangeSignificance` it sends a `NotifyChargingLimit` (with `chargingLimitSource` never set to `CSO`, optionally including the schedule when `EnableNotifyChargingLimitWithSchedules` is true). If the actual charging rate changes significantly it also emits a transaction event with `triggerReason = ChargingRateChanged`. New in 2.1, the station may represent the external limit as an Absolute, Relative, or Dynamic profile (`operationMode = ExternalLimits`).

**Messages:** [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-CONFIG** — The interface and protocol between the External Control System and the station, and whether limits are modelled as Absolute/Relative/Dynamic profiles, are deployment decisions outside OCPP.

### K12 — Set / Update External Charging Limit Without Ongoing Transaction
The same external-limit mechanism as [K11](#k11--set--update-external-charging-limit-with-ongoing-transaction), but applied when no transaction is active — the limit constrains the grid connection and any future transactions rather than an in-progress session. The total load of all EVSEs must stay within the received limit, the station represents it as a `ChargingStationExternalConstraints` profile (it is recommended to use negative profile IDs to avoid clashing with CSMS-assigned IDs), and it notifies the CSMS via `NotifyChargingLimit` when the limit changes by more than `LimitChangeSignificance`, again never using `chargingLimitSource = CSO`. Because no transaction is running, no transaction event is involved.

**Messages:** [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit)

> **ESCALATE: VENDOR-CONFIG** — The non-OCPP interface to the external system and the profile representation are deployment decisions outside OCPP.

### K13 — Reset / Release External Charging Limit
The mirror of [K11](#k11--set--update-external-charging-limit-with-ongoing-transaction)/[K12](#k12--set--update-external-charging-limit-without-ongoing-transaction): the External Control System lifts a previously imposed limit. The station stops constraining charging based on that limit, and if a transaction is ongoing it recalculates the schedule and ramps the charging rate back up. It tells the CSMS the limit is gone by sending `ClearedChargingLimit` (carrying the `chargingLimitSource`), and if the resulting rate change on an active transaction exceeds `LimitChangeSignificance` it also emits a transaction event with `triggerReason = ChargingRateChanged`.

**Messages:** [ClearedChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearedcharginglimit), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

### K14 — External Charging Limit with Local Controller
The external-limit pattern applied to a cluster managed by a Local Controller instead of a single station. When the External Control System sets a grid limit, the Local Controller notifies the CSMS with `NotifyChargingLimit`, recalculates schedules for the whole cluster, and pushes a `SetChargingProfile` to every station whose profile changed. When the external limit is released, it sends `ClearedChargingLimit` and clears the affected profiles with `ClearChargingProfile`. Requires `ExternalControlSignalsEnabled = true`.

**Messages:** [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [ClearedChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearedcharginglimit), [ClearChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearchargingprofile)

> **ESCALATE: VENDOR-CONFIG** — The Local Controller's cluster-recalculation algorithm and its non-OCPP link to the External Control System are implementation decisions outside OCPP.

### K15 — ISO 15118-2 Charging with load leveling
Maps ISO 15118-2 high-level-communication charging (AC or DC) onto OCPP smart charging. When the EV sends its `ChargeParameterDiscoveryReq`, the station relays the EV's energy needs to the CSMS via `NotifyEVChargingNeeds`; the CSMS computes a schedule and returns it as a `SetChargingProfile` `TxProfile`, which the station folds into the ISO 15118 `ChargeParameterDiscoveryRes` (`SAScheduleList`) it sends back to the EV. Because that ISO message has a 60-second timeout, the CSMS must respond promptly — if it does not, or replies `Processing`, the station returns a schedule matching the EVSE's own capability and a late profile then triggers a renegotiation per [K16](#k16--renegotiation-initiated-by-csms). The `TxStartPoint` must fire before `ChargeParameterDiscoveryReq` so a transaction exists to attach the `TxProfile` to. Optionally the station forwards the EV's own calculated schedule with `NotifyEVChargingSchedule`. New in 2.1: signed SalesTariffs are supported via the `signatureValue` field.

**Messages:** [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyEVChargingSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingschedule), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

### K16 — Renegotiation initiated by CSMS
During an ISO 15118 session the CSMS changes the charging schedule by sending a new `SetChargingProfile`. The station cannot push this to the EV unilaterally; instead, on the EV's next `CurrentDemandReq` (DC) or `ChargingStatusReq` (AC) it signals `evseNotification = ReNegotiation`, the EV confirms with a `PowerDeliveryReq` (`chargeProgress = ReNegotiate`), and a fresh `ChargeParameterDiscovery` exchange then delivers the new `SAScheduleList`. The EV–station message detail is informative only; OCPP mandates only the profile push. Because every limit change in a dynamic schedule would force a renegotiation, the CSMS should avoid frequently updated `Dynamic` profiles for ISO 15118-2 sessions.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

### K17 — Renegotiation initiated by EV
The EV triggers the new schedule. When it sends a `ChargeParameterDiscoveryReq` carrying updated charging-needs parameters, the station forwards them to the CSMS via `NotifyEVChargingNeeds`; the CSMS computes a schedule that tries to honour the EV's needs while respecting other constraints and returns it as a `SetChargingProfile`. The station relays the new schedule to the EV in a `ChargeParameterDiscoveryRes`, the EV confirms with `PowerDeliveryReq` (`chargeProgress = Start`), and the station resumes power delivery if it had been suspended for the renegotiation. If the EV supplies its own charging profile, the station reports it back with `NotifyEVChargingSchedule`.

**Messages:** [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyEVChargingSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingschedule)

### K18 — ISO 15118-20 Scheduled Control Mode
New in OCPP 2.1: ISO 15118-20 scheduled-control charging. After the EV sends its energy needs and departure time in a `ScheduleExchangeReq`, the station relays them to the CSMS via `NotifyEVChargingNeeds` with `controlMode = ScheduledControl`. The CSMS replies with a `SetChargingProfile` carrying up to three alternative charging schedules plus optional price information; the station offers these to the EV in its `ScheduleExchangeRes`, and the EV picks one and returns its own calculated schedule, which the station forwards with `NotifyEVChargingSchedule`. See the [OCPP 2.1 Smart Charging deltas deep-dive](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md) for ISO 15118-20 control-mode details.

**Messages:** [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyEVChargingSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingschedule)

### K19 — ISO 15118-20 Dynamic Control Mode
New in OCPP 2.1: ISO 15118-20 dynamic-control charging, where the operator (not the EV) drives the schedule in real time. The station relays the EV's `ScheduleExchangeReq` to the CSMS via `NotifyEVChargingNeeds` with `controlMode = DynamicControl`; the CSMS returns a single charging schedule plus optional price information in a `SetChargingProfile`. The station passes only the pricing schedule (not the charging schedule) to the EV in its `ScheduleExchangeRes`; the EV then sends its fastest-possible `EVPowerProfile` in a `PowerDeliveryReq`, which the station ignores, instead applying the CSMS schedule and reporting it back with `NotifyEVChargingSchedule`. See the [OCPP 2.1 Smart Charging deltas deep-dive](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md) for dynamic-mode behaviour.

**Messages:** [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyEVChargingSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingschedule)

### K20 — ISO 15118-20 Adjusting charging schedule when energy needs change
New in OCPP 2.1: handles a mid-session change in the EV's departure time or target energy during an ISO 15118-20 session, regardless of which actor noticed the change. Whether the new `DepartureTime`/`EVTargetEnergyRequest` arrives via the EV (in `ScheduleExchangeReq` for scheduled control, or `ChargeLoopReq` for dynamic control) or is set by the station itself, the station reports the updated needs to the CSMS with `NotifyEVChargingNeeds`. The CSMS recomputes and pushes a new schedule via `SetChargingProfile`, which the station applies — in scheduled mode it returns the schedule to the EV and forwards the EV's projected `EVPowerProfile` back with `NotifyEVChargingSchedule`; in dynamic mode it steers charging directly through the `ChargeLoopRes`.

**Messages:** [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyEVChargingSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingschedule)

### K21 — Requesting priority charging remotely
New in OCPP 2.1: a driver requests immediate, maximum-power charging through the CSMS (for example via a smartphone app), overriding any V2X discharging or deferred schedule. The CSMS sends `UsePriorityCharging` with `activate = true` for the transaction; if the station holds a `PriorityCharging` profile it accepts, stops applying the `TxDefaultProfile`/`TxProfile` to that transaction, switches to the priority profile, and confirms with `NotifyPriorityCharging` (`activated = true`). If it has no such profile it responds `NoProfile`; if it cannot activate for another reason (e.g. unknown transaction) it responds `Rejected`. The priority profile stays in effect until the session ends or the CSMS deactivates it; the achieved power may still be below station maximum if other limits (e.g. load balancing) apply. Priority charging is not limited to V2X transactions. See the [V2X bidirectional deep-dive](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) for how priority charging suppresses discharging.

**Messages:** [UsePriorityCharging](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#useprioritycharging), [NotifyPriorityCharging](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyprioritycharging)

### K22 — Requesting priority charging locally
New in OCPP 2.1: the same priority-charging switch as [K21](#k21--requesting-priority-charging-remotely), but triggered at the station itself (a button or display) rather than through the CSMS. The station stops applying the `TxDefaultProfile`/`TxProfile` to the transaction, switches to its `PriorityCharging` profile, and informs the CSMS with `NotifyPriorityCharging` (`activated = true`). If the station has no `PriorityCharging` profile it cannot switch. If it is offline when the user activates, it applies the priority profile immediately and queues the `NotifyPriorityCharging` message for when it reconnects. The profile remains active until the session ends or priority charging is cancelled.

**Messages:** [NotifyPriorityCharging](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyprioritycharging)

### K23 — Smart Charging with EMS connected to Charging Stations
New in OCPP 2.1: a worked example of [K11](#k11--set--update-external-charging-limit-with-ongoing-transaction)/[K12](#k12--set--update-external-charging-limit-without-ongoing-transaction) where the External Control System is a building Energy Management System wired directly to each station. The EMS measures other site loads and local generation, computes the power available for charging so the grid connection is not overloaded, and sets a limit (or schedule) on each station over a non-OCPP link. Each station represents this internally as a `ChargingStationExternalConstraints` profile and, when the limit shifts by more than `LimitChangeSignificance`, notifies the CSMS with `NotifyChargingLimit` (`chargingLimitSource = EMS`); an ongoing transaction also gets a transaction event with `triggerReason = ChargingRateChanged`. Requires `ExternalControlSignalsEnabled = true`. The requirements are fully covered by K11 and K12.

**Messages:** [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-CONFIG** — The EMS-to-station interface and the site load-management algorithm are deployment decisions outside OCPP.

### K24 — Smart Charging with EMS connected to Local Controller
New in OCPP 2.1: the [K14](#k14--external-charging-limit-with-local-controller) pattern where the External Control System is a building EMS wired to a Local Controller that manages a cluster of stations. The EMS regularly updates a current/power limit for the whole cluster to protect the grid connection; the Local Controller notifies the CSMS, recalculates per-station profiles, and pushes them down. The message flow and requirements are those of K14.

**Messages:** [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [ClearedChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearedcharginglimit), [ClearChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#clearchargingprofile)

> **ESCALATE: VENDOR-CONFIG** — The EMS-to-Local-Controller interface and the cluster scheduling algorithm are deployment decisions outside OCPP.

### K25 — Smart Charging with EMS acting as a Local Controller
New in OCPP 2.1: the EMS and Local Controller are combined into one component, so all OCPP traffic passes through it. This lets the EMS-part see the full transaction state — schedules imposed by the CSMS, EV state-of-charge, planned departure time — and therefore do more advanced scheduling than an external EMS could. It calculates a power profile per station and sends each as a `ChargingStationMaxProfile` (in addition to any CSMS profiles flowing through it), keeping the grid connection within limits.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

> **ESCALATE: VENDOR-CONFIG** — The combined EMS/Local-Controller scheduling logic and its site-measurement inputs are implementation decisions outside OCPP.

### K26 — Smart Charging with Hybrid Local & Cloud EMS
New in OCPP 2.1: a variant of [K25](#k25--smart-charging-with-ems-acting-as-a-local-controller) where the EMS is split between a cloud instance and a local on-site instance. Two topologies are possible: the cloud part handles scheduling and Local Controller functionality while the local part measures site loads and acts as a fail-safe against grid overload; or the cloud part handles only scheduling while the local part is the Local Controller plus fail-safe. Either way the local component provides the overload protection that a purely cloud-based EMS could not guarantee during connectivity loss. Profiles reach the stations as in K25 (`ChargingStationMaxProfile` via `SetChargingProfile`).

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

> **ESCALATE: VENDOR-CONFIG** — Which functions run in the cloud vs. on-site (the split topology), the inter-component protocol, and the fail-safe logic are deployment/vendor decisions outside OCPP.

### K27 — Smart Charging with EMS and LocalGeneration
New in OCPP 2.1: lets locally generated power (e.g. solar) that the CSMS does not know about be added on top of the normal charging limit. The station represents the generation forecast internally as a `LocalGeneration` charging profile; the effective ceiling becomes the merged limit plus the local-generation capacity (so, for example, a 5 kW `TxDefaultProfile` plus 2 kW of solar allows 7 kW). When the available generation changes by more than `LimitChangeSignificance`, the station notifies the CSMS with `NotifyChargingLimit`, flagging the source as local generation. See [K04](#k04--internal-load-balancing) for how `LocalGeneration` raises the `ChargingStationMaxProfile` ceiling.

**Messages:** [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit)

> **ESCALATE: VENDOR-CONFIG** — How the station obtains and forecasts the local-generation schedule (the EMS interface) is a deployment decision outside OCPP.

### K28 — Dynamic charging profiles from CSMS
New in OCPP 2.1: a `Dynamic` charging profile has a single schedule period whose `limit`/`setpoint` can be updated repeatedly without resending the whole profile. Two update modes exist. Push: the CSMS first installs the dynamic profile with `SetChargingProfile` (no `dynUpdateInterval`), then sends new values with `UpdateDynamicSchedule` whenever it wants; the station applies each value and stamps `dynUpdateTime`. Pull: the CSMS installs the profile with a `dynUpdateInterval` (e.g. 60 s), and the station periodically requests fresh values with `PullDynamicScheduleUpdate`, the CSMS returning them in the response. In both modes, if a `duration` is set and no update arrives before it elapses the schedule ends and the station falls back to the next valid profile; with no `duration` the schedule lasts until cleared or replaced. See the [OCPP 2.1 Smart Charging deltas deep-dive](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md) for dynamic-profile mechanics.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [UpdateDynamicSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule), [PullDynamicScheduleUpdate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate)

### K29 — Dynamic charging profiles from external system
New in OCPP 2.1: a `Dynamic` profile whose `limit`/`setpoint` is updated not by the CSMS but by an external system, signalled with `operationMode = ExternalLimits` or `ExternalSetpoint`. In the first scenario the station itself originates the dynamic profile as a `ChargingStationExternalConstraints` profile fed by the external system, applies each new value as it arrives, and notifies the CSMS via `NotifyChargingLimit` (as in [K11](#k11--set--update-external-charging-limit-with-ongoing-transaction)) when it shifts by more than `LimitChangeSignificance`. In the second, the CSMS pre-authorizes external control by sending a `TxProfile`/`TxDefaultProfile` whose period has `operationMode = ExternalLimits`/`ExternalSetpoint`, telling the station an external system will supply the values; this is the path used when `ExternalConstraintsProfileDisallowed` is true and the station is not permitted to create its own `ChargingStationExternalConstraints` profile. As with [K28](#k28--dynamic-charging-profiles-from-csms), an unrefreshed schedule expires after its `duration` and falls back to the next valid profile.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyChargingLimit](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifycharginglimit)

> **ESCALATE: VENDOR-CONFIG** — Whether the station or the CSMS owns the externally driven profile (governed by `ExternalConstraintsProfileDisallowed`) and the external-system interface are deployment/policy decisions.

---

## L. Firmware Management

### L01 — Secure Firmware Update

The CSMS schedules a signed firmware upgrade by sending an `UpdateFirmwareRequest` that carries the download URI, a scheduled retrieval time, the manufacturer signing certificate, and a digital signature. The charging station waits until the scheduled time, downloads the image, verifies the certificate chain against the installed manufacturer root, and then validates the firmware signature before installing. Each phase is reported back through `FirmwareStatusNotification`: Downloading → Downloaded → SignatureVerified → Installing → Installed. If certificate validation fails the station reports `InvalidCertificate` and also emits a `SecurityEventNotification`; a signature mismatch yields `InvalidSignature` with the same security event, and the upgrade is aborted in both cases.

**Messages:** [UpdateFirmwareRequest](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#updatefirmware), [FirmwareStatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#firmwarestatusnotification)

### L02 — Non-Secure Firmware Update

The CSMS schedules a firmware upgrade without requiring a manufacturer certificate or digital signature. The `UpdateFirmwareRequest` carries only the download URI and a scheduled retrieval time; the charging station downloads and installs the image without any cryptographic verification step. Progress is reported through `FirmwareStatusNotification` with states Downloading → Downloaded → Installing → Installed (the `SignatureVerified` state does not appear because no signature check is performed). This variant is intended for deployments that rely on transport-layer security alone rather than end-to-end firmware signing.

**Messages:** [UpdateFirmwareRequest](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#updatefirmware), [FirmwareStatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#firmwarestatusnotification)

> **ESCALATE: SECURITY-POLICY** — Choosing between secure (L01) and non-secure (L02) firmware update is a CSO security-policy decision; operators must decide which update path is permitted in their deployment.

### L03 — Publish Firmware file on Local Controller

When a fleet of charging stations shares a Local Controller on a common LAN, the CSMS can reduce WAN traffic by pre-staging the firmware on the controller. The CSMS sends a `PublishFirmwareRequest` to the Local Controller specifying the remote firmware URI, an MD5 checksum, and an optional retry count. The controller downloads the file, verifies the MD5 checksum, and then makes the image available over HTTP/HTTPS/FTP on the local network. Each phase is reported to the CSMS via `PublishFirmwareStatusNotification` with states Downloading → Downloaded → ChecksumVerified → Published; failure paths yield DownloadFailed, InvalidChecksum, or PublishFailed. Once the status reaches Published, the notification includes the local URI(s) so the CSMS can redirect individual charging stations to the on-site copy using L01 or L02.

**Messages:** [PublishFirmwareRequest](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#publishfirmware), [PublishFirmwareStatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#publishfirmwarestatusnotification)

### L04 — Unpublish Firmware file on Local Controller

Once a staged firmware image is no longer needed, the CSMS can remove it from the Local Controller by sending an `UnpublishFirmwareRequest` identified by the MD5 checksum of the image. The controller removes the file and responds with `UnpublishFirmwareResponse`; the status is `Unpublished` on success, `NoFirmware` if no matching file was found, or `Downloading` if a charging station is currently retrieving that image — in the last case the controller deliberately withholds deletion to avoid interrupting an in-progress update.

**Messages:** [UnpublishFirmwareRequest](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md#unpublishfirmware)

---

## M. Certificate Management

### M01 — Certificate installation EV

When an EV supporting ISO 15118 PnC connects and requests a new contract certificate, the charging station intercepts the `CertificateInstallationReq` from the EV and forwards it to the CSMS as a `Get15118EVCertificateRequest` with `action = Install`. The CSMS contacts the appropriate contract certificate pool, assembles the `CertificateInstallationRes` payload, and returns it in `Get15118EVCertificateResponse`. The charging station relays the response to the EV, completing the contract certificate installation without the CSMS needing a direct channel to the vehicle. For ISO 15118-20 sessions the message also carries a `maximumContractCertificateChains` field so the EV can batch-install multiple contracts in a single connection.

**Messages:** [Get15118EVCertificate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#get15118evcertificate)

> **ESCALATE: PKI-INTEGRATION** — Which contract certificate pool(s) the CSMS queries and how the CSMS integrates with external provisioning services are operator/back-end design decisions.

### M02 — Certificate Update EV

When an already-provisioned EV detects that its contract certificate is approaching expiry and sends a `CertificateUpdateReq` (ISO 15118-2) or a `CertificateInstallationReq` (ISO 15118-20), the charging station forwards the request to the CSMS as a `Get15118EVCertificateRequest` with `action = Update`. The CSMS retrieves the refreshed certificate payload and returns it via `Get15118EVCertificateResponse`, which the charging station passes back to the EV to replace the expiring certificate. ISO 15118-20 does not distinguish install from update at the protocol level, so the charging station falls back to the M01 flow in that case.

**Messages:** [Get15118EVCertificate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#get15118evcertificate)

### M03 — Retrieve list of available certificates from a Charging Station

The CSMS requests an inventory of certificates currently installed in a charging station's trust store by sending `GetInstalledCertificateIdsRequest` with an optional `certificateType` filter. The charging station computes hash data for each matching certificate and returns them in `GetInstalledCertificateIdsResponse`; if no certificates match the filter the response status is `NotFound`. For V2G certificate chains, sub-CA certificates are nested as child entries under the EVSE leaf certificate in the response. The CSMS uses this information to track which roots, intermediate CAs, and leaf certificates are present before deciding whether to install or delete.

**Messages:** [GetInstalledCertificateIds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getinstalledcertificateids)

### M04 — Delete a specific certificate from a Charging Station

The CSMS removes an individual certificate from a charging station's trust store by sending `DeleteCertificateRequest` with the hash data identifying the target certificate. The charging station attempts deletion and responds with `DeleteCertificateResponse`: `Accepted` on success, `NotFound` if the certificate is not present, or `Failed` if deletion is refused (for example, because it is the last certificate of its type or because it is the station's own TLS identity certificate, which cannot be removed via this path). When deleting a sub-CA or root, the charging station may also remove dependent child certificates.

**Messages:** [DeleteCertificate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#deletecertificate)

> **ESCALATE: LIFECYCLE-POLICY** — The decision about when to remove a root or intermediate CA (e.g., during rotation vs. immediate removal) and whether to allow deletion of the last certificate of a given type is an operator policy decision.

### M05 — Install CA certificate in a Charging Station

The CSMS pushes a new root or intermediate CA certificate into a charging station's trust store by sending `InstallCertificateRequest` with the certificate type (CSMS root, MO root, V2G root, Manufacturer root, or others) and the DER-encoded certificate. The charging station validates and installs the certificate and responds with `InstallCertificateResponse`: `Accepted` on success, `Failed` on installation error, or `Rejected` if the certificate store capacity limit would be exceeded. When the `AdditionalRootCertificateCheck` configuration flag is active and a new CSMS root is installed, the existing root is temporarily retained as a fallback to avoid losing connectivity during a root rotation.

**Messages:** [InstallCertificate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#installcertificate)

> **ESCALATE: ROOT-ROTATION** — The timing and sequencing of CSMS root certificate rotation (including whether to use the fallback mechanism) is an operational procedure that must be coordinated between the CSO and the CSMS operator.

### M06 — Get V2G Charging Station Certificate status

ISO 15118 requires the charging station to include OCSP stapling information for its own V2G certificate during the TLS handshake with an EV, but querying an OCSP responder inline is too slow. To satisfy this constraint the charging station periodically fetches and caches the revocation status in advance by sending `GetCertificateStatusRequest` to the CSMS with the OCSP request data for each relevant sub-CA certificate. The CSMS contacts the appropriate OCSP responder, wraps the DER-encoded ASN.1 response, and returns it in `GetCertificateStatusResponse`. The charging station caches the result and refreshes it at least once a week or immediately after installing a new V2G certificate.

**Messages:** [GetCertificateStatus](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getcertificatestatus)

### M07 — Get Vehicle Certificate Chain Revocation Status

New in OCPP 2.1, this use case allows a charging station to verify the revocation status of the full vehicle certificate chain presented by an EV during a PnC session without the station needing direct access to external OCSP responders or CRL distribution points. The station sends `GetCertificateChainStatusRequest` with a list of certificate entries, each specifying hash data, the check source (OCSP or CRL), and the relevant URL(s). The CSMS checks its local cache first (valid for up to one week per ISO 15118-20) and only performs external lookups for entries not already cached; it responds with `GetCertificateChainStatusResponse` containing the status (Good/Revoked/Failed) and a `nextUpdate` timestamp for each certificate. The station caches these results locally and avoids repeat queries for entries whose `nextUpdate` has not expired.

**Messages:** [GetCertificateChainStatus](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md#getcertificatechainstatus)

---

## N. Diagnostics

### N01 — Retrieve Log Information

The CSMS asks a charging station to upload a log file to a given location by sending `GetLogRequest`, naming a log type (`DiagnosticsLog`, `SecurityLog`, or — new in OCPP 2.1 — `DataCollectorLog`) and an upload URL whose scheme also selects the transfer protocol. The station replies with `GetLogResponse` (`Accepted` with the file name it will use, `Rejected` if no matching log is available, or `AcceptedCanceled` if a new request supersedes an in-progress upload). It then drives the transfer asynchronously, emitting `LogStatusNotificationRequest` messages — `Uploading`, then `Uploaded`, or a failure status such as `UploadFailure`/`PermissionDenied` — all carrying the same `requestId` as the originating request. The file format is unspecified; HTTP(S) is the recommended transport, redirects must not be followed, and basic-auth credentials may be embedded in the URL userinfo. The `DataCollectorLog` type bulk-retrieves high-frequency measurand samples buffered by the DataCollector component, far cheaper than installing a sampling monitor.

**Messages:** [GetLog](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getlog), [LogStatusNotification](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#logstatusnotification)

> **ESCALATE: BACKEND-INTEGRATION** — The upload endpoint, its transfer protocol, and credential handling (the spec recommends a different basic-auth password than the OCPP connection, and the log store may live outside the CSMS trust chain) are operator/back-end design decisions.

### N02 — Get Monitoring report

The CSMS retrieves the monitoring settings currently configured on a charging station by sending `GetMonitoringReportRequest`, optionally narrowed by `monitoringCriteria` (threshold, delta, or periodic monitors) and/or a list of `componentVariables`. The station answers `GetMonitoringReportResponse` with `Accepted`, `NotSupported` (for unsupported criteria), or `EmptyResultSet`, then streams the data back in one or more `NotifyMonitoringReportRequest` messages, each carrying the originating `requestId` and an incrementing `seqNo` starting at 0. Component-variable filtering follows the same wildcard expansion rules used elsewhere in the device model (a missing variable, instance, or connector matches all). In OCPP 2.1 each reported monitor also includes its `eventNotificationType`. The per-message item count is bounded by `ItemsPerMessageGetReport`.

**Messages:** [GetMonitoringReport](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getmonitoringreport), [NotifyMonitoringReport](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifymonitoringreport)

### N03 — Set Monitoring Base

The CSMS activates a preconfigured set of monitors on a charging station by sending `SetMonitoringBaseRequest` with a `monitoringBase` of `All`, `FactoryDefault`, or `HardWiredOnly`; the station replies `SetMonitoringBaseResponse` with `Accepted` or `NotSupported`. `HardWiredOnly` disables all preconfigured monitors and removes custom ones, leaving only firmware hard-wired monitors. `FactoryDefault` reactivates the manufacturer's preconfigured monitors and removes all custom monitors. `All` activates preconfigured monitors while preserving existing custom monitors (including custom monitors created by overriding a preconfigured one). Which concrete monitors each base maps to is defined by the manufacturer.

**Messages:** [SetMonitoringBase](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setmonitoringbase)

### N04 — Set Variable Monitoring

The CSMS installs monitoring triggers on individual variables by sending `SetVariableMonitoringRequest` with a list of `SetMonitoringData` elements, each defining a monitor type — `UpperThreshold`, `LowerThreshold`, `Delta`, `Periodic`, `PeriodicClockAligned`, and (new in 2.1) `TargetDelta`/`TargetDeltaRelative` — a value, and a severity. The station returns `SetVariableMonitoringResponse` with one `SetMonitoringResult` per requested element, reporting per-monitor status: `Accepted` (with a station-generated `id` when none was supplied), `UnknownComponent`, `UnknownVariable`, `UnsupportedMonitorType`, `Duplicate` (a same-type, same-severity monitor already exists on the variable), or `Rejected` (e.g. threshold value outside the variable's min/max, a negative or zero Delta, an attempt to alter a hard-wired monitor, or a conflict with safety monitoring). Supplying an existing `id` replaces that monitor, provided the component/variable still matches; a replaced preconfigured monitor becomes a custom monitor. Monitors persist across reboot and survive firmware updates as long as the variable remains monitor-able. Batch limits come from `ItemsPerMessageSetVariableMonitoring`/`BytesPerMessageSetVariableMonitoring`.

**Messages:** [SetVariableMonitoring](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setvariablemonitoring)

### N05 — Set Monitoring Level

To limit how much monitoring traffic a charging station reports, the CSMS sends `SetMonitoringLevelRequest` with a severity threshold; the station answers `SetMonitoringLevelResponse` with `Accepted` or `Rejected` (severity out of range). Once set, the station only raises `NotifyEventRequest` for monitors whose severity number is less than or equal to the configured level (lower numbers mean higher severity), suppressing less-important events — useful when the communications link must be conserved.

**Messages:** [SetMonitoringLevel](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setmonitoringlevel)

### N06 — Clear / Remove Monitoring

The CSMS removes one or more monitors by sending `ClearVariableMonitoringRequest` with a list of monitor `id`s; the station replies `ClearVariableMonitoringResponse` with a `clearMonitoringResult` per id: `Accepted`, `NotFound` (no such id), or `Rejected` (the monitor cannot be cleared — e.g. a hard-wired monitor). The number of ids per request is bounded by `ItemsPerMessageClearVariableMonitoring`/`BytesPerMessageClearVariableMonitoring`; exceeding either may draw a `CALLERROR` (`OccurenceConstraintViolation` or `FormatViolation`).

**Messages:** [ClearVariableMonitoring](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#clearvariablemonitoring)

### N07 — Alert Event

When a threshold or delta monitor trips, the charging station reports it to the CSMS with `NotifyEventRequest`, including only the component/variable/`variableMonitoringId` combinations responsible for the event and the trigger reason (`Alerting` for thresholds and the new `TargetDelta`/`TargetDeltaRelative` types, `Delta` for delta monitors). When a monitored value returns within bounds the station sends a follow-up event with `cleared = true`. The CSMS always answers with an empty `NotifyEventResponse`. Events at or below `OfflineMonitoringEventQueuingSeverity` are queued while the station is offline and delivered on reconnect; higher-severity events triggered while offline may be dropped, so the CSMS must tolerate a `cleared` notification for a condition whose onset it never saw. In OCPP 2.1, hard-wired notifications carry an implementation-defined severity, and threshold modifications/removals have explicit rules for whether a `cleared` event is emitted.

**Messages:** [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent)

### N08 — Periodic Event

For monitors of type `Periodic` or `PeriodicClockAligned`, the charging station emits `NotifyEventRequest` at the configured cadence with `trigger = Periodic`, rather than waiting for a threshold breach. `Periodic` counts seconds from when the monitor was set or last fired; `PeriodicClockAligned` aligns to wall-clock boundaries (e.g. a value of 900 fires at :00, :15, :30, :45 each hour). The first or only report part has `seqNo = 0`, the CSMS responds with an empty `NotifyEventResponse`, and offline queuing follows the same `OfflineMonitoringEventQueueingSeverity` rule as N07. For high-frequency periodic monitors the more efficient event-stream mechanism of N11–N15 is preferred.

**Messages:** [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent)

### N09 — Get Customer Information

To satisfy privacy requests, the CSMS retrieves the raw data a charging station holds about a customer by sending `CustomerInformationRequest` with `report = true` and exactly one customer reference — an `idToken`, a `customerCertificate`, or a free-form `customerIdentifier`. The station answers `CustomerInformationResponse` with `Accepted`, `Rejected` (cannot process now), or `Invalid` (zero or more than one reference supplied), then returns the data in one or more `NotifyCustomerInformationRequest` messages (an empty `data` string if nothing is stored), each acknowledged by `NotifyCustomerInformationResponse`. When referencing by certificate, the CSMS must use the same hash algorithm that was used to install it.

**Messages:** [CustomerInformation](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#customerinformation), [NotifyCustomerInformation](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifycustomerinformation)

### N10 — Clear Customer Information

This is the erasure counterpart to N09: the CSMS sends `CustomerInformationRequest` with `clear = true` (and `report` either true or false) plus a single customer reference. The station responds `CustomerInformationResponse` (`Accepted`/`Rejected`) and then removes all data it holds about that customer **except** the Local Authorization List — which only the CSMS may change, via `SendLocalListRequest` (see D01) to avoid version conflicts. If `report = true` the cleared data is streamed back in `NotifyCustomerInformationRequest` messages (or one message indicating no data was found); if `report = false` a single notification confirms the data was cleared. Setting both `report` and `clear` to false should be rejected. As with N09, certificate references must use the install-time hash algorithm.

**Messages:** [CustomerInformation](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#customerinformation), [NotifyCustomerInformation](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifycustomerinformation)

> **ESCALATE: PRIVACY-POLICY** — Which data items constitute "customer related data," how erasure is enforced across back-end systems, and how the resulting Local Authorization List update is coordinated are operator/legal-compliance decisions.

### N11 — Set Frequent Periodic Variable Monitoring

New in OCPP 2.1, this use case sets up an efficient "event stream" for monitors expected to fire frequently (typically `Periodic`/`PeriodicClockAligned`, but also frequent `Delta` monitors), so that many values can be batched into a single unconfirmed message instead of one `NotifyEventRequest` each. In the CSMS-driven path, `SetVariableMonitoringRequest` carries a `periodicEventStream` element (with `interval` and/or `values` flush parameters) per monitor; after responding with `SetVariableMonitoringResponse`, the station opens a stream for each such monitor by sending `OpenPeriodicEventStreamRequest` (the constant per-monitor data plus the `variableMonitoringId`), which the CSMS accepts or rejects via `OpenPeriodicEventStreamResponse`. A station may also open a stream on its own for hard-wired or preconfigured periodic monitors. The CSMS associates the stream's static fields (variableMonitoringId, trigger=Periodic, eventNotificationType, severity, component, variable) with subsequent stream data. If the CSMS rejects the stream, the station falls back to ordinary `NotifyEventRequest` reporting. See the [Periodic Event Stream Lifecycle](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md#5-periodic-event-stream-lifecycle) sequence and the [Smart Charging deltas](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md) doc.

**Messages:** [SetVariableMonitoring](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setvariablemonitoring), [OpenPeriodicEventStream](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#openperiodiceventstream), [NotifyPeriodicEventStream](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream)

### N12 — Get Periodic Event Streams

New in OCPP 2.1, this lets the CSMS recover its inventory of open event streams — needed only if it has lost track of them. The CSMS sends `GetPeriodicEventStreamRequest` (no parameters) and the station replies `GetPeriodicEventStreamResponse` with a list of zero or more `ConstantStreamData` entries, one per currently open stream.

**Messages:** [GetPeriodicEventStream](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#getperiodiceventstream)

### N13 — Close Periodic Event Streams

New in OCPP 2.1, this terminates an event stream. The charging station may close a stream at any time: it first flushes all buffered values, then sends `ClosePeriodicEventStreamRequest` with the stream `id` (acknowledged by `ClosePeriodicEventStreamResponse`) and reverts to ordinary `NotifyEventRequest` reporting for that variable. Closing is normally a consequence of the CSMS removing the monitor: a `ClearVariableMonitoringRequest` (N06) that clears a monitor backed by a stream, or a `SetVariableMonitoringRequest` that replaces the monitor without a `periodicEventStream` element, automatically closes the associated stream. See the [Periodic Event Stream Lifecycle](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md#5-periodic-event-stream-lifecycle) sequence.

**Messages:** [ClosePeriodicEventStream](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#closeperiodiceventstream), [ClearVariableMonitoring](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#clearvariablemonitoring), [SetVariableMonitoring](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#setvariablemonitoring)

### N14 — Adjust Periodic Event Streams

New in OCPP 2.1, this lets the CSMS retune how often a stream flushes without tearing it down. The CSMS sends `AdjustPeriodicEventStreamRequest` with the stream `id` and a `params` object carrying new `interval` and/or `values` values; the station answers `AdjustPeriodicEventStreamResponse` with `Accepted` (and changes its `NotifyPeriodicEventStream` cadence accordingly) or `Rejected` if it cannot comply. This pairs with N15.FR.05, where a growing `pending` count signals the CSMS to consider larger or more frequent messages.

**Messages:** [AdjustPeriodicEventStream](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#adjustperiodiceventstream)

### N15 — Periodic Event Streams

New in OCPP 2.1, this describes the actual data transfer over an open stream. As a monitor produces values, the charging station buffers each with a timestamp and flushes the buffer once `params.interval` seconds have elapsed since the last flush or once `params.values` values have accumulated, writing them as a `NotifyPeriodicEventStream` message. This message uses the new RPC "SEND" message type — it is unconfirmed: the CSMS does not return a `CALLRESULT`/`CALLERROR`, which allows the station to send without waiting and greatly reduces overhead. Each message carries a `basetime` set to the timestamp of its first value (so that value's offset `t` is 0), a list of `StreamDataElement` entries (value `v` and time offset `t`), and a `pending` count of values buffered but not yet sent. The CSMS recombines this with the monitor's static data (variableMonitoringId, trigger, eventNotificationType, severity, component, variable) to reconstruct what a `NotifyEventRequest` would have carried; the only absent required field, `eventId`, may be assigned any value since it is never sent back. Because there is no reply, the CSMS cannot signal errors over the stream — its only recourse is to clear the associated monitor (N06/N13). See the RPC SEND framing in [Part 4 / the Sequences doc](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md#5-periodic-event-stream-lifecycle).

**Messages:** [NotifyPeriodicEventStream](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyperiodiceventstream)

---

## O. Display Message

### O01 — Set DisplayMessage

The CSMS pushes a custom message to a charging station's display by sending `SetDisplayMessageRequest` with a unique ID, the message content (optionally in multiple languages via the `messageExtra` field), a priority (NormalCycle, InFront, or AlwaysFront), an optional display state, optional start/end time window, and an optional target display identifier for stations with multiple screens. The charging station stores the message persistently so it survives power cycles, and responds `Accepted` or rejects with a specific status code such as `NotSupportedPriority`, `NotSupportedState`, `NotSupportedMessageFormat`, `LanguageNotSupported` (when `DisplayMessageLanguage` is configured and the message language is not in the allowed list), or `Rejected` when the station's message capacity is full. In OCPP 2.1, the `DisplayMessageLanguage` configuration variable governs which language tags are accepted, and multi-display targeting is supported via the `display` element in `MessageInfoType`. Language tags must conform to RFC 5646.

**Messages:** [SetDisplayMessage](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#setdisplaymessage)

> **ESCALATE: DISPLAY-POLICY** — Which priorities, states, and message formats a station supports, and what maximum message count is configured, are vendor/operator configuration decisions.

### O02 — Set DisplayMessage for Transaction

When a CSO wants to show a message on the display only while a specific transaction is active, the CSMS sends `SetDisplayMessageRequest` with the relevant `transactionId` included in the message object. Behaviour is otherwise identical to O01 — the charging station stores and displays the message according to its priority and timing parameters — but with the additional rule that the message is automatically discarded as soon as the referenced transaction ends. If the charging station does not recognise the supplied transaction ID it immediately responds `UnknownTransaction`. This prevents orphaned messages from remaining on screen after a session has closed.

**Messages:** [SetDisplayMessage](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#setdisplaymessage)

### O03 — Get All DisplayMessages

The CSMS retrieves the complete list of OCPP-configured messages currently stored in a charging station by sending `GetDisplayMessagesRequest` with all filter fields omitted (i.e. requesting everything). The station responds immediately with `GetDisplayMessagesResponse` — `Accepted` if at least one message is configured, `Unknown` if none are present — and then streams the full message inventory in one or more `NotifyDisplayMessagesRequest` batches. When the list spans multiple batches, the `tbc` (to be continued) flag is set to `true` on all but the last `NotifyDisplayMessages` message. The `requestId` field ties all notifications back to the original query. Only messages that were set via OCPP can be retrieved; firmware-built-in messages are not visible through this flow.

**Messages:** [GetDisplayMessages](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#getdisplaymessages), [NotifyDisplayMessages](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#notifydisplaymessages)

### O04 — Get Specific DisplayMessages

The CSMS queries a subset of OCPP-configured messages by sending `GetDisplayMessagesRequest` with one or more filter fields populated (e.g., message ID, priority, or state). The charging station checks whether any stored messages match the supplied criteria: if matches exist it responds `Accepted` and delivers the results in one or more `NotifyDisplayMessagesRequest` messages using the same batching and `tbc` mechanism as O03; if no messages match the filter the station responds `Unknown` and sends no notifications. This use case is useful for confirming that a specific message is still active or for auditing messages by priority class without pulling the entire list.

**Messages:** [GetDisplayMessages](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#getdisplaymessages), [NotifyDisplayMessages](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#notifydisplaymessages)

### O05 — Clear a DisplayMessage

The CSMS removes a specific OCPP-managed message from a charging station by sending `ClearDisplayMessageRequest` with the numeric ID of the message to remove. The charging station deletes the matching message and responds with `ClearDisplayMessageResponse`: `Accepted` if the message was found and removed, `Unknown` if no message with that ID exists, or `Rejected` (added in OCPP 2.1) if the station is unable to process the request. Only messages that were originally installed via OCPP can be cleared through this mechanism; firmware-resident messages are unaffected.

**Messages:** [ClearDisplayMessage](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#cleardisplaymessage)

### O06 — Replace DisplayMessage

When the CSMS needs to update the content or parameters of a message that already exists on a charging station, it sends a `SetDisplayMessageRequest` reusing the same message ID as the message to be replaced. The charging station matches the incoming ID to the stored message, replaces both the content and all parameters (priority, state, timing, language, etc.) atomically with the new values, and responds `Accepted`. This differs from O01 in that a pre-existing entry with the same ID is a prerequisite; the use case avoids having to delete-then-re-add when refreshing a message.

**Messages:** [SetDisplayMessage](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md#setdisplaymessage)

---

## P. Data Transfer

### P01 — Data Transfer to the Charging Station

When the CSMS needs to exchange information with a charging station for a function that falls outside the standardised OCPP message set, it sends `DataTransferRequest` to the station carrying a `vendorId` (a reversed-DNS name uniquely identifying the vendor), an optional `messageId` indicating the specific operation, and an optional free-form `data` payload. The charging station processes the request according to the bilateral agreement with the CSMS vendor and responds with `DataTransferResponse`; if it has no implementation for the specified `vendorId` it must respond `UnknownVendor`, and a `messageId` mismatch yields `UnknownMessageId`. The `Accepted` or `Rejected` meaning of the response status, and the structure of the `data` field, are entirely vendor-specific. Data Transfer is not intended for standard production use and the spec strongly cautions that it risks interoperability with systems that do not support the same extension.

**Messages:** [DataTransfer](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DataTransfer.md#datatransfer)

> **ESCALATE: VENDOR-EXTENSION** — The `vendorId`, `messageId`, and `data` semantics are a bilateral vendor agreement and must be documented separately outside of OCPP; the decision to use Data Transfer at all is a deployment/architecture policy choice.

### P02 — Data Transfer to the CSMS

The mirror of P01: when a charging station needs to send information to the CSMS for a function not covered by standard OCPP, it initiates `DataTransferRequest` with its own `vendorId`, an optional `messageId`, and an optional `data` payload. The CSMS responds with `DataTransferResponse`; if it has no implementation for the `vendorId` it responds `UnknownVendor`. As with P01, the interpretation of `Accepted`/`Rejected` and the `data` content are governed entirely by the vendor-specific bilateral agreement, and the payload length is undefined and should be agreed upon by both parties in advance.

**Messages:** [DataTransfer](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DataTransfer.md#datatransfer)

> **ESCALATE: VENDOR-EXTENSION** — Same bilateral vendor agreement requirement as P01; payload length limits should be agreed between the charging station and CSMS vendor before deployment.

---

## Q. Bidirectional Power Transfer (V2X)

> Block Q introduces bidirectional power transfer (V2X) — the EV exporting energy back to the grid as well as importing it. The control surface is the existing smart-charging machinery extended with an `operationMode` field on each charging-schedule period and signed `setpoint`/`dischargeLimit` values. For the conceptual model, the operation-mode catalogue, and how V2X profiles merge with ordinary limits, see the [Bidirectional Power Transfer deep-dive](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) and the [Smart Charging deep-dive](../OCPP-2.1-SmartCharging/OCPP-2.1-SmartCharging.md).

### Q01 — V2X Authorization

When an ISO 15118-20 EV is authorized for bidirectional transfer, the station includes the vehicle's EVCCID in the `idToken.additionalInfo` of `AuthorizeRequest` so the CSMS can decide whether to allow V2X for this vehicle; the CSMS answers with `idTokenInfo.status = Accepted` and an `allowedEnergyTransfer` list naming the permitted transfer types (e.g. `DC_BPT`, `AC_BPT`). The station then opens a transaction and reports the EV's chosen `requestedEnergyTransfer` together with `v2xChargingParameters`, `controlMode` and an optional `departureTime` via `NotifyEVChargingNeeds`; the CSMS accepts (optionally `Processing` while it computes a profile) or rejects, in which case the station either renegotiates a different service with the EV or stops the transaction with `stoppedReason = ReqEnergyTransferRejected`. A V2X-mode charging schedule arrives by `SetChargingProfile` (or a pre-installed `TxDefaultProfile`, signalled by a `NoChargingProfile` response). If the allowed set changes mid-session, the CSMS pushes `NotifyAllowedEnergyTransfer`.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent), [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyAllowedEnergyTransfer](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer)

> **ESCALATE: GRID-MARKET** — Whether a given vehicle (by idToken, EVCCID or vehicle certificate) is permitted to perform V2X, and whether third-party (eMSP/aggregator) authorization must be obtained before granting it, is an operator/market-contract decision outside the protocol.

### Q02 — Starting in operationMode ChargingOnly before enabling V2X

This use case covers the common situation where, at authorization time, the CSMS cannot yet confirm whether V2X is allowed (for example because a third-party permission or the selected EVSE is not yet known). The CSMS accepts the authorization but omits `allowedEnergyTransfer`, and the session begins in `operationMode = ChargingOnly` — an ordinary unidirectional charge with no `setpoint`/`dischargeLimit` fields set. Once the CSMS later decides V2X is permitted (using the EVCCID, vehicle certificate, or idToken it has on file), it sends `NotifyAllowedEnergyTransfer` carrying the transaction id and an updated list that now includes a bidirectional type; the station accepts and triggers an ISO 15118 service renegotiation so the EV can upgrade to the bidirectional service, after which a new `NotifyEVChargingNeeds` reports the upgraded `requestedEnergyTransfer`.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize), [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyAllowedEnergyTransfer](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#notifyallowedenergytransfer)

### Q03 — Central V2X control with charging schedule

The CSMS dictates the EV's charge/discharge behaviour by sending a `TxProfile` or `TxDefaultProfile` whose `chargingSchedule` contains one or more periods with `operationMode = CentralSetpoint` and a (signed) `setpoint` for the active power the EV should import (positive) or export (negative); it may also bound the range with `limit` and `dischargeLimit`. In ISO 15118 Scheduled mode the station hands the schedule to the EV and any change triggers a 15118 renegotiation; in Dynamic mode the station simply applies the period's setpoint at each boundary without renegotiation. For a `Dynamic` profile kind the CSMS can later revise the setpoint with `UpdateDynamicSchedule`. How long the schedule survives an offline period is governed by `maxOfflineDuration`/`invalidAfterOfflineDuration` (see Q11/Q12).

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [UpdateDynamicSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

### Q04 — Central V2X control with dynamic CSMS setpoint

A variant of Q03 in which, instead of a multi-period schedule, the CSMS sends a `Dynamic` profile holding a single `chargingSchedulePeriod` (again `operationMode = CentralSetpoint`) and then steers it in near-real-time with frequent `UpdateDynamicSchedule` messages — suited to following an external dispatch signal. The optional `chargingSchedule.duration` acts as a watchdog: if no update arrives within `duration` seconds of the last `SetChargingProfile`/`UpdateDynamicSchedule`, the schedule expires and the station falls back to the next valid charging profile. As an alternative the station may pull updates itself via `PullDynamicScheduleUpdate` on the configured `dynUpdateInterval`.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [UpdateDynamicSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule), [PullDynamicScheduleUpdate](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#pulldynamicscheduleupdate)

### Q05 — External V2X setpoint control with a charging profile from CSMS

Here the CSMS explicitly delegates real-time control to an External System (e.g. a local EMS) but only inside a window it defines. The CSMS sends a `Dynamic` `TxProfile`/`TxDefaultProfile` whose period carries `operationMode = ExternalSetpoint` (External System drives `setpoint`/`setpointReactive`) or `ExternalLimits` (it drives `limit`/`dischargeLimit`). During that period the station applies values supplied by the external system and stamps `dynUpdateTime` on each change; the configuration variable `ExternalConstraintsProfileDisallowed = true` ensures the external system cannot otherwise impose its own profile. If `chargingSchedule.duration` is set and no external update arrives in time, the profile becomes invalid and the station falls back, regaining validity once a fresh update is received. The transport between the External System and the station is out of OCPP scope.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

> **ESCALATE: VENDOR-EXTENSION** — The communication channel and protocol by which the External System conveys setpoints/limits to the Charging Station is explicitly out of scope of OCPP and is a vendor/integration decision.

### Q06 — External V2X control with a charging profile from an External System

Unlike Q05, here the External System itself owns the profile: it installs a `ChargingStationExternalConstraints` charging profile (possible only when `ExternalConstraintsProfileDisallowed` is false/absent). Three flavours exist — a scheduled list of limits (`Absolute`, `ExternalLimits`), a dynamically-varied single limit (`Dynamic`, `ExternalLimits`), or a dynamically-varied setpoint (`Dynamic`, `ExternalSetpoint`). Because an external system is unaware of individual sessions, such a profile typically targets EVSE #0 (the whole station), which must then divide charge/discharge power across its EVSEs to honour the aggregate `limit`/`dischargeLimit`/`setpoint`. When the profile is set or changes by more than `LimitChangeSignificance`, the station reports it to the CSMS with `NotifyChargingLimit` (`chargingLimitSource = EMS`). When both an external setpoint and a Tx(Default)Profile setpoint are active, `SmartChargingCtrlr.SetpointPriority` resolves which wins.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

> **ESCALATE: VENDOR-EXTENSION** — How the External System delivers its `ChargingStationExternalConstraints` profile to the station is out of OCPP scope; whether external profiles are allowed at all (`ExternalConstraintsProfileDisallowed`) and the `SetpointPriority` tie-break are operator configuration choices.

### Q07 — Central V2X control for frequency support

A specialisation of Q04 for grid frequency regulation when calibrated central frequency measurements are needed. The CSMS sends a `Dynamic` profile with a single period of `operationMode = CentralFrequency` and a `setpoint`, then continuously revises it with `UpdateDynamicSchedule` as it tracks the centrally-measured frequency (usually for an aggregated fleet). `limit`/`dischargeLimit` must not appear in a `CentralFrequency` period, and the CSMS is advised to set a `duration` so the schedule does not run forever if updates stop — at which point the station can fall back to a lower-stack-level `LocalFrequency` profile (Q08). This frequency support is the charging profile's primary purpose, distinct from the grid-code frequency-droop behaviour configured under DER Control (block R).

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [UpdateDynamicSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule)

### Q08 — Local V2X control for frequency support

Frequency support computed locally by the station from its own frequency readings, with no live setpoint from the CSMS. The CSMS sends a `LocalFrequency` schedule carrying a `v2xBaseline` power and a `v2xFreqWattCurve` (at least two points); the station continuously measures grid frequency and sets power to the baseline plus the curve-interpolated value, re-evaluating whenever the frequency moves by `LocalFrequencyUpdateThreshold` mHz. For an aFRR (automatic Frequency Restoration Reserve) service the schedule also includes a `v2xSignalWattCurve`, and the CSMS relays the TSO's dispatch via `AFRRSignal` (a `signal` plus a `timestamp` at which it applies); the station adds that delta on top of the frequency-watt setpoint. The schedule must use `chargingRateUnit = W`, and missing curves are rejected with `NoFreqWattCurve`/`NoSignalWattCurve`.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [AFRRSignal](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md#afrrsignal)

> **ESCALATE: GRID-MARKET** — The frequency-watt and signal-watt curves, the baseline, and the source/meaning of the aFRR signal forwarded to the station are dictated by the TSO/grid-code and market product the operator is participating in.

### Q09 — Local V2X control for load balancing

The station is given a `LocalLoadBalancing` schedule and continuously reads an upstream (building/site) grid meter to keep the measured load between a configured `LowerThreshold` and `UpperThreshold`, modulating the EV's charge/discharge `setpoint` by the computed delta (with optional `UpperOffset`/`LowerOffset` to control permitted overshoot). It rejects the profile with `UnsupportedParam` if `LocalLoadBalancing` is not in `V2XSupportedOperationModes`, or `MissingDevModelInfo` if the threshold/offset variables are unset or inconsistent. The resulting setpoint is capped at `limit`/`dischargeLimit` when those are present. This works for a single station (possibly across its EVSEs); coordinating multiple stations requires a central or local controller using the CentralSetpoint mode instead.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

### Q10 — Idle, minimizing energy consumption

An `operationMode = Idle` schedule period asks the EV to neither charge nor discharge while the session stays connected. Two boolean controls modulate the period: `preconditioning = true` permits the EV to draw some power to keep its battery at an optimal temperature for later charge/discharge, and `evseSleep = true` (only if `SupportsEvseSleep`) lets the station power down the EVSE's electronics for this transaction until an event wakes it (a new period, a new profile — including 0 W limits — or transaction end). While asleep the station reports `evseSleep = true` in `TransactionEvent`. A period with `operationMode = Idle` must not carry any `limit`/`dischargeLimit`/`setpoint`/`setpointReactive`, otherwise the profile is rejected with `InvalidSchedule`.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

### Q11 — Going offline during V2X operation

This use case defines how long a V2X session may continue once the station loses its CSMS connection. The `maxOfflineDuration` field of the active `ChargingProfileType` sets a countdown that starts the moment the station detects it is offline; when it elapses the station reverts to the next valid (lower stack-level) profile — which may itself be another V2X profile if its own `maxOfflineDuration` has not run out, or ultimately a `ChargingOnly` fallback or unlimited charging if nothing remains. The CSMS should simply assume the V2X operation has reverted on detecting the outage rather than trying to predict the exact instant, since the two sides notice the disconnection at different times. Profiles with `invalidAfterOfflineDuration = true` whose window has elapsed are not reactivated on reconnection. The requirements are those of K01's `maxOfflineDuration`.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

### Q12 — Resuming a V2X operation after an offline period

The mirror of Q11, describing the state on reconnection. If the offline interval was shorter than the V2X profile's `maxOfflineDuration`, the profile stayed active throughout and nothing changes when the link returns. If it was longer, the profile had already expired while offline and the station has been running on the next valid (lower stack-level) profile — for instance reverting from a `CentralSetpoint` V2X profile at stack level #2 to a `ChargingOnly` profile at level #1; whether it can be resumed depends on `invalidAfterOfflineDuration`. On reconnection the CSMS can re-establish the desired V2X mode by re-sending or updating the relevant charging profile.

**Messages:** [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [UpdateDynamicSchedule](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#updatedynamicschedule)

---

## R. DER Control

> Block R covers Distributed Energy Resource (DER) controls — grid-code behaviours such as Volt-Watt and Volt-Var curves, frequency droop, ride-through (must-trip / may-trip) and discharge-power limits — that a utility mandates for bidirectional sessions to protect the grid. These satisfy grid-code obligations and are conceptually separate from the V2X frequency-support use cases of block Q. For the control catalogue, curve types, default-vs-scheduled priority model and alarm semantics, see the [DER Control deep-dive](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md). The DER control may be enforced by the inverter in the EVSE, by the inverter in the EV, or split between them.

### R01 — Starting a V2X session with DER control in EVSE

When the inverter sits in the EVSE — always the case for DC (ISO 15118-20 `DC_BPT`, CHAdeMO) and possible for AC `AC_BPT` where the station controls the EV's power via the charge loop — the station enforces the utility's DER controls itself and the EV needs no DER configuration. Beforehand the CSMS installs the controls (e.g. a `VoltWatt` curve and a `LimitMaxDischarge` of 50 %) with `SetDERControl`, which the station must store persistently; a DC station exposes its inverter nameplate capabilities in the `DCDERCtrlr` component (reportable via the device model). The bidirectional session then proceeds as an ordinary V2X transaction (`NotifyEVChargingNeeds` → `SetChargingProfile` `TxProfile`), with the station continuously applying the curves and discharge limit during the charge loop.

**Messages:** [SetDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol), [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile)

> **ESCALATE: GRID-MARKET** — Which DER controls (curves, droop parameters, discharge limits) apply and their values are dictated by the utility/grid code for the station's region, not by the protocol.

### R02 — Starting a V2X session with DER control in EV

For an AC `AC_BPT_DER` session the inverter is inside the EV and the station cannot operate it directly; instead the station passes the DER controls down to the EV to execute. The CSMS still installs the controls with `SetDERControl` (persisted by the station), but because they are not listed in `ACDERCtrlr.ModesSupported` the station forwards them to the EV during ISO 15118-20 `ChargeParameterDiscovery`, and reports the EV inverter's nameplate and supported-control list to the CSMS in the `derChargingParameters` of `NotifyEVChargingNeeds`. When a control acts on the session (e.g. a high-frequency trip or a discharge-power cap), the EV signals the station via the 15118 DERAlarm element and the station forwards it to the CSMS with `NotifyDERAlarm`.

**Messages:** [SetDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol), [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyDERAlarm](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm)

> **ESCALATE: GRID-MARKET** — The set of DER controls the EV must support for `AC_BPT_DER` (advertised via `DERControlFunctions` in service negotiation) and their values reflect the utility's grid-code requirements.

### R03 — Starting a V2X session with hybrid DER control in both EV and EVSE

A blend of R01 and R02 for `AC_BPT_DER` sessions where the EV's inverter supports only some of the required controls. The station advertises the controls it can emulate locally (via the charge loop) in `ACDERCtrlr.ModesSupported`; for those it can emulate it may omit them from the 15118 `AC_BPT_DER` service negotiation, letting an EV with a less-capable inverter still participate. Controls the EV does support are configured in the EV (the station does not emulate what the EV can do natively), while the remainder are enforced by the station. As in R02 the station persists the `SetDERControl` settings, reports EV nameplate data in `NotifyEVChargingNeeds`, and raises `NotifyDERAlarm` whenever any control — whether executed by EV or EVSE — affects the session.

**Messages:** [SetDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol), [NotifyEVChargingNeeds](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#notifyevchargingneeds), [SetChargingProfile](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md#setchargingprofile), [NotifyDERAlarm](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm)

### R04 — Configure DER control settings at Charging Station

The management workflow for DER controls. The CSMS configures a control with `SetDERControl`, marking it either a default (`isDefault = true`, no `startTime`/`duration`, takes effect immediately) or a scheduled control (`isDefault = false`, with a `startTime`/`duration`). Each `controlType` (e.g. `FreqDroop`, `VoltVar`, `VoltWatt`, `HFMustTrip`, `HFMayTrip`, `LimitMaxDischarge`, `EnterService`, `Gradients`) must carry exactly its matching control field and, for curve types, the `yUnit` prescribed for that type; `EnterService` and `Gradients` exist only as defaults. Conflicts are resolved by a numeric `priority` (lower value wins): a higher-priority new control supersedes the existing one (which gets `isSuperseded = true` and is named via `supersededId`), while a lower-priority new control is itself immediately superseded. The station deletes scheduled controls after `startTime + duration`, reverts to the default when no scheduled control is active, and reports start/stop of scheduled controls with `NotifyDERStartStop`. The CSMS reads back configured controls with `GetDERControl` (filtering by `isDefault`/`controlType`/`controlId`), which the station answers with one or more paged `ReportDERControl` messages (`tbc` flag set on all but the last), and removes them with `ClearDERControl`.

**Messages:** [SetDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#setdercontrol), [GetDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#getdercontrol), [ReportDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#reportdercontrol), [ClearDERControl](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#cleardercontrol), [NotifyDERStartStop](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderstartstop)

> **ESCALATE: GRID-MARKET** — The DER programs, curve points, droop parameters and their relative priorities originate from the utility/grid code; the CSMS merely relays the highest-priority applicable control to each station.

### R05 — Charging station reporting a DER event

When a grid anomaly forces the station to deviate from the active charging profile because of a DER control — for example an overvoltage that makes a configured `VoltWatt` curve reduce discharge power — the station reports the event once per occurrence with `NotifyDERAlarm`, setting the `controlType` (e.g. `VoltWatt`) and the `gridEventFault` (e.g. `OverVoltage`) together with a `timestamp`. A DC station then lowers discharge power per the curve directly; an AC station instructs the EV via repeated 15118 `AC_ChargeLoop` messages each time the curve value changes. When conditions return to normal the station sends a closing `NotifyDERAlarm` with `alarmEnded = true` and resumes following the charging profile. (Purely reactive-power actions such as Volt-Var are not reported unless they affect the session's active-power profile.)

**Messages:** [NotifyDERAlarm](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md#notifyderalarm)

---

## S. Battery Swapping

> Block S models a battery-swap station (BSS) as an ordinary OCPP Charging Station in which each battery slot is a logical EVSE. The swap dialogue (recording which pack went in and which came out) uses the dedicated `BatterySwap`/`RequestBatterySwap` messages, while the subsequent recharging of the returned packs is plain transaction handling. See the swap event ordering walkthrough in the [Sequences deep-dive](../OCPP-2.1-Sequences/OCPP-2.1-Sequences.md).

### S01 — Battery Swap Local Authorization

The driver authorizes locally at the swap station by presenting an RFID card; the station sends `Authorize` and, on `idTokenInfo.status = Accepted` (and provided enough charged packs are available), opens or indicates the empty slot(s) into which the depleted pack(s) can be inserted. This mirrors ordinary RFID authorization (use case C01), except that the authorization does not start a transaction, so C01's transaction-in-progress rules do not apply. If the driver fails to insert a battery before the `BatterySwapInTimeout` expires, the station ends the authorization and aborts the swap (no `BatterySwap` message having been sent yet); if too few charged packs are on hand, the swap is refused.

**Messages:** [Authorize](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md#authorize)

### S02 — Battery Swap Remote Start

The remote-initiated counterpart of S01: the driver triggers the swap from a smartphone app (e.g. scanning a QR code), and the CSMS — having authorized the token — sends `RequestBatterySwap` carrying the `idToken` and a `requestId`. If enough charged packs are available the station answers `Accepted`; otherwise it returns `Rejected` with `reasonCode = NoBatteryAvailable`. The `requestId` from this request must be reused in the `BatterySwap` events that follow (S03), letting the CSMS correlate the swap with its originating request. As in S01, failure to insert a pack before `BatterySwapInTimeout` aborts the process.

**Messages:** [RequestBatterySwap](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#requestbatteryswap), [BatterySwap](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap)

### S03 — Battery Swap In/Out

This use case records the physical exchange. In the default In-Out order the driver (or swapping machinery) first inserts the depleted pack(s) into empty slot(s), and the station sends `BatterySwap` with `eventType = BatteryIn`, the shared `requestId`, the authorized `idToken`, and a `batteryData` entry per pack (slot `evseId`, `serialNumber`, `SoC`, `SoH`); it then reports each slot's connector as `Occupied` via `NotifyEvent`. The station then offers charged pack(s); when the driver takes them out the station sends a second `BatterySwap` with `eventType = BatteryOut`, the same `requestId` and the data of the extracted pack(s), and reports those slots `Available`. If a charged pack offered after the BatteryIn is not collected within `BatterySwapOutTimeout`, the station sends a `BatterySwap` with `eventType = BatteryOutTimeout` so the CSMS does not retain an orphan BatteryIn with no matching BatteryOut. A station that swaps in the reverse order reports `BatterySwapCtrlr.SwapOrder = Out-In`. The `BatterySwapResponse` has no rejection status, so a CSMS that needs to reject an inserted pack must use the `org.openchargealliance.batteryswapresponse` customData extension.

**Messages:** [BatterySwap](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md#batteryswap), [NotifyEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md#notifyevent), [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)

> **ESCALATE: VENDOR-EXTENSION** — Rejecting an inserted battery requires the bilateral `org.openchargealliance.batteryswapresponse` customData extension (reason codes such as `BatterySoHLow`, `BatteryDamaged`, `BatteryUnknown`); whether a station implements it is a vendor decision flagged via `CustomizationCtrlr.CustomImplementationEnabled`.

### S04 — Battery Swap Charging

After a depleted pack is inserted, the station recharges it as a normal transaction on that slot's logical EVSE. With `TxStartPoint`/`TxStopPoint` configured to `EVConnected`, inserting the pack opens a transaction: `TransactionEvent` with `eventType = Started`, `triggerReason = CablePluggedIn` (meaning the pack was inserted) and either the predefined `BatterySwapIdtoken` (type `Central`) or an empty token (type `NoAuthorization`). The station then sends periodic `TransactionEvent` updates carrying the battery's `SoC` measurand; the pack becomes eligible for swapping at `BatterySwapTargetSoc` and, on reaching `BatterySwapMaxSoc` (which must be ≥ the target), the station suspends energy transfer with `chargingState = SuspendedEVSE` and `triggerReason = EnergyLimitReached`, keeping the transaction alive so charging can resume (e.g. for V2X). Removing the pack ends the transaction (`eventType = Ended`, `stoppedReason = EVDisconnected`). After a reboot the station restarts transactions for every slot still holding a battery. These transaction messages are not tied to the driver's idToken.

**Messages:** [TransactionEvent](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md#transactionevent)
