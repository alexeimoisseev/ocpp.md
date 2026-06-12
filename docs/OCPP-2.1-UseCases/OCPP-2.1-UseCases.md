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
