# OCPP 2.1 — Standardized Open Enumerations

> **Source:** OCA OCPP 2.1 appendix CSVs. These are **open enumerations**: the JSON schemas type these fields as free-form strings and point here for the standardized values. Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md).

## Connector Types (33)

> Backs the free-form `connectorType` field.

| Value | Description |
| --- | --- |
| bBatterySlot | Slot of a battery swap station to accept battery cartridges (type unspecified) |
| cCCS1 | Combined Charging System 1 (captive cabled) a.k.a. Combo 1 |
| cCCS2 | Combined Charging System 2 (captive cabled) a.k.a. Combo 2 |
| cChaoJi | ChaoJi (captive cabled) a.k.a. CHAdeMO 3.0 |
| cG105 | JARI G105-1993 (captive cabled) a.k.a. CHAdeMO (captive cabled) |
| cGBT-DC | GB/T 20234.3 DC connector (captive cabled) |
| cLECCS | Light Equipment Combined Charging System IS17017 (captive cabled) |
| cMCS | Megawatt Charging System (captive cabled) |
| cNACS | North American Charging Standard J3400 (captive cabled) |
| cNACS-CCS1 | Built-in NACS to CCS1 adapter (captive cabled) |
| cCCS1-NACS | Built-in CCS1 to NACS adapter (captive cabled) |
| cTesla | Tesla Connector (captive cabled) |
| cType1 | IEC62196-2 Type 1 connector (captive cabled) a.k.a. J1772 |
| cType2 | IEC62196-2 Type 2 connector (captive cabled) a.k.a. Mennekes connector |
| cUltraChaoJi | Ultra-ChaoJi for megawatt charging (captive cabled) |
| s309-1P-16A | 16A 1 phase IEC60309 socket |
| s309-1P-32A | 32A 1 phase IEC60309 socket |
| s309-3P-16A | 16A 3 phase IEC60309 socket |
| s309-3P-32A | 32A 3 phase IEC60309 socket |
| sBS1361 | UK domestic socket a.k.a. 13Amp |
| sCEE-7-7 | CEE 7/7 16A socket. May represent 7/4 and 7/5 a.k.a Schuko |
| sType1 | IEC62196-2 Type 1 socket a.k.a. J1772 |
| sType2 | IEC62196-2 Type 2 socket a.k.a. Mennekes connector |
| sType3 | IEC62196-2 Type 3 socket a.k.a. Scame |
| wInductive | Wireless inductively coupled connection (generic) |
| wResonant | Wireless resonant coupled connection (generic) |
| OppCharge | Pantograph down connector |
| Other1PhMax16A | Other single phase (domestic) sockets not mentioned above, rated at no more than 16A. CEE7/17, AS3112, NEMA 5-15, NEMA 5-20, JISC8303, TIS166, SI 32, CPCS-CCC, SEV1011, etc. |
| Other1PhOver16A | Other single phase sockets not mentioned above (over 16A) |
| Other3Ph | Other 3 phase sockets not mentioned above. NEMA14-30, NEMA14-50. |
| Pan | Pantograph up connector |
| Undetermined | Yet to be determined (e.g. before plugged in) |
| Unknown | Unknown/not determinable |

## Units of Measure (34)

> Backs the `unit` field in MeterValues/measurands.

