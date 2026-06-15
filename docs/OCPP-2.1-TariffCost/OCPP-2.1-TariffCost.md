# OCPP 2.1 — Tariff, Cost, and Payment Deep-Dive

> **Purpose:** Practical reference for AI agents implementing or debugging OCPP 2.1 tariffs, local cost calculation, settlement, and ad-hoc/web payment — functional block I (Tariff And Cost) plus the payment/settlement use cases of block C (Authorization). Covers the first-class tariff model, default vs driver-specific tariffs, running and final cost, VAT/tax handling, and the NotifySettlement / NotifyWebPaymentStarted / VatNumberValidation flows.

> **Last updated:** 2026-06-11

---

## How This Document Was Produced

This document covers the tariff, cost, settlement, and payment functionality of OCPP 2.1 functional block I (Tariff And Cost, use cases I01–I12) together with the related ad-hoc/web payment use cases C18–C25 in block C; per-use-case detail lives in the use-case catalog. Its dominant confidence tier is **spec-knowledge** — behavioral rules summarized in original wording from the OCPP 2.1 Edition 2 Part 2 specification. Message names, field names, enum values, and structural constraints are **schema-derived** — cross-referenced against the [TariffAndCost schema reference](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md), the [data types reference](../OCPP-2.1-DataTypes.md), and the [enumerations reference](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md), all mechanically extracted from the official OCA artifacts. No spec prose is reproduced verbatim (the OCA specification is CC BY-ND licensed); all explanatory text is original.

This document contains **6 escalation points** marked with `> **ESCALATE:**`. They are all `POLICY-DEPENDENT` — actual tariff values, VAT rates, payment-provider choices, and settlement policies are business/operator/regulatory decisions. When an AI agent encounters one, it MUST stop and ask the developer (or the commercial/finance/regulatory stakeholder) to make the decision. See [METHODOLOGY.md](../METHODOLOGY.md) for the full confidence and escalation model.

