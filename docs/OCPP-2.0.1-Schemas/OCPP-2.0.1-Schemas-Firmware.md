# OCPP 2.0.1 Schemas — Firmware

> **Functional Block:** I
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [UpdateFirmware](#updatefirmware) (CSMS → CS)
- [FirmwareStatusNotification](#firmwarestatusnotification) (CS → CSMS)
- [PublishFirmware](#publishfirmware) (CSMS → CS)
- [PublishFirmwareStatusNotification](#publishfirmwarestatusnotification) (CS → CSMS)
- [UnpublishFirmware](#unpublishfirmware) (CSMS → CS)

---

## UpdateFirmware

**Direction:** CSMS → CS

### UpdateFirmwareRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `firmware` | [FirmwareType](#firmwaretype) | **Yes** |  |  |
| `requestId` | integer | **Yes** |  | The Id of this request |
| `retries` | integer | No |  | This specifies how many times Charging Station must try to download the firmware before giving up. If this field is not present, it is left to Charging Station to decide how many times it wants to retry. |
| `retryInterval` | integer | No |  | The interval in seconds after which a retry may be attempted. If this field is not present, it is left to Charging Station to decide how long to wait between attempts. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example UpdateFirmwareRequest</summary>

```json
{
  "firmware": {
    "location": "string",
    "retrieveDateTime": "2024-01-15T10:30:00Z"
  },
  "requestId": 0
}
```

</details>

### UpdateFirmwareResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [UpdateFirmwareStatusEnumType](#updatefirmwarestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## FirmwareStatusNotification

**Direction:** CS → CSMS

### FirmwareStatusNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [FirmwareStatusEnumType](#firmwarestatusenumtype) | **Yes** |  |  |
| `requestId` | integer | No |  | The request id that was provided in the UpdateFirmwareRequest that started this firmware update. This field is mandatory, unless the message was triggered by a TriggerMessageRequest AND there is no firmware update ongoing. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example FirmwareStatusNotificationRequest</summary>

```json
{
  "status": "Downloaded"
}
```

</details>

### FirmwareStatusNotificationResponse

*No required fields. An empty `{}` is a valid response.*

---

## PublishFirmware

**Direction:** CSMS → CS

### PublishFirmwareRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `checksum` | string | **Yes** | maxLength: 32 | The MD5 checksum over the entire firmware file as a hexadecimal string of length 32. |
| `location` | string | **Yes** | maxLength: 512 | This contains a string containing a URI pointing to a location from which to retrieve the firmware. |
| `requestId` | integer | **Yes** |  | The Id of the request. |
| `retries` | integer | No |  | This specifies how many times Charging Station must try to download the firmware before giving up. If this field is not present, it is left to Charging Station to decide how many times it wants to retry. |
| `retryInterval` | integer | No |  | The interval in seconds after which a retry may be attempted. If this field is not present, it is left to Charging Station to decide how long to wait between attempts. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example PublishFirmwareRequest</summary>

```json
{
  "checksum": "string",
  "location": "string",
  "requestId": 0
}
```

</details>

### PublishFirmwareResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## PublishFirmwareStatusNotification

**Direction:** CS → CSMS

### PublishFirmwareStatusNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [PublishFirmwareStatusEnumType](#publishfirmwarestatusenumtype) | **Yes** |  |  |
| `location` | string[] | No | minItems: 1 | Required if status is Published. Can be multiple URI’s, if the Local Controller supports e.g. HTTP, HTTPS, and FTP. |
| `requestId` | integer | No |  | The request id that was provided in the PublishFirmwareRequest which triggered this action. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example PublishFirmwareStatusNotificationRequest</summary>

```json
{
  "status": "Idle"
}
```

</details>

### PublishFirmwareStatusNotificationResponse

*No required fields. An empty `{}` is a valid response.*

---

## UnpublishFirmware

**Direction:** CSMS → CS

### UnpublishFirmwareRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `checksum` | string | **Yes** | maxLength: 32 | The MD5 checksum over the entire firmware file as a hexadecimal string of length 32. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example UnpublishFirmwareRequest</summary>

```json
{
  "checksum": "string"
}
```

</details>

### UnpublishFirmwareResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [UnpublishFirmwareStatusEnumType](#unpublishfirmwarestatusenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### FirmwareStatusEnumType

This contains the progress status of the firmware installation.

| Value |
|-------|
| `Downloaded` |
| `DownloadFailed` |
| `Downloading` |
| `DownloadScheduled` |
| `DownloadPaused` |
| `Idle` |
| `InstallationFailed` |
| `Installing` |
| `Installed` |
| `InstallRebooting` |
| `InstallScheduled` |
| `InstallVerificationFailed` |
| `InvalidSignature` |
| `SignatureVerified` |

**Used in:** FirmwareStatusNotification

---

### PublishFirmwareStatusEnumType

This contains the progress status of the publishfirmware installation.

| Value |
|-------|
| `Idle` |
| `DownloadScheduled` |
| `Downloading` |
| `Downloaded` |
| `Published` |
| `DownloadFailed` |
| `DownloadPaused` |
| `InvalidChecksum` |
| `ChecksumVerified` |
| `PublishFailed` |

**Used in:** PublishFirmwareStatusNotification

---

### UnpublishFirmwareStatusEnumType

Indicates whether the Local Controller succeeded in unpublishing the firmware.

| Value |
|-------|
| `DownloadOngoing` |
| `NoFirmware` |
| `Unpublished` |

**Used in:** UnpublishFirmware

---

### UpdateFirmwareStatusEnumType

This field indicates whether the Charging Station was able to accept the request.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `AcceptedCanceled` |
| `InvalidCertificate` |
| `RevokedCertificate` |

**Used in:** UpdateFirmware

---

### FirmwareType

Represents a copy of the firmware that can be loaded/updated on the Charging Station.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `location` | string | **Yes** | maxLength: 512 | URI defining the origin of the firmware. |
| `retrieveDateTime` | string (date-time) | **Yes** |  | Date and time at which the firmware shall be retrieved. |
| `installDateTime` | string (date-time) | No |  | Date and time at which the firmware shall be installed. |
| `signature` | string | No | maxLength: 800 | Base64 encoded firmware signature. |
| `signingCertificate` | string | No | maxLength: 5500 | Certificate with which the firmware was signed. PEM encoded X.509 certificate. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** UpdateFirmware

---
