# OCPP 2.0.1 Schemas — Transactions

> **Functional Block:** D
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [TransactionEvent](#transactionevent) (CS → CSMS)
- [RequestStartTransaction](#requeststarttransaction) (CSMS → CS)
- [RequestStopTransaction](#requeststoptransaction) (CSMS → CS)
- [GetTransactionStatus](#gettransactionstatus) (CSMS → CS)
- [MeterValues](#metervalues) (CS → CSMS)

---

## TransactionEvent

**Direction:** CS → CSMS

### TransactionEventRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `eventType` | [TransactionEventEnumType](#transactioneventenumtype) | **Yes** |  |  |
| `seqNo` | integer | **Yes** |  | Incremental sequence number, helps with determining if all messages of a transaction have been received. |
| `timestamp` | string (date-time) | **Yes** |  | The date and time at which this transaction event occurred. |
| `transactionInfo` | [TransactionType](#transactiontype) | **Yes** |  |  |
| `triggerReason` | [TriggerReasonEnumType](#triggerreasonenumtype) | **Yes** |  |  |
| `cableMaxCurrent` | integer | No |  | The maximum current of the connected cable in Ampere (A). |
| `evse` | [EVSEType](../OCPP-2.0.1-DataTypes.md#evsetype) | No |  |  |
| `idToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | No |  |  |
| `meterValue` | [MeterValueType](#metervaluetype)[] | No | minItems: 1 |  |
| `numberOfPhasesUsed` | integer | No |  | If the Charging Station is able to report the number of phases used, then it SHALL provide it. When omitted the CSMS may be able to determine the number of phases used via device management. |
| `offline` | boolean | No |  | Indication that this transaction event happened when the Charging Station was offline. Default = false, meaning: the event occurred when the Charging Station was online. Default: `False` |
| `reservationId` | integer | No |  | This contains the Id of the reservation that terminates as a result of this transaction. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


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
  "triggerReason": "Authorized"
}
```

</details>

### TransactionEventResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingPriority` | integer | No |  | Priority from a business point of view. Default priority is 0, The range is from -9 to 9. Higher values indicate a higher priority. The chargingPriority in TransactionEventResponse is temporarily, so it may not be set in the IdTokenInfoType afterwards. Also the chargingPriority in TransactionEventResponse overrules the one in IdTokenInfoType. |
| `idTokenInfo` | [IdTokenInfoType](../OCPP-2.0.1-DataTypes.md#idtokeninfotype) | No |  |  |
| `totalCost` | number | No |  | SHALL only be sent when charging has ended. Final total cost of this transaction, including taxes. In the currency configured with the Configuration Variable: Currency. When omitted, the transaction was NOT free. To indicate a free transaction, the CSMS SHALL send 0.00. |
| `updatedPersonalMessage` | [MessageContentType](../OCPP-2.0.1-DataTypes.md#messagecontenttype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


*No fields are required. An empty `{}` is a valid response.*

---

## RequestStartTransaction

**Direction:** CSMS → CS

### RequestStartTransactionRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `remoteStartId` | integer | **Yes** |  | Id given by the server to this start request. The Charging Station might return this in the TransactionEventRequest, letting the server know which transaction was started for this request. Use to start a transaction. |
| `chargingProfile` | [ChargingProfileType](../OCPP-2.0.1-DataTypes.md#chargingprofiletype) | No |  |  |
| `evseId` | integer | No |  | Number of the EVSE on which to start the transaction. EvseId SHALL be > 0 |
| `groupIdToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example RequestStartTransactionRequest</summary>

```json
{
  "idToken": {
    "idToken": "string",
    "type": "Central"
  },
  "remoteStartId": 0
}
```

</details>

### RequestStartTransactionResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [RequestStartStopStatusEnumType](#requeststartstopstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `transactionId` | string | No | maxLength: 36 | When the transaction was already started by the Charging Station before the RequestStartTransactionRequest was received, for example: cable plugged in first. This contains the transactionId of the already started transaction. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## RequestStopTransaction

**Direction:** CSMS → CS

### RequestStopTransactionRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | string | **Yes** | maxLength: 36 | The identifier of the transaction which the Charging Station is requested to stop. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example RequestStopTransactionRequest</summary>

```json
{
  "transactionId": "string"
}
```

</details>

### RequestStopTransactionResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [RequestStartStopStatusEnumType](#requeststartstopstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetTransactionStatus

**Direction:** CSMS → CS

### GetTransactionStatusRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | string | No | maxLength: 36 | The Id of the transaction for which the status is requested. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


### GetTransactionStatusResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `messagesInQueue` | boolean | **Yes** |  | Whether there are still message to be delivered. |
| `ongoingIndicator` | boolean | No |  | Whether the transaction is still ongoing. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## MeterValues

**Direction:** CS → CSMS

### MeterValuesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | **Yes** |  | This contains a number (>0) designating an EVSE of the Charging Station. ‘0’ (zero) is used to designate the main power meter. |
| `meterValue` | [MeterValueType](#metervaluetype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example MeterValuesRequest</summary>

```json
{
  "evseId": 0,
  "meterValue": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "sampledValue": [
        "{...}"
      ]
    }
  ]
}
```

</details>

### MeterValuesResponse

*No required fields. An empty `{}` is a valid response.*

---

## Local Types

*Types used only within this block's messages.*

### ChargingStateEnumType

Current charging state, is required when state has changed.

| Value |
|-------|
| `Charging` |
| `EVConnected` |
| `SuspendedEV` |
| `SuspendedEVSE` |
| `Idle` |

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

**Used in:** MeterValues, TransactionEvent

---

### MeasurandEnumType

Type of measurement. Default = "Energy.Active.Import.Register"

**Default:** `Energy.Active.Import.Register`

| Value |
|-------|
| `Current.Export` |
| `Current.Import` |
| `Current.Offered` |
| `Energy.Active.Export.Register` |
| `Energy.Active.Import.Register` |
| `Energy.Reactive.Export.Register` |
| `Energy.Reactive.Import.Register` |
| `Energy.Active.Export.Interval` |
| `Energy.Active.Import.Interval` |
| `Energy.Active.Net` |
| `Energy.Reactive.Export.Interval` |
| `Energy.Reactive.Import.Interval` |
| `Energy.Reactive.Net` |
| `Energy.Apparent.Net` |
| `Energy.Apparent.Import` |
| `Energy.Apparent.Export` |
| `Frequency` |
| `Power.Active.Export` |
| `Power.Active.Import` |
| `Power.Factor` |
| `Power.Offered` |
| `Power.Reactive.Export` |
| `Power.Reactive.Import` |
| `SoC` |
| `Voltage` |

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

This contains the reason why the transaction was stopped. MAY only be omitted when Reason is "Local".

| Value |
|-------|
| `DeAuthorized` |
| `EmergencyStop` |
| `EnergyLimitReached` |
| `EVDisconnected` |
| `GroundFault` |
| `ImmediateReset` |
| `Local` |
| `LocalOutOfCredit` |
| `MasterPass` |
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

**Used in:** TransactionEvent

---

### RequestStartStopStatusEnumType

Status indicating whether the Charging Station accepts the request to start a transaction.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** RequestStartTransaction, RequestStopTransaction

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
| `Authorized` |
| `CablePluggedIn` |
| `ChargingRateChanged` |
| `ChargingStateChanged` |
| `Deauthorized` |
| `EnergyLimitReached` |
| `EVCommunicationLost` |
| `EVConnectTimeout` |
| `MeterValueClock` |
| `MeterValuePeriodic` |
| `TimeLimitReached` |
| `Trigger` |
| `UnlockCommand` |
| `StopAuthorized` |
| `EVDeparted` |
| `EVDetected` |
| `RemoteStop` |
| `RemoteStart` |
| `AbnormalCondition` |
| `SignedDataReceived` |
| `ResetCommand` |

**Used in:** TransactionEvent

---

### MeterValueType

Collection of one or more sampled values in MeterValuesRequest and TransactionEvent. All sampled values in a MeterValue are sampled at the same point in time.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `sampledValue` | [SampledValueType](#sampledvaluetype)[] | **Yes** | minItems: 1 |  |
| `timestamp` | string (date-time) | **Yes** |  | Timestamp for measured value(s). |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


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
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---

### SignedMeterValueType

Represent a signed version of the meter value.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `encodingMethod` | string | **Yes** | maxLength: 50 | Method used to encode the meter values before applying the digital signature algorithm. |
| `publicKey` | string | **Yes** | maxLength: 2500 | Base64 encoded, sending depends on configuration variable _PublicKeyWithSignedMeterValue_. |
| `signedMeterData` | string | **Yes** | maxLength: 2500 | Base64 encoded, contains the signed data which might contain more then just the meter value. It can contain information like timestamps, reference to a customer etc. |
| `signingMethod` | string | **Yes** | maxLength: 50 | Method used to create the digital signature. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---

### TransactionType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | string | **Yes** | maxLength: 36 | This contains the Id of the transaction. |
| `chargingState` | [ChargingStateEnumType](#chargingstateenumtype) | No |  |  |
| `remoteStartId` | integer | No |  | The ID given to remote start request (RequestStartTransactionRequest. This enables to CSMS to match the started transaction to the given start request. |
| `stoppedReason` | [ReasonEnumType](#reasonenumtype) | No |  |  |
| `timeSpentCharging` | integer | No |  | Contains the total time that energy flowed from EVSE to EV during the transaction (in seconds). Note that timeSpentCharging is smaller or equal to the duration of the transaction. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** TransactionEvent

---

### UnitOfMeasureType

Represents a UnitOfMeasure with a multiplier

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `multiplier` | integer | No |  | Multiplier, this value represents the exponent to base 10. I.e. multiplier 3 means 10 raised to the 3rd power. Default is 0. Default: `0` |
| `unit` | string | No | maxLength: 20 | Unit of the value. Default = "Wh" if the (default) measurand is an "Energy" type. This field SHALL use a value from the list Standardized Units of Measurements in Part 2 Appendices. If an applicable unit is available in that list, otherwise a "custom" unit might be used. Default: `Wh` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---