| Value | Description |
| --- | --- |
| A | Amperes (current) |
| ASU | Arbitrary Strength Unit (Signal Strength) |
| B | Bytes |
| Celsius | Degrees (temperature) |
| dB | Decibel (for example Signal Strength) |
| dBm | Power relative to 1mW (^10^log(P/1mW)) |
| Deg | Degrees (angle/rotation) |
| Fahrenheit | Degrees (temperature) |
| Hz | Hertz (frequency) |
| mHz | milliHertz (frequency) |
| K | Degrees Kelvin (temperature) |
| lx | Lux (Light Intensity) |
| m | Meter (length) |
| ms2 | m/s^2^ (Acceleration) |
| N | Newtons (Force) |
| Ohm | Ohm (Impedance) |
| kPa | kiloPascal (Pressure) |
| Percent | Percentage |
| RH | Relative Humidity% |
| RPM | Revolutions per Minute |
| s | Seconds (Time) |
| V | Voltage (DC or r.m.s. AC) |
| VA | Volt-Ampere (apparent power) |
| kVA | kiloVolt-Ampere (apparent power) |
| VAh | Volt-Ampere-hours (apparent energy) |
| kVAh | kiloVolt-Ampere-hours (apparent energy) |
| var | vars (reactive power) |
| kvar | kilovars (reactive power) |
| varh | var-hours (reactive energy) |
| kvarh | kilovar-hours (reactive energy) |
| W | Watts (power) |
| kW | kilowatts (power) |
| Wh | Watt-hours (energy). Default |
| kWh | kilowatt-hours (energy) |

## Security Events (21)

> Backs `SecurityEventNotification.type`.

| Security Event | Description | Critical |
| --- | --- | --- |
| FirmwareUpdated | The Charging Station firmware is updated | Yes |
| FailedToAuthenticateAtCsms | The authentication credentials provided by the Charging Station were rejected by the CSMS | No |
| CsmsFailedToAuthenticate | The authentication credentials provided by the CSMS were rejected by the Charging Station | No |
| SettingSystemTime | The system time on the Charging Station was changed more than `ClockCtrlr.TimeAdjustmentReportingThreshold` seconds | Yes |
| StartupOfTheDevice | The Charging Station has booted | Yes |
| ResetOrReboot | The Charging Station was rebooted or reset | Yes |
| SecurityLogWasCleared | The security log was cleared | Yes |
| ReconfigurationOfSecurityParameters | Security parameters, such as keys or the security profile used, were changed | No |
| MemoryExhaustion | The Flash or RAM memory of the Charging Station is getting full | Yes |
| InvalidMessages | The Charging Station has received messages that are not valid OCPP messages, if signed messages, signage invalid/incorrect | No |
| AttemptedReplayAttacks | The Charging Station has received a replayed message (other than the CSMS trying to resend a message because it there was for example a network problem) | No |
| TamperDetectionActivated | The physical tamper detection sensor was triggered | Yes |
| InvalidFirmwareSignature | The firmware signature is not valid | Yes |
| InvalidFirmwareSigningCertificate | The certificate used to verify the firmware signature is not valid | Yes |
| InvalidCsmsCertificate | The certificate that the CSMS uses was not valid or could not be verified | Yes |
| InvalidChargingStationCertificate | The certificate sent to the Charging Station using the CertificateSignedRequest message is not a valid certificate | Yes |
| DiscardedRenewedClientCertificate | The Charging Station discarded the renewed client certificate, because it was unable to successfully establish a connection using it. | Yes |
| InvalidTLSVersion | The TLS version used by the CSMS is lower than 1.2 and is not allowed by the security specification | Yes |
| InvalidTLSCipherSuite | The CSMS did only allow connections using TLS cipher suites that are not allowed by the security specification | Yes |
| MaintenanceLoginAccepted | Successful login to the local maintenance interface. It is recommended to include information like the user identification and the origin of the login attempt, which can be an ip-address or a touch screen for example, to the techInfo field. For this the following format is strongly recommended: '{\'user\': \'...\', \'origin\': \'...\'}' | Yes |
| MaintenanceLoginFailed | Failed login attempt to the local maintenance interface. It is recommended to include information like the user identification and the origin of the login attempt, which can be an ip-address or a touch screen for example, to the techInfo field. For this the following format is strongly recommended: '{\'user\': \'...\', \'origin\': \'...\'}' | Yes |

## Status Reason Codes (72)

> Standardized `StatusInfo.reasonCode` values.

