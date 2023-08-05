import rev._sparkmaxdriver._rev_spark_driver
import typing

__all__ = [
    "frc_deviceType_t",
    "frc_manufacturer_t",
    "getFRCDeviceTypeText",
    "getFRCManufacturerText",
    "getTelemetryDataLowerBound",
    "getTelemetryDataName",
    "getTelemetryDataUnits",
    "getTelemetryDataUpperBound"
]


class frc_deviceType_t():
    """
    Members:

      deviceBroadcast

      robotController

      motorController

      relayController

      gyroSensor

      accelerometerSensor

      ultrasonicSensor

      gearToothSensor

      powerDistribution

      pneumaticsController

      miscCANDevice

      IOBreakout

      dev_rsvd12

      dev_rsvd13

      dev_rsvd14

      dev_rsvd15

      dev_rsvd16

      dev_rsvd17

      dev_rsvd18

      dev_rsvd19

      dev_rsvd20

      dev_rsvd21

      dev_rsvd22

      dev_rsvd23

      dev_rsvd24

      dev_rsvd25

      dev_rsvd26

      dev_rsvd27

      dev_rsvd28

      dev_rsvd29

      dev_rsvd30

      firmwareUpdate
    """
    def __eq__(self, arg0: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, arg0: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: int) -> None: ...
    @property
    def name(self) -> None:
        """
        :type: None
        """
    IOBreakout: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.IOBreakout
    __members__: dict # value = {'deviceBroadcast': frc_deviceType_t.deviceBroadcast, 'robotController': frc_deviceType_t.robotController, 'motorController': frc_deviceType_t.motorController, 'relayController': frc_deviceType_t.relayController, 'gyroSensor': frc_deviceType_t.gyroSensor, 'accelerometerSensor': frc_deviceType_t.accelerometerSensor, 'ultrasonicSensor': frc_deviceType_t.ultrasonicSensor, 'gearToothSensor': frc_deviceType_t.gearToothSensor, 'powerDistribution': frc_deviceType_t.powerDistribution, 'pneumaticsController': frc_deviceType_t.pneumaticsController, 'miscCANDevice': frc_deviceType_t.miscCANDevice, 'IOBreakout': frc_deviceType_t.IOBreakout, 'dev_rsvd12': frc_deviceType_t.dev_rsvd12, 'dev_rsvd13': frc_deviceType_t.dev_rsvd13, 'dev_rsvd14': frc_deviceType_t.dev_rsvd14, 'dev_rsvd15': frc_deviceType_t.dev_rsvd15, 'dev_rsvd16': frc_deviceType_t.dev_rsvd16, 'dev_rsvd17': frc_deviceType_t.dev_rsvd17, 'dev_rsvd18': frc_deviceType_t.dev_rsvd18, 'dev_rsvd19': frc_deviceType_t.dev_rsvd19, 'dev_rsvd20': frc_deviceType_t.dev_rsvd20, 'dev_rsvd21': frc_deviceType_t.dev_rsvd21, 'dev_rsvd22': frc_deviceType_t.dev_rsvd22, 'dev_rsvd23': frc_deviceType_t.dev_rsvd23, 'dev_rsvd24': frc_deviceType_t.dev_rsvd24, 'dev_rsvd25': frc_deviceType_t.dev_rsvd25, 'dev_rsvd26': frc_deviceType_t.dev_rsvd26, 'dev_rsvd27': frc_deviceType_t.dev_rsvd27, 'dev_rsvd28': frc_deviceType_t.dev_rsvd28, 'dev_rsvd29': frc_deviceType_t.dev_rsvd29, 'dev_rsvd30': frc_deviceType_t.dev_rsvd30, 'firmwareUpdate': frc_deviceType_t.firmwareUpdate}
    accelerometerSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.accelerometerSensor
    dev_rsvd12: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd12
    dev_rsvd13: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd13
    dev_rsvd14: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd14
    dev_rsvd15: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd15
    dev_rsvd16: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd16
    dev_rsvd17: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd17
    dev_rsvd18: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd18
    dev_rsvd19: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd19
    dev_rsvd20: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd20
    dev_rsvd21: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd21
    dev_rsvd22: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd22
    dev_rsvd23: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd23
    dev_rsvd24: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd24
    dev_rsvd25: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd25
    dev_rsvd26: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd26
    dev_rsvd27: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd27
    dev_rsvd28: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd28
    dev_rsvd29: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd29
    dev_rsvd30: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.dev_rsvd30
    deviceBroadcast: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.deviceBroadcast
    firmwareUpdate: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.firmwareUpdate
    gearToothSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.gearToothSensor
    gyroSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.gyroSensor
    miscCANDevice: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.miscCANDevice
    motorController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.motorController
    pneumaticsController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.pneumaticsController
    powerDistribution: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.powerDistribution
    relayController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.relayController
    robotController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.robotController
    ultrasonicSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = frc_deviceType_t.ultrasonicSensor
    pass
class frc_manufacturer_t():
    """
    Members:

      manufacturerBroadcast

      NI

      LM

      DEKA

      CTRE

      REV

      Grapple

      MindSensors

      TeamUse
    """
    def __eq__(self, arg0: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, arg0: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: int) -> None: ...
    @property
    def name(self) -> None:
        """
        :type: None
        """
    CTRE: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.CTRE
    DEKA: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.DEKA
    Grapple: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.Grapple
    LM: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.LM
    MindSensors: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.MindSensors
    NI: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.NI
    REV: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.REV
    TeamUse: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.TeamUse
    __members__: dict # value = {'manufacturerBroadcast': frc_manufacturer_t.manufacturerBroadcast, 'NI': frc_manufacturer_t.NI, 'LM': frc_manufacturer_t.LM, 'DEKA': frc_manufacturer_t.DEKA, 'CTRE': frc_manufacturer_t.CTRE, 'REV': frc_manufacturer_t.REV, 'Grapple': frc_manufacturer_t.Grapple, 'MindSensors': frc_manufacturer_t.MindSensors, 'TeamUse': frc_manufacturer_t.TeamUse}
    manufacturerBroadcast: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = frc_manufacturer_t.manufacturerBroadcast
    pass
def getFRCDeviceTypeText(index: int) -> str:
    pass
def getFRCManufacturerText(index: int) -> str:
    pass
def getTelemetryDataLowerBound(index: int) -> float:
    pass
def getTelemetryDataName(index: int) -> str:
    pass
def getTelemetryDataUnits(index: int) -> str:
    pass
def getTelemetryDataUpperBound(index: int) -> float:
    pass
