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
_(summary pending)_

### A02 — Update Charging Station Certificate by request of CSMS
_(summary pending)_

### A03 — Update Charging Station Certificate initiated by the Charging Station
_(summary pending)_

### A04 — Security Event Notification
_(summary pending)_

### A05 — Upgrade Charging Station Security Profile
_(summary pending)_

---

## B. Provisioning

### B01 — Cold Boot Charging Station
_(summary pending)_

### B02 — Cold Boot Charging Station - Pending
_(summary pending)_

### B03 — Cold Boot Charging Station - Rejected
_(summary pending)_

### B04 — Offline Behavior Idle Charging Station
_(summary pending)_

### B05 — Set Variables
_(summary pending)_

### B06 — Get Variables
_(summary pending)_

### B07 — Get Base Report
_(summary pending)_

### B08 — Get Custom Report
_(summary pending)_

### B09 — Setting a new NetworkConnectionProfile
_(summary pending)_

### B10 — Migrate to new CSMS
_(summary pending)_

### B11 — Reset - Without Ongoing Transaction
_(summary pending)_

### B12 — Reset - With Ongoing Transaction
_(summary pending)_

### B13 — Reset - With Ongoing Transaction - Resuming Transaction
_(summary pending)_

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
