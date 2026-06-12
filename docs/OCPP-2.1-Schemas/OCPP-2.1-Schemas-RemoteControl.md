# OCPP 2.1 Schemas — RemoteControl

> **Functional Block:** F
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [RequestStartTransaction](#requeststarttransaction) (CSMS → CS)
- [RequestStopTransaction](#requeststoptransaction) (CSMS → CS)
- [UnlockConnector](#unlockconnector) (CSMS → CS)
- [TriggerMessage](#triggermessage) (CSMS → CS)

---

## RequestStartTransaction

**Direction:** CSMS → CS

### RequestStartTransactionRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `remoteStartId` | integer | **Yes** |  | Id given by the server to this start request. The Charging Station will return this in the TransactionEventRequest, letting the server know which transaction was started for this request. Use to start a transaction. |
| `chargingProfile` | [ChargingProfileType](../OCPP-2.1-DataTypes.md#chargingprofiletype) | No |  |  |
| `evseId` | integer | No | min: 1.0 | Number of the EVSE on which to start the transaction. EvseId SHALL be > 0 |
| `groupIdToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example RequestStartTransactionRequest</summary>

```json
{
  "idToken": {
    "idToken": "string",
    "type": "string"
  },
  "remoteStartId": 0
}
```

</details>

### RequestStartTransactionResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [RequestStartStopStatusEnumType](#requeststartstopstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `transactionId` | string | No | maxLength: 36 | When the transaction was already started by the Charging Station before the RequestStartTransactionRequest was received, for example: cable plugged in first. This contains the transactionId of the already started transaction. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## RequestStopTransaction

**Direction:** CSMS → CS

### RequestStopTransactionRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | string | **Yes** | maxLength: 36 | The identifier of the transaction which the Charging Station is requested to stop. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## UnlockConnector

**Direction:** CSMS → CS

### UnlockConnectorRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** | min: 0.0 | This contains the identifier of the connector that needs to be unlocked. |
| `evseId` | integer | **Yes** | min: 0.0 | This contains the identifier of the EVSE for which a connector needs to be unlocked. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example UnlockConnectorRequest</summary>

```json
{
  "connectorId": 0,
  "evseId": 0
}
```

</details>

### UnlockConnectorResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [UnlockStatusEnumType](#unlockstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## TriggerMessage

**Direction:** CSMS → CS

### TriggerMessageRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestedMessage` | [MessageTriggerEnumType](#messagetriggerenumtype) | **Yes** |  |  |
| `customTrigger` | string | No | maxLength: 50 | *(2.1)* When _requestedMessage_ = CustomTrigger this will trigger sending the corresponding message in field _customTrigger_, if supported by Charging Station. |
| `evse` | [EVSEType](../OCPP-2.1-DataTypes.md#evsetype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example TriggerMessageRequest</summary>

```json
{
  "requestedMessage": "BootNotification"
}
```

</details>

### TriggerMessageResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [TriggerMessageStatusEnumType](#triggermessagestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### MessageTriggerEnumType

Type of message to be triggered.

| Value |
|-------|
| `BootNotification` |
| `LogStatusNotification` |
| `FirmwareStatusNotification` |
| `Heartbeat` |
| `MeterValues` |
| `SignChargingStationCertificate` |
| `SignV2GCertificate` |
| `SignV2G20Certificate` |
| `StatusNotification` |
| `TransactionEvent` |
| `SignCombinedCertificate` |
| `PublishFirmwareStatusNotification` |
| `CustomTrigger` |

**Used in:** TriggerMessage

---

### RequestStartStopStatusEnumType

Status indicating whether the Charging Station accepts the request to start a transaction.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** RequestStartTransaction, RequestStopTransaction

---

### TriggerMessageStatusEnumType

Indicates whether the Charging Station will send the requested notification or not.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NotImplemented` |

**Used in:** TriggerMessage

---

### UnlockStatusEnumType

This indicates whether the Charging Station has unlocked the connector.

| Value |
|-------|
| `Unlocked` |
| `UnlockFailed` |
| `OngoingAuthorizedTransaction` |
| `UnknownConnector` |

**Used in:** UnlockConnector

---
