# OCPP 2.0.1 — Standardized Open Enumerations

> **Source:** OCA OCPP 2.0.1 appendix CSVs (Appendices v1.4). These are **open enumerations**: the JSON schemas type these fields as free-form strings and point here for the standardized values. Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md).

> OCPP 2.0.1 defines no formal schema type names for these open enumerations (unlike OCPP 2.1's `...EnumStringType` names). Closed enumerations such as `IdTokenEnumType` and `ConnectorEnumType` live in the JSON schemas — see [Data Types](../OCPP-2.0.1-DataTypes.md).

## Units of Measure (33)

> Backs the free-form `unit` field of `UnitOfMeasureType` in sampled meter values.

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

## Security Events (20)

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
| InvalidTLSVersion | The TLS version used by the CSMS is lower than 1.2 and is not allowed by the security specification | Yes |
| InvalidTLSCipherSuite | The CSMS did only allow connections using TLS cipher suites that are not allowed by the security specification | Yes |
| MaintenanceLoginAccepted | Successful login to the local maintenance interface. It is recommended to include information like the user identification and the origin of the login attempt, which can be an ip-address or a touch screen for example, to the techInfo field. For this the following format is strongly recommended: '{\'user\': \'...\', \'origin\': \'...\'}' | Yes |
| MaintenanceLoginFailed | Failed login attempt to the local maintenance interface. It is recommended to include information like the user identification and the origin of the login attempt, which can be an ip-address or a touch screen for example, to the techInfo field. For this the following format is strongly recommended: '{\'user\': \'...\', \'origin\': \'...\'}' | Yes |

## Status Reason Codes (43)

> Standardized `StatusInfo.reasonCode` values.

| Reason Code | Description | Typically used for |
| --- | --- | --- |
| CSNotAccepted | BootNotification of Charging Station has not (yet) been accepted by CSMS. | RequestStartTransaction, RequestStopTransaction |
| DuplicateProfile | A charging profile with same _stackLevel - chargingProfilePurpose_ combination already exists on the Charging Station and has an overlapping validity period. | SetChargingProfile |
| DuplicateRequestId | A _requestId_ is provided, that has already been used for this type of request. | UpdateFirmware, PublishFirmware and requests for reports. |
| FixedCable | The connector has its own fixed cable that cannot be unlocked. | UnlockConnector |
| FwUpdateInProgress | Operation is not possible, because a firmware update is in progress. | Reset |
| InternalError | Operation cannot be completed due to an internal error. | (generic) |
| InvalidCertificate | Provided certificate is invalid. | CertificateSigned, InstallCertificate |
| InvalidCSR | Provided CSR is invalid | SignCertificate |
| InvalidIdToken | Provided _idToken_ is not valid. | RequestStartTransaction |
| InvalidMessageSeq | Message should not be sent at this moment in current scenario. | (generic), SetChargingProfile with ISO15118 |
| InvalidProfile | Provided _chargingProfile_ contains invalid elements. | SetChargingProfile, RequestStartTransaction |
| InvalidSchedule | Provided _chargingSchedule_ contains invalid elements. | SetChargingProfile, RequestStartTransaction |
| InvalidStackLevel | Provided value for _stackLevel_ is invalid. | SetChargingProfile |
| InvalidURL | Provided URL is invalid. | UpdateFirmware, PublishFirmware |
| InvalidValue | An invalid value has been provided. | (generic) |
| MissingDevModelInfo | Information needed for operation is missing from Device Model | (generic) |
| MissingParam | A parameter that is required for the request is missing. | (generic) |
| NoCable | No cable is connected at this time. | UnlockConnector |
| NoError | No error has occurred, but some extra information is in _additionalInfo_ . | (generic) |
| NotEnabled | Feature is not enabled. | ClearCache |
| NotFound | No object(s) found that match a provided ID or criteria. | ClearVariableMonitoring, CustomerInformation, GetChargingProfiles, GetDisplayMessages, GetInstalledCertificateIds, GetReport |
| OutOfMemory | Operation not possible, because system does not have enough memory. | (generic) |
| OutOfStorage | Operation not possible, because system does not have enough storage. | (generic) |
| ReadOnly | Targeted variable is read-only and cannot be set. | SetVariables |
| TooLargeElement | Provided element is too large to handle. | CertificateSigned, InstallCertificate |
| TooManyElements | Too many elements have been provided. | SetChargingProfile, SetVariables, SendLocalList |
| TxInProgress | A transaction is in progress. | ChangeAvailability, Reset, RequestStartTransaction |
| TxNotFound | There is no such transaction. | RequestStopTransaction, SetChargingProfile |
| TxStarted | A transaction had already started (e.g. due to cable being plugged in). | RequestStartTransaction |
| UnknownConnectorId | Connector Id is not known on EVSE | ChangeAvailability, UnlockConnector |
| UnknownConnectorType | Connector type is not known on EVSE | ReserveNow |
| UnknownEvse | EVSE is not known on Charging Stations | ChangeAvailability, ReserveNow, RequestStartTransaction |
| UnknownTxId | Provided _transactionId_ is not known. | RequestStopTransaction |
| Unspecified | No reason is specified, but some extra information is in _additionalInfo_ | (generic) |
| UnsupportedParam | A parameter was provided that is not supported. | (generic) |
| UnsupportedRateUnit | A _chargingRateUnit_ is provided that is not supported. | SetChargingProfile |
| UnsupportedRequest | This request is not supported. | (generic) |
| ValueOutOfRange | Provided value is out of range. | SetVariables, SetVariableMonitoring |
| ValuePositiveOnly | Provided value is not greater than zero. | (generic) |
| ValueTooHigh | Provided value is too high. | (generic) |
| ValueTooLow | Provided value is too low. | (generic) |
| ValueZeroNotAllowed | Provided value cannot be zero. | (generic) |
| WriteOnly | Targeted variable is write-only and cannot be read. | GetVariables |
