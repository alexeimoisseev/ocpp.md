# OCPP 1.6J Schemas — SmartCharging

> **Feature Profile:** SmartCharging
>
> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.
> Field names, types, required status, enum values, and constraints are
> extracted mechanically. No manual editing applied.

## Messages

- [SetChargingProfile](#setchargingprofile) (CS → CP)
- [ClearChargingProfile](#clearchargingprofile) (CS → CP)
- [GetCompositeSchedule](#getcompositeschedule) (CS → CP)

---

## SetChargingProfile

**Direction:** CS → CP

Install or update a charging profile on a connector.

### SetChargingProfile.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `csChargingProfiles` | object | **Yes** |  |  |

**`csChargingProfiles` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfileId` | integer | **Yes** |  |  |
| `chargingProfileKind` | string (enum) | **Yes** |  | Values: `Absolute`, `Recurring`, `Relative` |
| `chargingProfilePurpose` | string (enum) | **Yes** |  | Values: `ChargePointMaxProfile`, `TxDefaultProfile`, `TxProfile` |
| `chargingSchedule` | object | **Yes** |  |  |

**`chargingSchedule` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingRateUnit` | string (enum) | **Yes** |  | Values: `A`, `W` |
| `chargingSchedulePeriod` | object[] | **Yes** |  |  |

**`chargingSchedulePeriod[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `limit` | number | **Yes** | multipleOf: 0.1 |  |
| `startPeriod` | integer | **Yes** |  |  |
| `numberPhases` | integer | No |  |  |
| `duration` | integer | No |  |  |
| `minChargingRate` | number | No | multipleOf: 0.1 |  |
| `startSchedule` | string (date-time) | No |  |  |
| `stackLevel` | integer | **Yes** |  |  |
| `recurrencyKind` | string (enum) | No |  | Values: `Daily`, `Weekly` |
| `transactionId` | integer | No |  |  |
| `validFrom` | string (date-time) | No |  |  |
| `validTo` | string (date-time) | No |  |  |

<details>
<summary>Example SetChargingProfile.req</summary>

```json
{
  "connectorId": 0,
  "csChargingProfiles": {
    "chargingProfileId": 0,
    "chargingProfileKind": "Absolute",
    "chargingProfilePurpose": "ChargePointMaxProfile",
    "chargingSchedule": {
      "chargingRateUnit": "A",
      "chargingSchedulePeriod": [
        {
          "limit": 0.0,
          "startPeriod": 0
        }
      ]
    },
    "stackLevel": 0
  }
}
```

</details>

### SetChargingProfile.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected`, `NotSupported` |

<details>
<summary>Example SetChargingProfile.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## ClearChargingProfile

**Direction:** CS → CP

Remove one or more charging profiles.

### ClearChargingProfile.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingProfilePurpose` | string (enum) | No |  | Values: `ChargePointMaxProfile`, `TxDefaultProfile`, `TxProfile` |
| `connectorId` | integer | No |  |  |
| `id` | integer | No |  |  |
| `stackLevel` | integer | No |  |  |

<details>
<summary>Example ClearChargingProfile.req</summary>

```json
{}
```

</details>

### ClearChargingProfile.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Unknown` |

<details>
<summary>Example ClearChargingProfile.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## GetCompositeSchedule

**Direction:** CS → CP

Request the combined effective charging schedule.

### GetCompositeSchedule.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `duration` | integer | **Yes** |  |  |
| `chargingRateUnit` | string (enum) | No |  | Values: `A`, `W` |

<details>
<summary>Example GetCompositeSchedule.req</summary>

```json
{
  "connectorId": 0,
  "duration": 0
}
```

</details>

### GetCompositeSchedule.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected` |
| `chargingSchedule` | object | No |  |  |

**`chargingSchedule` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargingRateUnit` | string (enum) | **Yes** |  | Values: `A`, `W` |
| `chargingSchedulePeriod` | object[] | **Yes** |  |  |

**`chargingSchedulePeriod[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `limit` | number | **Yes** | multipleOf: 0.1 |  |
| `startPeriod` | integer | **Yes** |  |  |
| `numberPhases` | integer | No |  |  |
| `duration` | integer | No |  |  |
| `minChargingRate` | number | No | multipleOf: 0.1 |  |
| `startSchedule` | string (date-time) | No |  |  |
| `connectorId` | integer | No |  |  |
| `scheduleStart` | string (date-time) | No |  |  |

<details>
<summary>Example GetCompositeSchedule.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---
