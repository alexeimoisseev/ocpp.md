# OCPP 2.1 — Data Types Reference

> **Purpose:** Complete reference of all reusable data types and enumerations in OCPP 2.1.
> Generated from the official OCA JSON schemas.
>
> **See also:** Message schemas by functional block:
> [Schemas — Security](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Security.md) |
> [Schemas — Provisioning](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Provisioning.md) |
> [Schemas — Authorization](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Authorization.md) |
> [Schemas — LocalAuthList](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-LocalAuthList.md) |
> [Schemas — Transactions](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Transactions.md) |
> [Schemas — RemoteControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-RemoteControl.md) |
> [Schemas — Availability](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Availability.md) |
> [Schemas — Reservation](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Reservation.md) |
> [Schemas — TariffAndCost](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-TariffAndCost.md) |
> [Schemas — MeterValues](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-MeterValues.md) |
> [Schemas — SmartCharging](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-SmartCharging.md) |
> [Schemas — Firmware](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Firmware.md) |
> [Schemas — Certificates](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Certificates.md) |
> [Schemas — Diagnostics](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Diagnostics.md) |
> [Schemas — Display](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Display.md) |
> [Schemas — DataTransfer](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DataTransfer.md) |
> [Schemas — Bidirectional](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-Bidirectional.md) |
> [Schemas — DERControl](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-DERControl.md) |
> [Schemas — BatterySwap](./OCPP-2.1-Schemas/OCPP-2.1-Schemas-BatterySwap.md) |

**21 Enum Types** | **43 Composite Types**

---

## Table of Contents

### Enums

