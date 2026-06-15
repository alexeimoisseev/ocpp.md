# OCPP 2.1 Schemas — BatterySwap

> **Functional Block:** S
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [BatterySwap](#batteryswap) (CS → CSMS)
- [RequestBatterySwap](#requestbatteryswap) (CSMS → CS)

---

## BatterySwap

**Direction:** CS → CSMS

### BatterySwapRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `batteryData` | [BatteryDataType](#batterydatatype)[] | **Yes** | minItems: 1 |  |
| `eventType` | [BatterySwapEventEnumType](#batteryswapeventenumtype) | **Yes** |  |  |
| `idToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | RequestId to correlate BatteryIn/Out events and optional RequestBatterySwapRequest. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example BatterySwapRequest</summary>

```json
{
  "batteryData": [
    {
      "evseId": 0,
      "serialNumber": "string",
      "soC": 0.0,
      "soH": 0.0
    }
  ],
  "eventType": "BatteryIn",
  "idToken": {
    "idToken": "string",
    "type": "string"
  },
  "requestId": 0
}
```

</details>

### BatterySwapResponse

*No required fields. An empty `{}` is a valid response.*

---

## RequestBatterySwap

**Direction:** CSMS → CS

### RequestBatterySwapRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | Request id to match with BatterySwapRequest. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example RequestBatterySwapRequest</summary>

```json
{
  "idToken": {
    "idToken": "string",
    "type": "string"
  },
  "requestId": 0
}
```

</details>

### RequestBatterySwapResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### BatterySwapEventEnumType

Battery in/out

| Value |
|-------|
| `BatteryIn` |
| `BatteryOut` |
| `BatteryOutTimeout` |

**Used in:** BatterySwap

---

### BatteryDataType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | **Yes** | min: 0.0 | Slot number where battery is inserted or removed. |
| `serialNumber` | string | **Yes** | maxLength: 50 | Serial number of battery. |
| `soC` | number | **Yes** | min: 0.0, max: 100.0 | State of charge |
| `soH` | number | **Yes** | min: 0.0, max: 100.0 | State of health |
| `productionDate` | string (date-time) | No |  | Production date of battery. |
| `vendorInfo` | string | No | maxLength: 500 | Vendor-specific info from battery in undefined format. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** BatterySwap

---
