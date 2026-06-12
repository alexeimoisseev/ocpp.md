# OCPP 2.1 — Device Model Reference

> **Source:** OCA OCPP 2.1 appendix CSVs (`components.csv`, `dm_components_vars.csv`). Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md). These are the **standardized** component and variable names referenced by free-form `name` fields in `GetVariables`/`SetVariables`/`GetReport`. Vendors may extend with optional custom components/variables.

## Components (82)

> Component names link to their variables in [Variables by Component](#variables-by-component) below (components with no component-specific variables use only generic variables).

| Component | Description |
| --- | --- |
| [ACDERCtrlr](#acderctrlr) | Responsible for configuration relating to DER capabilities that the EVSE of the Charging Station can emulate by using ISO 15118-20 ChargeLoop messages to control the inverter in the EV. The component is located at the EVSE level, since it represents the DER capabilities of the EVSE. |
| [AlignedDataCtrlr](#aligneddatactrlr) | Logical Component responsible for configuration relating to the reporting of clock-aligned meter data. |
| [AuthCacheCtrlr](#authcachectrlr) | Logical Component responsible for configuration relating to the use of a local cache for authorization for Charging Station use. |
| [AuthCtrlr](#authctrlr) | Logical Component responsible for configuration relating to the use of authorization for Charging Station use. |
| [BatterySwapCtrlr](#batteryswapctrlr) | Responsible for configuration relating to Battery swapping. |
| [CHAdeMOCtrlr](#chademoctrlr) | A CHAdeMO Controller component communicates with an EV using the wired CANbus protocol to exchange information and control charging using the CHAdeMO protocol |
| [ClockCtrlr](#clockctrlr) | Provides a means to configure management of time tracking by Charging Station. |
| [CustomizationCtrlr](#customizationctrlr) | Responsible for configuration relating to custom vendor-specific implementations, like the DataTransfer message and CustomData extensions or CustomTriggers. |
| [DCDERCtrlr](#dcderctrlr) | Responsible for configuration relating to DER capabilities of the DC inverter of the EVSE in the Charging Station. The component is located at the EVSE level, since it represents the DER capabilities, also referred to as nameplate information, of the EVSE. |
| [DeviceDataCtrlr](#devicedatactrlr) | Logical Component responsible for configuration relating to the exchange and storage of Charging Station Device Model data. |
| [DisplayMessageCtrlr](#displaymessagectrlr) | Logical Component responsible for configuration relating to the display of messages to Charging Station users. |
| [ISO15118Ctrlr](#iso15118ctrlr) | Communicates with an EV to exchange information and control charging using the ISO 15118 protocol. |
| [LocalAuthListCtrlr](#localauthlistctrlr) | Logical Component responsible for configuration relating to the use of Local Authorization Lists for Charging Station use. |
| [MonitoringCtrlr](#monitoringctrlr) | Logical Component responsible for configuration relating to the exchange of monitoring event data. |
| [PaymentCtrlr](#paymentctrlr) | Logical Component responsible for configuration relating to payment terminals. |
| [OCPPCommCtrlr](#ocppcommctrlr) | Logical Component responsible for configuration relating to information exchange between Charging Station and CSMS. |
| [ReservationCtrlr](#reservationctrlr) | Logical Component responsible for configuration relating to reservations. |
| [SampledDataCtrlr](#sampleddatactrlr) | Logical Component responsible for configuration relating to the reporting of sampled meter data. |
| [SecurityCtrlr](#securityctrlr) | Logical Component responsible for configuration relating to security of communications between Charging Station and CSMS. |
| [SmartChargingCtrlr](#smartchargingctrlr) | Logical Component responsible for configuration relating to smart charging. |
| [TariffCostCtrlr](#tariffcostctrlr) | Logical Component responsible for configuration relating to tariff and cost display. |
| [TxCtrlr](#txctrlr) | Logical Component responsible for configuration relating to transaction characteristics and behaviour. |
| [V2XChargingCtrlr](#v2xchargingctrlr) | Responsible for configuration relating to V2X charging/discharging. This component exists on the EVSE tier hierarchy. |
| [WebPaymentsCtrlr](#webpaymentsctrlr) | Responsible for configuration of a dynamic QR code for ad hoc payments. |
| AccessBarrier | Allows physical access of vehicles to a charging site to be controlled. |
| AcDcConverter | Provides a variable DC current source to force energy directly into an EV battery stack, under tight control of the EV's battery management system. |
| AcPhaseSelector | Allows a specific AC phase to be selected (typically at EVSE tier) for single phase vehicle charging in order to lower overall (e.g. site) phase imbalance. |
| Actuator | A general purpose electro-mechanical output system, with optional completion tracking sensing. Each output should use a Variable instance key indicating the nature of the output. |
| AirCoolingSystem | Fans (or equivalent devices) used to provide cooling. |
| AreaVentilation | Fans (or equivalent devices) used to ensure that EVs that require ventilation during charging |
| [BatteryCartridge](#batterycartridge) | BatteryCartridge represents the battery cartridge that is currently inserted into the EVSE of a battery swap station |
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
| Controller | An embedded logic controller |
| ControlMetering | Energy, Power, Electricity meter, used to measure energy, current, voltages etc. |
| [CPPWMController](#cppwmcontroller) | Control Pilot PWM Controller: provides and senses the IEC 61851-1 / SAE J1772 low voltage DC and PWM signalling between an EVSE and EV over a control pilot line. |
| DataLink | Provides a communications link from a Charging Station to a CSMS. It may use fixed infrastructure, mobile telephony data services, WiFi, or other connectivity channels. |
| Display | Provides information and feedback to the user. |
| DistributionPanel | Defines the Distribution Panel, with it's fuses and connections to both Charging Stations and other Distribution Panel's. |
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
| [NetworkConfiguration](#networkconfiguration) | The instances of component NetworkConfiguration represent network connection configurations. |
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

> All 438 component/variable pairings, grouped by the component they belong to. **Generic** variables apply to any component. Each variable lists its required flag, datatype, unit, and instance where applicable.

> ⚠️ **Suspected OCA source defects (flag, not authoritative).** The OCA's component×variable appendix table (the source for the groups below) disagrees with its separate standardized-variable definitions list in ways that look like errors in the source data. None are listed in the OCPP 2.1 errata (2026-04), so they appear **unreported** (spec checked: Edition 2, 2025-12-03 — published, not draft). Device-model variable names are **case-sensitive on the wire**, so verify against the official spec before relying on a spelling:

> - **Casing:** the groups below use `TargetSoC` (BatterySwapCtrlr) and `VehicleID` (ConnectedEV), but the Part 2 prose / Appendix 3.2.13 and the standardized-variable list use `TargetSoc` and `VehicleId` — the spellings below are the **deviant ones**.
> - **Name mismatch (same concept, different name):** `NotificationDelay` below (ISO15118Ctrlr) is `NotificationMaxDelay` in the variable-definitions list; `SupportedIdTokenType` below (AuthCtrlr) is `SupportedIdTokenTypes` there.
> - **Defined but absent here:** `EnergyCapacity` and `Present` exist in the OCA variable-definitions list but are mapped to no component, so they do not appear below; both read like generic variables (cf. `Available`/`Enabled`).

### ACDERCtrlr

**`ModesSupported`** — Required: yes  ·  Type: MemberList

Indication of support for each control mode function

### AlignedDataCtrlr

**`Available`** — Required: no  ·  Type: boolean

If this variable reports a value of true, Clock-Aligned Data is supported.

**`Enabled`** — Required: no  ·  Type: boolean

If this variable reports a value of true, Clock-Aligned Data is enabled

**`Interval`** — Required: yes  ·  Type: integer  ·  Unit: s

Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the MeterValuesRequest or TransactionEventRequest message.

**`Measurands`** — Required: yes  ·  Type: MemberList

Clock-aligned measurand(s) to be included in MeterValuesRequest or TransactionEventRequest, every AlignedDataInterval seconds.

**`SendDuringIdle`** — Required: no  ·  Type: boolean

If set to true, the Charging Station SHALL NOT send clock aligned meter values when a transaction is ongoing.

**`SignReadings`** — Required: no  ·  Type: boolean

If set to true, the Charging Station SHALL include signed meter values in the SampledValueType in theTransactionEventRequest(Ended).

**`SignUpdatedReadings`** — Required: no  ·  Type: boolean

If set to true, the Charging Station SHALL include signed meter values in the SampledValueType in theTransactionEventRequest(Updated).

**`TxEndedInterval`** — Required: yes  ·  Type: integer  ·  Unit: s

Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the TransactionEventRequest (eventType = Ended) message.

**`TxEndedMeasurands`** — Required: yes  ·  Type: MemberList

Clock-aligned measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended), every SampledDataTxEndedInterval seconds from the start of the transaction.

**`UpstreamInterval`** — Required: no  ·  Type: integer  ·  Unit: s

Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the MeterValuesRequest message for location `Upstream` only.

**`UpstreamMeasurands`** — Required: no  ·  Type: MemberList

Clock-aligned measurand(s) to be included in MeterValuesReques for location `Upstream` only.

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

**`SupportedIdTokenType`** — Required: no  ·  Type: MemberList

The subset of the list of supported IdTokenTypes as defined in Appendix 7. "Standardized values for enumerations as string: IdTokenEnumStringType", that is supported by the Charging Station.

### BatteryCartridge

**`SoC`** — Required: no  ·  Type: integer  ·  Unit: %

The component BatteryCartridge refers to the battery that is inserted at the EVSE. The variable SoC represents current state of charge as a percentage from 0..100.

**`SoH`** — Required: no  ·  Type: integer  ·  Unit: %

The component BatteryCartridge refers to the battery that is inserted at the EVSE. The variable SoH represents current state of health as a value from 0..100.

**`WorkingMode`** — Required: no  ·  Type: OptionList

This variable represents the current working mode of the battery.

### BatterySwapCtrlr

**`TargetSoC`** — Required: no  ·  Type: integer  ·  Unit: %

The state of charge that a battery must have in order to be eligible for swapping.

**`MaxSoc`** — Required: no  ·  Type: integer  ·  Unit: %

The maximum state of charge that a battery will be charged to.

**`IdToken`** — Required: no  ·  Type: string

The idToken that is used for charging transactions of swap batteries.

**`Timeout`** — Required: no  ·  Type: integer  ·  Unit: s  ·  Instance: `In`

imeout in seconds in which a set of batteries must be inserted after successful authorization.

**`Timeout`** — Required: no  ·  Type: integer  ·  Unit: s  ·  Instance: `Out`

Timeout in seconds in which the set of batteries that is offered by Charging Station to take out in exchange for the inserted set of batteries must be removed.

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

**`ActiveTransactionId`** — Required: no  ·  Type: string

This variable for the ChargingStation component contains a comma-separated list of transaction IDs actively running on the Charging Station.

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

A Time Offset with respect to Coordinated Universal Time (aka UTC or Greenwich Mean Time) in the form of an [RFC3339] time (zone) offset suffix, including the mandatory + or - prefix.

**`TimeSource`** — Required: yes  ·  Type: SequenceList

Via this variable, the Charging Station provides the CSMS with the option to configure multiple clock sources

**`TimeZone`** — Required: no  ·  Type: string

Configured current local time zone in the format: "Europe/Oslo", "Asia/Singapore" etc. For display purposes.

### ConnectedEV

**`ProtocolAgreed`** — Required: V2X  ·  Type: string

Information about uri and version that was agreed upon between EV and EVSE in the supportedAppProtocolReq message from ISO 15118. Example: urn:iso:15118:2:2013:MsgDef,2,0

**`ProtocolSupportedByEV`** — Required: V2X  ·  Type: string  ·  Instance: `<Priority>`

Information from the supportedAppProtocolReq message from ISO 15118. Each priority is given its own variable instance. Example: urn:iso:15118:2:2013:MsgDef,2,0

**`VehicleID`** — Required: V2X  ·  Type: string

EVCCID (from ISO 15118 SessionSetupReq)

**`VehicleCertificate`** — Required: V2X  ·  Type: string  ·  Instance: `Leaf`

The PEM encoded X.509 Leaf certificate of the vehicle certificate chain

**`VehicleCertificate`** — Required: V2X  ·  Type: string  ·  Instance: `SubCA1`

The PEM encoded X.509 Intermediate certificate of the vehicle certificate chain

**`VehicleCertificate`** — Required: V2X  ·  Type: string  ·  Instance: `SubCA2`

The PEM encoded X.509 Intermediate certificate of the vehicle certificate chain

**`VehicleCertificate`** — Required: V2X  ·  Type: string  ·  Instance: `Root`

The PEM encoded X.509 Root certificate of the vehicle certificate chain

**`ACCurrent(Min/MaxSet)`** — Required: no  ·  Type: decimal  ·  Unit: A

EV min/max AC current

**`DCCurrent(Min/MaxSet)`** — Required: no  ·  Type: decimal  ·  Unit: A

EV min/max DC current

**`DCCurrent(Target)`** — Required: no  ·  Type: decimal  ·  Unit: V

EV target current from DC_ChargeLoopReq

**`DCVoltage(Min/MaxSet)`** — Required: no  ·  Type: decimal  ·  Unit: V

EV min/max DC voltage

**`DCVoltage(Target)`** — Required: no  ·  Type: decimal  ·  Unit: V

EV target voltage from DC_ChargeLoopReq

**`Power(MaxSet)`** — Required: no  ·  Type: decimal  ·  Unit: W

EV max power limit

**`DischargePower(MaxSet)`** — Required: no  ·  Type: decimal  ·  Unit: W

EV max discharge power limit

**`EnergyImport(MaxSet)`** — Required: no  ·  Type: decimal  ·  Unit: Wh

EV energy capacity / maximum energy request

**`EnergyImport(MinSet)`** — Required: no  ·  Type: decimal  ·  Unit: Wh

EV minimum energy request

**`EnergyImport(Target)`** — Required: no  ·  Type: decimal  ·  Unit: Wh

EV target energy request

**`BatteryCapacity`** — Required: no  ·  Type: decimal  ·  Unit: Wh

EV battery capacity

**`DepartureTime`** — Required: no  ·  Type: DateTime

EV planned departure time

**`RemainingTimeBulk`** — Required: no  ·  Type: integer  ·  Unit: s

Remaining time to bulk SoC

**`RemainingTimeFull`** — Required: no  ·  Type: integer  ·  Unit: s

Remaining time to full SoC

**`StateOfChargeBulk`** — Required: no  ·  Type: integer  ·  Unit: %

Defined % for bulk SoC

**`StateOfCharge(MaxSet)`** — Required: no  ·  Type: integer  ·  Unit: %

Defined % for full SoC

**`StateOfCharge`** — Required: no  ·  Type: integer  ·  Unit: %

Current SoC

**`ChargingCompleteBulk`** — Required: no  ·  Type: boolean

Charging to bulk SoC is complete

**`ChargingCompleteFull`** — Required: no  ·  Type: boolean

Charging to full SoC is complete

**`ChargingState`** — Required: no  ·  Type: OptionList

EVTerminationCode to signal error condition

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

**`SlotStatus`** — Required: no  ·  Type: OptionList

Battery slot status of swapping station: Open, Locked, Faulted.

### CPPWMController

**`State`** — Required: no  ·  Type: string

IEC 61851-1 states ("A" to "E")

### CustomizationCtrlr

**`CustomImplementationEnabled`** — Required: no  ·  Type: boolean  ·  Instance: `<vendorId>`

Custom implementation <vendorId> has been enabled.

**`CustomTriggers`** — Required: no  ·  Type: MemberList

This variable defines the names of custom triggers that Charging Station supports in a customTrigger field of TriggerMessageRequest.

### DataCollector

**`Enabled`** — Required: no  ·  Type: boolean

This variable must be set to True in order to activate the DataCollector.

**`DateTime`** — Required: no  ·  Type: DateTime  ·  Instance: `Start`

If _Enabled_ the DataCollector will sample measurandes from SampledMeasurands as long as time >= DateTime["Start"] and time < DateTime["End"].

**`DateTime`** — Required: no  ·  Type: DateTime  ·  Instance: `End`

If _Enabled_ the DataCollector will sample measurandes from SampledMeasurands as long as time >= DateTime["Start"] and time < DateTime["End"].

**`SamplingInterval`** — Required: no  ·  Type: decimal  ·  Unit: s

The sampling interval in seconds.

**`SampledMeasurands`** — Required: no  ·  Type: MemberList

The set of measurands to be sampled by the DataCollector.

### DCDERCtrlr

**`Enabled`** — Required: no  ·  Type: boolean

Whether DC DER control is enabled and DER capabilities are reported in this component.

**`MaxW`** — Required: yes  ·  Type: decimal  ·  Unit: W

Active power rating in watts at unity power factor

**`OverExcitedW`** — Required: yes  ·  Type: decimal  ·  Unit: W

Active power rating in watts at specified over-excited power factor

**`OverExcitedPF`** — Required: yes  ·  Type: decimal

Over-excited power factor

**`UnderExcitedW`** — Required: yes  ·  Type: decimal  ·  Unit: W

Active power rating in watts at specified under-excited power factor

**`UnderExcitedPF`** — Required: yes  ·  Type: decimal

Under-excited power factor

**`MaxVA`** — Required: yes  ·  Type: decimal  ·  Unit: VA

Maximum apparent power rating in voltamperes

**`MaxVar`** — Required: yes  ·  Type: decimal  ·  Unit: Var

Maximum injected reactive power rating in vars

**`MaxVarNeg`** — Required: yes  ·  Type: decimal  ·  Unit: Var

Maximum absorbed reactive power rating in vars

**`MaxChargeRateW`** — Required: yes  ·  Type: decimal  ·  Unit: W

Maximum active power charge rating in watts

**`MaxChargeRateVA`** — Required: yes  ·  Type: decimal  ·  Unit: VA

Maximum apparent power charge rating in voltamperes; may differ from the apparent power maximum rating

**`VNom`** — Required: no  ·  Type: decimal  ·  Unit: V

Nominal ac voltage rating in rms volts

**`MaxV`** — Required: no  ·  Type: decimal  ·  Unit: V

Maximum ac voltage rating in rms volts

**`MinV`** — Required: no  ·  Type: decimal  ·  Unit: V

Minimum ac voltage rating in rms volts

**`ModesSupported`** — Required: yes  ·  Type: MemberList

Indication of support for each control mode function

**`InverterManufacturer`** — Required: yes  ·  Type: string

Manufacturer of inverter

**`InverterModel`** — Required: yes  ·  Type: string

Model of inverter

**`InverterSerialNumber`** — Required: no  ·  Type: string

Serial number of inverter

**`InverterSwVersion`** — Required: yes  ·  Type: string

Software version of inverter

**`InverterHwVersion`** — Required: yes  ·  Type: string

Hardware version of inverter

**`IslandingDetectionMethod`** — Required: no  ·  Type: OptionList

Type of IslandingDetectionMethod

**`IslandingDetectionTripTime`** — Required: no  ·  Type: decimal  ·  Unit: s

Time until tripping after island detection

**`ReactiveSusceptance`** — Required: yes  ·  Type: decimal  ·  Unit: s

Reactive susceptance that remains connected to the electrical power system in the cease to energize and trip state

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

**`SupportedStates`** — Required: yes  ·  Type: MemberList

List of the states during which to display a message supported by this Charging Station.

**`SupportedFormats`** — Required: yes  ·  Type: MemberList

List of message formats supported by this Charging Station.

**`SupportedPriorities`** — Required: yes  ·  Type: MemberList

List of the priorities supported by this Charging Station.

**`Language`** — Required: yes  ·  Type: OptionList

Default language code, per RFC 5646, of this Charging Station. Languages that are supported are listed in the valuesList.

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

**`DischargePower`** — Required: V2X  ·  Type: decimal  ·  Unit: W, kW

The variableCharacteristic maxLimit holds the maximum rated discharge power that this EVSE can provide.  The variableCharacteristic maxSet holds the maximum configured discharge power that this EVSE can provide. The Actual value of the instantaneous (real) discharge power is recommended to be supported, but not required. Discharge power is represented by a positive value.

**`SupplyPhases`** — Required: yes  ·  Type: integer

Number of alternating current phases connected/available.

**`DCInputPhaseControl`** — Required: no  ·  Type: boolean

When DCInputPhaseControl is true, then the values of numberPhases and PhaseToUse in a ChargingSchedulePeriodType will select the input phases from the grid to be used by the DC EVSE.

**`ISO15118EvseId`** — Required: no  ·  Type: string

The name of the EVSE in the string format as required by ISO 15118 and IEC 63119-2. Example: "DE*ICE*E*1234567890*1"

**`ChargingState`** — Required: no  ·  Type: OptionList

This variable reports the current transaction charging state for an EVSE.

**`ActiveTransactionId`** — Required: no  ·  Type: string

This variable contains the transaction ID of the running transaction at the EVSE. If no transaction is active, it is an empty string.

### FiscalMetering

**`EnergyExport`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Total energy transferred: e.g.  from EV during (ongoing or terminated) charging session (in wH by default)

**`EnergyExportRegister`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Cumulative export kWh register value, such as from a (certified) fiscal energy meter.

**`EnergyImport`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Total energy transferred.

**`EnergyImportRegister`** — Required: no  ·  Type: decimal  ·  Unit: Wh, kWh

Cumulative export kWh register value, such as from a (certified) fiscal energy meter.

**`PublicKey`** — Required: no  ·  Type: string

The public key for a meter connected to a specific EVSE.

### FrequencySimulator

**`Enabled`** — Required: no  ·  Type: boolean

This variable must be set to true in order to activate the FrequencySimulator and gather data with the DataCollector.

**`DateTime`** — Required: no  ·  Type: DateTime  ·  Instance: `Start`

If _Enabled_ the FrequencySimulator will simulate a net frequency as long as time >= DateTime["Start"] and time < DateTime["End"].

**`DateTime`** — Required: no  ·  Type: DateTime  ·  Instance: `End`

If _Enabled_ the FrequencySimulator will simulate a net frequency as long as time >= DateTime["Start"] and time < DateTime["End"].

**`FrequencySchedule`** — Required: no  ·  Type: string

A JSON-formatted string with an array of { time, freq } pairs.

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

**`CertificateStatusSource`** — Required: no  ·  Type: MemberList

When present, this variable tells CSMS whether Charging Station uses OCSP or CRL to check for revoked certificates.

**`NotificationDelay`** — Required: no  ·  Type: integer  ·  Unit: s

The SECC (EVSE) uses the NotificationMaxDelay element in the EVSEStatus to indicate the time in seconds until it expects the EVCC (EV) to react on the action request indicated in EVSENotification.

**`ServiceRenegotiationSupport`** — Required: no  ·  Type: boolean

If set to 'True' the SECC (EVSE) is capable of ServiceRenegotiation.

**`SupportedProviders`** — Required: no  ·  Type: string

A comma-separated list of all providers (eMSPs) that are supported on this Charging Station. The providers are listed using country and provider ID from the EMAID, as defined in ISO 15118-20.

**`MaxPriceElements`** — Required: no  ·  Type: integer

The maximum number of priceRuleStacks and priceLevelScheduleEntries that Charging Station is able to accept in a ChargingScheduleType.

**`ProtocolSupported`** — Required: no  ·  Type: string  ·  Instance: `1, 2 .. 20`

A string with the following comma-separated items:  <uri>,<major>,<minor>. <uri> is in the format as used in the SupportedAppProtocolReq message from ISO 15118-2 and ISO 15118-20.

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

**`SupportsExpiryDateTime`** — Required: no  ·  Type: boolean

When set to true Charging Station will disregard idTokens for authorization as if not present in the Local Authorization List when current date/time is past the value of cacheExpiryDateTime.

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

Shows the last set MonitoringBase. Valid values according MonitoringBaseEnumType: All, FactoryDefault, HardwiredOnly.

**`ActiveMonitoringLevel`** — Required: no  ·  Type: integer

Shows the currently used MonitoringLevel. Valid values are severity levels of SetMonitoringLevelRequest: 0-9.

**`MaxPeriodicEventStreams`** — Required: no  ·  Type: integer

The maximum number of open periodic event streams that Charging Station supports.

### NetworkConfiguration

**`OcppCsmsUrl`** — Required: yes  ·  Type: string

URL of the CSMS (without the Charging Station Identity)

**`OcppInterface`** — Required: yes  ·  Type: OptionList

OptionList of values of OcppInterfaceEnumType.

**`OcppTransport`** — Required: yes  ·  Type: OptionList

OptionList of values of OCPPTransportEnumType. Is always "JSON".

**`OcppVersion`** — Required: yes  ·  Type: OptionList

OptionList of values of OcppVersionEnumType. This field is ignored.

**`MessageTimeout`** — Required: yes  ·  Type: integer

Duration in seconds before a message send by the Charging Station via this network connection times out.

**`SecurityProfile`** — Required: yes  ·  Type: integer

Security profile level.

**`Identity`** — Required: no  ·  Type: string

Required if SecurityCtrlr/Identity is ReadWrite

**`BasicAuthPassword`** — Required: yes  ·  Type: string

Writing to this variable only sets the password for the instance configurationSlot of Component NetworkConfiguration.

**`CsmsRootCertificateHashAlgorithm`** — Required: no  ·  Type: string

References a specific CSMS Root Certificate which has to be contained in the chain.

**`CsmsRootCertificateIssuerKeyHash`** — Required: no  ·  Type: string

References a specific CSMS Root Certificate which has to be contained in the chain.

**`CsmsRootCertificateIssuerNameHash`** — Required: no  ·  Type: string

References a specific CSMS Root Certificate which has to be contained in the chain.

**`CsmsRootCertificateSerialNumber`** — Required: no  ·  Type: string

References a specific CSMS Root Certificate which has to be contained in the chain.

**`VpnEnabled`** — Required: yes  ·  Type: boolean

True: VPN is configured.

**`VpnType`** — Required: no  ·  Type: string

Value from VPNEnumType

**`VpnServer`** — Required: no  ·  Type: string

VPN server address

**`VpnUser`** — Required: no  ·  Type: string

VPN user name

**`VpnGroup`** — Required: no  ·  Type: string

VPN group name

**`VpnPassword`** — Required: no  ·  Type: string

VPN password

**`VpnKey`** — Required: no  ·  Type: string

VPN shared secret

**`ApnEnabled`** — Required: yes  ·  Type: boolean

True: APN is configured.

**`Apn`** — Required: no  ·  Type: string

Access Point Name as URL

**`ApnUserName`** — Required: no  ·  Type: string

APN user name

**`ApnPassword`** — Required: no  ·  Type: string

APN password

**`SimPin`** — Required: no  ·  Type: string

SIM card PIN code

**`PreferredNetwork`** — Required: no  ·  Type: string

Preferred network as concatenation of MCC and MNC

**`UseOnlyPreferredNetwork`** — Required: no  ·  Type: boolean

When true use only the preferred network

**`ApnAuthentication`** — Required: no  ·  Type: string

Value from APNAuthenticationEnumType

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

**`ExternalConfigChangeDate`** — Required: no  ·  Type: DateTime

Date/time when the configuration was changed externally, i.e. outside of CSMS, for example by a local service action.

### PaymentCtrlr

**`Enabled`** — Required: yes  ·  Type: boolean

Payment terminal support is enabled.

**`Problem`** — Required: yes  ·  Type: boolean

There's a problem with the payment terminal.

**`AuthorizeDirectPayment`** — Required: yes  ·  Type: boolean

If true, an AuthorizeRequest must be sent to CSMS to approve the direct payment.

**`AuthorizationAmount`** — Required: yes  ·  Type: decimal

Amount used for the pre-authorization.

**`IncrementalAuthorizationAmount`** — Required: no  ·  Type: decimal

If value is 0, then incremental authorization is not allowed. Variable will be absent if Charging Station or payment terminal do not support incremental authorization.

**`IncrementalAuthorizationThreshold`** — Required: no  ·  Type: decimal

If costs exceed current authorization amount minus IncrementalAuthorizationThreshold then the authorization needs to be increased.

**`PaymentDetails`** — Required: yes  ·  Type: MemberList

The _valuesList_ of PaymentDetails contains the information that the payment terminal is able to provide. The Actual value of PaymentDetails determines which of these details shall be provided in the idToken.additionInfo field.

**`SettlementByCSMS`** — Required: yes  ·  Type: boolean

When true, CSMS will take care of settlement

**`ReceiptServerUrl`** — Required: yes  ·  Type: string

URL to the receipt server, where an EV driver can find the receipt afterwards.

**`ReceiptByCSMS`** — Required: yes  ·  Type: boolean

When true, CSMS will provide a URL to receipt, else it is provided by payment terminal.

**`Merchant`** — Required: yes  ·  Type: string  ·  Instance: `Id`

Merchant ID to be added to a PSP/locally generated receipt.

**`Merchant`** — Required: yes  ·  Type: string  ·  Instance: `TaxId`

Tax ID of the merchant to be added to a PSP/locally generated receipt.

**`Merchant`** — Required: yes  ·  Type: string  ·  Instance: `Name`

Name of the merchant to be added to a PSP/locally generated receipt.

**`Merchant`** — Required: yes  ·  Type: string  ·  Instance: `Address`

Address of the merchant to be added to a PSP/locally generated receipt.

**`Merchant`** — Required: yes  ·  Type: string  ·  Instance: `City`

City of the merchant to be added to a PSP/locally generated receipt.

**`TerminalID`** — Required: yes  ·  Type: string

Terminal ID of the payment terminal.

**`PaymentServiceProvider`** — Required: yes  ·  Type: string

The payment service provider that the terminal is using. Typically read-only.

**`VendorName`** — Required: yes  ·  Type: string

Manufacturer of the payment terminal.

**`Model`** — Required: yes  ·  Type: string

Model of the payment terminal.

**`SerialNumber`** — Required: yes  ·  Type: string

Payment terminal serial number.

**`FirmwareVersion`** — Required: yes  ·  Type: string

Payment terminal firmware version.

**`IMSI`** — Required: yes  ·  Type: string

IMSI of the payment terminals SIM card.

**`ICCID`** — Required: yes  ·  Type: string

ICCID of the payment terminals SIM card.

**`Connected`** — Required: yes  ·  Type: boolean

Boolean to indicate whether the payment terminal is connected to its payment service provider.

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

**`SignStartedReadings`**

If set to true, the Charging Station SHALL include signed meter values for context_= `Transaction.Begin` in the metervalues field in the TransactionEventRequest(Started or Updated)+

**`SignUpdatedReadings`**

If set to true, the Charging Station SHALL include signed meter values in the TransactionEventRequest Updated)

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

**`UpstreamInterval`** — Required: no  ·  Type: integer  ·  Unit: s

Size (in seconds) of the samplng interval, intended to be transmitted in the TransactionEventyRequest message for location `Upstream` only.

**`UpstreamMeasurands`** — Required: no  ·  Type: MemberList

Sampled measurand(s) to be included in TransactionEventRequest for location `Upstream` only.

### SecurityCtrlr

**`AllowSecurityProfileDowngrade`** — Required: no  ·  Type: boolean

If this variable is implemented and set to true, then the Charging Station allows downgrading the security profile from 3 to 2.

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

**`ExternalConstraintsProfileDisallowed`** — Required: no  ·  Type: boolean

Indicates whether a Charging Station allows an external system to submit limits to be represented as a `ChargingStationExternalConstraints` charging profile.

**`ChargingProfilePersistence`** — Required: no  ·  Type: boolean  ·  Instance: `TxProfile`

If an instance of this variable is true, then charging profiles with the chargingProfilePurpose mentioned in the variableInstance are persistent, i.e. they are stored persistently and will still exist after a reboot.

**`ChargingProfilePersistence`** — Required: no  ·  Type: boolean  ·  Instance: `LocalGeneration`

If an instance of this variable is true, then charging profiles with the chargingProfilePurpose mentioned in the variableInstance are persistent, i.e. they are stored persistently and will still exist after a reboot.

**`ChargingProfilePersistence`** — Required: no  ·  Type: boolean  ·  Instance: `ChargingStationExternalConstraints`

If an instance of this variable is true, then charging profiles with the chargingProfilePurpose mentioned in the variableInstance are persistent, i.e. they are stored persistently and will still exist after a reboot.

**`SetpointPriority`** — Required: no  ·  Type: OptionList

Defines which setpoint shall be used when a `ChargingStationExternalConstraints` profile with a operationMode = `ExternalSetpoint` is active, but at the same time a `Tx(Default)Profile` charging profile is also active with a setpoint.

**`MaxExternalConstraintsId`** — Required: no  ·  Type: integer

Defines the highest value that a charging profile id of a `ChargingStationExternalConstraints` profile in the Charging Station can have.

**`SupportedAdditionalPurposes`** — Required: no  ·  Type: MemberList

This configuration variable lists the additional chargingProfilePurposes, that have been introduced in OCPP 2.1, that are supported by the Charging Station.

**`SupportsDynamicProfiles`** — Required: no  ·  Type: boolean

When this variable has value True, then the Charging Station supports charging profiles of kind `Dynamic`.

**`SupportsMaxOfflineDuration`** — Required: no  ·  Type: boolean

When this variable has value True, then the Charging Station supports the fields maxOfflineDuration and invalidAfterOfflineDuration in a charging profile.

**`SupportsUseLocalTime`** — Required: no  ·  Type: boolean

When this variable has value True, then the Charging Station supports the field useLocalTime in a charging schedule.

**`SupportsRandomizedDelay`** — Required: no  ·  Type: boolean

When this variable has value True, then the Charging Station supports the field randomizedDelay_in a charging schedule, which will delay the start of each charging schedule period by a random number between 0 and randomizedDelay.

**`SupportsLimitAtSoC`** — Required: no  ·  Type: boolean

When this variable has value True, then the Charging Station supports the field limitAtSoC in a charging schedule, which will cap the limit or setpoint in the ChargingSchedulePeriodType by the value of _imitAtSoC.limit.

**`SupportsEvseSleep`** — Required: no  ·  Type: boolean

When reported as true the Charging Station supports the evseSleep flag in a charging schedule period, which requests the EVSE electronics to go to sleep during operationMode = 'Idle'.

### TariffCostCtrlr

**`Available`** — Required: no  ·  Type: boolean  ·  Instance: `Tariff`

If true then the Charging Station supports the TariffType structure,

**`Available`** — Required: no  ·  Type: boolean  ·  Instance: `Cost`

If true, then Charging Station supports local cost calculation.

**`Currency`** — Required: yes  ·  Type: string

Currency used by this Charging Station in a ISO 4217 [ISO4217] formatted currency code.

**`Enabled`** — Required: no  ·  Type: boolean  ·  Instance: `Tariff`

If true then the Charging Station has enabled support for the TariffType structure, that describes the tariff in a machine-readable format.

**`Enabled`** — Required: no  ·  Type: boolean  ·  Instance: `Cost`

If true, then local cost calculation is enabled on Charging Station.

**`Enabled`** — Required: no  ·  Type: boolean  ·  Instance: `RunningCost`

If true then Charging Station will provide periodic running cost updates in costDetails in TransactionEventRequest messages.

**`TariffFallbackMessage`** — Required: yes  ·  Type: string  ·  Instance: `<language>`

Message (and/or tariff information) to be shown to an EV Driver when there is no driver specific tariff information available.

**`TotalCostFallbackMessage`** — Required: yes  ·  Type: string  ·  Instance: `<language>`

Message to be shown to an EV Driver when the Charging Station cannot retrieve the cost for a transaction at the end of the transaction.

**`OfflineTariffFallbackMessage`** — Required: no  ·  Type: string  ·  Instance: `<language>`

Message (and/or tariff information) to be shown to an EV Driver when Charging Station is offline.

**`Interval`** — Required: no  ·  Type: integer  ·  Unit: s  ·  Instance: `Tariff`

Interval specifies the maximum interval in seconds to use when evaluating the conditions regarding current, power and energy of a tariff element during a transaction.

**`Interval`** — Required: no  ·  Type: integer  ·  Unit: s  ·  Instance: `Cost`

Specifies the interval in seconds to use to provide periodic running cost updates during a transaction.

**`MaxElements`** — Required: no  ·  Type: integer  ·  Instance: `Tariff`

Specifies the maximum number of prices elements that the Charging Station supports in each energy, chargingTime, idleTime and fixedFee field of a TariffType.

**`ConditionsSupported`** — Required: no  ·  Type: boolean  ·  Instance: `Tariff`

If set to true the Charging Station supports tariffs with conditions.

**`HandleFailedTariff`** — Required: no  ·  Type: OptionList  ·  Instance: `Tariff`

This configuration determines how to act when a driver-specific tariff is received, which cannot be processed.

### TokenReader

**`Token`** — Required: no  ·  Type: string

String of bytes representing an ID token.

**`TokenType`** — Required: no  ·  Type: OptionList

Type of Token. Value is one of IdTokenEnumType.

### TxCtlrl

**`EnergyTransferResumptionRandomRange`** — Required: no  ·  Type: integer  ·  Unit: s

Maximum length of random time to delay resumption of energy transfer after an interruption

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

**`ResumptionTimeout`** — Required: no  ·  Type: integer  ·  Unit: s

This variable defines the maximum number of seconds that a transaction may be interrupted by a power outage and still be resumed afterwards.

**`AllowEnergyTransferResumption`** — Required: no  ·  Type: boolean

This variable defines whether energy transfer is allowed to be resumed when the transaction is resumed after a reset or power outage.

**`SupportedLimits`** — Required: no  ·  Type: MemberList

This variable defines which transaction limits in TransactionLimitType are supported by the Charging Station.

### V2XChargingCtrlr

**`Enabled`** — Required: yes  ·  Type: boolean

Way for the CSMS to either activate or deactivate V2X functionality on a Charging Station.

**`SupportedEnergyTransferModes`** — Required: yes  ·  Type: MemberList

Lists the energy transfer services that are supported by the Charging Station.

**`SupportedOperationModes`** — Required: yes  ·  Type: MemberList

Lists the operation modes that are supported by the Charging Station.

**`LocalFrequencyUpdateThreshold`** — Required: no  ·  Type: boolean

The amount of change in net frequency in *mHz* is needed to trigger a recalculation of the setpoint.

**`TxStartedMeasurands`** — Required: no  ·  Type: MemberList  ·  Instance: `<OperationMode>`

List of sampled measurands to send in addition to those configured in SampledDataCtrlr.TxStartedMeasurands, when the Charging Station is in V2X operation mode <OperationMode>

**`TxEndedMeasurands`** — Required: no  ·  Type: MemberList  ·  Instance: `<OperationMode>`

List of sampled measurands to send in addition to SampledDataCtrlr.TxEndedMeasurands, when the Charging Station is in V2X operaion mode <OperationMode>.

**`TxUpdatedMeasurands`** — Required: no  ·  Type: MemberList  ·  Instance: `<OperationMode>`

List of sampled measurands to send in addition to SampledDataCtrlr.TxUpdatedMeasurands, when the Charging Station is in V2X operation mode <OperationMode>.

**`TxEndedInterval`** — Required: no  ·  Type: integer  ·  Unit: s  ·  Instance: `<OperationMode>`

The interval used to sample the list of measurands in V2XChargingCtrlr.TxEndedMeasurands, while the Charging Station is in V2X operation mode <OperationMode>.

**`TxUpdatedInterval`** — Required: no  ·  Type: integer  ·  Unit: s  ·  Instance: `<OperationMode>`

The interval used to sample the list of measurands in V2XChargingCtrlr.TxUpdatedMeasurands, while the Charging Station is in V2X operation mode <OperationMode>.

**`LocalLoadBalancing`** — Required: no  ·  Type: decimal  ·  Unit: W  ·  Instance: `UpperThreshold`

When power (in Watts) exceeds this limit, the local load balancing mechanism will try to imit the power to a maximum of UpperThreshold + UpperOffset.

**`LocalLoadBalancing`** — Required: no  ·  Type: decimal  ·  Unit: W  ·  Instance: `LowerThreshold`

When power (in Watts) drops below this limit, the local load balancing mechanism will try to keep the power to a minimum of LowerThreshold + LowerOffset.

**`LocalLoadBalancing`** — Required: no  ·  Type: decimal  ·  Unit: W  ·  Instance: `UpperOffset`

An offset value (in Watts) to add to the UpperThreshold. This allows for some tuning of the upper limit without changing the threshold value.

**`LocalLoadBalancing`** — Required: no  ·  Type: decimal  ·  Unit: W  ·  Instance: `LowerOffset`

An offset value (in Watts) to add to the LowerThreshold. This allows for some tuning of the lower limit without changing the threshold value.

### WebPaymentsCtrlr

**`URLTemplate`** — Required: yes  ·  Type: string

URL template

**`URLParameters`** — Required: no  ·  Type: MemberList

List of supported URL parameters, valuesList: "maxtime", "maxenergy", "maxcost".  When absent, none of these are supported.

**`TOTPVersion`** — Required: yes  ·  Type: string

Version of TOTP algorithm.  valuesList: list of supported TOTP versions, e.g. "v1"

**`ChargingStationId`** — Required: no  ·  Type: string

Charging station Id to use in URL.  When absent will default to Charging Station identity, as defined in SecurityCtrlr.Identity.

**`ValidityTime`** — Required: yes  ·  Type: integer  ·  Unit: s

Time in seconds to show QR, e.g. 30

**`SharedSecret`** — Required: yes  ·  Type: string

<random text> set to a random value on first boot

**`Length`** — Required: yes  ·  Type: integer

Length of TOTP, e.g. 8

**`QRCodeQuality`** — Required: no  ·  Type: OptionList

Low, Medium, Quartile, High

### Generic variables

Variables that apply generically to any component, not bound to one specific component.

**`ACCurrent`** — Required: no  ·  Type: decimal  ·  Unit: A

RMS AC Current (in amperes). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average of all per-phase readings and written values are common per-phase settings. Example(s): ChargingStation: Total AC current consumption (all EVSEs, ancillaries), EVSE: Total current consumed by EVSE: includes losses (AC->DC) and EVSE specific ancillaries (e.g. fans), ElectricalFeed: Inflow AC current on feed

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

Reports (impact) force/ acceleration values (estimates) in one or more directions, in units of Newtons or g. Multiple force readings in different (orthogonal) dimensions may be reported using Variable instance values, such as Down, Right, Forward.

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

Instantaneous (real) Power (measured/calculated, including power factor for AC). Where a component (e.g. AC to DC Power Converter) has multiple power measurements, the default (unkeyed) instance is input power.

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

**`CommunicationParent`** — Required: no  ·  Type: string

Points to a communication parent component (data flow source), to allow rendering the communication hierarchy in a UI.

**`ElectricalParent`** — Required: no  ·  Type: string

Points to a electrical parent component (energy flow source), to allow rendering the electrical hierarchy in a UI.

**`LogicalParent`** — Required: no  ·  Type: string

Points to a logical parent component, to allow rendering a comprehensive overview of the Charging Station components in a UI.

**`PhysicalParent`** — Required: no  ·  Type: string

Points to a physical parent component (container), to allow rendering an overview of the Charging Station component locations in a UI.

**`Label`** — Required: no  ·  Type: string

Specifies a non-unique label to be used in a hierarchy UI rendering, in place of the unique component name and instance, in case a duplicate label is needed.
