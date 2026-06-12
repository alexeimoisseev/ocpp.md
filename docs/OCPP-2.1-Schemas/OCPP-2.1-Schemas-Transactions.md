# OCPP 2.1 Schemas — Transactions

> **Functional Block:** E
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [TransactionEvent](#transactionevent) (CS → CSMS)
- [GetTransactionStatus](#gettransactionstatus) (CSMS → CS)

---

## TransactionEvent

**Direction:** CS → CSMS

### TransactionEventRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `eventType` | [TransactionEventEnumType](#transactioneventenumtype) | **Yes** |  |  |
| `seqNo` | integer | **Yes** | min: 0.0 | Incremental sequence number, helps with determining if all messages of a transaction have been received. |
| `timestamp` | string (date-time) | **Yes** |  | The date and time at which this transaction event occurred. |
| `transactionInfo` | [TransactionType](#transactiontype) | **Yes** |  |  |
| `triggerReason` | [TriggerReasonEnumType](#triggerreasonenumtype) | **Yes** |  |  |
| `cableMaxCurrent` | integer | No |  | The maximum current of the connected cable in Ampere (A). |
| `costDetails` | [CostDetailsType](#costdetailstype) | No |  |  |
| `evse` | [EVSEType](../OCPP-2.1-DataTypes.md#evsetype) | No |  |  |
| `evseSleep` | boolean | No |  | *(2.1)* True when EVSE electronics are in sleep mode for this transaction. Default value (when absent) is false. |
| `idToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | No |  |  |
| `meterValue` | [MeterValueType](#metervaluetype)[] | No | minItems: 1 |  |
| `numberOfPhasesUsed` | integer | No | min: 0.0, max: 3.0 | If the Charging Station is able to report the number of phases used, then it SHALL provide it. When omitted the CSMS may be able to determine the number of phases used as follows: + 1: The numberPhases in the currently used ChargingSchedule. + 2: The number of phases provided via device management. |
| `offline` | boolean | No |  | Indication that this transaction event happened when the Charging Station was offline. Default = false, meaning: the event occurred when the Charging Station was online. Default: `False` |
| `preconditioningStatus` | [PreconditioningStatusEnumType](#preconditioningstatusenumtype) | No |  |  |
| `reservationId` | integer | No | min: 0.0 | This contains the Id of the reservation that terminates as a result of this transaction. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example TransactionEventRequest</summary>

```json
{
  "eventType": "Ended",
  "seqNo": 0,
  "timestamp": "2024-01-15T10:30:00Z",
  "transactionInfo": {
    "transactionId": "string"
  },
  "triggerReason": "AbnormalCondition"
}
```

</details>

### TransactionEventResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingPriority` | integer | No |  | Priority from a business point of view. Default priority is 0, The range is from -9 to 9. Higher values indicate a higher priority. The chargingPriority in TransactionEventResponse is temporarily, so it may not be set in the IdTokenInfoType afterwards. Also the chargingPriority in TransactionEventResponse has a higher priority than the one in IdTokenInfoType. |
| `idTokenInfo` | [IdTokenInfoType](../OCPP-2.1-DataTypes.md#idtokeninfotype) | No |  |  |
| `totalCost` | number | No |  | When _eventType_ of TransactionEventRequest is Updated, then this value contains the running cost. When _eventType_ of TransactionEventRequest is Ended, then this contains the final total cost of this transaction, including taxes, in the currency configured with the Configuration Variable: Currency. Absence of this value does not imply that the transaction was free. To indicate a free transaction, the CSMS SHALL send a value of 0.00. |
| `transactionLimit` | [TransactionLimitType](#transactionlimittype) | No |  |  |
| `updatedPersonalMessage` | [MessageContentType](../OCPP-2.1-DataTypes.md#messagecontenttype) | No |  |  |
| `updatedPersonalMessageExtra` | [MessageContentType](../OCPP-2.1-DataTypes.md#messagecontenttype)[] | No | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


*No fields are required. An empty `{}` is a valid response.*

---

## GetTransactionStatus

**Direction:** CSMS → CS

### GetTransactionStatusRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | string | No | maxLength: 36 | The Id of the transaction for which the status is requested. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### GetTransactionStatusResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `messagesInQueue` | boolean | **Yes** |  | Whether there are still message to be delivered. |
| `ongoingIndicator` | boolean | No |  | Whether the transaction is still ongoing. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### ChargingStateEnumType

Current charging state, is required when state has changed. Omitted when there is no communication between EVSE and EV, because no cable is plugged in.

| Value |
|-------|
| `EVConnected` |
| `Charging` |
| `SuspendedEV` |
| `SuspendedEVSE` |
| `Idle` |

**Used in:** TransactionEvent

---

### CostDimensionEnumType

Type of cost dimension: energy, power, time, etc.

| Value |
|-------|
| `Energy` |
| `MaxCurrent` |
| `MinCurrent` |
| `MaxPower` |
| `MinPower` |
| `IdleTIme` |
| `ChargingTime` |

**Used in:** TransactionEvent

---

### LocationEnumType

Indicates where the measured value has been sampled. Default = "Outlet"

**Default:** `Outlet`

| Value |
|-------|
| `Body` |
| `Cable` |
| `EV` |
| `Inlet` |
| `Outlet` |
| `Upstream` |

**Used in:** MeterValues, TransactionEvent

---

### MeasurandEnumType

Type of measurement. Default = "Energy.Active.Import.Register"

**Default:** `Energy.Active.Import.Register`

| Value |
|-------|
| `Current.Export` |
| `Current.Export.Offered` |
| `Current.Export.Minimum` |
| `Current.Import` |
| `Current.Import.Offered` |
| `Current.Import.Minimum` |
| `Current.Offered` |
| `Display.PresentSOC` |
| `Display.MinimumSOC` |
| `Display.TargetSOC` |
| `Display.MaximumSOC` |
| `Display.RemainingTimeToMinimumSOC` |
| `Display.RemainingTimeToTargetSOC` |
| `Display.RemainingTimeToMaximumSOC` |
| `Display.ChargingComplete` |
| `Display.BatteryEnergyCapacity` |
| `Display.InletHot` |
| `Energy.Active.Export.Interval` |
| `Energy.Active.Export.Register` |
| `Energy.Active.Import.Interval` |
| `Energy.Active.Import.Register` |
| `Energy.Active.Import.CableLoss` |
| `Energy.Active.Import.LocalGeneration.Register` |
| `Energy.Active.Net` |
| `Energy.Active.Setpoint.Interval` |
| `Energy.Apparent.Export` |
| `Energy.Apparent.Import` |
| `Energy.Apparent.Net` |
| `Energy.Reactive.Export.Interval` |
| `Energy.Reactive.Export.Register` |
| `Energy.Reactive.Import.Interval` |
| `Energy.Reactive.Import.Register` |
| `Energy.Reactive.Net` |
| `EnergyRequest.Target` |
| `EnergyRequest.Minimum` |
| `EnergyRequest.Maximum` |
| `EnergyRequest.Minimum.V2X` |
| `EnergyRequest.Maximum.V2X` |
| `EnergyRequest.Bulk` |
| `Frequency` |
| `Power.Active.Export` |
| `Power.Active.Import` |
| `Power.Active.Setpoint` |
| `Power.Active.Residual` |
| `Power.Export.Minimum` |
| `Power.Export.Offered` |
| `Power.Factor` |
| `Power.Import.Offered` |
| `Power.Import.Minimum` |
| `Power.Offered` |
| `Power.Reactive.Export` |
| `Power.Reactive.Import` |
| `SoC` |
| `Voltage` |
| `Voltage.Minimum` |
| `Voltage.Maximum` |

**Used in:** MeterValues, TransactionEvent

---

### PhaseEnumType

Indicates how the measured value is to be interpreted. For instance between L1 and neutral (L1-N) Please note that not all values of phase are applicable to all Measurands. When phase is absent, the measured value is interpreted as an overall value.

| Value |
|-------|
| `L1` |
| `L2` |
| `L3` |
| `N` |
| `L1-N` |
| `L2-N` |
| `L3-N` |
| `L1-L2` |
| `L2-L3` |
| `L3-L1` |

**Used in:** MeterValues, TransactionEvent

---

### PreconditioningStatusEnumType

*(2.1)* The current preconditioning status of the BMS in the EV. Default value is Unknown.

| Value |
|-------|
| `Unknown` |
| `Ready` |
| `NotReady` |
| `Preconditioning` |

**Used in:** TransactionEvent

---

### ReadingContextEnumType

Type of detail value: start, end or sample. Default = "Sample.Periodic"

**Default:** `Sample.Periodic`

| Value |
|-------|
| `Interruption.Begin` |
| `Interruption.End` |
| `Other` |
| `Sample.Clock` |
| `Sample.Periodic` |
| `Transaction.Begin` |
| `Transaction.End` |
| `Trigger` |

**Used in:** MeterValues, TransactionEvent

---

### ReasonEnumType

The _stoppedReason_ is the reason/event that initiated the process of stopping the transaction. It will normally be the user stopping authorization via card (Local or MasterPass) or app (Remote), but it can also be CSMS revoking authorization (DeAuthorized), or disconnecting the EV when TxStopPoint = EVConnected (EVDisconnected). Most other reasons are related to technical faults or energy limitations. + MAY only be omitted when _stoppedReason_ is "Local"

| Value |
|-------|
| `DeAuthorized` |
| `EmergencyStop` |
| `EnergyLimitReached` |
| `EVDisconnected` |
| `GroundFault` |
| `ImmediateReset` |
| `MasterPass` |
| `Local` |
| `LocalOutOfCredit` |
| `Other` |
| `OvercurrentFault` |
| `PowerLoss` |
| `PowerQuality` |
| `Reboot` |
| `Remote` |
| `SOCLimitReached` |
| `StoppedByEV` |
| `TimeLimitReached` |
| `Timeout` |
| `ReqEnergyTransferRejected` |

**Used in:** TransactionEvent

---

### TariffCostEnumType

Type of cost: normal or the minimum or maximum cost.

| Value |
|-------|
| `NormalCost` |
| `MinCost` |
| `MaxCost` |

**Used in:** TransactionEvent

---

### TransactionEventEnumType

This contains the type of this event. The first TransactionEvent of a transaction SHALL contain: "Started" The last TransactionEvent of a transaction SHALL contain: "Ended" All others SHALL contain: "Updated"

| Value |
|-------|
| `Ended` |
| `Started` |
| `Updated` |

**Used in:** TransactionEvent

---

### TriggerReasonEnumType

Reason the Charging Station sends this message to the CSMS

| Value |
|-------|
| `AbnormalCondition` |
| `Authorized` |
| `CablePluggedIn` |
| `ChargingRateChanged` |
| `ChargingStateChanged` |
| `CostLimitReached` |
| `Deauthorized` |
| `EnergyLimitReached` |
| `EVCommunicationLost` |
| `EVConnectTimeout` |
| `EVDeparted` |
| `EVDetected` |
| `LimitSet` |
| `MeterValueClock` |
| `MeterValuePeriodic` |
| `OperationModeChanged` |
| `RemoteStart` |
| `RemoteStop` |
| `ResetCommand` |
| `RunningCost` |
| `SignedDataReceived` |
| `SoCLimitReached` |
| `StopAuthorized` |
| `TariffChanged` |
| `TariffNotAccepted` |
| `TimeLimitReached` |
| `Trigger` |
| `TxResumed` |
| `UnlockCommand` |

**Used in:** TransactionEvent

---

### ChargingPeriodType

A ChargingPeriodType consists of a start time, and a list of possible values that influence this period, for example: amount of energy charged this period, maximum current during this period etc.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `startPeriod` | string (date-time) | **Yes** |  | Start timestamp of charging period. A period ends when the next period starts. The last period ends when the session ends. |
| `dimensions` | [CostDimensionType](#costdimensiontype)[] | No | minItems: 1 |  |
| `tariffId` | string | No | maxLength: 60 | Unique identifier of the Tariff that was used to calculate cost. If not provided, then cost was calculated by some other means. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### CostDetailsType

CostDetailsType contains the cost as calculated by Charging Station based on provided TariffType. NOTE: Reservation is not shown as a _chargingPeriod_, because it took place outside of the transaction.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `totalCost` | [TotalCostType](#totalcosttype) | **Yes** |  |  |
| `totalUsage` | [TotalUsageType](#totalusagetype) | **Yes** |  |  |
| `chargingPeriods` | [ChargingPeriodType](#chargingperiodtype)[] | No | minItems: 1 |  |
| `failureReason` | string | No | maxLength: 500 | Optional human-readable reason text in case of failure to calculate. |
| `failureToCalculate` | boolean | No |  | If set to true, then Charging Station has failed to calculate the cost. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### CostDimensionType

Volume consumed of cost dimension.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `type` | [CostDimensionEnumType](#costdimensionenumtype) | **Yes** |  |  |
| `volume` | number | **Yes** |  | Volume of the dimension consumed, measured according to the dimension type. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### MeterValueType

Collection of one or more sampled values in MeterValuesRequest and TransactionEvent. All sampled values in a MeterValue are sampled at the same point in time.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `sampledValue` | [SampledValueType](#sampledvaluetype)[] | **Yes** | minItems: 1 |  |
| `timestamp` | string (date-time) | **Yes** |  | Timestamp for measured value(s). |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---

### SampledValueType

Single sampled value in MeterValues. Each value can be accompanied by optional fields. To save on mobile data usage, default values of all of the optional fields are such that. The value without any additional fields will be interpreted, as a register reading of active import energy in Wh (Watt-hour) units.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `value` | number | **Yes** |  | Indicates the measured value. |
| `context` | [ReadingContextEnumType](#readingcontextenumtype) | No |  |  |
| `location` | [LocationEnumType](#locationenumtype) | No |  |  |
| `measurand` | [MeasurandEnumType](#measurandenumtype) | No |  |  |
| `phase` | [PhaseEnumType](#phaseenumtype) | No |  |  |
| `signedMeterValue` | [SignedMeterValueType](#signedmetervaluetype) | No |  |  |
| `unitOfMeasure` | [UnitOfMeasureType](#unitofmeasuretype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---

### SignedMeterValueType

Represent a signed version of the meter value.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `encodingMethod` | string | **Yes** | maxLength: 50 | Format used by the energy meter to encode the meter data. For example: OCMF or EDL. |
| `signedMeterData` | string | **Yes** | maxLength: 32768 | Base64 encoded, contains the signed data from the meter in the format specified in _encodingMethod_, which might contain more then just the meter value. It can contain information like timestamps, reference to a customer etc. |
| `publicKey` | string | No | maxLength: 2500 | *(2.1)* Base64 encoded, sending depends on configuration variable _PublicKeyWithSignedMeterValue_. |
| `signingMethod` | string | No | maxLength: 50 | *(2.1)* Method used to create the digital signature. Optional, if already included in _signedMeterData_. Standard values for this are defined in Appendix as SigningMethodEnumStringType. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---

### TotalCostType

This contains the cost calculated during a transaction. It is used both for running cost and final cost of the transaction.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currency` | string | **Yes** | maxLength: 3 | Currency of the costs in ISO 4217 Code. |
| `total` | [TotalPriceType](#totalpricetype) | **Yes** |  |  |
| `typeOfCost` | [TariffCostEnumType](#tariffcostenumtype) | **Yes** |  |  |
| `chargingTime` | [PriceType](../OCPP-2.1-DataTypes.md#pricetype) | No |  |  |
| `energy` | [PriceType](../OCPP-2.1-DataTypes.md#pricetype) | No |  |  |
| `fixed` | [PriceType](../OCPP-2.1-DataTypes.md#pricetype) | No |  |  |
| `idleTime` | [PriceType](../OCPP-2.1-DataTypes.md#pricetype) | No |  |  |
| `reservationFixed` | [PriceType](../OCPP-2.1-DataTypes.md#pricetype) | No |  |  |
| `reservationTime` | [PriceType](../OCPP-2.1-DataTypes.md#pricetype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### TotalPriceType

Total cost with and without tax. Contains the total of energy, charging time, idle time, fixed and reservation costs including and/or excluding tax.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `exclTax` | number | No |  | Price/cost excluding tax. Can be absent if _inclTax_ is present. |
| `inclTax` | number | No |  | Price/cost including tax. Can be absent if _exclTax_ is present. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### TotalUsageType

This contains the calculated usage of energy, charging time and idle time during a transaction.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingTime` | integer | **Yes** |  | Total duration of the charging session (including the duration of charging and not charging), in seconds. |
| `energy` | number | **Yes** |  |  |
| `idleTime` | integer | **Yes** |  | Total duration of the charging session where the EV was not charging (no energy was transferred between EVSE and EV), in seconds. |
| `reservationTime` | integer | No |  | Total time of reservation in seconds. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### TransactionLimitType

Cost, energy, time or SoC limit for a transaction.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `maxCost` | number | No |  | Maximum allowed cost of transaction in currency of tariff. |
| `maxEnergy` | number | No |  | Maximum allowed energy in Wh to charge in transaction. |
| `maxSoC` | integer | No | min: 0.0, max: 100.0 | Maximum State of Charge of EV in percentage. |
| `maxTime` | integer | No |  | Maximum duration of transaction in seconds from start to end. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### TransactionType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | string | **Yes** | maxLength: 36 | This contains the Id of the transaction. |
| `chargingState` | [ChargingStateEnumType](#chargingstateenumtype) | No |  |  |
| `operationMode` | [OperationModeEnumType](../OCPP-2.1-DataTypes.md#operationmodeenumtype) | No |  |  |
| `remoteStartId` | integer | No |  | The ID given to remote start request (RequestStartTransactionRequest. This enables to CSMS to match the started transaction to the given start request. |
| `stoppedReason` | [ReasonEnumType](#reasonenumtype) | No |  |  |
| `tariffId` | string | No | maxLength: 60 | *(2.1)* Id of tariff in use for transaction |
| `timeSpentCharging` | integer | No |  | Contains the total time that energy flowed from EVSE to EV during the transaction (in seconds). Note that timeSpentCharging is smaller or equal to the duration of the transaction. |
| `transactionLimit` | [TransactionLimitType](#transactionlimittype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### UnitOfMeasureType

Represents a UnitOfMeasure with a multiplier

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `multiplier` | integer | No |  | Multiplier, this value represents the exponent to base 10. I.e. multiplier 3 means 10 raised to the 3rd power. Default is 0. + The _multiplier_ only multiplies the value of the measurand. It does not specify a conversion between units, for example, kW and W. Default: `0` |
| `unit` | string | No | maxLength: 20 | Unit of the value. Default = "Wh" if the (default) measurand is an "Energy" type. This field SHALL use a value from the list Standardized Units of Measurements in Part 2 Appendices. If an applicable unit is available in that list, otherwise a "custom" unit might be used. Default: `Wh` |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---
