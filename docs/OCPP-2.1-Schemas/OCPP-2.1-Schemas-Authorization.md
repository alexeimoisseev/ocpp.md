# OCPP 2.1 Schemas — Authorization

> **Functional Block:** C
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [Authorize](#authorize) (CS → CSMS)
- [ClearCache](#clearcache) (CSMS → CS)

---

## Authorize

**Direction:** CS → CSMS

### AuthorizeRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idToken` | [IdTokenType](../OCPP-2.1-DataTypes.md#idtokentype) | **Yes** |  |  |
| `certificate` | string | No | maxLength: 10000 | *(2.1)* The X.509 certificate chain presented by EV and encoded in PEM format. Order of certificates in chain is from leaf up to (but excluding) root certificate. + Only needed in case of central contract validation when Charging Station cannot validate the contract certificate. |
| `iso15118CertificateHashData` | [OCSPRequestDataType](#ocsprequestdatatype)[] | No | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example AuthorizeRequest</summary>

```json
{
  "idToken": {
    "idToken": "string",
    "type": "string"
  }
}
```

</details>

### AuthorizeResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `idTokenInfo` | [IdTokenInfoType](../OCPP-2.1-DataTypes.md#idtokeninfotype) | **Yes** |  |  |
| `allowedEnergyTransfer` | [EnergyTransferModeEnumType](../OCPP-2.1-DataTypes.md#energytransfermodeenumtype)[] | No | minItems: 1 | *(2.1)* List of allowed energy transfer modes the EV can choose from. If omitted this defaults to charging only. |
| `certificateStatus` | [AuthorizeCertificateStatusEnumType](#authorizecertificatestatusenumtype) | No |  |  |
| `tariff` | [TariffType](../OCPP-2.1-DataTypes.md#tarifftype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearCache

**Direction:** CSMS → CS

### ClearCacheRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### ClearCacheResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [ClearCacheStatusEnumType](#clearcachestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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

### OCSPRequestDataType

Information about a certificate for an OCSP check.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `hashAlgorithm` | [HashAlgorithmEnumType](../OCPP-2.1-DataTypes.md#hashalgorithmenumtype) | **Yes** |  |  |
| `issuerKeyHash` | string | **Yes** | maxLength: 128 | The hash of the DER encoded public key: the value (excluding tag and length) of the subject public key field in the issuer’s certificate. |
| `issuerNameHash` | string | **Yes** | maxLength: 128 | The hash of the issuer’s distinguished name (DN), that must be calculated over the DER encoding of the issuer’s name field in the certificate being checked. |
| `responderURL` | string | **Yes** | maxLength: 2000 | This contains the responder URL (Case insensitive). |
| `serialNumber` | string | **Yes** | maxLength: 40 | The string representation of the hexadecimal value of the serial number without the prefix "0x" and without leading zeroes. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** Authorize, GetCertificateStatus

---
