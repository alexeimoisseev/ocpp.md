# OCPP 1.6J Schemas — Reservation

> **Feature Profile:** Reservation
>
> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.
> Field names, types, required status, enum values, and constraints are
> extracted mechanically. No manual editing applied.

## Messages

- [ReserveNow](#reservenow) (CS → CP)
- [CancelReservation](#cancelreservation) (CS → CP)

---

## ReserveNow

**Direction:** CS → CP

Reserve a connector for a specific idTag.

### ReserveNow.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `expiryDate` | string (date-time) | **Yes** |  |  |
| `idTag` | string | **Yes** | maxLength: 20 |  |
| `reservationId` | integer | **Yes** |  |  |
| `parentIdTag` | string | No | maxLength: 20 |  |

<details>
<summary>Example ReserveNow.req</summary>

```json
{
  "connectorId": 0,
  "expiryDate": "2024-01-15T10:30:00Z",
  "idTag": "ABCDEF1234",
  "reservationId": 0
}
```

</details>

### ReserveNow.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Faulted`, `Occupied`, `Rejected`, `Unavailable` |

<details>
<summary>Example ReserveNow.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## CancelReservation

**Direction:** CS → CP

Cancel an existing reservation.

### CancelReservation.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `reservationId` | integer | **Yes** |  |  |

<details>
<summary>Example CancelReservation.req</summary>

```json
{
  "reservationId": 0
}
```

</details>

### CancelReservation.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected` |

<details>
<summary>Example CancelReservation.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---
