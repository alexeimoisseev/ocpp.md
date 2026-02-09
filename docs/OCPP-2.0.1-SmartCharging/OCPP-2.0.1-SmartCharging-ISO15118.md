# OCPP 2.0.1 — Smart Charging & ISO 15118

> **Purpose:** Reference for AI agents working with OCPP 2.0.1 smart charging features that interact with ISO 15118 — EV charging needs, EV-proposed schedules, and sales tariffs. Companion to the [Smart Charging Deep-Dive](./OCPP-2.0.1-SmartCharging.md).

> **Last updated:** 2026-02-07

---

## How This Document Was Produced

This document covers how ISO 15118 EV charging needs, schedules, and tariffs flow through OCPP 2.0.1. Its dominant confidence tier is **schema-derived** — field names, types, enum values, and type structures (`ACChargingParametersType`, `DCChargingParametersType`, `ChargingNeedsType`, `SalesTariffType`) are cross-referenced against the [schema documentation](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) and [data types reference](../OCPP-2.0.1-DataTypes.md). "Practical meaning" paragraphs and CSMS decision logic guidance are **interpretation**. ISO 15118 protocol behavior itself (as distinct from the OCPP messages that carry it) is outside the scope of the OCA JSON schemas — what this document says about ISO 15118 internals is **spec-knowledge** from a separate standard.

This document contains **2 escalation points** marked with `> **ESCALATE:**`. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

---

## 1. Overview

ISO 15118 enables high-level communication between the EV and the EVSE (via the charging cable), allowing the EV to express its charging needs and receive optimized charging schedules. OCPP 2.0.1 bridges this communication to the CSMS through three messages:

| Message | Direction | Purpose |
|---------|-----------|---------|
| `NotifyEVChargingNeeds` | CS → CSMS | EV tells the CS what it needs; CS forwards to CSMS |
| `NotifyEVChargingSchedule` | CS → CSMS | EV proposes a schedule; CS forwards for CSMS approval |
| `SetChargingProfile` | CSMS → CS | CSMS responds with an optimized `TxProfile` |

