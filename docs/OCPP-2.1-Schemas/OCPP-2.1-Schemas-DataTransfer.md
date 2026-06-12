# OCPP 2.1 Schemas — DataTransfer

> **Functional Block:** P
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [DataTransfer](#datatransfer) (Both)

---

## DataTransfer

**Direction:** Both

### DataTransferRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `vendorId` | string | **Yes** | maxLength: 255 | This identifies the Vendor specific implementation |
| `data` | any | No |  | Data without specified length or format. This needs to be decided by both parties (Open to implementation). |
| `messageId` | string | No | maxLength: 50 | May be used to indicate a specific message or implementation. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example DataTransferRequest</summary>

```json
{
  "vendorId": "string"
}
```

</details>

### DataTransferResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [DataTransferStatusEnumType](#datatransferstatusenumtype) | **Yes** |  |  |
| `data` | any | No |  | Data without specified length or format, in response to request. |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### DataTransferStatusEnumType

This indicates the success or failure of the data transfer.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `UnknownMessageId` |
| `UnknownVendorId` |

**Used in:** DataTransfer

---
