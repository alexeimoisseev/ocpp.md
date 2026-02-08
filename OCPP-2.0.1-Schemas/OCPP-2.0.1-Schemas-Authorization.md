# OCPP 2.0.1 Schemas — Authorization

> **Functional Block:** C
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [Authorize](#authorize) (CS → CSMS)
- [SendLocalList](#sendlocallist) (CSMS → CS)
- [GetLocalListVersion](#getlocallistversion) (CSMS → CS)
- [ClearCache](#clearcache) (CSMS → CS)

---

## Authorize

**Direction:** CS → CSMS

### AuthorizeRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `certificate` | string | No | maxLength: 5500 | The X.509 certificated presented by EV and encoded in PEM format. |
| `iso15118CertificateHashData` | [OCSPRequestDataType](#ocsprequestdatatype)[] | No | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example AuthorizeRequest</summary>

```json
{
  "idToken": {
    "idToken": "string",
    "type": "Central"
  }
}
```

</details>

### AuthorizeResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTokenInfo` | [IdTokenInfoType](../OCPP-2.0.1-DataTypes.md#idtokeninfotype) | **Yes** |  |  |
| `certificateStatus` | [AuthorizeCertificateStatusEnumType](#authorizecertificatestatusenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## SendLocalList

**Direction:** CSMS → CS

### SendLocalListRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `updateType` | [UpdateEnumType](#updateenumtype) | **Yes** |  |  |
| `versionNumber` | integer | **Yes** |  | In case of a full update this is the version number of the full list. In case of a differential update it is the version number of the list after the update has been applied. |
| `localAuthorizationList` | [AuthorizationData](#authorizationdata)[] | No | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetLocalListVersion

**Direction:** CSMS → CS

### GetLocalListVersionRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


### GetLocalListVersionResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `versionNumber` | integer | **Yes** |  | This contains the current version number of the local authorization list in the Charging Station. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearCache

**Direction:** CSMS → CS

### ClearCacheRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


### ClearCacheResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ClearCacheStatusEnumType](#clearcachestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### AuthorizeCertificateStatusEnumType

Certificate status information. - if all certificates are valid: return 'Accepted'. - if one of the certificates was revoked, return 'CertificateRevoked'.

| Value |
|-------|
| `Accepted` |
| `SignatureError` |
| `CertificateExpired` |
| `CertificateRevoked` |
| `NoCertificateAvailable` |
| `CertChainError` |
| `ContractCancelled` |

**Used in:** Authorize

---

### ClearCacheStatusEnumType

Accepted if the Charging Station has executed the request, otherwise rejected.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** ClearCache

---

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
| `idToken` | [IdTokenType](../OCPP-2.0.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `idTokenInfo` | [IdTokenInfoType](../OCPP-2.0.1-DataTypes.md#idtokeninfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** SendLocalList

---

### OCSPRequestDataType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `hashAlgorithm` | [HashAlgorithmEnumType](../OCPP-2.0.1-DataTypes.md#hashalgorithmenumtype) | **Yes** |  |  |
| `issuerKeyHash` | string | **Yes** | maxLength: 128 | Hashed value of the issuers public key |
| `issuerNameHash` | string | **Yes** | maxLength: 128 | Hashed value of the Issuer DN (Distinguished Name). |
| `responderURL` | string | **Yes** | maxLength: 512 | This contains the responder URL (Case insensitive). |
| `serialNumber` | string | **Yes** | maxLength: 40 | The serial number of the certificate. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** Authorize, GetCertificateStatus

---
