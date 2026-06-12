# OCPP 2.1 — Certification Profiles Summary (Part 5)

> **Purpose:** Orientation for AI agents and developers on the OCPP 2.1 certification program — what certification profiles are, the profiles defined in Part 5, which functional blocks (A–S) and use cases each profile bundles, the mandatory controller components per profile, and how the new 2.1 functionality (DER control, V2X / bidirectional power transfer, tariff/payment, battery swapping) maps to certification.

> **Last updated:** 2026-06-12

> **NON-NORMATIVE SUMMARY.** This document is an original, paraphrased overview of OCPP 2.1 Part 5 (Certification Profiles). It is **not** the certification specification and is **not** authoritative for any certification decision. The OCA (Open Charge Alliance) certification program — its Part 5 document, the Part 6 test cases, the OCA Compliance Testing Tool, and the OCA-accredited test labs — are the only authoritative sources. Always confirm the current profiles, features, and requirements against the official OCA artifacts and your accredited test lab before relying on anything here. Do not treat this file as a Protocol Implementation Conformance Statement (PICS).

---

## How This Document Was Produced

This document's dominant confidence tier is **spec-knowledge** — an original summary of the OCPP 2.1 Edition 2 Part 5 "Certification Profiles" specification (Edition 2, 2025-12-03, 68 pp). Profile names, the feature lists per profile, the feature→use-case mapping, and the mandatory-controller-component lists are all paraphrased and restructured from Part 5; **no spec prose is reproduced verbatim** (the OCA specification is CC BY-ND licensed). The A–S functional-block taxonomy used in the matrix below is cross-referenced against the mechanically generated [Use-Case Catalog](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md) and the schema block docs.

**Mapping basis (important).** Part 5 does **not** organize requirements by the A–S functional-block letters. It organizes them by **certification profile** and by **optional feature ID** (e.g. `C-01`, `SC-8`, `BPT-1`). Part 5 Appendix C ("Features vs. OCPP use cases") maps each feature ID to the **Part 2 use-case IDs** it touches (e.g. feature `C-30` → use case `C01`). Those use-case IDs carry the A–S block letter as their prefix (use cases `A01…A05` = block A, `C01…C25` = block C, and so on). This document therefore derives the profile → A–S block mapping **transitively**: profile → feature IDs / described functionality → use-case IDs (from Appendix C and the profile tables) → A–S block. Where a profile's functionality is described only in prose (Part 5 Table 1) rather than via a feature ID, the block assignment is inferred from the matching use-case names and is noted as such. This is a non-normative interpretation; the authoritative artifact is the per-test-case condition column in Part 5 Chapter 4.

This document contains **2 escalation points** marked with `> **ESCALATE:**`. When an AI agent encounters one, it MUST stop and ask the developer / product owner to make the decision — certification scope is a business and deployment decision, not a code decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [OCPP 2.1 Overview & Migration Guide](../OCPP-2.1.md) — what is new in 2.1 and how the docs fit together
- [Use-Case Catalog (Part 2)](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md) — the A–S blocks and every use case the profiles reference
- [DER Control Deep-Dive](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md) — block R, certified by the DER control profile
- [Bidirectional Power Transfer (V2X) Deep-Dive](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md) — block Q, certified by the Bidirectional Power Transfer profile
- Schema block references (field-level messages): [Security](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Security.md), [Provisioning](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md), [Authorization](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md), [Transactions](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md), [Smart Charging](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md), [Bidirectional](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md), [DER Control](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md), [Certificates](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md), [Tariff & Cost](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md)
- [Device Model Reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md) — the controller components that must exist for a profile to be testable

---

## 1. What Certification Profiles Are

OCPP supports everything from a simple AC home charger to a megawatt DC charger, so requiring every vendor to implement and pass every OCPP feature would be pointless. The OCA certification program therefore bundles functionality into **certification profiles**: a profile is a named set of OCPP functionality that a charging station or CSMS can be certified against. A vendor certifies for the profiles relevant to its product, not necessarily for all OCPP functionality.

Key facts (paraphrased from Part 5):

