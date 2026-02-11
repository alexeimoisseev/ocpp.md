# OCPP 1.6J Schemas — RemoteTrigger

> **Feature Profile:** RemoteTrigger
>
> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.
> Field names, types, required status, enum values, and constraints are
> extracted mechanically. No manual editing applied.

## Messages

- [TriggerMessage](#triggermessage) (CS → CP)

---

## TriggerMessage

**Direction:** CS → CP

Request the Charge Point to send a specific message now.

### TriggerMessage.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `requestedMessage` | string (enum) | **Yes** |  | Values: `BootNotification`, `DiagnosticsStatusNotification`, `FirmwareStatusNotification`, `Heartbeat`, `MeterValues`, `StatusNotification` |
| `connectorId` | integer | No |  |  |

<details>
<summary>Example TriggerMessage.req</summary>

```json
{
  "requestedMessage": "BootNotification"
}
```

</details>

### TriggerMessage.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Rejected`, `NotImplemented` |

<details>
<summary>Example TriggerMessage.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---
