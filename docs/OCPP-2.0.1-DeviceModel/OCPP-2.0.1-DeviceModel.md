# OCPP 2.0.1 — Device Model Reference

> **Source:** OCA OCPP 2.0.1 appendix CSVs (`components.csv`, `dm_components_vars.csv`, Appendices v1.4). Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md). These are the **standardized** component and variable names referenced by free-form `name` fields in `GetVariables`/`SetVariables`/`GetReport`. Vendors may extend with optional custom components/variables.

## Components (73)

> Component names link to their variables in [Variables by Component](#variables-by-component) below (components with no component-specific variables use only generic variables).

| Component | Description |
| --- | --- |
| [AlignedDataCtrlr](#aligneddatactrlr) | Logical Component responsible for configuration relating to the reporting of clock-aligned meter data. |
| [AuthCtrlr](#authctrlr) | Logical Component responsible for configuration relating to the use of authorization for Charging Station use. |
| [AuthCacheCtrlr](#authcachectrlr) | Logical Component responsible for configuration relating to the use of a local cache for authorization for Charging Station use. |
| [CHAdeMOCtrlr](#chademoctrlr) | A CHAdeMO Controller component communicates with an EV using the wired CANbus protocol to exchange information and control charging using the CHAdeMO protocol |
| [ClockCtrlr](#clockctrlr) | Provides a means to configure management of time tracking by Charging Station. |
| [DeviceDataCtrlr](#devicedatactrlr) | Logical Component responsible for configuration relating to the exchange and storage of Charging Station Device Model data. |
| [DisplayMessageCtrlr](#displaymessagectrlr) | Logical Component responsible for configuration relating to the display of messages to Charging Station users. |
| [ISO15118Ctrlr](#iso15118ctrlr) | Communicates with an EV to exchange information and control charging using the ISO 15118 protocol. |
| [LocalAuthListCtrlr](#localauthlistctrlr) | Logical Component responsible for configuration relating to the use of Local Authorization Lists for Charging Station use. |
| [MonitoringCtrlr](#monitoringctrlr) | Logical Component responsible for configuration relating to the exchange of monitoring event data. |
| [OCPPCommCtrlr](#ocppcommctrlr) | Logical Component responsible for configuration relating to information exchange between Charging Station and CSMS. |
| [ReservationCtrlr](#reservationctrlr) | Logical Component responsible for configuration relating to reservations. |
| [SampledDataCtrlr](#sampleddatactrlr) | Logical Component responsible for configuration relating to the reporting of sampled meter data. |
| [SecurityCtrlr](#securityctrlr) | Logical Component responsible for configuration relating to security of communications between Charging Station and CSMS. |
| [SmartChargingCtrlr](#smartchargingctrlr) | Logical Component responsible for configuration relating to smart charging. |
| [TariffCostCtrlr](#tariffcostctrlr) | Logical Component responsible for configuration relating to tariff and cost display. |
| [TxCtrlr](#txctrlr) | Logical Component responsible for configuration relating to transaction characteristics and behaviour. |
| AccessBarrier | Allows physical access of vehicles to a charging site to be controlled. |
| AcDcConverter | Provides a variable DC current source to force energy directly into an EV battery stack, under tight control of the EV's battery management system. |
| AcPhaseSelector | Allows a specific AC phase to be selected (typically at EVSE tier) for single phase vehicle charging in order to lower overall (e.g. site) phase imbalance. |
| Actuator | A general purpose electro-mechanical output system, with optional completion tracking sensing. Each output should use a Variable instance key indicating the nature of the output. |
| AirCoolingSystem | Fans (or equivalent devices) used to provide cooling. |
| AreaVentilation | Fans (or equivalent devices) used to ensure that EVs that require ventilation during charging |
| BayOccupancySensor | Sensor (optical, ground loop, ultrasonic, etc.) to detect whether the associated parking/charging bay is physically vacant, or is occupied by a vehicle or other obstruction |
| BeaconLighting | Beacon Lighting to help EV drivers to locate nearby charging places, and/or to determine charging availability state, usually by color variation. |
| CableBreakawaySensor | A sensor that detects when a charging cable (captive or removable) has been forcibly pulled from the Charging Station. |
| CaseAccessSensor | Reports when an access door/panel is open |
| [ChargingStation](#chargingstation) | The entire Charging Station as a logical entity |
| ChargingStatusIndicator | The Charging Status Indicator, provides visible feedback to the user about the connection and charging status of an EVSE/Connector. This is commonly in the form of multi-colored lighting. |
| [ConnectedEV](#connectedev) | ConnectedEV is a component that represents a connected vehicle for which data is received via an ISO 15118 or CHAdeMO interface. The generic information that is received, is represented as variables of ConnectedEV. Any protocol-specific information is represented in variables of the ISO15118Ctrlr or CHAdeMOCtrlr component. |
| [Connector](#connector) | A means to connect an EV to a Charging Station with either a socket, an attached cable & inline connector, or any wireless power transfer device. |
| ConnectorHolsterRelease | A mechanism present in a connector holster to prevent the connector from being removed inappropriately: typically unlocks connector after authorization. |
| ConnectorHolsterSensor | A mechanism to report when a tethered cable connector has been removed from its normal stowage position. May be used for detection of connectors left un-holstered, and possible penalty billing. |
| ConnectorPlugRetentionLock | Locking mechanism to retain an inserted plug, both to prevent on-load disconnection, and to prevent theft of charging cables |
| ConnectorProtectionRelease | External protective mechanism (e.g. an external shutter or a connector holster lock mechanism) to prevent contact with conductors that may become 'live' under other failure modes |
| [Controller](#controller) | An embedded logic controller |
| ControlMetering | Energy, Power, Electricity meter, used to measure energy, current, voltages etc. |
| [CPPWMController](#cppwmcontroller) | Control Pilot PWM Controller: provides and senses the IEC 61851-1 / SAE J1772 low voltage DC and PWM signalling between an EVSE and EV over a control pilot line. |
| DataLink | Provides a communications link from a Charging Station to a CSMS. It may use fixed infrastructure, mobile telephony data services, WiFi, or other connectivity channels. |
| Display | Provides information and feedback to the user. |
| [DistributionPanel](#distributionpanel) | Defines the Distribution Panel, with it's fuses and connections to both Charging Stations and other Distribution Panel's. |
| ElectricalFeed | Represents an incoming electrical connection to a Charging Station, that may be a grid/distribution network connection, of a connection to local power generation and/or storage. Each electrical feed can record the electrical and other characteristics of that feed, including power rating, fusing, upstream metering, etc. When a Charging Station has more than one electrical feed, it must represent which feed supplies each EVSE, and which feed supplies the house load of the Charging Station itself. Simple Charging Stations with only a single electrical feed may omit all electrical feed information, in which case it is inferred that all power is supplied from a single feed, and what would otherwise be ElectricalFeed data (Variables) may be reported as being associated with the ChargingStation component. |
| ELVSupply | Represents the low voltage power supply (typically 12V DC and often other ELV voltages) that provides operating power for controllers, relays, and other electrical components. |
| EmergencyStopSensor | An 'Emergency Stop' button that should be pressed by the user or other nearby persons if serious faulty behavior is observed (e.g. smoke/flames from EV or Charging Station). |
| EnvironmentalLighting | Provides reporting/control of general illumination lighting in use at Charging Station. |
| EVRetentionLock | A locking mechanism on the EV side as a safety measure to prevent it being disconnected while high currents are flowing. |
| [EVSE](#evse) | The entire chain of components responsible for transporting energy from the incoming supply to the electric vehicle (or vice versa) |
| ExternalTemperatureSensor | Reports ambient air temperature |
| [FiscalMetering](#fiscalmetering) | Provides energy transfer readings that are the basis for billing. |
| FloodSensor | A sensor reporting whether the Charging Station is experiencing water ingress/pooling. |
| GroundIsolationProtection | An Isolation Tester as part of their own self-test mechanisms, to confirm the isolation of floating circuitry when no Evs are connected |
| Heater | Heater to ensure reliable operation in cold environments |
| HumiditySensor | Reports relative air humidity |
| LightSensor | Reports ambient light levels. |
| LiquidCoolingSystem | A liquid based cooling system, typically used to cool the connector cables of very high power Charging Stations. |
| LocalAvailabilitySensor | Accepts local signal inputs controlling whether new Charging Sessions can start and/or whether ongoing sessions should continue. Typically connected to a site/building power supply, to automatically report unavailability when closed. |
| LocalController | The entire Local Controller as a logical entity |
| [LocalEnergyStorage](#localenergystorage) | Energy storage |
| OverCurrentProtection | Protects equipment by disconnecting the electrical supply when the current drawn (on any phase) exceeds the rated value to a substantial degree. |
| OverCurrentProtectionRecloser | Recloser mechanism of an OverCurrentProtection to perform re-arm retries after a trip, or may be set for remotely controlled re-arming on command. |
| PowerContactor | Switches on and off the power to the EV after all authorization and safety requirements have been met. May have secondary contacts to report closure state. |
| RCD | A Residual Current Device (US: ground fault breaker) protects human life and/or downstream equipment by quickly detecting abnormal current flows (usually indicative in earth faults) in the Charging Station, cable, or EV during charging. |
| RCDRecloser | A motorized recloser mechanism of an RCD that may be configured to perform re-arm retries after a trip, or may be set for remotely controlled re-arming on command. |
| RealTimeClock | Represents realtime clock hardware that can maintain accurate date & time information in a Charging Station, even in the case of simultaneous CSMS uncontactability and power outages or resets. |
| ShockSensor | Measures impact forces/accelerations experienced, indicative of possible damage. |
| SpacesCountSignage | Electronic signage allowing a charging controller for a large charging facility to advertise counts of available spaces to passing traffic. |
| Switch | A general purpose electromechanical input device, with optional remote defaulting/resetting of values. Each input should use a Variable instance key indicating the nature of the input. |
| TemperatureSensor | Temperature sensor at a point inside the Charging Station, multiple sensing points for a single sensing controller. Multiple sensing points for a single sensing controller may be reported using distinct Variable instance keys. |
| TiltSensor | Measures Tilt angle from normal reference position (normally 90 degree vertical). |
| [TokenReader](#tokenreader) | An authorization token reader (e.g. RFID) |
| UpstreamProtectionTrigger | Circuitry designed to trigger the disconnection of power to the structure by an upstream protection device after a severe problem has been detected |
| UIInput | A logical input mechanism (e.g. set of buttons) that is part of a UI whose use may be communicated to the CSMS (in near real time). May support momentary inputs ('Operated') or modal state ('Active'). Multiple input sources should use explicit Variable instance keys (where the input function is key name). |
| VehicleIdSensor | Reports an identifier associated with a vehicle occupying a charging bay. The identifier may be a vehicle registration number via ANPR hardware, a VIN, or other local identifier of the vehicle based on medium range/active RFID, or any other relevant technology and result. |

## Variables by Component

> All 249 component/variable pairings, grouped by the component they belong to. **Generic** variables apply to any component. Each variable lists its required flag, datatype, unit, and instance where applicable.

> ⚠️ **Suspected OCA source defects (flag, not authoritative).** The OCA's component×variable appendix CSV (the source for the groups below) disagrees with the appendices document (Edition 3, appendices v1.4) in ways that look like errors in the CSV export. None are listed in the OCPP 2.0.1 errata (2024-06), so they appear **unreported**. Device-model variable names are **case-sensitive on the wire**, so verify against the official spec before relying on a spelling:

> - **Casing:** the groups below use `VehicleID` (ConnectedEV), but the appendix standardized-variable list uses `VehicleId` — the spelling below is the **deviant one** (same defect exists in the OCPP 2.1 appendix CSVs).
> - **Component missing from the Components table:** `CustomizationCtrlr` owns variables below but is absent from `components.csv`; the appendices document defines it in section 3.1.6 ("Logical Component responsible for configuration relating to custom vendor-specific implementations, using the DataTransfer message and CustomData extensions"). It is therefore missing from the [Components](#components) table above.
> - **Defined but absent here:** `ChargingCompleteBulk`, `ChargingCompleteFull`, `DepartureTime`, `EnergyCapacity`, `RemainingTimeBulk`, `RemainingTimeFull`, and `StateOfChargeBulk` exist in the OCA variable-definitions list but are mapped to no component in the matrix, so they do not appear below. Most are EV-session values that the appendices document maps to ISO 15118 / CHAdeMO data under the ConnectedEV component.

### AlignedDataCtrlr

**`Available`** — Required: no  ·  Type: boolean

If this variable reports a value of true, Clock-Aligned Data is supported.

**`Enabled`** — Required: no  ·  Type: boolean

If this variable reports a value of true, Clock-Aligned Data is enabled

**`Interval`** — Required: yes  ·  Type: integer  ·  Unit: s

Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the MeterValuesRequest message.

**`Measurands`** — Required: yes  ·  Type: MemberList

Clock-aligned measurand(s) to be included in MeterValuesRequest, every AlignedDataInterval seconds.

**`SendDuringIdle`** — Required: no  ·  Type: boolean

If set to true, the Charging Station SHALL NOT send clock aligned meter values when a transaction is ongoing.

**`SignReadings`** — Required: no  ·  Type: boolean

If set to true, the Charging Station SHALL include signed meter values in the SampledValueType in the MeterValuesRequest to the CSMS.

**`TxEndedInterval`** — Required: yes  ·  Type: integer  ·  Unit: s

Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the TransactionEventRequest (eventType = Ended) message.

**`TxEndedMeasurands`** — Required: yes  ·  Type: MemberList

Clock-aligned measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended), every SampledDataTxEndedInterval seconds from the start of the transaction.

### AuthCacheCtrlr

**`Available`** — Required: no  ·  Type: boolean

Authorization caching is available, but not necessarily enabled.

**`Enabled`** — Required: no  ·  Type: boolean

If set to true, Authorizaiton caching is enabled.

**`LifeTime`** — Required: no  ·  Type: integer

Indicates how long it takes until a token expires in the authorization cache since it is last used

**`Policy`** — Required: no  ·  Type: OptionList

Cache Entry Replacement Policy: least recently used, least frequently used, first in first out, other custom mechanism.

**`Storage`** — Required: no  ·  Type: integer  ·  Unit: B

Indicates the number of bytes currently used by the Authorization Cache. MaxLimit indicates the maximum number of bytes that can be used by the Authorization Cache.

**`DisablePostAuthorize`** — Required: no  ·  Type: boolean

When set to true this variable disables the behavior to request authorization for an idToken that is stored in the cache with a status other than Accepted, as stated in C10.FR.03 and C12.FR.05.

### AuthCtrlr

**`AdditionalInfoItemsPerMessage`** — Required: no  ·  Type: integer

Maximum number of AdditionalInfo items that can be sent in one message.

**`AuthorizeRemoteStart`** — Required: yes  ·  Type: boolean

Whether a remote request to start a transaction in the form of RequestStartTransactionRequest message should be authorized beforehand like a local action to start a transaction.

**`Enabled`** — Required: no  ·  Type: boolean

If set to false, then no authorization is done before starting a transaction or when reading an idToken. If an idToken was provided, then it will be put in the idToken field of the TransactionEventRequest. If no idToken was provided, then idToken in TransactionEventRequest will be left empty and type is set to NoAuthorization.

**`LocalAuthorizeOffline`** — Required: yes  ·  Type: boolean

Whether the Charging Station, when Offline, will start a transaction for locally-authorized identifiers

**`LocalPreAuthorize`** — Required: yes  ·  Type: boolean

Whether the Charging Station, when online, will start a transaction for locally-authorized identifiers without waiting for or requesting an AuthorizeResponse from the CSMS.

**`MasterPassGroupId`** — Required: no  ·  Type: string

IdTokens that have this id as groupId belong to the Master Pass Group. Meaning they can stop any ongoing transaction, but cannot start transactions.

**`OfflineTxForUnknownIdEnabled`** — Required: no  ·  Type: boolean

Support for unknown offline transactions.

**`DisableRemoteAuthorization`** — Required: no  ·  Type: boolean

When set to true this instructs the Charging Station to not issue any AuthorizationRequests, but only use Authorization Cache and Local Authorization List to determine validity of idTokens.

### CHAdeMOCtrlr

**`SelftestActive`** — Required: no  ·  Type: boolean

Self-test is active or self-test is started by setting to true.

**`CHAdeMOProtocolNumber`** — Required: no  ·  Type: integer

CHAdeMO protocol number (H'102.0)

**`VehicleStatus`** — Required: no  ·  Type: boolean

Vehicle status (H'102.5.3)

**`DynamicControl`** — Required: no  ·  Type: boolean

Vehicle is compatible with dynamic control (H'110.0.0)

**`HighCurrentControl`** — Required: no  ·  Type: boolean

Vehicle is compatible with high current control (H'110.0.1)

**`HighVoltageControl`** — Required: no  ·  Type: boolean

Vehicle is compatible with high voltage control (H'110.1.2)

**`AutoManufacturerCode`** — Required: no  ·  Type: integer

Auto manufacturer code (H'700.0)

### ChargingStation

**`AllowNewSessionsPendingFirmwareUpdate`** — Required: no  ·  Type: boolean

Indicates whether new sessions can be started on EVSEs, while Charging Station is waiting for all EVSEs to become Available in order to start a pending firmware update

**`AvailabilityState`** — Required: yes  ·  Type: OptionList

This variable reports current availability state for the ChargingStation

**`Available`** — Required: yes  ·  Type: boolean

Component exists

**`Model`** — Required: no  ·  Type: string

Charging station model as reported in BootNotification.

**`SupplyPhases`** — Required: yes  ·  Type: integer

Number of alternating current phases connected/available.

**`VendorName`** — Required: no  ·  Type: string

Charging station vendor name as reported in BootNotification.

### ClockCtrlr

**`DateTime`** — Required: yes  ·  Type: dateTime

Contains the current date and time

**`NextTimeOffsetTransitionDateTime`** — Required: no  ·  Type: dateTime

Date time of the next time offset transition.

**`NtpServerUri`** — Required: no  ·  Type: string

This contains the address of the NTP server.

**`NtpSource`** — Required: no  ·  Type: OptionList

When an NTP client is implemented, this variable can be used to configure the client

**`TimeAdjustmentReportingThreshold`** — Required: no  ·  Type: integer

If set, then time adjustments with an absolute value in seconds larger than this need to be reported as a security event SettingSystemTime

**`TimeOffset`** — Required: no  ·  Type: string

A Time Offset with respect to Coordinated Universal Time (aka UTC or Greenwich Mean Time) in the form of an [RFC3339] time (zone) offset suffix, including the mandatory “+” or “-“ prefix.

**`TimeSource`** — Required: yes  ·  Type: SequenceList

Via this variable, the Charging Station provides the CSMS with the option to configure multiple clock sources

**`TimeZone`** — Required: no  ·  Type: string

Configured current local time zone in the format: "Europe/Oslo", "Asia/Singapore" etc. For display purposes.

### ConnectedEV

**`ProtocolAgreed`** — Required: no  ·  Type: string

Information about uri and version that was agreed upon between EV and EVSE in the supportedAppProtocolReq message from ISO 15118. Example: urn:iso:15118:2:2013:MsgDef,2,0

**`ProtocolSupportedByEV`** — Required: no  ·  Type: string  ·  Instance: `<Priority>`

Information from the supportedAppProtocolReq message from ISO 15118. Each priority is given its own variable instance. Example: urn:iso:15118:2:2013:MsgDef,2,0

**`VehicleID`** — Required: no  ·  Type: string

EVCCID (from ISO 15118 SessionSetupReq)

### Connector

**`AvailabilityState`** — Required: no  ·  Type: OptionList

This variable reports current availability state for the Connector. Optional, because already reported in StatusNotification.

**`Available`** — Required: yes  ·  Type: boolean

Component exists

**`ChargeProtocol`** — Required: no  ·  Type: string

The Charging Control Protocol applicable to a Connector. CHAdeMO: CHAdeMO protocol, ISO15118: ISO15118 V2G protocol (wired or wireless) as used with CCS, CPPWM: IEC61851-1 / SAE J1772  protocol (ELV DC & PWM signalling via Control Pilot wire), Uncontrolled: No charging power management applies (e.g. Schuko socket), Undetermined: Yet to be determined (e.g. before plugged in), Unknown: Not determinable, NOTE: ChargeProtocol is distinct from and orthogonal to connectorType.

**`ConnectorType`** — Required: yes  ·  Type: string

A value of ConnectorEnumType (See part 2) plus additionally: cGBT, cChaoJi, OppCharge. Specific type of connector, including sub-variant information. Note: Distinct and orthogonal to Charging Protocol, Power Type, Phases.

**`SupplyPhases`** — Required: yes  ·  Type: integer

Number of alternating current phases connected/available.

### Controller

**`MaxMsgElements`** — Required: no  ·  Type: integer

Array of implementation-defined limits to the number of elements of specific type that the Charging Station can accept in one message.

### CPPWMController

**`State`** — Required: no  ·  Type: string

IEC 61851-1 states ("A" to "E")

### CustomizationCtrlr

**`CustomImplementationEnabled`** — Required: no  ·  Type: boolean  ·  Instance: `<vendorId>`

Custom implementation <vendorId> has been enabled.

### DeviceDataCtrlr

**`BytesPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `GetReport`

Maximum number of bytes in a message related to instance name: GetReport, GetVariables, SetVariables

**`BytesPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `GetVariables`

Maximum number of bytes in a message related to instance name: GetReport, GetVariables, SetVariables

**`BytesPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `SetVariables`

Maximum number of bytes in a message related to instance name: GetReport, GetVariables, SetVariables

**`ConfigurationValueSize`** — Required: no  ·  Type: integer

The limit to the following fields: SetVariableData.attributeValue and VariableCharacteristics.valueList. The max size of these values will always remain equal.

**`ItemsPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `GetReport`

Maximum number of ComponentVariable entries in message related to the instance name: GetReport, GetVariables, SetVariables

**`ItemsPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `GetVariables`

Maximum number of ComponentVariable entries in message related to the instance name: GetReport, GetVariables, SetVariables

**`ItemsPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `SetVariables`

Maximum number of ComponentVariable entries in message related to the instance name: GetReport, GetVariables, SetVariables

**`ReportingValueSize`** — Required: no  ·  Type: integer

The limit to the following fields: GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal.

**`ValueSize`** — Required: no  ·  Type: integer

Can be used to limit the following fields: SetVariableData.attributeValue, GetVariableResult.attributeValue, VariableAttribute.value, VariableCharacteristics.valueList and EventData.actualValue.

### DisplayMessageCtrlr

**`Available`** — Required: no  ·  Type: boolean

Whether display messages are supported.

**`DisplayMessages`** — Required: yes  ·  Type: integer

Amount of different messages that are currently configured in this Charging Station, via SetDisplayMessageRequest

**`Enabled`** — Required: no  ·  Type: boolean

Whether display messages are enabled.

**`PersonalMessageSize`** — Required: no  ·  Type: integer

Max size (in characters) of the personal message element of the IdTokenInfo data (0 specifies no personal data may be stored).

**`SupportedFormats`** — Required: yes  ·  Type: MemberList

List of message formats supported by this Charging Station.

**`SupportedPriorities`** — Required: yes  ·  Type: MemberList

List of the priorities supported by this Charging Station.

### DistributionPanel

**`ChargingStation`** — Required: no  ·  Type: string

Identity of charging station connected to the distribution panel.

**`DistributionPanel`** — Required: no  ·  Type: string

List of Distribution Panels InstanceNames connected to this LocalController.

**`Fuse`** — Required: no  ·  Type: integer  ·  Unit: A  ·  Instance: `<n>`

Fuse (index n) is the fuse for phase Ln in Ampere

### EVSE

**`AllowReset`** — Required: no  ·  Type: boolean

Can be used to announce that an EVSE can be reset individually

**`AvailabilityState`** — Required: yes  ·  Type: OptionList

This variable reports current availability state for the EVSE

**`Available`** — Required: yes  ·  Type: boolean

Component exists

**`EvseId`** — Required: no  ·  Type: string

The name of the EVSE in the string format as required by ISO 15118 and IEC 63119-2.

**`Power`** — Required: yes  ·  Type: decimal  ·  Unit: W, kW

The variableCharacteristic maxLimit, that holds the maximum power that this EVSE can provide, is required. The Actual value of the instantaneous (real) power is desired, but not required.

**`SupplyPhases`** — Required: yes  ·  Type: integer

Number of alternating current phases connected/available.

**`ISO15118EvseId`** — Required: no  ·  Type: string

The name of the EVSE in the string format as required by ISO 15118 and IEC 63119-2. Example: "DE*ICE*E*1234567890*1"

### FiscalMetering

**`EnergyExport`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Total energy transferred: e.g.  from EV during (ongoing or terminated) charging session (in wH by default)

**`EnergyExportRegister`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Cumulative export kWh register value, such as from a (certified) fiscal energy meter.

**`EnergyImport`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Total energy transferred.

**`EnergyImportRegister`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Cumulative export kWh register value, such as from a (certified) fiscal energy meter.

### ISO15118Ctrlr

**`CentralContractValidationAllowed`** — Required: no  ·  Type: boolean

If this variable exists and has the value true, then Charging Station can provide a contract certificate that it cannot validate, to the CSMS for validation as part of the AuthorizeRequest.

**`ContractValidationOffline`** — Required: yes  ·  Type: boolean

If this variable is true, then Charging Station will try to validate a contract certificate when it is offline

**`SeccId`** — Required: no  ·  Type: string

The ID of the SECC in string format as defined by ISO15118.

**`MaxScheduleEntries`** — Required: no  ·  Type: integer

Maximum number of allowed schedule periods.

**`RequestedEnergyTransferMode`** — Required: no  ·  Type: OptionList

The requested energy transfer mode.

**`RequestMeteringReceipt`** — Required: no  ·  Type: boolean

If true, then Charging Station shall request a metering receipt from EV.

**`CountryName`** — Required: no  ·  Type: string

The countryName of the SECC in the ISO 3166-1 format. It is used as the countryName (C) of the SECC leaf certificate. Example: "DE"

**`OrganizationName`** — Required: no  ·  Type: string

The organizationName of the CSO operating the charging station. It is used as the organizationName (O) of the SECC leaf certificate. Example: "John Doe Charging Services Ltd" Note: This value will usually be identical to SecurityCtrlr.OrganizationName, but it does not have to be.

**`PnCEnabled`** — Required: no  ·  Type: boolean

If this variable is true, then ISO 15118 plug and charge as described by use case C07 - Authorization using Contract Certificates is enabled. If this variable is false, then ISO 15118 plug and charge as described by use case C07 - Authorization using Contract Certificates is disabled.

**`V2GCertificateInstallationEnabled`** — Required: no  ·  Type: boolean

If this variable is true, then ISO 15118 V2G Charging Station certificate installation as described by use case A02 - Update Charging Station Certificate by request of CSMS and A03 - Update Charging Station Certificate initiated by the Charging Station is enabled.  If this variable is false, then ISO 15118 V2G Charging Station certificate installation as described by use case A02 - Update Charging Station Certificate by request of CSMS and A03 - Update Charging Station Certificate initiated by the Charging Station is disabled.

**`ContractCertificateInstallationEnabled`** — Required: no  ·  Type: boolean

If this variable is true, then ISO 15118 contract certificate installation/update as described by use case M01 - Certificate installation EV and M02 - Certificate Update EV is enabled. If this variable is false, then ISO 15118 contract certificate installation/update as described by use case M01 - Certificate installation EV and M02 - Certificate Update EV is disabled.

### LocalAuthListCtrlr

**`Available`** — Required: no  ·  Type: boolean

Local Authorization List is available.

**`BytesPerMessage`** — Required: yes  ·  Type: integer

Maximum number of bytes in a SendLocalList message.

**`Enabled`** — Required: no  ·  Type: boolean

If this variable exists and reports a value of true, Local Authorization List is enabled.

**`Entries`** — Required: yes  ·  Type: integer

Amount of IdTokens currently in the Local Authorization List

**`ItemsPerMessage`** — Required: yes  ·  Type: integer

Maximum number of records in SendLocalList

**`Storage`** — Required: no  ·  Type: integer  ·  Unit: B

Indicates the number of bytes currently used by the Local Authorization List. MaxLimit indicates the maximum number of bytes that can be used by the Local Authorization List.

**`DisablePostAuthorize`** — Required: no  ·  Type: boolean

When set to true this variable disables the behavior to request authorization for an idToken that is stored in the local authorization list with a status other than Accepted, as stated in C14.FR.03.

### LocalEnergyStorage

**`Capacity`** — Required: no  ·  Type: decimal  ·  Unit: Wh

Maximum storage capacity

### MonitoringCtrlr

**`Available`** — Required: no  ·  Type: boolean

Whether monitoring is available

**`BytesPerMessage`** — Required: no  ·  Type: integer  ·  Instance: `ClearVariableMonitoring`

Maximum number of bytes in a ClearVariableMonitoring message.

**`BytesPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `SetVariableMonitoring`

Maximum number of bytes in a SetVariableMonitoring message

**`Enabled`** — Required: no  ·  Type: boolean

Whether monitoring is enabled.

**`ItemsPerMessage`** — Required: no  ·  Type: integer  ·  Instance: `ClearVariableMonitoring`

Maximum number of IDs in a ClearVariableMonitoringRequest.

**`ItemsPerMessage`** — Required: yes  ·  Type: integer  ·  Instance: `SetVariableMonitoring`

Maximum number of setMonitoringData elements that can be sent in one setVariableMonitoringRequest message.

**`OfflineQueuingSeverity`** — Required: no  ·  Type: integer

When set and the Charging Station is offline, the Charging Station shall queue any notifyEventRequest messages triggered by a monitor with a severity number equal to or lower than the severity configured here.

**`MonitoringBase`** — Required: no  ·  Type: OptionList

Currently used monitoring base (readonly)

**`MonitoringLevel`** — Required: no  ·  Type: integer

Currently used monitoring level (readonly)

**`ActiveMonitoringBase`** — Required: no  ·  Type: OptionList

Shows the currently used MonitoringBase. Valid values according MonitoringBaseEnumType: All, FactoryDefault, HardwiredOnly.

**`ActiveMonitoringLevel`** — Required: no  ·  Type: integer

Shows the currently used MonitoringLevel. Valid values are severity levels of SetMonitoringLevelRequest: 0-9.

### OCPPCommCtrlr

**`ActiveNetworkProfile`** — Required: no  ·  Type: string

Indicates the configuration profile the station uses at that moment to connect to the network.

**`FileTransferProtocols`** — Required: yes  ·  Type: MemberList

List of supported file transfer protocols

**`HeartbeatInterval`** — Required: no  ·  Type: integer  ·  Unit: s

Interval of inactivity (no OCPP exchanges) with CSMS after which the Charging Station should send HeartbeatRequest.

**`MessageTimeout`** — Required: yes  ·  Type: integer  ·  Unit: s  ·  Instance: `Default`

MessageTimeout(Default) specifies after which time a message times out. It is configured in the network connection profile.

**`MessageAttemptInterval`** — Required: yes  ·  Type: integer  ·  Instance: `TransactionEvent`

MessageAttemptInterval(TransactionEvent) specifies long the Charging Station should wait before resubmitting a TransactionEventRequest message that the CSMS failed to process.

**`MessageAttempts`** — Required: yes  ·  Type: integer  ·  Instance: `TransactionEvent`

MessageAttempts(TransactionEvent) specifies how often the Charging Station should try to submit a TransactionEventRequest message when the CSMS fails to process it.

**`NetworkConfigurationPriority`** — Required: yes  ·  Type: string

A comma separated ordered list of the priority of the possible Network Connection Profiles.

**`NetworkProfileConnectionAttempts`** — Required: yes  ·  Type: integer

Specifies the number of connection attempts the Charging Station executes before switching to a different profile.

**`OfflineThreshold`** — Required: yes  ·  Type: integer  ·  Unit: s

When the offline period of a Charging Station exceeds the OfflineThreshold it is recommended to send a StatusNotificationRequest for all its Connectors.

**`PublicKeyWithSignedMeterValue`** — Required: no  ·  Type: OptionList

This Configuration Variable can be used to configure whether a public key needs to be sent with a signed meter value. Note, that the field is required, so it needs to be present as an empty string when the public key is not sent.

**`QueueAllMessages`** — Required: no  ·  Type: boolean

When this variable is set to true, the Charging Station will queue all message until they are delivered to the CSMS.

**`ResetRetries`** — Required: yes  ·  Type: integer

Number of times to retry a reset of the Charging Station when a reset was unsuccessful

**`RetryBackOffRandomRange`** — Required: no  ·  Type: integer

When the Charging Station is reconnecting, after a connection loss, it will use this variable as the maximum value for the random part of the back-off time

**`RetryBackOffRepeatTimes`** — Required: no  ·  Type: integer

When the Charging Station is reconnecting, after a connection loss, it will use this variable for the amount of times it will double the previous back-off time.

**`RetryBackOffWaitMinimum`** — Required: no  ·  Type: integer

When the Charging Station is reconnecting, after a connection loss, it will use this variable as the minimum back-off time, the first time it tries to reconnect.

**`UnlockOnEVSideDisconnect`** — Required: yes  ·  Type: boolean

When set to true, the Charging Station SHALL unlock the cable on the Charging Station side when the cable is unplugged at the EV. For an EVSE with only fixed cables, the mutability SHALL be ReadOnly and the actual value SHALL be false. For a charging station with fixed cables and sockets, the variable is only applicable to the sockets.

**`WebSocketPingInterval`** — Required: no  ·  Type: integer  ·  Unit: s

0 disables client side websocket Ping/Pong. In this case there is either no ping/pong or the server initiates the ping and client responds with Pong. Positive values are interpreted as number of seconds between pings. Negative values are not allowed.

**`FieldLength`** — Required: no  ·  Type: integer

This variable is used to report the length of <field> in <message> when it is larger than the length that is defined in the standard OCPP message schema.

### ReservationCtrlr

**`Available`** — Required: no  ·  Type: boolean

Whether reservation is supported.

**`Enabled`** — Required: no  ·  Type: boolean

Whether reservation is enabled.

**`NonEvseSpecific`** — Required: no  ·  Type: boolean

If this configuration variable is present and set to true: Charging Station supports Reservation where EVSE id is not specified.

### SampledDataCtrlr

**`Available`** — Required: no  ·  Type: boolean

If this variable reports a value of true, Sampled Data is supported

**`Enabled`** — Required: no  ·  Type: boolean

If this variable reports a value of true, Sampled Data is enabled.

**`SignReadings`** — Required: no  ·  Type: boolean

If set to true, the Charging Station SHALL include signed meter values in the TransactionEventRequest to the CSMS

**`TxEndedInterval`** — Required: yes  ·  Type: integer  ·  Unit: s

Interval between sampling of metering (or other) data, intended to be transmitted in the TransactionEventRequest (eventType = Ended) message.

**`TxEndedMeasurands`** — Required: yes  ·  Type: MemberList

Sampled measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended), every SampledDataTxEndedInterval seconds from the start of the transaction.

**`TxStartedMeasurands`** — Required: yes  ·  Type: MemberList

Sampled measurand(s) to be taken at the start of any transaction to be included in the meterValues field of the first TransactionEventRequest message send at the start of a transaction (eventType = Started)

**`TxUpdatedInterval`** — Required: yes  ·  Type: integer  ·  Unit: s

Interval between sampling of metering (or other) data, intended to be transmitted via TransactionEventRequest (eventType = Updated) messages

**`TxUpdatedMeasurands`** — Required: yes  ·  Type: MemberList

Sampled measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended)

**`RegisterValuesWithoutPhases`** — Required: no  ·  Type: boolean

If this variable reports a value of true, then meter values of measurand Energy.Active.Import.Register will only report the total energy over all phases without reporting the individual phase values. If this variable is absent or false, then the value for each phase is reported, possibly also with a total value (depending on the meter).

### SecurityCtrlr

**`AdditionalRootCertificateCheck`** — Required: no  ·  Type: boolean

Required for all security profiles except profile 1.

**`BasicAuthPassword`** — Required: no  ·  Type: passwordString

The basic authentication password is used for HTTP Basic Authentication.

**`CertificateEntries`** — Required: yes  ·  Type: integer

Amount of Certificates currently installed on the Charging Station

**`CertSigningRepeatTimes`** — Required: no  ·  Type: integer

Number of times to resend a SignCertificateRequest when CSMS does nor return a signed certificate.

**`CertSigningWaitMinimum`** — Required: no  ·  Type: integer  ·  Unit: s

Seconds to wait before generating another CSR in case CSMS does not return a signed certificate.

**`Identity`** — Required: no  ·  Type: identifierString

The Charging Station identity.

**`MaxCertificateChainSize`** — Required: no  ·  Type: integer

Limit of the size of the 'certificateChain' field from the CertificateSignedRequest

**`OrganizationName`** — Required: yes  ·  Type: string

The organization name of the CSO or an organization trusted by the CSO. This organization name is used to specify the subject field in the client certificate.

**`SecurityProfile`** — Required: yes  ·  Type: integer

The security profile used by the Charging Station.

### SmartChargingCtrlr

**`ACPhaseSwitchingSupported`** — Required: no  ·  Type: boolean

This variable can be used to indicate an on-load/in-transaction capability. If defined and true, this EVSE supports the selection of which phase to use for 1 phase AC charging.

**`Available`** — Required: no  ·  Type: boolean

Whether smart charging is supported.

**`Enabled`** — Required: no  ·  Type: boolean

Whether smart charging is enabled.

**`Entries`** — Required: yes  ·  Type: integer  ·  Instance: `ChargingProfiles`

Entries(ChargingProfiles) is the amount of Charging profiles currently installed on the Charging Station

**`ExternalControlSignalsEnabled`** — Required: no  ·  Type: boolean

Indicates whether a Charging Station should respond to external control signals that influence charging.

**`LimitChangeSignificance`** — Required: yes  ·  Type: decimal  ·  Unit: Percent

If at the Charging Station side a change in the limit in a ChargingProfile is lower than this percentage, the Charging Station MAY skip sending a NotifyChargingLimitRequest or a TransactionEventRequest message to the CSMS.

**`NotifyChargingLimitWithSchedules`** — Required: no  ·  Type: boolean

Indicates if the Charging Station should include the externally set charging limit/schedule in the message when it sends a NotifyChargingLimitRequest message.

**`PeriodsPerSchedule`** — Required: yes  ·  Type: integer

Maximum number of periods that may be defined per ChargingSchedule.

**`Phases3to1`** — Required: no  ·  Type: boolean

If defined and true, this Charging Station supports switching from 3 to 1 phase during a transaction

**`ProfileStackLevel`** — Required: yes  ·  Type: integer

Maximum acceptable value for stackLevel in a ChargingProfile. Since the lowest stackLevel is 0, this means that if SmartChargingCtrlr.ProfileStackLevel = 1, there can be at most 2 valid charging profiles per Charging Profile Purpose per EVSE.

**`RateUnit`** — Required: yes  ·  Type: MemberList

A list of supported quantities for use in a ChargingSchedule. Allowed values: 'A' and 'W

### TariffCostCtrlr

**`Available`** — Required: no  ·  Type: boolean  ·  Instance: `Tariff`

Instance Tariff: Whether tariffs are supported.

**`Available`** — Required: no  ·  Type: boolean  ·  Instance: `Cost`

Instance Cost: Wheter costs are supported.

**`Currency`** — Required: yes  ·  Type: string

Currency used by this Charging Station in a ISO 4217 [ISO4217] formatted currency code.

**`Enabled`** — Required: no  ·  Type: boolean  ·  Instance: `Tariff`

Instance Tariff: Whether tariffs are enabled.

**`Enabled`** — Required: no  ·  Type: boolean  ·  Instance: `Cost`

Instance Cost: Wheter costs are enabled.

**`TariffFallbackMessage`** — Required: yes  ·  Type: string

Message (and/or tariff information) to be shown to an EV Driver when there is no driver specific tariff information available.

**`TotalCostFallbackMessage`** — Required: yes  ·  Type: string

Message to be shown to an EV Driver when the Charging Station cannot retrieve the cost for a transaction at the end of the transaction.

### TokenReader

**`Token`** — Required: no  ·  Type: string

String of bytes representing an ID token.

**`TokenType`** — Required: no  ·  Type: OptionList

Type of Token. Value is one of IdTokenEnumType.

### TxCtrlr

**`ChargingTime`** — Required: no  ·  Type: decimal  ·  Unit: s

Time from earliest to latest substantive energy transfer

**`EVConnectionTimeOut`** — Required: yes  ·  Type: integer  ·  Unit: s

Interval from between "starting" of a transaction until incipient transaction is automatically canceled, due to failure of EV driver to (correctly) insert the charging cable connector(s) into the appropriate socket(s).

**`MaxEnergyOnInvalidId`** — Required: no  ·  Type: integer

Maximum amount of energy in Wh delivered when an identifier is deauthorized by the CSMS after start of a transaction.

**`StopTxOnEVSideDisconnect`** — Required: yes  ·  Type: boolean

When set to true, the Charging Station SHALL deauthorize the transaction when the cable is unplugged from the EV.

**`StopTxOnInvalidId`** — Required: yes  ·  Type: boolean

Whether the Charging Station will deauthorize an ongoing transaction when it receives a non- Accepted authorization status in TransactionEventResponse for this transaction.

**`TxBeforeAcceptedEnabled`** — Required: no  ·  Type: boolean

Allow charging before having received a BootNotificationResponse with RegistrationStatus: Accepted.

**`TxStartPoint`** — Required: yes  ·  Type: MemberList

Defines when the Charging Station starts a new transaction

**`TxStopPoint`** — Required: yes  ·  Type: MemberList

Defines when the Charging Station ends a transaction

### Generic variables

Variables that apply generically to any component, not bound to one specific component.

**`ACCurrent`** — Required: no  ·  Type: decimal  ·  Unit: A

RMS AC Current (in amperes). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average of all per-phase readings and written values are common per-phase settings. Example(s): ChargingStation: Total AC current consumption (all EVSE’s, ancillaries), EVSE: Total current consumed by EVSE: includes losses (AC->DC) and EVSE specific ancillaries (e.g. fans), ElectricalFeed: Inflow AC current on feed

**`Active`** — Required: no  ·  Type: boolean

Component is in its non-resting / active state: e.g: On, Engaged, Locked. Some Components may have secondary functions that have corresponding Active Variables with an explicit Variable instance., Note: Monitoring of changes in the Active state of any Component can be specified by setting Delta monitoring on the boolean value with a delta values of 1. Setting/clearing an Active Variable activates/stops the associated functionality, where remotely controllable. Only components that are Available and Enabled can be in the Active state.

**`ACVoltage`** — Required: no  ·  Type: decimal  ·  Unit: V

RMS AC Voltage (in volts). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average ofall per-phase readings and written values are common per-phase settings. Example(s): ElectricalFeed: Input Voltage

**`AllowReset`** — Required: no  ·  Type: boolean

Component can be reset.

**`Angle`** — Required: no  ·  Type: decimal  ·  Unit: Deg

Angle(s) relative to normal/design idle position. Multiple Variable instance values may be used to indicate angular position in multiple axes (e.g. Left-Right, Forward-Back).

**`Attempts`** — Required: no  ·  Type: integer

Number of attempts (INCLUDING the original attempt) in the last successful or attempted, cycle of operation. Applies typically to self-monitoring motorized electro-mechanical equipment, etc. {Null}: Unknown, 0: Not Attempted/Not allowed, 1: Single attempt/No retries [allowed], 2-N: [up to] N tries [allowed]

**`Available`** — Required: no  ·  Type: boolean

The Component exists and is locally configured/wired for use, but might not be (remotely) Enabled.

**`Certificate`** — Required: no  ·  Type: string

Digital Certificate (in Base64 encoding)

**`Color`** — Required: no  ·  Type: string

Standard 24 bit hexadecimal RGB values. Reg Green Blue color intensity, expressed as standard 24 bit hexadecimal RGB values: 3  00-FF (0-255), in order RRGGBB). E.g. 000000: Black, FF0000: Red, 00FF00: Green, 0000FF: Blue, FFFF00:Yellow, FFFFFF: White, 008000: Medium intensity green.

**`Complete`** — Required: no  ·  Type: boolean

Component operation cycle has completed. Used only in event notifications, where it is always true.

**`ConnectedTime`** — Required: no  ·  Type: decimal  ·  Unit: s

Time since logical connection established

**`Count`** — Required: no  ·  Type: integer

General purpose integer count variable for Component state reporting

**`CurrentImbalance`** — Required: no  ·  Type: decimal  ·  Unit: Percent

Percentage current imbalance in an AC three phase supply.

**`DataText`** — Required: no  ·  Type: string

Text associated with a Component, e.g. a Display.

**`DateTime`** — Required: no  ·  Type: dateTime

Point in time value, in [RFC3339] datetime format. Time zone optional.

**`DCCurrent`** — Required: no  ·  Type: decimal  ·  Unit: A

DC Current (in amperes). May be an instantaneous measurement, or a period average, depending on context/equipment.

**`DCVoltage`** — Required: no  ·  Type: decimal  ·  Unit: V

DC Voltage (volts). May be an instantaneous measurement, or a period average, depending on context/equipment.

**`ECVariant`** — Required: no  ·  Type: string

Production series variants reflecting internal design changes or sub-component substitutions not affecting external functionality.

**`Enabled`** — Required: no  ·  Type: boolean

The Component is Enabled for operation. For Available components that cannot be selectively (remotely) enabled / disabled, this value is always true. Note: Available cannot be false of Enabled is true, so during inventory reporting, Enabled=1 also logically states Available=true

**`Energy`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Energy quantity (in Wh) for reporting/configuring values related to stored energy (i.e. not transferred energy).

**`Entries`** — Required: no  ·  Type: integer

General purpose variable for reporting/managing numbers of entries in repetitive data structures. maxLimit characteristic reports maximum possible entries.

**`Fallback`** — Required: no  ·  Type: boolean

Component is operating in a fallback, or backup mode. In inventory reports, a Value of 1 for the maxLimit characteristic indicates that the component can enter a fallback state (i.e. a fallback mode is present).

**`FanSpeed`** — Required: no  ·  Type: decimal  ·  Unit: RPM

Fan Speed (in RPM). A value of 0 represents stopped/stalled. An empty value indicates that fan speed cannot be read.

**`FirmwareVersion`** — Required: no  ·  Type: string

Version number of firmware.

**`Force`** — Required: no  ·  Type: decimal  ·  Unit: N

Reports (impact) force/ acceleration values (estimates) in one or more directions, in units of Newtons or “g”. Multiple force readings in different (orthogonal) dimensions may be reported using Variable instance values, such as Down, Right, Forward.

**`Formats`** — Required: no  ·  Type: MemberList

List of message formats supported by this Charging Station. Possible values: ASCII, HTML, URI, UTF-8.

**`Frequency`** — Required: no  ·  Type: decimal  ·  Unit: Hz

Frequency of AC power, signal, or component operation.

**`FuseRating`** — Required: no  ·  Type: decimal  ·  Unit: A

Current rating of a fuse/breaker. Variable instances keyed by phase identifier (L1/L2/L3/N).

**`Height`** — Required: no  ·  Type: decimal  ·  Unit: m

Height above(+)/below(-) reference level (ground level unless context demands otherwise).

**`Humidity`** — Required: no  ·  Type: decimal  ·  Unit: RH

The relative humidity in %.

**`Hysteresis`** — Required: no  ·  Type: decimal  ·  Unit: Percent

Specifies the width of a 'dead band' (as a percentage of the threshold) around the central value of a threshold setting (e.g. MinSet, MaxSet, monitor thresholds) to avoid repeated triggering when the measured quantity lies close to the threshold and is subject to small variations.

**`ICCID`** — Required: no  ·  Type: string

ICCID (Integrated Circuit Card IDentifier) of mobile data SIM card.

**`Impedance`** — Required: no  ·  Type: decimal  ·  Unit: Ohm

Impedance: Primary value is real (resistive only) impedance. Where a complex impedance is to be reported, the imaginary part (reactance) must be represented with a separate Variable instance value of 'reactance'. Reactance values are expressed at the (nominal) relevant operating frequency of the Component (e.g. 50/60Hz for mains electricity feed).

**`IMSI`** — Required: no  ·  Type: string

IMSI (International Mobile Subscriber Identity) number of mobile data SIM card

**`Interval`** — Required: no  ·  Type: integer  ·  Unit: s

Minimum Interval (in seconds) between (attempted) operations.

**`Length`** — Required: no  ·  Type: decimal  ·  Unit: m

General Purpose linear distance measure.

**`Light`** — Required: no  ·  Type: decimal  ·  Unit: lx

(Ambient) light level. The value is in Lux.

**`Manufacturer`** — Required: no  ·  Type: string

Component Manufacturer name

**`Message`** — Required: no  ·  Type: string

Specific stored message for display.

**`MinimumStatusDuration`** — Required: no  ·  Type: integer  ·  Unit: s

Minimum duration that a Charging Station or EVSE status is stable before StatusNotificationRequest is sent to the CSMS.

**`Mode`** — Required: no  ·  Type: string

Operating mode string from among valid options (communicated by OptionList, etc. during capability/configuration  discovery).

**`Model`** — Required: no  ·  Type: string

Manufacturer's Model code/number of Component, including suffixes etc. to identify functional, regional or linguistic variation, but NOT engineering change level internal 				variation not affecting external behaviour, etc.

**`NetworkAddress`** — Required: no  ·  Type: string

Current network address of a Component.

**`Operated`** — Required: no  ·  Type: boolean

The Component operated in an instantaneous, transient, or immediately self-resetting pattern. Used only in event notifications, where it is always true.

**`OperatingTimes`** — Required: no  ·  Type: string

Recurring operating times in iCalendar RRULE format.

**`Overload`** — Required: no  ·  Type: boolean

Component is in Overload state.

**`Percent`** — Required: no  ·  Type: decimal  ·  Unit: Percent

Generic dimensionless value reporting/setting value.

**`PhaseRotation`** — Required: no  ·  Type: OptionList

The phase wiring of Component, relative to it's upstream feed Component/device. This variable describes the phase rotation of a Component relative to its parent Component, using a three letter string consisting of the letters: R, S, T and x. The letter 'R' can be identified as phase 1 (L1), 'S' as phase 2 (L2), 'T' as phase 3 (L3). The lower case 'x' is used to designate a phase that is not connected. An empty string means that phase rotation is not applicable or not known.

**`PostChargingTime`** — Required: no  ·  Type: decimal  ·  Unit: s

Elapsed time in seconds since last substantive energy transfer

**`Power`** — Required: no  ·  Type: decimal  ·  Unit: W, kW

Instantaneous (real) Power (measured/calculated, including power factor for AC). Where a component (e.g. AC to DC Power Converter) has multiple power measurements, the default (unkeyed) instance is “input” power.

**`Problem`** — Required: no  ·  Type: boolean

Component itself has a 'Problem' condition that impacts in any significant way on its normal operation. By definition, 'Problem' state includes (logical OR) 'Fault' state. 'Problem' specifically INCLUDES inability to operate that is propagated (up/down/sideways) from any other associated/connected/containing/contained Component.

**`Protecting`** — Required: no  ·  Type: boolean

Applies to 'sensor' type Components that have an associated protection capability, whereby they can  disconnect power (e.g. using the main PowerContactor) if the sensed quantity is outside preset/configured limits. If Protecting is true, the Component is actively preventing/interrupting charging.

**`SerialNumber`** — Required: no  ·  Type: string

Serial number of Component.

**`SignalStrength`** — Required: no  ·  Type: decimal  ·  Unit: dBm

(Radio/Wired/Optical) data signal strength, in ASU (typically 0-31 or 99 for unknown). Or dbmW (typically -140 to -50).

**`State`** — Required: no  ·  Type: string

A state code or name identifier string, to allow the internal state of  components to be reported and/or  controlled

**`StateOfCharge`** — Required: no  ·  Type: decimal  ·  Unit: Percent

Energy Storage Device (e.g. battery) state of charge, expressed as a percentage of nominal design 0-100% operating range. Note: Values below or above 0-100% are possible and represent over discharged/charged states.

**`Storage`** — Required: no  ·  Type: integer  ·  Unit: B

In bytes. Amount of storage occupied. Storage(maxLimit) specifies absolute limit Storage(MaxSet) restricts usage to specified Max, if supported.

**`SupplyPhases`** — Required: no  ·  Type: integer

Number of alternating current phases connected/available. 1 or 3 for AC, 0 means DC (no alternating phases). Null value indicates that the number of phases (e.g. in use) is unknown.

**`Suspending`** — Required: no  ·  Type: boolean

If Suspending is true, the Component can is currently suspending charging.

**`Suspension`** — Required: no  ·  Type: boolean

Applies to 'sensor' type Components that have a charging suspension capability, typically for safety or equipment protection reasons. If Suspension is true, the component can suspend charging when the sensed quantity is outside preset/configured limits.

**`Temperature`** — Required: no  ·  Type: decimal  ·  Unit: Celsius, Fahrenheit

Temperature(s) of component (in Celsius, by default). Components may have multiple indexed temperature sensors.

**`Time`** — Required: no  ·  Type: dateTime

Point in time value, in ISO 8601 datetime format. Time zone optional.

**`Timeout`** — Required: no  ·  Type: decimal  ·  Unit: s

Generic timeout value for Component operation (in seconds).

**`Tries`** — Required: no  ·  Type: integer

Number of attempts done by a Component.

**`Tripped`** — Required: no  ·  Type: boolean

Single-shot device requires explicit intervention to re-prime/activate to normal.

**`VendorName`** — Required: no  ·  Type: string

Vendor or manufacturer of component.

**`VersionDate`** — Required: no  ·  Type: dateTime

Version date of component in [RFC3339] format.

**`VersionNumber`** — Required: no  ·  Type: string

Version number of hardware

**`VoltageImbalance`** — Required: no  ·  Type: decimal  ·  Unit: Percent

Percentage voltage imbalance in three phase supply.
