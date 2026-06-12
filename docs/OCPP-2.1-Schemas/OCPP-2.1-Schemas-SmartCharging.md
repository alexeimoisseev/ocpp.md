# OCPP 2.1 Schemas — SmartCharging

> **Functional Block:** K
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

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
- [PullDynamicScheduleUpdate](#pulldynamicscheduleupdate) (CS → CSMS)
- [UpdateDynamicSchedule](#updatedynamicschedule) (CSMS → CS)
- [NotifyPriorityCharging](#notifyprioritycharging) (CS → CSMS)
- [UsePriorityCharging](#useprioritycharging) (CSMS → CS)

---

## SetChargingProfile

**Direction:** CSMS → CS

### SetChargingProfileRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfile` | [ChargingProfileType](../OCPP-2.1-DataTypes.md#chargingprofiletype) | **Yes** |  |  |
| `evseId` | integer | **Yes** | min: 0.0 | For TxDefaultProfile an evseId=0 applies the profile to each individual evse. For ChargingStationMaxProfile and ChargingStationExternalConstraints an evseId=0 contains an overal limit for the whole Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `status` | [ChargingProfileStatusEnumType](../OCPP-2.1-DataTypes.md#chargingprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetChargingProfiles

**Direction:** CSMS → CS

### GetChargingProfilesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfile` | [ChargingProfileCriterionType](#chargingprofilecriteriontype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | Reference identification that is to be used by the Charging Station in the ReportChargingProfilesRequest when provided. |
| `evseId` | integer | No | min: 0.0 | For which EVSE installed charging profiles SHALL be reported. If 0, only charging profiles installed on the Charging Station itself (the grid connection) SHALL be reported. If omitted, all installed charging profiles SHALL be reported. + Reported charging profiles SHALL match the criteria in field _chargingProfile_. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearChargingProfile

**Direction:** CSMS → CS

### ClearChargingProfileRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileCriteria` | [ClearChargingProfileType](#clearchargingprofiletype) | No |  |  |
| `chargingProfileId` | integer | No |  | The Id of the charging profile to clear. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### ClearChargingProfileResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ClearChargingProfileStatusEnumType](#clearchargingprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ReportChargingProfiles

**Direction:** CS → CSMS

### ReportChargingProfilesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | string | **Yes** | maxLength: 20 | Source that has installed this charging profile. Values defined in Appendix as ChargingLimitSourceEnumStringType. |
| `chargingProfile` | [ChargingProfileType](../OCPP-2.1-DataTypes.md#chargingprofiletype)[] | **Yes** | minItems: 1 |  |
| `evseId` | integer | **Yes** | min: 0.0 | The evse to which the charging profile applies. If evseId = 0, the message contains an overall limit for the Charging Station. |
| `requestId` | integer | **Yes** |  | Id used to match the GetChargingProfilesRequest message with the resulting ReportChargingProfilesRequest messages. When the CSMS provided a requestId in the GetChargingProfilesRequest, this field SHALL contain the same value. |
| `tbc` | boolean | No |  | To Be Continued. Default value when omitted: false. false indicates that there are no further messages as part of this report. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ReportChargingProfilesRequest</summary>

```json
{
  "chargingLimitSource": "string",
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
| `evseId` | integer | **Yes** | min: 0.0 | The ID of the EVSE for which the schedule is requested. When evseid=0, the Charging Station will calculate the expected consumption for the grid connection. |
| `chargingRateUnit` | [ChargingRateUnitEnumType](../OCPP-2.1-DataTypes.md#chargingrateunitenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `status` | [GenericStatusEnumType](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `schedule` | [CompositeScheduleType](#compositescheduletype) | No |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearedChargingLimit

**Direction:** CS → CSMS

### ClearedChargingLimitRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | string | **Yes** | maxLength: 20 | Source of the charging limit. Allowed values defined in Appendix as ChargingLimitSourceEnumStringType. |
| `evseId` | integer | No | min: 0.0 | EVSE Identifier. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ClearedChargingLimitRequest</summary>

```json
{
  "chargingLimitSource": "string"
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
| `chargingSchedule` | [ChargingScheduleType](../OCPP-2.1-DataTypes.md#chargingscheduletype)[] | No | minItems: 1 |  |
| `evseId` | integer | No | min: 0.0 | The EVSE to which the charging limit is set. If absent or when zero, it applies to the entire Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyChargingLimitRequest</summary>

```json
{
  "chargingLimit": {
    "chargingLimitSource": "string"
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
| `chargingSchedule` | [ChargingScheduleType](../OCPP-2.1-DataTypes.md#chargingscheduletype) | **Yes** |  |  |
| `evseId` | integer | **Yes** | min: 1.0 | The charging schedule contained in this notification applies to an EVSE. EvseId must be > 0. |
| `timeBase` | string (date-time) | **Yes** |  | Periods contained in the charging profile are relative to this point in time. |
| `powerToleranceAcceptance` | boolean | No |  | *(2.1)* True when power tolerance is accepted by EV. This value is taken from EVPowerProfile.PowerToleranceAcceptance in the ISO 15118-20 PowerDeliverReq message.. |
| `selectedChargingScheduleId` | integer | No | min: 0.0 | *(2.1)* Id of the _chargingSchedule_ that EV selected from the provided ChargingProfile. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `status` | [GenericStatusEnumType](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyEVChargingNeeds

**Direction:** CS → CSMS

### NotifyEVChargingNeedsRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingNeeds` | [ChargingNeedsType](#chargingneedstype) | **Yes** |  |  |
| `evseId` | integer | **Yes** | min: 1.0 | Defines the EVSE and connector to which the EV is connected. EvseId may not be 0. |
| `maxScheduleTuples` | integer | No | min: 0.0 | Contains the maximum elements the EV supports for: + - ISO 15118-2: schedule tuples in SASchedule (both Pmax and Tariff). + - ISO 15118-20: PowerScheduleEntry, PriceRule and PriceLevelScheduleEntries. |
| `timestamp` | string (date-time) | No |  | *(2.1)* Time when EV charging needs were received. + Field can be added when charging station was offline when charging needs were received. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyEVChargingNeedsRequest</summary>

```json
{
  "chargingNeeds": {
    "requestedEnergyTransfer": "AC_single_phase"
  },
  "evseId": 0
}
```

</details>

### NotifyEVChargingNeedsResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [NotifyEVChargingNeedsStatusEnumType](#notifyevchargingneedsstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## PullDynamicScheduleUpdate

**Direction:** CS → CSMS

### PullDynamicScheduleUpdateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileId` | integer | **Yes** |  | Id of charging profile to update. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example PullDynamicScheduleUpdateRequest</summary>

```json
{
  "chargingProfileId": 0
}
```

</details>

### PullDynamicScheduleUpdateResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ChargingProfileStatusEnumType](../OCPP-2.1-DataTypes.md#chargingprofilestatusenumtype) | **Yes** |  |  |
| `scheduleUpdate` | [ChargingScheduleUpdateType](#chargingscheduleupdatetype) | No |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## UpdateDynamicSchedule

**Direction:** CSMS → CS

### UpdateDynamicScheduleRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileId` | integer | **Yes** |  | Id of charging profile to update. |
| `scheduleUpdate` | [ChargingScheduleUpdateType](#chargingscheduleupdatetype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example UpdateDynamicScheduleRequest</summary>

```json
{
  "chargingProfileId": 0,
  "scheduleUpdate": {}
}
```

</details>

### UpdateDynamicScheduleResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ChargingProfileStatusEnumType](../OCPP-2.1-DataTypes.md#chargingprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyPriorityCharging

**Direction:** CS → CSMS

### NotifyPriorityChargingRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `activated` | boolean | **Yes** |  | True if priority charging was activated. False if it has stopped using the priority charging profile. |
| `transactionId` | string | **Yes** | maxLength: 36 | The transaction for which priority charging is requested. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyPriorityChargingRequest</summary>

```json
{
  "activated": false,
  "transactionId": "string"
}
```

</details>

### NotifyPriorityChargingResponse

*No required fields. An empty `{}` is a valid response.*

---

## UsePriorityCharging

**Direction:** CSMS → CS

### UsePriorityChargingRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `activate` | boolean | **Yes** |  | True to request priority charging. False to request stopping priority charging. |
| `transactionId` | string | **Yes** | maxLength: 36 | The transaction for which priority charging is requested. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example UsePriorityChargingRequest</summary>

```json
{
  "activate": false,
  "transactionId": "string"
}
```

</details>

### UsePriorityChargingResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [PriorityChargingStatusEnumType](#prioritychargingstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### ClearChargingProfileStatusEnumType

Indicates if the Charging Station was able to execute the request.

| Value |
|-------|
| `Accepted` |
| `Unknown` |

**Used in:** ClearChargingProfile

---

### ControlModeEnumType

*(2.1)* Indicates whether EV wants to operate in Dynamic or Scheduled mode. When absent, Scheduled mode is assumed for backwards compatibility. + *ISO 15118-20:* + ServiceSelectionReq(SelectedEnergyTransferService)

| Value |
|-------|
| `ScheduledControl` |
| `DynamicControl` |

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

### IslandingDetectionEnumType

| Value |
|-------|
| `NoAntiIslandingSupport` |
| `RoCoF` |
| `UVP_OVP` |
| `UFP_OFP` |
| `VoltageVectorShift` |
| `ZeroCrossingDetection` |
| `OtherPassive` |
| `ImpedanceMeasurement` |
| `ImpedanceAtFrequency` |
| `SlipModeFrequencyShift` |
| `SandiaFrequencyShift` |
| `SandiaVoltageShift` |
| `FrequencyJump` |
| `RCLQFactor` |
| `OtherActive` |

**Used in:** NotifyEVChargingNeeds

---

### MobilityNeedsModeEnumType

*(2.1)* Value of EVCC indicates that EV determines min/target SOC and departure time. + A value of EVCC_SECC indicates that charging station or CSMS may also update min/target SOC and departure time. + *ISO 15118-20:* + ServiceSelectionReq(SelectedEnergyTransferService)

| Value |
|-------|
| `EVCC` |
| `EVCC_SECC` |

**Used in:** NotifyEVChargingNeeds

---

### NotifyEVChargingNeedsStatusEnumType

Returns whether the CSMS has been able to process the message successfully. It does not imply that the evChargingNeeds can be met with the current charging profile.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Processing` |
| `NoChargingProfile` |

**Used in:** NotifyEVChargingNeeds

---

### PriorityChargingStatusEnumType

Result of the request.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NoProfile` |

**Used in:** UsePriorityCharging

---

### ACChargingParametersType

EV AC charging parameters for ISO 15118-2

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `energyAmount` | number | **Yes** |  | Amount of energy requested (in Wh). This includes energy required for preconditioning. Relates to: + *ISO 15118-2*: AC_EVChargeParameterType: EAmount + *ISO 15118-20*: Dynamic/Scheduled_SEReqControlModeType: EVTargetEnergyRequest |
| `evMaxCurrent` | number | **Yes** |  | Maximum current (amps) supported by the electric vehicle (per phase). Includes cable capacity. Relates to: + *ISO 15118-2*: AC_EVChargeParameterType: EVMaxCurrent |
| `evMaxVoltage` | number | **Yes** |  | Maximum voltage supported by the electric vehicle. Relates to: + *ISO 15118-2*: AC_EVChargeParameterType: EVMaxVoltage |
| `evMinCurrent` | number | **Yes** |  | Minimum current (amps) supported by the electric vehicle (per phase). Relates to: + *ISO 15118-2*: AC_EVChargeParameterType: EVMinCurrent |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### ChargingLimitType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | string | **Yes** | maxLength: 20 | Represents the source of the charging limit. Values defined in appendix as ChargingLimitSourceEnumStringType. |
| `isGridCritical` | boolean | No |  | Indicates whether the charging limit is critical for the grid. |
| `isLocalGeneration` | boolean | No |  | *(2.1)* True when the reported limit concerns local generation that is providing extra capacity, instead of a limitation. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit

---

### ChargingNeedsType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestedEnergyTransfer` | [EnergyTransferModeEnumType](../OCPP-2.1-DataTypes.md#energytransfermodeenumtype) | **Yes** |  |  |
| `acChargingParameters` | [ACChargingParametersType](#acchargingparameterstype) | No |  |  |
| `availableEnergyTransfer` | [EnergyTransferModeEnumType](../OCPP-2.1-DataTypes.md#energytransfermodeenumtype)[] | No | minItems: 1 | *(2.1)* Modes of energy transfer that are marked as available by EV. |
| `controlMode` | [ControlModeEnumType](#controlmodeenumtype) | No |  |  |
| `dcChargingParameters` | [DCChargingParametersType](#dcchargingparameterstype) | No |  |  |
| `departureTime` | string (date-time) | No |  | Estimated departure time of the EV. + *ISO 15118-2:* AC/DC_EVChargeParameterType: DepartureTime + *ISO 15118-20:* Dynamic/Scheduled_SEReqControlModeType: DepartureTIme |
| `derChargingParameters` | [DERChargingParametersType](#derchargingparameterstype) | No |  |  |
| `evEnergyOffer` | [EVEnergyOfferType](#evenergyoffertype) | No |  |  |
| `mobilityNeedsMode` | [MobilityNeedsModeEnumType](#mobilityneedsmodeenumtype) | No |  |  |
| `v2xChargingParameters` | [V2XChargingParametersType](#v2xchargingparameterstype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### ChargingProfileCriterionType

A ChargingProfileCriterionType is a filter for charging profiles to be selected by a GetChargingProfilesRequest.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingLimitSource` | string[] | No | minItems: 1, maxItems: 4 | For which charging limit sources, charging profiles SHALL be reported. If omitted, the Charging Station SHALL not filter on chargingLimitSource. Values defined in Appendix as ChargingLimitSourceEnumStringType. |
| `chargingProfileId` | integer[] | No | minItems: 1 | List of all the chargingProfileIds requested. Any ChargingProfile that matches one of these profiles will be reported. If omitted, the Charging Station SHALL not filter on chargingProfileId. This field SHALL NOT contain more ids than set in ChargingProfileEntries.maxLimit |
| `chargingProfilePurpose` | [ChargingProfilePurposeEnumType](../OCPP-2.1-DataTypes.md#chargingprofilepurposeenumtype) | No |  |  |
| `stackLevel` | integer | No | min: 0.0 | Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetChargingProfiles

---

### ChargingScheduleUpdateType

Updates to a ChargingSchedulePeriodType for dynamic charging profiles.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `dischargeLimit` | number | No | max: 0.0 | *(2.1)* Limit in _chargingRateUnit_ that the EV is allowed to discharge with. Note, these are negative values in order to be consistent with _setpoint_, which can be positive and negative. + For AC this field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `dischargeLimit_L2` | number | No | max: 0.0 | *(2.1)* Limit in _chargingRateUnit_ on phase L2 that the EV is allowed to discharge with. |
| `dischargeLimit_L3` | number | No | max: 0.0 | *(2.1)* Limit in _chargingRateUnit_ on phase L3 that the EV is allowed to discharge with. |
| `limit` | number | No |  | Optional only when not required by the _operationMode_, as in CentralSetpoint, ExternalSetpoint, ExternalLimits, LocalFrequency, LocalLoadBalancing. + Charging rate limit during the schedule period, in the applicable _chargingRateUnit_. This SHOULD be a non-negative value; a negative value is only supported for backwards compatibility with older systems that use a negative value to specify a discharging limit. For AC this field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `limit_L2` | number | No |  | *(2.1)* Charging rate limit on phase L2 in the applicable _chargingRateUnit_. |
| `limit_L3` | number | No |  | *(2.1)* Charging rate limit on phase L3 in the applicable _chargingRateUnit_. |
| `setpoint` | number | No |  | *(2.1)* Setpoint in _chargingRateUnit_ that the EV should follow as close as possible. Use negative values for discharging. + When a limit and/or _dischargeLimit_ are given the overshoot when following _setpoint_ must remain within these values. This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `setpointReactive` | number | No |  | *(2.1)* Setpoint for reactive power (or current) in _chargingRateUnit_ that the EV should follow as closely as possible. Positive values for inductive, negative for capacitive reactive power or current. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `setpointReactive_L2` | number | No |  | *(2.1)* Setpoint for reactive power (or current) in _chargingRateUnit_ that the EV should follow on phase L2 as closely as possible. |
| `setpointReactive_L3` | number | No |  | *(2.1)* Setpoint for reactive power (or current) in _chargingRateUnit_ that the EV should follow on phase L3 as closely as possible. |
| `setpoint_L2` | number | No |  | *(2.1)* Setpoint in _chargingRateUnit_ that the EV should follow on phase L2 as close as possible. |
| `setpoint_L3` | number | No |  | *(2.1)* Setpoint in _chargingRateUnit_ that the EV should follow on phase L3 as close as possible. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** PullDynamicScheduleUpdate, UpdateDynamicSchedule

---

### ClearChargingProfileType

A ClearChargingProfileType is a filter for charging profiles to be cleared by ClearChargingProfileRequest.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfilePurpose` | [ChargingProfilePurposeEnumType](../OCPP-2.1-DataTypes.md#chargingprofilepurposeenumtype) | No |  |  |
| `evseId` | integer | No | min: 0.0 | Specifies the id of the EVSE for which to clear charging profiles. An evseId of zero (0) specifies the charging profile for the overall Charging Station. Absence of this parameter means the clearing applies to all charging profiles that match the other criteria in the request. |
| `stackLevel` | integer | No | min: 0.0 | Specifies the stackLevel for which charging profiles will be cleared, if they meet the other criteria in the request. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ClearChargingProfile

---

### CompositeScheduleType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingRateUnit` | [ChargingRateUnitEnumType](../OCPP-2.1-DataTypes.md#chargingrateunitenumtype) | **Yes** |  |  |
| `chargingSchedulePeriod` | [ChargingSchedulePeriodType](../OCPP-2.1-DataTypes.md#chargingscheduleperiodtype)[] | **Yes** | minItems: 1 |  |
| `duration` | integer | **Yes** |  |  |
| `evseId` | integer | **Yes** | min: 0.0 |  |
| `scheduleStart` | string (date-time) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetCompositeSchedule

---

### DCChargingParametersType

EV DC charging parameters for ISO 15118-2

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evMaxCurrent` | number | **Yes** |  | Maximum current (in A) supported by the electric vehicle. Includes cable capacity. Relates to: + *ISO 15118-2*: DC_EVChargeParameterType:EVMaximumCurrentLimit |
| `evMaxVoltage` | number | **Yes** |  | Maximum voltage supported by the electric vehicle. Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: EVMaximumVoltageLimit |
| `bulkSoC` | integer | No | min: 0.0, max: 100.0 | Percentage of SoC at which the EV considers a fast charging process to end. (possible values: 0 - 100) Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: BulkSOC |
| `energyAmount` | number | No |  | Amount of energy requested (in Wh). This inludes energy required for preconditioning. Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: EVEnergyRequest |
| `evEnergyCapacity` | number | No |  | Capacity of the electric vehicle battery (in Wh). Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: EVEnergyCapacity |
| `evMaxPower` | number | No |  | Maximum power (in W) supported by the electric vehicle. Required for DC charging. Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: EVMaximumPowerLimit |
| `fullSoC` | integer | No | min: 0.0, max: 100.0 | Percentage of SoC at which the EV considers the battery fully charged. (possible values: 0 - 100) Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: FullSOC |
| `stateOfCharge` | integer | No | min: 0.0, max: 100.0 | Energy available in the battery (in percent of the battery capacity) Relates to: + *ISO 15118-2*: DC_EVChargeParameterType: DC_EVStatus: EVRESSSOC |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### DERChargingParametersType

*(2.1)* DERChargingParametersType is used in ChargingNeedsType during an ISO 15118-20 session for AC_BPT_DER to report the inverter settings related to DER control that were agreed between EVSE and EV. Fields starting with "ev" contain values from the EV. Other fields contain a value that is supported by both EV and EVSE. DERChargingParametersType type is only relevant in case of an ISO 15118-20 AC_BPT_DER/AC_DER charging session. NOTE: All these fields have values greater or equal to zero (i.e. are non-negative)

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evDurationLevel1DCInjection` | number | No |  | Maximum allowed duration of DC injection at level 1 charging. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVDurationLevel1DCInjection |
| `evDurationLevel2DCInjection` | number | No |  | Maximum allowed duration of DC injection at level 2 charging. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVDurationLevel2DCInjection |
| `evInverterHwVersion` | string | No | maxLength: 50 | Hardware version of EV inverter. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVInverterHwVersion |
| `evInverterManufacturer` | string | No | maxLength: 50 | Manufacturer of the EV inverter. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVInverterManufacturer |
| `evInverterModel` | string | No | maxLength: 50 | Model name of the EV inverter. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVInverterModel |
| `evInverterSerialNumber` | string | No | maxLength: 50 | Serial number of the EV inverter. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVInverterSerialNumber |
| `evInverterSwVersion` | string | No | maxLength: 50 | Software version of EV inverter. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVInverterSwVersion |
| `evIslandingDetectionMethod` | [IslandingDetectionEnumType](#islandingdetectionenumtype)[] | No | minItems: 1 | Type of islanding detection method. Only mandatory when islanding detection is required at the site, as set in the ISO 15118 Service Details configuration. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVIslandingDetectionMethod |
| `evIslandingTripTime` | number | No |  | Time after which EV will trip if an island has been detected. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVIslandingTripTime |
| `evMaximumLevel1DCInjection` | number | No |  | Maximum injected DC current allowed at level 1 charging. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumLevel1DCInjection |
| `evMaximumLevel2DCInjection` | number | No |  | Maximum injected DC current allowed at level 2 charging. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumLevel2DCInjection |
| `evOverExcitedMaxDischargePower` | number | No |  | Rated maximum injected active power by EV, at specified over-excited power factor (overExcitedPowerFactor). + It can also be defined as the rated maximum discharge power at the rated minimum injected reactive power value. This means that if the EV is providing reactive power support, and it is requested to discharge at max power (e.g. to satisfy an EMS request), the EV may override the request and discharge up to overExcitedMaximumDischargePower to meet the minimum reactive power requirements. + Corresponds to the WOvPF attribute in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVOverExcitedMaximumDischargePower |
| `evOverExcitedPowerFactor` | number | No |  | EV power factor when injecting (over excited) the minimum reactive power. + Corresponds to the OvPF attribute in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVOverExcitedPowerFactor |
| `evReactiveSusceptance` | number | No |  | Measure of the susceptibility of the circuit to reactance, in Siemens (S). + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVReactiveSusceptance |
| `evSessionTotalDischargeEnergyAvailable` | number | No |  | Total energy value, in Wh, that EV is allowed to provide during the entire V2G session. The value is independent of the V2X Cycling area. Once this value reaches the value of 0, the EV may block any attempt to discharge in order to protect the battery health. *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVSessionTotalDischargeEnergyAvailable |
| `evSupportedDERControl` | [DERControlEnumType](../OCPP-2.1-DataTypes.md#dercontrolenumtype)[] | No | minItems: 1 | DER control functions supported by EV. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType:DERControlFunctions (bitmap) |
| `evUnderExcitedMaxDischargePower` | number | No |  | Rated maximum injected active power by EV supported at specified under-excited power factor (EVUnderExcitedPowerFactor). + It can also be defined as the rated maximum dischargePower at the rated minimum absorbed reactive power value. This means that if the EV is providing reactive power support, and it is requested to discharge at max power (e.g. to satisfy an EMS request), the EV may override the request and discharge up to underExcitedMaximumDischargePower to meet the minimum reactive power requirements. + This corresponds to the WUnPF attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVUnderExcitedMaximumDischargePower |
| `evUnderExcitedPowerFactor` | number | No |  | EV power factor when injecting (under excited) the minimum reactive power. + Corresponds to the OvPF attribute in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVUnderExcitedPowerFactor |
| `maxApparentPower` | number | No |  | Rated maximum total apparent power, defined by min(EV, EVSE) in va. Corresponds to the VAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumApparentPower |
| `maxChargeApparentPower` | number | No |  | Rated maximum absorbed apparent power, defined by min(EV, EVSE) in va. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + Corresponds to the ChaVAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumChargeApparentPower |
| `maxChargeApparentPower_L2` | number | No |  | Rated maximum absorbed apparent power on phase L2, defined by min(EV, EVSE) in va. Corresponds to the ChaVAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumChargeApparentPower_L2 |
| `maxChargeApparentPower_L3` | number | No |  | Rated maximum absorbed apparent power on phase L3, defined by min(EV, EVSE) in va. Corresponds to the ChaVAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumChargeApparentPower_L3 |
| `maxChargeReactivePower` | number | No |  | Rated maximum absorbed reactive power, defined by min(EV, EVSE), in vars. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + Corresponds to the AvarMax attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumChargeReactivePower |
| `maxChargeReactivePower_L2` | number | No |  | Rated maximum absorbed reactive power, defined by min(EV, EVSE), in vars on phase L2. + Corresponds to the AvarMax attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumChargeReactivePower_L2 |
| `maxChargeReactivePower_L3` | number | No |  | Rated maximum absorbed reactive power, defined by min(EV, EVSE), in vars on phase L3. + Corresponds to the AvarMax attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumChargeReactivePower_L3 |
| `maxDischargeApparentPower` | number | No |  | Rated maximum injected apparent power, defined by min(EV, EVSE) in va. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + Corresponds to the DisVAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumDischargeApparentPower |
| `maxDischargeApparentPower_L2` | number | No |  | Rated maximum injected apparent power on phase L2, defined by min(EV, EVSE) in va. + Corresponds to the DisVAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumDischargeApparentPower_L2 |
| `maxDischargeApparentPower_L3` | number | No |  | Rated maximum injected apparent power on phase L3, defined by min(EV, EVSE) in va. + Corresponds to the DisVAMaxRtg in IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumDischargeApparentPower_L3 |
| `maxDischargeReactivePower` | number | No |  | Rated maximum injected reactive power, defined by min(EV, EVSE), in vars. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + Corresponds to the IvarMax attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumDischargeReactivePower |
| `maxDischargeReactivePower_L2` | number | No |  | Rated maximum injected reactive power, defined by min(EV, EVSE), in vars on phase L2. + Corresponds to the IvarMax attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumDischargeReactivePower_L2 |
| `maxDischargeReactivePower_L3` | number | No |  | Rated maximum injected reactive power, defined by min(EV, EVSE), in vars on phase L3. + Corresponds to the IvarMax attribute in the IEC 61850. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumDischargeReactivePower_L3 |
| `maxNominalVoltage` | number | No |  | Maximum AC rms voltage, as defined by min(EV, EVSE) to operate with. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMaximumNominalVoltage |
| `minChargeReactivePower` | number | No |  | Rated minimum absorbed reactive power, defined by max(EV, EVSE), in vars. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumChargeReactivePower |
| `minChargeReactivePower_L2` | number | No |  | Rated minimum absorbed reactive power, defined by max(EV, EVSE), in vars on phase L2. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumChargeReactivePower_L2 |
| `minChargeReactivePower_L3` | number | No |  | Rated minimum absorbed reactive power, defined by max(EV, EVSE), in vars on phase L3. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumChargeReactivePower_L3 |
| `minDischargeReactivePower` | number | No |  | Rated minimum injected reactive power, defined by max(EV, EVSE), in vars. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumDischargeReactivePower |
| `minDischargeReactivePower_L2` | number | No |  | Rated minimum injected reactive power, defined by max(EV, EVSE), in var on phase L2. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumDischargeReactivePower_L2 |
| `minDischargeReactivePower_L3` | number | No |  | Rated minimum injected reactive power, defined by max(EV, EVSE), in var on phase L3. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumDischargeReactivePower_L3 |
| `minNominalVoltage` | number | No |  | Minimum AC rms voltage, as defined by max(EV, EVSE) to operate with. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVMinimumNominalVoltage |
| `nominalVoltage` | number | No |  | Line voltage supported by EVSE and EV. *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVNominalVoltage |
| `nominalVoltageOffset` | number | No |  | The nominal AC voltage (rms) offset between the Charging Station's electrical connection point and the utility’s point of common coupling. + *ISO 15118-20*: DER_BPT_AC_CPDReqEnergyTransferModeType: EVNominalVoltageOffset |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### EVAbsolutePriceScheduleEntryType

*(2.1)* An entry in price schedule over time for which EV is willing to discharge.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `duration` | integer | **Yes** |  | The amount of seconds of this entry. |
| `evPriceRule` | [EVPriceRuleType](#evpriceruletype)[] | **Yes** | minItems: 1, maxItems: 8 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### EVAbsolutePriceScheduleType

*(2.1)* Price schedule of EV energy offer.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currency` | string | **Yes** | maxLength: 3 | Currency code according to ISO 4217. |
| `evAbsolutePriceScheduleEntries` | [EVAbsolutePriceScheduleEntryType](#evabsolutepricescheduleentrytype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `priceAlgorithm` | string | **Yes** | maxLength: 2000 | ISO 15118-20 URN of price algorithm: Power, PeakPower, StackedEnergy. |
| `timeAnchor` | string (date-time) | **Yes** |  | Starting point in time of the EVEnergyOffer. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### EVEnergyOfferType

*(2.1)* A schedule of the energy amount over time that EV is willing to discharge. A negative value indicates the willingness to discharge under specific conditions, a positive value indicates that the EV currently is not able to offer energy to discharge.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evPowerSchedule` | [EVPowerScheduleType](#evpowerscheduletype) | **Yes** |  |  |
| `evAbsolutePriceSchedule` | [EVAbsolutePriceScheduleType](#evabsolutepricescheduletype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### EVPowerScheduleEntryType

*(2.1)* An entry in schedule of the energy amount over time that EV is willing to discharge. A negative value indicates the willingness to discharge under specific conditions, a positive value indicates that the EV currently is not able to offer energy to discharge.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `duration` | integer | **Yes** |  | The duration of this entry. |
| `power` | number | **Yes** |  | Defines maximum amount of power for the duration of this EVPowerScheduleEntry to be discharged from the EV battery through EVSE power outlet. Negative values are used for discharging. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### EVPowerScheduleType

*(2.1)* Schedule of EV energy offer.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evPowerScheduleEntries` | [EVPowerScheduleEntryType](#evpowerscheduleentrytype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `timeAnchor` | string (date-time) | **Yes** |  | The time that defines the starting point for the EVEnergyOffer. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### EVPriceRuleType

*(2.1)* An entry in price schedule over time for which EV is willing to discharge.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `energyFee` | number | **Yes** |  | Cost per kWh. |
| `powerRangeStart` | number | **Yes** |  | The EnergyFee applies between this value and the value of the PowerRangeStart of the subsequent EVPriceRule. If the power is below this value, the EnergyFee of the previous EVPriceRule applies. Negative values are used for discharging. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---

### V2XChargingParametersType

Charging parameters for ISO 15118-20, also supporting V2X charging/discharging.+ All values are greater or equal to zero, with the exception of EVMinEnergyRequest, EVMaxEnergyRequest, EVTargetEnergyRequest, EVMinV2XEnergyRequest and EVMaxV2XEnergyRequest.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evMaxEnergyRequest` | number | No |  | Energy to maximum state of charge in Wh Relates to: *ISO 15118-20*: Dynamic/Scheduled_SEReqControlModeType: EVMaximumEnergyRequest |
| `evMaxV2XEnergyRequest` | number | No |  | Energy (in Wh) to maximum state of charge for cycling (V2X) activity. Negative value indicates that current state of charge is above V2X range. Relates to: *ISO 15118-20*: Dynamic_SEReqControlModeType: EVMaximumV2XEnergyRequest |
| `evMinEnergyRequest` | number | No |  | Energy to minimum allowed state of charge in Wh Relates to: *ISO 15118-20*: Dynamic/Scheduled_SEReqControlModeType: EVMinimumEnergyRequest |
| `evMinV2XEnergyRequest` | number | No |  | Energy (in Wh) to minimum state of charge for cycling (V2X) activity. Positive value means that current state of charge is below V2X range. Relates to: *ISO 15118-20*: Dynamic_SEReqControlModeType: EVMinimumV2XEnergyRequest |
| `evTargetEnergyRequest` | number | No |  | Energy to requested state of charge in Wh Relates to: *ISO 15118-20*: Dynamic/Scheduled_SEReqControlModeType: EVTargetEnergyRequest |
| `maxChargeCurrent` | number | No |  | Maximum charge current in A, defined by min(EV, EVSE) Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: EVMaximumChargeCurrent |
| `maxChargePower` | number | No |  | Maximum charge (absorbed) power in W, defined by min(EV, EVSE) at unity power factor. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. It corresponds to the ChaWMax attribute in the IEC 61850. It is usually equivalent to the rated apparent power of the EV when discharging (ChaVAMax) in IEC 61850. + Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMaximumChargePower |
| `maxChargePower_L2` | number | No |  | Maximum charge power on phase L2 in W, defined by min(EV, EVSE) Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMaximumChargePower_L2 |
| `maxChargePower_L3` | number | No |  | Maximum charge power on phase L3 in W, defined by min(EV, EVSE) Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMaximumChargePower_L3 |
| `maxDischargeCurrent` | number | No |  | Maximum discharge current in A, defined by min(EV, EVSE). Value >= 0. Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: EVMaximumDischargeCurrent |
| `maxDischargePower` | number | No |  | Maximum discharge (injected) power in W, defined by min(EV, EVSE) at unity power factor. Value >= 0. This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMaximumDischargePower |
| `maxDischargePower_L2` | number | No |  | Maximum discharge power on phase L2 in W, defined by min(EV, EVSE). Value >= 0. Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMaximumDischargePowe_L2 |
| `maxDischargePower_L3` | number | No |  | Maximum discharge power on phase L3 in W, defined by min(EV, EVSE). Value >= 0. Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMaximumDischargePower_L3 |
| `maxVoltage` | number | No |  | Maximum voltage in V, defined by min(EV, EVSE) Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: EVMaximumVoltage |
| `minChargeCurrent` | number | No |  | Minimum charge current in A, defined by max(EV, EVSE) Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: EVMinimumChargeCurrent |
| `minChargePower` | number | No |  | Minimum charge power in W, defined by max(EV, EVSE). This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMinimumChargePower |
| `minChargePower_L2` | number | No |  | Minimum charge power on phase L2 in W, defined by max(EV, EVSE). Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMinimumChargePower_L2 |
| `minChargePower_L3` | number | No |  | Minimum charge power on phase L3 in W, defined by max(EV, EVSE). Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMinimumChargePower_L3 |
| `minDischargeCurrent` | number | No |  | Minimum discharge current in A, defined by max(EV, EVSE). Value >= 0. Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: EVMinimumDischargeCurrent |
| `minDischargePower` | number | No |  | Minimum discharge (injected) power in W, defined by max(EV, EVSE) at unity power factor. Value >= 0. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. + It corresponds to the WMax attribute in the IEC 61850. It is usually equivalent to the rated apparent power of the EV when discharging (VAMax attribute in the IEC 61850). Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMinimumDischargePower |
| `minDischargePower_L2` | number | No |  | Minimum discharge power on phase L2 in W, defined by max(EV, EVSE). Value >= 0. Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMinimumDischargePower_L2 |
| `minDischargePower_L3` | number | No |  | Minimum discharge power on phase L3 in W, defined by max(EV, EVSE). Value >= 0. Relates to: *ISO 15118-20*: BPT_AC/DC_CPDReqEnergyTransferModeType: EVMinimumDischargePower_L3 |
| `minVoltage` | number | No |  | Minimum voltage in V, defined by max(EV, EVSE) Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: EVMinimumVoltage |
| `targetSoC` | integer | No | min: 0.0, max: 100.0 | Target state of charge at departure as percentage. Relates to: *ISO 15118-20*: BPT_DC_CPDReqEnergyTransferModeType: TargetSOC |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEVChargingNeeds

---