- [AttributeEnumType](#attributeenumtype)
- [AuthorizationStatusEnumType](#authorizationstatusenumtype)
- [ChargingProfileKindEnumType](#chargingprofilekindenumtype)
- [ChargingProfilePurposeEnumType](#chargingprofilepurposeenumtype)
- [ChargingProfileStatusEnumType](#chargingprofilestatusenumtype)
- [ChargingRateUnitEnumType](#chargingrateunitenumtype)
- [CostKindEnumType](#costkindenumtype)
- [DERControlEnumType](#dercontrolenumtype)
- [DERControlStatusEnumType](#dercontrolstatusenumtype)
- [DayOfWeekEnumType](#dayofweekenumtype)
- [EnergyTransferModeEnumType](#energytransfermodeenumtype)
- [EvseKindEnumType](#evsekindenumtype)
- [GenericDeviceModelStatusEnumType](#genericdevicemodelstatusenumtype)
- [GenericStatusEnumType](#genericstatusenumtype)
- [HashAlgorithmEnumType](#hashalgorithmenumtype)
- [MessageFormatEnumType](#messageformatenumtype)
- [MessagePriorityEnumType](#messagepriorityenumtype)
- [MessageStateEnumType](#messagestateenumtype)
- [MonitorEnumType](#monitorenumtype)
- [OperationModeEnumType](#operationmodeenumtype)
- [RecurrencyKindEnumType](#recurrencykindenumtype)

### Composite Types

- [AbsolutePriceScheduleType](#absolutepricescheduletype)
- [AdditionalInfoType](#additionalinfotype)
- [AdditionalSelectedServicesType](#additionalselectedservicestype)
- [CertificateHashDataType](#certificatehashdatatype)
- [ChargingProfileType](#chargingprofiletype)
- [ChargingSchedulePeriodType](#chargingscheduleperiodtype)
- [ChargingScheduleType](#chargingscheduletype)
- [ComponentType](#componenttype)
- [ConsumptionCostType](#consumptioncosttype)
- [CostType](#costtype)
- [CustomDataType](#customdatatype)
- [EVSEType](#evsetype)
- [IdTokenInfoType](#idtokeninfotype)
- [IdTokenType](#idtokentype)
- [LimitAtSoCType](#limitatsoctype)
- [MessageContentType](#messagecontenttype)
- [OverstayRuleListType](#overstayrulelisttype)
- [OverstayRuleType](#overstayruletype)
- [PeriodicEventStreamParamsType](#periodiceventstreamparamstype)
- [PriceLevelScheduleEntryType](#pricelevelscheduleentrytype)
- [PriceLevelScheduleType](#pricelevelscheduletype)
- [PriceRuleStackType](#pricerulestacktype)
- [PriceRuleType](#priceruletype)
- [PriceType](#pricetype)
- [RationalNumberType](#rationalnumbertype)
- [RelativeTimeIntervalType](#relativetimeintervaltype)
- [SalesTariffEntryType](#salestariffentrytype)
- [SalesTariffType](#salestarifftype)
- [StatusInfoType](#statusinfotype)
- [TariffConditionsFixedType](#tariffconditionsfixedtype)
- [TariffConditionsType](#tariffconditionstype)
- [TariffEnergyPriceType](#tariffenergypricetype)
- [TariffEnergyType](#tariffenergytype)
- [TariffFixedPriceType](#tarifffixedpricetype)
- [TariffFixedType](#tarifffixedtype)
- [TariffTimePriceType](#tarifftimepricetype)
- [TariffTimeType](#tarifftimetype)
- [TariffType](#tarifftype)
- [TaxRateType](#taxratetype)
- [TaxRuleType](#taxruletype)
- [V2XFreqWattPointType](#v2xfreqwattpointtype)
- [V2XSignalWattPointType](#v2xsignalwattpointtype)
- [VariableType](#variabletype)

---

## Enums

### AttributeEnumType

Attribute type for which value is requested. When absent, default Actual is assumed.

**Default:** `Actual`

| Value |
|-------|
| `Actual` |
| `Target` |
| `MinSet` |
| `MaxSet` |

**Used in:** GetVariables, NotifyReport, SetVariables

---

### AuthorizationStatusEnumType

Current status of the ID Token.

| Value |
|-------|
| `Accepted` |
| `Blocked` |
| `ConcurrentTx` |
| `Expired` |
| `Invalid` |
| `NoCredit` |
| `NotAllowedTypeEVSE` |
| `NotAtThisLocation` |
| `NotAtThisTime` |
| `Unknown` |

**Used in:** Authorize, SendLocalList, TransactionEvent

---

### ChargingProfileKindEnumType

Indicates the kind of schedule.

| Value |
|-------|
| `Absolute` |
| `Recurring` |
| `Relative` |
| `Dynamic` |

**Used in:** ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingProfilePurposeEnumType

Specifies to purpose of the charging profiles that will be cleared, if they meet the other criteria in the request.

| Value |
|-------|
| `ChargingStationExternalConstraints` |
| `ChargingStationMaxProfile` |
| `TxDefaultProfile` |
| `TxProfile` |
| `PriorityCharging` |
| `LocalGeneration` |

**Used in:** ClearChargingProfile, GetChargingProfiles, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingProfileStatusEnumType

Returns whether the Charging Station has been able to process the message successfully. This does not guarantee the schedule will be followed to the letter. There might be other constraints the Charging Station may need to take into account.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** PullDynamicScheduleUpdate, SetChargingProfile, UpdateDynamicSchedule

---

### ChargingRateUnitEnumType

The unit of measure in which limits and setpoints are expressed.

| Value |
|-------|
| `W` |
| `A` |

**Used in:** GetCompositeSchedule, NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### CostKindEnumType

The kind of cost referred to in the message element amount

| Value |
|-------|
| `CarbonDioxideEmission` |
| `RelativePricePercentage` |
| `RenewableGenerationPercentage` |

**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### DERControlEnumType

Type of control settings to retrieve. Not used when _controlId_ is provided.

| Value |
|-------|
| `EnterService` |
| `FreqDroop` |
| `FreqWatt` |
| `FixedPFAbsorb` |
| `FixedPFInject` |
| `FixedVar` |
| `Gradients` |
| `HFMustTrip` |
| `HFMayTrip` |
| `HVMustTrip` |
| `HVMomCess` |
| `HVMayTrip` |
| `LimitMaxDischarge` |
| `LFMustTrip` |
| `LVMustTrip` |
| `LVMomCess` |
| `LVMayTrip` |
| `PowerMonitoringMustTrip` |
| `VoltVar` |
| `VoltWatt` |
| `WattPF` |
| `WattVar` |

**Used in:** ClearDERControl, GetDERControl, NotifyDERAlarm, NotifyEVChargingNeeds, ReportDERControl, SetDERControl

---

### DERControlStatusEnumType

Result of operation.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NotSupported` |
| `NotFound` |

**Used in:** ClearDERControl, GetDERControl, SetDERControl

---

### DayOfWeekEnumType

| Value |
|-------|
| `Monday` |
| `Tuesday` |
| `Wednesday` |
| `Thursday` |
| `Friday` |
| `Saturday` |
| `Sunday` |

**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### EnergyTransferModeEnumType

Mode of energy transfer requested by the EV.

| Value |
|-------|
| `AC_single_phase` |
| `AC_two_phase` |
| `AC_three_phase` |
| `DC` |
| `AC_BPT` |
| `AC_BPT_DER` |
| `AC_DER` |
| `DC_BPT` |
| `DC_ACDP` |
| `DC_ACDP_BPT` |
| `WPT` |

**Used in:** Authorize, NotifyAllowedEnergyTransfer, NotifyEVChargingNeeds

---

### EvseKindEnumType

Type of EVSE (AC, DC) this tariff applies to.

| Value |
|-------|
| `AC` |
| `DC` |

**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### GenericDeviceModelStatusEnumType

This field indicates whether the Charging Station was able to accept the request.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NotSupported` |
| `EmptyResultSet` |

**Used in:** GetBaseReport, GetMonitoringReport, GetReport, SetMonitoringBase

---

### GenericStatusEnumType

Returns whether the CSMS has been able to process the message successfully. It does not imply any approval of the charging schedule.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** AFRRSignal, AdjustPeriodicEventStream, GetCompositeSchedule, NotifyEVChargingSchedule, OpenPeriodicEventStream, PublishFirmware, RequestBatterySwap, SetMonitoringLevel, SignCertificate, VatNumberValidation

---

### HashAlgorithmEnumType

Used algorithms for the hashes provided.

| Value |
|-------|
| `SHA256` |
| `SHA384` |
| `SHA512` |

**Used in:** Authorize, CustomerInformation, DeleteCertificate, GetCertificateChainStatus, GetCertificateStatus, GetInstalledCertificateIds, SignCertificate

---

### MessageFormatEnumType

Format of the message.

| Value |
|-------|
| `ASCII` |
| `HTML` |
| `URI` |
| `UTF8` |
| `QRCODE` |

**Used in:** Authorize, ChangeTransactionTariff, NotifyDisplayMessages, SendLocalList, SetDefaultTariff, SetDisplayMessage, TransactionEvent

---

### MessagePriorityEnumType

If provided the Charging Station shall return Display Messages with the given priority only.

| Value |
|-------|
| `AlwaysFront` |
| `InFront` |
| `NormalCycle` |

**Used in:** GetDisplayMessages, NotifyDisplayMessages, SetDisplayMessage

---

### MessageStateEnumType

During what state should this message be shown. When omitted this message should be shown in any state of the Charging Station.

| Value |
|-------|
| `Charging` |
| `Faulted` |
| `Idle` |
| `Unavailable` |
| `Suspended` |
| `Discharging` |

**Used in:** GetDisplayMessages, NotifyDisplayMessages, SetDisplayMessage

---

### MonitorEnumType

The type of this monitor, e.g. a threshold, delta or periodic monitor.

| Value |
|-------|
| `UpperThreshold` |
| `LowerThreshold` |
| `Delta` |
| `Periodic` |
| `PeriodicClockAligned` |
| `TargetDelta` |
| `TargetDeltaRelative` |

**Used in:** NotifyMonitoringReport, SetVariableMonitoring

---

### OperationModeEnumType

*(2.1)* Charging operation mode to use during this time interval. When absent defaults to ChargingOnly.

| Value |
|-------|
| `Idle` |
| `ChargingOnly` |
| `CentralSetpoint` |
| `ExternalSetpoint` |
| `ExternalLimits` |
| `CentralFrequency` |
| `LocalFrequency` |
| `LocalLoadBalancing` |

**Used in:** GetCompositeSchedule, NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile, TransactionEvent

---

### RecurrencyKindEnumType

Indicates the start point of a recurrence.

| Value |
|-------|
| `Daily` |
| `Weekly` |

**Used in:** ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

## Composite Types

### AbsolutePriceScheduleType

The AbsolutePriceScheduleType is modeled after the same type that is defined in ISO 15118-20, such that if it is supplied by an EMSP as a signed EXI message, the conversion from EXI to JSON (in OCPP) and back to EXI (for ISO 15118-20) does not change the digest and therefore does not invalidate the signature. image::images/AbsolutePriceSchedule-Simple.png[]

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currency` | string | **Yes** | maxLength: 3 | Currency according to ISO 4217. |
| `language` | string | **Yes** | maxLength: 8 | String that indicates what language is used for the human readable strings in the price schedule. Based on ISO 639. |
| `priceAlgorithm` | string | **Yes** | maxLength: 2000 | A string in URN notation which shall uniquely identify an algorithm that defines how to compute an energy fee sum for a specific power profile based on the EnergyFee information from the PriceRule elements. |
| `priceRuleStacks` | [PriceRuleStackType](#pricerulestacktype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `priceScheduleID` | integer | **Yes** | min: 0.0 | Unique ID of price schedule |
| `timeAnchor` | string (date-time) | **Yes** |  | Starting point of price schedule. |
| `additionalSelectedServices` | [AdditionalSelectedServicesType](#additionalselectedservicestype)[] | No | minItems: 1, maxItems: 5 |  |
| `maximumCost` | [RationalNumberType](#rationalnumbertype) | No |  |  |
| `minimumCost` | [RationalNumberType](#rationalnumbertype) | No |  |  |
| `overstayRuleList` | [OverstayRuleListType](#overstayrulelisttype) | No |  |  |
| `priceScheduleDescription` | string | No | maxLength: 160 | Description of the price schedule. |
| `taxRules` | [TaxRuleType](#taxruletype)[] | No | minItems: 1, maxItems: 10 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### AdditionalInfoType

Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `additionalIdToken` | string | **Yes** | maxLength: 255 | *(2.1)* This field specifies the additional IdToken. |
| `type` | string | **Yes** | maxLength: 50 | _additionalInfo_ can be used to send extra information to CSMS in addition to the regular authorization with _IdToken_. _AdditionalInfo_ contains one or more custom _types_, which need to be agreed upon by all parties involved. When the _type_ is not supported, the CSMS/Charging Station MAY ignore the _additionalInfo_. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, BatterySwap, CustomerInformation, RequestBatterySwap, RequestStartTransaction, ReserveNow, SendLocalList, TransactionEvent

---

### AdditionalSelectedServicesType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `serviceFee` | [RationalNumberType](#rationalnumbertype) | **Yes** |  |  |
| `serviceName` | string | **Yes** | maxLength: 80 | Human readable string to identify this service. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### CertificateHashDataType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `hashAlgorithm` | [HashAlgorithmEnumType](#hashalgorithmenumtype) | **Yes** |  |  |
| `issuerKeyHash` | string | **Yes** | maxLength: 128 | The hash of the DER encoded public key: the value (excluding tag and length) of the subject public key field in the issuer’s certificate. |
| `issuerNameHash` | string | **Yes** | maxLength: 128 | The hash of the issuer’s distinguished name (DN), that must be calculated over the DER encoding of the issuer’s name field in the certificate being checked. |
| `serialNumber` | string | **Yes** | maxLength: 40 | The string representation of the hexadecimal value of the serial number without the prefix "0x" and without leading zeroes. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** CustomerInformation, DeleteCertificate, GetCertificateChainStatus, GetInstalledCertificateIds, SignCertificate

---

### ChargingProfileType

A ChargingProfile consists of 1 to 3 ChargingSchedules with a list of ChargingSchedulePeriods, describing the amount of power or current that can be delivered per time interval. image::images/ChargingProfile-Simple.png[]

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileKind` | [ChargingProfileKindEnumType](#chargingprofilekindenumtype) | **Yes** |  |  |
| `chargingProfilePurpose` | [ChargingProfilePurposeEnumType](#chargingprofilepurposeenumtype) | **Yes** |  |  |
| `chargingSchedule` | [ChargingScheduleType](#chargingscheduletype)[] | **Yes** | minItems: 1, maxItems: 3 |  |
| `id` | integer | **Yes** |  | Id of ChargingProfile. Unique within charging station. Id can have a negative value. This is useful to distinguish charging profiles from an external actor (external constraints) from charging profiles received from CSMS. |
| `stackLevel` | integer | **Yes** | min: 0.0 | Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0. |
| `dynUpdateInterval` | integer | No |  | *(2.1)* Interval in seconds after receipt of last update, when to request a profile update by sending a PullDynamicScheduleUpdateRequest message. A value of 0 or no value means that no update interval applies. + Only relevant in a dynamic charging profile. |
| `dynUpdateTime` | string (date-time) | No |  | *(2.1)* Time at which limits or setpoints in this charging profile were last updated by a PullDynamicScheduleUpdateRequest or UpdateDynamicScheduleRequest or by an external actor. + Only relevant in a dynamic charging profile. |
| `invalidAfterOfflineDuration` | boolean | No |  | *(2.1)* When set to true this charging profile will not be valid anymore after being offline for more than _maxOfflineDuration_. + When absent defaults to false. |
| `maxOfflineDuration` | integer | No |  | *(2.1)* Period in seconds that this charging profile remains valid after the Charging Station has gone offline. After this period the charging profile becomes invalid for as long as it is offline and the Charging Station reverts back to a valid profile with a lower stack level. If _invalidAfterOfflineDuration_ is true, then this charging profile will become permanently invalid. A value of 0 means that the charging profile is immediately invalid while offline. When the field is absent, then no timeout applies and the charging profile remains valid when offline. |
| `priceScheduleSignature` | string | No | maxLength: 256 | *(2.1)* ISO 15118-20 signature for all price schedules in _chargingSchedules_. + Note: for 256-bit elliptic curves (like secp256k1) the ECDSA signature is 512 bits (64 bytes) and for 521-bit curves (like secp521r1) the signature is 1042 bits. This equals 131 bytes, which can be encoded as base64 in 176 bytes. |
| `recurrencyKind` | [RecurrencyKindEnumType](#recurrencykindenumtype) | No |  |  |
| `transactionId` | string | No | maxLength: 36 | SHALL only be included if ChargingProfilePurpose is set to TxProfile in a SetChargingProfileRequest. The transactionId is used to match the profile to a specific transaction. |
| `validFrom` | string (date-time) | No |  | Point in time at which the profile starts to be valid. If absent, the profile is valid as soon as it is received by the Charging Station. |
| `validTo` | string (date-time) | No |  | Point in time at which the profile stops to be valid. If absent, the profile is valid until it is replaced by another profile. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingSchedulePeriodType

Charging schedule period structure defines a time period in a charging schedule. It is used in: CompositeScheduleType and in ChargingScheduleType. When used in a NotifyEVChargingScheduleRequest only _startPeriod_, _limit_, _limit_L2_, _limit_L3_ are relevant.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `startPeriod` | integer | **Yes** |  | Start of the period, in seconds from the start of schedule. The value of StartPeriod also defines the stop time of the previous period. |
| `dischargeLimit` | number | No | max: 0.0 | *(2.1)* Limit in _chargingRateUnit_ that the EV is allowed to discharge with. Note, these are negative values in order to be consistent with _setpoint_, which can be positive and negative. + For AC this field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `dischargeLimit_L2` | number | No | max: 0.0 | *(2.1)* Limit in _chargingRateUnit_ on phase L2 that the EV is allowed to discharge with. |
| `dischargeLimit_L3` | number | No | max: 0.0 | *(2.1)* Limit in _chargingRateUnit_ on phase L3 that the EV is allowed to discharge with. |
| `evseSleep` | boolean | No |  | *(2.1)* If true, the EVSE must turn off power electronics/modules associated with this transaction. Default value when absent is false. |
| `limit` | number | No |  | Optional only when not required by the _operationMode_, as in CentralSetpoint, ExternalSetpoint, ExternalLimits, LocalFrequency, LocalLoadBalancing. + Charging rate limit during the schedule period, in the applicable _chargingRateUnit_. This SHOULD be a non-negative value; a negative value is only supported for backwards compatibility with older systems that use a negative value to specify a discharging limit. When using _chargingRateUnit_ = W, this field represents the sum of the power of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `limit_L2` | number | No |  | *(2.1)* Charging rate limit on phase L2 in the applicable _chargingRateUnit_. |
| `limit_L3` | number | No |  | *(2.1)* Charging rate limit on phase L3 in the applicable _chargingRateUnit_. |
| `numberPhases` | integer | No | min: 0.0, max: 3.0 | The number of phases that can be used for charging. + For a DC EVSE this field should be omitted. + For an AC EVSE a default value of _numberPhases_ = 3 will be assumed if the field is absent. |
| `operationMode` | [OperationModeEnumType](#operationmodeenumtype) | No |  |  |
| `phaseToUse` | integer | No | min: 0.0, max: 3.0 | Values: 1..3, Used if numberPhases=1 and if the EVSE is capable of switching the phase connected to the EV, i.e. ACPhaseSwitchingSupported is defined and true. It’s not allowed unless both conditions above are true. If both conditions are true, and phaseToUse is omitted, the Charging Station / EVSE will make the selection on its own. |
| `preconditioningRequest` | boolean | No |  | *(2.1)* If true, the EV should attempt to keep the BMS preconditioned for this time interval. |
| `setpoint` | number | No |  | *(2.1)* Setpoint in _chargingRateUnit_ that the EV should follow as close as possible. Use negative values for discharging. + When a limit and/or _dischargeLimit_ are given the overshoot when following _setpoint_ must remain within these values. This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `setpointReactive` | number | No |  | *(2.1)* Setpoint for reactive power (or current) in _chargingRateUnit_ that the EV should follow as closely as possible. Positive values for inductive, negative for capacitive reactive power or current. + This field represents the sum of all phases, unless values are provided for L2 and L3, in which case this field represents phase L1. |
| `setpointReactive_L2` | number | No |  | *(2.1)* Setpoint for reactive power (or current) in _chargingRateUnit_ that the EV should follow on phase L2 as closely as possible. |
| `setpointReactive_L3` | number | No |  | *(2.1)* Setpoint for reactive power (or current) in _chargingRateUnit_ that the EV should follow on phase L3 as closely as possible. |
| `setpoint_L2` | number | No |  | *(2.1)* Setpoint in _chargingRateUnit_ that the EV should follow on phase L2 as close as possible. |
| `setpoint_L3` | number | No |  | *(2.1)* Setpoint in _chargingRateUnit_ that the EV should follow on phase L3 as close as possible. |
| `v2xBaseline` | number | No |  | *(2.1)* Power value that, when present, is used as a baseline on top of which values from _v2xFreqWattCurve_ and _v2xSignalWattCurve_ are added. |
| `v2xFreqWattCurve` | [V2XFreqWattPointType](#v2xfreqwattpointtype)[] | No | minItems: 1, maxItems: 20 |  |
| `v2xSignalWattCurve` | [V2XSignalWattPointType](#v2xsignalwattpointtype)[] | No | minItems: 1, maxItems: 20 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** GetCompositeSchedule, NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingScheduleType

Charging schedule structure defines a list of charging periods, as used in: NotifyEVChargingScheduleRequest and ChargingProfileType. When used in a NotifyEVChargingScheduleRequest only _duration_ and _chargingSchedulePeriod_ are relevant and _chargingRateUnit_ must be 'W'. + An ISO 15118-20 session may provide either an _absolutePriceSchedule_ or a _priceLevelSchedule_. An ISO 15118-2 session can only provide a_salesTariff_ element. The field _digestValue_ is used when price schedule or sales tariff are signed. image::images/ChargingSchedule-Simple.png[]

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingRateUnit` | [ChargingRateUnitEnumType](#chargingrateunitenumtype) | **Yes** |  |  |
| `chargingSchedulePeriod` | [ChargingSchedulePeriodType](#chargingscheduleperiodtype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `id` | integer | **Yes** |  |  |
| `absolutePriceSchedule` | [AbsolutePriceScheduleType](#absolutepricescheduletype) | No |  |  |
| `digestValue` | string | No | maxLength: 88 | *(2.1)* Base64 encoded hash (SHA256 for ISO 15118-2, SHA512 for ISO 15118-20) of the EXI price schedule element. Used in signature. |
| `duration` | integer | No |  | Duration of the charging schedule in seconds. If the duration is left empty, the last period will continue indefinitely or until end of the transaction in case startSchedule is absent. |
| `limitAtSoC` | [LimitAtSoCType](#limitatsoctype) | No |  |  |
| `minChargingRate` | number | No |  | Minimum charging rate supported by the EV. The unit of measure is defined by the chargingRateUnit. This parameter is intended to be used by a local smart charging algorithm to optimize the power allocation for in the case a charging process is inefficient at lower charging rates. |
| `powerTolerance` | number | No |  | *(2.1)* Power tolerance when following EVPowerProfile. |
| `priceLevelSchedule` | [PriceLevelScheduleType](#pricelevelscheduletype) | No |  |  |
| `randomizedDelay` | integer | No | min: 0.0 | *(2.1)* Defaults to 0. When _randomizedDelay_ not equals zero, then the start of each ChargingSchedulePeriodType is delayed by a randomly chosen number of seconds between 0 and _randomizedDelay_. Only allowed for TxProfile and TxDefaultProfile. |
| `salesTariff` | [SalesTariffType](#salestarifftype) | No |  |  |
| `signatureId` | integer | No | min: 0.0 | *(2.1)* Id of this element for referencing in a signature. |
| `startSchedule` | string (date-time) | No |  | Starting point of an absolute schedule or recurring schedule. |
| `useLocalTime` | boolean | No |  | *(2.1)* Defaults to false. When true, disregard time zone offset in dateTime fields of _ChargingScheduleType_ and use unqualified local time at Charging Station instead. This allows the same Absolute or Recurring charging profile to be used in both summer and winter time. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ComponentType

A physical or logical component

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | **Yes** | maxLength: 50 | Name of the component. Name should be taken from the list of standardized component names whenever possible. Case Insensitive. strongly advised to use Camel Case. |
| `evse` | [EVSEType](#evsetype) | No |  |  |
| `instance` | string | No | maxLength: 50 | Name of instance in case the component exists as multiple instances. Case Insensitive. strongly advised to use Camel Case. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** GetMonitoringReport, GetReport, GetVariables, NotifyDisplayMessages, NotifyEvent, NotifyMonitoringReport, NotifyReport, SetDisplayMessage, SetVariableMonitoring, SetVariables

---

### ConsumptionCostType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `cost` | [CostType](#costtype)[] | **Yes** | minItems: 1, maxItems: 3 |  |
| `startValue` | number | **Yes** |  | The lowest level of consumption that defines the starting point of this consumption block. The block interval extends to the start of the next interval. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### CostType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `amount` | integer | **Yes** |  | The estimated or actual cost per kWh |
| `costKind` | [CostKindEnumType](#costkindenumtype) | **Yes** |  |  |
| `amountMultiplier` | integer | No |  | Values: -3..3, The amountMultiplier defines the exponent to base 10 (dec). The final value is determined by: amount * 10 ^ amountMultiplier |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### CustomDataType

This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `vendorId` | string | **Yes** | maxLength: 255 |  |


**Used in:** AFRRSignal, AdjustPeriodicEventStream, Authorize, BatterySwap, BootNotification, CancelReservation, CertificateSigned, ChangeAvailability, ChangeTransactionTariff, ClearCache, ClearChargingProfile, ClearDERControl, ClearDisplayMessage, ClearTariffs, ClearVariableMonitoring, ClearedChargingLimit, ClosePeriodicEventStream, CostUpdated, CustomerInformation, DataTransfer, DeleteCertificate, FirmwareStatusNotification, Get15118EVCertificate, GetBaseReport, GetCertificateChainStatus, GetCertificateStatus, GetChargingProfiles, GetCompositeSchedule, GetDERControl, GetDisplayMessages, GetInstalledCertificateIds, GetLocalListVersion, GetLog, GetMonitoringReport, GetPeriodicEventStream, GetReport, GetTariffs, GetTransactionStatus, GetVariables, Heartbeat, InstallCertificate, LogStatusNotification, MeterValues, NotifyAllowedEnergyTransfer, NotifyChargingLimit, NotifyCustomerInformation, NotifyDERAlarm, NotifyDERStartStop, NotifyDisplayMessages, NotifyEVChargingNeeds, NotifyEVChargingSchedule, NotifyEvent, NotifyMonitoringReport, NotifyPeriodicEventStream, NotifyPriorityCharging, NotifyReport, NotifySettlement, NotifyWebPaymentStarted, OpenPeriodicEventStream, PublishFirmware, PublishFirmwareStatusNotification, PullDynamicScheduleUpdate, ReportChargingProfiles, ReportDERControl, RequestBatterySwap, RequestStartTransaction, RequestStopTransaction, ReservationStatusUpdate, ReserveNow, Reset, SecurityEventNotification, SendLocalList, SetChargingProfile, SetDERControl, SetDefaultTariff, SetDisplayMessage, SetMonitoringBase, SetMonitoringLevel, SetNetworkProfile, SetVariableMonitoring, SetVariables, SignCertificate, StatusNotification, TransactionEvent, TriggerMessage, UnlockConnector, UnpublishFirmware, UpdateDynamicSchedule, UpdateFirmware, UsePriorityCharging, VatNumberValidation

---

### EVSEType

Electric Vehicle Supply Equipment

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** | min: 0.0 | EVSE Identifier. This contains a number (> 0) designating an EVSE of the Charging Station. |
| `connectorId` | integer | No | min: 0.0 | An id to designate a specific connector (on an EVSE) by connector index number. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** ChangeAvailability, GetMonitoringReport, GetReport, GetVariables, NotifyDisplayMessages, NotifyEvent, NotifyMonitoringReport, NotifyReport, SetDisplayMessage, SetVariableMonitoring, SetVariables, TransactionEvent, TriggerMessage

---

### IdTokenInfoType

Contains status information about an identifier. It is advised to not stop charging for a token that expires during charging, as ExpiryDate is only used for caching purposes. If ExpiryDate is not given, the status has no end date.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [AuthorizationStatusEnumType](#authorizationstatusenumtype) | **Yes** |  |  |
| `cacheExpiryDateTime` | string (date-time) | No |  | Date and Time after which the token must be considered invalid. |
| `chargingPriority` | integer | No |  | Priority from a business point of view. Default priority is 0, The range is from -9 to 9. Higher values indicate a higher priority. The chargingPriority in TransactionEventResponse overrules this one. |
| `evseId` | integer[] | No | minItems: 1 | Only used when the IdToken is only valid for one or more specific EVSEs, not for the entire Charging Station. |
| `groupIdToken` | [IdTokenType](#idtokentype) | No |  |  |
| `language1` | string | No | maxLength: 8 | Preferred user interface language of identifier user. Contains a language code as defined in RFC5646. |
| `language2` | string | No | maxLength: 8 | Second preferred user interface language of identifier user. Don’t use when language1 is omitted, has to be different from language1. Contains a language code as defined in RFC5646. |
| `personalMessage` | [MessageContentType](#messagecontenttype) | No |  |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, SendLocalList, TransactionEvent

---

### IdTokenType

Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | string | **Yes** | maxLength: 255 | *(2.1)* IdToken is case insensitive. Might hold the hidden id of an RFID tag, but can for example also contain a UUID. |
| `type` | string | **Yes** | maxLength: 20 | *(2.1)* Enumeration of possible idToken types. Values defined in Appendix as IdTokenEnumStringType. |
| `additionalInfo` | [AdditionalInfoType](#additionalinfotype)[] | No | minItems: 1 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, BatterySwap, CustomerInformation, RequestBatterySwap, RequestStartTransaction, ReserveNow, SendLocalList, TransactionEvent

---

### LimitAtSoCType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `limit` | number | **Yes** |  | Charging rate limit beyond the SoC value. The unit is defined by _chargingSchedule.chargingRateUnit_. |
| `soc` | integer | **Yes** | min: 0.0, max: 100.0 | The SoC value beyond which the charging rate limit should be applied. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### MessageContentType

Contains message details, for a message to be displayed on a Charging Station.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `content` | string | **Yes** | maxLength: 1024 | *(2.1)* Required. Message contents. + Maximum length supported by Charging Station is given in OCPPCommCtrlr.FieldLength["MessageContentType.content"]. Maximum length defaults to 1024. |
| `format` | [MessageFormatEnumType](#messageformatenumtype) | **Yes** |  |  |
| `language` | string | No | maxLength: 8 | Message language identifier. Contains a language code as defined in RFC5646. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, NotifyDisplayMessages, SendLocalList, SetDefaultTariff, SetDisplayMessage, TransactionEvent

---

### OverstayRuleListType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `overstayRule` | [OverstayRuleType](#overstayruletype)[] | **Yes** | minItems: 1, maxItems: 5 |  |
| `overstayPowerThreshold` | [RationalNumberType](#rationalnumbertype) | No |  |  |
| `overstayTimeThreshold` | integer | No |  | Time till overstay is applied in seconds. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### OverstayRuleType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `overstayFee` | [RationalNumberType](#rationalnumbertype) | **Yes** |  |  |
| `overstayFeePeriod` | integer | **Yes** |  | Time till overstay will be reapplied |
| `startTime` | integer | **Yes** |  | Time in seconds after trigger of the parent Overstay Rules for this particular fee to apply. |
| `overstayRuleDescription` | string | No | maxLength: 32 | Human readable string to identify the overstay rule. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### PeriodicEventStreamParamsType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `interval` | integer | No | min: 0.0 | Time in seconds after which stream data is sent. |
| `values` | integer | No | min: 0.0 | Number of items to be sent together in stream. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** AdjustPeriodicEventStream, GetPeriodicEventStream, OpenPeriodicEventStream, SetVariableMonitoring

---

### PriceLevelScheduleEntryType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `duration` | integer | **Yes** |  | The amount of seconds that define the duration of this given PriceLevelScheduleEntry. |
| `priceLevel` | integer | **Yes** | min: 0.0 | Defines the price level of this PriceLevelScheduleEntry (referring to NumberOfPriceLevels). Small values for the PriceLevel represent a cheaper PriceLevelScheduleEntry. Large values for the PriceLevel represent a more expensive PriceLevelScheduleEntry. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### PriceLevelScheduleType

The PriceLevelScheduleType is modeled after the same type that is defined in ISO 15118-20, such that if it is supplied by an EMSP as a signed EXI message, the conversion from EXI to JSON (in OCPP) and back to EXI (for ISO 15118-20) does not change the digest and therefore does not invalidate the signature.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `numberOfPriceLevels` | integer | **Yes** | min: 0.0 | Defines the overall number of distinct price level elements used across all PriceLevelSchedules. |
| `priceLevelScheduleEntries` | [PriceLevelScheduleEntryType](#pricelevelscheduleentrytype)[] | **Yes** | minItems: 1, maxItems: 100 |  |
| `priceScheduleId` | integer | **Yes** | min: 0.0 | Unique ID of this price schedule. |
| `timeAnchor` | string (date-time) | **Yes** |  | Starting point of this price schedule. |
| `priceScheduleDescription` | string | No | maxLength: 32 | Description of the price schedule. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### PriceRuleStackType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `duration` | integer | **Yes** |  | Duration of the stack of price rules. he amount of seconds that define the duration of the given PriceRule(s). |
| `priceRule` | [PriceRuleType](#priceruletype)[] | **Yes** | minItems: 1, maxItems: 8 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### PriceRuleType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `energyFee` | [RationalNumberType](#rationalnumbertype) | **Yes** |  |  |
| `powerRangeStart` | [RationalNumberType](#rationalnumbertype) | **Yes** |  |  |
| `carbonDioxideEmission` | integer | No | min: 0.0 | Number of grams of CO2 per kWh. |
| `parkingFee` | [RationalNumberType](#rationalnumbertype) | No |  |  |
| `parkingFeePeriod` | integer | No |  | The duration of the parking fee period (in seconds). When the time enters into a ParkingFeePeriod, the ParkingFee will apply to the session. . |
| `renewableGenerationPercentage` | integer | No | min: 0.0, max: 100.0 | Percentage of the power that is created by renewable resources. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### PriceType

Price with and without tax. At least one of _exclTax_, _inclTax_ must be present.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `exclTax` | number | No |  | Price/cost excluding tax. Can be absent if _inclTax_ is present. |
| `inclTax` | number | No |  | Price/cost including tax. Can be absent if _exclTax_ is present. |
| `taxRates` | [TaxRateType](#taxratetype)[] | No | minItems: 1, maxItems: 5 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff, TransactionEvent

---

### RationalNumberType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `exponent` | integer | **Yes** |  | The exponent to base 10 (dec) |
| `value` | integer | **Yes** |  | Value which shall be multiplied. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### RelativeTimeIntervalType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `start` | integer | **Yes** |  | Start of the interval, in seconds from NOW. |
| `duration` | integer | No |  | Duration of the interval, in seconds. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### SalesTariffEntryType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `relativeTimeInterval` | [RelativeTimeIntervalType](#relativetimeintervaltype) | **Yes** |  |  |
| `consumptionCost` | [ConsumptionCostType](#consumptioncosttype)[] | No | minItems: 1, maxItems: 3 |  |
| `ePriceLevel` | integer | No | min: 0.0 | Defines the price level of this SalesTariffEntry (referring to NumEPriceLevels). Small values for the EPriceLevel represent a cheaper TariffEntry. Large values for the EPriceLevel represent a more expensive TariffEntry. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### SalesTariffType

A SalesTariff provided by a Mobility Operator (EMSP) . NOTE: This dataType is based on dataTypes from ISO 15118-2.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** | min: 0.0 | SalesTariff identifier used to identify one sales tariff. An SAID remains a unique identifier for one schedule throughout a charging session. |
| `salesTariffEntry` | [SalesTariffEntryType](#salestariffentrytype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `numEPriceLevels` | integer | No | min: 0.0 | Defines the overall number of distinct price levels used across all provided SalesTariff elements. |
| `salesTariffDescription` | string | No | maxLength: 32 | A human readable title/short description of the sales tariff e.g. for HMI display purposes. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### StatusInfoType

Element providing more information about the status.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `reasonCode` | string | **Yes** | maxLength: 20 | A predefined code for the reason why the status is returned in this response. The string is case-insensitive. |
| `additionalInfo` | string | No | maxLength: 1024 | Additional text to provide detailed information. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** AFRRSignal, AdjustPeriodicEventStream, BootNotification, CancelReservation, CertificateSigned, ChangeAvailability, ChangeTransactionTariff, ClearCache, ClearChargingProfile, ClearDERControl, ClearDisplayMessage, ClearTariffs, ClearVariableMonitoring, CustomerInformation, DataTransfer, DeleteCertificate, FirmwareStatusNotification, Get15118EVCertificate, GetBaseReport, GetCertificateStatus, GetChargingProfiles, GetCompositeSchedule, GetDERControl, GetDisplayMessages, GetInstalledCertificateIds, GetLog, GetMonitoringReport, GetReport, GetTariffs, GetVariables, InstallCertificate, LogStatusNotification, NotifyAllowedEnergyTransfer, NotifyEVChargingNeeds, NotifyEVChargingSchedule, OpenPeriodicEventStream, PublishFirmware, PublishFirmwareStatusNotification, PullDynamicScheduleUpdate, RequestBatterySwap, RequestStartTransaction, RequestStopTransaction, ReserveNow, Reset, SendLocalList, SetChargingProfile, SetDERControl, SetDefaultTariff, SetDisplayMessage, SetMonitoringBase, SetMonitoringLevel, SetNetworkProfile, SetVariableMonitoring, SetVariables, SignCertificate, TriggerMessage, UnlockConnector, UpdateDynamicSchedule, UpdateFirmware, UsePriorityCharging, VatNumberValidation

---

### TariffConditionsFixedType

These conditions describe if a FixedPrice applies at start of the transaction. When more than one restriction is set, they are to be treated as a logical AND. All need to be valid before this price is active. NOTE: _startTimeOfDay_ and _endTimeOfDay_ are in local time, because it is the time in the tariff as it is shown to the EV driver at the Charging Station. A Charging Station will convert this to the internal time zone that it uses (which is recommended to be UTC, see section Generic chapter 3.1) when performing cost calculation.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `dayOfWeek` | [DayOfWeekEnumType](#dayofweekenumtype)[] | No | minItems: 1, maxItems: 7 | Day(s) of the week this is tariff applies. |
| `endTimeOfDay` | string | No |  | End time of day in local time. Same syntax as _startTimeOfDay_. + If end time < start time then the period wraps around to the next day. + To stop at end of the day use: 00:00. |
| `evseKind` | [EvseKindEnumType](#evsekindenumtype) | No |  |  |
| `paymentBrand` | string | No | maxLength: 20 | For which payment brand this (adhoc) tariff applies. Can be used to add a surcharge for certain payment brands. Based on value of _additionalIdToken_ from _idToken.additionalInfo.type_ = "PaymentBrand". |
| `paymentRecognition` | string | No | maxLength: 20 | Type of adhoc payment, e.g. CC, Debit. Based on value of _additionalIdToken_ from _idToken.additionalInfo.type_ = "PaymentRecognition". |
| `startTimeOfDay` | string | No |  | Start time of day in local time. + Format as per RFC 3339: time-hour ":" time-minute + Must be in 24h format with leading zeros. Hour/Minute separator: ":" Regex: ([0-1][0-9]\|2[0-3]):[0-5][0-9] |
| `validFromDate` | string | No |  | Start date in local time, for example: 2015-12-24. Valid from this day (inclusive). + Format as per RFC 3339: full-date + Regex: ([12][0-9]{3})-(0[1-9]\|1[0-2])-(0[1-9]\|[12][0-9]\|3[01]) |
| `validToDate` | string | No |  | End date in local time, for example: 2015-12-27. Valid until this day (exclusive). Same syntax as _validFromDate_. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffConditionsType

These conditions describe if and when a TariffEnergyType or TariffTimeType applies during a transaction. When more than one restriction is set, they are to be treated as a logical AND. All need to be valid before this price is active. For reverse energy flow (discharging) negative values of energy, power and current are used. NOTE: _minXXX_ (where XXX = Kwh/A/Kw) must be read as "closest to zero", and _maxXXX_ as "furthest from zero". For example, a *charging* power range from 10 kW to 50 kWh is given by _minPower_ = 10000 and _maxPower_ = 50000, and a *discharging* power range from -10 kW to -50 kW is given by _minPower_ = -10 and _maxPower_ = -50. NOTE: _startTimeOfDay_ and _endTimeOfDay_ are in local time, because it is the time in the tariff as it is shown to the EV driver at the Charging Station. A Charging Station will convert this to the internal time zone that it uses (which is recommended to be UTC, see section Generic chapter 3.1) when performing cost calculation.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `dayOfWeek` | [DayOfWeekEnumType](#dayofweekenumtype)[] | No | minItems: 1, maxItems: 7 | Day(s) of the week this is tariff applies. |
| `endTimeOfDay` | string | No |  | End time of day in local time. Same syntax as _startTimeOfDay_. + If end time < start time then the period wraps around to the next day. + To stop at end of the day use: 00:00. |
| `evseKind` | [EvseKindEnumType](#evsekindenumtype) | No |  |  |
| `maxChargingTime` | integer | No |  | Maximum duration in seconds the charging MUST last (exclusive). When the duration of a charging is shorter than the defined value, this price is or becomes active. After that moment, this price is no longer active. |
| `maxCurrent` | number | No |  | Sum of the maximum current (in Amperes) over all phases, for example 20 A. When the EV is charging with less than the defined amount of current, this price becomes/is active. If the charging current is or becomes higher, this price is not or no longer valid and becomes inactive. This is NOT about the maximum current over the entire transaction. |
| `maxEnergy` | number | No |  | Maximum consumed energy in Wh, for example 50000 Wh. Valid until this amount of energy (exclusive) being used. |
| `maxIdleTime` | integer | No |  | Maximum duration in seconds the idle period (i.e. not charging) MUST last (exclusive). When the duration of idle time is shorter than the defined value, this price is or becomes active. After that moment, this price is no longer active. |
| `maxPower` | number | No |  | Maximum power in W, for example 20000 W. When the EV is charging with less than the defined amount of power, this price becomes/is active. If the charging power is or becomes higher, this price is not or no longer valid and becomes inactive. This is NOT about the maximum power over the entire transaction. |
| `maxTime` | integer | No |  | Maximum duration in seconds the transaction (charging & idle) MUST last (exclusive). When the duration of a transaction is shorter than the defined value, this price is or becomes active. After that moment, this price is no longer active. |
| `minChargingTime` | integer | No |  | Minimum duration in seconds the charging MUST last (inclusive). When the duration of a charging is longer than the defined value, this price is or becomes active. Before that moment, this price is not yet active. |
| `minCurrent` | number | No |  | Sum of the minimum current (in Amperes) over all phases, for example 5 A. When the EV is charging with more than, or equal to, the defined amount of current, this price is/becomes active. If the charging current is or becomes lower, this price is not or no longer valid and becomes inactive. + This is NOT about the minimum current over the entire transaction. |
| `minEnergy` | number | No |  | Minimum consumed energy in Wh, for example 20000 Wh. Valid from this amount of energy (inclusive) being used. |
| `minIdleTime` | integer | No |  | Minimum duration in seconds the idle period (i.e. not charging) MUST last (inclusive). When the duration of the idle time is longer than the defined value, this price is or becomes active. Before that moment, this price is not yet active. |
| `minPower` | number | No |  | Minimum power in W, for example 5000 W. When the EV is charging with more than, or equal to, the defined amount of power, this price is/becomes active. If the charging power is or becomes lower, this price is not or no longer valid and becomes inactive. This is NOT about the minimum power over the entire transaction. |
| `minTime` | integer | No |  | Minimum duration in seconds the transaction (charging & idle) MUST last (inclusive). When the duration of a transaction is longer than the defined value, this price is or becomes active. Before that moment, this price is not yet active. |
| `startTimeOfDay` | string | No |  | Start time of day in local time. + Format as per RFC 3339: time-hour ":" time-minute + Must be in 24h format with leading zeros. Hour/Minute separator: ":" Regex: ([0-1][0-9]\|2[0-3]):[0-5][0-9] |
| `validFromDate` | string | No |  | Start date in local time, for example: 2015-12-24. Valid from this day (inclusive). + Format as per RFC 3339: full-date + Regex: ([12][0-9]{3})-(0[1-9]\|1[0-2])-(0[1-9]\|[12][0-9]\|3[01]) |
| `validToDate` | string | No |  | End date in local time, for example: 2015-12-27. Valid until this day (exclusive). Same syntax as _validFromDate_. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffEnergyPriceType

Tariff with optional conditions for an energy price.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `priceKwh` | number | **Yes** |  | Price per kWh (excl. tax) for this element. |
| `conditions` | [TariffConditionsType](#tariffconditionstype) | No |  |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffEnergyType

Price elements and tax for energy

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `prices` | [TariffEnergyPriceType](#tariffenergypricetype)[] | **Yes** | minItems: 1 |  |
| `taxRates` | [TaxRateType](#taxratetype)[] | No | minItems: 1, maxItems: 5 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffFixedPriceType

Tariff with optional conditions for a fixed price.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `priceFixed` | number | **Yes** |  | Fixed price for this element e.g. a start fee. |
| `conditions` | [TariffConditionsFixedType](#tariffconditionsfixedtype) | No |  |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffFixedType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `prices` | [TariffFixedPriceType](#tarifffixedpricetype)[] | **Yes** | minItems: 1 |  |
| `taxRates` | [TaxRateType](#taxratetype)[] | No | minItems: 1, maxItems: 5 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffTimePriceType

Tariff with optional conditions for a time duration price.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `priceMinute` | number | **Yes** |  | Price per minute (excl. tax) for this element. |
| `conditions` | [TariffConditionsType](#tariffconditionstype) | No |  |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffTimeType

Price elements and tax for time

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `prices` | [TariffTimePriceType](#tarifftimepricetype)[] | **Yes** | minItems: 1 |  |
| `taxRates` | [TaxRateType](#taxratetype)[] | No | minItems: 1, maxItems: 5 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TariffType

A tariff is described by fields with prices for: energy, charging time, idle time, fixed fee, reservation time, reservation fixed fee. + Each of these fields may have (optional) conditions that specify when a price is applicable. + The _description_ contains a human-readable explanation of the tariff to be shown to the user. + The other fields are parameters that define the tariff. These are used by the charging station to calculate the price.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currency` | string | **Yes** | maxLength: 3 | Currency code according to ISO 4217 |
| `tariffId` | string | **Yes** | maxLength: 60 | Unique id of tariff |
| `chargingTime` | [TariffTimeType](#tarifftimetype) | No |  |  |
| `description` | [MessageContentType](#messagecontenttype)[] | No | minItems: 1, maxItems: 10 |  |
| `energy` | [TariffEnergyType](#tariffenergytype) | No |  |  |
| `fixedFee` | [TariffFixedType](#tarifffixedtype) | No |  |  |
| `idleTime` | [TariffTimeType](#tarifftimetype) | No |  |  |
| `maxCost` | [PriceType](#pricetype) | No |  |  |
| `minCost` | [PriceType](#pricetype) | No |  |  |
| `reservationFixed` | [TariffFixedType](#tarifffixedtype) | No |  |  |
| `reservationTime` | [TariffTimeType](#tarifftimetype) | No |  |  |
| `validFrom` | string (date-time) | No |  | Time when this tariff becomes active. When absent, it is immediately active. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff

---

### TaxRateType

Tax percentage

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `tax` | number | **Yes** |  | Tax percentage |
| `type` | string | **Yes** | maxLength: 20 | Type of this tax, e.g. "Federal ", "State", for information on receipt. |
| `stack` | integer | No | min: 0.0 | Stack level for this type of tax. Default value, when absent, is 0. + _stack_ = 0: tax on net price; + _stack_ = 1: tax added on top of _stack_ 0; + _stack_ = 2: tax added on top of _stack_ 1, etc. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, ChangeTransactionTariff, SetDefaultTariff, TransactionEvent

---

### TaxRuleType

Part of ISO 15118-20 price schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `appliesToEnergyFee` | boolean | **Yes** |  | Indicates whether this tax applies to Energy Fees. |
| `appliesToMinimumMaximumCost` | boolean | **Yes** |  | Indicates whether this tax applies to Minimum/Maximum Cost. |
| `appliesToOverstayFee` | boolean | **Yes** |  | Indicates whether this tax applies to Overstay Fees. |
| `appliesToParkingFee` | boolean | **Yes** |  | Indicates whether this tax applies to Parking Fees. |
| `taxRate` | [RationalNumberType](#rationalnumbertype) | **Yes** |  |  |
| `taxRuleID` | integer | **Yes** | min: 0.0 | Id for the tax rule. |
| `taxIncludedInPrice` | boolean | No |  | Indicates whether the tax is included in any price or not. |
| `taxRuleName` | string | No | maxLength: 100 | Human readable string to identify the tax rule. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### V2XFreqWattPointType

*(2.1)* A point of a frequency-watt curve.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `frequency` | number | **Yes** |  | Net frequency in Hz. |
| `power` | number | **Yes** |  | Power in W to charge (positive) or discharge (negative) at specified frequency. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** GetCompositeSchedule, NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### V2XSignalWattPointType

*(2.1)* A point of a signal-watt curve.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `power` | number | **Yes** |  | Power in W to charge (positive) or discharge (negative) at specified frequency. |
| `signal` | integer | **Yes** |  | Signal value from an AFRRSignalRequest. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** GetCompositeSchedule, NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### VariableType

Reference key to a component-variable.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | **Yes** | maxLength: 50 | Name of the variable. Name should be taken from the list of standardized variable names whenever possible. Case Insensitive. strongly advised to use Camel Case. |
| `instance` | string | No | maxLength: 50 | Name of instance in case the variable exists as multiple instances. Case Insensitive. strongly advised to use Camel Case. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** GetMonitoringReport, GetReport, GetVariables, NotifyEvent, NotifyMonitoringReport, NotifyReport, SetVariableMonitoring, SetVariables

---