| Topic | Summary |
|-------|---------|
| Authoritative body | Certification is performed by **OCA-accredited test labs** using the **OCA Compliance Testing Tool**. The OCA, not this document, defines what passes. |
| Core is mandatory | The **Core** profile must always be present; it contains the basic OCPP functionality. Other profiles are added on top. |
| Profiles are independent | Profiles can be certified independently — **except** ISO 15118 support, which depends on a number of Advanced Security and Smart Charging test cases, and Bidirectional Power Transfer, which has Smart Charging as a prerequisite. |
| "Feature" vs "test case" | Part 5 deliberately avoids marking individual test cases mandatory/optional. Instead it defines optional **features** (often the presence/value of a config variable or an optional message field). A feature maps to one or more test cases; whether the System Under Test (SUT) implements the feature determines whether those test cases must pass. |
| Mandatory vs optional within a profile | Within a profile, some test cases are **M** (Mandatory — must pass if you certify for the profile) and some are **C** (Conditional — must pass only if you implement the related feature). Optional features are listed in Part 5 Chapter 3 (Tables 2 and 3). |
| PICS | The vendor declares supported features and answers additional lab questions (Part 5 Appendices A and B) in a Protocol Implementation Conformance Statement; the test system uses the PICS to select test cases. |

> **ESCALATE: POLICY-DEPENDENT** — *Which* profiles to certify for (and which optional features to implement within them) is a product, market, and commercial decision. Do not infer it from the code. Confirm the target profile set with the product owner and the chosen OCA test lab.

---

## 2. The Profiles Defined in Part 5

These are the **actual** profile names from Part 5 Table 1 (Certification profiles) and Chapter 5 (mandatory controller components). Do not invent others.

