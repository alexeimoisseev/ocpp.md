# OCPP 2.1 Schemas — Provisioning

> **Functional Block:** B
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [BootNotification](#bootnotification) (CS → CSMS)
- [Heartbeat](#heartbeat) (CS → CSMS)
- [GetBaseReport](#getbasereport) (CSMS → CS)
- [GetReport](#getreport) (CSMS → CS)
- [NotifyReport](#notifyreport) (CS → CSMS)
- [GetVariables](#getvariables) (CSMS → CS)
- [SetVariables](#setvariables) (CSMS → CS)
- [SetNetworkProfile](#setnetworkprofile) (CSMS → CS)
- [Reset](#reset) (CSMS → CS)

---

## BootNotification

**Direction:** CS → CSMS

### BootNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingStation` | [ChargingStationType](#chargingstationtype) | **Yes** |  |  |
| `reason` | [BootReasonEnumType](#bootreasonenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example BootNotificationRequest</summary>

```json
{
  "chargingStation": {
    "model": "string",
    "vendorName": "string"
  },
  "reason": "ApplicationReset"
}
```

</details>

### BootNotificationResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currentTime` | string (date-time) | **Yes** |  | This contains the CSMS’s current time. |
| `interval` | integer | **Yes** |  | When Status is Accepted, this contains the heartbeat interval in seconds. If the CSMS returns something other than Accepted, the value of the interval field indicates the minimum wait time before sending a next BootNotification request. |
| `status` | [RegistrationStatusEnumType](#registrationstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Heartbeat

**Direction:** CS → CSMS

### HeartbeatRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### HeartbeatResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currentTime` | string (date-time) | **Yes** |  | Contains the current time of the CSMS. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetBaseReport

**Direction:** CSMS → CS

### GetBaseReportRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `reportBase` | [ReportBaseEnumType](#reportbaseenumtype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | The Id of the request. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetBaseReportRequest</summary>

```json
{
  "reportBase": "ConfigurationInventory",
  "requestId": 0
}
```

</details>

### GetBaseReportResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericDeviceModelStatusEnumType](../OCPP-2.1-DataTypes.md#genericdevicemodelstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetReport

**Direction:** CSMS → CS

### GetReportRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestId` | integer | **Yes** |  | The Id of the request. |
| `componentCriteria` | [ComponentCriterionEnumType](#componentcriterionenumtype)[] | No | minItems: 1, maxItems: 4 | This field contains criteria for components for which a report is requested |
| `componentVariable` | [ComponentVariableType](#componentvariabletype)[] | No | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetReportRequest</summary>

```json
{
  "requestId": 0
}
```

</details>

### GetReportResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericDeviceModelStatusEnumType](../OCPP-2.1-DataTypes.md#genericdevicemodelstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyReport

**Direction:** CS → CSMS

### NotifyReportRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `generatedAt` | string (date-time) | **Yes** |  | Timestamp of the moment this message was generated at the Charging Station. |
| `requestId` | integer | **Yes** |  | The id of the GetReportRequest or GetBaseReportRequest that requested this report |
| `seqNo` | integer | **Yes** | min: 0.0 | Sequence number of this message. First message starts at 0. |
| `reportData` | [ReportDataType](#reportdatatype)[] | No | minItems: 1 |  |
| `tbc` | boolean | No |  | “to be continued” indicator. Indicates whether another part of the report follows in an upcoming notifyReportRequest message. Default value when omitted is false. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyReportRequest</summary>

```json
{
  "generatedAt": "2024-01-15T10:30:00Z",
  "requestId": 0,
  "seqNo": 0
}
```

</details>

### NotifyReportResponse

*No required fields. An empty `{}` is a valid response.*

---

## GetVariables

**Direction:** CSMS → CS

### GetVariablesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `getVariableData` | [GetVariableDataType](#getvariabledatatype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetVariablesRequest</summary>

```json
{
  "getVariableData": [
    {
      "component": "{...}",
      "variable": "{...}"
    }
  ]
}
```

</details>

### GetVariablesResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `getVariableResult` | [GetVariableResultType](#getvariableresulttype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## SetVariables

**Direction:** CSMS → CS

### SetVariablesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `setVariableData` | [SetVariableDataType](#setvariabledatatype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetVariablesRequest</summary>

```json
{
  "setVariableData": [
    {
      "attributeValue": "string",
      "component": "{...}",
      "variable": "{...}"
    }
  ]
}
```

</details>

### SetVariablesResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `setVariableResult` | [SetVariableResultType](#setvariableresulttype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## SetNetworkProfile

**Direction:** CSMS → CS

### SetNetworkProfileRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `configurationSlot` | integer | **Yes** |  | Slot in which the configuration should be stored. |
| `connectionData` | [NetworkConnectionProfileType](#networkconnectionprofiletype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetNetworkProfileRequest</summary>

```json
{
  "configurationSlot": 0,
  "connectionData": {
    "ocppInterface": "Wired0",
    "ocppTransport": "SOAP",
    "messageTimeout": 0,
    "ocppCsmsUrl": "string",
    "securityProfile": 0
  }
}
```

</details>

### SetNetworkProfileResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [SetNetworkProfileStatusEnumType](#setnetworkprofilestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Reset

**Direction:** CSMS → CS

### ResetRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `type` | [ResetEnumType](#resetenumtype) | **Yes** |  |  |
| `evseId` | integer | No | min: 0.0 | This contains the ID of a specific EVSE that needs to be reset, instead of the entire Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ResetRequest</summary>

```json
{
  "type": "Immediate"
}
```

</details>

### ResetResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ResetStatusEnumType](#resetstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### APNAuthenticationEnumType

Authentication method.

| Value |
|-------|
| `PAP` |
| `CHAP` |
| `NONE` |
| `AUTO` |

**Used in:** SetNetworkProfile

---

### BootReasonEnumType

This contains the reason for sending this message to the CSMS.

| Value |
|-------|
| `ApplicationReset` |
| `FirmwareUpdate` |
| `LocalReset` |
| `PowerUp` |
| `RemoteReset` |
| `ScheduledReset` |
| `Triggered` |
| `Unknown` |
| `Watchdog` |

**Used in:** BootNotification

---

### ComponentCriterionEnumType

| Value |
|-------|
| `Active` |
| `Available` |
| `Enabled` |
| `Problem` |

**Used in:** GetReport

---

### DataEnumType

Data type of this variable.

| Value |
|-------|
| `string` |
| `decimal` |
| `integer` |
| `dateTime` |
| `boolean` |
| `OptionList` |
| `SequenceList` |
| `MemberList` |

**Used in:** NotifyReport

---

### GetVariableStatusEnumType

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `UnknownComponent` |
| `UnknownVariable` |
| `NotSupportedAttributeType` |

**Used in:** GetVariables

---

### MutabilityEnumType

Defines the mutability of this attribute. Default is ReadWrite when omitted.

**Default:** `ReadWrite`

| Value |
|-------|
| `ReadOnly` |
| `WriteOnly` |
| `ReadWrite` |

**Used in:** NotifyReport

---

### OCPPInterfaceEnumType

Applicable Network Interface. Charging Station is allowed to use a different network interface to connect if the given one does not work.

| Value |
|-------|
| `Wired0` |
| `Wired1` |
| `Wired2` |
| `Wired3` |
| `Wireless0` |
| `Wireless1` |
| `Wireless2` |
| `Wireless3` |
| `Any` |

**Used in:** SetNetworkProfile

---

### OCPPTransportEnumType

Defines the transport protocol (e.g. SOAP or JSON). Note: SOAP is not supported in OCPP 2.x, but is supported by earlier versions of OCPP.

| Value |
|-------|
| `SOAP` |
| `JSON` |

**Used in:** SetNetworkProfile

---

### OCPPVersionEnumType

*(2.1)* This field is ignored, since the OCPP version to use is determined during the websocket handshake. The field is only kept for backwards compatibility with the OCPP 2.0.1 JSON schema.

| Value |
|-------|
| `OCPP12` |
| `OCPP15` |
| `OCPP16` |
| `OCPP20` |
| `OCPP201` |
| `OCPP21` |

**Used in:** SetNetworkProfile

---

### RegistrationStatusEnumType

This contains whether the Charging Station has been registered within the CSMS.

| Value |
|-------|
| `Accepted` |
| `Pending` |
| `Rejected` |

**Used in:** BootNotification

---

### ReportBaseEnumType

This field specifies the report base.

| Value |
|-------|
| `ConfigurationInventory` |
| `FullInventory` |
| `SummaryInventory` |

**Used in:** GetBaseReport

---

### ResetEnumType

This contains the type of reset that the Charging Station or EVSE should perform.

| Value |
|-------|
| `Immediate` |
| `OnIdle` |
| `ImmediateAndResume` |

**Used in:** Reset

---

### ResetStatusEnumType

This indicates whether the Charging Station is able to perform the reset.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Scheduled` |

**Used in:** Reset

---

### SetNetworkProfileStatusEnumType

Result of operation.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Failed` |

**Used in:** SetNetworkProfile

---

### SetVariableStatusEnumType

Result status of setting the variable.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `UnknownComponent` |
| `UnknownVariable` |
| `NotSupportedAttributeType` |
| `RebootRequired` |

**Used in:** SetVariables

---

### VPNEnumType

Type of VPN

| Value |
|-------|
| `IKEv2` |
| `IPSec` |
| `L2TP` |
| `PPTP` |

**Used in:** SetNetworkProfile

---

### APNType

Collection of configuration data needed to make a data-connection over a cellular network. NOTE: When asking a GSM modem to dial in, it is possible to specify which mobile operator should be used. This can be done with the mobile country code (MCC) in combination with a mobile network code (MNC). Example: If your preferred network is Vodafone Netherlands, the MCC=204 and the MNC=04 which means the key PreferredNetwork = 20404 Some modems allows to specify a preferred network, which means, if this network is not available, a different network is used. If you specify UseOnlyPreferredNetwork and this network is not available, the modem will not dial in.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `apn` | string | **Yes** | maxLength: 2000 | The Access Point Name as an URL. |
| `apnAuthentication` | [APNAuthenticationEnumType](#apnauthenticationenumtype) | **Yes** |  |  |
| `apnPassword` | string | No | maxLength: 64 | *(2.1)* APN Password. |
| `apnUserName` | string | No | maxLength: 50 | APN username. |
| `preferredNetwork` | string | No | maxLength: 6 | Preferred network, written as MCC and MNC concatenated. See note. |
| `simPin` | integer | No |  | SIM card pin code. |
| `useOnlyPreferredNetwork` | boolean | No |  | Default: false. Use only the preferred Network, do not dial in when not available. See Note. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetNetworkProfile

---

### ChargingStationType

The physical system where an Electrical Vehicle (EV) can be charged.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `model` | string | **Yes** | maxLength: 20 | Defines the model of the device. |
| `vendorName` | string | **Yes** | maxLength: 50 | Identifies the vendor (not necessarily in a unique manner). |
| `firmwareVersion` | string | No | maxLength: 50 | This contains the firmware version of the Charging Station. |
| `modem` | [ModemType](#modemtype) | No |  |  |
| `serialNumber` | string | No | maxLength: 25 | Vendor-specific device identifier. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** BootNotification

---

### ComponentVariableType

Class to report components, variables and variable attributes and characteristics.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.1-DataTypes.md#variabletype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetMonitoringReport, GetReport

---

### GetVariableDataType

Class to hold parameters for GetVariables request.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `attributeType` | [AttributeEnumType](../OCPP-2.1-DataTypes.md#attributeenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetVariables

---

### GetVariableResultType

Class to hold results of GetVariables request.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `attributeStatus` | [GetVariableStatusEnumType](#getvariablestatusenumtype) | **Yes** |  |  |
| `component` | [ComponentType](../OCPP-2.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `attributeStatusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `attributeType` | [AttributeEnumType](../OCPP-2.1-DataTypes.md#attributeenumtype) | No |  |  |
| `attributeValue` | string | No | maxLength: 2500 | Value of requested attribute type of component-variable. This field can only be empty when the given status is NOT accepted. The Configuration Variable ReportingValueSize can be used to limit GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetVariables

---

### ModemType

Defines parameters required for initiating and maintaining wireless communication with other devices.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `iccid` | string | No | maxLength: 20 | This contains the ICCID of the modem’s SIM card. |
| `imsi` | string | No | maxLength: 20 | This contains the IMSI of the modem’s SIM card. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** BootNotification

---

### NetworkConnectionProfileType

The NetworkConnectionProfile defines the functional and technical parameters of a communication link.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `messageTimeout` | integer | **Yes** |  | Duration in seconds before a message send by the Charging Station via this network connection times-out. The best setting depends on the underlying network and response times of the CSMS. If you are looking for a some guideline: use 30 seconds as a starting point. |
| `ocppCsmsUrl` | string | **Yes** | maxLength: 2000 | URL of the CSMS(s) that this Charging Station communicates with, without the Charging Station identity part. + The SecurityCtrlr.Identity field is appended to _ocppCsmsUrl_ to provide the full websocket URL. |
| `ocppInterface` | [OCPPInterfaceEnumType](#ocppinterfaceenumtype) | **Yes** |  |  |
| `ocppTransport` | [OCPPTransportEnumType](#ocpptransportenumtype) | **Yes** |  |  |
| `securityProfile` | integer | **Yes** | min: 0.0 | This field specifies the security profile used when connecting to the CSMS with this NetworkConnectionProfile. |
| `apn` | [APNType](#apntype) | No |  |  |
| `basicAuthPassword` | string | No | maxLength: 64 | *(2.1)* BasicAuthPassword to use for security profile 1 or 2. |
| `identity` | string | No | maxLength: 48 | *(2.1)* Charging Station identity to be used as the basic authentication username. |
| `ocppVersion` | [OCPPVersionEnumType](#ocppversionenumtype) | No |  |  |
| `vpn` | [VPNType](#vpntype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetNetworkProfile

---

### ReportDataType

Class to report components, variables and variable attributes and characteristics.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `variableAttribute` | [VariableAttributeType](#variableattributetype)[] | **Yes** | minItems: 1, maxItems: 4 |  |
| `variableCharacteristics` | [VariableCharacteristicsType](#variablecharacteristicstype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyReport

---

### SetVariableDataType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `attributeValue` | string | **Yes** | maxLength: 2500 | Value to be assigned to attribute of variable. This value is allowed to be an empty string (""). The Configuration Variable ConfigurationValueSize can be used to limit SetVariableData.attributeValue and VariableCharacteristics.valuesList. The max size of these values will always remain equal. |
| `component` | [ComponentType](../OCPP-2.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `attributeType` | [AttributeEnumType](../OCPP-2.1-DataTypes.md#attributeenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetVariables

---

### SetVariableResultType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `attributeStatus` | [SetVariableStatusEnumType](#setvariablestatusenumtype) | **Yes** |  |  |
| `component` | [ComponentType](../OCPP-2.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `attributeStatusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `attributeType` | [AttributeEnumType](../OCPP-2.1-DataTypes.md#attributeenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetVariables

---

### VPNType

VPN Configuration settings

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `key` | string | **Yes** | maxLength: 255 | VPN shared secret. |
| `password` | string | **Yes** | maxLength: 64 | *(2.1)* VPN Password. |
| `server` | string | **Yes** | maxLength: 2000 | VPN Server Address |
| `type` | [VPNEnumType](#vpnenumtype) | **Yes** |  |  |
| `user` | string | **Yes** | maxLength: 50 | VPN User |
| `group` | string | No | maxLength: 50 | VPN group. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetNetworkProfile

---

### VariableAttributeType

Attribute data of a variable.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `constant` | boolean | No |  | If true, value that will never be changed by the Charging Station at runtime. Default when omitted is false. Default: `False` |
| `mutability` | [MutabilityEnumType](#mutabilityenumtype) | No |  |  |
| `persistent` | boolean | No |  | If true, value will be persistent across system reboots or power down. Default when omitted is false. Default: `False` |
| `type` | [AttributeEnumType](../OCPP-2.1-DataTypes.md#attributeenumtype) | No |  |  |
| `value` | string | No | maxLength: 2500 | Value of the attribute. May only be omitted when mutability is set to 'WriteOnly'. The Configuration Variable ReportingValueSize can be used to limit GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyReport

---

### VariableCharacteristicsType

Fixed read-only parameters of a variable.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `dataType` | [DataEnumType](#dataenumtype) | **Yes** |  |  |
| `supportsMonitoring` | boolean | **Yes** |  | Flag indicating if this variable supports monitoring. |
| `maxElements` | integer | No | min: 1.0 | *(2.1)* Maximum number of elements from _valuesList_ that are supported as _attributeValue_. |
| `maxLimit` | number | No |  | Maximum possible value of this variable. When the datatype of this Variable is String, OptionList, SequenceList or MemberList, this field defines the maximum length of the (CSV) string. |
| `minLimit` | number | No |  | Minimum possible value of this variable. |
| `unit` | string | No | maxLength: 16 | Unit of the variable. When the transmitted value has a unit, this field SHALL be included. |
| `valuesList` | string | No | maxLength: 1000 | Mandatory when _dataType_ = OptionList, MemberList or SequenceList. In that case _valuesList_ specifies the allowed values for the type. The length of this field can be limited by DeviceDataCtrlr.ConfigurationValueSize. * OptionList: The (Actual) Variable value must be a single value from the reported (CSV) enumeration list. * MemberList: The (Actual) Variable value may be an (unordered) (sub-)set of the reported (CSV) valid values list. * SequenceList: The (Actual) Variable value may be an ordered (priority, etc) (sub-)set of the reported (CSV) valid values. This is a comma separated list. The Configuration Variable ConfigurationValueSize can be used to limit SetVariableData.attributeValue and VariableCharacteristics.valuesList. The max size of these values will always remain equal. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyReport

---