| Group | Reason code | Description | Typically used for |
| --- | --- | --- | --- |
| Charging Profiles |  |  |  |
|  | DuplicateProfile | A charging profile with same _stackLevel - chargingProfilePurpose_ combination already exists on the Charging Station and has an overlapping validity period. | SetChargingProfile |
|  | InvalidProfile | Provided _chargingProfile_ contains invalid elements. | SetChargingProfile, RequestStartTransaction |
|  | InvalidProfileId | Provided _chargingProfile_ has an id that is within an invalid range. | SetChargingProfile, RequestStartTransaction |
|  | InvalidSchedule | Provided _chargingSchedule_ contains invalid elements. | SetChargingProfile, RequestStartTransaction |
|  | InvalidStackLevel | Provided value for _stackLevel_ is invalid. | SetChargingProfile |
|  | InvalidOperationMode | Provided operationMode is invalid for this chargingProfilePurpose | SetChargingProfile |
|  | NoFreqWattCurve | A frequency-watt curve is missing in a charging schedule period with operation mode = LocalFrequency. | SetChargingProfile |
|  | NoPhaseForDC | Phase selection for a DC EVSE is not supported | SetChargingProfile |
|  | PhaseConflict | Phase conflict between applicable charging profiles | SetChargingProfile |
|  | NoSignalWattCurve | A signal-watt curve is missing in a charging schedule period when an AFRRSignalRequest is received. | AFRRSignal |
|  | RateLimitExceeded | A charging profile of the same purpose is submitted too frequently | SetChargingProfile |
|  | UnsupportedKind | The requested charging profile kind is not supported | SetChargingProfile |
|  | UnsupportedPurpose | The requested charging profile purpose is not supported | SetChargingProfile |
|  | UnsupportedRateUnit | A _chargingRateUnit_ is provided that is not supported. | SetChargingProfile |
| Charging Station |  |  |  |
|  | CSNotAccepted | BootNotification of Charging Station has not (yet) been accepted by CSMS. | RequestStartTransaction, RequestStopTransaction |
|  | FixedCable | The connector has its own fixed cable that cannot be unlocked. | UnlockConnector |
|  | NoCable | No cable is connected at this time. | UnlockConnector |
|  | UnknownConnectorId | Connector Id is not known on EVSE | ChangeAvailability, UnlockConnector |
|  | UnknownConnectorType | Connector type is not known on EVSE | ReserveNow |
|  | UnknownEvse | EVSE is not known on Charging Stations | ChangeAvailability, ReserveNow, RequestStartTransaction |
| Swap Station |  |  |  |
|  | BatterySoHLow | Battery State of Health is too low | BatterySwap |
|  | BatterySoC | Battery State of Charge has unacceptable value | BatterySwap |
|  | BatteryDamaged | Battery is damaged | BatterySwap |
|  | BatteryUnknown | Battery has unknown serial number | BatterySwap |
|  | BatteryType | Battery type not accepted | BatterySwap |
|  | NoBatteryAvailable | No battery available for swapping | BatterySwap, RequestBatterySwap |
| Network Configuration |  |  |  |
|  | PriorityNetworkConf | A network configuration variable of an NetworkConfiguration instance present in NetworkConfigurationPriority is not allowed to be changed | SetVariablesRequest of NetworkConfiguration |
|  | InvalidConfSlot | A value for configurationSlot is used that is not present in NetworkConfigurationPriority.valuesList | SetNetworkProfileRequest |
|  | InvalidNetworkConf | Some values in NetworkConfiguration instance are invalid | SetVariablesRequest of NetworkConfigurationPriority,SetNetworkProfileRequest |
|  | NoSecurityDowngrade | Security profile downgrade is not allowed | SetVariablesRequest of SecurityProfile, SetNetworkProfileRequest |
| Miscellaneous |  |  |  |
|  | DuplicateRequestId | A _requestId_ is provided, that has already been used for this type of request. | UpdateFirmware, PublishFirmware and requests for reports. |
|  | InvalidMessageSeq | Message should not be sent at this moment in current scenario. | (generic), SetChargingProfile with ISO15118 |
|  | MissingDevModelInfo | Information needed for operation is missing from Device Model | (generic) |
|  | NoError | No error has occurred, but some extra information is in _additionalInfo_ . | (generic) |
|  | NotFound | No object(s) found that match a provided ID or criteria. | ClearVariableMonitoring, CustomerInformation, GetChargingProfiles, GetDisplayMessages, GetInstalledCertificateIds, GetReport |
|  | Unspecified | No reason is specified, but some extra information is in _additionalInfo_ | (generic) |
|  | UnsupportedRequest | This request is not supported. | (generic) |
| Operations and Permissions |  |  |  |
|  | FwUpdateInProgress | Operation is not possible, because a firmware update is in progress. | Reset |
|  | NotEnabled | Feature is not enabled. | ClearCache |
|  | ReadOnly | Targeted variable is read-only and cannot be set. | SetVariables |
|  | WriteOnly | Targeted variable is write-only and cannot be read. | GetVariables |
| Security |  |  |  |
|  | InvalidCSR | Provided CSR is invalid | SignCertificate |
|  | InvalidCertificate | Provided certificate is invalid. | CertificateSigned, InstallCertificate |
|  | InvalidURL | Provided URL is invalid. | UpdateFirmware, PublishFirmware |
|  | RedirectNotAllowed | HTTP Redirection is not allowed | LogStatusNotification |
| System Errors |  |  |  |
|  | InternalError | Operation cannot be completed due to an internal error. | (generic) |
|  | OutOfMemory | Operation not possible, because system does not have enough memory. | (generic) |
|  | OutOfStorage | Operation not possible, because system does not have enough storage. | (generic) |
| Transactions |  |  |  |
|  | InvalidIdToken | Provided _idToken_ is not valid. | RequestStartTransaction |
|  | TxInProgress | A transaction is in progress. | ChangeAvailability, Reset, RequestStartTransaction |
|  | TxNotFound | There is no such transaction. | RequestStopTransaction, SetChargingProfile, GetVehicleCertificate |
|  | TxStarted | A transaction had already started (e.g. due to cable being plugged in). | RequestStartTransaction |
| Values and Ranges |  |  |  |
|  | InvalidValue | An invalid value has been provided. | (generic) |
|  | MissingParam | A parameter that is required for the request is missing. | (generic) |
|  | TooLargeElement | Provided element is too large to handle. | CertificateSigned, InstallCertificate |
|  | TooManyElements | Too many elements have been provided. | SetChargingProfile, SetVariables, SendLocalList |
|  | UnsupportedParam | A parameter was provided that is not supported. | (generic) |
|  | ValueOutOfRange | Provided value is out of range. | SetVariables, SetVariableMonitoring |
|  | ValuePositiveOnly | Provided value is not greater than zero. | (generic) |
|  | ValueTooHigh | Provided value is too high. | (generic) |
|  | ValueTooLow | Provided value is too low. | (generic) |
|  | ValueZeroNotAllowed | Provided value cannot be zero. | (generic) |

