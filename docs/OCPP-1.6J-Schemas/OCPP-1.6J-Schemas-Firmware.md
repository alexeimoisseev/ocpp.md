# OCPP 1.6J Schemas — Firmware

> **Feature Profile:** Firmware
>
> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.
> Field names, types, required status, enum values, and constraints are
> extracted mechanically. No manual editing applied.

## Messages

- [GetDiagnostics](#getdiagnostics) (CS → CP)
- [DiagnosticsStatusNotification](#diagnosticsstatusnotification) (CP → CS)
- [UpdateFirmware](#updatefirmware) (CS → CP)
- [FirmwareStatusNotification](#firmwarestatusnotification) (CP → CS)

---

## GetDiagnostics

**Direction:** CS → CP

Request the Charge Point to upload diagnostic logs.

### GetDiagnostics.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `location` | string (uri) | **Yes** |  |  |
| `retries` | integer | No |  |  |
| `retryInterval` | integer | No |  |  |
| `startTime` | string (date-time) | No |  |  |
| `stopTime` | string (date-time) | No |  |  |

<details>
<summary>Example GetDiagnostics.req</summary>

```json
{
  "location": "string"
}
```

</details>

### GetDiagnostics.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `fileName` | string | No | maxLength: 255 |  |

<details>
<summary>Example GetDiagnostics.conf</summary>

```json
{}
```

</details>

---

## DiagnosticsStatusNotification

**Direction:** CP → CS

Charge Point reports diagnostic upload progress.

### DiagnosticsStatusNotification.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Idle`, `Uploaded`, `UploadFailed`, `Uploading` |

<details>
<summary>Example DiagnosticsStatusNotification.req</summary>

```json
{
  "status": "Idle"
}
```

</details>

### DiagnosticsStatusNotification.conf

*No fields (empty object `{}`).*

<details>
<summary>Example DiagnosticsStatusNotification.conf</summary>

```json
{}
```

</details>

---

## UpdateFirmware

**Direction:** CS → CP

Request the Charge Point to download and install firmware.

### UpdateFirmware.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `location` | string (uri) | **Yes** |  |  |
| `retrieveDate` | string (date-time) | **Yes** |  |  |
| `retries` | integer | No |  |  |
| `retryInterval` | integer | No |  |  |

<details>
<summary>Example UpdateFirmware.req</summary>

```json
{
  "location": "string",
  "retrieveDate": "2024-01-15T10:30:00Z"
}
```

</details>

### UpdateFirmware.conf

*No fields (empty object `{}`).*

<details>
<summary>Example UpdateFirmware.conf</summary>

```json
{}
```

</details>

---

## FirmwareStatusNotification

**Direction:** CP → CS

Charge Point reports firmware update progress.

### FirmwareStatusNotification.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Downloaded`, `DownloadFailed`, `Downloading`, `Idle`, `InstallationFailed`, `Installing`, `Installed` |

<details>
<summary>Example FirmwareStatusNotification.req</summary>

```json
{
  "status": "Downloaded"
}
```

</details>

### FirmwareStatusNotification.conf

*No fields (empty object `{}`).*

<details>
<summary>Example FirmwareStatusNotification.conf</summary>

```json
{}
```

</details>

---
