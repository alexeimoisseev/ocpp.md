# OCPP 2.0.1 Schemas — Availability

> **Functional Block:** E/F
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [ChangeAvailability](#changeavailability) (CSMS → CS)
- [UnlockConnector](#unlockconnector) (CSMS → CS)
- [TriggerMessage](#triggermessage) (CSMS → CS)

---

## ChangeAvailability

**Direction:** CSMS → CS

### ChangeAvailabilityRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `operationalStatus` | [OperationalStatusEnumType](#operationalstatusenumtype) | **Yes** |  |  |
| `evse` | [EVSEType](../OCPP-2.0.1-DataTypes.md#evsetype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ChangeAvailabilityRequest</summary>

```json
{
  "operationalStatus": "Inoperative"
}
```

</details>

### ChangeAvailabilityResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ChangeAvailabilityStatusEnumType](#changeavailabilitystatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## UnlockConnector

**Direction:** CSMS → CS

### UnlockConnectorRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  | This contains the identifier of the connector that needs to be unlocked. |
| `evseId` | integer | **Yes** |  | This contains the identifier of the EVSE for which a connector needs to be unlocked. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## TriggerMessage

**Direction:** CSMS → CS

### TriggerMessageRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestedMessage` | [MessageTriggerEnumType](#messagetriggerenumtype) | **Yes** |  |  |
| `evse` | [EVSEType](../OCPP-2.0.1-DataTypes.md#evsetype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### ChangeAvailabilityStatusEnumType

This indicates whether the Charging Station is able to perform the availability change.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Scheduled` |

**Used in:** ChangeAvailability

---

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
| `StatusNotification` |
| `TransactionEvent` |
| `SignCombinedCertificate` |
| `PublishFirmwareStatusNotification` |

**Used in:** TriggerMessage

---

### OperationalStatusEnumType

This contains the type of availability change that the Charging Station should perform.

| Value |
|-------|
| `Inoperative` |
| `Operative` |

**Used in:** ChangeAvailability

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
