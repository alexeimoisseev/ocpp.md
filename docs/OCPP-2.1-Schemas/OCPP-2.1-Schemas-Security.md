# OCPP 2.1 Schemas — Security

> **Functional Block:** A
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [SecurityEventNotification](#securityeventnotification) (CS → CSMS)

---

## SecurityEventNotification

**Direction:** CS → CSMS

### SecurityEventNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `timestamp` | string (date-time) | **Yes** |  | Date and time at which the event occurred. |
| `type` | string | **Yes** | maxLength: 50 | Type of the security event. This value should be taken from the Security events list. |
| `techInfo` | string | No | maxLength: 255 | Additional information about the occurred security event. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SecurityEventNotificationRequest</summary>

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "type": "string"
}
```

</details>

### SecurityEventNotificationResponse

*No required fields. An empty `{}` is a valid response.*

---