**Companion documents:**
- [TariffAndCost Schemas](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md) — complete field-level message and local-type schemas (mechanically generated, high confidence)
- [Data Types Reference](../OCPP-2.1-DataTypes.md) — shared types including [`TariffType`](../OCPP-2.1-DataTypes.md#tarifftype), [`PriceType`](../OCPP-2.1-DataTypes.md#pricetype), [`TaxRateType`](../OCPP-2.1-DataTypes.md#taxratetype)
- [Enumerations Reference](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md) — [Payment Brands](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#payment-brands-22), [Payment Recognition](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#payment-recognition-9), [IdToken Types](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#idtoken-types-11), [Additional Info Types (Ad-hoc)](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#additional-info-types-ad-hoc-11)
- [Device Model Reference](../OCPP-2.1-DeviceModel/OCPP-2.1-DeviceModel.md) — the `TariffCostCtrlr`, `PaymentCtrlr`, and `WebPaymentsCtrlr` components

---

## 1. What OCPP 2.1 Adds Over 2.0.1

In OCPP 2.0.1, cost was **always calculated centrally by the CSMS**. The only related message was `CostUpdated` (then part of the Display block), which pushed a running total to the station's display. The station knew nothing about how the price was derived.

OCPP 2.1 introduces a **first-class, machine-readable tariff model** ([`TariffType`](../OCPP-2.1-DataTypes.md#tarifftype)) and the option of **local cost calculation**: the CSMS pushes a tariff structure to the station, and the station computes the cost itself. This enables a real-time running-cost display without a message round-trip per update, and lets the station stop a charge at a preset amount (e.g. prepaid charging).

| Capability | 2.0.1 | 2.1 |
|------------|-------|-----|
| Central cost calculation | Yes (only option) | Yes (still supported) |
| Machine-readable tariff structure | No | Yes — [`TariffType`](../OCPP-2.1-DataTypes.md#tarifftype) |
| Local cost calculation on the station | No | Yes (opt-in via `TariffCostCtrlr.Enabled[Tariff]`) |
| Install default tariff per EVSE | No | Yes — `SetDefaultTariff` |
| Driver-specific tariff at authorization | No | Yes — `tariff` in `AuthorizeResponse` |
| Change tariff mid-transaction | No | Yes — `ChangeTransactionTariff` |
| Inspect installed tariffs | No | Yes — `GetTariffs` |
| Remove tariffs | No | Yes — `ClearTariffs` |
| Cost breakdown at end of transaction | `totalCost` (single number) | `CostDetailsType` (per-period breakdown + tax) |
| Ad-hoc / web payment settlement | use case C03 (2.0.1) | `NotifySettlement`, `NotifyWebPaymentStarted`, `VatNumberValidation` |

`CostUpdated` still exists in 2.1 but has **moved from the Display block to block I (Tariff And Cost)**. Its direction is unchanged: CSMS → CS.

### 1.1 Block-I messages

For complete field-level schemas, see the [TariffAndCost schema reference](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md).

| Message | Direction | Purpose |
|---------|-----------|---------|
| [`CostUpdated`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#costupdated) | CSMS → CS | Push a centrally-calculated running total cost for an ongoing transaction |
| [`SetDefaultTariff`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#setdefaulttariff) | CSMS → CS | Install the default tariff on an EVSE (or all EVSEs) for local cost calculation |
| [`ChangeTransactionTariff`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#changetransactiontariff) | CSMS → CS | Replace the tariff of an active transaction |
| [`GetTariffs`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#gettariffs) | CSMS → CS | List the tariffs currently installed on an EVSE (or all) |
| [`ClearTariffs`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#cleartariffs) | CSMS → CS | Remove one or more default tariffs |
| [`NotifySettlement`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifysettlement) | CS → CSMS | Report the result of settling an ad-hoc payment |
| [`NotifyWebPaymentStarted`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#notifywebpaymentstarted) | CSMS → CS | Tell the station a web/QR payment flow has started, so it locks the EVSE |
| [`VatNumberValidation`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#vatnumbervalidation) | CS → CSMS | Validate a VAT/tax id (for a company receipt) against the CSMS |

> **Driver-specific tariffs do not have their own message.** A tariff for a particular driver is delivered inside the `tariff` field of `AuthorizeResponse` (block C). See §4.2.

---

## 2. Tariff Structure

A tariff is a [`TariffType`](../OCPP-2.1-DataTypes.md#tarifftype): a set of optional price fields (energy, charging time, idle time, fixed fee, reservation), each of which may carry conditions that decide when its price applies. The station uses this to compute cost locally. The same structure maps cleanly onto the roaming protocols OCPI, OCHP, and OICP.

### 2.1 `TariffType` fields

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `tariffId` | string (maxLength 60) | **Yes** | Unique id of the tariff on this station |
| `currency` | string (maxLength 3) | **Yes** | ISO 4217 currency code |
| `energy` | [`TariffEnergyType`](../OCPP-2.1-DataTypes.md#tariffenergytype) | No | Per-kWh price element(s) + tax |
| `chargingTime` | [`TariffTimeType`](../OCPP-2.1-DataTypes.md#tarifftimetype) | No | Per-minute price while actively charging |
| `idleTime` | [`TariffTimeType`](../OCPP-2.1-DataTypes.md#tarifftimetype) | No | Per-minute price while connected but not charging |
| `fixedFee` | [`TariffFixedType`](../OCPP-2.1-DataTypes.md#tarifffixedtype) | No | Flat fee, evaluated **only at the start** of a transaction (e.g. a start fee) |
| `reservationTime` | [`TariffTimeType`](../OCPP-2.1-DataTypes.md#tarifftimetype) | No | Per-minute price for reservation time |
| `reservationFixed` | [`TariffFixedType`](../OCPP-2.1-DataTypes.md#tarifffixedtype) | No | Flat fee for a reservation |
| `minCost` | [`PriceType`](../OCPP-2.1-DataTypes.md#pricetype) | No | Floor on total cost |
| `maxCost` | [`PriceType`](../OCPP-2.1-DataTypes.md#pricetype) | No | Cap on total cost |
| `description` | [`MessageContentType`](../OCPP-2.1-DataTypes.md#messagecontenttype)[] (1–10) | No | Human-readable tariff text shown to the driver (per language) |
| `validFrom` | string (date-time) | No | Time the tariff becomes active; absent = active immediately. Usually in UTC. |

### 2.2 Nested price-element types

Each "time"/"fixed"/"energy" field wraps a list of price entries plus an optional tax block. The price entries are evaluated **in order**, and the **first entry whose conditions all match** is the one applied. An entry with no `conditions` always matches, so it should be placed **last** as a fallback.

| Wrapper type | Holds | Tax field | Price entry type | Price field |
|--------------|-------|-----------|------------------|-------------|
| [`TariffEnergyType`](../OCPP-2.1-DataTypes.md#tariffenergytype) | `prices` (≥1) | `taxRates` (≤5) | [`TariffEnergyPriceType`](../OCPP-2.1-DataTypes.md#tariffenergypricetype) | `priceKwh` (excl. tax, per kWh) |
| [`TariffTimeType`](../OCPP-2.1-DataTypes.md#tarifftimetype) | `prices` (≥1) | `taxRates` (≤5) | [`TariffTimePriceType`](../OCPP-2.1-DataTypes.md#tarifftimepricetype) | `priceMinute` (excl. tax, per minute) |
| [`TariffFixedType`](../OCPP-2.1-DataTypes.md#tarifffixedtype) | `prices` (≥1) | `taxRates` (≤5) | [`TariffFixedPriceType`](../OCPP-2.1-DataTypes.md#tarifffixedpricetype) | `priceFixed` (flat amount) |

The energy/time entries carry [`TariffConditionsType`](../OCPP-2.1-DataTypes.md#tariffconditionstype); the fixed entries carry [`TariffConditionsFixedType`](../OCPP-2.1-DataTypes.md#tariffconditionsfixedtype) (a reduced set, since a flat fee at start cannot depend on energy/power/time consumed during the session).

### 2.3 Conditions

When more than one condition is set on an entry, they are combined with logical **AND** — all must hold for the price to be active. Time/date conditions are in **local time** because they are shown to the driver as written; the station converts to its internal timezone (recommended UTC) when calculating cost.

[`TariffConditionsType`](../OCPP-2.1-DataTypes.md#tariffconditionstype) (energy & time elements):

| Condition | Type | Meaning (summarized) |
|-----------|------|----------------------|
| `dayOfWeek` | [`DayOfWeekEnumType`](../OCPP-2.1-DataTypes.md#dayofweekenumtype)[] (1–7) | Day(s) this price applies |
| `startTimeOfDay` / `endTimeOfDay` | string `HH:MM` | Local time-of-day window (wraps past midnight if end < start) |
| `validFromDate` / `validToDate` | string `YYYY-MM-DD` | Local date window (from inclusive, to exclusive) |
| `evseKind` | [`EvseKindEnumType`](../OCPP-2.1-DataTypes.md#evsekindenumtype) | AC or DC EVSE |
| `paymentBrand` | string (maxLength 20) | Surcharge per card brand — value from [Payment Brands](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#payment-brands-22) |
| `paymentRecognition` | string (maxLength 20) | Surcharge per payment method — value from [Payment Recognition](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#payment-recognition-9) |
| `minEnergy` / `maxEnergy` | number (Wh) | Consumed-energy window |
| `minPower` / `maxPower` | number (W) | Instantaneous charging power window |
| `minCurrent` / `maxCurrent` | number (A) | Instantaneous current window (sum over phases) |
| `minTime` / `maxTime` | integer (s) | Total transaction (charge + idle) duration window |
| `minChargingTime` / `maxChargingTime` | integer (s) | Active charging duration window |
| `minIdleTime` / `maxIdleTime` | integer (s) | Idle (not charging) duration window |

For reverse energy flow (V2X discharging), power/current/energy take **negative** values; `minXXX` means "closest to zero" and `maxXXX` means "furthest from zero".

[`TariffConditionsFixedType`](../OCPP-2.1-DataTypes.md#tariffconditionsfixedtype) is the same set **minus** the energy/power/current/time-duration conditions (it keeps `dayOfWeek`, `startTimeOfDay`/`endTimeOfDay`, `validFromDate`/`validToDate`, `evseKind`, `paymentBrand`, `paymentRecognition`).

A station MAY decline to support conditions. If so it MUST report `TariffCostCtrlr.ConditionsSupported[Tariff]` = false; the CSMS then knows not to send conditional tariffs, and a `SetDefaultTariff` carrying conditions is rejected with status `ConditionNotSupported`.

> **ESCALATE: POLICY-DEPENDENT** — The actual price values (`priceKwh`, `priceMinute`, `priceFixed`, `minCost`/`maxCost`), the currency, time-of-day windows, idle-fee thresholds, and any per-brand/per-method surcharges are commercial decisions. Do not invent tariff numbers; obtain them from the operator's pricing.

---

## 3. Tax / VAT Handling

Tax is attached at the price-element level via [`TaxRateType`](../OCPP-2.1-DataTypes.md#taxratetype) (each of `energy`, `chargingTime`, `idleTime`, `fixedFee` can carry up to 5 tax rates). Prices in the tariff are quoted **excluding tax**; tax is then applied on top.

| `TaxRateType` field | Type | Meaning |
|---------------------|------|---------|
| `tax` | number | Tax percentage |
| `type` | string (maxLength 20) | Human label for the receipt, e.g. `"vat"`, `"federal"`, `"state"` |
| `stack` | integer (default 0) | Compounding level: `0` = tax on the net price; `1` = added on top of stack 0; `2` on top of 1; etc. |

[`PriceType`](../OCPP-2.1-DataTypes.md#pricetype) (used for `minCost`/`maxCost` and inside the cost breakdown) carries `exclTax` and/or `inclTax` (at least one required) plus its own `taxRates`. This lets the station report both the net and gross amounts so the driver and the receipt agree.

A separate [`TaxRuleType`](../OCPP-2.1-DataTypes.md#taxruletype) exists for ISO 15118-20 price schedules (not the OCPP local tariff) — do not confuse the two.

> **ESCALATE: POLICY-DEPENDENT** — VAT/tax rates, the set of tax types, and whether taxes compound (the `stack` levels) are regulatory/jurisdictional decisions. Obtain them from the operator's finance/tax function, not from assumptions.

---

## 4. Setting and Managing Tariffs

Local cost calculation is opt-in and controlled by the `TariffCostCtrlr` device-model component:

| Variable | Effect |
|----------|--------|
| `TariffCostCtrlr.Available[Tariff]` | Station supports the `TariffType` structure |
| `TariffCostCtrlr.Enabled[Tariff]` | Local cost calculation enabled |
| `TariffCostCtrlr.ConditionsSupported[Tariff]` | Station can evaluate tariff conditions |
| `TariffCostCtrlr.MaxElements[Tariff]` | Max price elements per field (caps tariff complexity) |
| `TariffCostCtrlr.Interval[Tariff]` | Max interval (s) for re-evaluating power/current/energy conditions |
| `TariffCostCtrlr.Currency` | Station's ISO 4217 currency |
| `TariffCostCtrlr.HandleFailedTariff[Tariff]` | What to do when a driver tariff cannot be processed (see §4.2) |

> A **Local Authorization List cannot be combined with local cost calculation** for driver-specific tariffs, because an `AuthorizeRequest` is required to fetch the driver tariff. Local lists are only usable when the **default** tariff applies to all drivers.

Two kinds of tariff exist, tracked by [`TariffKindEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffkindenumtype): `DefaultTariff` (installed per EVSE) and `DriverTariff` (delivered in `AuthorizeResponse`, tied to an idToken).

### 4.1 Default tariffs — `SetDefaultTariff` (use case I07)

The CSMS installs a default tariff on a specific EVSE, or on all EVSEs with `evseId = 0`. A `tariffId` uniquely identifies the tariff on the station.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `SetDefaultTariff` (`evseId`, `tariff`) | `evseId = 0` installs to every EVSE individually |
| 2 | CS → CSMS | `SetDefaultTariffResponse` (`status`) | Status from [`TariffSetStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffsetstatusenumtype) |
| 3 | CS → EV Driver | (display) | Station shows `tariff.description` for the relevant EVSE(s) |

`SetDefaultTariffResponse` status values: `Accepted`, `Rejected`, `TooManyElements` (more price elements than `MaxElements` supports), `ConditionNotSupported`, `DuplicateTariffId` (a tariff with that `tariffId` already exists).

**Updating a default tariff with a future activation:** because `tariffId` is unique, an updated default tariff must use a **new** `tariffId`. To switch at a specific time, install the new tariff with a `validFrom` in the future; the station ignores it until the current time reaches `validFrom`, then it replaces the old default. If a tariff with an earlier `validFrom` would otherwise overwrite one with a later `validFrom`, the station keeps the later one (it does not remove a tariff that becomes valid after the incoming one). A tariff in use by an **active transaction** keeps being used for that transaction until it ends, even after a replacement default is installed (override only via `ChangeTransactionTariff`).

**Time semantics:** `startTimeOfDay`/`endTimeOfDay` and `validFromDate`/`validToDate` inside conditions are **local time** (`HH:MM` 5-character notation for times). `TariffType.validFrom` is in **system time, usually UTC** (`"Z"`).

### 4.2 Driver-specific tariffs — via `AuthorizeResponse` (use case I08)

A tariff for an individual driver is returned in the `tariff` field of `AuthorizeResponse` (no dedicated request). This is a `DriverTariff`.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CS → CSMS | `AuthorizeRequest` (`idToken`) | Driver presents token |
| 2 | CSMS → CS | `AuthorizeResponse` (`idTokenInfo.status = Accepted`, `tariff`) | CSMS attaches the driver's tariff |
| 3 | CS → EV Driver | (display) | Station shows the driver tariff description |
| 4 | CS → CSMS | `TransactionEventRequest` (`transactionInfo.tariffId` = driver tariff) | On `Started`/`Updated`, station associates the tariff with the transaction |

Key rules:
- A `validFrom` MUST NOT be sent in a driver tariff (and is ignored if present) — driver tariffs are immediate.
- The station uses the driver tariff only for the transaction started for that idToken.
- If `AuthCacheEnabled` = true the station caches the driver tariff (so be aware no new tariff is fetched while the cached idToken is valid; operators are advised to disable/clear the cache when tariffs change).
- After the transaction ends, the station removes the driver tariff (unless it is still in use at another EVSE).
- The CSMS MUST give `TariffType`s with different content **different `tariffId`s**, so the `tariffId`s recorded in historical `CostDetailsType` records stay valid (the `tariffId` may be a sequence number, UUID, or content hash).

**Tariff acceptance and failure handling.** If the driver does not accept the tariff: if a transaction already started, the station de-authorizes the idToken and sends `TransactionEventRequest` with `triggerReason = TariffNotAccepted` (ending with `stoppedReason = DeAuthorized` if `TxStopPoint` includes `Authorized`/`PowerPathClosed`); if not yet started, the idToken is de-authorized (a transaction can still start without authorization but delivers no energy). If the driver accepts (implicitly by plugging in, or explicitly), the station associates the tariff via `transactionInfo.tariffId` in the next `TransactionEventRequest`.

If the station **cannot process** a received driver tariff, `TariffCostCtrlr.HandleFailedTariff[Tariff]` decides the behavior:

| `HandleFailedTariff` value | Station behavior |
|----------------------------|------------------|
| `Deauthorize` | Do not authorize the idToken for charging |
| `UseDefaultTariff` | Authorize and use the installed default tariff (spec prose inconsistently writes `UseDefault` in one requirement) |
| `CentralCost` | Authorize, do **not** do local cost calculation — CSMS calculates cost centrally (as in I02/I03) |

On a processing failure the station also sets `TariffCostCtrlr.Problem` = true and notifies the CSMS via `NotifyEventRequest` (and clears it to false on the next successful tariff).

### 4.3 Changing the tariff of an active transaction — `ChangeTransactionTariff` (use case I11)

Used when prices change unexpectedly during a session and the operator wants the active transaction repriced.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `ChangeTransactionTariff` (`tariff`, `transactionId`) | Override the tariff on a running transaction |
| 2 | CS → CSMS | `ChangeTransactionTariffResponse` (`status`) | Status from [`TariffChangeStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffchangestatusenumtype) |

`ChangeTransactionTariffResponse` status values: `Accepted`, `Rejected`, `TooManyElements`, `ConditionNotSupported`, `TxNotFound` (no such transaction), `NoCurrencyChange` (the new tariff's currency differs from the running one — not allowed mid-transaction). The change shows up in `CostDetailsType` as a new `ChargingPeriodType`, reported with `triggerReason = TariffChanged`.

### 4.4 Inspecting tariffs — `GetTariffs` (use case I09)

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `GetTariffs` (`evseId`) | `evseId = 0` returns tariffs from all EVSEs |
| 2 | CS → CSMS | `GetTariffsResponse` (`status`, `tariffAssignments[]`) | Status from [`TariffGetStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffgetstatusenumtype) |

`GetTariffsResponse` status: `Accepted`, `Rejected`, `NoTariff` (no tariffs present — `tariffAssignments` absent). Each [`TariffAssignmentType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffassignmenttype) reports a `tariffId`, its `tariffKind`, the `evseIds` where it is installed, any `idTokens` it is tied to (for driver tariffs), and `validFrom`. For an active transaction the assignment also lists the EVSE where the transaction is running. Note `GetTariffs` returns the **assignments**, not the full tariff structures.

### 4.5 Removing tariffs — `ClearTariffs` (use case I10)

`ClearTariffs` removes **default** tariffs. (Driver tariffs are removed automatically when no longer in use — see §4.2.)

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `ClearTariffs` (`tariffIds?`, `evseId?`) | Both fields optional — see matching rules below |
| 2 | CS → CSMS | `ClearTariffsResponse` (`clearTariffsResult[]`) | One [`ClearTariffsResultType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#cleartariffsresulttype) per matched/attempted tariff |

Matching:
- No parameters → clear **all** tariffs on the station.
- `tariffIds` only → clear matching tariff ids on all EVSEs.
- `evseId` only → clear all tariffs at that EVSE.
- Both → clear only tariffs matching both id and EVSE.

Each result carries a `status` from [`TariffClearStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffclearstatusenumtype) (`Accepted`, `Rejected`, `NoTariff`) and the `tariffId`. A tariff that is **in use by an active transaction** is still reported `Accepted` (cleared from EVSEs), **but the station keeps using it for that transaction until it ends**. If nothing matched, `clearTariffsResult` has no `tariffId` and status `NoTariff`.

### 4.6 Default vs driver-specific and fallback

When a transaction starts for an idToken: if a driver tariff was received it is used; otherwise the EVSE's installed default tariff is used for cost calculation. There are also two display-only fallbacks, configured as device-model strings (per language):

| Situation | Variable | Use case |
|-----------|----------|----------|
| No driver-specific tariff available / station offline at authorization | `TariffCostCtrlr.TariffFallbackMessage` | I04 — Show Fallback Tariff Information |
| Station offline at transaction end, cannot retrieve total cost | `TariffCostCtrlr.TotalCostFallbackMessage` | I05 — Show Fallback Total Cost Message |
| Station offline (tariff fallback) | `TariffCostCtrlr.OfflineTariffFallbackMessage` | (device-model config) |

These are messages shown to the driver, not tariffs used for calculation.

---

## 5. Cost

### 5.1 Pre-transaction tariff display (use cases I01, I04)

Before a transaction, the EV driver-specific tariff can be shown via the `idTokenInfo.personalMessage` field of `AuthorizeResponse` (a textual representation — distinct from the machine-readable `TariffType`). The CSMS sends it only if the station supports tariff or display-message functionality. This works with central cost calculation; the machine-readable `TariffType` (I07/I08) is the local-calculation equivalent.

### 5.2 Running cost during a transaction (use case I02)

Two mechanisms, both CSMS-driven for **central** calculation.

Push model:

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CSMS → CS | `CostUpdated` (`totalCost`, `transactionId`) | Pushed at the interval configured by `TariffCostCtrlr.Interval[Cost]`; `totalCost` includes taxes, in the station's `Currency` |
| 2 | CS → CSMS | `CostUpdatedResponse` | Empty `{}` |
| 3 | CS → EV Driver | (display) | Station shows current total |

Alternative: when the station sends a `TransactionEventRequest` with `eventType = Updated`, the CSMS returns the running cost in the `totalCost` field of `TransactionEventResponse`.

For **local** calculation, the station computes the running cost itself from the installed tariff; `TariffCostCtrlr.Enabled[RunningCost]` and `TariffCostCtrlr.Interval[Cost]` control whether and how often it emits running-cost updates in `costDetails`.

> Sending `CostUpdated` very frequently generates many messages and can drive up mobile data cost — choose the interval deliberately.

### 5.3 Final cost at end of transaction (use cases I03, C24/C25)

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | EV Driver → CS | (present token / stop) | Driver ends the transaction |
| 2 | CS → CSMS | `TransactionEventRequest` (`eventType = Ended`) | Carries `costDetails` (local calc) or relies on central calc |
| 3 | CSMS → CS | `TransactionEventResponse` (`totalCost`) | For central calc, CSMS returns the total |
| 4 | CS → EV Driver | (display) | Station shows the final cost / breakdown |

- For central calculation, the CSMS sets `totalCost` in `TransactionEventResponse`. To indicate a **free** transaction the CSMS sets `totalCost = 0.00` (omitting it does **not** imply free).
- For local calculation, the station includes a `CostDetailsType` cost breakdown in the final `TransactionEventRequest`.
- If `TxStopPoint = ParkingBayOccupancy`, the driver has already left, so the station SHOULD NOT display the final cost.

### 5.4 Cost breakdown — `CostDetailsType`

At the end of a locally-calculated transaction, the station includes a `CostDetailsType` in the last `TransactionEventRequest`. It contains a list of `ChargingPeriodType` entries, each representing a span during which the same price element applied; a new period is created whenever conditions change and a different price becomes valid. (A `TariffFixedPriceType` is evaluated only at start, so it does not create periods.) A simple tariff with no conditions yields a single period. The breakdown also includes `totalCost` (per dimension: `energy`, `chargingTime`, `fixed`, etc., each with `exclTax`/`inclTax`/`taxRates`, plus a `total`) and `totalUsage`.

The period start is an absolute timestamp (not seconds-since-start), so a CSO/EMSP can validate the price against the tariff. Unit prices and conditions are **not** repeated in `CostDetailsType` — they are already in the `TariffType` referenced by `tariffId`. Because historical cost records reference `tariffId`, that id must remain stable for unchanged tariff content (see §4.2).

> **ESCALATE: POLICY-DEPENDENT** — Whether cost is calculated **locally on the station or centrally by the CSMS**, the running-cost update interval, and the rounding/free-transaction policy are operator decisions affecting billing.

---

## 6. Settlement and Payment

OCPP 2.1 supports **ad-hoc payment** (credit/debit card or digital wallet, no account), via three physical channels: an **integrated** payment terminal, a **stand-alone** terminal/kiosk (block C use case C24), and a **web/QR** flow (C25). The block-I messages `NotifySettlement`, `NotifyWebPaymentStarted`, and `VatNumberValidation` are the OCPP-level touchpoints. The protocol between the station/CSMS and the Payment Service Provider (PSP) is out of OCPP scope.

The ad-hoc idToken carries the PSP reference: `idToken.type = DirectPayment` (see [IdToken Types](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#idtoken-types-11)) and the PSP reference ("pspRef") as the token value, with card details added as [Additional Info Types (Ad-hoc)](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#additional-info-types-ad-hoc-11) (`PaymentBrand`, `PaymentRecognition`, `CardBin`, `CardLast4Digits`, etc.). `PaymentBrand` values come from [Payment Brands](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#payment-brands-22); `PaymentRecognition` from [Payment Recognition](../OCPP-2.1-Enumerations/OCPP-2.1-Enumerations.md#payment-recognition-9).

`PaymentCtrlr` device-model variables govern the terminal:

| Variable | Meaning |
|----------|---------|
| `PaymentCtrlr.Enabled` | Payment terminal support enabled |
| `PaymentCtrlr.AuthorizeDirectPayment` | Require an `AuthorizeRequest` to approve a direct payment |
| `PaymentCtrlr.AuthorizationAmount` | Pre-authorization (reserved) amount |
| `PaymentCtrlr.IncrementalAuthorizationAmount` | Step to extend the authorization (0/absent = not allowed) |
| `PaymentCtrlr.IncrementalAuthorizationThreshold` | When cost nears the authorized amount minus this, increase the authorization |
| `PaymentCtrlr.SettlementByCSMS` | true → CSMS settles directly with the PSP, bypassing the terminal |
| `PaymentCtrlr.ReceiptByCSMS` | true → CSMS provides the receipt URL; false → the terminal does |
| `PaymentCtrlr.ReceiptServerUrl` | Receipt-server URL shown to the driver |
| `PaymentCtrlr.Merchant[Id/TaxId/Name/Address/City]` | Merchant details for the receipt |

### 6.1 Settlement at end of transaction — `NotifySettlement` (use case C21)

After an ad-hoc transaction ends, the cost is settled and the station reports the outcome with `NotifySettlement`.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CS → CSMS | `TransactionEventRequest` (`eventType = Ended`, `costDetails`) | End of transaction |
| 2 | CSMS → CS | `TransactionEventResponse` | (central calc returns `totalCost` + `updatedPersonalMessage`) |
| 3 | CS → terminal/PSP | settle `costDetails.totalCost` | Via terminal, or CSMS↔PSP if `SettlementByCSMS` |
| 4 | CS → CSMS | `NotifySettlement` (`pspRef`, `settlementAmount`, `settlementTime`, `status = Settled`, `transactionId`, optional `vatNumber`/`vatCompany`/`receiptId`/`receiptUrl`) | `pspRef` is the value used as the idToken |
| 5 | CSMS → CS | `NotifySettlementResponse` (`receiptId?`, `receiptUrl?`) | If `ReceiptByCSMS`, CSMS returns the receipt URL; station can QR-encode it for the driver |

`status` is a [`PaymentStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#paymentstatusenumtype): `Settled`, `Canceled`, `Rejected`, `Failed`.

Who provides the receipt depends on config: with `ReceiptByCSMS = true` the CSMS returns `receiptUrl` in the response; with `ReceiptByCSMS = false` the station puts the terminal's receipt URL into `receiptUrl`/`receiptId` of the request. With `SettlementByCSMS = true`, settlement happens CSMS↔PSP directly and there may be no receipt feedback to the driver (the operator must offer a website/app to retrieve it).

### 6.2 Settlement canceled before any cost — `NotifySettlement` status `Canceled` (use cases C19/C20)

If the driver authorizes via the terminal but no transaction/cost occurs, the authorization reservation on the card is released and the station sends `NotifySettlement` with `status = Canceled` and `settlementTime` = now, so the CSMS knows the pre-authorized `idToken` will not result in a charge.

Two sub-cases distinguish the timing:

- **C19 — canceled before transaction start:** `transactionId` is empty (or absent). Example: the driver tapped the card but never plugged in and the station timed out before any OCPP transaction was opened.
- **C20 — canceled after transaction start:** `transactionId` is present (the OCPP transaction had already started). Example: `EVConnectionTimeout` fires after the transaction was opened — the card pre-authorization is voided and `transactionId` identifies the aborted transaction.

### 6.3 Settlement rejected or failed — `NotifySettlement` status `Rejected`/`Failed` (use case C22)

| Outcome | `status` | Cause |
|---------|----------|-------|
| PSP rejected the settlement | `Rejected` | PSP declined |
| Settlement failed technically | `Failed` | e.g. cannot reach PSP |

The station sends `NotifySettlement` with `transactionId`, `settlementAmount`, `settlementTime`, the status, and optional error detail in `statusInfo` (no receipt fields). The CSO can then attempt manual capture with the PSP using the `pspRef` (the idToken value).

### 6.4 Web / QR-code payment — `NotifyWebPaymentStarted` (use case C25)

For QR-code / web ad-hoc payment, the station shows a URL (often with a time-based one-time password for dynamic QR codes) that the driver scans to reach the CSMS payment page; the CSMS then drives the PSP flow and remotely starts the transaction. `NotifyWebPaymentStarted` tells the station to lock the EVSE while the web flow is in progress, so it cannot be started locally.

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CS → EV Driver | (display QR / URL) | Per `WebPaymentsCtrlr` config (URL template, TOTP) |
| 2 | EV Driver → CSMS | (scan, open URL) | CSMS validates the URL / one-time password |
| 3 | CSMS → CS | `NotifyWebPaymentStarted` (`evseId`, `timeout`) | Station locks the EVSE for `timeout` seconds |
| 4 | CS → CSMS | `NotifyWebPaymentStartedResponse` | Empty `{}` |
| 5 | CSMS ↔ PSP | (payment authorization) | Out of OCPP scope; PSP returns a `pspRef` |
| 6 | CSMS → CS | `RequestStartTransaction` (`idToken` = pspRef, `type = DirectPayment`) | Remote start after approval |

`WebPaymentsCtrlr` variables: `URLTemplate` (with `{chargingstationid}` / `{roamingevseid}` / `{evse}` / `{totp}` / `{version}` placeholders), `URLParameters` (`maxtime`/`maxenergy`/`maxcost`), `TOTPVersion`, `ValidityTime`, `SharedSecret`, `Length`, `QRCodeQuality`. The maximum the driver entered (time/energy/cost) becomes a `transactionLimit` (`maxTime`/`maxEnergy`/`maxCost`) on the transaction. If URL/one-time-password validation fails, no transaction is started.

### 6.5 VAT number validation — `VatNumberValidation`

When an ad-hoc customer wants a company (VAT) receipt, the entered VAT number can be validated against the CSMS before being put on the receipt (or attached to a `NotifySettlement` as `vatNumber`/`vatCompany`).

| Step | Sender → Receiver | Message | Trigger / Notes |
|------|-------------------|---------|-----------------|
| 1 | CS → CSMS | `VatNumberValidation` (`vatNumber`, `evseId?`) | Driver entered a VAT number |
| 2 | CSMS → CS | `VatNumberValidationResponse` (`status`, `vatNumber`, `company?`, `evseId?`, `statusInfo?`) | `status` is [`GenericStatusEnumType`](../OCPP-2.1-DataTypes.md#genericstatusenumtype) (`Accepted`/`Rejected`); on success `company` ([`AddressType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#addresstype)) is returned for the receipt |

The validated `vatNumber` and `company` (`vatCompany`, an `AddressType`) can then be included in `NotifySettlement` for a company receipt.

### 6.6 Incremental authorization (use case C23)

Not a tariff/settlement message, but relevant to cost-limited ad-hoc charging: when transaction cost approaches the pre-authorized amount minus `PaymentCtrlr.IncrementalAuthorizationThreshold`, the station asks the terminal to extend the authorization by `PaymentCtrlr.IncrementalAuthorizationAmount` and raises `transactionInfo.transactionLimit.maxCost`, reported via `TransactionEventRequest` with `triggerReason = LimitSet`. If incremental authorization is not allowed (`IncrementalAuthorizationAmount` = 0/absent), the energy flow halts when `maxCost` is reached.

> **ESCALATE: POLICY-DEPENDENT** — The pre-authorization amount, incremental-authorization step and threshold, choice of payment service provider, and the settlement channel (terminal vs CSMS, `SettlementByCSMS`/`ReceiptByCSMS`) are operator/commercial decisions.

> **ESCALATE: POLICY-DEPENDENT** — Whether to issue company/VAT receipts and how VAT numbers are validated and stored are finance/regulatory decisions; the OCPP messages are only the transport.

> **ESCALATE: POLICY-DEPENDENT** — Receipt generation and delivery (who generates the receipt, the receipt-server URL, retention) are operator decisions.

---

## 7. Quick Reference — Enumerations

| Enum | Message | Values |
|------|---------|--------|
| [`TariffSetStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffsetstatusenumtype) | SetDefaultTariff | `Accepted`, `Rejected`, `TooManyElements`, `ConditionNotSupported`, `DuplicateTariffId` |
| [`TariffChangeStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffchangestatusenumtype) | ChangeTransactionTariff | `Accepted`, `Rejected`, `TooManyElements`, `ConditionNotSupported`, `TxNotFound`, `NoCurrencyChange` |
| [`TariffGetStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffgetstatusenumtype) | GetTariffs | `Accepted`, `Rejected`, `NoTariff` |
| [`TariffClearStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffclearstatusenumtype) | ClearTariffs (per result) | `Accepted`, `Rejected`, `NoTariff` |
| [`TariffKindEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#tariffkindenumtype) | GetTariffs (assignment) | `DefaultTariff`, `DriverTariff` |
| [`PaymentStatusEnumType`](../OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md#paymentstatusenumtype) | NotifySettlement | `Settled`, `Canceled`, `Rejected`, `Failed` |
| [`GenericStatusEnumType`](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | VatNumberValidation | `Accepted`, `Rejected` |
