# OCPP 2.1 Schemas — Availability

> **Functional Block:** G
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [ChangeAvailability](#changeavailability) (CSMS → CS)
- [StatusNotification](#statusnotification) (CS → CSMS)

---

## ChangeAvailability

**Direction:** CSMS → CS

### ChangeAvailabilityRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `operationalStatus` | [OperationalStatusEnumType](#operationalstatusenumtype) | **Yes** |  |  |
| `evse` | [EVSEType](../OCPP-2.1-DataTypes.md#evsetype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## StatusNotification

**Direction:** CS → CSMS

### StatusNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** | min: 0.0 | The id of the connector within the EVSE for which the status is reported. |
| `connectorStatus` | [ConnectorStatusEnumType](#connectorstatusenumtype) | **Yes** |  |  |
| `evseId` | integer | **Yes** | min: 0.0 | The id of the EVSE to which the connector belongs for which the the status is reported. |
| `timestamp` | string (date-time) | **Yes** |  | The time for which the status is reported. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example StatusNotificationRequest</summary>

```json
{
  "connectorId": 0,
  "connectorStatus": "Available",
  "evseId": 0,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

</details>

### StatusNotificationResponse

*No required fields. An empty `{}` is a valid response.*

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

### ConnectorStatusEnumType

This contains the current status of the Connector.

| Value |
|-------|
| `Available` |
| `Occupied` |
| `Reserved` |
| `Unavailable` |
| `Faulted` |

**Used in:** StatusNotification

---

### OperationalStatusEnumType

This contains the type of availability change that the Charging Station should perform.

| Value |
|-------|
| `Inoperative` |
| `Operative` |

**Used in:** ChangeAvailability

---
