# OCPP 2.1 Schemas — MeterValues

> **Functional Block:** J
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [MeterValues](#metervalues) (CS → CSMS)

---

## MeterValues

**Direction:** CS → CSMS

### MeterValuesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | **Yes** | min: 0.0 | This contains a number (>0) designating an EVSE of the Charging Station. ‘0’ (zero) is used to designate the main power meter. |
| `meterValue` | [MeterValueType](#metervaluetype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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

### UnitOfMeasureType

Represents a UnitOfMeasure with a multiplier

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `multiplier` | integer | No |  | Multiplier, this value represents the exponent to base 10. I.e. multiplier 3 means 10 raised to the 3rd power. Default is 0. + The _multiplier_ only multiplies the value of the measurand. It does not specify a conversion between units, for example, kW and W. Default: `0` |
| `unit` | string | No | maxLength: 20 | Unit of the value. Default = "Wh" if the (default) measurand is an "Energy" type. This field SHALL use a value from the list Standardized Units of Measurements in Part 2 Appendices. If an applicable unit is available in that list, otherwise a "custom" unit might be used. Default: `Wh` |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** MeterValues, TransactionEvent

---
