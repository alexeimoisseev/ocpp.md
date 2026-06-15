# OCPP 2.1 Schemas — Certificates

> **Functional Block:** M
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [Get15118EVCertificate](#get15118evcertificate) (CS → CSMS)
- [GetCertificateStatus](#getcertificatestatus) (CS → CSMS)
- [GetCertificateChainStatus](#getcertificatechainstatus) (CS → CSMS)
- [SignCertificate](#signcertificate) (CS → CSMS)
- [CertificateSigned](#certificatesigned) (CSMS → CS)
- [InstallCertificate](#installcertificate) (CSMS → CS)
- [DeleteCertificate](#deletecertificate) (CSMS → CS)
- [GetInstalledCertificateIds](#getinstalledcertificateids) (CSMS → CS)

---

## Get15118EVCertificate

**Direction:** CS → CSMS

### Get15118EVCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `action` | [CertificateActionEnumType](#certificateactionenumtype) | **Yes** |  |  |
| `exiRequest` | string | **Yes** | maxLength: 11000 | *(2.1)* Raw CertificateInstallationReq request from EV, Base64 encoded. + Extended to support ISO 15118-20 certificates. The minimum supported length is 11000. If a longer _exiRequest_ is supported, then the supported length must be communicated in variable OCPPCommCtrlr.FieldLength[ "Get15118EVCertificateRequest.exiRequest" ]. |
| `iso15118SchemaVersion` | string | **Yes** | maxLength: 50 | Schema version currently used for the 15118 session between EV and Charging Station. Needed for parsing of the EXI stream by the CSMS. |
| `maximumContractCertificateChains` | integer | No | min: 0.0 | *(2.1)* Absent during ISO 15118-2 session. Required during ISO 15118-20 session. + Maximum number of contracts that EV wants to install. |
| `prioritizedEMAIDs` | string[] | No | minItems: 1, maxItems: 8 | *(2.1)* Absent during ISO 15118-2 session. Optional during ISO 15118-20 session. List of EMAIDs for which contract certificates must be requested first, in case there are more certificates than allowed by _maximumContractCertificateChains_. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `exiResponse` | string | **Yes** | maxLength: 17000 | *(2/1)* Raw CertificateInstallationRes response for the EV, Base64 encoded. + Extended to support ISO 15118-20 certificates. The minimum supported length is 17000. If a longer _exiResponse_ is supported, then the supported length must be communicated in variable OCPPCommCtrlr.FieldLength[ "Get15118EVCertificateResponse.exiResponse" ]. |
| `status` | [Iso15118EVCertificateStatusEnumType](#iso15118evcertificatestatusenumtype) | **Yes** |  |  |
| `remainingContracts` | integer | No | min: 0.0 | *(2.1)* Number of contracts that can be retrieved with additional requests. |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetCertificateStatus

**Direction:** CS → CSMS

### GetCertificateStatusRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `ocspRequestData` | [OCSPRequestDataType](#ocsprequestdatatype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `ocspResult` | string | No | maxLength: 18000 | *(2.1)* OCSPResponse class as defined in IETF RFC 6960. DER encoded (as defined in IETF RFC 6960), and then base64 encoded. MAY only be omitted when status is not Accepted. + The minimum supported length is 18000. If a longer _ocspResult_ is supported, then the supported length must be communicated in variable OCPPCommCtrlr.FieldLength[ "GetCertificateStatusResponse.ocspResult" ]. |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetCertificateChainStatus

**Direction:** CS → CSMS

### GetCertificateChainStatusRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateStatusRequests` | [CertificateStatusRequestInfoType](#certificatestatusrequestinfotype)[] | **Yes** | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetCertificateChainStatusRequest</summary>

```json
{
  "certificateStatusRequests": [
    {
      "source": "CRL",
      "urls": [
        "string"
      ],
      "certificateHashData": "{...}"
    }
  ]
}
```

</details>

### GetCertificateChainStatusResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateStatus` | [CertificateStatusType](#certificatestatustype)[] | **Yes** | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## SignCertificate

**Direction:** CS → CSMS

### SignCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `csr` | string | **Yes** | maxLength: 5500 | The Charging Station SHALL send the public key in form of a Certificate Signing Request (CSR) as described in RFC 2986 [22] and then PEM encoded, using the SignCertificateRequest message. |
| `certificateType` | [CertificateSigningUseEnumType](#certificatesigninguseenumtype) | No |  |  |
| `hashRootCertificate` | [CertificateHashDataType](../OCPP-2.1-DataTypes.md#certificatehashdatatype) | No |  |  |
| `requestId` | integer | No |  | *(2.1)* RequestId to match this message with the CertificateSignedRequest. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `status` | [GenericStatusEnumType](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## CertificateSigned

**Direction:** CSMS → CS

### CertificateSignedRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateChain` | string | **Yes** | maxLength: 10000 | The signed PEM encoded X.509 certificate. This SHALL also contain the necessary sub CA certificates, when applicable. The order of the bundle follows the certificate chain, starting from the leaf certificate. The Configuration Variable MaxCertificateChainSize can be used to limit the maximum size of this field. |
| `certificateType` | [CertificateSigningUseEnumType](#certificatesigninguseenumtype) | No |  |  |
| `requestId` | integer | No |  | *(2.1)* RequestId to correlate this message with the SignCertificateRequest. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## InstallCertificate

**Direction:** CSMS → CS

### InstallCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificate` | string | **Yes** | maxLength: 10000 | A PEM encoded X.509 certificate. |
| `certificateType` | [InstallCertificateUseEnumType](#installcertificateuseenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## DeleteCertificate

**Direction:** CSMS → CS

### DeleteCertificateRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateHashData` | [CertificateHashDataType](../OCPP-2.1-DataTypes.md#certificatehashdatatype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## GetInstalledCertificateIds

**Direction:** CSMS → CS

### GetInstalledCertificateIdsRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateType` | [GetCertificateIdUseEnumType](#getcertificateiduseenumtype)[] | No | minItems: 1 | Indicates the type of certificates requested. When omitted, all certificate types are requested. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### GetInstalledCertificateIdsResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GetInstalledCertificateStatusEnumType](#getinstalledcertificatestatusenumtype) | **Yes** |  |  |
| `certificateHashDataChain` | [CertificateHashDataChainType](#certificatehashdatachaintype)[] | No | minItems: 1 |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


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
| `V2G20Certificate` |

**Used in:** CertificateSigned, SignCertificate

---

### CertificateStatusEnumType

Status of certificate: good, revoked or unknown.

| Value |
|-------|
| `Good` |
| `Revoked` |
| `Unknown` |
| `Failed` |

**Used in:** GetCertificateChainStatus

---

### CertificateStatusSourceEnumType

Source of status: OCSP, CRL

| Value |
|-------|
| `CRL` |
| `OCSP` |

**Used in:** GetCertificateChainStatus

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
| `OEMRootCertificate` |

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
| `ManufacturerRootCertificate` |
| `CSMSRootCertificate` |
| `OEMRootCertificate` |

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
| `certificateHashData` | [CertificateHashDataType](../OCPP-2.1-DataTypes.md#certificatehashdatatype) | **Yes** |  |  |
| `certificateType` | [GetCertificateIdUseEnumType](#getcertificateiduseenumtype) | **Yes** |  |  |
| `childCertificateHashData` | [CertificateHashDataType](../OCPP-2.1-DataTypes.md#certificatehashdatatype)[] | No | minItems: 1, maxItems: 4 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetInstalledCertificateIds

---

### CertificateStatusRequestInfoType

Data necessary to request the revocation status of a certificate.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateHashData` | [CertificateHashDataType](../OCPP-2.1-DataTypes.md#certificatehashdatatype) | **Yes** |  |  |
| `source` | [CertificateStatusSourceEnumType](#certificatestatussourceenumtype) | **Yes** |  |  |
| `urls` | string[] | **Yes** | minItems: 1, maxItems: 5 | URL(s) of _source_. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetCertificateChainStatus

---

### CertificateStatusType

Revocation status of certificate

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `certificateHashData` | [CertificateHashDataType](../OCPP-2.1-DataTypes.md#certificatehashdatatype) | **Yes** |  |  |
| `nextUpdate` | string (date-time) | **Yes** |  |  |
| `source` | [CertificateStatusSourceEnumType](#certificatestatussourceenumtype) | **Yes** |  |  |
| `status` | [CertificateStatusEnumType](#certificatestatusenumtype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetCertificateChainStatus

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
