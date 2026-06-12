# OCPP 2.1 Schemas — TariffAndCost

> **Functional Block:** I
>
> **Types Reference:** Shared types referenced below are defined in [OCPP-2.1-DataTypes.md](../OCPP-2.1-DataTypes.md).
> Types used only within this block are documented [inline below](#local-types).

## Messages

- [CostUpdated](#costupdated) (CSMS → CS)
- [GetTariffs](#gettariffs) (CSMS → CS)
- [SetDefaultTariff](#setdefaulttariff) (CSMS → CS)
- [ChangeTransactionTariff](#changetransactiontariff) (CSMS → CS)
- [ClearTariffs](#cleartariffs) (CSMS → CS)
- [NotifySettlement](#notifysettlement) (CS → CSMS)
- [NotifyWebPaymentStarted](#notifywebpaymentstarted) (CSMS → CS)
- [VatNumberValidation](#vatnumbervalidation) (CS → CSMS)

---

## CostUpdated

**Direction:** CSMS → CS

### CostUpdatedRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `totalCost` | number | **Yes** |  | Current total cost, based on the information known by the CSMS, of the transaction including taxes. In the currency configured with the configuration Variable: [Currency] |
| `transactionId` | string | **Yes** | maxLength: 36 | Transaction Id of the transaction the current cost are asked for. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example CostUpdatedRequest</summary>

```json
{
  "totalCost": 0.0,
  "transactionId": "string"
}
```

</details>

### CostUpdatedResponse

*No required fields. An empty `{}` is a valid response.*

---

## GetTariffs

**Direction:** CSMS → CS

### GetTariffsRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | **Yes** | min: 0.0 | EVSE id to get tariff from. When _evseId_ = 0, this gets tariffs from all EVSEs. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example GetTariffsRequest</summary>

```json
{
  "evseId": 0
}
```

</details>

### GetTariffsResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [TariffGetStatusEnumType](#tariffgetstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `tariffAssignments` | [TariffAssignmentType](#tariffassignmenttype)[] | No | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## SetDefaultTariff

**Direction:** CSMS → CS

### SetDefaultTariffRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | **Yes** | min: 0.0 | EVSE that tariff applies to. When _evseId_ = 0, then tarriff applies to all EVSEs. |
| `tariff` | [TariffType](../OCPP-2.1-DataTypes.md#tarifftype) | **Yes** |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example SetDefaultTariffRequest</summary>

```json
{
  "evseId": 0,
  "tariff": {
    "tariffId": "string",
    "currency": "string"
  }
}
```

</details>

### SetDefaultTariffResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [TariffSetStatusEnumType](#tariffsetstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ChangeTransactionTariff

**Direction:** CSMS → CS

### ChangeTransactionTariffRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `tariff` | [TariffType](../OCPP-2.1-DataTypes.md#tarifftype) | **Yes** |  |  |
| `transactionId` | string | **Yes** | maxLength: 36 | Transaction id for new tariff. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example ChangeTransactionTariffRequest</summary>

```json
{
  "tariff": {
    "tariffId": "string",
    "currency": "string"
  },
  "transactionId": "string"
}
```

</details>

### ChangeTransactionTariffResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [TariffChangeStatusEnumType](#tariffchangestatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## ClearTariffs

**Direction:** CSMS → CS

### ClearTariffsRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | No | min: 0.0 | When present only clear tariffs matching _tariffIds_ at EVSE _evseId_. |
| `tariffIds` | string[] | No | minItems: 1 | List of tariff Ids to clear. When absent clears all tariffs at _evseId_. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


### ClearTariffsResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `clearTariffsResult` | [ClearTariffsResultType](#cleartariffsresulttype)[] | **Yes** | minItems: 1 |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## NotifySettlement

**Direction:** CS → CSMS

### NotifySettlementRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `pspRef` | string | **Yes** | maxLength: 255 | The payment reference received from the payment terminal and is used as the value for _idToken_. |
| `settlementAmount` | number | **Yes** |  | The amount that was settled, or attempted to be settled (in case of failure). |
| `settlementTime` | string (date-time) | **Yes** |  | The time when the settlement was done. |
| `status` | [PaymentStatusEnumType](#paymentstatusenumtype) | **Yes** |  |  |
| `receiptId` | string | No | maxLength: 50 |  |
| `receiptUrl` | string | No | maxLength: 2000 | The receipt URL, to be used if the receipt is generated by the payment terminal or the CS. |
| `statusInfo` | string | No | maxLength: 500 | Additional information from payment terminal/payment process. |
| `transactionId` | string | No | maxLength: 36 | The _transactionId_ that the settlement belongs to. Can be empty if the payment transaction is canceled prior to the start of the OCPP transaction. |
| `vatCompany` | [AddressType](#addresstype) | No |  |  |
| `vatNumber` | string | No | maxLength: 20 | VAT number for a company receipt. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifySettlementRequest</summary>

```json
{
  "pspRef": "string",
  "settlementAmount": 0.0,
  "settlementTime": "2024-01-15T10:30:00Z",
  "status": "Settled"
}
```

</details>

### NotifySettlementResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `receiptId` | string | No | maxLength: 50 | The receipt id if the receipt is generated by CSMS. |
| `receiptUrl` | string | No | maxLength: 2000 | The receipt URL if receipt generated by CSMS. The Charging Station can QR encode it and show it to the EV Driver. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


*No fields are required. An empty `{}` is a valid response.*

---

## NotifyWebPaymentStarted

**Direction:** CSMS → CS

### NotifyWebPaymentStartedRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `evseId` | integer | **Yes** | min: 0.0 | EVSE id for which transaction is requested. |
| `timeout` | integer | **Yes** |  | Timeout value in seconds after which no result of web payment process (e.g. QR code scanning) is to be expected anymore. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example NotifyWebPaymentStartedRequest</summary>

```json
{
  "evseId": 0,
  "timeout": 0
}
```

</details>

### NotifyWebPaymentStartedResponse

*No required fields. An empty `{}` is a valid response.*

---

## VatNumberValidation

**Direction:** CS → CSMS

### VatNumberValidationRequest

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `vatNumber` | string | **Yes** | maxLength: 20 | VAT number to check. |
| `evseId` | integer | No | min: 0.0 | EVSE id for which check is done |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


<details>
<summary>Example VatNumberValidationRequest</summary>

```json
{
  "vatNumber": "string"
}
```

</details>

### VatNumberValidationResponse

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [GenericStatusEnumType](../OCPP-2.1-DataTypes.md#genericstatusenumtype) | **Yes** |  |  |
| `vatNumber` | string | **Yes** | maxLength: 20 | VAT number that was requested. |
| `company` | [AddressType](#addresstype) | No |  |  |
| `evseId` | integer | No | min: 0.0 | EVSE id for which check was requested. |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


---

## Local Types

*Types used only within this block's messages.*

### PaymentStatusEnumType

The status of the settlement attempt.

| Value |
|-------|
| `Settled` |
| `Canceled` |
| `Rejected` |
| `Failed` |

**Used in:** NotifySettlement

---

### TariffChangeStatusEnumType

Status of the operation

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `TooManyElements` |
| `ConditionNotSupported` |
| `TxNotFound` |
| `NoCurrencyChange` |

**Used in:** ChangeTransactionTariff

---

### TariffClearStatusEnumType

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NoTariff` |

**Used in:** ClearTariffs

---

### TariffGetStatusEnumType

Status of operation

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `NoTariff` |

**Used in:** GetTariffs

---

### TariffKindEnumType

Kind of tariff (driver/default)

| Value |
|-------|
| `DefaultTariff` |
| `DriverTariff` |

**Used in:** GetTariffs

---

### TariffSetStatusEnumType

| Value |
|-------|
| `Accepted` |
| `Rejected` |
| `TooManyElements` |
| `ConditionNotSupported` |
| `DuplicateTariffId` |

**Used in:** SetDefaultTariff

---

### AddressType

*(2.1)* A generic address format.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `address1` | string | **Yes** | maxLength: 100 | Address line 1 |
| `city` | string | **Yes** | maxLength: 100 |  |
| `country` | string | **Yes** | maxLength: 50 | Country name |
| `name` | string | **Yes** | maxLength: 50 | Name of person/company |
| `address2` | string | No | maxLength: 100 | Address line 2 |
| `postalCode` | string | No | maxLength: 20 | Postal code |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** NotifySettlement, VatNumberValidation

---

### ClearTariffsResultType

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `status` | [TariffClearStatusEnumType](#tariffclearstatusenumtype) | **Yes** |  |  |
| `statusInfo` | [StatusInfoType](../OCPP-2.1-DataTypes.md#statusinfotype) | No |  |  |
| `tariffId` | string | No | maxLength: 60 | Id of tariff for which _status_ is reported. If no tariffs were found, then this field is absent, and _status_ will be NoTariff. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** ClearTariffs

---

### TariffAssignmentType

Shows assignment of tariffs to EVSE or IdToken.

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `tariffId` | string | **Yes** | maxLength: 60 | Tariff id. |
| `tariffKind` | [TariffKindEnumType](#tariffkindenumtype) | **Yes** |  |  |
| `evseIds` | integer[] | No | minItems: 1 |  |
| `idTokens` | string[] | No | minItems: 1 | IdTokens related to tariff |
| `validFrom` | string (date-time) | No |  | Date/time when this tariff become active. |
| `customData` | [CustomDataType](../OCPP-2.1-DataTypes.md#customdatatype) | No |  |  |


**Used in:** GetTariffs

---
