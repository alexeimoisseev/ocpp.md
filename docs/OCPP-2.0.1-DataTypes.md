# OCPP 2.0.1 — Data Types Reference

> **Purpose:** Complete reference of all reusable data types and enumerations in OCPP 2.0.1.
> Generated from the official OCA JSON schemas.
>
> **See also:** Message schemas by functional block:
> [Schemas — Provisioning](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Provisioning.md) |
> [Schemas — Authorization](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Authorization.md) |
> [Schemas — Transactions](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Transactions.md) |
> [Schemas — SmartCharging](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-SmartCharging.md) |
> [Schemas — Firmware](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Firmware.md) |
> [Schemas — Security](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Security.md) |
> [Schemas — Diagnostics](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Diagnostics.md) |
> [Schemas — Availability](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Availability.md) |
> [Schemas — Reservation](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Reservation.md) |
> [Schemas — Display](./OCPP-2.0.1-Schemas/OCPP-2.0.1-Schemas-Display.md) |

**16 Enum Types** | **18 Composite Types**

---

## Table of Contents

### Enums

- [AttributeEnumType](#attributeenumtype)
- [AuthorizationStatusEnumType](#authorizationstatusenumtype)
- [ChargingLimitSourceEnumType](#charginglimitsourceenumtype)
- [ChargingProfileKindEnumType](#chargingprofilekindenumtype)
- [ChargingProfilePurposeEnumType](#chargingprofilepurposeenumtype)
- [ChargingRateUnitEnumType](#chargingrateunitenumtype)
- [CostKindEnumType](#costkindenumtype)
- [GenericDeviceModelStatusEnumType](#genericdevicemodelstatusenumtype)
- [GenericStatusEnumType](#genericstatusenumtype)
- [HashAlgorithmEnumType](#hashalgorithmenumtype)
- [IdTokenEnumType](#idtokenenumtype)
- [MessageFormatEnumType](#messageformatenumtype)
- [MessagePriorityEnumType](#messagepriorityenumtype)
- [MessageStateEnumType](#messagestateenumtype)
- [MonitorEnumType](#monitorenumtype)
- [RecurrencyKindEnumType](#recurrencykindenumtype)

### Composite Types

- [AdditionalInfoType](#additionalinfotype)
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
- [MessageContentType](#messagecontenttype)
- [RelativeTimeIntervalType](#relativetimeintervaltype)
- [SalesTariffEntryType](#salestariffentrytype)
- [SalesTariffType](#salestarifftype)
- [StatusInfoType](#statusinfotype)
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

### ChargingLimitSourceEnumType

Represents the source of the charging limit.

| Value |
|-------|
| `EMS` |
| `Other` |
| `SO` |
| `CSO` |

**Used in:** ClearedChargingLimit, GetChargingProfiles, NotifyChargingLimit, ReportChargingProfiles

---

### ChargingProfileKindEnumType

Indicates the kind of schedule.

| Value |
|-------|
| `Absolute` |
| `Recurring` |
| `Relative` |

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

**Used in:** ClearChargingProfile, GetChargingProfiles, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingRateUnitEnumType

The unit of measure Limit is expressed in.

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

**Used in:** GetCompositeSchedule, NotifyEVChargingSchedule, PublishFirmware, SetMonitoringLevel, SignCertificate

---

### HashAlgorithmEnumType

Used algorithms for the hashes provided.

| Value |
|-------|
| `SHA256` |
| `SHA384` |
| `SHA512` |

**Used in:** Authorize, CustomerInformation, DeleteCertificate, GetCertificateStatus, GetInstalledCertificateIds

---

### IdTokenEnumType

Enumeration of possible idToken types.

| Value |
|-------|
| `Central` |
| `eMAID` |
| `ISO14443` |
| `ISO15693` |
| `KeyCode` |
| `Local` |
| `MacAddress` |
| `NoAuthorization` |

**Used in:** Authorize, CustomerInformation, RequestStartTransaction, ReserveNow, SendLocalList, TransactionEvent

---

### MessageFormatEnumType

Format of the message.

| Value |
|-------|
| `ASCII` |
| `HTML` |
| `URI` |
| `UTF8` |

**Used in:** Authorize, NotifyDisplayMessages, SendLocalList, SetDisplayMessage, TransactionEvent

---

### MessagePriorityEnumType

With what priority should this message be shown

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

**Used in:** NotifyMonitoringReport, SetVariableMonitoring

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

### AdditionalInfoType

Contains a case insensitive identifier to use for the authorization and the type of authorization to support multiple forms of identifiers.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `additionalIdToken` | string | **Yes** | maxLength: 36 | This field specifies the additional IdToken. |
| `type` | string | **Yes** | maxLength: 50 | This defines the type of the additionalIdToken. This is a custom type, so the implementation needs to be agreed upon by all involved parties. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, CustomerInformation, RequestStartTransaction, ReserveNow, SendLocalList, TransactionEvent

---

### CertificateHashDataType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `hashAlgorithm` | [HashAlgorithmEnumType](#hashalgorithmenumtype) | **Yes** |  |  |
| `issuerKeyHash` | string | **Yes** | maxLength: 128 | Hashed value of the issuers public key |
| `issuerNameHash` | string | **Yes** | maxLength: 128 | Hashed value of the Issuer DN (Distinguished Name). |
| `serialNumber` | string | **Yes** | maxLength: 40 | The serial number of the certificate. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** CustomerInformation, DeleteCertificate, GetInstalledCertificateIds

---

### ChargingProfileType

A ChargingProfile consists of ChargingSchedule, describing the amount of power or current that can be delivered per time interval.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileKind` | [ChargingProfileKindEnumType](#chargingprofilekindenumtype) | **Yes** |  |  |
| `chargingProfilePurpose` | [ChargingProfilePurposeEnumType](#chargingprofilepurposeenumtype) | **Yes** |  |  |
| `chargingSchedule` | [ChargingScheduleType](#chargingscheduletype)[] | **Yes** | minItems: 1, maxItems: 3 |  |
| `id` | integer | **Yes** |  | Id of ChargingProfile. |
| `stackLevel` | integer | **Yes** |  | Value determining level in hierarchy stack of profiles. Higher values have precedence over lower values. Lowest level is 0. |
| `recurrencyKind` | [RecurrencyKindEnumType](#recurrencykindenumtype) | No |  |  |
| `transactionId` | string | No | maxLength: 36 | SHALL only be included if ChargingProfilePurpose is set to TxProfile. The transactionId is used to match the profile to a specific transaction. |
| `validFrom` | string (date-time) | No |  | Point in time at which the profile starts to be valid. If absent, the profile is valid as soon as it is received by the Charging Station. |
| `validTo` | string (date-time) | No |  | Point in time at which the profile stops to be valid. If absent, the profile is valid until it is replaced by another profile. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingSchedulePeriodType

Charging schedule period structure defines a time period in a charging schedule.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `limit` | number | **Yes** |  | Charging rate limit during the schedule period, in the applicable chargingRateUnit, for example in Amperes (A) or Watts (W). Accepts at most one digit fraction (e.g. 8.1). |
| `startPeriod` | integer | **Yes** |  | Start of the period, in seconds from the start of schedule. The value of StartPeriod also defines the stop time of the previous period. |
| `numberPhases` | integer | No |  | The number of phases that can be used for charging. If a number of phases is needed, numberPhases=3 will be assumed unless another number is given. |
| `phaseToUse` | integer | No |  | Values: 1..3, Used if numberPhases=1 and if the EVSE is capable of switching the phase connected to the EV, i.e. ACPhaseSwitchingSupported is defined and true. It’s not allowed unless both conditions above are true. If both conditions are true, and phaseToUse is omitted, the Charging Station / EVSE will make the selection on its own. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** GetCompositeSchedule, NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### ChargingScheduleType

Charging schedule structure defines a list of charging periods, as used in: GetCompositeSchedule.conf and ChargingProfile.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingRateUnit` | [ChargingRateUnitEnumType](#chargingrateunitenumtype) | **Yes** |  |  |
| `chargingSchedulePeriod` | [ChargingSchedulePeriodType](#chargingscheduleperiodtype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `id` | integer | **Yes** |  | Identifies the ChargingSchedule. |
| `duration` | integer | No |  | Duration of the charging schedule in seconds. If the duration is left empty, the last period will continue indefinitely or until end of the transaction if chargingProfilePurpose = TxProfile. |
| `minChargingRate` | number | No |  | Minimum charging rate supported by the EV. The unit of measure is defined by the chargingRateUnit. This parameter is intended to be used by a local smart charging algorithm to optimize the power allocation for in the case a charging process is inefficient at lower charging rates. Accepts at most one digit fraction (e.g. 8.1) |
| `salesTariff` | [SalesTariffType](#salestarifftype) | No |  |  |
| `startSchedule` | string (date-time) | No |  | Starting point of an absolute schedule. If absent the schedule will be relative to start of charging. |
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


**Used in:** Authorize, BootNotification, CancelReservation, CertificateSigned, ChangeAvailability, ClearCache, ClearChargingProfile, ClearDisplayMessage, ClearVariableMonitoring, ClearedChargingLimit, CostUpdated, CustomerInformation, DataTransfer, DeleteCertificate, FirmwareStatusNotification, Get15118EVCertificate, GetBaseReport, GetCertificateStatus, GetChargingProfiles, GetCompositeSchedule, GetDisplayMessages, GetInstalledCertificateIds, GetLocalListVersion, GetLog, GetMonitoringReport, GetReport, GetTransactionStatus, GetVariables, Heartbeat, InstallCertificate, LogStatusNotification, MeterValues, NotifyChargingLimit, NotifyCustomerInformation, NotifyDisplayMessages, NotifyEVChargingNeeds, NotifyEVChargingSchedule, NotifyEvent, NotifyMonitoringReport, NotifyReport, PublishFirmware, PublishFirmwareStatusNotification, ReportChargingProfiles, RequestStartTransaction, RequestStopTransaction, ReservationStatusUpdate, ReserveNow, Reset, SecurityEventNotification, SendLocalList, SetChargingProfile, SetDisplayMessage, SetMonitoringBase, SetMonitoringLevel, SetNetworkProfile, SetVariableMonitoring, SetVariables, SignCertificate, StatusNotification, TransactionEvent, TriggerMessage, UnlockConnector, UnpublishFirmware, UpdateFirmware

---

### EVSEType

Electric Vehicle Supply Equipment

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** |  | EVSE Identifier. This contains a number (> 0) designating an EVSE of the Charging Station. |
| `connectorId` | integer | No |  | An id to designate a specific connector (on an EVSE) by connector index number. |
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
| `idToken` | string | **Yes** | maxLength: 36 | IdToken is case insensitive. Might hold the hidden id of an RFID tag, but can for example also contain a UUID. |
| `type` | [IdTokenEnumType](#idtokenenumtype) | **Yes** |  |  |
| `additionalInfo` | [AdditionalInfoType](#additionalinfotype)[] | No | minItems: 1 |  |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, CustomerInformation, RequestStartTransaction, ReserveNow, SendLocalList, TransactionEvent

---

### MessageContentType

Contains message details, for a message to be displayed on a Charging Station.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `content` | string | **Yes** | maxLength: 512 | Message contents. |
| `format` | [MessageFormatEnumType](#messageformatenumtype) | **Yes** |  |  |
| `language` | string | No | maxLength: 8 | Message language identifier. Contains a language code as defined in RFC5646. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** Authorize, NotifyDisplayMessages, SendLocalList, SetDisplayMessage, TransactionEvent

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

NOTE: This dataType is based on dataTypes from ISO 15118-2.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** |  | SalesTariff identifier used to identify one sales tariff. An SAID remains a unique identifier for one schedule throughout a charging session. |
| `salesTariffEntry` | [SalesTariffEntryType](#salestariffentrytype)[] | **Yes** | minItems: 1, maxItems: 1024 |  |
| `numEPriceLevels` | integer | No |  | Defines the overall number of distinct price levels used across all provided SalesTariff elements. |
| `salesTariffDescription` | string | No | maxLength: 32 | A human readable title/short description of the sales tariff e.g. for HMI display purposes. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** NotifyChargingLimit, NotifyEVChargingSchedule, ReportChargingProfiles, RequestStartTransaction, SetChargingProfile

---

### StatusInfoType

Element providing more information about the status.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `reasonCode` | string | **Yes** | maxLength: 20 | A predefined code for the reason why the status is returned in this response. The string is case-insensitive. |
| `additionalInfo` | string | No | maxLength: 512 | Additional text to provide detailed information. |
| `customData` | [CustomDataType](#customdatatype) | No |  |  |


**Used in:** BootNotification, CancelReservation, CertificateSigned, ChangeAvailability, ClearCache, ClearChargingProfile, ClearDisplayMessage, ClearVariableMonitoring, CustomerInformation, DataTransfer, DeleteCertificate, Get15118EVCertificate, GetBaseReport, GetCertificateStatus, GetChargingProfiles, GetCompositeSchedule, GetDisplayMessages, GetInstalledCertificateIds, GetLog, GetMonitoringReport, GetReport, GetVariables, InstallCertificate, NotifyEVChargingNeeds, NotifyEVChargingSchedule, PublishFirmware, RequestStartTransaction, RequestStopTransaction, ReserveNow, Reset, SendLocalList, SetChargingProfile, SetDisplayMessage, SetMonitoringBase, SetMonitoringLevel, SetNetworkProfile, SetVariableMonitoring, SetVariables, SignCertificate, TriggerMessage, UnlockConnector, UpdateFirmware

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
