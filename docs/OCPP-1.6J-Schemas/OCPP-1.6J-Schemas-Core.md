# OCPP 1.6J Schemas — Core

> **Feature Profile:** Core
>
> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.
> Field names, types, required status, enum values, and constraints are
> extracted mechanically. No manual editing applied.

## Messages

- [Authorize](#authorize) (CP → CS)
- [BootNotification](#bootnotification) (CP → CS)
- [ChangeAvailability](#changeavailability) (CS → CP)
- [ChangeConfiguration](#changeconfiguration) (CS → CP)
- [ClearCache](#clearcache) (CS → CP)
- [DataTransfer](#datatransfer) (CP ↔ CS)
- [GetConfiguration](#getconfiguration) (CS → CP)
- [Heartbeat](#heartbeat) (CP → CS)
- [MeterValues](#metervalues) (CP → CS)
- [RemoteStartTransaction](#remotestarttransaction) (CS → CP)
- [RemoteStopTransaction](#remotestoptransaction) (CS → CP)
- [Reset](#reset) (CS → CP)
- [StartTransaction](#starttransaction) (CP → CS)
- [StatusNotification](#statusnotification) (CP → CS)
- [StopTransaction](#stoptransaction) (CP → CS)
- [UnlockConnector](#unlockconnector) (CS → CP)

---

## Authorize

**Direction:** CP → CS

Validate an idTag before or during a transaction.

### Authorize.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTag` | string | **Yes** | maxLength: 20 |  |

<details>
<summary>Example Authorize.req</summary>

```json
{
  "idTag": "ABCDEF1234"
}
```

</details>

### Authorize.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTagInfo` | object | **Yes** |  |  |

**`idTagInfo` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Blocked`, `Expired`, `Invalid`, `ConcurrentTx` |
| `expiryDate` | string (date-time) | No |  |  |
| `parentIdTag` | string | No | maxLength: 20 |  |

<details>
<summary>Example Authorize.conf</summary>

```json
{
  "idTagInfo": {
    "status": "Accepted"
  }
}
```

</details>

---

## BootNotification

**Direction:** CP → CS

Charge Point registers with the Central System after (re)boot.

### BootNotification.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `chargePointModel` | string | **Yes** | maxLength: 20 |  |
| `chargePointVendor` | string | **Yes** | maxLength: 20 |  |
| `chargeBoxSerialNumber` | string | No | maxLength: 25 |  |
| `chargePointSerialNumber` | string | No | maxLength: 25 |  |
| `firmwareVersion` | string | No | maxLength: 50 |  |
| `iccid` | string | No | maxLength: 20 |  |
| `imsi` | string | No | maxLength: 20 |  |
| `meterSerialNumber` | string | No | maxLength: 25 |  |
| `meterType` | string | No | maxLength: 25 |  |

<details>
<summary>Example BootNotification.req</summary>

```json
{
  "chargePointModel": "ABCDEF1234",
  "chargePointVendor": "ABCDEF1234"
}
```

</details>

### BootNotification.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currentTime` | string (date-time) | **Yes** |  |  |
| `interval` | integer | **Yes** |  |  |
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Pending`, `Rejected` |

<details>
<summary>Example BootNotification.conf</summary>

```json
{
  "currentTime": "2024-01-15T10:30:00Z",
  "interval": 0,
  "status": "Accepted"
}
```

</details>

---

## ChangeAvailability

**Direction:** CS → CP

Change a connector or the entire Charge Point to operative/inoperative.

### ChangeAvailability.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `type` | string (enum) | **Yes** |  | Values: `Inoperative`, `Operative` |

<details>
<summary>Example ChangeAvailability.req</summary>

```json
{
  "connectorId": 0,
  "type": "Inoperative"
}
```

</details>

### ChangeAvailability.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected`, `Scheduled` |

<details>
<summary>Example ChangeAvailability.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## ChangeConfiguration

**Direction:** CS → CP

Set a configuration key on the Charge Point.

### ChangeConfiguration.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `key` | string | **Yes** | maxLength: 50 |  |
| `value` | string | **Yes** | maxLength: 500 |  |

<details>
<summary>Example ChangeConfiguration.req</summary>

```json
{
  "key": "string",
  "value": "string"
}
```

</details>

### ChangeConfiguration.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected`, `RebootRequired`, `NotSupported` |

<details>
<summary>Example ChangeConfiguration.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## ClearCache

**Direction:** CS → CP

Clear the Charge Point's authorization cache.

### ClearCache.req

*No fields (empty object `{}`).*

<details>
<summary>Example ClearCache.req</summary>

```json
{}
```

</details>

### ClearCache.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected` |

<details>
<summary>Example ClearCache.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## DataTransfer

**Direction:** CP ↔ CS

Vendor-specific data exchange (bidirectional).

### DataTransfer.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `vendorId` | string | **Yes** | maxLength: 255 |  |
| `data` | string | No |  |  |
| `messageId` | string | No | maxLength: 50 |  |

<details>
<summary>Example DataTransfer.req</summary>

```json
{
  "vendorId": "string"
}
```

</details>

### DataTransfer.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected`, `UnknownMessageId`, `UnknownVendorId` |
| `data` | string | No |  |  |

<details>
<summary>Example DataTransfer.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## GetConfiguration

**Direction:** CS → CP

Read one or more configuration keys from the Charge Point.

### GetConfiguration.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `key` | string[] | No |  |  |

<details>
<summary>Example GetConfiguration.req</summary>

```json
{}
```

</details>

### GetConfiguration.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `configurationKey` | object[] | No |  |  |

**`configurationKey[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `key` | string | **Yes** | maxLength: 50 |  |
| `readonly` | boolean | **Yes** |  |  |
| `value` | string | No | maxLength: 500 |  |
| `unknownKey` | string[] | No |  |  |

<details>
<summary>Example GetConfiguration.conf</summary>

```json
{}
```

</details>

---

## Heartbeat

**Direction:** CP → CS

Keepalive — Charge Point signals it is still connected.

### Heartbeat.req

*No fields (empty object `{}`).*

<details>
<summary>Example Heartbeat.req</summary>

```json
{}
```

</details>

### Heartbeat.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `currentTime` | string (date-time) | **Yes** |  |  |

<details>
<summary>Example Heartbeat.conf</summary>

```json
{
  "currentTime": "2024-01-15T10:30:00Z"
}
```

</details>

---

## MeterValues

**Direction:** CP → CS

Send periodic or clock-aligned meter readings.

### MeterValues.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `meterValue` | object[] | **Yes** |  |  |

**`meterValue[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `sampledValue` | object[] | **Yes** |  |  |

**`sampledValue[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `value` | string | **Yes** |  |  |
| `context` | string (enum) | No |  | Values: `Interruption.Begin`, `Interruption.End`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`, `Other` |
| `format` | string (enum) | No |  | Values: `Raw`, `SignedData` |
| `location` | string (enum) | No |  | Values: `Cable`, `EV`, `Inlet`, `Outlet`, `Body` |
| `measurand` | string (enum) | No |  | Values: `Energy.Active.Export.Register`, `Energy.Active.Import.Register`, `Energy.Reactive.Export.Register`, `Energy.Reactive.Import.Register`, `Energy.Active.Export.Interval`, `Energy.Active.Import.Interval`, `Energy.Reactive.Export.Interval`, `Energy.Reactive.Import.Interval`, `Power.Active.Export`, `Power.Active.Import`, `Power.Offered`, `Power.Reactive.Export`, `Power.Reactive.Import`, `Power.Factor`, `Current.Import`, `Current.Export`, `Current.Offered`, `Voltage`, `Frequency`, `Temperature`, `SoC`, `RPM` |
| `phase` | string (enum) | No |  | Values: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1` |
| `unit` | string (enum) | No |  | Values: `Wh`, `kWh`, `varh`, `kvarh`, `W`, `kW`, `VA`, `kVA`, `var`, `kvar`, `A`, `V`, `K`, `Celcius`, `Celsius`, `Fahrenheit`, `Percent` |
| `timestamp` | string (date-time) | **Yes** |  |  |
| `transactionId` | integer | No |  |  |

<details>
<summary>Example MeterValues.req</summary>

```json
{
  "connectorId": 0,
  "meterValue": [
    {
      "sampledValue": [
        {
          "value": "string"
        }
      ],
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

</details>

### MeterValues.conf

*No fields (empty object `{}`).*

<details>
<summary>Example MeterValues.conf</summary>

```json
{}
```

</details>

---

## RemoteStartTransaction

**Direction:** CS → CP

Central System requests the Charge Point to start a transaction.

### RemoteStartTransaction.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTag` | string | **Yes** | maxLength: 20 |  |
| `chargingProfile` | object | No |  |  |

**`chargingProfile` object:**

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
| `connectorId` | integer | No |  |  |

<details>
<summary>Example RemoteStartTransaction.req</summary>

```json
{
  "idTag": "ABCDEF1234"
}
```

</details>

### RemoteStartTransaction.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected` |

<details>
<summary>Example RemoteStartTransaction.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## RemoteStopTransaction

**Direction:** CS → CP

Central System requests the Charge Point to stop a transaction.

### RemoteStopTransaction.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `transactionId` | integer | **Yes** |  |  |

<details>
<summary>Example RemoteStopTransaction.req</summary>

```json
{
  "transactionId": 0
}
```

</details>

### RemoteStopTransaction.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected` |

<details>
<summary>Example RemoteStopTransaction.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## Reset

**Direction:** CS → CP

Reboot the Charge Point (Hard or Soft).

### Reset.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `type` | string (enum) | **Yes** |  | Values: `Hard`, `Soft` |

<details>
<summary>Example Reset.req</summary>

```json
{
  "type": "Hard"
}
```

</details>

### Reset.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected` |

<details>
<summary>Example Reset.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## StartTransaction

**Direction:** CP → CS

Charge Point reports that a transaction has started.

### StartTransaction.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `idTag` | string | **Yes** | maxLength: 20 |  |
| `meterStart` | integer | **Yes** |  |  |
| `timestamp` | string (date-time) | **Yes** |  |  |
| `reservationId` | integer | No |  |  |

<details>
<summary>Example StartTransaction.req</summary>

```json
{
  "connectorId": 0,
  "idTag": "ABCDEF1234",
  "meterStart": 0,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

</details>

### StartTransaction.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTagInfo` | object | **Yes** |  |  |

**`idTagInfo` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Blocked`, `Expired`, `Invalid`, `ConcurrentTx` |
| `expiryDate` | string (date-time) | No |  |  |
| `parentIdTag` | string | No | maxLength: 20 |  |
| `transactionId` | integer | **Yes** |  |  |

<details>
<summary>Example StartTransaction.conf</summary>

```json
{
  "idTagInfo": {
    "status": "Accepted"
  },
  "transactionId": 0
}
```

</details>

---

## StatusNotification

**Direction:** CP → CS

Charge Point reports a connector status or error change.

### StatusNotification.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |
| `errorCode` | string (enum) | **Yes** |  | Values: `ConnectorLockFailure`, `EVCommunicationError`, `GroundFailure`, `HighTemperature`, `InternalError`, `LocalListConflict`, `NoError`, `OtherError`, `OverCurrentFailure`, `PowerMeterFailure`, `PowerSwitchFailure`, `ReaderFailure`, `ResetFailure`, `UnderVoltage`, `OverVoltage`, `WeakSignal` |
| `status` | string (enum) | **Yes** |  | Values: `Available`, `Preparing`, `Charging`, `SuspendedEVSE`, `SuspendedEV`, `Finishing`, `Reserved`, `Unavailable`, `Faulted` |
| `info` | string | No | maxLength: 50 |  |
| `timestamp` | string (date-time) | No |  |  |
| `vendorErrorCode` | string | No | maxLength: 50 |  |
| `vendorId` | string | No | maxLength: 255 |  |

<details>
<summary>Example StatusNotification.req</summary>

```json
{
  "connectorId": 0,
  "errorCode": "ConnectorLockFailure",
  "status": "Available"
}
```

</details>

### StatusNotification.conf

*No fields (empty object `{}`).*

<details>
<summary>Example StatusNotification.conf</summary>

```json
{}
```

</details>

---

## StopTransaction

**Direction:** CP → CS

Charge Point reports that a transaction has ended.

### StopTransaction.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `meterStop` | integer | **Yes** |  |  |
| `timestamp` | string (date-time) | **Yes** |  |  |
| `transactionId` | integer | **Yes** |  |  |
| `idTag` | string | No | maxLength: 20 |  |
| `reason` | string (enum) | No |  | Values: `EmergencyStop`, `EVDisconnected`, `HardReset`, `Local`, `Other`, `PowerLoss`, `Reboot`, `Remote`, `SoftReset`, `UnlockCommand`, `DeAuthorized` |
| `transactionData` | object[] | No |  |  |

**`transactionData[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `sampledValue` | object[] | **Yes** |  |  |

**`sampledValue[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `value` | string | **Yes** |  |  |
| `context` | string (enum) | No |  | Values: `Interruption.Begin`, `Interruption.End`, `Sample.Clock`, `Sample.Periodic`, `Transaction.Begin`, `Transaction.End`, `Trigger`, `Other` |
| `format` | string (enum) | No |  | Values: `Raw`, `SignedData` |
| `location` | string (enum) | No |  | Values: `Cable`, `EV`, `Inlet`, `Outlet`, `Body` |
| `measurand` | string (enum) | No |  | Values: `Energy.Active.Export.Register`, `Energy.Active.Import.Register`, `Energy.Reactive.Export.Register`, `Energy.Reactive.Import.Register`, `Energy.Active.Export.Interval`, `Energy.Active.Import.Interval`, `Energy.Reactive.Export.Interval`, `Energy.Reactive.Import.Interval`, `Power.Active.Export`, `Power.Active.Import`, `Power.Offered`, `Power.Reactive.Export`, `Power.Reactive.Import`, `Power.Factor`, `Current.Import`, `Current.Export`, `Current.Offered`, `Voltage`, `Frequency`, `Temperature`, `SoC`, `RPM` |
| `phase` | string (enum) | No |  | Values: `L1`, `L2`, `L3`, `N`, `L1-N`, `L2-N`, `L3-N`, `L1-L2`, `L2-L3`, `L3-L1` |
| `unit` | string (enum) | No |  | Values: `Wh`, `kWh`, `varh`, `kvarh`, `W`, `kW`, `VA`, `kVA`, `var`, `kvar`, `A`, `V`, `K`, `Celcius`, `Celsius`, `Fahrenheit`, `Percent` |
| `timestamp` | string (date-time) | **Yes** |  |  |

<details>
<summary>Example StopTransaction.req</summary>

```json
{
  "meterStop": 0,
  "timestamp": "2024-01-15T10:30:00Z",
  "transactionId": 0
}
```

</details>

### StopTransaction.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTagInfo` | object | No |  |  |

**`idTagInfo` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Blocked`, `Expired`, `Invalid`, `ConcurrentTx` |
| `expiryDate` | string (date-time) | No |  |  |
| `parentIdTag` | string | No | maxLength: 20 |  |

<details>
<summary>Example StopTransaction.conf</summary>

```json
{}
```

</details>

---

## UnlockConnector

**Direction:** CS → CP

Remotely unlock a connector (for cable removal).

### UnlockConnector.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `connectorId` | integer | **Yes** |  |  |

<details>
<summary>Example UnlockConnector.req</summary>

```json
{
  "connectorId": 0
}
```

</details>

### UnlockConnector.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Unlocked`, `UnlockFailed`, `NotSupported` |

<details>
<summary>Example UnlockConnector.conf</summary>

```json
{
  "status": "Unlocked"
}
```

</details>

---