## Signing Methods (7)

> Backs `signingMethod` in signed meter values.

| SigningMethod | Algorithm | Curve | Key Length | Hash Algorithm |
| --- | --- | --- | --- | --- |
| ECDSA-secp192k1-SHA256 | ECDSA | secp192k1 | 192 bits | SHA-256 |
| ECDSA-secp256k1-SHA256 | ECDSA | secp256k1 | 256 bits | SHA-256 |
| ECDSA-secp192r1-SHA256 | ECDSA | secp192r1 | 192 bits | SHA-256 |
| ECDSA-secp256r1-SHA256 | ECDSA | secp256r1 | 256 bits | SHA-256 |
| ECDSA-brainpool256r1-SHA256 | ECDSA | brainpool256r1 | 256 bits | SHA-256 |
| ECDSA-secp384r1-SHA256 | ECDSA | secp384r1 | 384 bits | SHA-256 |
| ECDSA-brainpool384r1-SHA256 | ECDSA | brainpool384r1 | 384 bits | SHA-256 |

## Charging Limit Sources (4)

> Backs `chargingLimitSource`.

| Value | Description |
| --- | --- |
| EMS | Indicates that an Energy Management System has sent a charging limit. |
| Other | Indicates that an external source, not being an EMS or system operator, has sent a charging limit. |
| SO | Indicates that a System Operator (DSO or TSO) has sent a charging limit. |
| CSO | Indicates that the CSO has set this charging profile. |

