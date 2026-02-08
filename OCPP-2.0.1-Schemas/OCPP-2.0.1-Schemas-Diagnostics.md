# OCPP 2.0.1 Schemas — Diagnostics

> **Functional Block:** K
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [GetLog](#getlog) (CSMS → CS)
- [LogStatusNotification](#logstatusnotification) (CS → CSMS)
- [NotifyEvent](#notifyevent) (CS → CSMS)
- [SetMonitoringBase](#setmonitoringbase) (CSMS → CS)
- [SetVariableMonitoring](#setvariablemonitoring) (CSMS → CS)
- [SetMonitoringLevel](#setmonitoringlevel) (CSMS → CS)
- [GetMonitoringReport](#getmonitoringreport) (CSMS → CS)
- [ClearVariableMonitoring](#clearvariablemonitoring) (CSMS → CS)
- [NotifyMonitoringReport](#notifymonitoringreport) (CS → CSMS)
- [CustomerInformation](#customerinformation) (CSMS → CS)
- [NotifyCustomerInformation](#notifycustomerinformation) (CS → CSMS)

---

## GetLog

**Direction:** CSMS → CS

### GetLogRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `log` | [LogParametersType](#logparameterstype) | **Yes** |  |  |
| `logType` | [LogEnumType](#logenumtype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | The Id of this request |
| `retries` | integer | No |  | This specifies how many times the Charging Station must try to upload the log before giving up. If this field is not present, it is left to Charging Station to decide how many times it wants to retry. |
| `retryInterval` | integer | No |  | The interval in seconds after which a retry may be attempted. If this field is not present, it is left to Charging Station to decide how long to wait between attempts. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetLogRequest</summary>

```json
{
  "log": {
    "remoteLocation": "string"
  },
  "logType": "DiagnosticsLog",
  "requestId": 0
}
```

</details>

### GetLogResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [LogStatusEnumType](#logstatusenumtype) | **Yes** |  |  |
| `filename` | string | No | maxLength: 255 | This contains the name of the log file that will be uploaded. This field is not present when no logging information is available. |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## LogStatusNotification

**Direction:** CS → CSMS

### LogStatusNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [UploadLogStatusEnumType](#uploadlogstatusenumtype) | **Yes** |  |  |
| `requestId` | integer | No |  | The request id that was provided in GetLogRequest that started this log upload. This field is mandatory, unless the message was triggered by a TriggerMessageRequest AND there is no log upload ongoing. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example LogStatusNotificationRequest</summary>

```json
{
  "status": "BadMessage"
}
```

</details>

### LogStatusNotificationResponse

*No required fields. An empty `{}` is a valid response.*

---

## NotifyEvent

**Direction:** CS → CSMS

### NotifyEventRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `eventData` | [EventDataType](#eventdatatype)[] | **Yes** | minItems: 1 |  |
| `generatedAt` | string (date-time) | **Yes** |  | Timestamp of the moment this message was generated at the Charging Station. |
| `seqNo` | integer | **Yes** |  | Sequence number of this message. First message starts at 0. |
| `tbc` | boolean | No |  | “to be continued” indicator. Indicates whether another part of the report follows in an upcoming notifyEventRequest message. Default value when omitted is false. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyEventRequest</summary>

```json
{
  "eventData": [
    {
      "eventId": 0,
      "timestamp": "2024-01-15T10:30:00Z",
      "trigger": "Alerting",
      "actualValue": "string",
      "eventNotificationType": "HardWiredNotification",
      "component": "{...}",
      "variable": "{...}"
    }
  ],
  "generatedAt": "2024-01-15T10:30:00Z",
  "seqNo": 0
}
```

</details>

### NotifyEventResponse

*No required fields. An empty `{}` is a valid response.*

---

## SetMonitoringBase

**Direction:** CSMS → CS

### SetMonitoringBaseRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `monitoringBase` | [MonitoringBaseEnumType](#monitoringbaseenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetMonitoringBaseRequest</summary>

```json
{
  "monitoringBase": "All"
}
```

</details>

### SetMonitoringBaseResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericDeviceModelStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericdevicemodelstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## SetVariableMonitoring

**Direction:** CSMS → CS

### SetVariableMonitoringRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `setMonitoringData` | [SetMonitoringDataType](#setmonitoringdatatype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetVariableMonitoringRequest</summary>

```json
{
  "setMonitoringData": [
    {
      "value": 0.0,
      "type": "UpperThreshold",
      "severity": 0,
      "component": "{...}",
      "variable": "{...}"
    }
  ]
}
```

</details>

### SetVariableMonitoringResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `setMonitoringResult` | [SetMonitoringResultType](#setmonitoringresulttype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## SetMonitoringLevel

**Direction:** CSMS → CS

### SetMonitoringLevelRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `severity` | integer | **Yes** |  | The Charging Station SHALL only report events with a severity number lower than or equal to this severity. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event. + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetMonitoringLevelRequest</summary>

```json
{
  "severity": 0
}
```

</details>

### SetMonitoringLevelResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetMonitoringReport

**Direction:** CSMS → CS

### GetMonitoringReportRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestId` | integer | **Yes** |  | The Id of the request. |
| `componentVariable` | [ComponentVariableType](#componentvariabletype)[] | No | minItems: 1 |  |
| `monitoringCriteria` | [MonitoringCriterionEnumType](#monitoringcriterionenumtype)[] | No | minItems: 1, maxItems: 3 | This field contains criteria for components for which a monitoring report is requested |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetMonitoringReportRequest</summary>

```json
{
  "requestId": 0
}
```

</details>

### GetMonitoringReportResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericDeviceModelStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericdevicemodelstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearVariableMonitoring

**Direction:** CSMS → CS

### ClearVariableMonitoringRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer[] | **Yes** | minItems: 1 | List of the monitors to be cleared, identified by there Id. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ClearVariableMonitoringRequest</summary>

```json
{
  "id": [
    0
  ]
}
```

</details>

### ClearVariableMonitoringResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `clearMonitoringResult` | [ClearMonitoringResultType](#clearmonitoringresulttype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyMonitoringReport

**Direction:** CS → CSMS

### NotifyMonitoringReportRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `generatedAt` | string (date-time) | **Yes** |  | Timestamp of the moment this message was generated at the Charging Station. |
| `requestId` | integer | **Yes** |  | The id of the GetMonitoringRequest that requested this report. |
| `seqNo` | integer | **Yes** |  | Sequence number of this message. First message starts at 0. |
| `monitor` | [MonitoringDataType](#monitoringdatatype)[] | No | minItems: 1 |  |
| `tbc` | boolean | No |  | “to be continued” indicator. Indicates whether another part of the monitoringData follows in an upcoming notifyMonitoringReportRequest message. Default value when omitted is false. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyMonitoringReportRequest</summary>

```json
{
  "generatedAt": "2024-01-15T10:30:00Z",
  "requestId": 0,
  "seqNo": 0
}
```

</details>

### NotifyMonitoringReportResponse

*No required fields. An empty `{}` is a valid response.*

---

## CustomerInformation

**Direction:** CSMS → CS

### CustomerInformationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `clear` | boolean | **Yes** |  | Flag indicating whether the Charging Station should clear all information about the customer referred to. |
| `report` | boolean | **Yes** |  | Flag indicating whether the Charging Station should return NotifyCustomerInformationRequest messages containing information about the customer referred to. |
| `requestId` | integer | **Yes** |  | The Id of the request. |
| `customerCertificate` | [CertificateHashDataType](../OCPP-2.0.1-DataTypes.md#certificatehashdatatype) | No |  |  |
| `customerIdentifier` | string | No | maxLength: 64 | A (e.g. vendor specific) identifier of the customer this request refers to. This field contains a custom identifier other than IdToken and Certificate. One of the possible identifiers (customerIdentifier, customerIdToken or customerCertificate) should be in the request message. |
| `idToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example CustomerInformationRequest</summary>

```json
{
  "clear": false,
  "report": false,
  "requestId": 0
}
```

</details>

### CustomerInformationResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [CustomerInformationStatusEnumType](#customerinformationstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyCustomerInformation

**Direction:** CS → CSMS

### NotifyCustomerInformationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `data` | string | **Yes** | maxLength: 512 | (Part of) the requested data. No format specified in which the data is returned. Should be human readable. |
| `generatedAt` | string (date-time) | **Yes** |  | Timestamp of the moment this message was generated at the Charging Station. |
| `requestId` | integer | **Yes** |  | The Id of the request. |
| `seqNo` | integer | **Yes** |  | Sequence number of this message. First message starts at 0. |
| `tbc` | boolean | No |  | “to be continued” indicator. Indicates whether another part of the monitoringData follows in an upcoming notifyMonitoringReportRequest message. Default value when omitted is false. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyCustomerInformationRequest</summary>

```json
{
  "data": "string",
  "generatedAt": "2024-01-15T10:30:00Z",
  "requestId": 0,
  "seqNo": 0
}
```

</details>

### NotifyCustomerInformationResponse

*No required fields. An empty `{}` is a valid response.*

---

## Local Types

*Types used only within this block's messages.*

### ClearMonitoringStatusEnumType

Result of the clear request for this monitor, identified by its Id.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NotFound` |

**Used in:** ClearVariableMonitoring

---

### CustomerInformationStatusEnumType

Indicates whether the request was accepted.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Invalid` |

**Used in:** CustomerInformation

---

### EventNotificationEnumType

Specifies the event notification type of the message.

| Value |
|-------|
| `HardWiredNotification` |
| `HardWiredMonitor` |
| `PreconfiguredMonitor` |
| `CustomMonitor` |

**Used in:** NotifyEvent

---

### EventTriggerEnumType

Type of monitor that triggered this event, e.g. exceeding a threshold value.

| Value |
|-------|
| `Alerting` |
| `Delta` |
| `Periodic` |

**Used in:** NotifyEvent

---

### LogEnumType

This contains the type of log file that the Charging Station should send.

| Value |
|-------|
| `DiagnosticsLog` |
| `SecurityLog` |

**Used in:** GetLog

---

### LogStatusEnumType

This field indicates whether the Charging Station was able to accept the request.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `AcceptedCanceled` |

**Used in:** GetLog

---

### MonitoringBaseEnumType

Specify which monitoring base will be set

| Value |
|-------|
| `All` |
| `FactoryDefault` |
| `HardWiredOnly` |

**Used in:** SetMonitoringBase

---

### MonitoringCriterionEnumType

| Value |
|-------|
| `ThresholdMonitoring` |
| `DeltaMonitoring` |
| `PeriodicMonitoring` |

**Used in:** GetMonitoringReport

---

### SetMonitoringStatusEnumType

Status is OK if a value could be returned. Otherwise this will indicate the reason why a value could not be returned.

| Value |
|-------|
| `Accepted` |
| `UnknownComponent` |
| `UnknownVariable` |
| `UnsupportedMonitorType` |
| `Rejected` |
| `Duplicate` |

**Used in:** SetVariableMonitoring

---

### UploadLogStatusEnumType

This contains the status of the log upload.

| Value |
|-------|
| `BadMessage` |
| `Idle` |
| `NotSupportedOperation` |
| `PermissionDenied` |
| `Uploaded` |
| `UploadFailure` |
| `Uploading` |
| `AcceptedCanceled` |

**Used in:** LogStatusNotification

---

### ClearMonitoringResultType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** |  | Id of the monitor of which a clear was requested. |
| `status` | [ClearMonitoringStatusEnumType](#clearmonitoringstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ClearVariableMonitoring

---

### ComponentVariableType

Class to report components, variables and variable attributes and characteristics.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.0.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.0.1-DataTypes.md#variabletype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetMonitoringReport, GetReport

---

### EventDataType

Class to report an event notification for a component-variable.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `actualValue` | string | **Yes** | maxLength: 2500 | Actual value (_attributeType_ Actual) of the variable. The Configuration Variable ReportingValueSize can be used to limit GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal. |
| `component` | [ComponentType](../OCPP-2.0.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `eventId` | integer | **Yes** |  | Identifies the event. This field can be referred to as a cause by other events. |
| `eventNotificationType` | [EventNotificationEnumType](#eventnotificationenumtype) | **Yes** |  |  |
| `timestamp` | string (date-time) | **Yes** |  | Timestamp of the moment the report was generated. |
| `trigger` | [EventTriggerEnumType](#eventtriggerenumtype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.0.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `cause` | integer | No |  | Refers to the Id of an event that is considered to be the cause for this event. |
| `cleared` | boolean | No |  | _Cleared_ is set to true to report the clearing of a monitored situation, i.e. a 'return to normal'. |
| `techCode` | string | No | maxLength: 50 | Technical (error) code as reported by component. |
| `techInfo` | string | No | maxLength: 500 | Technical detail information as reported by component. |
| `transactionId` | string | No | maxLength: 36 | If an event notification is linked to a specific transaction, this field can be used to specify its transactionId. |
| `variableMonitoringId` | integer | No |  | Identifies the VariableMonitoring which triggered the event. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyEvent

---

### LogParametersType

Generic class for the configuration of logging entries.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `remoteLocation` | string | **Yes** | maxLength: 512 | The URL of the location at the remote system where the log should be stored. |
| `latestTimestamp` | string (date-time) | No |  | This contains the date and time of the latest logging information to include in the diagnostics. |
| `oldestTimestamp` | string (date-time) | No |  | This contains the date and time of the oldest logging information to include in the diagnostics. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetLog

---

### MonitoringDataType

Class to hold parameters of SetVariableMonitoring request.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.0.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.0.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `variableMonitoring` | [VariableMonitoringType](#variablemonitoringtype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyMonitoringReport

---

### SetMonitoringDataType

Class to hold parameters of SetVariableMonitoring request.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.0.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `severity` | integer | **Yes** |  | The severity that will be assigned to an event that is triggered by this monitor. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event. + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations. |
| `type` | [MonitorEnumType](../OCPP-2.0.1-DataTypes.md#monitorenumtype) | **Yes** |  |  |
| `value` | number | **Yes** |  | Value for threshold or delta monitoring. For Periodic or PeriodicClockAligned this is the interval in seconds. |
| `variable` | [VariableType](../OCPP-2.0.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `id` | integer | No |  | An id SHALL only be given to replace an existing monitor. The Charging Station handles the generation of id's for new monitors. |
| `transaction` | boolean | No |  | Monitor only active when a transaction is ongoing on a component relevant to this transaction. Default = false. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetVariableMonitoring

---

### SetMonitoringResultType

Class to hold result of SetVariableMonitoring request.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `component` | [ComponentType](../OCPP-2.0.1-DataTypes.md#componenttype) | **Yes** |  |  |
| `severity` | integer | **Yes** |  | The severity that will be assigned to an event that is triggered by this monitor. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event. + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations. |
| `status` | [SetMonitoringStatusEnumType](#setmonitoringstatusenumtype) | **Yes** |  |  |
| `type` | [MonitorEnumType](../OCPP-2.0.1-DataTypes.md#monitorenumtype) | **Yes** |  |  |
| `variable` | [VariableType](../OCPP-2.0.1-DataTypes.md#variabletype) | **Yes** |  |  |
| `id` | integer | No |  | Id given to the VariableMonitor by the Charging Station. The Id is only returned when status is accepted. Installed VariableMonitors should have unique id's but the id's of removed Installed monitors should have unique id's but the id's of removed monitors MAY be reused. |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SetVariableMonitoring

---

### VariableMonitoringType

A monitoring setting for a variable.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** |  | Identifies the monitor. |
| `severity` | integer | **Yes** |  | The severity that will be assigned to an event that is triggered by this monitor. The severity range is 0-9, with 0 as the highest and 9 as the lowest severity level. The severity levels have the following meaning: + *0-Danger* + Indicates lives are potentially in danger. Urgent attention is needed and action should be taken immediately. + *1-Hardware Failure* + Indicates that the Charging Station is unable to continue regular operations due to Hardware issues. Action is required. + *2-System Failure* + Indicates that the Charging Station is unable to continue regular operations due to software or minor hardware issues. Action is required. + *3-Critical* + Indicates a critical error. Action is required. + *4-Error* + Indicates a non-urgent error. Action is required. + *5-Alert* + Indicates an alert event. Default severity for any type of monitoring event. + *6-Warning* + Indicates a warning event. Action may be required. + *7-Notice* + Indicates an unusual event. No immediate action is required. + *8-Informational* + Indicates a regular operational event. May be used for reporting, measuring throughput, etc. No action is required. + *9-Debug* + Indicates information useful to developers for debugging, not useful during operations. |
| `transaction` | boolean | **Yes** |  | Monitor only active when a transaction is ongoing on a component relevant to this transaction. |
| `type` | [MonitorEnumType](../OCPP-2.0.1-DataTypes.md#monitorenumtype) | **Yes** |  |  |
| `value` | number | **Yes** |  | Value for threshold or delta monitoring. For Periodic or PeriodicClockAligned this is the interval in seconds. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyMonitoringReport

---
