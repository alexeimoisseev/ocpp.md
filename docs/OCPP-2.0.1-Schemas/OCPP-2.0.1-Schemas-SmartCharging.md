# OCPP 2.0.1 Schemas — SmartCharging

> **Functional Block:** H
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).
>
> **Deep-dive:** For conceptual explanations, composite schedule calculation, worked examples, and implementation guidance, see the [Smart Charging Deep-Dive](../OCPP-2.0.1-SmartCharging/OCPP-2.0.1-SmartCharging.md).

## Messages

- [SetChargingProfile](#setchargingprofile) (CSMS → CS)
- [GetChargingProfiles](#getchargingprofiles) (CSMS → CS)
- [ClearChargingProfile](#clearchargingprofile) (CSMS → CS)
- [ReportChargingProfiles](#reportchargingprofiles) (CS → CSMS)
- [GetCompositeSchedule](#getcompositeschedule) (CSMS → CS)
- [ClearedChargingLimit](#clearedcharginglimit) (CS → CSMS)
- [NotifyChargingLimit](#notifycharginglimit) (CS → CSMS)
- [NotifyEVChargingSchedule](#notifyevchargingschedule) (CS → CSMS)
- [NotifyEVChargingNeeds](#notifyevchargingneeds) (CS → CSMS)

---

## SetChargingProfile

**Direction:** CSMS → CS

### SetChargingProfileRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfile` | [ChargingProfileType](../OCPP-2.0.1-DataTypes.md#chargingprofiletype) | **Yes** |  |  |
| `evseId` | integer | **Yes** |  | For TxDefaultProfile an evseId=0 applies the profile to each individual evse. For ChargingStationMaxProfile and ChargingStationExternalConstraints an evseId=0 contains an overal limit for the whole Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetChargingProfileRequest</summary>

```json
{
  "chargingProfile": {
    "id": 0,
    "stackLevel": 0,
    "chargingProfilePurpose": "ChargingStationExternalConstraints",
    "chargingProfileKind": "Absolute",
    "chargingSchedule": [
      "{...}"
    ]
  },
  "evseId": 0
}
```

</details>

### SetChargingProfileResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ChargingProfileStatusEnumType](#chargingprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetChargingProfiles

**Direction:** CSMS → CS

### GetChargingProfilesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfile` | [ChargingProfileCriterionType](#chargingprofilecriteriontype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | Reference identification that is to be used by the Charging Station in the ReportChargingProfilesRequest when provided. |
| `evseId` | integer | No |  | For which EVSE installed charging profiles SHALL be reported. If 0, only charging profiles installed on the Charging Station itself (the grid connection) SHALL be reported. If omitted, all installed charging profiles SHALL be reported. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetChargingProfilesRequest</summary>

```json
{
  "chargingProfile": {},
  "requestId": 0
}
```

</details>

### GetChargingProfilesResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GetChargingProfileStatusEnumType](#getchargingprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearChargingProfile

**Direction:** CSMS → CS

### ClearChargingProfileRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileCriteria` | [ClearChargingProfileType](#clearchargingprofiletype) | No |  |  |
| `chargingProfileId` | integer | No |  | The Id of the charging profile to clear. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


### ClearChargingProfileResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ClearChargingProfileStatusEnumType](#clearchargingprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ReportChargingProfiles

**Direction:** CS → CSMS

### ReportChargingProfilesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | [ChargingLimitSourceEnumType](../OCPP-2.0.1-DataTypes.md#charginglimitsourceenumtype) | **Yes** |  |  |
| `chargingProfile` | [ChargingProfileType](../OCPP-2.0.1-DataTypes.md#chargingprofiletype)[] | **Yes** | minItems: 1 |  |
| `evseId` | integer | **Yes** |  | The evse to which the charging profile applies. If evseId = 0, the message contains an overall limit for the Charging Station. |
| `requestId` | integer | **Yes** |  | Id used to match the GetChargingProfilesRequest message with the resulting ReportChargingProfilesRequest messages. When the CSMS provided a requestId in the GetChargingProfilesRequest, this field SHALL contain the same value. |
| `tbc` | boolean | No |  | To Be Continued. Default value when omitted: false. false indicates that there are no further messages as part of this report. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ReportChargingProfilesRequest</summary>

```json
{
  "chargingLimitSource": "EMS",
  "chargingProfile": [
    {
      "id": 0,
      "stackLevel": 0,
      "chargingProfilePurpose": "ChargingStationExternalConstraints",
      "chargingProfileKind": "Absolute",
      "chargingSchedule": [
        "{...}"
      ]
    }
  ],
  "evseId": 0,
  "requestId": 0
}
```

</details>

### ReportChargingProfilesResponse

*No required fields. An empty `{}` is a valid response.*

---

## GetCompositeSchedule

**Direction:** CSMS → CS

### GetCompositeScheduleRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `duration` | integer | **Yes** |  | Length of the requested schedule in seconds. |
| `evseId` | integer | **Yes** |  | The ID of the EVSE for which the schedule is requested. When evseid=0, the Charging Station will calculate the expected consumption for the grid connection. |
| `chargingRateUnit` | [ChargingRateUnitEnumType](../OCPP-2.0.1-DataTypes.md#chargingrateunitenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetCompositeScheduleRequest</summary>

```json
{
  "duration": 0,
  "evseId": 0
}
```

</details>

### GetCompositeScheduleResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `schedule` | [CompositeScheduleType](#compositescheduletype) | No |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearedChargingLimit

**Direction:** CS → CSMS

### ClearedChargingLimitRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | [ChargingLimitSourceEnumType](../OCPP-2.0.1-DataTypes.md#charginglimitsourceenumtype) | **Yes** |  |  |
| `evseId` | integer | No |  | EVSE Identifier. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ClearedChargingLimitRequest</summary>

```json
{
  "chargingLimitSource": "EMS"
}
```

</details>

### ClearedChargingLimitResponse

*No required fields. An empty `{}` is a valid response.*

---

## NotifyChargingLimit

**Direction:** CS → CSMS

### NotifyChargingLimitRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimit` | [ChargingLimitType](#charginglimittype) | **Yes** |  |  |
| `chargingSchedule` | [ChargingScheduleType](../OCPP-2.0.1-DataTypes.md#chargingscheduletype)[] | No | minItems: 1 |  |
| `evseId` | integer | No |  | The charging schedule contained in this notification applies to an EVSE. evseId must be > 0. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyChargingLimitRequest</summary>

```json
{
  "chargingLimit": {
    "chargingLimitSource": "EMS"
  }
}
```

</details>

### NotifyChargingLimitResponse

*No required fields. An empty `{}` is a valid response.*

---

## NotifyEVChargingSchedule

**Direction:** CS → CSMS

### NotifyEVChargingScheduleRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingSchedule` | [ChargingScheduleType](../OCPP-2.0.1-DataTypes.md#chargingscheduletype) | **Yes** |  |  |
| `evseId` | integer | **Yes** |  | The charging schedule contained in this notification applies to an EVSE. EvseId must be > 0. |
| `timeBase` | string (date-time) | **Yes** |  | Periods contained in the charging profile are relative to this point in time. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyEVChargingScheduleRequest</summary>

```json
{
  "chargingSchedule": {
    "id": 0,
    "chargingRateUnit": "W",
    "chargingSchedulePeriod": [
      "{...}"
    ]
  },
  "evseId": 0,
  "timeBase": "2024-01-15T10:30:00Z"
}
```

</details>

### NotifyEVChargingScheduleResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyEVChargingNeeds

**Direction:** CS → CSMS

### NotifyEVChargingNeedsRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingNeeds` | [ChargingNeedsType](#chargingneedstype) | **Yes** |  |  |
| `evseId` | integer | **Yes** |  | Defines the EVSE and connector to which the EV is connected. EvseId may not be 0. |
| `maxScheduleTuples` | integer | No |  | Contains the maximum schedule tuples the car supports per schedule. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyEVChargingNeedsRequest</summary>

```json
{
  "chargingNeeds": {
    "requestedEnergyTransfer": "DC"
  },
  "evseId": 0
}
```

</details>

### NotifyEVChargingNeedsResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [NotifyEVChargingNeedsStatusEnumType](#notifyevchargingneedsstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### ChargingProfileStatusEnumType

Returns whether the Charging Station has been able to process the message successfully. This does not guarantee the schedule will be followed to the letter. There might be other constraints the Charging Station may need to take into account.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** SetChargingProfile

---

### ClearChargingProfileStatusEnumType

Indicates if the Charging Station was able to execute the request.

| Value |
|-------|
| `Accepted` |
| `Unknown` |

**Used in:** ClearChargingProfile

---

### EnergyTransferModeEnumType

Mode of energy transfer requested by the EV.

| Value |
|-------|
| `DC` |
| `AC_single_phase` |
| `AC_two_phase` |
| `AC_three_phase` |

**Used in:** NotifyEVChargingNeeds

---

### GetChargingProfileStatusEnumType

This indicates whether the Charging Station is able to process this request and will send ReportChargingProfilesRequest messages.

| Value |
|-------|
| `Accepted` |
| `NoProfiles` |

**Used in:** GetChargingProfiles

---

### NotifyEVChargingNeedsStatusEnumType

Returns whether the CSMS has been able to process the message successfully. It does not imply that the evChargingNeeds can be met with the current charging profile.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Processing` |

**Used in:** NotifyEVChargingNeeds

---

### ACChargingParametersType

EV AC charging parameters.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `energyAmount` | integer | **Yes** |  | Amount of energy requested (in Wh). This includes energy required for preconditioning. |
| `evMaxCurrent` | integer | **Yes** |  | Maximum current (amps) supported by the electric vehicle (per phase). Includes cable capacity. |
| `evMaxVoltage` | integer | **Yes** |  | Maximum voltage supported by the electric vehicle |
| `evMinCurrent` | integer | **Yes** |  | Minimum current (amps) supported by the electric vehicle (per phase). |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### ChargingLimitType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | [ChargingLimitSourceEnumType](../OCPP-2.0.1-DataTypes.md#charginglimitsourceenumtype) | **Yes** |  |  |
| `isGridCritical` | boolean | No |  | Indicates whether the charging limit is critical for the grid. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit

---

### ChargingNeedsType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestedEnergyTransfer` | [EnergyTransferModeEnumType](#energytransfermodeenumtype) | **Yes** |  |  |
| `acChargingParameters` | [ACChargingParametersType](#acchargingparameterstype) | No |  |  |
| `dcChargingParameters` | [DCChargingParametersType](#dcchargingparameterstype) | No |  |  |
| `departureTime` | string (date-time) | No |  | Estimated departure time of the EV. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### ChargingProfileCriterionType

A ChargingProfile consists of ChargingSchedule, describing the amount of power or current that can be delivered per time interval.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | [ChargingLimitSourceEnumType](../OCPP-2.0.1-DataTypes.md#charginglimitsourceenumtype)[] | No | minItems: 1, maxItems: 4 | For which charging limit sources, charging profiles SHALL be reported. If omitted, the Charging Station SHALL not filter on chargingLimitSource. |
| `chargingProfileId` | integer[] | No | minItems: 1 | List of all the chargingProfileIds requested. Any ChargingProfile that matches one of these profiles will be reported. If omitted, the Charging Station SHALL not filter on chargingProfileId. This field SHALL NOT contain more ids than set in ChargingProfileEntries.maxLimit |
| `chargingProfilePurpose` | [ChargingProfilePurposeEnumType](../OCPP-2.0.1-DataTypes.md#chargingprofilepurposeenumtype) | No |  |  |
| `stackLevel` | integer | No |  | Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetChargingProfiles

---

### ClearChargingProfileType

A ChargingProfile consists of a ChargingSchedule, describing the amount of power or current that can be delivered per time interval.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfilePurpose` | [ChargingProfilePurposeEnumType](../OCPP-2.0.1-DataTypes.md#chargingprofilepurposeenumtype) | No |  |  |
| `evseId` | integer | No |  | Specifies the id of the EVSE for which to clear charging profiles. An evseId of zero (0) specifies the charging profile for the overall Charging Station. Absence of this parameter means the clearing applies to all charging profiles that match the other criteria in the request. |
| `stackLevel` | integer | No |  | Specifies the stackLevel for which charging profiles will be cleared, if they meet the other criteria in the request. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ClearChargingProfile

---

### CompositeScheduleType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingRateUnit` | [ChargingRateUnitEnumType](../OCPP-2.0.1-DataTypes.md#chargingrateunitenumtype) | **Yes** |  |  |
| `chargingSchedulePeriod` | [ChargingSchedulePeriodType](../OCPP-2.0.1-DataTypes.md#chargingscheduleperiodtype)[] | **Yes** | minItems: 1 |  |
| `duration` | integer | **Yes** |  | Duration of the schedule in seconds. |
| `evseId` | integer | **Yes** |  | The ID of the EVSE for which the schedule is requested. When evseid=0, the Charging Station calculated the expected consumption for the grid connection. |
| `scheduleStart` | string (date-time) | **Yes** |  | Date and time at which the schedule becomes active. All time measurements within the schedule are relative to this timestamp. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetCompositeSchedule

---

### DCChargingParametersType

EV DC charging parameters

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evMaxCurrent` | integer | **Yes** |  | Maximum current (amps) supported by the electric vehicle. Includes cable capacity. |
| `evMaxVoltage` | integer | **Yes** |  | Maximum voltage supported by the electric vehicle |
| `bulkSoC` | integer | No | min: 0.0, max: 100.0 | Percentage of SoC at which the EV considers a fast charging process to end. (possible values: 0 - 100) |
| `energyAmount` | integer | No |  | Amount of energy requested (in Wh). This inludes energy required for preconditioning. |
| `evEnergyCapacity` | integer | No |  | Capacity of the electric vehicle battery (in Wh) |
| `evMaxPower` | integer | No |  | Maximum power (in W) supported by the electric vehicle. Required for DC charging. |
| `fullSoC` | integer | No | min: 0.0, max: 100.0 | Percentage of SoC at which the EV considers the battery fully charged. (possible values: 0 - 100) |
| `stateOfCharge` | integer | No | min: 0.0, max: 100.0 | Energy available in the battery (in percent of the battery capacity) |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---
