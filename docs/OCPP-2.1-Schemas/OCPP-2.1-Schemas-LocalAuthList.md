# OCPP 2.1 Schemas — LocalAuthList

> **Functional Block:** D
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [SendLocalList](#sendlocallist) (CSMS → CS)
- [GetLocalListVersion](#getlocallistversion) (CSMS → CS)

---

## SendLocalList

**Direction:** CSMS → CS

### SendLocalListRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `updateType` | [UpdateEnumType](#updateenumtype) | **Yes** |  |  |
| `versionNumber` | integer | **Yes** |  | In case of a full update this is the version number of the full list. In case of a differential update it is the version number of the list after the update has been applied. |
| `localAuthorizationList` | [AuthorizationData](#authorizationdata)[] | No | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SendLocalListRequest</summary>

```json
{
  "updateType": "Differential",
  "versionNumber": 0
}
```

</details>

### SendLocalListResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [SendLocalListStatusEnumType](#sendlocalliststatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetLocalListVersion

**Direction:** CSMS → CS

### GetLocalListVersionRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### GetLocalListVersionResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `versionNumber` | integer | **Yes** |  | This contains the current version number of the local authorization list in the Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### SendLocalListStatusEnumType

This indicates whether the Charging Station has successfully received and applied the update of the Local Authorization List.

| Value |
|-------|
| `Accepted` |
| `Failed` |
| `VersionMismatch` |

**Used in:** SendLocalList

---

### UpdateEnumType

This contains the type of update (full or differential) of this request.

| Value |
|-------|
| `Differential` |
| `Full` |

**Used in:** SendLocalList

---

### AuthorizationData

Contains the identifier to use for authorization.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `idTokenInfo` | [IdTokenInfoType](../OCPP-2.1-DataTypes.md#idtokeninfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SendLocalList

---
