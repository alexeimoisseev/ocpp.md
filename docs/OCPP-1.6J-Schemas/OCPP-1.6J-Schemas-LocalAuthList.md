# OCPP 1.6J Schemas — LocalAuthList

> **Feature Profile:** LocalAuthList
>
> Generated from the official OCA JSON schemas for OCPP 1.6 edition 2.
> Field names, types, required status, enum values, and constraints are
> extracted mechanically. No manual editing applied.

## Messages

- [SendLocalList](#sendlocallist) (CS → CP)
- [GetLocalListVersion](#getlocallistversion) (CS → CP)

---

## SendLocalList

**Direction:** CS → CP

Push a local authorization list to the Charge Point.

### SendLocalList.req

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `listVersion` | integer | **Yes** |  |  |
| `updateType` | string (enum) | **Yes** |  | Values: `Differential`, `Full` |
| `localAuthorizationList` | object[] | No |  |  |

**`localAuthorizationList[]` items:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTag` | string | **Yes** | maxLength: 20 |  |
| `idTagInfo` | object | No |  |  |

**`idTagInfo` object:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Blocked`, `Expired`, `Invalid`, `ConcurrentTx` |
| `expiryDate` | string (date-time) | No |  |  |
| `parentIdTag` | string | No | maxLength: 20 |  |

<details>
<summary>Example SendLocalList.req</summary>

```json
{
  "listVersion": 0,
  "updateType": "Differential"
}
```

</details>

### SendLocalList.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | string (enum) | **Yes** |  | Values: `Accepted`, `Failed`, `NotSupported`, `VersionMismatch` |

<details>
<summary>Example SendLocalList.conf</summary>

```json
{
  "status": "Accepted"
}
```

</details>

---

## GetLocalListVersion

**Direction:** CS → CP

Query the version of the local authorization list.

### GetLocalListVersion.req

*No fields (empty object `{}`).*

<details>
<summary>Example GetLocalListVersion.req</summary>

```json
{}
```

</details>

### GetLocalListVersion.conf

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `listVersion` | integer | **Yes** |  |  |

<details>
<summary>Example GetLocalListVersion.conf</summary>

```json
{
  "listVersion": 0
}
```

</details>

---
