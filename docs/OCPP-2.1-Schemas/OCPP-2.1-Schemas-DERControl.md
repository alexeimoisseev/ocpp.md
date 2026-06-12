# OCPP 2.1 Schemas — DERControl

> **Functional Block:** R
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [GetDERControl](#getdercontrol) (CSMS → CS)
- [SetDERControl](#setdercontrol) (CSMS → CS)
- [ClearDERControl](#cleardercontrol) (CSMS → CS)
- [ReportDERControl](#reportdercontrol) (CS → CSMS)
- [NotifyDERAlarm](#notifyderalarm) (CS → CSMS)
- [NotifyDERStartStop](#notifyderstartstop) (CS → CSMS)

---

## GetDERControl

**Direction:** CSMS → CS

### GetDERControlRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestId` | integer | **Yes** |  | RequestId to be used in ReportDERControlRequest. |
| `controlId` | string | No | maxLength: 36 | Id of setting to get. When omitted all settings for _controlType_ are retrieved. |
| `controlType` | [DERControlEnumType](../OCPP-2.1-DataTypes.md#dercontrolenumtype) | No |  |  |
| `isDefault` | boolean | No |  | True: get a default DER control. False: get a scheduled control. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetDERControlRequest</summary>

```json
{
  "requestId": 0
}
```

</details>

### GetDERControlResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [DERControlStatusEnumType](../OCPP-2.1-DataTypes.md#dercontrolstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## SetDERControl

**Direction:** CSMS → CS

### SetDERControlRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `controlId` | string | **Yes** | maxLength: 36 | Unique id of this control, e.g. UUID |
| `controlType` | [DERControlEnumType](../OCPP-2.1-DataTypes.md#dercontrolenumtype) | **Yes** |  |  |
| `isDefault` | boolean | **Yes** |  | True if this is a default DER control |
| `curve` | [DERCurveType](#dercurvetype) | No |  |  |
| `enterService` | [EnterServiceType](#enterservicetype) | No |  |  |
| `fixedPFAbsorb` | [FixedPFType](#fixedpftype) | No |  |  |
| `fixedPFInject` | [FixedPFType](#fixedpftype) | No |  |  |
| `fixedVar` | [FixedVarType](#fixedvartype) | No |  |  |
| `freqDroop` | [FreqDroopType](#freqdrooptype) | No |  |  |
| `gradient` | [GradientType](#gradienttype) | No |  |  |
| `limitMaxDischarge` | [LimitMaxDischargeType](#limitmaxdischargetype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetDERControlRequest</summary>

```json
{
  "controlId": "string",
  "controlType": "EnterService",
  "isDefault": false
}
```

</details>

### SetDERControlResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [DERControlStatusEnumType](../OCPP-2.1-DataTypes.md#dercontrolstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `supersededIds` | string[] | No | minItems: 1, maxItems: 24 | List of controlIds that are superseded as a result of setting this control. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearDERControl

**Direction:** CSMS → CS

### ClearDERControlRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `isDefault` | boolean | **Yes** |  | True: clearing default DER controls. False: clearing scheduled controls. |
| `controlId` | string | No | maxLength: 36 | Id of control setting to clear. When omitted all settings for _controlType_ are cleared. |
| `controlType` | [DERControlEnumType](../OCPP-2.1-DataTypes.md#dercontrolenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ClearDERControlRequest</summary>

```json
{
  "isDefault": false
}
```

</details>

### ClearDERControlResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [DERControlStatusEnumType](../OCPP-2.1-DataTypes.md#dercontrolstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ReportDERControl

**Direction:** CS → CSMS

### ReportDERControlRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestId` | integer | **Yes** |  | RequestId from GetDERControlRequest. |
| `curve` | [DERCurveGetType](#dercurvegettype)[] | No | minItems: 1, maxItems: 24 |  |
| `enterService` | [EnterServiceGetType](#enterservicegettype)[] | No | minItems: 1, maxItems: 24 |  |
| `fixedPFAbsorb` | [FixedPFGetType](#fixedpfgettype)[] | No | minItems: 1, maxItems: 24 |  |
| `fixedPFInject` | [FixedPFGetType](#fixedpfgettype)[] | No | minItems: 1, maxItems: 24 |  |
| `fixedVar` | [FixedVarGetType](#fixedvargettype)[] | No | minItems: 1, maxItems: 24 |  |
| `freqDroop` | [FreqDroopGetType](#freqdroopgettype)[] | No | minItems: 1, maxItems: 24 |  |
| `gradient` | [GradientGetType](#gradientgettype)[] | No | minItems: 1, maxItems: 24 |  |
| `limitMaxDischarge` | [LimitMaxDischargeGetType](#limitmaxdischargegettype)[] | No | minItems: 1, maxItems: 24 |  |
| `tbc` | boolean | No |  | To Be Continued. Default value when omitted: false. + False indicates that there are no further messages as part of this report. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ReportDERControlRequest</summary>

```json
{
  "requestId": 0
}
```

</details>

### ReportDERControlResponse

*No required fields. An empty `{}` is a valid response.*

---

## NotifyDERAlarm

**Direction:** CS → CSMS

### NotifyDERAlarmRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `controlType` | [DERControlEnumType](../OCPP-2.1-DataTypes.md#dercontrolenumtype) | **Yes** |  |  |
| `timestamp` | string (date-time) | **Yes** |  | Time of start or end of alarm. |
| `alarmEnded` | boolean | No |  | True when error condition has ended. Absent or false when alarm has started. |
| `extraInfo` | string | No | maxLength: 200 | Optional info provided by EV. |
| `gridEventFault` | [GridEventFaultEnumType](#grideventfaultenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyDERAlarmRequest</summary>

```json
{
  "controlType": "EnterService",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

</details>

### NotifyDERAlarmResponse

*No required fields. An empty `{}` is a valid response.*

---

## NotifyDERStartStop

**Direction:** CS → CSMS

### NotifyDERStartStopRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `controlId` | string | **Yes** | maxLength: 36 | Id of the started or stopped DER control. Corresponds to the _controlId_ of the SetDERControlRequest. |
| `started` | boolean | **Yes** |  | True if DER control has started. False if it has ended. |
| `timestamp` | string (date-time) | **Yes** |  | Time of start or end of event. |
| `supersededIds` | string[] | No | minItems: 1, maxItems: 24 | List of controlIds that are superseded as a result of this control starting. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyDERStartStopRequest</summary>

```json
{
  "controlId": "string",
  "started": false,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

</details>

### NotifyDERStartStopResponse

*No required fields. An empty `{}` is a valid response.*

---

## Local Types

*Types used only within this block's messages.*

### DERUnitEnumType

Unit of the Y-axis of DER curve

| Value |
|-------|
| `Not_Applicable` |
| `PctMaxW` |
| `PctMaxVar` |
| `PctWAvail` |
| `PctVarAvail` |
| `PctEffectiveV` |

**Used in:** ReportDERControl, SetDERControl

---

### GridEventFaultEnumType

Type of grid event that caused this

| Value |
|-------|
| `CurrentImbalance` |
| `LocalEmergency` |
| `LowInputPower` |
| `OverCurrent` |
| `OverFrequency` |
| `OverVoltage` |
| `PhaseRotation` |
| `RemoteEmergency` |
| `UnderFrequency` |
| `UnderVoltage` |
| `VoltageImbalance` |

**Used in:** NotifyDERAlarm

---

### PowerDuringCessationEnumType

Parameter is only sent, if the EV has to feed-in power or reactive power during fault-ride through (FRT) as defined by HVMomCess curve and LVMomCess curve.

| Value |
|-------|
| `Active` |
| `Reactive` |

**Used in:** ReportDERControl, SetDERControl

---

### DERCurveGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `curve` | [DERCurveType](#dercurvetype) | **Yes** |  |  |
| `curveType` | [DERControlEnumType](../OCPP-2.1-DataTypes.md#dercontrolenumtype) | **Yes** |  |  |
| `id` | string | **Yes** | maxLength: 36 | Id of DER curve |
| `isDefault` | boolean | **Yes** |  | True if this is a default curve |
| `isSuperseded` | boolean | **Yes** |  | True if this setting is superseded by a higher priority setting (i.e. lower value of _priority_) |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### DERCurvePointsType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `x` | number | **Yes** |  | The data value of the X-axis (independent) variable, depending on the curve type. |
| `y` | number | **Yes** |  | The data value of the Y-axis (dependent) variable, depending on the of the curve. If _y_ is power factor, then a positive value means DER is absorbing reactive power (under-excited), a negative value when DER is injecting reactive power (over-excited). |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### DERCurveType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `curveData` | [DERCurvePointsType](#dercurvepointstype)[] | **Yes** | minItems: 1, maxItems: 10 |  |
| `priority` | integer | **Yes** | min: 0.0 | Priority of curve (0=highest) |
| `yUnit` | [DERUnitEnumType](#derunitenumtype) | **Yes** |  |  |
| `duration` | number | No |  | Duration in seconds that this curve will be active. Only absent when _default_ is true. |
| `hysteresis` | [HysteresisType](#hysteresistype) | No |  |  |
| `reactivePowerParams` | [ReactivePowerParamsType](#reactivepowerparamstype) | No |  |  |
| `responseTime` | number | No |  | Open loop response time, the time to ramp up to 90% of the new target in response to the change in voltage, in seconds. A value of 0 is used to mean no limit. When not present, the device should follow its default behavior. |
| `startTime` | string (date-time) | No |  | Point in time when this curve will become activated. Only absent when _default_ is true. |
| `voltageParams` | [VoltageParamsType](#voltageparamstype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### EnterServiceGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `enterService` | [EnterServiceType](#enterservicetype) | **Yes** |  |  |
| `id` | string | **Yes** | maxLength: 36 | Id of setting |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### EnterServiceType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `highFreq` | number | **Yes** |  | Enter service frequency high |
| `highVoltage` | number | **Yes** |  | Enter service voltage high |
| `lowFreq` | number | **Yes** |  | Enter service frequency low |
| `lowVoltage` | number | **Yes** |  | Enter service voltage low |
| `priority` | integer | **Yes** | min: 0.0 | Priority of setting (0=highest) |
| `delay` | number | No |  | Enter service delay |
| `rampRate` | number | No |  | Enter service ramp rate in seconds |
| `randomDelay` | number | No |  | Enter service randomized delay |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### FixedPFGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `fixedPF` | [FixedPFType](#fixedpftype) | **Yes** |  |  |
| `id` | string | **Yes** | maxLength: 36 | Id of setting. |
| `isDefault` | boolean | **Yes** |  | True if setting is a default control. |
| `isSuperseded` | boolean | **Yes** |  | True if this setting is superseded by a lower priority setting. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### FixedPFType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `displacement` | number | **Yes** |  | Power factor, cos(phi), as value between 0..1. |
| `excitation` | boolean | **Yes** |  | True when absorbing reactive power (under-excited), false when injecting reactive power (over-excited). |
| `priority` | integer | **Yes** | min: 0.0 | Priority of setting (0=highest) |
| `duration` | number | No |  | Duration in seconds that this setting is active. |
| `startTime` | string (date-time) | No |  | Time when this setting becomes active |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### FixedVarGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `fixedVar` | [FixedVarType](#fixedvartype) | **Yes** |  |  |
| `id` | string | **Yes** | maxLength: 36 | Id of setting |
| `isDefault` | boolean | **Yes** |  | True if setting is a default control. |
| `isSuperseded` | boolean | **Yes** |  | True if this setting is superseded by a lower priority setting |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### FixedVarType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `priority` | integer | **Yes** | min: 0.0 | Priority of setting (0=highest) |
| `setpoint` | number | **Yes** |  | The value specifies a target var output interpreted as a signed percentage (-100 to 100). A negative value refers to charging, whereas a positive one refers to discharging. The value type is determined by the unit field. |
| `unit` | [DERUnitEnumType](#derunitenumtype) | **Yes** |  |  |
| `duration` | number | No |  | Duration in seconds that this setting is active. |
| `startTime` | string (date-time) | No |  | Time when this setting becomes active. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### FreqDroopGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `freqDroop` | [FreqDroopType](#freqdrooptype) | **Yes** |  |  |
| `id` | string | **Yes** | maxLength: 36 | Id of setting |
| `isDefault` | boolean | **Yes** |  | True if setting is a default control. |
| `isSuperseded` | boolean | **Yes** |  | True if this setting is superseded by a higher priority setting (i.e. lower value of _priority_) |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### FreqDroopType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `overDroop` | number | **Yes** |  | Over-frequency droop per unit, oFDroop |
| `overFreq` | number | **Yes** |  | Over-frequency start of droop |
| `priority` | integer | **Yes** | min: 0.0 | Priority of setting (0=highest) |
| `responseTime` | number | **Yes** |  | Open loop response time in seconds |
| `underDroop` | number | **Yes** |  | Under-frequency droop per unit, uFDroop |
| `underFreq` | number | **Yes** |  | Under-frequency start of droop |
| `duration` | number | No |  | Duration in seconds that this setting is active |
| `startTime` | string (date-time) | No |  | Time when this setting becomes active |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### GradientGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `gradient` | [GradientType](#gradienttype) | **Yes** |  |  |
| `id` | string | **Yes** | maxLength: 36 | Id of setting |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### GradientType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `gradient` | number | **Yes** |  | Default ramp rate in seconds (0 if not applicable) |
| `priority` | integer | **Yes** | min: 0.0 | Id of setting |
| `softGradient` | number | **Yes** |  | Soft-start ramp rate in seconds (0 if not applicable) |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### HysteresisType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `hysteresisDelay` | number | No |  | Delay in seconds, once grid parameter within HysteresisLow and HysteresisHigh, for the EV to return to normal operation after a grid event. |
| `hysteresisGradient` | number | No |  | Set default rate of change (ramp rate %/s) for the EV to return to normal operation after a grid event |
| `hysteresisHigh` | number | No |  | High value for return to normal operation after a grid event, in absolute value. This value adopts the same unit as defined by yUnit |
| `hysteresisLow` | number | No |  | Low value for return to normal operation after a grid event, in absolute value. This value adopts the same unit as defined by yUnit |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### LimitMaxDischargeGetType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | string | **Yes** | maxLength: 36 | Id of setting |
| `isDefault` | boolean | **Yes** |  | True if setting is a default control. |
| `isSuperseded` | boolean | **Yes** |  | True if this setting is superseded by a higher priority setting (i.e. lower value of _priority_) |
| `limitMaxDischarge` | [LimitMaxDischargeType](#limitmaxdischargetype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl

---

### LimitMaxDischargeType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `priority` | integer | **Yes** | min: 0.0 | Priority of setting (0=highest) |
| `duration` | number | No |  | Duration in seconds that this setting is active |
| `pctMaxDischargePower` | number | No |  | Only for PowerMonitoring. + The value specifies a percentage (0 to 100) of the rated maximum discharge power of EV. The PowerMonitoring curve becomes active when power exceeds this percentage. |
| `powerMonitoringMustTrip` | [DERCurveType](#dercurvetype) | No |  |  |
| `startTime` | string (date-time) | No |  | Time when this setting becomes active |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### ReactivePowerParamsType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `autonomousVRefEnable` | boolean | No |  | Only for VoltVar: Enable/disable autonomous VRef adjustment |
| `autonomousVRefTimeConstant` | number | No |  | Only for VoltVar: Adjustment range for VRef time constant |
| `vRef` | number | No |  | Only for VoltVar curve: The nominal ac voltage (rms) adjustment to the voltage curve points for Volt-Var curves (percentage). |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---

### VoltageParamsType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `hv10MinMeanTripDelay` | number | No |  | Time for which the voltage is allowed to stay above the 10 min mean value. After this time, the EV must trip. This value is mandatory if OverVoltageMeanValue10min is set. |
| `hv10MinMeanValue` | number | No |  | EN 50549-1 chapter 4.9.3.4 Voltage threshold for the 10 min time window mean value monitoring. The 10 min mean is recalculated up to every 3 s. If the present voltage is above this threshold for more than the time defined by _hv10MinMeanValue_, the EV must trip. This value is mandatory if _hv10MinMeanTripDelay_ is set. |
| `powerDuringCessation` | [PowerDuringCessationEnumType](#powerduringcessationenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ReportDERControl, SetDERControl

---
