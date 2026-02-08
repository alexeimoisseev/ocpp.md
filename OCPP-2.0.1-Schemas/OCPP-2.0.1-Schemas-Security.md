# OCPP 2.0.1 Schemas — Security

> **Functional Block:** B/J
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.0.1-DataTypes.md](../OCPP-2.0.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [Get15118EVCertificate](#get15118evcertificate) (CS → CSMS)
- [GetCertificateStatus](#getcertificatestatus) (CS → CSMS)
- [SignCertificate](#signcertificate) (CS → CSMS)
- [CertificateSigned](#certificatesigned) (CSMS → CS)
- [InstallCertificate](#installcertificate) (CSMS → CS)
- [DeleteCertificate](#deletecertificate) (CSMS → CS)
- [GetInstalledCertificateIds](#getinstalledcertificateids) (CSMS → CS)
- [SecurityEventNotification](#securityeventnotification) (CS → CSMS)

---

## Get15118EVCertificate

**Direction:** CS → CSMS

### Get15118EVCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `action` | [CertificateActionEnumType](#certificateactionenumtype) | **Yes** |  |  |
| `exiRequest` | string | **Yes** | maxLength: 5600 | Raw CertificateInstallationReq request from EV, Base64 encoded. |
| `iso15118SchemaVersion` | string | **Yes** | maxLength: 50 | Schema version currently used for the 15118 session between EV and Charging Station. Needed for parsing of the EXI stream by the CSMS. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example Get15118EVCertificateRequest</summary>

```json
{
  "action": "Install",
  "exiRequest": "string",
  "iso15118SchemaVersion": "string"
}
```

</details>

### Get15118EVCertificateResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `exiResponse` | string | **Yes** | maxLength: 5600 | Raw CertificateInstallationRes response for the EV, Base64 encoded. |
| `status` | [Iso15118EVCertificateStatusEnumType](#iso15118evcertificatestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetCertificateStatus

**Direction:** CS → CSMS

### GetCertificateStatusRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `ocspRequestData` | [OCSPRequestDataType](#ocsprequestdatatype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetCertificateStatusRequest</summary>

```json
{
  "ocspRequestData": {
    "hashAlgorithm": "SHA256",
    "issuerNameHash": "string",
    "issuerKeyHash": "string",
    "serialNumber": "string",
    "responderURL": "string"
  }
}
```

</details>

### GetCertificateStatusResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GetCertificateStatusEnumType](#getcertificatestatusenumtype) | **Yes** |  |  |
| `ocspResult` | string | No | maxLength: 5500 | OCSPResponse class as defined in IETF RFC 6960. DER encoded (as defined in IETF RFC 6960), and then base64 encoded. MAY only be omitted when status is not Accepted. |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## SignCertificate

**Direction:** CS → CSMS

### SignCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `csr` | string | **Yes** | maxLength: 5500 | The Charging Station SHALL send the public key in form of a Certificate Signing Request (CSR) as described in RFC 2986 [22] and then PEM encoded, using the SignCertificateRequest message. |
| `certificateType` | [CertificateSigningUseEnumType](#certificatesigninguseenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SignCertificateRequest</summary>

```json
{
  "csr": "string"
}
```

</details>

### SignCertificateResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.0.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## CertificateSigned

**Direction:** CSMS → CS

### CertificateSignedRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateChain` | string | **Yes** | maxLength: 10000 | The signed PEM encoded X.509 certificate. This can also contain the necessary sub CA certificates. In that case, the order of the bundle should follow the certificate chain, starting from the leaf certificate. The Configuration Variable MaxCertificateChainSize can be used to limit the maximum size of this field. |
| `certificateType` | [CertificateSigningUseEnumType](#certificatesigninguseenumtype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example CertificateSignedRequest</summary>

```json
{
  "certificateChain": "string"
}
```

</details>

### CertificateSignedResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [CertificateSignedStatusEnumType](#certificatesignedstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## InstallCertificate

**Direction:** CSMS → CS

### InstallCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificate` | string | **Yes** | maxLength: 5500 | A PEM encoded X.509 certificate. |
| `certificateType` | [InstallCertificateUseEnumType](#installcertificateuseenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example InstallCertificateRequest</summary>

```json
{
  "certificate": "string",
  "certificateType": "V2GRootCertificate"
}
```

</details>

### InstallCertificateResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [InstallCertificateStatusEnumType](#installcertificatestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## DeleteCertificate

**Direction:** CSMS → CS

### DeleteCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateHashData` | [CertificateHashDataType](../OCPP-2.0.1-DataTypes.md#certificatehashdatatype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example DeleteCertificateRequest</summary>

```json
{
  "certificateHashData": {
    "hashAlgorithm": "SHA256",
    "issuerNameHash": "string",
    "issuerKeyHash": "string",
    "serialNumber": "string"
  }
}
```

</details>

### DeleteCertificateResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [DeleteCertificateStatusEnumType](#deletecertificatestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetInstalledCertificateIds

**Direction:** CSMS → CS

### GetInstalledCertificateIdsRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateType` | [GetCertificateIdUseEnumType](#getcertificateiduseenumtype)[] | No | minItems: 1 | Indicates the type of certificates requested. When omitted, all certificate types are requested. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


### GetInstalledCertificateIdsResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GetInstalledCertificateStatusEnumType](#getinstalledcertificatestatusenumtype) | **Yes** |  |  |
| `certificateHashDataChain` | [CertificateHashDataChainType](#certificatehashdatachaintype)[] | No | minItems: 1 |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.0.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


---

## SecurityEventNotification

**Direction:** CS → CSMS

### SecurityEventNotificationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `timestamp` | string (date-time) | **Yes** |  | Date and time at which the event occurred. |
| `type` | string | **Yes** | maxLength: 50 | Type of the security event. This value should be taken from the Security events list. |
| `techInfo` | string | No | maxLength: 255 | Additional information about the occurred security event. |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


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

## Local Types

*Types used only within this block's messages.*

### CertificateActionEnumType

Defines whether certificate needs to be installed or updated.

| Value |
|-------|
| `Install` |
| `Update` |

**Used in:** Get15118EVCertificate

---

### CertificateSignedStatusEnumType

Returns whether certificate signing has been accepted, otherwise rejected.

| Value |
|-------|
| `Accepted` |
| `Rejected` |

**Used in:** CertificateSigned

---

### CertificateSigningUseEnumType

Indicates the type of the signed certificate that is returned. When omitted the certificate is used for both the 15118 connection (if implemented) and the Charging Station to CSMS connection. This field is required when a typeOfCertificate was included in the SignCertificateRequest that requested this certificate to be signed AND both the 15118 connection and the Charging Station connection are implemented.

| Value |
|-------|
| `ChargingStationCertificate` |
| `V2GCertificate` |

**Used in:** CertificateSigned, SignCertificate

---

### DeleteCertificateStatusEnumType

Charging Station indicates if it can process the request.

| Value |
|-------|
| `Accepted` |
| `Failed` |
| `NotFound` |

**Used in:** DeleteCertificate

---

### GetCertificateIdUseEnumType

Indicates the type of the requested certificate(s).

| Value |
|-------|
| `V2GRootCertificate` |
| `MORootCertificate` |
| `CSMSRootCertificate` |
| `V2GCertificateChain` |
| `ManufacturerRootCertificate` |

**Used in:** GetInstalledCertificateIds

---

### GetCertificateStatusEnumType

This indicates whether the charging station was able to retrieve the OCSP certificate status.

| Value |
|-------|
| `Accepted` |
| `Failed` |

**Used in:** GetCertificateStatus

---

### GetInstalledCertificateStatusEnumType

Charging Station indicates if it can process the request.

| Value |
|-------|
| `Accepted` |
| `NotFound` |

**Used in:** GetInstalledCertificateIds

---

### InstallCertificateStatusEnumType

Charging Station indicates if installation was successful.

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `Failed` |

**Used in:** InstallCertificate

---

### InstallCertificateUseEnumType

Indicates the certificate type that is sent.

| Value |
|-------|
| `V2GRootCertificate` |
| `MORootCertificate` |
| `CSMSRootCertificate` |
| `ManufacturerRootCertificate` |

**Used in:** InstallCertificate

---

### Iso15118EVCertificateStatusEnumType

Indicates whether the message was processed properly.

| Value |
|-------|
| `Accepted` |
| `Failed` |

**Used in:** Get15118EVCertificate

---

### CertificateHashDataChainType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateHashData` | [CertificateHashDataType](../OCPP-2.0.1-DataTypes.md#certificatehashdatatype) | **Yes** |  |  |
| `certificateType` | [GetCertificateIdUseEnumType](#getcertificateiduseenumtype) | **Yes** |  |  |
| `childCertificateHashData` | [CertificateHashDataType](../OCPP-2.0.1-DataTypes.md#certificatehashdatatype)[] | No | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.0.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetInstalledCertificateIds

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