| Profile | New in 2.1? | Scope (paraphrased) |
|---------|-------------|---------------------|
| **Core** | No (baseline) | Mandatory baseline. Basic auth & TLS server-side cert, security event notification, boot/configure/reset, authorization (incl. GroupId, master pass), start/stop transaction options, remote start/stop/unlock, TriggerMessage, availability changes, clock-aligned & sampled meter values, certificate install/retrieve, log retrieval, customer information, secure firmware update, authorization-cache management. Core also bundles several named sub-areas — **Local Authorization List Management**, **Advanced Device Management** (monitoring), **Advanced User Interface** (display messages + tariff/cost display), **Reservation**, and the 2.1 **Payment** sub-area. |
| **Advanced Security** | No | TLS **client-side** certificate, update Charging Station certificate, upgrade Charging Station security profile. (Security profile 2/3 functionality on top of Core's basic auth.) |
| **Smart Charging (2.0.1 / 2.1)** | Extended in 2.1 | Set/get/clear charging profile, get composite schedule, remote start with charging profile; **2.1 additions**: priority charging, dynamic charging profiles. Also bundles an **EMS Control** sub-area: dynamic charging profiles driven by an external system, and external V2X control (with and without ISO 15118-20). |
| **ISO 15118 support (2.0.1 / 2.1)** | Extended in 2.1 | Covers ISO 15118-2 (2.0.1 and 2.1) and ISO 15118-20 (2.1). ISO 15118 certificate management (update CS cert, contract cert install/update on EV, get cert status, install/retrieve/delete V2G/MO/OEMRoot CA certs), EIM and Plug-and-Charge (contract certificate) authorization, ISO 15118 smart charging (incl. schedule renegotiation), and ISO 15118 signed meter values. Depends on Advanced Security and Smart Charging test cases. |
| **Bidirectional Power Transfer (2.1)** | **Yes** | Central & local V2X control, frequency support, V2X authorization over ISO 15118-20, idle / minimizing energy consumption. **Prerequisite: the Smart Charging profile.** |
| **DER control (2.1)** | **Yes** | Starting a V2X session with DER control, configuring DER control settings at the CS, and the CS reporting a DER event. |

Notes:
- **Payment (2.1)** appears in Part 5 as a sub-section *within the Core profile* (set default tariff, local cost calculation, prepaid card, integrated/standalone payment terminal, settlement, QR codes), and it has its own mandatory controller components (`Core: P-0 (2.1)`). It is not a separate top-level profile; treat it as an optional Core feature group certified via the `P-*` feature IDs.
- **Battery Swapping** is **not** a standalone certification profile. It is handled as a product **subtype** of a charging station: the `BatterySwapCtrlr` component is mandatory in Core *only for the Battery Swapping Charging Station subtype*, and CSMS feature `C-76 (2.1)` ("Support for Battery Swapping Stations") is optional. See [§4](#4-new-21-functionality-and-how-it-maps-to-certification).

---

## 3. Profile × Functional-Block / Use-Case Matrix

This table maps each certification profile to the A–S functional blocks of the [Use-Case Catalog](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md). Legend: **R** = block is core to (required scope of) the profile; **O** = block is touched only through optional features within the profile; **·** = not applicable.

The mapping basis is the transitive derivation described in [How This Document Was Produced](#how-this-document-was-produced) (profile → feature/described functionality → Part 2 use-case IDs → A–S block). For block letters whose membership is described only in profile prose, the assignment is from matching use-case names.

| Block (link) | Core | Adv. Security | Smart Charging | ISO 15118 | Bidir. Power Transfer | DER control |
|--------------|:----:|:-------------:|:--------------:|:---------:|:---------------------:|:-----------:|
| [A. Security](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#a-security) | R | R | · | O | · | · |
| [B. Provisioning](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#b-provisioning) | R | · | · | · | · | · |
| [C. Authorization](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#c-authorization) | R | · | · | R | O | · |
| [D. Local Authorization List](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#d-local-authorization-list-management) | O | · | · | · | · | · |
| [E. Transactions](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#e-transactions) | R | · | O | O | O | O |
| [F. Remote Control](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#f-remote-control) | R | · | R | R | · | · |
| [G. Availability](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#g-availability) | R | · | · | · | · | · |
| [H. Reservation](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#h-reservation) | O | · | · | · | · | · |
| [I. Tariff And Cost](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#i-tariff-and-cost) | O | · | · | · | · | · |
| [J. Meter Values](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#j-meter-values) | R | · | · | O | · | · |
| [K. Smart Charging](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#k-smart-charging) | · | · | R | R | R | O |
| [L. Firmware Management](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#l-firmware-management) | R | · | · | · | · | · |
| [M. Certificate Management](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#m-certificate-management) | R | R | · | R | · | · |
| [N. Diagnostics](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#n-diagnostics) | R | · | · | · | · | · |
| [O. Display Message](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#o-display-message) | O | · | · | · | · | · |
| [P. Data Transfer](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#p-data-transfer) | O | · | · | · | · | · |
| [Q. Bidirectional Power Transfer (V2X)](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#q-bidirectional-power-transfer-v2x) | · | · | O | O | R | O |
| [R. DER Control](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#r-der-control) | · | · | · | · | · | R |
| [S. Battery Swapping](../OCPP-2.1-UseCases/OCPP-2.1-UseCases.md#s-battery-swapping) | O | · | · | · | · | · |

Reading notes:
- **Core** is broad because Part 5 places the bulk of OCPP functionality in it (auth, provisioning, transactions, remote control, availability, metering, firmware, certificate install/retrieve, diagnostics/customer-info) plus optional Core sub-areas (D Local Auth List, H Reservation, I/O tariff & display, P data transfer, S battery swapping for the battery-swap subtype).
- **Adv. Security** is narrow: it sits on top of Core's certificate/security functionality (blocks A and M) — client-side cert, update CS cert, security-profile upgrade.
- **ISO 15118 support** spans authorization (C, incl. PnC contract certs and EIM), smart charging (K/F), certificate management (M), and signed meter values (J); its dependency on Advanced Security and Smart Charging is why those blocks appear under it as well.
- **Smart Charging** EMS-control sub-area reaches into V2X (block Q) via external V2X control features (`SC-10`), hence the **O** there.
- **Bidirectional Power Transfer** is block Q; it requires Smart Charging (K) and uses authorization (C) for V2X authorization over ISO 15118-20.
- **DER control** is block R; in practice it is exercised alongside V2X sessions (block Q) and smart-charging setpoints (block K), hence the **O** marks.

### 3.1 Feature → use-case anchors (selected, from Part 5 Appendix C)

These are representative feature IDs and the Part 2 use cases they map to, illustrating the derivation. Full lists are in Part 5 Tables 2, 3 and Appendix C.

| Feature ID | Feature (paraphrased) | Profile | Maps to use case(s) | Block |
|------------|------------------------|---------|---------------------|-------|
| `C-61` | Security Profile 1 (unsecured transport + basic auth) | Core | A01 | A |
| `C-13` | Reset per EVSE | Core | B11, B12 | B |
| `C-30`/`C-36` | Authorization via RFID ISO14443 | Core | C01 | C |
| `C-09.x` | Transaction start points (TxStartPoint) | Core | E01 (S1–S6) | E |
| `C-48` | Authorization of remote start | Core | F01, F02 | F |
| `C-04` | Limit StatusNotifications | Core | (config var for G01) | G |
| `R-0`/`R-2` | Reservation support | Core (Reservation) | H block use cases | H |
| `C-40`/`C-42` | Supported / signed meter measurands | Core | J01, J02 | J |
| `C-60` | Cancel ongoing firmware update | Core | L01, L02 | L |
| `C-56` | Provide SummaryInventory | Core | B07 | B |
| `C-14` | Retrieve/delete CustomerInformation | Core | N09, N10 | N |
| `C-62 (2.1)` | Resume transactions (ImmediateAndResume) | Core | B13 | B |
| `C-63 (2.1)` | Transaction limits | Core | E16 | E |
| `C-64 (2.1)` | Resume transaction after interruption | Core | E17 | E |
| `SC-8 (2.1)` | Dynamic charging profiles | Smart Charging | block K use cases | K |
| `SC-6 (2.1)` | Priority charging | Smart Charging | block K use cases | K |
| `SC-10 (2.1)` | EMS Control (external system / external V2X) | Smart Charging | K, Q | K/Q |
| `ISO-1.2 (2.1)` | ISO 15118-20 supported | ISO 15118 | C, K, M, Q use cases | C/K/M/Q |
| `ISO-6 (2.1)` | ServiceRenegotiation | ISO 15118 | block K renegotiation | K |
| `BPT-1` | Frequency support | Bidir. Power Transfer | Q01… (V2X) | Q |
| `BPT-2` | Local load balancing | Bidir. Power Transfer | Q (V2X) | Q |
| `C-76 (2.1)` | Battery Swapping Stations (CSMS) | Core (battery-swap subtype) | S block use cases | S |

> The **DER control** and **Advanced Security** profiles have **no optional features** in Part 5 (their tables state "No optional features for this profile"); all their certification test cases are Mandatory (or Conditional on hardware/ISO features) once you certify for the profile.

---

## 4. New 2.1 Functionality and How It Maps to Certification

OCPP 2.1 introduces functionality that Part 5 wires into certification as follows:

| 2.1 area | Functional block | How it maps to certification |
|----------|------------------|------------------------------|
| **DER control** (grid-code behavior: curves, limits, frequency/voltage response) | R | Its **own** profile, "DER control (2.1)". Mandatory components: `ACDERCtrlr` and/or `DCDERCtrlr` (AC vs DC station). No optional features — test cases TC_R_100…TC_R_108 are Mandatory or Conditional on ISO/hardware. See the [DER Control Deep-Dive](../OCPP-2.1-DERControl/OCPP-2.1-DERControl.md). |
| **V2X / Bidirectional Power Transfer** (central & local V2X control, frequency support, AFRR) | Q | Its **own** profile, "Bidirectional Power Transfer (2.1)". Mandatory component: `V2XChargingCtrlr`. **Requires the Smart Charging profile.** Optional features `BPT-1` (frequency support) and `BPT-2` (local load balancing). See the [Bidirectional Power Transfer Deep-Dive](../OCPP-2.1-Bidirectional/OCPP-2.1-Bidirectional.md). |
| **Tariff & payment** (set default tariff, local cost calc, prepaid card, integrated/standalone payment terminal, settlement, QR codes) | I (Tariff & Cost), C (payment authorization) | A **Payment (2.1)** sub-area **inside Core**, with its own mandatory components `TariffCostCtrlr` + `WebPaymentsCtrlr` (`Core: P-0 (2.1)`). Certified via the optional `P-*` features. Tariff/cost display is part of Core's Advanced User Interface (`Core: UI-0`, components `TariffCostCtrlr` + `DisplayMessageCtrlr`). |
| **Battery swapping** | S | **No standalone profile.** Handled as a charging-station product **subtype**: `BatterySwapCtrlr` is mandatory in Core only for the Battery Swapping subtype; CSMS optional feature `C-76 (2.1)`. |
| **Other 2.1 Core additions** | E, B, N, F | Resume transactions / `ImmediateAndResume` (`C-62`→B13), transaction limits (`C-63`→E16), resume after interruption (`C-64`→E17), `DataCollectorLog` (`C-65`→N01), CustomTrigger (`C-29.7`→F06). All optional Core features. |

> **ESCALATE: POLICY-DEPENDENT** — Whether to pursue the new 2.1 profiles (DER control, Bidirectional Power Transfer) or the Payment/battery-swap feature groups is a deployment and grid/utility decision (and for V2X depends on certifying Smart Charging first). Confirm scope with the product owner and grid/utility stakeholder.

---

## 5. Mandatory Controller Components per Profile

A functional area cannot be tested without the device-model controller component that holds its variables, so Part 5 Chapter 5 makes specific components **mandatory** for certification. (Component details: [Device Model Reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md).)

| Profile / feature ID | Mandatory controller components |
|----------------------|---------------------------------|
| **Core** | `OCPPCommCtrlr`, `TxCtrlr`, `DeviceDataCtrlr`, `ClockCtrlr`, `SecurityCtrlr`, `SampledDataCtrlr`, `AlignedDataCtrlr`, `AuthCtrlr`; `BatterySwapCtrlr` (Battery Swapping subtype only) |
| **Core: DM-0** (Advanced Device Management) | `MonitoringCtrlr` |
| **Core: LA-0** (Local Authorization List) | `LocalAuthListCtrlr` |
| **Core: UI-0** (Advanced User Interface) | `TariffCostCtrlr`, `DisplayMessageCtrlr` |
| **Core: R-0** (Reservation) | `ReservationCtrlr` |
| **Core: P-0 (2.1)** (Payment) | `TariffCostCtrlr`, `WebPaymentsCtrlr` |
| **Advanced Security** | `SecurityCtrlr` (already part of Core) |
| **Smart Charging** | `SmartChargingCtrlr` |
| **ISO 15118 support** | `ISO15118Ctrlr`, `SmartChargingCtrlr` |
| **Bidirectional Power Transfer (2.1)** | `V2XChargingCtrlr` |
| **DER control (2.1)** | `DCDERCtrlr` and/or `ACDERCtrlr` (AC vs DC station) |

---

## 6. How the Test Tables Work (Part 5 Chapter 4)

For orientation only — these are not reproduced here. Each test case row in Part 5 Chapter 4 carries:

| Column | Meaning |
|--------|---------|
| TC Id | Test-case identifier, e.g. `TC_A_01`, `TC_R_108`, `TC_Q_117`. Prefix letter mirrors the functional block (A=Security, B=Provisioning, …, Q=V2X, R=DER). |
| Conf. Test for Charging Station / for CSMS | **M** = Mandatory if you certify the profile; **C** = Conditional (must pass only if the linked feature/hardware condition holds); blank = not applicable to that side. |
| Condition / remark, Feature no., Feature | The optional feature ID(s) (and/or lab question `AQ-n` / hardware feature `HFS-n`) whose support makes a `C` test case required. |

The Part 5 test sections are: Core (4.2), Advanced Security (4.3), Smart Charging (4.4), ISO 15118 Support (4.5), Bidirectional Power Transfer 2.1 (4.6), DER Control 2.1 (4.7). The Part 6 document holds the full test-case bodies; the OCA Compliance Testing Tool executes them. For the authoritative M/C status of any specific test case, consult Part 5 and Part 6 directly.

---

## 7. Quick Reference

| Question | Answer (non-normative) |
|----------|------------------------|
| Which profile is always required? | Core. |
| Which profiles are new in 2.1? | Bidirectional Power Transfer, DER control (plus the Payment sub-area and battery-swap subtype within Core, and 2.1 extensions to Smart Charging and ISO 15118). |
| Which profiles have dependencies? | ISO 15118 support depends on Advanced Security + Smart Charging test cases; Bidirectional Power Transfer requires Smart Charging. |
| Which profiles have no optional features? | Advanced Security and DER control. |
| Is battery swapping its own profile? | No — it is a charging-station subtype (`BatterySwapCtrlr` in Core; CSMS feature `C-76`). |
| Is payment its own profile? | No — it is a Payment (2.1) sub-area within Core (`Core: P-0 (2.1)`). |
| Who certifies? | OCA-accredited test labs using the OCA Compliance Testing Tool. This document does not. |
