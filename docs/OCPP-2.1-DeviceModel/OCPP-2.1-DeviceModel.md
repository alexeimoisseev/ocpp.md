# OCPP 2.1 — Device Model Reference

> **Source:** OCA OCPP 2.1 appendix CSVs (`components.csv`, `variables.csv`, `dm_components_vars.csv`). Mechanically generated — see [METHODOLOGY](../METHODOLOGY.md). These are the **standardized** component and variable names referenced by free-form `name` fields in `GetVariables`/`SetVariables`/`GetReport`. Vendors may extend with optional custom components/variables.

## Components (82)

| Component | Description |
| --- | --- |
| ACDERCtrlr | Responsible for configuration relating to DER capabilities that the EVSE of the Charging Station can emulate by using ISO 15118-20 ChargeLoop messages to control the inverter in the EV. The component is located at the EVSE level, since it represents the DER capabilities of the EVSE. |
| AlignedDataCtrlr | Logical Component responsible for configuration relating to the reporting of clock-aligned meter data. |
| AuthCacheCtrlr | Logical Component responsible for configuration relating to the use of a local cache for authorization for Charging Station use. |
| AuthCtrlr | Logical Component responsible for configuration relating to the use of authorization for Charging Station use. |
| BatterySwapCtrlr | Responsible for configuration relating to Battery swapping. |
| CHAdeMOCtrlr | A CHAdeMO Controller component communicates with an EV using the wired CANbus protocol to exchange information and control charging using the CHAdeMO protocol |
| ClockCtrlr | Provides a means to configure management of time tracking by Charging Station. |
| CustomizationCtrlr | Responsible for configuration relating to custom vendor-specific implementations, like the DataTransfer message and CustomData extensions or CustomTriggers. |
| DCDERCtrlr | Responsible for configuration relating to DER capabilities of the DC inverter of the EVSE in the Charging Station. The component is located at the EVSE level, since it represents the DER capabilities, also referred to as nameplate information, of the EVSE. |
| DeviceDataCtrlr | Logical Component responsible for configuration relating to the exchange and storage of Charging Station Device Model data. |
| DisplayMessageCtrlr | Logical Component responsible for configuration relating to the display of messages to Charging Station users. |
| ISO15118Ctrlr | Communicates with an EV to exchange information and control charging using the ISO 15118 protocol. |
| LocalAuthListCtrlr | Logical Component responsible for configuration relating to the use of Local Authorization Lists for Charging Station use. |
| MonitoringCtrlr | Logical Component responsible for configuration relating to the exchange of monitoring event data. |
| PaymentCtrlr | Logical Component responsible for configuration relating to payment terminals. |
| OCPPCommCtrlr | Logical Component responsible for configuration relating to information exchange between Charging Station and CSMS. |
| ReservationCtrlr | Logical Component responsible for configuration relating to reservations. |
| SampledDataCtrlr | Logical Component responsible for configuration relating to the reporting of sampled meter data. |
| SecurityCtrlr | Logical Component responsible for configuration relating to security of communications between Charging Station and CSMS. |
| SmartChargingCtrlr | Logical Component responsible for configuration relating to smart charging. |
| TariffCostCtrlr | Logical Component responsible for configuration relating to tariff and cost display. |
| TxCtrlr | Logical Component responsible for configuration relating to transaction characteristics and behaviour. |
| V2XChargingCtrlr | Responsible for configuration relating to V2X charging/discharging. This component exists on the EVSE tier hierarchy. |
| WebPaymentsCtrlr | Responsible for configuration of a dynamic QR code for ad hoc payments. |
| AccessBarrier | Allows physical access of vehicles to a charging site to be controlled. |
| AcDcConverter | Provides a variable DC current source to force energy directly into an EV battery stack, under tight control of the EV's battery management system. |
| AcPhaseSelector | Allows a specific AC phase to be selected (typically at EVSE tier) for single phase vehicle charging in order to lower overall (e.g. site) phase imbalance. |
| Actuator | A general purpose electro-mechanical output system, with optional completion tracking sensing. Each output should use a Variable instance key indicating the nature of the output. |
| AirCoolingSystem | Fans (or equivalent devices) used to provide cooling. |
| AreaVentilation | Fans (or equivalent devices) used to ensure that EVs that require ventilation during charging |
| BatteryCartridge | BatteryCartridge represents the battery cartridge that is currently inserted into the EVSE of a battery swap station |
| BayOccupancySensor | Sensor (optical, ground loop, ultrasonic, etc.) to detect whether the associated parking/charging bay is physically vacant, or is occupied by a vehicle or other obstruction |
| BeaconLighting | Beacon Lighting to help EV drivers to locate nearby charging places, and/or to determine charging availability state, usually by color variation. |
| CableBreakawaySensor | A sensor that detects when a charging cable (captive or removable) has been forcibly pulled from the Charging Station. |
| CaseAccessSensor | Reports when an access door/panel is open |
| ChargingStation | The entire Charging Station as a logical entity |
| ChargingStatusIndicator | The Charging Status Indicator, provides visible feedback to the user about the connection and charging status of an EVSE/Connector. This is commonly in the form of multi-colored lighting. |
| ConnectedEV | ConnectedEV is a component that represents a connected vehicle for which data is received via an ISO 15118 or CHAdeMO interface. The generic information that is received, is represented as variables of ConnectedEV. Any protocol-specific information is represented in variables of the ISO15118Ctrlr or CHAdeMOCtrlr component. |
| Connector | A means to connect an EV to a Charging Station with either a socket, an attached cable & inline connector, or any wireless power transfer device. |
| ConnectorHolsterRelease | A mechanism present in a connector holster to prevent the connector from being removed inappropriately: typically unlocks connector after authorization. |
| ConnectorHolsterSensor | A mechanism to report when a tethered cable connector has been removed from its normal stowage position. May be used for detection of connectors left un-holstered, and possible penalty billing. |
| ConnectorPlugRetentionLock | Locking mechanism to retain an inserted plug, both to prevent on-load disconnection, and to prevent theft of charging cables |
| ConnectorProtectionRelease | External protective mechanism (e.g. an external shutter or a connector holster lock mechanism) to prevent contact with conductors that may become 'live' under other failure modes |
| Controller | An embedded logic controller |
| ControlMetering | Energy, Power, Electricity meter, used to measure energy, current, voltages etc. |
| CPPWMController | Control Pilot PWM Controller: provides and senses the IEC 61851-1 / SAE J1772 low voltage DC and PWM signalling between an EVSE and EV over a control pilot line. |
| DataLink | Provides a communications link from a Charging Station to a CSMS. It may use fixed infrastructure, mobile telephony data services, WiFi, or other connectivity channels. |
| Display | Provides information and feedback to the user. |
| DistributionPanel | Defines the Distribution Panel, with it's fuses and connections to both Charging Stations and other Distribution Panel's. |
| ElectricalFeed | Represents an incoming electrical connection to a Charging Station, that may be a grid/distribution network connection, of a connection to local power generation and/or storage. Each electrical feed can record the electrical and other characteristics of that feed, including power rating, fusing, upstream metering, etc. When a Charging Station has more than one electrical feed, it must represent which feed supplies each EVSE, and which feed supplies the house load of the Charging Station itself. Simple Charging Stations with only a single electrical feed may omit all electrical feed information, in which case it is inferred that all power is supplied from a single feed, and what would otherwise be ElectricalFeed data (Variables) may be reported as being associated with the ChargingStation component. |
| ELVSupply | Represents the low voltage power supply (typically 12V DC and often other ELV voltages) that provides operating power for controllers, relays, and other electrical components. |
| EmergencyStopSensor | An 'Emergency Stop' button that should be pressed by the user or other nearby persons if serious faulty behavior is observed (e.g. smoke/flames from EV or Charging Station). |
| EnvironmentalLighting | Provides reporting/control of general illumination lighting in use at Charging Station. |
| EVRetentionLock | A locking mechanism on the EV side as a safety measure to prevent it being disconnected while high currents are flowing. |
| EVSE | The entire chain of components responsible for transporting energy from the incoming supply to the electric vehicle (or vice versa) |
| ExternalTemperatureSensor | Reports ambient air temperature |
| FiscalMetering | Provides energy transfer readings that are the basis for billing. |
| FloodSensor | A sensor reporting whether the Charging Station is experiencing water ingress/pooling. |
| GroundIsolationProtection | An Isolation Tester as part of their own self-test mechanisms, to confirm the isolation of floating circuitry when no Evs are connected |
| Heater | Heater to ensure reliable operation in cold environments |
| HumiditySensor | Reports relative air humidity |
| LightSensor | Reports ambient light levels. |
| LiquidCoolingSystem | A liquid based cooling system, typically used to cool the connector cables of very high power Charging Stations. |
| LocalAvailabilitySensor | Accepts local signal inputs controlling whether new Charging Sessions can start and/or whether ongoing sessions should continue. Typically connected to a site/building power supply, to automatically report unavailability when closed. |
| LocalController | The entire Local Controller as a logical entity |
| LocalEnergyStorage | Energy storage |
| NetworkConfiguration | The instances of component NetworkConfiguration represent network connection configurations. |
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
| TokenReader | An authorization token reader (e.g. RFID) |
| UpstreamProtectionTrigger | Circuitry designed to trigger the disconnection of power to the structure by an upstream protection device after a severe problem has been detected |
| UIInput | A logical input mechanism (e.g. set of buttons) that is part of a UI whose use may be communicated to the CSMS (in near real time). May support momentary inputs ('Operated') or modal state ('Active'). Multiple input sources should use explicit Variable instance keys (where the input function is key name). |
| VehicleIdSensor | Reports an identifier associated with a vehicle occupying a charging bay. The identifier may be a vehicle registration number via ANPR hardware, a VIN, or other local identifier of the vehicle based on medium range/active RFID, or any other relevant technology and result. |

## Component × Variable Matrix (438)

> `<generic>` in the Component column means the variable applies generically, not to one specific component.