For complete field-level schemas, see the [schema reference](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#notifyevchargingneeds).

---

## 2. EV Charging Needs

### 2.1 `NotifyEVChargingNeeds`

When an ISO 15118-capable EV connects, it communicates its charging requirements to the EVSE. The CS forwards these to the CSMS via `NotifyEVChargingNeeds`.

The request contains a [`ChargingNeedsType`](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#chargingneedstype) with:

| Field | Description |
|-------|-------------|
| `requestedEnergyTransfer` | **Required.** The energy transfer mode: `DC`, `AC_single_phase`, `AC_two_phase`, or `AC_three_phase` |
| `departureTime` | **Optional.** When the EV expects to leave. Enables the CSMS to spread charging over the available window |
| `acChargingParameters` | **Optional.** AC-specific parameters (if AC mode) |
| `dcChargingParameters` | **Optional.** DC-specific parameters (if DC mode) |

The `evseId` field identifies which EVSE the EV is connected to (must be > 0).

The optional `maxScheduleTuples` field tells the CSMS the maximum number of schedule periods the EV's onboard system can handle.

### 2.2 Energy Transfer Modes

The `EnergyTransferModeEnumType` specifies how energy will be transferred:

| Value | Description |
|-------|-------------|
| `DC` | DC charging — power converted by the EVSE |
| `AC_single_phase` | AC single-phase — EV's onboard charger, one phase |
| `AC_two_phase` | AC two-phase — uncommon, used in some regions |
| `AC_three_phase` | AC three-phase — EV's onboard charger, three phases |

> **Schema source (schema-described):** Enum values from [`EnergyTransferModeEnumType`](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#energytransfermodeenumtype).

### 2.3 AC Charging Parameters

[`ACChargingParametersType`](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#acchargingparameterstype) — all fields are **required**:

| Field | Type | Description |
|-------|------|-------------|
| `energyAmount` | integer | Energy requested in Wh (includes preconditioning) |
| `evMaxCurrent` | integer | Maximum current per phase the EV supports (including cable capacity) |
| `evMaxVoltage` | integer | Maximum voltage the EV supports |
| `evMinCurrent` | integer | Minimum current per phase the EV can usefully accept |

**Practical meaning:**
- `energyAmount` tells the CSMS the total energy the EV wants. Combined with `departureTime`, the CSMS can calculate the average power needed: `energyAmount / (departureTime - now)`.
- `evMaxCurrent` and `evMinCurrent` define the EV's operating range. The CSMS should not set a profile limit above `evMaxCurrent` (wasted capacity) or below `evMinCurrent` (inefficient charging, similar to `minChargingRate`).

### 2.4 DC Charging Parameters

[`DCChargingParametersType`](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#dcchargingparameterstype) — `evMaxCurrent` and `evMaxVoltage` are **required**, others optional:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `evMaxCurrent` | integer | **Yes** | Maximum DC current the EV supports (including cable) |
| `evMaxVoltage` | integer | **Yes** | Maximum DC voltage the EV supports |
| `energyAmount` | integer | No | Energy requested in Wh (includes preconditioning) |
| `evMaxPower` | integer | No | Maximum power in W the EV supports |
| `evEnergyCapacity` | integer | No | Battery capacity in Wh |
| `stateOfCharge` | integer | No | Current SoC (0-100%) |
| `fullSoC` | integer | No | SoC at which EV considers battery full (0-100%) |
| `bulkSoC` | integer | No | SoC at which EV considers fast charging complete (0-100%) |

**Practical meaning:**
- `stateOfCharge` + `energyAmount` (or `evEnergyCapacity` + `fullSoC`) lets the CSMS calculate how much energy is actually needed.
- `bulkSoC` indicates when the EV will reduce its charging rate (DC fast charging tapers above ~80% SoC on most EVs). The CSMS can plan accordingly.
- `evMaxPower` is important for DC — it defines the upper bound the CSMS should use when setting profiles in watts.

### 2.5 CSMS Response

The CSMS responds to `NotifyEVChargingNeeds` with a status:

| Value | Meaning |
|-------|---------|
| `Accepted` | CSMS has processed the needs and will provide a charging schedule |
| `Rejected` | CSMS cannot accommodate the requested needs |
| `Processing` | CSMS is still computing an optimal schedule; will send a profile later |

> **Schema source (schema-described):** [`NotifyEVChargingNeedsStatusEnumType`](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md#notifyevchargingneedsstatusenumtype).

After responding, the CSMS typically creates an optimized `TxProfile` via `SetChargingProfile` tailored to the EV's needs, the available grid capacity, and any active constraints.

> **ESCALATE: POLICY-DEPENDENT** — CSMS optimization strategy for EV charging needs.
> How the CSMS creates a `TxProfile` from the EV's needs is a business/policy decision with multiple valid approaches. An AI agent MUST NOT implement a default optimization strategy. Ask the developer:
> 1. Minimize cost — spread charging across cheapest tariff periods, using `departureTime` as the deadline
> 2. Minimize time — charge as fast as possible within grid constraints, ignoring tariff optimization
> 3. Balance grid load — distribute charging evenly across the available window to flatten the building demand curve
> 4. Custom logic — site-specific algorithm (e.g., prioritize renewable energy, respect demand response signals)

---

## 3. EV Charging Schedules

### 3.1 `NotifyEVChargingSchedule`

In some ISO 15118 flows, the EV itself proposes a charging schedule (based on the tariff information it received). The CS forwards this to the CSMS via `NotifyEVChargingSchedule`.

| Field | Description |
|-------|-------------|
| `evseId` | Which EVSE (must be > 0) |
| `timeBase` | Reference timestamp — periods in the schedule are relative to this |
| `chargingSchedule` | The EV's proposed [`ChargingScheduleType`](../OCPP-2.0.1-DataTypes.md#chargingscheduletype) |

The CSMS responds with `Accepted` or `Rejected` (`GenericStatusEnumType`).

**How this interacts with CSMS profiles:**

The EV's proposed schedule is informational — it tells the CSMS what the EV would like to do. The CSMS can:
- Accept the schedule and set a matching `TxProfile`.
- Modify the schedule based on grid constraints and set a different `TxProfile`.
- Reject the schedule if it cannot be accommodated.

The actual charging limits are still controlled by the profiles installed on the CS, not by the EV's proposed schedule directly.

> **ESCALATE: POLICY-DEPENDENT** — How the CSMS handles the EV's proposed schedule.
> The CSMS must decide whether to accept, modify, or override the EV's preferred schedule. An AI agent MUST NOT choose a default strategy. Ask the developer:
> 1. Accept the EV's schedule if it fits within constraints — set a matching `TxProfile`
> 2. Always compute an independent optimal schedule — ignore the EV's proposal, use only the needs data
> 3. Use the EV's schedule as a starting point — adjust only where it violates constraints

---

## 4. Sales Tariffs

Sales tariffs enable the CSMS to communicate pricing information to the EV via the Charging Station, using ISO 15118's tariff structures. The EV can then optimize its charging schedule based on cost.

### 4.1 Tariff Structure

A [`SalesTariffType`](../OCPP-2.0.1-DataTypes.md#salestarifftype) is embedded within a `ChargingScheduleType` and contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | **Required.** Unique identifier for this tariff within the charging session |
| `salesTariffEntry[]` | array | **Required.** Time-based tariff entries (1-1024 entries) |
| `numEPriceLevels` | integer | Optional. Total number of distinct price levels across all entries |
| `salesTariffDescription` | string | Optional. Human-readable description (max 32 chars) |

Each [`SalesTariffEntryType`](../OCPP-2.0.1-DataTypes.md#salestariffentrytype) contains:

| Field | Type | Description |
|-------|------|-------------|
| `relativeTimeInterval` | `RelativeTimeIntervalType` | **Required.** When this tariff entry applies (start offset + optional duration) |
| `ePriceLevel` | integer | Optional. Relative price level (lower = cheaper). Refers to `numEPriceLevels` |
| `consumptionCost[]` | array | Optional. Detailed cost breakdown (up to 3 entries) |

### 4.2 Cost Kinds

The [`CostKindEnumType`](../OCPP-2.0.1-DataTypes.md#costkindenumtype) allows different types of cost information:

| Value | Meaning |
|-------|---------|
| `CarbonDioxideEmission` | CO2 emissions associated with the energy |
| `RelativePricePercentage` | Relative price (percentage, for comparison across periods) |
| `RenewableGenerationPercentage` | Percentage of energy from renewable sources |

These enable the EV (or the driver via the EV's interface) to optimize not just for cost but also for environmental impact.

### 4.3 How Tariffs Flow

Three actors: CSMS, CS, and EV (via ISO 15118 over the charging cable).

1. CSMS sends `SetChargingProfile` to CS — includes `salesTariff` in the `chargingSchedule`.
2. CS forwards the tariff to the EV via ISO 15118 `ChargeParameterDiscovery`.
3. EV optimizes its charging schedule based on the tariff (choosing cheaper periods, minimizing cost or carbon).
4. CS sends `NotifyEVChargingSchedule` to CSMS — the EV's preferred schedule.
5. CSMS evaluates the EV's schedule against grid constraints and other profiles.
6. CSMS sends `SetChargingProfile` to CS — a `TxProfile` that approves, modifies, or overrides the EV's proposal.

### 4.4 `ConsumptionCostType` and `CostType`

For detailed pricing (beyond simple price levels), [`ConsumptionCostType`](../OCPP-2.0.1-DataTypes.md#consumptioncosttype) defines cost blocks:

| Field | Description |
|-------|-------------|
| `startValue` | Consumption threshold (kWh) where this cost block begins |
| `cost[]` | Array of up to 3 [`CostType`](../OCPP-2.0.1-DataTypes.md#costtype) entries — one per `CostKindEnumType` |

Each `CostType`:
| Field | Description |
|-------|-------------|
| `costKind` | Which type of cost (`CarbonDioxideEmission`, `RelativePricePercentage`, `RenewableGenerationPercentage`) |
| `amount` | The cost value |
| `amountMultiplier` | Exponent (base 10). Final value = `amount × 10^amountMultiplier`. Range: -3 to 3 |

This structure allows expressing tiered pricing (different cost per kWh at different consumption levels) with multiple cost dimensions.

---

## 5. When ISO 15118 Smart Charging Applies

ISO 15118 smart charging features are only relevant when:
- The EVSE supports ISO 15118 communication (typically DC CCS or AC with powerline communication).
- The EV supports ISO 15118-2 (or later) and has implemented the smart charging features.
- The CSMS is configured to handle EV charging needs and generate optimized profiles.

Most AC charging today uses IEC 61851 basic signaling (no ISO 15118), in which case `NotifyEVChargingNeeds`, `NotifyEVChargingSchedule`, and sales tariffs are not used. Smart charging still works — it just relies on CSMS-set profiles without EV input.

---

## 6. Related Documents

| Document | What it contains |
|----------|-----------------|
| [Smart Charging Deep-Dive](./OCPP-2.0.1-SmartCharging.md) | Profile model, composite schedules, pitfalls, config variables |
| [Smart Charging Examples](./OCPP-2.0.1-SmartCharging-Examples.md) | Worked calculations, JSON payloads, sequence diagrams |
| [Smart Charging Schemas](../OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) | Field-level message schemas |
| [Data Types Reference](../OCPP-2.0.1-DataTypes.md) | All shared types |

---

*This document is a community reference for AI agents. It is not affiliated with or endorsed by the Open Charge Alliance or ISO. For the authoritative specifications, refer to the official OCPP 2.0.1 documents from OCA and ISO 15118 from ISO.*
