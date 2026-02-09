# OCPP 2.0.1 Schemas — Reservation

> **Functional Block:** N
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [ReserveNow](#reservenow) (CSMS → CS)
- [CancelReservation](#cancelreservation) (CSMS → CS)
- [ReservationStatusUpdate](#reservationstatusupdate) (CS → CSMS)

---

## ReserveNow

**Direction:** CSMS → CS

### ReserveNowRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `expiryDateTime` | string (date-time) | **Yes** |  | Date and time at which the reservation expires. |
| `id` | integer | **Yes** |  | Id of reservation. |
| `idToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `connectorType` | [ConnectorEnumType](#connectorenumtype) | No |  |  |
| `evseId` | integer | No |  | This contains ID of the evse to be reserved. |
| `groupIdToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ReserveNowRequest</summary>

```json
{
  "expiryDateTime": "2024-01-15T10:30:00Z",
  "id": 0,
  "idToken": {
    "idToken": "string",
    "type": "Central"
  }
}
```

</details>

### ReserveNowResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ReserveNowStatusEnumType](#reservenowstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## CancelReservation

**Direction:** CSMS → CS

### CancelReservationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `reservationId` | integer | **Yes** |  | Id of the reservation to cancel. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example CancelReservationRequest</summary>

```json
{
  "reservationId": 0
}
```

</details>

### CancelReservationResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [CancelReservationStatusEnumType](#cancelreservationstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ReservationStatusUpdate

**Direction:** CS → CSMS

### ReservationStatusUpdateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `reservationId` | integer | **Yes** |  | The ID of the reservation. |
| `reservationUpdateStatus` | [ReservationUpdateStatusEnumType](#reservationupdatestatusenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ReservationStatusUpdateRequest</summary>

```json
{
  "reservationId": 0,
  "reservationUpdateStatus": "Expired"
}
```

</details>

### ReservationStatusUpdateResponse

*No required fields. An empty `{}` is a valid response.*

---

## Local Types

*Types used only within this block's messages.*

### CancelReservationStatusEnumType

This indicates the success or failure of the canceling of a reservation by CSMS.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** CancelReservation

---

### ConnectorEnumType

This field specifies the connector type.

| Value |
|-------|
| `cCCS1` |
| `cCCS2` |
| `cG105` |
| `cTesla` |
| `cType1` |
| `cType2` |
| `s309-1P-16A` |
| `s309-1P-32A` |
| `s309-3P-16A` |
| `s309-3P-32A` |
| `sBS1361` |
| `sCEE-7-7` |
| `sType2` |
| `sType3` |
| `Other1PhMax16A` |
| `Other1PhOver16A` |
| `Other3Ph` |
| `Pan` |
| `wInductive` |
| `wResonant` |
| `Undetermined` |
| `Unknown` |

**Used in:** ReserveNow

---

### ReservationUpdateStatusEnumType

The updated reservation status.

| Value |
|-------|
| `Expired` |
| `Removed` |

**Used in:** ReservationStatusUpdate

---

### ReserveNowStatusEnumType

This indicates the success or failure of the reservation.

| Value |
|-------|
| `Accepted` |
| `Faulted` |
| `Occupied` |
| `Rejected` |
| `Unavailable` |

**Used in:** ReserveNow

---