| Specific Component | Variable | Instance | Required? | DataType | Unit | Description |
| --- | --- | --- | --- | --- | --- | --- |
| <generic> | ACCurrent |  | no | decimal | A | RMS AC Current (in amperes). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average of all per-phase readings and written values are common per-phase settings. Example(s): ChargingStation: Total AC current consumption (all EVSEs, ancillaries), EVSE: Total current consumed by EVSE: includes losses (AC->DC) and EVSE specific ancillaries (e.g. fans), ElectricalFeed: Inflow AC current on feed |
| <generic> | Active |  | no | boolean |  | Component is in its non-resting / active state: e.g: On, Engaged, Locked. Some Components may have secondary functions that have corresponding Active Variables with an explicit Variable instance., Note: Monitoring of changes in the Active state of any Component can be specified by setting Delta monitoring on the boolean value with a delta values of 1. Setting/clearing an Active Variable activates/stops the associated functionality, where remotely controllable. Only components that are Available and Enabled can be in the Active state. |
| <generic> | ACVoltage |  | no | decimal | V | RMS AC Voltage (in volts). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average ofall per-phase readings and written values are common per-phase settings. Example(s): ElectricalFeed: Input Voltage |
| <generic> | AllowReset |  | no | boolean |  | Component can be reset. |
| <generic> | Angle |  | no | decimal | Deg | Angle(s) relative to normal/design idle position. Multiple Variable instance values may be used to indicate angular position in multiple axes (e.g. Left-Right, Forward-Back). |
| <generic> | Attempts |  | no | integer |  | Number of attempts (INCLUDING the original attempt) in the last successful or attempted, cycle of operation. Applies typically to self-monitoring motorized electro-mechanical equipment, etc. {Null}: Unknown, 0: Not Attempted/Not allowed, 1: Single attempt/No retries [allowed], 2-N: [up to] N tries [allowed] |
| <generic> | Available |  | no | boolean |  | The Component exists and is locally configured/wired for use, but might not be (remotely) Enabled. |
| <generic> | Certificate |  | no | string |  | Digital Certificate (in Base64 encoding) |
| <generic> | Color |  | no | string |  | Standard 24 bit hexadecimal RGB values. Reg Green Blue color intensity, expressed as standard 24 bit hexadecimal RGB values: 3  00-FF (0-255), in order RRGGBB). E.g. 000000: Black, FF0000: Red, 00FF00: Green, 0000FF: Blue, FFFF00:Yellow, FFFFFF: White, 008000: Medium intensity green. |
| <generic> | Complete |  | no | boolean |  | Component operation cycle has completed. Used only in event notifications, where it is always true. |
| <generic> | ConnectedTime |  | no | decimal | s | Time since logical connection established |
| <generic> | Count |  | no | integer |  | General purpose integer count variable for Component state reporting |
| <generic> | CurrentImbalance |  | no | decimal | Percent | Percentage current imbalance in an AC three phase supply. |
| <generic> | DataText |  | no | string |  | Text associated with a Component, e.g. a Display. |
| <generic> | DateTime |  | no | dateTime |  | Point in time value, in [RFC3339] datetime format. Time zone optional. |
| <generic> | DCCurrent |  | no | decimal | A | DC Current (in amperes). May be an instantaneous measurement, or a period average, depending on context/equipment. |
| <generic> | DCVoltage |  | no | decimal | V | DC Voltage (volts). May be an instantaneous measurement, or a period average, depending on context/equipment. |
| <generic> | ECVariant |  | no | string |  | Production series variants reflecting internal design changes or sub-component substitutions not affecting external functionality. |
| <generic> | Enabled |  | no | boolean |  | The Component is Enabled for operation. For Available components that cannot be selectively (remotely) enabled / disabled, this value is always true. Note: Available cannot be false of Enabled is true, so during inventory reporting, Enabled=1 also logically states Available=true |
| <generic> | Energy |  | no | decimal | Wh, kWh | Energy quantity (in Wh) for reporting/configuring values related to stored energy (i.e. not transferred energy). |
| <generic> | Entries |  | no | integer |  | General purpose variable for reporting/managing numbers of entries in repetitive data structures. maxLimit characteristic reports maximum possible entries. |
| <generic> | Fallback |  | no | boolean |  | Component is operating in a fallback, or backup mode. In inventory reports, a Value of 1 for the maxLimit characteristic indicates that the component can enter a fallback state (i.e. a fallback mode is present). |
| <generic> | FanSpeed |  | no | decimal | RPM | Fan Speed (in RPM). A value of 0 represents stopped/stalled. An empty value indicates that fan speed cannot be read. |
| <generic> | FirmwareVersion |  | no | string |  | Version number of firmware. |
| <generic> | Force |  | no | decimal | N | Reports (impact) force/ acceleration values (estimates) in one or more directions, in units of Newtons or g. Multiple force readings in different (orthogonal) dimensions may be reported using Variable instance values, such as Down, Right, Forward. |
| <generic> | Formats |  | no | MemberList |  | List of message formats supported by this Charging Station. Possible values: ASCII, HTML, URI, UTF-8. |
| <generic> | Frequency |  | no | decimal | Hz | Frequency of AC power, signal, or component operation. |
| <generic> | FuseRating |  | no | decimal | A | Current rating of a fuse/breaker. Variable instances keyed by phase identifier (L1/L2/L3/N). |
| <generic> | Height |  | no | decimal | m | Height above(+)/below(-) reference level (ground level unless context demands otherwise). |
| <generic> | Humidity |  | no | decimal | RH | The relative humidity in %. |
| <generic> | Hysteresis |  | no | decimal | Percent | Specifies the width of a 'dead band' (as a percentage of the threshold) around the central value of a threshold setting (e.g. MinSet, MaxSet, monitor thresholds) to avoid repeated triggering when the measured quantity lies close to the threshold and is subject to small variations. |
| <generic> | ICCID |  | no | string |  | ICCID (Integrated Circuit Card IDentifier) of mobile data SIM card. |
| <generic> | Impedance |  | no | decimal | Ohm | Impedance: Primary value is real (resistive only) impedance. Where a complex impedance is to be reported, the imaginary part (reactance) must be represented with a separate Variable instance value of 'reactance'. Reactance values are expressed at the (nominal) relevant operating frequency of the Component (e.g. 50/60Hz for mains electricity feed). |
| <generic> | IMSI |  | no | string |  | IMSI (International Mobile Subscriber Identity) number of mobile data SIM card |
| <generic> | Interval |  | no | integer | s | Minimum Interval (in seconds) between (attempted) operations. |
| <generic> | Length |  | no | decimal | m | General Purpose linear distance measure. |
| <generic> | Light |  | no | decimal | lx | (Ambient) light level. The value is in Lux. |
| <generic> | Manufacturer |  | no | string |  | Component Manufacturer name |
| <generic> | Message |  | no | string |  | Specific stored message for display. |
| <generic> | MinimumStatusDuration |  | no | integer | s | Minimum duration that a Charging Station or EVSE status is stable before StatusNotificationRequest is sent to the CSMS. |
| <generic> | Mode |  | no | string |  | Operating mode string from among valid options (communicated by OptionList, etc. during capability/configuration  discovery). |
| <generic> | Model |  | no | string |  | Manufacturer's Model code/number of Component, including suffixes etc. to identify functional, regional or linguistic variation, but NOT engineering change level internal 				variation not affecting external behaviour, etc. |
| <generic> | NetworkAddress |  | no | string |  | Current network address of a Component. |
| <generic> | Operated |  | no | boolean |  | The Component operated in an instantaneous, transient, or immediately self-resetting pattern. Used only in event notifications, where it is always true. |
| <generic> | OperatingTimes |  | no | string |  | Recurring operating times in iCalendar RRULE format. |
| <generic> | Overload |  | no | boolean |  | Component is in Overload state. |
| <generic> | Percent |  | no | decimal | Percent | Generic dimensionless value reporting/setting value. |
| <generic> | PhaseRotation |  | no | OptionList |  | The phase wiring of Component, relative to it's upstream feed Component/device. This variable describes the phase rotation of a Component relative to its parent Component, using a three letter string consisting of the letters: R, S, T and x. The letter 'R' can be identified as phase 1 (L1), 'S' as phase 2 (L2), 'T' as phase 3 (L3). The lower case 'x' is used to designate a phase that is not connected. An empty string means that phase rotation is not applicable or not known. |
| <generic> | PostChargingTime |  | no | decimal | s | Elapsed time in seconds since last substantive energy transfer |
| <generic> | Power |  | no | decimal | W, kW | Instantaneous (real) Power (measured/calculated, including power factor for AC). Where a component (e.g. AC to DC Power Converter) has multiple power measurements, the default (unkeyed) instance is input power. |
| <generic> | Problem |  | no | boolean |  | Component itself has a 'Problem' condition that impacts in any significant way on its normal operation. By definition, 'Problem' state includes (logical OR) 'Fault' state. 'Problem' specifically INCLUDES inability to operate that is propagated (up/down/sideways) from any other associated/connected/containing/contained Component. |
| <generic> | Protecting |  | no | boolean |  | Applies to 'sensor' type Components that have an associated protection capability, whereby they can  disconnect power (e.g. using the main PowerContactor) if the sensed quantity is outside preset/configured limits. If Protecting is true, the Component is actively preventing/interrupting charging. |
| <generic> | SerialNumber |  | no | string |  | Serial number of Component. |
| <generic> | SignalStrength |  | no | decimal | dBm | (Radio/Wired/Optical) data signal strength, in ASU (typically 0-31 or 99 for unknown). Or dbmW (typically -140 to -50). |
| <generic> | State |  | no | string |  | A state code or name identifier string, to allow the internal state of  components to be reported and/or  controlled |
| <generic> | StateOfCharge |  | no | decimal | Percent | Energy Storage Device (e.g. battery) state of charge, expressed as a percentage of nominal design 0-100% operating range. Note: Values below or above 0-100% are possible and represent over discharged/charged states. |
| <generic> | Storage |  | no | integer | B | In bytes. Amount of storage occupied. Storage(maxLimit) specifies absolute limit Storage(MaxSet) restricts usage to specified Max, if supported. |
| <generic> | SupplyPhases |  | no | integer |  | Number of alternating current phases connected/available. 1 or 3 for AC, 0 means DC (no alternating phases). Null value indicates that the number of phases (e.g. in use) is unknown. |
| <generic> | Suspending |  | no | boolean |  | If Suspending is true, the Component can is currently suspending charging. |
| <generic> | Suspension |  | no | boolean |  | Applies to 'sensor' type Components that have a charging suspension capability, typically for safety or equipment protection reasons. If Suspension is true, the component can suspend charging when the sensed quantity is outside preset/configured limits. |
| <generic> | Temperature |  | no | decimal | Celsius, Fahrenheit | Temperature(s) of component (in Celsius, by default). Components may have multiple indexed temperature sensors. |
| <generic> | Time |  | no | dateTime |  | Point in time value, in ISO 8601 datetime format. Time zone optional. |
| <generic> | Timeout |  | no | decimal | s | Generic timeout value for Component operation (in seconds). |
| <generic> | Tries |  | no | integer |  | Number of attempts done by a Component. |
| <generic> | Tripped |  | no | boolean |  | Single-shot device requires explicit intervention to re-prime/activate to normal. |
| <generic> | VendorName |  | no | string |  | Vendor or manufacturer of component. |
| <generic> | VersionDate |  | no | dateTime |  | Version date of component in [RFC3339] format. |
| <generic> | VersionNumber |  | no | string |  | Version number of hardware |
| <generic> | VoltageImbalance |  | no | decimal | Percent | Percentage voltage imbalance in three phase supply. |
| <generic> | CommunicationParent |  | no | string |  | Points to a communication parent component (data flow source), to allow rendering the communication hierarchy in a UI. |
| <generic> | ElectricalParent |  | no | string |  | Points to a electrical parent component (energy flow source), to allow rendering the electrical hierarchy in a UI. |
| <generic> | LogicalParent |  | no | string |  | Points to a logical parent component, to allow rendering a comprehensive overview of the Charging Station components in a UI. |
| <generic> | PhysicalParent |  | no | string |  | Points to a physical parent component (container), to allow rendering an overview of the Charging Station component locations in a UI. |
| <generic> | Label |  | no | string |  | Specifies a non-unique label to be used in a hierarchy UI rendering, in place of the unique component name and instance, in case a duplicate label is needed. |
| AlignedDataCtrlr | Available |  | no | boolean |  | If this variable reports a value of true, Clock-Aligned Data is supported. |
| AlignedDataCtrlr | Enabled |  | no | boolean |  | If this variable reports a value of true, Clock-Aligned Data is enabled |
| AlignedDataCtrlr | Interval |  | yes | integer | s | Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the MeterValuesRequest or TransactionEventRequest message. |
| AlignedDataCtrlr | Measurands |  | yes | MemberList |  | Clock-aligned measurand(s) to be included in MeterValuesRequest or TransactionEventRequest, every AlignedDataInterval seconds. |
| AlignedDataCtrlr | SendDuringIdle |  | no | boolean |  | If set to true, the Charging Station SHALL NOT send clock aligned meter values when a transaction is ongoing. |
| AlignedDataCtrlr | SignReadings |  | no | boolean |  | If set to true, the Charging Station SHALL include signed meter values in the SampledValueType in theTransactionEventRequest(Ended). |
| AlignedDataCtrlr | SignUpdatedReadings |  | no | boolean |  | If set to true, the Charging Station SHALL include signed meter values in the SampledValueType in theTransactionEventRequest(Updated). |
| AlignedDataCtrlr | TxEndedInterval |  | yes | integer | s | Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the TransactionEventRequest (eventType = Ended) message. |
| AlignedDataCtrlr | TxEndedMeasurands |  | yes | MemberList |  | Clock-aligned measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended), every SampledDataTxEndedInterval seconds from the start of the transaction. |
| AlignedDataCtrlr | UpstreamInterval |  | no | integer | s | Size (in seconds) of the clock-aligned data interval, intended to be transmitted in the MeterValuesRequest message for location `Upstream` only. |
| AlignedDataCtrlr | UpstreamMeasurands |  | no | MemberList |  | Clock-aligned measurand(s) to be included in MeterValuesReques for location `Upstream` only. |
| AuthCacheCtrlr | Available |  | no | boolean |  | Authorization caching is available, but not necessarily enabled. |
| AuthCacheCtrlr | Enabled |  | no | boolean |  | If set to true, Authorizaiton caching is enabled. |
| AuthCacheCtrlr | LifeTime |  | no | integer |  | Indicates how long it takes until a token expires in the authorization cache since it is last used |
| AuthCacheCtrlr | Policy |  | no | OptionList |  | Cache Entry Replacement Policy: least recently used, least frequently used, first in first out, other custom mechanism. |
| AuthCacheCtrlr | Storage |  | no | integer | B | Indicates the number of bytes currently used by the Authorization Cache. MaxLimit indicates the maximum number of bytes that can be used by the Authorization Cache. |
| AuthCacheCtrlr | DisablePostAuthorize |  | no | boolean |  | When set to true this variable disables the behavior to request authorization for an idToken that is stored in the cache with a status other than Accepted, as stated in C10.FR.03 and C12.FR.05. |
| AuthCtrlr | AdditionalInfoItemsPerMessage |  | no | integer |  | Maximum number of AdditionalInfo items that can be sent in one message. |
| AuthCtrlr | AuthorizeRemoteStart |  | yes | boolean |  | Whether a remote request to start a transaction in the form of RequestStartTransactionRequest message should be authorized beforehand like a local action to start a transaction. |
| AuthCtrlr | Enabled |  | no | boolean |  | If set to false, then no authorization is done before starting a transaction or when reading an idToken. If an idToken was provided, then it will be put in the idToken field of the TransactionEventRequest. If no idToken was provided, then idToken in TransactionEventRequest will be left empty and type is set to NoAuthorization. |
| AuthCtrlr | LocalAuthorizeOffline |  | yes | boolean |  | Whether the Charging Station, when Offline, will start a transaction for locally-authorized identifiers |
| AuthCtrlr | LocalPreAuthorize |  | yes | boolean |  | Whether the Charging Station, when online, will start a transaction for locally-authorized identifiers without waiting for or requesting an AuthorizeResponse from the CSMS. |
| AuthCtrlr | MasterPassGroupId |  | no | string |  | IdTokens that have this id as groupId belong to the Master Pass Group. Meaning they can stop any ongoing transaction, but cannot start transactions. |
| AuthCtrlr | OfflineTxForUnknownIdEnabled |  | no | boolean |  | Support for unknown offline transactions. |
| AuthCtrlr | DisableRemoteAuthorization |  | no | boolean |  | When set to true this instructs the Charging Station to not issue any AuthorizationRequests, but only use Authorization Cache and Local Authorization List to determine validity of idTokens. |
| AuthCtrlr | SupportedIdTokenType |  | no | MemberList |  | The subset of the list of supported IdTokenTypes as defined in Appendix 7. "Standardized values for enumerations as string: IdTokenEnumStringType", that is supported by the Charging Station. |
| CHAdeMOCtrlr | SelftestActive |  | no | boolean |  | Self-test is active or self-test is started by setting to true. |
| CHAdeMOCtrlr | CHAdeMOProtocolNumber |  | no | integer |  | CHAdeMO protocol number (H'102.0) |
| CHAdeMOCtrlr | VehicleStatus |  | no | boolean |  | Vehicle status (H'102.5.3) |
| CHAdeMOCtrlr | DynamicControl |  | no | boolean |  | Vehicle is compatible with dynamic control (H'110.0.0) |
| CHAdeMOCtrlr | HighCurrentControl |  | no | boolean |  | Vehicle is compatible with high current control (H'110.0.1) |
| CHAdeMOCtrlr | HighVoltageControl |  | no | boolean |  | Vehicle is compatible with high voltage control (H'110.1.2) |
| CHAdeMOCtrlr | AutoManufacturerCode |  | no | integer |  | Auto manufacturer code (H'700.0) |
| ChargingStation | AllowNewSessionsPendingFirmwareUpdate |  | no | boolean |  | Indicates whether new sessions can be started on EVSEs, while Charging Station is waiting for all EVSEs to become Available in order to start a pending firmware update |
| ChargingStation | AvailabilityState |  | yes | OptionList |  | This variable reports current availability state for the ChargingStation |
| ChargingStation | Available |  | yes | boolean |  | Component exists |
| ChargingStation | Model |  | no | string |  | Charging station model as reported in BootNotification. |
| ChargingStation | SupplyPhases |  | yes | integer |  | Number of alternating current phases connected/available. |
| ChargingStation | VendorName |  | no | string |  | Charging station vendor name as reported in BootNotification. |
| ChargingStation | ActiveTransactionId |  | no | string |  | This variable for the ChargingStation component contains a comma-separated list of transaction IDs actively running on the Charging Station. |
| ClockCtrlr | DateTime |  | yes | dateTime |  | Contains the current date and time |
| ClockCtrlr | NextTimeOffsetTransitionDateTime |  | no | dateTime |  | Date time of the next time offset transition. |
| ClockCtrlr | NtpServerUri |  | no | string |  | This contains the address of the NTP server. |
| ClockCtrlr | NtpSource |  | no | OptionList |  | When an NTP client is implemented, this variable can be used to configure the client |
| ClockCtrlr | TimeAdjustmentReportingThreshold |  | no | integer |  | If set, then time adjustments with an absolute value in seconds larger than this need to be reported as a security event SettingSystemTime |
| ClockCtrlr | TimeOffset |  | no | string |  | A Time Offset with respect to Coordinated Universal Time (aka UTC or Greenwich Mean Time) in the form of an [RFC3339] time (zone) offset suffix, including the mandatory + or - prefix. |
| ClockCtrlr | TimeSource |  | yes | SequenceList |  | Via this variable, the Charging Station provides the CSMS with the option to configure multiple clock sources |
| ClockCtrlr | TimeZone |  | no | string |  | Configured current local time zone in the format: "Europe/Oslo", "Asia/Singapore" etc. For display purposes. |
| ConnectedEV | ProtocolAgreed |  | V2X | string |  | Information about uri and version that was agreed upon between EV and EVSE in the supportedAppProtocolReq message from ISO 15118. Example: urn:iso:15118:2:2013:MsgDef,2,0 |
| ConnectedEV | ProtocolSupportedByEV | <Priority> | V2X | string |  | Information from the supportedAppProtocolReq message from ISO 15118. Each priority is given its own variable instance. Example: urn:iso:15118:2:2013:MsgDef,2,0 |
| ConnectedEV | VehicleID |  | V2X | string |  | EVCCID (from ISO 15118 SessionSetupReq) |
| ConnectedEV | VehicleCertificate | Leaf | V2X | string |  | The PEM encoded X.509 Leaf certificate of the vehicle certificate chain |
| ConnectedEV | VehicleCertificate | SubCA1 | V2X | string |  | The PEM encoded X.509 Intermediate certificate of the vehicle certificate chain |
| ConnectedEV | VehicleCertificate | SubCA2 | V2X | string |  | The PEM encoded X.509 Intermediate certificate of the vehicle certificate chain |
| ConnectedEV | VehicleCertificate | Root | V2X | string |  | The PEM encoded X.509 Root certificate of the vehicle certificate chain |
| ConnectedEV | ACCurrent(Min/MaxSet) |  | no | decimal | A | EV min/max AC current |
| ConnectedEV | DCCurrent(Min/MaxSet) |  | no | decimal | A | EV min/max DC current |
| ConnectedEV | DCCurrent(Target) |  | no | decimal | V | EV target current from DC_ChargeLoopReq |
| ConnectedEV | DCVoltage(Min/MaxSet) |  | no | decimal | V | EV min/max DC voltage |
| ConnectedEV | DCVoltage(Target) |  | no | decimal | V | EV target voltage from DC_ChargeLoopReq |
| ConnectedEV | Power(MaxSet) |  | no | decimal | W | EV max power limit |
| ConnectedEV | DischargePower(MaxSet) |  | no | decimal | W | EV max discharge power limit |
| ConnectedEV | EnergyImport(MaxSet) |  | no | decimal | Wh | EV energy capacity / maximum energy request |
| ConnectedEV | EnergyImport(MinSet) |  | no | decimal | Wh | EV minimum energy request |
| ConnectedEV | EnergyImport(Target) |  | no | decimal | Wh | EV target energy request |
| ConnectedEV | BatteryCapacity |  | no | decimal | Wh | EV battery capacity |
| ConnectedEV | DepartureTime |  | no | DateTime |  | EV planned departure time |
| ConnectedEV | RemainingTimeBulk |  | no | integer | s | Remaining time to bulk SoC |
| ConnectedEV | RemainingTimeFull |  | no | integer | s | Remaining time to full SoC |
| ConnectedEV | StateOfChargeBulk |  | no | integer | % | Defined % for bulk SoC |
| ConnectedEV | StateOfCharge(MaxSet) |  | no | integer | % | Defined % for full SoC |
| ConnectedEV | StateOfCharge |  | no | integer | % | Current SoC |
| ConnectedEV | ChargingCompleteBulk |  | no | boolean |  | Charging to bulk SoC is complete |
| ConnectedEV | ChargingCompleteFull |  | no | boolean |  | Charging to full SoC is complete |
| ConnectedEV | ChargingState |  | no | OptionList |  | EVTerminationCode to signal error condition |
| Connector | AvailabilityState |  | no | OptionList |  | This variable reports current availability state for the Connector. Optional, because already reported in StatusNotification. |
| Connector | Available |  | yes | boolean |  | Component exists |
| Connector | ChargeProtocol |  | no | string |  | The Charging Control Protocol applicable to a Connector. CHAdeMO: CHAdeMO protocol, ISO15118: ISO15118 V2G protocol (wired or wireless) as used with CCS, CPPWM: IEC61851-1 / SAE J1772  protocol (ELV DC & PWM signalling via Control Pilot wire), Uncontrolled: No charging power management applies (e.g. Schuko socket), Undetermined: Yet to be determined (e.g. before plugged in), Unknown: Not determinable, NOTE: ChargeProtocol is distinct from and orthogonal to connectorType. |
| Connector | ConnectorType |  | yes | string |  | A value of ConnectorEnumType (See part 2) plus additionally: cGBT, cChaoJi, OppCharge. Specific type of connector, including sub-variant information. Note: Distinct and orthogonal to Charging Protocol, Power Type, Phases. |
| Connector | SupplyPhases |  | yes | integer |  | Number of alternating current phases connected/available. |
| Connector | SlotStatus |  | no | OptionList |  | Battery slot status of swapping station: Open, Locked, Faulted. |
| CPPWMController | State |  | no | string |  | IEC 61851-1 states ("A" to "E") |
| CustomizationCtrlr | CustomImplementationEnabled | <vendorId> | no | boolean |  | Custom implementation <vendorId> has been enabled. |
| CustomizationCtrlr | CustomTriggers |  | no | MemberList |  | This variable defines the names of custom triggers that Charging Station supports in a customTrigger field of TriggerMessageRequest. |
| DeviceDataCtrlr | BytesPerMessage | GetReport | yes | integer |  | Maximum number of bytes in a message related to instance name: GetReport, GetVariables, SetVariables |
| DeviceDataCtrlr | BytesPerMessage | GetVariables | yes | integer |  | Maximum number of bytes in a message related to instance name: GetReport, GetVariables, SetVariables |
| DeviceDataCtrlr | BytesPerMessage | SetVariables | yes | integer |  | Maximum number of bytes in a message related to instance name: GetReport, GetVariables, SetVariables |
| DeviceDataCtrlr | ConfigurationValueSize |  | no | integer |  | The limit to the following fields: SetVariableData.attributeValue and VariableCharacteristics.valueList. The max size of these values will always remain equal. |
| DeviceDataCtrlr | ItemsPerMessage | GetReport | yes | integer |  | Maximum number of ComponentVariable entries in message related to the instance name: GetReport, GetVariables, SetVariables |
| DeviceDataCtrlr | ItemsPerMessage | GetVariables | yes | integer |  | Maximum number of ComponentVariable entries in message related to the instance name: GetReport, GetVariables, SetVariables |
| DeviceDataCtrlr | ItemsPerMessage | SetVariables | yes | integer |  | Maximum number of ComponentVariable entries in message related to the instance name: GetReport, GetVariables, SetVariables |
| DeviceDataCtrlr | ReportingValueSize |  | no | integer |  | The limit to the following fields: GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. The max size of these values will always remain equal. |
| DeviceDataCtrlr | ValueSize |  | no | integer |  | Can be used to limit the following fields: SetVariableData.attributeValue, GetVariableResult.attributeValue, VariableAttribute.value, VariableCharacteristics.valueList and EventData.actualValue. |
| DisplayMessageCtrlr | Available |  | no | boolean |  | Whether display messages are supported. |
| DisplayMessageCtrlr | DisplayMessages |  | yes | integer |  | Amount of different messages that are currently configured in this Charging Station, via SetDisplayMessageRequest |
| DisplayMessageCtrlr | Enabled |  | no | boolean |  | Whether display messages are enabled. |
| DisplayMessageCtrlr | SupportedStates |  | yes | MemberList |  | List of the states during which to display a message supported by this Charging Station. |
| DisplayMessageCtrlr | SupportedFormats |  | yes | MemberList |  | List of message formats supported by this Charging Station. |
| DisplayMessageCtrlr | SupportedPriorities |  | yes | MemberList |  | List of the priorities supported by this Charging Station. |
| DisplayMessageCtrlr | Language |  | yes | OptionList |  | Default language code, per RFC 5646, of this Charging Station. Languages that are supported are listed in the valuesList. |
| EVSE | AllowReset |  | no | boolean |  | Can be used to announce that an EVSE can be reset individually |
| EVSE | AvailabilityState |  | yes | OptionList |  | This variable reports current availability state for the EVSE |
| EVSE | Available |  | yes | boolean |  | Component exists |
| EVSE | EvseId |  | no | string |  | The name of the EVSE in the string format as required by ISO 15118 and IEC 63119-2. |
| EVSE | Power |  | yes | decimal | W, kW | The variableCharacteristic maxLimit, that holds the maximum power that this EVSE can provide, is required. The Actual value of the instantaneous (real) power is desired, but not required. |
| EVSE | DischargePower |  | V2X | decimal | W, kW | The variableCharacteristic maxLimit holds the maximum rated discharge power that this EVSE can provide.  The variableCharacteristic maxSet holds the maximum configured discharge power that this EVSE can provide. The Actual value of the instantaneous (real) discharge power is recommended to be supported, but not required. Discharge power is represented by a positive value. |
| EVSE | SupplyPhases |  | yes | integer |  | Number of alternating current phases connected/available. |
| EVSE | DCInputPhaseControl |  | no | boolean |  | When DCInputPhaseControl is true, then the values of numberPhases and PhaseToUse in a ChargingSchedulePeriodType will select the input phases from the grid to be used by the DC EVSE. |
| EVSE | ISO15118EvseId |  | no | string |  | The name of the EVSE in the string format as required by ISO 15118 and IEC 63119-2. Example: "DE*ICE*E*1234567890*1" |
| EVSE | ChargingState |  | no | OptionList |  | This variable reports the current transaction charging state for an EVSE. |
| EVSE | ActiveTransactionId |  | no | string |  | This variable contains the transaction ID of the running transaction at the EVSE. If no transaction is active, it is an empty string. |
| FiscalMetering | EnergyExport |  | no | decimal | Wh, kWh | Total energy transferred: e.g.  from EV during (ongoing or terminated) charging session (in wH by default) |
| FiscalMetering | EnergyExportRegister |  | no | decimal | Wh, kWh | Cumulative export kWh register value, such as from a (certified) fiscal energy meter. |
| FiscalMetering | EnergyImport |  | no | decimal | Wh, kWh | Total energy transferred. |
| FiscalMetering | EnergyImportRegister |  | no | decimal | Wh, kWh | Cumulative export kWh register value, such as from a (certified) fiscal energy meter. |
| FiscalMetering | PublicKey |  | no | string |  | The public key for a meter connected to a specific EVSE. |
| ISO15118Ctrlr | CentralContractValidationAllowed |  | no | boolean |  | If this variable exists and has the value true, then Charging Station can provide a contract certificate that it cannot validate, to the CSMS for validation as part of the AuthorizeRequest. |
| ISO15118Ctrlr | ContractValidationOffline |  | yes | boolean |  | If this variable is true, then Charging Station will try to validate a contract certificate when it is offline |
| ISO15118Ctrlr | SeccId |  | no | string |  | The ID of the SECC in string format as defined by ISO15118. |
| ISO15118Ctrlr | MaxScheduleEntries |  | no | integer |  | Maximum number of allowed schedule periods. |
| ISO15118Ctrlr | RequestedEnergyTransferMode |  | no | OptionList |  | The requested energy transfer mode. |
| ISO15118Ctrlr | RequestMeteringReceipt |  | no | boolean |  | If true, then Charging Station shall request a metering receipt from EV. |
| ISO15118Ctrlr | CountryName |  | no | string |  | The countryName of the SECC in the ISO 3166-1 format. It is used as the countryName (C) of the SECC leaf certificate. Example: "DE" |
| ISO15118Ctrlr | OrganizationName |  | no | string |  | The organizationName of the CSO operating the charging station. It is used as the organizationName (O) of the SECC leaf certificate. Example: "John Doe Charging Services Ltd" Note: This value will usually be identical to SecurityCtrlr.OrganizationName, but it does not have to be. |
| ISO15118Ctrlr | PnCEnabled |  | no | boolean |  | If this variable is true, then ISO 15118 plug and charge as described by use case C07 - Authorization using Contract Certificates is enabled. If this variable is false, then ISO 15118 plug and charge as described by use case C07 - Authorization using Contract Certificates is disabled. |
| ISO15118Ctrlr | V2GCertificateInstallationEnabled |  | no | boolean |  | If this variable is true, then ISO 15118 V2G Charging Station certificate installation as described by use case A02 - Update Charging Station Certificate by request of CSMS and A03 - Update Charging Station Certificate initiated by the Charging Station is enabled.  If this variable is false, then ISO 15118 V2G Charging Station certificate installation as described by use case A02 - Update Charging Station Certificate by request of CSMS and A03 - Update Charging Station Certificate initiated by the Charging Station is disabled. |
| ISO15118Ctrlr | ContractCertificateInstallationEnabled |  | no | boolean |  | If this variable is true, then ISO 15118 contract certificate installation/update as described by use case M01 - Certificate installation EV and M02 - Certificate Update EV is enabled. If this variable is false, then ISO 15118 contract certificate installation/update as described by use case M01 - Certificate installation EV and M02 - Certificate Update EV is disabled. |
| ISO15118Ctrlr | CertificateStatusSource |  | no | MemberList |  | When present, this variable tells CSMS whether Charging Station uses OCSP or CRL to check for revoked certificates. |
| ISO15118Ctrlr | NotificationDelay |  | no | integer | s | The SECC (EVSE) uses the NotificationMaxDelay element in the EVSEStatus to indicate the time in seconds until it expects the EVCC (EV) to react on the action request indicated in EVSENotification. |
| ISO15118Ctrlr | ServiceRenegotiationSupport |  | no | boolean |  | If set to 'True' the SECC (EVSE) is capable of ServiceRenegotiation. |
| ISO15118Ctrlr | SupportedProviders |  | no | string |  | A comma-separated list of all providers (eMSPs) that are supported on this Charging Station. The providers are listed using country and provider ID from the EMAID, as defined in ISO 15118-20. |
| ISO15118Ctrlr | MaxPriceElements |  | no | integer |  | The maximum number of priceRuleStacks and priceLevelScheduleEntries that Charging Station is able to accept in a ChargingScheduleType. |
| ISO15118Ctrlr | ProtocolSupported | 1, 2 .. 20 | no | string |  | A string with the following comma-separated items:  <uri>,<major>,<minor>. <uri> is in the format as used in the SupportedAppProtocolReq message from ISO 15118-2 and ISO 15118-20. |
| LocalAuthListCtrlr | Available |  | no | boolean |  | Local Authorization List is available. |
| LocalAuthListCtrlr | BytesPerMessage |  | yes | integer |  | Maximum number of bytes in a SendLocalList message. |
| LocalAuthListCtrlr | Enabled |  | no | boolean |  | If this variable exists and reports a value of true, Local Authorization List is enabled. |
| LocalAuthListCtrlr | Entries |  | yes | integer |  | Amount of IdTokens currently in the Local Authorization List |
| LocalAuthListCtrlr | ItemsPerMessage |  | yes | integer |  | Maximum number of records in SendLocalList |
| LocalAuthListCtrlr | Storage |  | no | integer | B | Indicates the number of bytes currently used by the Local Authorization List. MaxLimit indicates the maximum number of bytes that can be used by the Local Authorization List. |
| LocalAuthListCtrlr | DisablePostAuthorize |  | no | boolean |  | When set to true this variable disables the behavior to request authorization for an idToken that is stored in the local authorization list with a status other than Accepted, as stated in C14.FR.03. |
| LocalAuthListCtrlr | SupportsExpiryDateTime |  | no | boolean |  | When set to true Charging Station will disregard idTokens for authorization as if not present in the Local Authorization List when current date/time is past the value of cacheExpiryDateTime. |
| LocalEnergyStorage | Capacity |  | no | decimal | Wh | Maximum storage capacity |
| MonitoringCtrlr | Available |  | no | boolean |  | Whether monitoring is available |
| MonitoringCtrlr | BytesPerMessage | ClearVariableMonitoring | no | integer |  | Maximum number of bytes in a ClearVariableMonitoring message. |
| MonitoringCtrlr | BytesPerMessage | SetVariableMonitoring | yes | integer |  | Maximum number of bytes in a SetVariableMonitoring message |
| MonitoringCtrlr | Enabled |  | no | boolean |  | Whether monitoring is enabled. |
| MonitoringCtrlr | ItemsPerMessage | ClearVariableMonitoring | no | integer |  | Maximum number of IDs in a ClearVariableMonitoringRequest. |
| MonitoringCtrlr | ItemsPerMessage | SetVariableMonitoring | yes | integer |  | Maximum number of setMonitoringData elements that can be sent in one setVariableMonitoringRequest message. |
| MonitoringCtrlr | OfflineQueuingSeverity |  | no | integer |  | When set and the Charging Station is offline, the Charging Station shall queue any notifyEventRequest messages triggered by a monitor with a severity number equal to or lower than the severity configured here. |
| MonitoringCtrlr | MonitoringBase |  | no | OptionList |  | Currently used monitoring base (readonly) |
| MonitoringCtrlr | MonitoringLevel |  | no | integer |  | Currently used monitoring level (readonly) |
| MonitoringCtrlr | ActiveMonitoringBase |  | no | OptionList |  | Shows the last set MonitoringBase. Valid values according MonitoringBaseEnumType: All, FactoryDefault, HardwiredOnly. |
| MonitoringCtrlr | ActiveMonitoringLevel |  | no | integer |  | Shows the currently used MonitoringLevel. Valid values are severity levels of SetMonitoringLevelRequest: 0-9. |
| MonitoringCtrlr | MaxPeriodicEventStreams |  | no | integer |  | The maximum number of open periodic event streams that Charging Station supports. |
| OCPPCommCtrlr | ActiveNetworkProfile |  | no | string |  | Indicates the configuration profile the station uses at that moment to connect to the network. |
| OCPPCommCtrlr | FileTransferProtocols |  | yes | MemberList |  | List of supported file transfer protocols |
| OCPPCommCtrlr | HeartbeatInterval |  | no | integer | s | Interval of inactivity (no OCPP exchanges) with CSMS after which the Charging Station should send HeartbeatRequest. |
| OCPPCommCtrlr | MessageTimeout | Default | yes | integer | s | MessageTimeout(Default) specifies after which time a message times out. It is configured in the network connection profile. |
| OCPPCommCtrlr | MessageAttemptInterval | TransactionEvent | yes | integer |  | MessageAttemptInterval(TransactionEvent) specifies long the Charging Station should wait before resubmitting a TransactionEventRequest message that the CSMS failed to process. |
| OCPPCommCtrlr | MessageAttempts | TransactionEvent | yes | integer |  | MessageAttempts(TransactionEvent) specifies how often the Charging Station should try to submit a TransactionEventRequest message when the CSMS fails to process it. |
| OCPPCommCtrlr | NetworkConfigurationPriority |  | yes | string |  | A comma separated ordered list of the priority of the possible Network Connection Profiles. |
| OCPPCommCtrlr | NetworkProfileConnectionAttempts |  | yes | integer |  | Specifies the number of connection attempts the Charging Station executes before switching to a different profile. |
| OCPPCommCtrlr | OfflineThreshold |  | yes | integer | s | When the offline period of a Charging Station exceeds the OfflineThreshold it is recommended to send a StatusNotificationRequest for all its Connectors. |
| OCPPCommCtrlr | PublicKeyWithSignedMeterValue |  | no | OptionList |  | This Configuration Variable can be used to configure whether a public key needs to be sent with a signed meter value. Note, that the field is required, so it needs to be present as an empty string when the public key is not sent. |
| OCPPCommCtrlr | QueueAllMessages |  | no | boolean |  | When this variable is set to true, the Charging Station will queue all message until they are delivered to the CSMS. |
| OCPPCommCtrlr | ResetRetries |  | yes | integer |  | Number of times to retry a reset of the Charging Station when a reset was unsuccessful |
| OCPPCommCtrlr | RetryBackOffRandomRange |  | no | integer |  | When the Charging Station is reconnecting, after a connection loss, it will use this variable as the maximum value for the random part of the back-off time |
| OCPPCommCtrlr | RetryBackOffRepeatTimes |  | no | integer |  | When the Charging Station is reconnecting, after a connection loss, it will use this variable for the amount of times it will double the previous back-off time. |
| OCPPCommCtrlr | RetryBackOffWaitMinimum |  | no | integer |  | When the Charging Station is reconnecting, after a connection loss, it will use this variable as the minimum back-off time, the first time it tries to reconnect. |
| OCPPCommCtrlr | UnlockOnEVSideDisconnect |  | yes | boolean |  | When set to true, the Charging Station SHALL unlock the cable on the Charging Station side when the cable is unplugged at the EV. For an EVSE with only fixed cables, the mutability SHALL be ReadOnly and the actual value SHALL be false. For a charging station with fixed cables and sockets, the variable is only applicable to the sockets. |
| OCPPCommCtrlr | WebSocketPingInterval |  | no | integer | s | 0 disables client side websocket Ping/Pong. In this case there is either no ping/pong or the server initiates the ping and client responds with Pong. Positive values are interpreted as number of seconds between pings. Negative values are not allowed. |
| OCPPCommCtrlr | FieldLength |  | no | integer |  | This variable is used to report the length of <field> in <message> when it is larger than the length that is defined in the standard OCPP message schema. |
| OCPPCommCtrlr | ExternalConfigChangeDate |  | no | DateTime |  | Date/time when the configuration was changed externally, i.e. outside of CSMS, for example by a local service action. |
| ReservationCtrlr | Available |  | no | boolean |  | Whether reservation is supported. |
| ReservationCtrlr | Enabled |  | no | boolean |  | Whether reservation is enabled. |
| ReservationCtrlr | NonEvseSpecific |  | no | boolean |  | If this configuration variable is present and set to true: Charging Station supports Reservation where EVSE id is not specified. |
| SampledDataCtrlr | Available |  | no | boolean |  | If this variable reports a value of true, Sampled Data is supported |
| SampledDataCtrlr | Enabled |  | no | boolean |  | If this variable reports a value of true, Sampled Data is enabled. |
| SampledDataCtrlr | SignReadings |  | no | boolean |  | If set to true, the Charging Station SHALL include signed meter values in the TransactionEventRequest to the CSMS |
| SampledDataCtrlr | SignStartedReadings |  |  |  |  | If set to true, the Charging Station SHALL include signed meter values for context_= `Transaction.Begin` in the metervalues field in the TransactionEventRequest(Started or Updated)+ |
| SampledDataCtrlr | SignUpdatedReadings |  |  |  |  | If set to true, the Charging Station SHALL include signed meter values in the TransactionEventRequest Updated) |
| SampledDataCtrlr | TxEndedInterval |  | yes | integer | s | Interval between sampling of metering (or other) data, intended to be transmitted in the TransactionEventRequest (eventType = Ended) message. |
| SampledDataCtrlr | TxEndedMeasurands |  | yes | MemberList |  | Sampled measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended), every SampledDataTxEndedInterval seconds from the start of the transaction. |
| SampledDataCtrlr | TxStartedMeasurands |  | yes | MemberList |  | Sampled measurand(s) to be taken at the start of any transaction to be included in the meterValues field of the first TransactionEventRequest message send at the start of a transaction (eventType = Started) |
| SampledDataCtrlr | TxUpdatedInterval |  | yes | integer | s | Interval between sampling of metering (or other) data, intended to be transmitted via TransactionEventRequest (eventType = Updated) messages |
| SampledDataCtrlr | TxUpdatedMeasurands |  | yes | MemberList |  | Sampled measurands to be included in the meterValues element of TransactionEventRequest (eventType = Ended) |
| SampledDataCtrlr | RegisterValuesWithoutPhases |  | no | boolean |  | If this variable reports a value of true, then meter values of measurand Energy.Active.Import.Register will only report the total energy over all phases without reporting the individual phase values. If this variable is absent or false, then the value for each phase is reported, possibly also with a total value (depending on the meter). |
| SampledDataCtrlr | UpstreamInterval |  | no | integer | s | Size (in seconds) of the samplng interval, intended to be transmitted in the TransactionEventyRequest message for location `Upstream` only. |
| SampledDataCtrlr | UpstreamMeasurands |  | no | MemberList |  | Sampled measurand(s) to be included in TransactionEventRequest for location `Upstream` only. |
| SecurityCtrlr | AllowSecurityProfileDowngrade |  | no | boolean |  | If this variable is implemented and set to true, then the Charging Station allows downgrading the security profile from 3 to 2. |
| SecurityCtrlr | AdditionalRootCertificateCheck |  | no | boolean |  | Required for all security profiles except profile 1. |
| SecurityCtrlr | BasicAuthPassword |  | no | passwordString |  | The basic authentication password is used for HTTP Basic Authentication. |
| SecurityCtrlr | CertificateEntries |  | yes | integer |  | Amount of Certificates currently installed on the Charging Station |
| SecurityCtrlr | CertSigningRepeatTimes |  | no | integer |  | Number of times to resend a SignCertificateRequest when CSMS does nor return a signed certificate. |
| SecurityCtrlr | CertSigningWaitMinimum |  | no | integer | s | Seconds to wait before generating another CSR in case CSMS does not return a signed certificate. |
| SecurityCtrlr | Identity |  | no | identifierString |  | The Charging Station identity. |
| SecurityCtrlr | MaxCertificateChainSize |  | no | integer |  | Limit of the size of the 'certificateChain' field from the CertificateSignedRequest |
| SecurityCtrlr | OrganizationName |  | yes | string |  | The organization name of the CSO or an organization trusted by the CSO. This organization name is used to specify the subject field in the client certificate. |
| SecurityCtrlr | SecurityProfile |  | yes | integer |  | The security profile used by the Charging Station. |
| SmartChargingCtrlr | ACPhaseSwitchingSupported |  | no | boolean |  | This variable can be used to indicate an on-load/in-transaction capability. If defined and true, this EVSE supports the selection of which phase to use for 1 phase AC charging. |
| SmartChargingCtrlr | Available |  | no | boolean |  | Whether smart charging is supported. |
| SmartChargingCtrlr | Enabled |  | no | boolean |  | Whether smart charging is enabled. |
| SmartChargingCtrlr | Entries | ChargingProfiles | yes | integer |  | Entries(ChargingProfiles) is the amount of Charging profiles currently installed on the Charging Station |
| SmartChargingCtrlr | ExternalControlSignalsEnabled |  | no | boolean |  | Indicates whether a Charging Station should respond to external control signals that influence charging. |
| SmartChargingCtrlr | LimitChangeSignificance |  | yes | decimal | Percent | If at the Charging Station side a change in the limit in a ChargingProfile is lower than this percentage, the Charging Station MAY skip sending a NotifyChargingLimitRequest or a TransactionEventRequest message to the CSMS. |
| SmartChargingCtrlr | NotifyChargingLimitWithSchedules |  | no | boolean |  | Indicates if the Charging Station should include the externally set charging limit/schedule in the message when it sends a NotifyChargingLimitRequest message. |
| SmartChargingCtrlr | PeriodsPerSchedule |  | yes | integer |  | Maximum number of periods that may be defined per ChargingSchedule. |
| SmartChargingCtrlr | Phases3to1 |  | no | boolean |  | If defined and true, this Charging Station supports switching from 3 to 1 phase during a transaction |
| SmartChargingCtrlr | ProfileStackLevel |  | yes | integer |  | Maximum acceptable value for stackLevel in a ChargingProfile. Since the lowest stackLevel is 0, this means that if SmartChargingCtrlr.ProfileStackLevel = 1, there can be at most 2 valid charging profiles per Charging Profile Purpose per EVSE. |
| SmartChargingCtrlr | RateUnit |  | yes | MemberList |  | A list of supported quantities for use in a ChargingSchedule. Allowed values: 'A' and 'W |
| SmartChargingCtrlr | ExternalConstraintsProfileDisallowed |  | no | boolean |  | Indicates whether a Charging Station allows an external system to submit limits to be represented as a `ChargingStationExternalConstraints` charging profile. |
| SmartChargingCtrlr | ChargingProfilePersistence | TxProfile | no | boolean |  | If an instance of this variable is true, then charging profiles with the chargingProfilePurpose mentioned in the variableInstance are persistent, i.e. they are stored persistently and will still exist after a reboot. |
| SmartChargingCtrlr | ChargingProfilePersistence | LocalGeneration | no | boolean |  | If an instance of this variable is true, then charging profiles with the chargingProfilePurpose mentioned in the variableInstance are persistent, i.e. they are stored persistently and will still exist after a reboot. |
| SmartChargingCtrlr | ChargingProfilePersistence | ChargingStationExternalConstraints | no | boolean |  | If an instance of this variable is true, then charging profiles with the chargingProfilePurpose mentioned in the variableInstance are persistent, i.e. they are stored persistently and will still exist after a reboot. |
| SmartChargingCtrlr | SetpointPriority |  | no | OptionList |  | Defines which setpoint shall be used when a `ChargingStationExternalConstraints` profile with a operationMode = `ExternalSetpoint` is active, but at the same time a `Tx(Default)Profile` charging profile is also active with a setpoint. |
| SmartChargingCtrlr | MaxExternalConstraintsId |  | no | integer |  | Defines the highest value that a charging profile id of a `ChargingStationExternalConstraints` profile in the Charging Station can have. |
| SmartChargingCtrlr | SupportedAdditionalPurposes |  | no | MemberList |  | This configuration variable lists the additional chargingProfilePurposes, that have been introduced in OCPP 2.1, that are supported by the Charging Station. |
| SmartChargingCtrlr | SupportsDynamicProfiles |  | no | boolean |  | When this variable has value True, then the Charging Station supports charging profiles of kind `Dynamic`. |
| SmartChargingCtrlr | SupportsMaxOfflineDuration |  | no | boolean |  | When this variable has value True, then the Charging Station supports the fields maxOfflineDuration and invalidAfterOfflineDuration in a charging profile. |
| SmartChargingCtrlr | SupportsUseLocalTime |  | no | boolean |  | When this variable has value True, then the Charging Station supports the field useLocalTime in a charging schedule. |
| SmartChargingCtrlr | SupportsRandomizedDelay |  | no | boolean |  | When this variable has value True, then the Charging Station supports the field randomizedDelay_in a charging schedule, which will delay the start of each charging schedule period by a random number between 0 and randomizedDelay. |
| SmartChargingCtrlr | SupportsLimitAtSoC |  | no | boolean |  | When this variable has value True, then the Charging Station supports the field limitAtSoC in a charging schedule, which will cap the limit or setpoint in the ChargingSchedulePeriodType by the value of _imitAtSoC.limit. |
| SmartChargingCtrlr | SupportsEvseSleep |  | no | boolean |  | When reported as true the Charging Station supports the evseSleep flag in a charging schedule period, which requests the EVSE electronics to go to sleep during operationMode = 'Idle'. |
| TariffCostCtrlr | Available | Tariff | no | boolean |  | If true then the Charging Station supports the TariffType structure, |
| TariffCostCtrlr | Available | Cost | no | boolean |  | If true, then Charging Station supports local cost calculation. |
| TariffCostCtrlr | Currency |  | yes | string |  | Currency used by this Charging Station in a ISO 4217 [ISO4217] formatted currency code. |
| TariffCostCtrlr | Enabled | Tariff | no | boolean |  | If true then the Charging Station has enabled support for the TariffType structure, that describes the tariff in a machine-readable format. |
| TariffCostCtrlr | Enabled | Cost | no | boolean |  | If true, then local cost calculation is enabled on Charging Station. |
| TariffCostCtrlr | Enabled | RunningCost | no | boolean |  | If true then Charging Station will provide periodic running cost updates in costDetails in TransactionEventRequest messages. |
| TariffCostCtrlr | TariffFallbackMessage | <language> | yes | string |  | Message (and/or tariff information) to be shown to an EV Driver when there is no driver specific tariff information available. |
| TariffCostCtrlr | TotalCostFallbackMessage | <language> | yes | string |  | Message to be shown to an EV Driver when the Charging Station cannot retrieve the cost for a transaction at the end of the transaction. |
| TariffCostCtrlr | OfflineTariffFallbackMessage | <language> | no | string |  | Message (and/or tariff information) to be shown to an EV Driver when Charging Station is offline. |
| TariffCostCtrlr | Interval | Tariff | no | integer | s | Interval specifies the maximum interval in seconds to use when evaluating the conditions regarding current, power and energy of a tariff element during a transaction. |
| TariffCostCtrlr | Interval | Cost | no | integer | s | Specifies the interval in seconds to use to provide periodic running cost updates during a transaction. |
| TariffCostCtrlr | MaxElements | Tariff | no | integer |  | Specifies the maximum number of prices elements that the Charging Station supports in each energy, chargingTime, idleTime and fixedFee field of a TariffType. |
| TariffCostCtrlr | ConditionsSupported | Tariff | no | boolean |  | If set to true the Charging Station supports tariffs with conditions. |
| TariffCostCtrlr | HandleFailedTariff | Tariff | no | OptionList |  | This configuration determines how to act when a driver-specific tariff is received, which cannot be processed. |
| TokenReader | Token |  | no | string |  | String of bytes representing an ID token. |
| TokenReader | TokenType |  | no | OptionList |  | Type of Token. Value is one of IdTokenEnumType. |
| TxCtrlr | ChargingTime |  | no | decimal | s | Time from earliest to latest substantive energy transfer |
| TxCtrlr | EVConnectionTimeOut |  | yes | integer | s | Interval from between "starting" of a transaction until incipient transaction is automatically canceled, due to failure of EV driver to (correctly) insert the charging cable connector(s) into the appropriate socket(s). |
| TxCtrlr | MaxEnergyOnInvalidId |  | no | integer |  | Maximum amount of energy in Wh delivered when an identifier is deauthorized by the CSMS after start of a transaction. |
| TxCtrlr | StopTxOnEVSideDisconnect |  | yes | boolean |  | When set to true, the Charging Station SHALL deauthorize the transaction when the cable is unplugged from the EV. |
| TxCtrlr | StopTxOnInvalidId |  | yes | boolean |  | Whether the Charging Station will deauthorize an ongoing transaction when it receives a non- Accepted authorization status in TransactionEventResponse for this transaction. |
| TxCtrlr | TxBeforeAcceptedEnabled |  | no | boolean |  | Allow charging before having received a BootNotificationResponse with RegistrationStatus: Accepted. |
| TxCtrlr | TxStartPoint |  | yes | MemberList |  | Defines when the Charging Station starts a new transaction |
| TxCtrlr | TxStopPoint |  | yes | MemberList |  | Defines when the Charging Station ends a transaction |
| TxCtrlr | ResumptionTimeout |  | no | integer | s | This variable defines the maximum number of seconds that a transaction may be interrupted by a power outage and still be resumed afterwards. |
| TxCtlrl | EnergyTransferResumptionRandomRange |  | no | integer | s | Maximum length of random time to delay resumption of energy transfer after an interruption |
| TxCtrlr | AllowEnergyTransferResumption |  | no | boolean |  | This variable defines whether energy transfer is allowed to be resumed when the transaction is resumed after a reset or power outage. |
| TxCtrlr | SupportedLimits |  | no | MemberList |  | This variable defines which transaction limits in TransactionLimitType are supported by the Charging Station. |
| V2XChargingCtrlr | Enabled |  | yes | boolean |  | Way for the CSMS to either activate or deactivate V2X functionality on a Charging Station. |
| V2XChargingCtrlr | SupportedEnergyTransferModes |  | yes | MemberList |  | Lists the energy transfer services that are supported by the Charging Station. |
| V2XChargingCtrlr | SupportedOperationModes |  | yes | MemberList |  | Lists the operation modes that are supported by the Charging Station. |
| V2XChargingCtrlr | LocalFrequencyUpdateThreshold |  | no | boolean |  | The amount of change in net frequency in *mHz* is needed to trigger a recalculation of the setpoint. |
| V2XChargingCtrlr | TxStartedMeasurands | <OperationMode> | no | MemberList |  | List of sampled measurands to send in addition to those configured in SampledDataCtrlr.TxStartedMeasurands, when the Charging Station is in V2X operation mode <OperationMode> |
| V2XChargingCtrlr | TxEndedMeasurands | <OperationMode> | no | MemberList |  | List of sampled measurands to send in addition to SampledDataCtrlr.TxEndedMeasurands, when the Charging Station is in V2X operaion mode <OperationMode>. |
| V2XChargingCtrlr | TxUpdatedMeasurands | <OperationMode> | no | MemberList |  | List of sampled measurands to send in addition to SampledDataCtrlr.TxUpdatedMeasurands, when the Charging Station is in V2X operation mode <OperationMode>. |
| V2XChargingCtrlr | TxEndedInterval | <OperationMode> | no | integer | s | The interval used to sample the list of measurands in V2XChargingCtrlr.TxEndedMeasurands, while the Charging Station is in V2X operation mode <OperationMode>. |
| V2XChargingCtrlr | TxUpdatedInterval | <OperationMode> | no | integer | s | The interval used to sample the list of measurands in V2XChargingCtrlr.TxUpdatedMeasurands, while the Charging Station is in V2X operation mode <OperationMode>. |
| V2XChargingCtrlr | LocalLoadBalancing | UpperThreshold | no | decimal | W | When power (in Watts) exceeds this limit, the local load balancing mechanism will try to imit the power to a maximum of UpperThreshold + UpperOffset. |
| V2XChargingCtrlr | LocalLoadBalancing | LowerThreshold | no | decimal | W | When power (in Watts) drops below this limit, the local load balancing mechanism will try to keep the power to a minimum of LowerThreshold + LowerOffset. |
| V2XChargingCtrlr | LocalLoadBalancing | UpperOffset | no | decimal | W | An offset value (in Watts) to add to the UpperThreshold. This allows for some tuning of the upper limit without changing the threshold value. |
| V2XChargingCtrlr | LocalLoadBalancing | LowerOffset | no | decimal | W | An offset value (in Watts) to add to the LowerThreshold. This allows for some tuning of the lower limit without changing the threshold value. |
| FrequencySimulator | Enabled |  | no | boolean |  | This variable must be set to true in order to activate the FrequencySimulator and gather data with the DataCollector. |
| FrequencySimulator | DateTime | Start | no | DateTime |  | If _Enabled_ the FrequencySimulator will simulate a net frequency as long as time >= DateTime["Start"] and time < DateTime["End"]. |
| FrequencySimulator | DateTime | End | no | DateTime |  | If _Enabled_ the FrequencySimulator will simulate a net frequency as long as time >= DateTime["Start"] and time < DateTime["End"]. |
| FrequencySimulator | FrequencySchedule |  | no | string |  | A JSON-formatted string with an array of { time, freq } pairs. |
| DataCollector | Enabled |  | no | boolean |  | This variable must be set to True in order to activate the DataCollector. |
| DataCollector | DateTime | Start | no | DateTime |  | If _Enabled_ the DataCollector will sample measurandes from SampledMeasurands as long as time >= DateTime["Start"] and time < DateTime["End"]. |
| DataCollector | DateTime | End | no | DateTime |  | If _Enabled_ the DataCollector will sample measurandes from SampledMeasurands as long as time >= DateTime["Start"] and time < DateTime["End"]. |
| DataCollector | SamplingInterval |  | no | decimal | s | The sampling interval in seconds. |
| DataCollector | SampledMeasurands |  | no | MemberList |  | The set of measurands to be sampled by the DataCollector. |
| DCDERCtrlr | Enabled |  | no | boolean |  | Whether DC DER control is enabled and DER capabilities are reported in this component. |
| DCDERCtrlr | MaxW |  | yes | decimal | W | Active power rating in watts at unity power factor |
| DCDERCtrlr | OverExcitedW |  | yes | decimal | W | Active power rating in watts at specified over-excited power factor |
| DCDERCtrlr | OverExcitedPF |  | yes | decimal |  | Over-excited power factor |
| DCDERCtrlr | UnderExcitedW |  | yes | decimal | W | Active power rating in watts at specified under-excited power factor |
| DCDERCtrlr | UnderExcitedPF |  | yes | decimal |  | Under-excited power factor |
| DCDERCtrlr | MaxVA |  | yes | decimal | VA | Maximum apparent power rating in voltamperes |
| DCDERCtrlr | MaxVar |  | yes | decimal | Var | Maximum injected reactive power rating in vars |
| DCDERCtrlr | MaxVarNeg |  | yes | decimal | Var | Maximum absorbed reactive power rating in vars |
| DCDERCtrlr | MaxChargeRateW |  | yes | decimal | W | Maximum active power charge rating in watts |
| DCDERCtrlr | MaxChargeRateVA |  | yes | decimal | VA | Maximum apparent power charge rating in voltamperes; may differ from the apparent power maximum rating |
| DCDERCtrlr | VNom |  | no | decimal | V | Nominal ac voltage rating in rms volts |
| DCDERCtrlr | MaxV |  | no | decimal | V | Maximum ac voltage rating in rms volts |
| DCDERCtrlr | MinV |  | no | decimal | V | Minimum ac voltage rating in rms volts |
| DCDERCtrlr | ModesSupported |  | yes | MemberList |  | Indication of support for each control mode function |
| DCDERCtrlr | InverterManufacturer |  | yes | string |  | Manufacturer of inverter |
| DCDERCtrlr | InverterModel |  | yes | string |  | Model of inverter |
| DCDERCtrlr | InverterSerialNumber |  | no | string |  | Serial number of inverter |
| DCDERCtrlr | InverterSwVersion |  | yes | string |  | Software version of inverter |
| DCDERCtrlr | InverterHwVersion |  | yes | string |  | Hardware version of inverter |
| DCDERCtrlr | IslandingDetectionMethod |  | no | OptionList |  | Type of IslandingDetectionMethod |
| DCDERCtrlr | IslandingDetectionTripTime |  | no | decimal | s | Time until tripping after island detection |
| DCDERCtrlr | ReactiveSusceptance |  | yes | decimal | s | Reactive susceptance that remains connected to the electrical power system in the cease to energize and trip state |
| ACDERCtrlr | ModesSupported |  | yes | MemberList |  | Indication of support for each control mode function |
| BatterySwapCtrlr | TargetSoC |  | no | integer | % | The state of charge that a battery must have in order to be eligible for swapping. |
| BatterySwapCtrlr | MaxSoc |  | no | integer | % | The maximum state of charge that a battery will be charged to. |
| BatterySwapCtrlr | IdToken |  | no | string |  | The idToken that is used for charging transactions of swap batteries. |
| BatterySwapCtrlr | Timeout | In | no | integer | s | imeout in seconds in which a set of batteries must be inserted after successful authorization. |
| BatterySwapCtrlr | Timeout | Out | no | integer | s | Timeout in seconds in which the set of batteries that is offered by Charging Station to take out in exchange for the inserted set of batteries must be removed. |
| BatteryCartridge | SoC |  | no | integer | % | The component BatteryCartridge refers to the battery that is inserted at the EVSE. The variable SoC represents current state of charge as a percentage from 0..100. |
| BatteryCartridge | SoH |  | no | integer | % | The component BatteryCartridge refers to the battery that is inserted at the EVSE. The variable SoH represents current state of health as a value from 0..100. |
| BatteryCartridge | WorkingMode |  | no | OptionList |  | This variable represents the current working mode of the battery. |
| NetworkConfiguration | OcppCsmsUrl |  | yes | string |  | URL of the CSMS (without the Charging Station Identity) |
| NetworkConfiguration | OcppInterface |  | yes | OptionList |  | OptionList of values of OcppInterfaceEnumType. |
| NetworkConfiguration | OcppTransport |  | yes | OptionList |  | OptionList of values of OCPPTransportEnumType. Is always "JSON". |
| NetworkConfiguration | OcppVersion |  | yes | OptionList |  | OptionList of values of OcppVersionEnumType. This field is ignored. |
| NetworkConfiguration | MessageTimeout |  | yes | integer |  | Duration in seconds before a message send by the Charging Station via this network connection times out. |
| NetworkConfiguration | SecurityProfile |  | yes | integer |  | Security profile level. |
| NetworkConfiguration | Identity |  | no | string |  | Required if SecurityCtrlr/Identity is ReadWrite |
| NetworkConfiguration | BasicAuthPassword |  | yes | string |  | Writing to this variable only sets the password for the instance configurationSlot of Component NetworkConfiguration. |
| NetworkConfiguration | CsmsRootCertificateHashAlgorithm |  | no | string |  | References a specific CSMS Root Certificate which has to be contained in the chain. |
| NetworkConfiguration | CsmsRootCertificateIssuerKeyHash |  | no | string |  | References a specific CSMS Root Certificate which has to be contained in the chain. |
| NetworkConfiguration | CsmsRootCertificateIssuerNameHash |  | no | string |  | References a specific CSMS Root Certificate which has to be contained in the chain. |
| NetworkConfiguration | CsmsRootCertificateSerialNumber |  | no | string |  | References a specific CSMS Root Certificate which has to be contained in the chain. |
| NetworkConfiguration | VpnEnabled |  | yes | boolean |  | True: VPN is configured. |
| NetworkConfiguration | VpnType |  | no | string |  | Value from VPNEnumType |
| NetworkConfiguration | VpnServer |  | no | string |  | VPN server address |
| NetworkConfiguration | VpnUser |  | no | string |  | VPN user name |
| NetworkConfiguration | VpnGroup |  | no | string |  | VPN group name |
| NetworkConfiguration | VpnPassword |  | no | string |  | VPN password |
| NetworkConfiguration | VpnKey |  | no | string |  | VPN shared secret |
| NetworkConfiguration | ApnEnabled |  | yes | boolean |  | True: APN is configured. |
| NetworkConfiguration | Apn |  | no | string |  | Access Point Name as URL |
| NetworkConfiguration | ApnUserName |  | no | string |  | APN user name |
| NetworkConfiguration | ApnPassword |  | no | string |  | APN password |
| NetworkConfiguration | SimPin |  | no | string |  | SIM card PIN code |
| NetworkConfiguration | PreferredNetwork |  | no | string |  | Preferred network as concatenation of MCC and MNC |
| NetworkConfiguration | UseOnlyPreferredNetwork |  | no | boolean |  | When true use only the preferred network |
| NetworkConfiguration | ApnAuthentication |  | no | string |  | Value from APNAuthenticationEnumType |
| PaymentCtrlr | Enabled |  | yes | boolean |  | Payment terminal support is enabled. |
| PaymentCtrlr | Problem |  | yes | boolean |  | There's a problem with the payment terminal. |
| PaymentCtrlr | AuthorizeDirectPayment |  | yes | boolean |  | If true, an AuthorizeRequest must be sent to CSMS to approve the direct payment. |
| PaymentCtrlr | AuthorizationAmount |  | yes | decimal |  | Amount used for the pre-authorization. |
| PaymentCtrlr | IncrementalAuthorizationAmount |  | no | decimal |  | If value is 0, then incremental authorization is not allowed. Variable will be absent if Charging Station or payment terminal do not support incremental authorization. |
| PaymentCtrlr | IncrementalAuthorizationThreshold |  | no | decimal |  | If costs exceed current authorization amount minus IncrementalAuthorizationThreshold then the authorization needs to be increased. |
| PaymentCtrlr | PaymentDetails |  | yes | MemberList |  | The _valuesList_ of PaymentDetails contains the information that the payment terminal is able to provide. The Actual value of PaymentDetails determines which of these details shall be provided in the idToken.additionInfo field. |
| PaymentCtrlr | SettlementByCSMS |  | yes | boolean |  | When true, CSMS will take care of settlement |
| PaymentCtrlr | ReceiptServerUrl |  | yes | string |  | URL to the receipt server, where an EV driver can find the receipt afterwards. |
| PaymentCtrlr | ReceiptByCSMS |  | yes | boolean |  | When true, CSMS will provide a URL to receipt, else it is provided by payment terminal. |
| PaymentCtrlr | Merchant | Id | yes | string |  | Merchant ID to be added to a PSP/locally generated receipt. |
| PaymentCtrlr | Merchant | TaxId | yes | string |  | Tax ID of the merchant to be added to a PSP/locally generated receipt. |
| PaymentCtrlr | Merchant | Name | yes | string |  | Name of the merchant to be added to a PSP/locally generated receipt. |
| PaymentCtrlr | Merchant | Address | yes | string |  | Address of the merchant to be added to a PSP/locally generated receipt. |
| PaymentCtrlr | Merchant | City | yes | string |  | City of the merchant to be added to a PSP/locally generated receipt. |
| PaymentCtrlr | TerminalID |  | yes | string |  | Terminal ID of the payment terminal. |
| PaymentCtrlr | PaymentServiceProvider |  | yes | string |  | The payment service provider that the terminal is using. Typically read-only. |
| PaymentCtrlr | VendorName |  | yes | string |  | Manufacturer of the payment terminal. |
| PaymentCtrlr | Model |  | yes | string |  | Model of the payment terminal. |
| PaymentCtrlr | SerialNumber |  | yes | string |  | Payment terminal serial number. |
| PaymentCtrlr | FirmwareVersion |  | yes | string |  | Payment terminal firmware version. |
| PaymentCtrlr | IMSI |  | yes | string |  | IMSI of the payment terminals SIM card. |
| PaymentCtrlr | ICCID |  | yes | string |  | ICCID of the payment terminals SIM card. |
| PaymentCtrlr | Connected |  | yes | boolean |  | Boolean to indicate whether the payment terminal is connected to its payment service provider. |
| WebPaymentsCtrlr | URLTemplate |  | yes | string |  | URL template |
| WebPaymentsCtrlr | URLParameters |  | no | MemberList |  | List of supported URL parameters, valuesList: "maxtime", "maxenergy", "maxcost".  When absent, none of these are supported. |
| WebPaymentsCtrlr | TOTPVersion |  | yes | string |  | Version of TOTP algorithm.  valuesList: list of supported TOTP versions, e.g. "v1" |
| WebPaymentsCtrlr | ChargingStationId |  | no | string |  | Charging station Id to use in URL.  When absent will default to Charging Station identity, as defined in SecurityCtrlr.Identity. |
| WebPaymentsCtrlr | ValidityTime |  | yes | integer | s | Time in seconds to show QR, e.g. 30 |
| WebPaymentsCtrlr | SharedSecret |  | yes | string |  | <random text> set to a random value on first boot |
| WebPaymentsCtrlr | Length |  | yes | integer |  | Length of TOTP, e.g. 8 |
| WebPaymentsCtrlr | QRCodeQuality |  | no | OptionList |  | Low, Medium, Quartile, High |

## Variables (240)

| Name | DataType | Unit | Description |
| --- | --- | --- | --- |
| ACCurrent | decimal | A | RMS AC Current (in amperes). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average of all per-phase readings and written values are common per-phase settings. Example(s): ChargingStation: Total AC current consumption (all EVSE’s, ancillaries), EVSE: Total current consumed by EVSE: includes losses (AC->DC) and EVSE specific ancillaries (e.g. fans), ElectricalFeed: Inflow AC current on feed |
| ACPhaseSwitchingSupported | boolean |  | If defined and true, this EVSE supports the selection of which phase to use for 1 phase AC charging. |
| ACVoltage | decimal | V | RMS AC Voltage (in volts). For 3-phase circuits, each phase (and optional neutral) is represented by a Variable instance equal to a value of the PhaseEnumType (e.g. L1,N). Unkeyed values reported for a Component declared to be multi-phase are assumed to be an average ofall per-phase readings and written values are common per-phase settings. Example(s): ElectricalFeed: Input Voltage |
| Active | boolean |  | Component is in its non-resting / active state: e.g: On, Engaged, Locked. Some Components may have secondary functions that have corresponding Active Variables with an explicit Variable instance., Note: Monitoring of changes in the Active state of any Component can be specified by setting Delta monitoring on the boolean value with a delta values of 1. Setting/clearing an Active Variable activates/stops the associated functionality, where remotely controllable. Only components that are Available and Enabled can be in the Active state. |
| ActiveMonitoringBase | OptionList |  | Shows the currently used MonitoringBase. |
| ActiveMonitoringLevel | integer |  | Shows the currently use MonitoringLevel. |
| ActiveNetworkProfile | boolean |  | Indicates the configuration profile the station uses to connect to the network. |
| ActiveTransactionId | string |  | Active transaction on charging station or EVSE. |
| AdditionalInfoItemsPerMessage | integer |  | Maximum number of _additionalInfo_ items that can be sent in one message. |
| AdditionalRootCertificateCheck | boolean |  | When set to true, only one certificate (plus a temporarily fallback certificate) of certificateType CSMSRootCertificate is allowed to be installed at a time. |
| AllowEnergyTransferResumption | boolean |  | This variable defines whether energy transfer is allowed to be resumed when the transaction is resumed after a reset or power outage. |
| AllowNewSessionsPendingFirmwareUpdate | boolean |  | Indicates whether new sessions can be started on EVSEs, while Charging Station is waiting for all EVSEs to become Available in order to start a pending firmware update. |
| AllowReset | boolean |  | Component can be reset. Can be used to announce that an EVSE can be reset individually. |
| AllowSecurityProfileDowngrade | boolean |  | If this variable is implemented and set to _true_, then the Charging Station allows downgrading the security profile from 3 to 2. |
| Angle | decimal | Deg | Angle(s) relative to normal/design idle position. Multiple Variable instance values may be used to indicate angular position in multiple axes (e.g. Left-Right, Forward-Back). |
| Attempts | integer |  | Number of attempts (INCLUDING the original attempt) in the last successful or attempted, cycle of operation. Applies typically to self-monitoring motorized electro-mechanical equipment, etc. {Null}: Unknown, 0: Not Attempted/Not allowed, 1: Single attempt/No retries [allowed], 2-N: [up to] N tries [allowed] |
| AuthorizeRemoteStart | boolean |  | Whether a remote request to start a transaction in the form of RequestStartTransactionRequest message should be authorized beforehand like a local action to start a transaction. |
| AvailabilityState | OptionList |  | A value of ConnectorStatusEnumType (See part 2): replicates ConnectorStatus values reported in StatusNotification messages. |
| Available | boolean |  | The Component exists and is locally configured/wired for use, but might not be (remotely) Enabled. |
| BasicAuthPassword | string |  | The basic authentication password is used for HTTP Basic Authentication. |
| BytesPerMessage | integer |  | Message Size (in bytes) - puts constraint on GetReportRequest, GetMonitoringReportRequest or GetVariableRequest message size. |
| CentralContractValidationAllowed | boolean |  | If this variable exists and has the value _true_, then Charging Station can provide a contract certificate that it cannot validate, to the CSMS for validation as part of the AuthorizeRequest. |
| CertSigningRepeatTimes | integer |  | This variable can be used to configure the amount of times the Charging Station SHALL double the previous back-off time, starting with the number of seconds configured at CertSigningWaitMinimum, every time the back-off time expires without having received the CertificateSignedRequest containing the from the CSR generated signed certificate. |
| CertSigningWaitMinimum | integer |  | This configuration variable defines how long the Charging Station has to wait before generating another CSR, in the case the CSMS accepts the SignCertificateRequest, but never returns the signed certificate. |
| Certificate | string |  | Digital Certificate (in Base64 encoding) |
| CertificateEntries | integer |  | Amount of Certificates currently installed on the Charging Station. |
| CertificateStatusSource | string |  | When present, this variable tells CSMS whether Charging Station uses OCSP or CRL to check for revoked certificates. |
| ChargeProtocol | string |  | The Charging Control Protocol applicable to a Connector. CHAdeMO: CHAdeMO protocol, ISO15118: ISO15118 V2G protocol (wired or wireless) as used with CCS, CPPWM: IEC61851-1 / SAE J1772  protocol (ELV DC & PWM signalling via Control Pilot wire), Uncontrolled: No charging power management applies (e.g. Schuko socket), Undetermined: Yet to be determined (e.g. before plugged in), Unknown: Not determinable, NOTE: ChargeProtocol is distinct from and orthogonal to connectorType. |
| ChargingCompleteBulk | boolean |  | Charging up to StateOfChargeBulk has completed. |
| ChargingCompleteFull | boolean |  | Charging up to StateOfCharge.maxSet has completed. |
| ChargingProfilePersistence | boolean |  | If an instance of this variable is true, then charging profiles with the _chargingProfilePurpose_ mentioned in the *variableInstance* are persistent, i.e. they are stored persistently and will still exist after a reboot. |
| ChargingState | OptionList |  | This variable reports the current transaction charging state for an EVSE. |
| ChargingTime | decimal | s | Time from earliest to latest substantive energy transfer |
| Color | string |  | Standard 24 bit hexadecimal RGB values. Reg Green Blue color intensity, expressed as standard 24 bit hexadecimal RGB values: 3  00-FF (0-255), in order RRGGBB). E.g. 000000: Black, FF0000: Red, 00FF00: Green, 0000FF: Blue, FFFF00:Yellow, FFFFFF: White, 008000: Medium intensity green. |
| CommunicationParent | string |  | Points to a communication parent component (data flow source), to allow rendering the communication hierarchy in a UI. |
| Complete | boolean |  | Component’s operation cycle has completed. Used only in event notifications, where it is always true. |
| ConditionsSupported | boolean |  | If set to true the Charging Station supports tariffs with conditions. |
| ConfigurationValueSize | integer |  | This Configuration Variable can be used to limit the following fields: SetVariableData.attributeValue and VariableCharacteristics.valuesList. |
| ConnectedTime | decimal | s | Time since logical connection established |
| ConnectorType | OptionList |  | A value of ConnectorStringEnumType (See Appendix 7). Specific type of connector, including sub-variant information. Note: Distinct and orthogonal to Charging Protocol, Power Type, Phases. |
| ContractCertificateInstallationEnabled | boolean |  | If this variable is _true_, then ISO 15118 contract certificate installation/update as described by use case M01 - Certificate installation EV |
| ContractValidationOffline | boolean |  | If this variable is _true_, then Charging Station will try to validate a contract certificate when it is offline. |
| Count | integer |  | General purpose integer count variable for Component state reporting |
| CountryName | string |  | The countryName of the SECC in the ISO 3166-1 format. |
| Currency | string |  | Currency in a ISO 4217 formatted currency code. |
| CurrentImbalance | decimal | Percent | Percentage current imbalance in an AC three phase supply. |
| CustomImplementationEnabled | boolean |  | This standard configuration variable is used to enable/disable the custom implementation named in the *variableInstance*. |
| CustomTriggers | MemberList |  | This variable defines the names of custom triggers that Charging Station supports in a _customTrigger_ field of TriggerMessageRequest. |
| DCCurrent | decimal | A | DC Current (in amperes). May be an instantaneous measurement, or a period average, depending on context/equipment. |
| DCInputPhaseControl | boolean |  | When DCInputPhaseControl is true, then the values of _numberPhases_ and _PhaseToUse_ in a ChargingSchedulePeriodType will select the input phases from the grid to be used by the DC EVSE. |
| DCVoltage | decimal | V | DC Voltage (volts). May be an instantaneous measurement, or a period average, depending on context/equipment. |
| DataText | string |  | Text associated with a Component, e.g. a Display. |
| DateTime | dateTime |  | Point in time value, in [RFC3339] datetime format. Time zone optional. |
| DepartureTime | dateTime |  | Time in [RFC3339] datetime format, when an EV intends to leave the charging station. |
| DisablePostAuthorize | boolean |  | When set to _true_ this variable disables the behavior to request authorization for an |
| DisableRemoteAuthorization | boolean |  | When set to _true_ this instructs the Charging Station to not issue any AuthorizationRequests, but only use Authorization Cache and Local Authorization List to determine validity of idTokens. |
| DischargePower | decimal |  | The variableCharacteristic _maxLimit_ holds the maximum rated discharge power that this EVSE can provide. The variableCharacteristic _maxSet_ holds the maximum configured discharge power that this EVSE can provide. The _Actual_ value of the instantaneous (real) discharge power is recommended to be supported, but not required. Discharge power is represented by a positive value. |
| DisplayMessages | integer |  | Maximum number of different messages that can configured in this Charging Station simultaneous, via SetDisplayMessageRequest. |
| ECVariant | string |  | Production series variants reflecting internal design changes or sub-component substitutions not affecting external functionality. |
| EVConnectionTimeOut | integer | s | Interval from between 'starting' of a transaction until incipient transaction is automatically canceled, due to failure of EV driver to (correctly) insert the charging cable connector(s) into the appropriate socket(s). |
| ElectricalParent | string |  | Points to a electrical parent component (energy flow source), to allow rendering the electrical hierarchy in a UI. |
| Enabled | boolean |  | The Component is Enabled for operation. For Available components that cannot be selectively (remotely) enabled / disabled, this value is always true. Note: Available cannot be false of Enabled is true, so during inventory reporting, Enabled=1 also logically states Available=true |
| Energy | decimal | Wh | Energy quantity (in Wh) for reporting/configuring values related to stored energy (i.e. not transferred energy). |
| EnergyCapacity | decimal | Wh | Energy capacity in Wh of an energy storage device. |
| EnergyExport | decimal | Wh | Total energy transferred: e.g.  from EV during (ongoing or terminated) charging session (in wH by default) |
| EnergyExportRegister | decimal | Wh | Cumulative export kWh register value, such as from a (certified) fiscal energy meter. |
| EnergyImport | decimal | Wh | Total energy transferred. |
| EnergyImportRegister | decimal | Wh | Cumulative export kWh register value, such as from a (certified) fiscal energy meter. |
| Entries | integer |  | General purpose variable for reporting/managing numbers of entries in repetitive data structures. maxLimit characteristic reports maximum possible entries. |
| ExternalConfigChangeDate | DateTime |  | Date/time when the configuration was changed externally, i.e. outside of CSMS, for example by a local service action. |
| ExternalConstraintsProfileDisallowed | boolean |  | Indicates whether a Charging Station allows an external system to submit a `ChargingStationExternalConstraints` charging profile. |
| ExternalControlSignalsEnabled | boolean |  | Indicates whether a Charging Station is able to respond to external control signals that influence charging. If the variable is true, but CSMS has set <<configkey-external-constraints-profile-disallowed>> = true, then external control signals are only allowed during a charging profile with a _chargingProfilePeriod_ = `ExternalLimits` or `ExternalSetpoint`. |
| Fallback | boolean |  | Component is operating in a fallback, or backup mode. In inventory reports, a Value of 1 for the maxLimit characteristic indicates that the component can enter a fallback state (i.e. a fallback mode is present). |
| FanSpeed | decimal | RPM | Fan Speed (in RPM). A value of 0 represents stopped/stalled. An empty value indicates that fan speed cannot be read. |
| FieldLength | integer |  | This variable is used to report the length of <field> in <message> when it is larger |
| FileTransferProtocols | MemberList |  | List of supported file transfer protocols. |
| FirmwareVersion | string |  | Version number of firmware. |
| Force | decimal | N | Reports (impact) force/ acceleration values (estimates) in one or more directions, in units of Newtons or “g”. Multiple force readings in different (orthogonal) dimensions may be reported using Variable instance values, such as Down, Right, Forward. |
| Formats | MemberList |  | List of message formats supported by this Charging Station. Possible values: ASCII, HTML, URI, UTF-8. |
| Frequency | decimal | Hz | Frequency of AC power, signal, or component operation. |
| FrequencySchedule | string |  | A JSON-formatted string with an array of { _time, freq_ } pairs, in which _time_ is |
| FuseRating | decimal | A | Current rating of a fuse/breaker. Variable instances keyed by phase identifier (L1/L2/L3/N). |
| HandleFailedTariff | OptionList |  | This configuration determines how to act when a driver-specific tariff is received, which cannot be processed. |
| HeartbeatInterval | integer | s | Interval of inactivity (no OCPP exchanges) with CSMS after which the Charging Station should send HeartbeatRequest. |
| Height | decimal | m | Height above(+)/below(-) reference level (ground level unless context demands otherwise). |
| Humidity | decimal | RH | The relative humidity in %. |
| Hysteresis | decimal | Percent | Specifies the width of a 'dead band' (as a percentage of the threshold) around the central value of a threshold setting (e.g. MinSet, MaxSet, monitor thresholds) to avoid repeated triggering when the measured quantity lies close to the threshold and is subject to small variations. |
| ICCID | string |  | ICCID (Integrated Circuit Card IDentifier) of mobile data SIM card. |
| IMSI | string |  | IMSI (International Mobile Subscriber Identity) number of mobile data SIM card |
| ISO15118EvseId | string |  | EVSE ID in string format as used in ISO 15118 and IEC 63119-2 |
| IdToken | string |  | The IdToken used to authorize a charging transaction. |
| Identity | string |  | The Charging Station identity. |
| Impedance | decimal | Ohm | Impedance: Primary value is real (resistive only) impedance. Where a complex impedance is to be reported, the imaginary part (reactance) must be represented with a separate Variable instance value of 'reactance'. Reactance values are expressed at the (nominal) relevant operating frequency of the Component (e.g. 50/60Hz for mains electricity feed). |
| Interval | integer | s | Minimum Interval (in seconds) between (attempted) operations. |
| ItemsPerMessage | integer |  | Maximum number of ComponentVariable entries that can be sent in one GetReportRequest or GetMonitoringReportRequest message. |
| Label | string |  | Label for a component. Specifies a non-unique label to be used in a hierarchy UI rendering, in place of the unique component name and instance |
| Language | OptionList |  | Default language code, per RFC 5646, of this Charging Station. |
| Length | decimal | m | General Purpose linear distance measure. |
| LifeTime | integer | s | Indicates how long it takes until a token expires in the authorization cache since it is last used. |
| Light | decimal | lx | (Ambient) light level. The value is in Lux. |
| LimitChangeSignificance | decimal |  | If at the Charging Station side a change in the limit in a ChargingProfile is lower than this percentage, the Charging Station MAY skip sending a NotifyChargingLimitRequest or a TransactionEventRequest message to the CSMS. |
| LocalAuthorizeOffline | boolean |  | Whether the Charging Station, when _Offline_, will start a transaction for locally-authorized identifiers. |
| LocalFrequencyUpdateThreshold | integer | mHz | The amount of change in net frequency in *mHz* is needed to trigger a recalculation of the setpoint. |
| LocalLoadBalancing | decimal |  | Variable with instances to control local load-balancing. |
| LocalPreAuthorize | boolean |  | Whether the Charging Station, when online, will start a transaction for locally-authorized identifiers without waiting for or requesting an AuthorizeResponse from the CSMS. |
| LogicalParent | string |  | Points to a logical parent component, to allow rendering a comprehensive overview of the Charging Station components in a UI. |
| Manufacturer | string |  | Component Manufacturer name |
| MasterPassGroupId | string |  | IdTokens that have this id as groupId belong to the Master Pass Group. |
| MaxCertificateChainSize | integer |  | This configuration variable can be used to limit the size of the 'certificateChain' field from the CertificateSignedRequest PDU. |
| MaxElements | integer |  | For TariffCostCtrlr: Specifies the maximum number of _prices_ elements that the Charging Station supports in each  _energy_, _chargingTime, _idleTime_ and _fixedFee_ of a TariffType. |
| MaxEnergyOnInvalidId | integer | Wh | Maximum amount of energy in Wh delivered when an identifier is deauthorized by the CSMS after start of a transaction. |
| MaxExternalConstraintsId | integer |  | Defines the highest value that a charging profile id of a `ChargingStationExternalConstraints` profile in the Charging Station can have. |
| MaxPeriodicEventStreams | integer |  | The maximum number of open periodic event streams that Charging Station supports. |
| MaxPriceElements | integer |  | For ISO15118Ctrlr: The maximum number of _priceRuleStacks_ and _priceLevelScheduleEntries_ that Charging Station is able to accept in a ChargingScheduleType. |
| MaxSoc | integer |  | The maximum state of charge that a battery will be charged to. |
| Measurands | MemberList |  | Measurand(s) to be included in <<metervaluesrequest,MeterValuesRequest>> or <<transactioneventrequest,TransactionEventRequest>> |
| Message | string |  | Specific stored message for display. |
| MessageAttemptInterval | integer | s | How long the Charging Station should wait before resubmitting a TransactionEventRequest message that the CSMS failed to process. |
| MessageAttempts | integer |  | How often the Charging Station should try to submit a TransactionEventRequest message when the CSMS fails to process it. |
| MessageTimeout | integer | s | The purpose of the message timeout is to be able to consider a request message as not sent and continue with other tasks when the message did not arrive due to communication errors or software failure. |
| MinimumStatusDuration | integer | s | Minimum duration that a Charging Station or EVSE status is stable before StatusNotificationRequest is sent to the CSMS. |
| Mode | string |  | Operating mode string from among valid options (communicated by OptionList, etc. during capability/configuration  discovery). |
| Model | string |  | Manufacturer's Model code/number of Component, including suffixes etc. to identify functional, regional or linguistic variation, but NOT engineering change level internal 				variation not affecting external behaviour, etc. |
| NetworkAddress | string |  | Current network address of a Component. |
| NetworkConfigurationPriority | SequenceList |  | A comma separated ordered list of the priority of the possible Network Connection Profiles. The list of possible available profile slots for the network configuration profiles SHALL be reported, via the valuesList characteristic of this Variable. |
| NetworkProfileConnectionAttempts | integer |  | Specifies the number of connection attempts the Charging Station executes before switching to a different profile. |
| NextTimeOffsetTransitionDateTime | DateTime |  | Date time of the next time offset transition. On this date time, the clock displayed to the EV driver will be given the new offset as configured via `TimeOffsetNextTransition`. |
| NonEvseSpecific | boolean |  | For ReservationCtrlr: If this configuration variable is present and set to _true_: Charging Station supports reservation where EVSE id is not specified. |
| NotificationMaxDelay | integer | s | For ISO15118Ctrlr: The SECC (EVSE) uses the NotificationMaxDelay element in the EVSEStatus to indicate the time in seconds until it expects the EVCC (EV) to react on the action request indicated in EVSENotification. |
| NotifyChargingLimitWithSchedules | boolean |  | Indicates if the Charging Station should include the externally set charging limit/schedule in the message when it sends a NotifyChargingLimitRequest message. |
| NtpServerUri | string |  | This contains the address of the NTP server. |
| NtpSource | OptionList |  | Use the NTP server provided via DHCP, or use the manually configured NTP server. |
| OfflineQueuingSeverity | integer |  | When set and the Charging Station is _offline_, the Charging Station shall queue any NotifyEventRequest messages triggered by a monitor with a severity number equal to or lower than the severity configured here. |
| OfflineTariffFallbackMessage | string |  | Message (and/or tariff information) to be shown to an EV Driver when Charging Station is offline. |
| OfflineThreshold | integer | s | When the offline period of a Charging Station exceeds the `OfflineThreshold` it is recommended to send a StatusNotificationRequest for all its Connectors when the Charging Station is back online. |
| OfflineTxForUnknownIdEnabled | boolean |  | If this key exists and is true, the Charging Station supports Unknown Offline Authorization. |
| Operated | boolean |  | The Component operated in an instantaneous, transient, or immediately self-resetting pattern. Used only in event notifications, where it is always true. |
| OperatingTimes | string |  | Recurring operating times in iCalendar RRULE format. |
| OrganizationName | string |  | The organizationName of the CSO operating the charging station. |
| Overload | boolean |  | Component is in Overload state. |
| Percent | decimal | Percent | Generic dimensionless value reporting/setting value. |
| PeriodsPerSchedule | integer |  | Maximum number of periods that may be defined per ChargingSchedule. |
| PhaseRotation | string |  | This variable describes the phase rotation of a Component relative to its parent Component, using a |
| Phases3to1 | boolean |  | If defined and true, this Charging Station supports switching from 3 to 1 phase during a transaction. |
| PhysicalParent | string |  | Points to a physical parent component (container), to allow rendering an overview of the Charging Station component locations in a UI. |
| PnCEnabled | boolean |  | If this variable is _true_, then ISO 15118 plug and charge as described by use case C07 - Authorization using Contract Certificates is enabled. |
| Policy | OptionList |  | Cache Entry Replacement Policy: least recently used, least frequently used, first in first out, other custom mechanism. |
| PostChargingTime | decimal | s | Elapsed time in seconds since last substantive energy transfer |
| Power | decimal | W,kW | Instantaneous (real) Power (measured/calculated, including power factor for AC). Where a component (e.g. AC to DC Power Converter) has multiple power measurements, the default (unkeyed) instance is “input” power. |
| Present | boolean |  | Component exists, but might not be locally configured/wired for use, nor (remotely) Enabled. |
| Problem | boolean |  | Component itself has a 'Problem' condition that impacts in any significant way on its normal operation. By definition, 'Problem' state includes (logical OR) 'Fault' state. 'Problem' specifically INCLUDES inability to operate that is propagated (up/down/sideways) from any other associated/connected/containing/contained Component. |
| ProfileStackLevel | integer |  | Maximum acceptable value for _stackLevel_ in a ChargingProfile. |
| Protecting | boolean |  | Applies to 'sensor' type Components that have an associated protection capability, whereby they can  disconnect power (e.g. using the main PowerContactor) if the sensed quantity is outside preset/configured limits. If Protecting is true, the Component is actively preventing/interrupting charging. |
| ProtocolAgreed | string |  | For ConnectedEV: A string with the following comma-separated items: “<uri>,<major>,<minor>”. This is the protocol uri and version information that was agreed upon between EV and EVSE in the supportedAppProtocolReq handshake from ISO 15118. |
| ProtocolSupported | string |  | For ISO15118Ctrlr: A string with the following comma-separated items: “<uri>,<major>,<minor>”. <uri> is in the format as used in the SupportedAppProtocolReq message from ISO 15118-2 and ISO 15118-20. This variable has at most 20 instances, one for each supported protocol version. |
| ProtocolSupportedByEV | string |  | For ConnectedEV: A string with the following comma-separated items: “<uri>,<major>,<minor>”. This is information from the SupportedAppProtocolReq message from ISO 15118. Each priority is given its own variable instance. Priority is a number from 1 to 20 as a string. |
| PublicKey | string |  | Configuration variable that can be used to retrieve the public key for a meter connected to a specific EVSE. |
| PublicKeyWithSignedMeterValue | boolean |  | This Configuration Variable can be used to configure whether a public key needs to be sent with a signed meter value. |
| QueueAllMessages | boolean |  | When this variable is set to _true_, the Charging Station will queue all message until they are delivered to the CSMS. |
| RateUnit | string |  | A list of supported quantities (A, W) for use in a ChargingSchedule. |
| RegisterValuesWithoutPhases | boolean |  | If this variable reports a value of _true_, then meter values of measurand `Energy.Active.Import.Register` will only report the total energy over all phases without reporting the individual phase values. |
| RemainingTimeBulk | integer | s | Number of seconds remaining to charge to bulk state of charge, given by StateOfChargeBulk. |
| RemainingTimeFull | integer | s | Number of seconds remaining to charge to 100% state of charge. |
| ReportingValueSize | integer |  | This Configuration Variable can be used to limit the following fields: GetVariableResult.attributeValue, VariableAttribute.value and EventData.actualValue. |
| RequestMeteringReceipt | boolean |  | For ISO15118Ctrlr: If this variable is _true_, then Charging Station shall request a metering receipt |
| ResetRetries | integer |  | Number of times to retry a reset of the Charging Station when a reset was unsuccessful. |
| ResumptionTimeout | integer | s | This variable defines the maximum number of seconds that a transaction may be interrupted by a power outage and still be resumed afterwards. |
| SampledMeasurands | MemberList |  | The set of measurands to be sampled by the DataCollector component. |
| SamplingInterval | decimal | s | The sampling interval in *seconds*. |
| SeccId | string |  | The name of the SECC in the string format as required by ISO 15118. |
| SecurityProfile | integer |  | This configuration variable is used to report the security profile used by the Charging Station. |
| SendDuringIdle | boolean |  | For AlignedDataCtrlr: If set to _true_, the Charging Station SHALL only send clock aligned meter values when there is no transaction ongoing. |
| SerialNumber | string |  | Serial number of Component. |
| ServiceRenegotiationSupport | boolean |  | For ISO15118Ctrlr: If set to 'True' the SECC (EVSE) is capable of ServiceRenegotiation. |
| SetpointPriority | OptionList |  | Defines which _setpoint_ shall be used when a `ChargingStationExternalConstraints` profile |
| SignReadings | boolean |  | If set to _true_, the Charging Station SHALL include signed meter values in the TransactionEventRequest(Ended). |
| SignStartedReadings | boolean |  | If set to _true_, the Charging Station SHALL include signed meter values for _context_ = `Transaction.Begin` in the _metervalues_ field in the TransactionEventRequest(Started or Updated). |
| SignUpdatedReadings | boolean |  | If set to _true_, the Charging Station SHALL include signed meter values in the _metervalues_ field in the TransactionEventRequest(Updated). |
| SignalStrength | decimal | dBm | (Radio/Wired/Optical) data signal strength, in ASU (typically 0-31 or 99 for unknown). Or dbmW (typically -140 to -50). |
| SlotStatus | OptionList |  | This variable represents the status of the door of the battery slot. |
| SoC | integer | Percent | SoC of the component BatteryCartridge which refers to the battery that is inserted at the EVSE. |
| SoH | integer | Percent | SoH of the component BatteryCartridge which refers to the battery that is inserted at the EVSE. |
| State | string |  | A state code or name identifier string, to allow the internal state of  components to be reported and/or  controlled |
| StateOfCharge | decimal | Percent | Energy Storage Device (e.g. battery) state of charge, expressed as a percentage of nominal design 0-100% operating range. The value of StateOfCharge.maxSet represents the maximum state of charge for a full battery and is usually at or near 100%. |
| StateOfChargeBulk | decimal | Percent | Energy Storage Device (e.g. battery) state of charge up to which fast charging is possible. Above this percentage charging speed will drop significantly. |
| StopTxOnEVSideDisconnect | boolean |  | When set to _true_, the Charging Station SHALL deauthorize the transaction when the cable is unplugged from the EV. |
| StopTxOnInvalidId | boolean |  | Whether the Charging Station will deauthorize an ongoing transaction when it receives a non- _Accepted_ authorization status in TransactionEventResponse for this transaction. |
| Storage | integer | B | In bytes. Amount of storage occupied. Storage(maxLimit) specifies absolute limit Storage(MaxSet) restricts usage to specified Max, if supported. |
| SupplyPhases | integer |  | Number of alternating current phases connected/available. 1 or 3 for AC, 0 means DC (no alternating phases). Null value indicates that the number of phases (e.g. in use) is unknown. |
| SupportedAdditionalPurposes | MemberList |  | This configuration variable lists the additional charging profile purposes, that have been introduced in OCPP 2.1, that are supported by the Charging Station. |
| SupportedEnergyTransferModes | MemberList |  | Lists the energy transfer services that are supported by the Charging Station. |
| SupportedFormats | MemberList |  | For DisplayMessageCtrlr: List of message formats supported by this Charging Station. |
| SupportedIdTokenTypes | MemberList |  | The subset of the list of supported IdTokenTypes as defined in Appendix 7. |
| SupportedLimits | MemberList |  | This variable defines which transaction limits in TransactionLimitType are supported by the Charging Station. |
| SupportedOperationModes | MemberList |  | Lists the V2X operation modes that are supported by the Charging Station. |
| SupportedPriorities | MemberList |  | For DisplayMessageCtrlr: List of the priorities supported by this Charging Station. |
| SupportedProviders | string |  | A comma-separated list of all providers (eMSPs) that are supported on this Charging Station. The providers are listed using country and provider ID from the EMAID, as defined in ISO 15118-20. |
| SupportedStates | MemberList |  | For DisplayMessageCtrlr: List of the states during which to display a message supported by this Charging Station. |
| SupportsDynamicProfiles | boolean |  | When this variable has value True, then the Charging Station supports charging profiles of type `Dynamic`. |
| SupportsEvseSleep | boolean |  | When reported as true the Charging Station supports the _evseSleep_ flag in a ChargingSchedulePeriod, which requests the EVSE electronics to go to sleep during _operationMode_ = 'Idle'. |
| SupportsExpiryDateTime | boolean |  | For LocalAuthListCtrlr: When set to _true_ Charging Station will disregard idTokens for authorization as if not present in the Local Authorization List when current date/time is past the value of _cacheExpiryDateTime_. |
| SupportsLimitAtSoC | boolean |  | When this variable has value True, then the Charging Station supports the field _limitAtSoC_ in ChargingSchedul, which will cap the limit or setpoint in the ChargingSchedulePeriodType by the value of _limitAtSoC.limit._ |
| SupportsMaxOfflineDuration | boolean |  | When this variable has value True, then the Charging Station supports the fields _maxOfflineDuration_ and _invalidAfterOfflineDuration_ in ChargingProfile. |
| SupportsRandomizedDelay | boolean |  | When this variable has value True, then the Charging Station supports the field _randomizedDelay_ in ChargingSchedule, which will delay the start of each charging schedule period by a random number between 0 and _randomizedDelay_. |
| SupportsUseLocalTime | boolean |  | When this variable has value True, then the Charging Station supports the field _useLocalTime_ in ChargingSchedule. |
| Suspending | boolean |  | If Suspending is true, the Component can is currently suspending charging. |
| Suspension | boolean |  | Applies to 'sensor' type Components that have a charging suspension capability, typically for safety or equipment protection reasons. If Suspension is true, the component can suspend charging when the sensed quantity is outside preset/configured limits. |
| TargetSoc | integer | Percent | For BatterySwapCtrlr: The state of charge that a battery must have in order to be eligible for swapping. |
| TariffFallbackMessage | string |  | Message (and/or tariff information) to be shown to an EV Driver when there is no driver specific tariff information available. |
| Temperature | decimal | Celsius, Fahrenheit | Temperature(s) of component (in Celsius, by default). Components may have multiple indexed temperature sensors. |
| Time | dateTime |  | Point in time value, in ISO 8601 datetime format. Time zone optional. |
| TimeAdjustmentReportingThreshold | integer | s | When the clock time is adjusted forwards or backwards for more then TimeAdjustmentReportingThreshold number of seconds, a SecurityEventNotification( 'SettingSystemTime' ) is sent by the charging station. |
| TimeOffset | string |  | A Time Offset with respect to Coordinated Universal Time (aka UTC or Greenwich Mean Time) in the form of an [RFC3339] time (zone) offset suffix, including the mandatory “+” or “-“ prefix. |
| TimeSource | SequenceList |  | Via this variable, the Charging Station provides the CSMS with the option to configure a clock source. |
| TimeZone | string |  | Configured current local time zone in the format: 'Europe/Oslo', 'Asia/Singapore' etc. |
| Timeout | decimal | s | Generic timeout value for Component operation (in seconds). |
| Timeout | integer | s | For BatterySwapCtrlr: Timeout in seconds in which a set of batteries must be inserted or removed after successful authorization. |
| Token | string |  | String of bytes representing an ID token. |
| TokenType | OptionList |  | Type of Token. Value is one of IdTokenEnumStringType (See Appendix 7). |
| TotalCostFallbackMessage | string |  | Message to be shown to an EV Driver when the Charging Station cannot retrieve the cost for a transaction at the end of the transaction. |
| Tries | integer |  | Number of attempts done by a Component. |
| Tripped | boolean |  | Single-shot device requires explicit intervention to re-prime/activate to normal. |
| TxBeforeAcceptedEnabled | boolean |  | With this configuration variable the Charging Station can be configured to allow charging before having received a BootNotificationResponse with status: Accepted. |
| TxEndedInterval | integer | s | Interval between sampling of metering (or other) data, intended to be transmitted in the TransactionEventRequest(Ended) message. |
| TxEndedMeasurands | MemberList |  | Sampled measurands to be included in the _meterValues_ element of TransactionEventRequest(Ended). |
| TxStartPoint | MemberList |  | Start points for a transaction. |
| TxStartedMeasurands | MemberList |  | Sampled measurands to be included in the _meterValues_ element of TransactionEventRequest(Started). |
| TxStopPoint | MemberList |  | Stop points of a transaction. |
| TxUpdatedInterval | integer | s | Interval between sampling of metering (or other) data, intended to be transmitted in the TransactionEventRequest(Updated) message. |
| TxUpdatedMeasurands | MemberList |  | Sampled measurands to be included in the _meterValues_ element of TransactionEventRequest(Updated). |
| UnlockOnEVSideDisconnect | boolean |  | When set to true, the Charging Station SHALL unlock the cable on the Charging Station side when the cable is unplugged at the EV. |
| UpstreamInterval | integer | s | Interval between sampling of metering (or other) data, intended to be transmitted via TransactionEventRequest(Updated) messages for location = `Upstream` only. |
| UpstreamMeasurands | MemberList |  | Sampled measurands to be included in the _meterValues_ element of every TransactionEventRequest(Updated) for location = `Upstream` only. |
| V2GCertificateInstallationEnabled | boolean |  | If this variable is _true_, then ISO 15118 V2G Charging Station certificate installation as described by use case A02 - Update Charging Station Certificate by request of CSMS |
| VehicleCertificate | string |  | For ConnectedEV: The PEM encoded X.509 leaf/intermediate/root certificate when present in the vehicle certificate chain. |
| VehicleId | string |  | ID that EV provides to charging station. Encoded as a hexbinary string. In ISO 15118 the EVCCID is 6 bytes (MAC address), in CHAdeMO the vehicle id can be 24 bytes. |
| VersionDate | dateTime |  | [RFC3339] |
| VersionNumber | string |  | Version number of hardware |
| VoltageImbalance | decimal | Percent | Percentage voltage imbalance in three phase supply. |
| WorkingMode | OptionList |  | This variable represents the current working mode of the battery in BatteryCartridge component. |