## IdToken Types (11)

> Standardized `idToken.type` values.

| Value | Description |
| --- | --- |
| Central | A centrally, in the CSMS (or other server) generated id (for example used for a remotely started transaction that is activated by SMS). No format defined, might be a UUID. |
| DirectPayment | IdToken from a payment terminal that authorized a payment card. Usually a reference id from payment service provider. |
| eMAID | Electro-mobility account id as defined in ISO 15118 |
| EVCCID | EVCCID of EV. For ISO 15118-2 this is the MAC address. For ISO 15118-20 this is an identifier up to 255 characters. |
| ISO14443 | ISO 14443 UID of RFID card. It is represented as an array of 4 or 7 bytes in hexadecimal representation. |
| ISO15693 | ISO 15693 UID of RFID card. It is represented as an array of 8 bytes in hexadecimal representation. |
| KeyCode | A private key-code to authorize a charging transaction. For example: Pin-code. |
| Local | A locally generated id (e.g. internal id created by the Charging Station). Needs no checking by CSMS. No format defined, might be a UUID |
| MacAddress | MacAddress of the EVCC (Electric Vehicle Communication Controller) that is connected to the EVSE. Used when MAC address is used for authorization (Autocharge). |
| NoAuthorization | Transaction is started and no authorization possible. Charging Station only has a start button or mechanical key etc. IdToken field SHALL be left empty. |
| VIN | Vehicle Identification Number of EV. |

## Additional Info Types (2)

> Backs `additionalInfo.type`.

| additionalInfo.type | Description |
| --- | --- |
| EVCCID | The EVCCID of EV is added as additionalInfo to an idToken for ISO 15118-20 sessions. |
| ISO14443SubType | The subtype of an ISO 14443 RFID card. For example: 'VDE-AR-E-2532-100' (a secure variant of ISO 14443). |

## Additional Info Types (Ad-hoc) (11)

> Ad-hoc payment additionalInfo types.

| additionalInfo.type | Description |
| --- | --- |
| PspRef | Payment Service Provider reference id for payment session. Only use when PspRef is not in _idToken_. |
| SessionRef | Payment session reference id from terminal (not the same as pspRef) |
| MerchantRef | Merchant (CSO) reference id for payment session |
| PaymentBrand | Brand of ad hoc payment card. See predefined list of values in table below. |
| ReadingMethod | Contactless / Contact / Magstripe |
| PaymentRecognition | Credit/debit card or digital wallet. See predefined list of values in table below. |
| CardBin | Card first 6 digits |
| CardLast4Digits | Card last 4 digits |
| CardExpiryDate | The expiry date of the card. Format: YYYY/MM |
| HashedCardNr | The hashed card number. |
| WalletUserId | User ID for a digital wallet, e.g. Alipay. |

## Payment Brands (22)

> Standardized payment brand values.

| PaymentBrand | Description |
| --- | --- |
| AMEX |  |
| ApplePay |  |
| Bancontact |  |
| BankAxept |  |
| Carnet |  |
| CartesBancaires |  |
| Dankort |  |
| Diners |  |
| Discover |  |
| EftposAustralia |  |
| Elo |  |
| Girocard |  |
| GooglePay |  |
| Hipercard |  |
| Interac |  |
| JCB |  |
| Maestro |  |
| Mastercard |  |
| SamsungPay |  |
| UnionPay |  |
| VPay |  |
| Visa |  |

## Payment Recognition (9)

> Payment recognition method values.

| PaymentRecognition | Description |
| --- | --- |
| CC | Credit card |
| Debit | Debit card |
| Alipay |  |
| ApplePay |  |
| GooglePay |  |
| GrabPay |  |
| PayPal |  |
| SamsungPay |  |
| WeChatPay |  |
