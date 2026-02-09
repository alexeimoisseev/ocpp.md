# OCPP 2.0.1 Schemas — Display

> **Functional Block:** L
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [SetDisplayMessage](#setdisplaymessage) (CSMS → CS)
- [GetDisplayMessages](#getdisplaymessages) (CSMS → CS)
- [ClearDisplayMessage](#cleardisplaymessage) (CSMS → CS)
- [NotifyDisplayMessages](#notifydisplaymessages) (CS → CSMS)
- [CostUpdated](#costupdated) (CSMS → CS)

---

## SetDisplayMessage

**Direction:** CSMS → CS

### SetDisplayMessageRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `message` | [MessageInfoType](#messageinfotype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetDisplayMessageRequest</summary>

```json
{
  "message": {
    "id": 0,
    "priority": "AlwaysFront",
    "message": {
      "format": "ASCII",
      "content": "string"
    }
  }
}
```

</details>

### SetDisplayMessageResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [DisplayMessageStatusEnumType](#displaymessagestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetDisplayMessages

**Direction:** CSMS → CS

### GetDisplayMessagesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestId` | integer | **Yes** |  | The Id of this request. |
| `id` | integer[] | No | minItems: 1 | If provided the Charging Station shall return Display Messages of the given ids. This field SHALL NOT contain more ids than set in NumberOfDisplayMessages.maxLimit |
| `priority` | [MessagePriorityEnumType](../OCPP-2.0.1-DataTypes.md#messagepriorityenumtype) | No |  |  |
| `state` | [MessageStateEnumType](../OCPP-2.0.1-DataTypes.md#messagestateenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetDisplayMessagesRequest</summary>

```json
{
  "requestId": 0
}
```

</details>

### GetDisplayMessagesResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GetDisplayMessagesStatusEnumType](#getdisplaymessagesstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearDisplayMessage

**Direction:** CSMS → CS

### ClearDisplayMessageRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** |  | Id of the message that SHALL be removed from the Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ClearDisplayMessageRequest</summary>

```json
{
  "id": 0
}
```

</details>

### ClearDisplayMessageResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ClearMessageStatusEnumType](#clearmessagestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifyDisplayMessages

**Direction:** CS → CSMS

### NotifyDisplayMessagesRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestId` | integer | **Yes** |  | The id of the GetDisplayMessagesRequest that requested this message. |
| `messageInfo` | [MessageInfoType](#messageinfotype)[] | No | minItems: 1 |  |
| `tbc` | boolean | No |  | "to be continued" indicator. Indicates whether another part of the report follows in an upcoming NotifyDisplayMessagesRequest message. Default value when omitted is false. Default: `False` |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyDisplayMessagesRequest</summary>

```json
{
  "requestId": 0
}
```

</details>

### NotifyDisplayMessagesResponse

*No required fields. An empty `{}` is a valid response.*

---

## CostUpdated

**Direction:** CSMS → CS

### CostUpdatedRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `totalCost` | number | **Yes** |  | Current total cost, based on the information known by the CSMS, of the transaction including taxes. In the currency configured with the configuration Variable: [Currency] |
| `transactionId` | string | **Yes** | maxLength: 36 | Transaction Id of the transaction the current cost are asked for. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example CostUpdatedRequest</summary>

```json
{
  "totalCost": 0.0,
  "transactionId": "string"
}
```

</details>

### CostUpdatedResponse

*No required fields. An empty `{}` is a valid response.*

---

## Local Types

*Types used only within this block's messages.*

### ClearMessageStatusEnumType

Returns whether the Charging Station has been able to remove the message.

| Value |
|-------|
| `Accepted` |
| `Unknown` |

**Used in:** ClearDisplayMessage

---

### DisplayMessageStatusEnumType

This indicates whether the Charging Station is able to display the message.

| Value |
|-------|
| `Accepted` |
| `NotSupportedMessageFormat` |
| `Rejected` |
| `NotSupportedPriority` |
| `NotSupportedState` |
| `UnknownTransaction` |

**Used in:** SetDisplayMessage

---

### GetDisplayMessagesStatusEnumType

Indicates if the Charging Station has Display Messages that match the request criteria in the GetDisplayMessagesRequest

| Value |
|-------|
| `Accepted` |
| `Unknown` |

**Used in:** GetDisplayMessages

---

### MessageInfoType

Contains message details, for a message to be displayed on a Charging Station.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | integer | **Yes** |  | Master resource identifier, unique within an exchange context. It is defined within the OCPP context as a positive Integer value (greater or equal to zero). |
| `message` | [MessageContentType](../OCPP-2.0.1-DataTypes.md#messagecontenttype) | **Yes** |  |  |
| `priority` | [MessagePriorityEnumType](../OCPP-2.0.1-DataTypes.md#messagepriorityenumtype) | **Yes** |  |  |
| `display` | [ComponentType](../OCPP-2.0.1-DataTypes.md#componenttype) | No |  |  |
| `endDateTime` | string (date-time) | No |  | Until what date-time should this message be shown, after this date/time this message SHALL be removed. |
| `startDateTime` | string (date-time) | No |  | From what date-time should this message be shown. If omitted: directly. |
| `state` | [MessageStateEnumType](../OCPP-2.0.1-DataTypes.md#messagestateenumtype) | No |  |  |
| `transactionId` | string | No | maxLength: 36 | ended. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifyDisplayMessages, SetDisplayMessage

---
