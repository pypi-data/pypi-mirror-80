import rev._rev
import typing
import AnalogMode
import ArbFFUnits
import CANAnalog
import CANDigitalInput
import CANEncoder
import CANPIDController
import CANSparkMax
import CANSparkMaxLowLevel
import ControlType
import EncoderType
import wpilib._wpilib
import wpilib.interfaces._interfaces

__all__ = [
    "CANAnalog",
    "CANDigitalInput",
    "CANEncoder",
    "CANError",
    "CANPIDController",
    "CANSensor",
    "CANSparkMax",
    "CANSparkMaxLowLevel",
    "ControlType",
    "SparkMax"
]


class CANSensor():
    def _getID(self) -> int: 
        """
        Get the ID of the sensor that is connected to the SparkMax through
        the encoder port on the front of the controller (not the top port).

        :returns: The ID of the sensor
        """
    def getInverted(self) -> bool: 
        """
        Get the phase of the CANSensor. This will just return false
        if the user tries to get the inversion of the hall effect.
        """
    def setInverted(self, inverted: bool) -> CANError: 
        """
        Set the phase of the CANSensor so that it is set to be in
        phase with the motor itself. This only works for quadrature
        encoders and analog sensors. This will throw an error
        if the user tries to set the inversion of the hall effect.
        """
    pass
class CANDigitalInput():
    class LimitSwitch():
        """
        Members:

          kForward

          kReverse
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
        __members__: dict # value = {'kForward': LimitSwitch.kForward, 'kReverse': LimitSwitch.kReverse}
        kForward: rev._rev.CANDigitalInput.LimitSwitch # value = LimitSwitch.kForward
        kReverse: rev._rev.CANDigitalInput.LimitSwitch # value = LimitSwitch.kReverse
        pass
    class LimitSwitchPolarity():
        """
        Members:

          kNormallyOpen

          kNormallyClosed
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
        __members__: dict # value = {'kNormallyOpen': LimitSwitchPolarity.kNormallyOpen, 'kNormallyClosed': LimitSwitchPolarity.kNormallyClosed}
        kNormallyClosed: rev._rev.CANDigitalInput.LimitSwitchPolarity # value = LimitSwitchPolarity.kNormallyClosed
        kNormallyOpen: rev._rev.CANDigitalInput.LimitSwitchPolarity # value = LimitSwitchPolarity.kNormallyOpen
        pass
    def __init__(self, device: CANSparkMax, limitSwitch: CANDigitalInput.LimitSwitch, polarity: CANDigitalInput.LimitSwitchPolarity) -> None: 
        """
        Constructs a CANDigitalInput.

        :param device: The Spark Max to which the limit switch is attached.

        :param limitSwitch: Whether this is forward or reverse limit switch.

        :param polarity: Whether the limit switch is normally open or normally
                   closed.
        """
    def enableLimitSwitch(self, enable: bool) -> CANError: 
        """
        Enables or disables controller shutdown based on limit switch.
        """
    def get(self) -> bool: 
        """
        Get the value from a digital input channel.

        Retrieve the value of a single digital input channel from a motor
        controller. This method will return the state of the limit input
        based on the selected polarity, whether or not it is enabled.
        """
    def isLimitSwitchEnabled(self) -> bool: 
        """
        Returns true if limit switch is enabled.
        """
    pass
class CANEncoder(CANSensor):
    class AlternateEncoderType():
        """
        Members:

          kQuadrature
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
        __members__: dict # value = {'kQuadrature': AlternateEncoderType.kQuadrature}
        kQuadrature: rev._rev.CANEncoder.AlternateEncoderType # value = AlternateEncoderType.kQuadrature
        pass
    class EncoderType():
        """
        Members:

          kNoSensor

          kHallSensor

          kQuadrature

          kSensorless
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
        __members__: dict # value = {'kNoSensor': EncoderType.kNoSensor, 'kHallSensor': EncoderType.kHallSensor, 'kQuadrature': EncoderType.kQuadrature, 'kSensorless': EncoderType.kSensorless}
        kHallSensor: rev._rev.CANEncoder.EncoderType # value = EncoderType.kHallSensor
        kNoSensor: rev._rev.CANEncoder.EncoderType # value = EncoderType.kNoSensor
        kQuadrature: rev._rev.CANEncoder.EncoderType # value = EncoderType.kQuadrature
        kSensorless: rev._rev.CANEncoder.EncoderType # value = EncoderType.kSensorless
        pass
    @typing.overload
    def __init__(self, device: CANSparkMax, sensorType: CANEncoder.AlternateEncoderType, counts_per_rev: int) -> None: 
        """
        Constructs a CANEncoder.

        :param device: The Spark Max to which the encoder is attached.

        :param sensorType: The encoder type for the motor: kHallEffect or kQuadrature

        :param counts_per_rev: The counts per revolution of the encoder

        Constructs a CANEncoder from the alternate encoder port

        :param device: The Spark Max to which the encoder is attached.

        :param sensorType: The alternate encoder type for the motor: kQuadrature

        :param counts_per_rev: The counts per revolution of the encoder
        """
    @typing.overload
    def __init__(self, device: CANSparkMax, sensorType: CANEncoder.EncoderType = EncoderType.kHallSensor, counts_per_rev: int = 42) -> None: ...
    def _getID(self) -> int: ...
    def getAverageDepth(self) -> int: 
        """
        Get the averafe sampling depth for a quadrature encoder.

        :returns: The average sampling depth
        """
    def getCPR(self) -> int: ...
    def getCountsPerRevolution(self) -> int: 
        """
        Get the counts per revolution of the quadrature encoder.

        For a description on the difference between CPR, PPR, etc. go to
        https://www.cuidevices.com/blog/what-is-encoder-ppr-cpr-and-lpr

        :returns: Counts per revolution
        """
    def getInverted(self) -> bool: 
        """
        Get the phase of the CANSensor. This will just return false
        if the user tries to get inverted while the SparkMax is
        Brushless and using the hall effect sensor.

        :returns: The phase of the encoder
        """
    def getMeasurementPeriod(self) -> int: 
        """
        Get the number of samples for reading from a quadrature encoder. This value
        sets the number of samples in the average for velocity readings.

        :returns: Measurement period in microseconds
        """
    def getPosition(self) -> float: 
        """
        Get the position of the motor. This returns the native units
        of 'rotations' by default, and can be changed by a scale factor
        using setPositionConversionFactor().

        :returns: Number of rotations of the motor
        """
    def getPositionConversionFactor(self) -> float: 
        """
        Get the conversion factor for position of the encoder. Multiplied by the
        native output units to give you position

        :returns: The conversion factor for position
        """
    def getVelocity(self) -> float: 
        """
        Get the velocity of the motor. This returns the native units
        of 'RPM' by default, and can be changed by a scale factor
        using setVelocityConversionFactor().

        :returns: Number the RPM of the motor
        """
    def getVelocityConversionFactor(self) -> float: 
        """
        Get the conversion factor for velocity of the encoder. Multiplied by the
        native output units to give you velocity

        :returns: The conversion factor for velocity
        """
    def setAverageDepth(self, depth: int) -> CANError: 
        """
        Set the average sampling depth for a quadrature encoder. This value
        sets the number of samples in the average for velocity readings. This
        can be any value from 1 to 64.

        When the SparkMax controller is in Brushless mode, this
        will not change any behavior.

        :param depth: The average sampling depth between 1 and 64 (default)

        :returns: CANError.kOK if successful
        """
    def setInverted(self, inverted: bool) -> CANError: 
        """
        Set the phase of the CANSensor so that it is set to be in
        phase with the motor itself. This only works for quadrature
        encoders. This will throw an error if the user tries to set
        inverted while the SparkMax is Brushless and using the hall
        effect sensor.

        :param inverted: The phase of the encoder

        :returns: CANError.kOK if successful
        """
    def setMeasurementPeriod(self, period_ms: int) -> CANError: 
        """
        Set the measurement period for velocity measurements of a quadrature encoder.
        When the SparkMax controller is in Brushless mode, this will not
        change any behavior.

        The basic formula to calculate velocity is change in positon / change in time.
        This parameter sets the change in time for measurement.

        :param period_us: Measurement period in milliseconds. This number may be
                 between 1 and 100 (default).

        :returns: CANError.kOK if successful
        """
    def setPosition(self, position: float) -> CANError: 
        """
        Set the position of the encoder.

        :param position: Number of rotations of the motor

        :returns: CANError Set to CANError.kOK if successful
        """
    def setPositionConversionFactor(self, factor: float) -> CANError: 
        """
        Set the conversion factor for position of the encoder. Multiplied by the
        native output units to give you position

        :param factor: The conversion factor to multiply the native units by

        :returns: CANError Set to CANError.kOK if successful
        """
    def setVelocityConversionFactor(self, factor: float) -> CANError: 
        """
        Set the conversion factor for velocity of the encoder. Multiplied by the
        native output units to give you velocity

        :param factor: The conversion factor to multiply the native units by

        :returns: CANError Set to CANError.kOK if successful
        """
    pass
class CANError():
    """
    Members:

      kOk

      kError

      kTimeout

      kNotImplmented

      kHALError

      kCantFindFirmware

      kFirmwareTooOld

      kFirmwareTooNew

      kParamInvalidID

      kParamMismatchType

      kParamAccessMode

      kParamInvalid

      kParamNotImplementedDeprecated

      kFollowConfigMismatch

      kInvalid

      kSetpointOutOfRange
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
    __members__: dict # value = {'kOk': CANError.kOk, 'kError': CANError.kError, 'kTimeout': CANError.kTimeout, 'kNotImplmented': CANError.kNotImplmented, 'kHALError': CANError.kHALError, 'kCantFindFirmware': CANError.kCantFindFirmware, 'kFirmwareTooOld': CANError.kFirmwareTooOld, 'kFirmwareTooNew': CANError.kFirmwareTooNew, 'kParamInvalidID': CANError.kParamInvalidID, 'kParamMismatchType': CANError.kParamMismatchType, 'kParamAccessMode': CANError.kParamAccessMode, 'kParamInvalid': CANError.kParamInvalid, 'kParamNotImplementedDeprecated': CANError.kParamNotImplementedDeprecated, 'kFollowConfigMismatch': CANError.kFollowConfigMismatch, 'kInvalid': CANError.kInvalid, 'kSetpointOutOfRange': CANError.kSetpointOutOfRange}
    kCantFindFirmware: rev._rev.CANError # value = CANError.kCantFindFirmware
    kError: rev._rev.CANError # value = CANError.kError
    kFirmwareTooNew: rev._rev.CANError # value = CANError.kFirmwareTooNew
    kFirmwareTooOld: rev._rev.CANError # value = CANError.kFirmwareTooOld
    kFollowConfigMismatch: rev._rev.CANError # value = CANError.kFollowConfigMismatch
    kHALError: rev._rev.CANError # value = CANError.kHALError
    kInvalid: rev._rev.CANError # value = CANError.kInvalid
    kNotImplmented: rev._rev.CANError # value = CANError.kNotImplmented
    kOk: rev._rev.CANError # value = CANError.kOk
    kParamAccessMode: rev._rev.CANError # value = CANError.kParamAccessMode
    kParamInvalid: rev._rev.CANError # value = CANError.kParamInvalid
    kParamInvalidID: rev._rev.CANError # value = CANError.kParamInvalidID
    kParamMismatchType: rev._rev.CANError # value = CANError.kParamMismatchType
    kParamNotImplementedDeprecated: rev._rev.CANError # value = CANError.kParamNotImplementedDeprecated
    kSetpointOutOfRange: rev._rev.CANError # value = CANError.kSetpointOutOfRange
    kTimeout: rev._rev.CANError # value = CANError.kTimeout
    pass
class CANPIDController():
    class AccelStrategy():
        """
        Members:

          kTrapezoidal

          kSCurve
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
        __members__: dict # value = {'kTrapezoidal': AccelStrategy.kTrapezoidal, 'kSCurve': AccelStrategy.kSCurve}
        kSCurve: rev._rev.CANPIDController.AccelStrategy # value = AccelStrategy.kSCurve
        kTrapezoidal: rev._rev.CANPIDController.AccelStrategy # value = AccelStrategy.kTrapezoidal
        pass
    class ArbFFUnits():
        """
        Members:

          kVoltage

          kPercentOut
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
        __members__: dict # value = {'kVoltage': ArbFFUnits.kVoltage, 'kPercentOut': ArbFFUnits.kPercentOut}
        kPercentOut: rev._rev.CANPIDController.ArbFFUnits # value = ArbFFUnits.kPercentOut
        kVoltage: rev._rev.CANPIDController.ArbFFUnits # value = ArbFFUnits.kVoltage
        pass
    def getD(self, slotID: int = 0) -> float: 
        """
        Get the Derivative Gain constant of the PIDF controller on the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double D Gain value
        """
    def getDFilter(self, slotID: int = 0) -> float: 
        """
        Get the Derivative Filter constant of the PIDF controller on the SPARK
        MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double D Filter value
        """
    def getFF(self, slotID: int = 0) -> float: 
        """
        Get the Feed-forward Gain constant of the PIDF controller on the SPARK
        MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double F Gain value
        """
    def getI(self, slotID: int = 0) -> float: 
        """
        Get the Integral Gain constant of the PIDF controller on the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double I Gain value
        """
    def getIAccum(self) -> float: 
        """
        Get the I accumulator of the PID controller. This is useful when wishing
        to see what the I accumulator value is to help with PID tuning

        :returns: The value of the I accumulator
        """
    def getIMaxAccum(self, slotID: int = 0) -> float: 
        """
        Get the maximum I accumulator of the PID controller. This value is used
        to constrain the I accumulator to help manage integral wind-up

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: The max value to contrain the I accumulator to
        """
    def getIZone(self, slotID: int = 0) -> float: 
        """
        Get the IZone constant of the PIDF controller on the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double IZone value
        """
    def getOutputMax(self, slotID: int = 0) -> float: 
        """
        Get the max output of the PIDF controller on the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double max value
        """
    def getOutputMin(self, slotID: int = 0) -> float: 
        """
        Get the min output of the PIDF controller on the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double min value
        """
    def getP(self, slotID: int = 0) -> float: 
        """
        Get the Proportional Gain constant of the PIDF controller on the SPARK
        MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: double P Gain value
        """
    def getSmartMotionAccelStrategy(self, slotID: int = 0) -> CANPIDController.AccelStrategy: 
        """
        Get the acceleration strategy used to control acceleration on the motor.
        The current strategy is trapezoidal motion profiling.

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: The acceleration strategy to use for the automatically generated
                  motion profile
        """
    def getSmartMotionAllowedClosedLoopError(self, slotID: int = 0) -> float: 
        """
        Get the allowed closed loop error of SmartMotion mode. This value is how
        much deviation from your setpoint is tolerated and is useful in
        preventing oscillation around your setpoint.

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: The allowed deviation for your setpoint vs actual position in
                  rotations
        """
    def getSmartMotionMaxAccel(self, slotID: int = 0) -> float: 
        """
        Get the maximum acceleration of the SmartMotion mode. This is the
        accleration that the motor velocity will increase at until the max
        velocity is reached

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: The maxmimum acceleration for the motion profile in RPM per
                  second
        """
    def getSmartMotionMaxVelocity(self, slotID: int = 0) -> float: 
        """
        Get the maximum velocity of the SmartMotion mode. This is the velocity
        that is reached in the middle of the profile and is what the motor should
        spend most of its time at

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: The maxmimum cruise velocity for the motion profile in RPM
        """
    def getSmartMotionMinOutputVelocity(self, slotID: int = 0) -> float: 
        """
        Get the mimimum velocity of the SmartMotion mode. Any requested
        velocities below this value will be set to 0.

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: The minimum velocity for the motion profile in RPM
        """
    def setD(self, gain: float, slotID: int = 0) -> CANError: 
        """
        Set the Derivative Gain constant of the PIDF controller on the SPARK MAX.
        This uses the Set Parameter API and should be used infrequently. The
        parameter does not presist unless burnFlash() is called.  The recommended
        method to configure this parameter is use to SPARK MAX GUI to tune and
        save parameters.

        :param gain: The derivative gain value, must be positive

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setDFilter(self, gain: float, slotID: int = 0) -> CANError: 
        """
        Set the Derivative Filter constant of the PIDF controller on the SPARK
        MAX. This uses the Set Parameter API and should be used infrequently. The
        parameter does not presist unless burnFlash() is called.

        :param gain: The derivative filter value, must be a positive number
              between 0 and 1

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setFF(self, gain: float, slotID: int = 0) -> CANError: 
        """
        Set the Feed-froward Gain constant of the PIDF controller on the SPARK
        MAX. This uses the Set Parameter API and should be used infrequently. The
        parameter does not presist unless burnFlash() is called.  The recommended
        method to configure this parameter is use to SPARK MAX GUI to tune and
        save parameters.

        :param gain: The feed-forward gain value

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setFeedbackDevice(self, sensor: CANSensor) -> CANError: 
        """
        Set the controller's feedback device.

        The default feedback device is assumed to be the integrated encoder.
        This is used to changed to another feedback device for the controller,
        such as an analog sensor.

        If there is a limited range on the feedback sensor that should be
        observed by the PIDController, it can be set by calling
        SetFeedbackSensorRange() on the sensor object.

        :param sensor: The sensor to be used as a feedback device

        :returns: CANError set to kOK if successful
        """
    def setI(self, gain: float, slotID: int = 0) -> CANError: 
        """
        Set the Integral Gain constant of the PIDF controller on the SPARK MAX.
        This uses the Set Parameter API and should be used infrequently. The
        parameter does not presist unless burnFlash() is called.  The recommended
        method to configure this parameter is use to SPARK MAX GUI to tune and
        save parameters.

        :param gain: The integral gain value, must be positive

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setIAccum(self, iAccum: float) -> CANError: 
        """
        Set the I accumulator of the PID controller. This is useful when wishing
        to force a reset on the I accumulator of the PID controller. You can also
        preset values to see how it will respond to certain I characteristics

        To use this function, the controller must be in a closed loop control
        mode by calling setReference()

        :param iAccum: The value to set the I accumulator to

        :returns: CANError Set to kOK if successful
        """
    def setIMaxAccum(self, iMaxAccum: float, slotID: int = 0) -> CANError: 
        """
        Configure the maximum I accumulator of the PID controller. This value is
        used to constrain the I accumulator to help manage integral wind-up

        :param iMaxAccum: The max value to contrain the I accumulator to

        :param slotID: Is the gain schedule slot, the value is a number
                 between 0 and 3. Each slot has its own set of gain values and
                 can be changed in each control frame using SetReference().

        :returns: CANError Set to kOK if successful
        """
    def setIZone(self, IZone: float, slotID: int = 0) -> CANError: 
        """
        Set the IZone range of the PIDF controller on the SPARK MAX. This value
        specifies the range the |error| must be within for the integral constant
        to take effect.

        This uses the Set Parameter API and should be used infrequently.
        The parameter does not presist unless burnFlash() is called.
        The recommended method to configure this parameter is to use the
        SPARK MAX GUI to tune and save parameters.

        :param gain: The IZone value, must be positive. Set to 0 to disable

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setOutputRange(self, min: float, max: float, slotID: int = 0) -> CANError: 
        """
        Set the min amd max output for the closed loop mode.

        This uses the Set Parameter API and should be used infrequently.
        The parameter does not presist unless burnFlash() is called.
        The recommended method to configure this parameter is to use the
        SPARK MAX GUI to tune and save parameters.

        :param min: Reverse power minimum to allow the controller to output

        :param max: Forward power maximum to allow the controller to output

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setP(self, gain: float, slotID: int = 0) -> CANError: 
        """
        Set the Proportional Gain constant of the PIDF controller on the SPARK
        MAX. This uses the Set Parameter API and should be used infrequently. The
        parameter does not presist unless burnFlash() is called.  The recommended
        method to configure this parameter is use to SPARK MAX GUI to tune and
        save parameters.

        :param gain: The proportional gain value, must be positive

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to REV_OK if successful
        """
    def setReference(self, value: float, ctrl: ControlType, pidSlot: int = 0, arbFeedforward: float = 0, arbFFUnits: CANPIDController.ArbFFUnits = ArbFFUnits.kVoltage) -> CANError: 
        """
        Set the controller reference value based on the selected control mode.

        :param value: The value to set depending on the control mode. For basic
                      duty cycle control this should be a value between -1 and 1
                      Otherwise: Voltage Control: Voltage (volts) Velocity Control: Velocity
                      (RPM) Position Control: Position (Rotations) Current Control: Current
                      (Amps). The units can be changed for position and velocity by a scale
                      factor using setPositionConversionFactor().

        :param ctrl:  Is the control type

        :param pidSlot: for this command

        :param arbFeedforward: A value from -32.0 to 32.0 which is a voltage
                      applied to the motor after the result of the specified control mode. The
                      units for the parameter is Volts. This value is set after the control
                      mode, but before any current limits or ramp rates.

        :returns: CANError Set to REV_OK if successful
        """
    def setSmartMotionAccelStrategy(self, accelStrategy: CANPIDController.AccelStrategy, slotID: int = 0) -> CANError: 
        """
        Coming soon. Configure the acceleration strategy used to control
        acceleration on the motor. The current strategy is trapezoidal motion
        profiling.

        :param accelStrategy: The acceleration strategy to use for the
                     automatically generated motion profile

        :param slotID: Is the gain schedule slot, the value is a number
                     between 0 and 3. Each slot has its own set of gain values and
                     can be changed in each control frame using SetReference().

        :returns: CANError Set to kOK if successful
        """
    def setSmartMotionAllowedClosedLoopError(self, allowedErr: float, slotID: int = 0) -> CANError: 
        """
        Configure the allowed closed loop error of SmartMotion mode. This value
        is how much deviation from your setpoint is tolerated and is useful in
        preventing oscillation around your setpoint.

        :param allowedErr: The allowed deviation for your setpoint vs actual
                  position in rotations

        :param slotID: Is the gain schedule slot, the value is a number
                  between 0 and 3. Each slot has its own set of gain values and
                  can be changed in each control frame using SetReference().

        :returns: CANError Set to kOK if successful
        """
    def setSmartMotionMaxAccel(self, maxAccel: float, slotID: int = 0) -> CANError: 
        """
        Configure the maximum acceleration of the SmartMotion mode. This is the
        accleration that the motor velocity will increase at until the max
        velocity is reached

        :param maxAccel: The maxmimum acceleration for the motion profile in RPM
                per second

        :param slotID: Is the gain schedule slot, the value is a number
                between 0 and 3. Each slot has its own set of gain values and
                can be changed in each control frame using SetReference().

        :returns: CANError Set to kOK if successful
        """
    def setSmartMotionMaxVelocity(self, maxVel: float, slotID: int = 0) -> CANError: 
        """
        Configure the maximum velocity of the SmartMotion mode. This is the
        velocity that is reached in the middle of the profile and is what the
        motor should spend most of its time at

        :param maxVel: The maxmimum cruise velocity for the motion profile in RPM

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to kOK if successful
        """
    def setSmartMotionMinOutputVelocity(self, minVel: float, slotID: int = 0) -> CANError: 
        """
        Configure the mimimum velocity of the SmartMotion mode. Any requested
        velocities below this value will be set to 0.

        :param minVel: The minimum velocity for the motion profile in RPM

        :param slotID: Is the gain schedule slot, the value is a number
              between 0 and 3. Each slot has its own set of gain values and
              can be changed in each control frame using SetReference().

        :returns: CANError Set to kOK if successful
        """
    pass
class CANAnalog(CANSensor):
    class AnalogMode():
        """
        Analog sensors have the ability to either be absolute or relative.
        By default, GetAnalog() will return an absolute analog sensor, but
        it can also be configured to be a relative sensor instead.

        Members:

          kAbsolute

          kRelative
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
        __members__: dict # value = {'kAbsolute': AnalogMode.kAbsolute, 'kRelative': AnalogMode.kRelative}
        kAbsolute: rev._rev.CANAnalog.AnalogMode # value = AnalogMode.kAbsolute
        kRelative: rev._rev.CANAnalog.AnalogMode # value = AnalogMode.kRelative
        pass
    def __init__(self, device: CANSparkMax, mode: CANAnalog.AnalogMode) -> None: 
        """
        Constucts a CANAnalog.

        :param device: The Spark Max to which the analog sensor is attached.
        """
    def _getID(self) -> int: ...
    def getAverageDepth(self) -> int: 
        """
        Get the averafe sampling depth for a quadrature encoder.

        :returns: The average sampling depth
        """
    def getInverted(self) -> bool: 
        """
        Get the phase of the CANSensor. This will just return false
        if the user tries to get inverted while the SparkMax is
        Brushless and using the hall effect sensor.

        :returns: The phase of the encoder
        """
    def getMeasurementPeriod(self) -> int: 
        """
        Get the number of samples for reading from a quadrature encoder. This value
        sets the number of samples in the average for velocity readings.

        :returns: Measurement period in microseconds
        """
    def getPosition(self) -> float: 
        """
        Get the position of the motor. Returns value in the native unit
        of 'volt' by default, and can be changed by a scale factor
        using setPositionConversionFactor().

        :returns: Position of the sensor in volts
        """
    def getPositionConversionFactor(self) -> float: 
        """
        Get the current conversion factor for the position of the analog
        sensor.

        :returns: Analog position conversion factor
        """
    def getVelocity(self) -> float: 
        """
        Get the velocity of the motor. Returns value in the native units of
        'volts per second' by default, and can be changed by a
        scale factor using setVelocityConversionFactor().

        :returns: Velocity of the sensor in volts per second
        """
    def getVelocityConversionFactor(self) -> float: 
        """
        Get the current conversion factor for the velocity of the analog
        sensor.

        :returns: Analog velocity conversion factor
        """
    def getVoltage(self) -> float: 
        """
        Get the voltage of the analog sensor.

        :returns: Voltage of the sensor
        """
    def setAverageDepth(self, depth: int) -> CANError: 
        """
        Set the average sampling depth for a quadrature encoder. This value
        sets the number of samples in the average for velocity readings. This
        can be any value from 1 to 64.

        When the SparkMax controller is in Brushless mode, this
        will not change any behavior.

        :param depth: The average sampling depth between 1 and 64 (default)

        :returns: CANError.kOK if successful
        """
    def setInverted(self, inverted: bool) -> CANError: 
        """
        Set the phase of the CANSensor so that it is set to be in
        phase with the motor itself. This only works for quadrature
        encoders. This will throw an error if the user tries to set
        inverted while the SparkMax is Brushless and using the hall
        effect sensor.

        :param inverted: The phase of the encoder

        :returns: CANError.kOK if successful
        """
    def setMeasurementPeriod(self, period_ms: int) -> CANError: 
        """
        Set the measurement period for velocity measurements of a quadrature encoder.
        When the SparkMax controller is in Brushless mode, this will not
        change any behavior.

        The basic formula to calculate velocity is change in positon / change in time.
        This parameter sets the change in time for measurement.

        :param period_us: Measurement period in milliseconds. This number may be
                 between 1 and 100 (default).

        :returns: CANError.kOK if successful
        """
    def setPositionConversionFactor(self, factor: float) -> CANError: 
        """
        Set the conversion factor for the position of the analog sensor.
        By default, revolutions per volt is 1. Changing the position conversion
        factor will also change the position units.

        :param factor: The conversion factor which will be multiplied by volts

        :returns: CANError Set to CANError.kOK if successful
        """
    def setVelocityConversionFactor(self, factor: float) -> CANError: 
        """
        Set the conversion factor for the veolocity of the analog sensor.
        By default, revolutions per volt second is 1. Changing the velocity
        conversion factor will also change the velocity units.

        :param factor: The conversion factor which will be multipled by volts per second

        :returns: CANError Set to CANError.kOK is successful
        """
    pass
class CANSparkMaxLowLevel(wpilib._wpilib.ErrorBase, wpilib.interfaces._interfaces.SpeedController, wpilib.interfaces._interfaces.PIDOutput):
    class MotorType():
        """
        Members:

          kBrushed

          kBrushless
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
        __members__: dict # value = {'kBrushed': MotorType.kBrushed, 'kBrushless': MotorType.kBrushless}
        kBrushed: rev._rev.CANSparkMaxLowLevel.MotorType # value = MotorType.kBrushed
        kBrushless: rev._rev.CANSparkMaxLowLevel.MotorType # value = MotorType.kBrushless
        pass
    class ParameterStatus():
        """
        Members:

          kOK

          kInvalidID

          kMismatchType

          kAccessMode

          kInvalid

          kNotImplementedDeprecated
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
        __members__: dict # value = {'kOK': ParameterStatus.kOK, 'kInvalidID': ParameterStatus.kInvalidID, 'kMismatchType': ParameterStatus.kMismatchType, 'kAccessMode': ParameterStatus.kAccessMode, 'kInvalid': ParameterStatus.kInvalid, 'kNotImplementedDeprecated': ParameterStatus.kNotImplementedDeprecated}
        kAccessMode: rev._rev.CANSparkMaxLowLevel.ParameterStatus # value = ParameterStatus.kAccessMode
        kInvalid: rev._rev.CANSparkMaxLowLevel.ParameterStatus # value = ParameterStatus.kInvalid
        kInvalidID: rev._rev.CANSparkMaxLowLevel.ParameterStatus # value = ParameterStatus.kInvalidID
        kMismatchType: rev._rev.CANSparkMaxLowLevel.ParameterStatus # value = ParameterStatus.kMismatchType
        kNotImplementedDeprecated: rev._rev.CANSparkMaxLowLevel.ParameterStatus # value = ParameterStatus.kNotImplementedDeprecated
        kOK: rev._rev.CANSparkMaxLowLevel.ParameterStatus # value = ParameterStatus.kOK
        pass
    class PeriodicFrame():
        """
        Members:

          kStatus0

          kStatus1

          kStatus2
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
        __members__: dict # value = {'kStatus0': PeriodicFrame.kStatus0, 'kStatus1': PeriodicFrame.kStatus1, 'kStatus2': PeriodicFrame.kStatus2}
        kStatus0: rev._rev.CANSparkMaxLowLevel.PeriodicFrame # value = PeriodicFrame.kStatus0
        kStatus1: rev._rev.CANSparkMaxLowLevel.PeriodicFrame # value = PeriodicFrame.kStatus1
        kStatus2: rev._rev.CANSparkMaxLowLevel.PeriodicFrame # value = PeriodicFrame.kStatus2
        pass
    class PeriodicStatus0():
        def __init__(self) -> None: ...
        @property
        def appliedOutput(self) -> float:
            """
            :type: float
            """
        @appliedOutput.setter
        def appliedOutput(self, arg0: float) -> None:
            pass
        @property
        def faults(self) -> int:
            """
            :type: int
            """
        @faults.setter
        def faults(self, arg0: int) -> None:
            pass
        @property
        def isFollower(self) -> bool:
            """
            :type: bool
            """
        @isFollower.setter
        def isFollower(self, arg0: bool) -> None:
            pass
        @property
        def isInverted(self) -> int:
            """
            :type: int
            """
        @isInverted.setter
        def isInverted(self, arg0: int) -> None:
            pass
        @property
        def lock(self) -> int:
            """
            :type: int
            """
        @lock.setter
        def lock(self, arg0: int) -> None:
            pass
        @property
        def motorType(self) -> CANSparkMaxLowLevel.MotorType:
            """
            :type: CANSparkMaxLowLevel.MotorType
            """
        @motorType.setter
        def motorType(self, arg0: CANSparkMaxLowLevel.MotorType) -> None:
            pass
        @property
        def roboRIO(self) -> int:
            """
            :type: int
            """
        @roboRIO.setter
        def roboRIO(self, arg0: int) -> None:
            pass
        @property
        def stickyFaults(self) -> int:
            """
            :type: int
            """
        @stickyFaults.setter
        def stickyFaults(self, arg0: int) -> None:
            pass
        @property
        def timestamp(self) -> int:
            """
            :type: int
            """
        @timestamp.setter
        def timestamp(self, arg0: int) -> None:
            pass
        pass
    class PeriodicStatus1():
        def __init__(self) -> None: ...
        @property
        def busVoltage(self) -> float:
            """
            :type: float
            """
        @busVoltage.setter
        def busVoltage(self, arg0: float) -> None:
            pass
        @property
        def motorTemperature(self) -> int:
            """
            :type: int
            """
        @motorTemperature.setter
        def motorTemperature(self, arg0: int) -> None:
            pass
        @property
        def outputCurrent(self) -> float:
            """
            :type: float
            """
        @outputCurrent.setter
        def outputCurrent(self, arg0: float) -> None:
            pass
        @property
        def sensorVelocity(self) -> float:
            """
            :type: float
            """
        @sensorVelocity.setter
        def sensorVelocity(self, arg0: float) -> None:
            pass
        @property
        def timestamp(self) -> int:
            """
            :type: int
            """
        @timestamp.setter
        def timestamp(self, arg0: int) -> None:
            pass
        pass
    class PeriodicStatus2():
        def __init__(self) -> None: ...
        @property
        def iAccum(self) -> float:
            """
            :type: float
            """
        @iAccum.setter
        def iAccum(self, arg0: float) -> None:
            pass
        @property
        def sensorPosition(self) -> float:
            """
            :type: float
            """
        @sensorPosition.setter
        def sensorPosition(self, arg0: float) -> None:
            pass
        @property
        def timestamp(self) -> int:
            """
            :type: int
            """
        @timestamp.setter
        def timestamp(self, arg0: int) -> None:
            pass
        pass
    class TelemetryID():
        """
        Members:

          kBusVoltage

          kOutputCurrent

          kVelocity

          kPosition

          kIAccum

          kAppliedOutput

          kMotorTemp

          kFaults

          kStickyFaults

          kAnalogVoltage

          kAnalogPosition

          kAnalogVelocity

          kAltEncPosition

          kAltEncVelocity

          kTotalStreams
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
        __members__: dict # value = {'kBusVoltage': TelemetryID.kBusVoltage, 'kOutputCurrent': TelemetryID.kOutputCurrent, 'kVelocity': TelemetryID.kVelocity, 'kPosition': TelemetryID.kPosition, 'kIAccum': TelemetryID.kIAccum, 'kAppliedOutput': TelemetryID.kAppliedOutput, 'kMotorTemp': TelemetryID.kMotorTemp, 'kFaults': TelemetryID.kFaults, 'kStickyFaults': TelemetryID.kStickyFaults, 'kAnalogVoltage': TelemetryID.kAnalogVoltage, 'kAnalogPosition': TelemetryID.kAnalogPosition, 'kAnalogVelocity': TelemetryID.kAnalogVelocity, 'kAltEncPosition': TelemetryID.kAltEncPosition, 'kAltEncVelocity': TelemetryID.kAltEncVelocity, 'kTotalStreams': TelemetryID.kTotalStreams}
        kAltEncPosition: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kAltEncPosition
        kAltEncVelocity: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kAltEncVelocity
        kAnalogPosition: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kAnalogPosition
        kAnalogVelocity: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kAnalogVelocity
        kAnalogVoltage: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kAnalogVoltage
        kAppliedOutput: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kAppliedOutput
        kBusVoltage: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kBusVoltage
        kFaults: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kFaults
        kIAccum: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kIAccum
        kMotorTemp: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kMotorTemp
        kOutputCurrent: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kOutputCurrent
        kPosition: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kPosition
        kStickyFaults: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kStickyFaults
        kTotalStreams: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kTotalStreams
        kVelocity: rev._rev.CANSparkMaxLowLevel.TelemetryID # value = TelemetryID.kVelocity
        pass
    class TelemetryMessage():
        def __init__(self) -> None: ...
        @property
        def id(self) -> CANSparkMaxLowLevel.TelemetryID:
            """
            :type: CANSparkMaxLowLevel.TelemetryID
            """
        @id.setter
        def id(self, arg0: CANSparkMaxLowLevel.TelemetryID) -> None:
            pass
        @property
        def lowerBnd(self) -> float:
            """
            :type: float
            """
        @lowerBnd.setter
        def lowerBnd(self, arg0: float) -> None:
            pass
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def timestamp(self) -> int:
            """
            :type: int
            """
        @timestamp.setter
        def timestamp(self, arg0: int) -> None:
            pass
        @property
        def units(self) -> str:
            """
            :type: str
            """
        @property
        def upperBnd(self) -> float:
            """
            :type: float
            """
        @upperBnd.setter
        def upperBnd(self, arg0: float) -> None:
            pass
        @property
        def value(self) -> float:
            """
            :type: float
            """
        @value.setter
        def value(self, arg0: float) -> None:
            pass
        pass
    def __init__(self, deviceID: int, type: CANSparkMaxLowLevel.MotorType) -> None: 
        """
        Create a new SPARK MAX Controller

        :param deviceID: The device ID.

        :param type: The motor type connected to the controller. Brushless
                motors must be connected to their matching color and the
                hall sensor plugged in. Brushed motors must be connected
                to the Red and Black terminals only.
        """
    def _getPeriodicStatus0(self) -> CANSparkMaxLowLevel.PeriodicStatus0: ...
    def _getPeriodicStatus1(self) -> CANSparkMaxLowLevel.PeriodicStatus1: ...
    def _getPeriodicStatus2(self) -> CANSparkMaxLowLevel.PeriodicStatus2: ...
    def _getSafeFloat(self, f: float) -> float: ...
    def _setEncPosition(self, value: float) -> CANError: ...
    def _setIAccum(self, value: float) -> CANError: ...
    def _setpointCommand(self, value: float, ctrl: ControlType = ControlType.kDutyCycle, pidSlot: int = 0, arbFeedforward: float = 0, arbFFUnits: int = 0) -> CANError: ...
    @staticmethod
    def enableExternalUSBControl(enable: bool) -> None: 
        """
        Allow external controllers to recieve control commands over USB.
        For example, a configuration where the heartbeat (and enable/disable)
        is sent by the main controller, but control frames are sent by
        other CAN devices over USB.

        This is global for all controllers on the same bus.

        This does not disable sending control frames from this device. To prevent
        conflicts, do not enable this feature and also send Set() for SetReference()
        from the controllers you wish to control.

        :param enable: Enable or disable external control
        """
    def getDeviceId(self) -> int: 
        """
        Get the configured Device ID of the SPARK MAX.

        :returns: int device ID
        """
    def getFirmwareString(self) -> str: 
        """
        Get the firmware version of the SPARK MAX as a string.

        :returns: std::string Human readable firmware version string
        """
    def getFirmwareVersion(self) -> int: 
        """
        Get the firmware version of the SPARK MAX.

        :returns: uint32_t Firmware version integer. Value is represented as 4
                  bytes, Major.Minor.Build H.Build L
        """
    def getInitialMotorType(self) -> CANSparkMaxLowLevel.MotorType: 
        """
        Get the motor type setting from when the SparkMax was created.

        This does not use the Get Parameter API which means it does not read
        what motor type is stored on the SparkMax itself. Instead, it reads
        the stored motor type from when the SparkMax object was first created.

        :returns: MotorType Motor type setting
        """
    def getMotorType(self) -> CANSparkMaxLowLevel.MotorType: 
        """
        Get the motor type setting for the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :returns: MotorType Motor type setting
        """
    def getSerialNumber(self) -> typing.List[int]: 
        """
        Get the unique serial number of the SPARK MAX. Currently not implemented.

        :returns: std::vector<uint8_t> Vector of bytes representig the unique
                  serial number
        """
    def restoreFactoryDefaults(self, persist: bool = False) -> CANError: 
        """
        Restore motor controller parameters to factory default

        :param persist: If true, burn the flash with the factory default
               parameters

        :returns: CANError Set to CANError::kOk if successful
        """
    def setControlFramePeriodMs(self, periodMs: int) -> None: 
        """
        Set the control frame send period for the native CAN Send thread. To
        disable periodic sends, set periodMs to 0.

        :param periodMs: The send period in milliseconds between 1ms and 100ms
                or set to 0 to disable periodic sends. Note this is not updated until
                the next call to Set() or SetReference().
        """
    @staticmethod
    def setEnable(enable: bool) -> None: 
        """
        Send enabled or disabled command to controllers. This is global for all
        controllers on the same bus, and will only work for non-roboRIO targets
        in non-competiton use. This function will also not work if a roboRIO is
        present on the CAN bus.

        This does not disable sending control frames from this device. To prevent
        conflicts, do not enable this feature and also send Set() for SetReference()
        from the controllers you wish to control.

        :param enable: Enable or disable external control
        """
    def setMotorType(self, type: CANSparkMaxLowLevel.MotorType) -> CANError: 
        """
        Set the motor type connected to the SPARK MAX.

        This uses the Set Parameter API and should be used infrequently.
        The parameter does not presist unless burnFlash() is called.
        The recommended method to configure this parameter is to use the
        SPARK MAX GUI to tune and save parameters.

        :param type: The type of motor connected to the controller. Brushless
            motors must be connected to their matching color and the hall sensor
            plugged in. Brushed motors must be connected to the Red and Black
            terminals only.

        :returns: CANError Set to CANError::kOk if successful
        """
    def setPeriodicFramePeriod(self, frame: CANSparkMaxLowLevel.PeriodicFrame, periodMs: int) -> CANError: 
        """
        Set the rate of transmission for periodic frames from the SPARK MAX

        Each motor controller sends back three status frames with different
        data at set rates. Use this function to change the default rates.

        Defaults:
        Status0 - 10ms
        Status1 - 20ms
        Status2 - 50ms

        This value is not stored in the FLASH after calling burnFlash()
        and is reset on powerup.

        Refer to the SPARK MAX reference manual on details for how and when
        to configure this parameter.

        :param frameID: The frame ID can be one of PeriodicFrame type

        :param periodMs: The rate the controller sends the frame to the
                controller.

        :returns: CANError Set to CANError::kOk if successful
        """
    kAPIBuildVersion = 255
    kAPIMajorVersion = 255
    kAPIMinorVersion = 255
    kAPIVersion = 1573398015
    pass
class CANSparkMax(CANSparkMaxLowLevel, wpilib._wpilib.ErrorBase, wpilib.interfaces._interfaces.SpeedController, wpilib.interfaces._interfaces.PIDOutput):
    class ExternalFollower():
        def __init__(self) -> None: ...
        @property
        def arbId(self) -> int:
            """
            :type: int
            """
        @arbId.setter
        def arbId(self, arg0: int) -> None:
            pass
        @property
        def configId(self) -> int:
            """
            :type: int
            """
        @configId.setter
        def configId(self, arg0: int) -> None:
            pass
        pass
    class FaultID():
        """
        Members:

          kBrownout

          kOvercurrent

          kIWDTReset

          kMotorFault

          kSensorFault

          kStall

          kEEPROMCRC

          kCANTX

          kCANRX

          kHasReset

          kDRVFault

          kOtherFault

          kSoftLimitFwd

          kSoftLimitRev

          kHardLimitFwd

          kHardLimitRev
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
        __members__: dict # value = {'kBrownout': FaultID.kBrownout, 'kOvercurrent': FaultID.kOvercurrent, 'kIWDTReset': FaultID.kIWDTReset, 'kMotorFault': FaultID.kMotorFault, 'kSensorFault': FaultID.kSensorFault, 'kStall': FaultID.kStall, 'kEEPROMCRC': FaultID.kEEPROMCRC, 'kCANTX': FaultID.kCANTX, 'kCANRX': FaultID.kCANRX, 'kHasReset': FaultID.kHasReset, 'kDRVFault': FaultID.kDRVFault, 'kOtherFault': FaultID.kOtherFault, 'kSoftLimitFwd': FaultID.kSoftLimitFwd, 'kSoftLimitRev': FaultID.kSoftLimitRev, 'kHardLimitFwd': FaultID.kHardLimitFwd, 'kHardLimitRev': FaultID.kHardLimitRev}
        kBrownout: rev._rev.CANSparkMax.FaultID # value = FaultID.kBrownout
        kCANRX: rev._rev.CANSparkMax.FaultID # value = FaultID.kCANRX
        kCANTX: rev._rev.CANSparkMax.FaultID # value = FaultID.kCANTX
        kDRVFault: rev._rev.CANSparkMax.FaultID # value = FaultID.kDRVFault
        kEEPROMCRC: rev._rev.CANSparkMax.FaultID # value = FaultID.kEEPROMCRC
        kHardLimitFwd: rev._rev.CANSparkMax.FaultID # value = FaultID.kHardLimitFwd
        kHardLimitRev: rev._rev.CANSparkMax.FaultID # value = FaultID.kHardLimitRev
        kHasReset: rev._rev.CANSparkMax.FaultID # value = FaultID.kHasReset
        kIWDTReset: rev._rev.CANSparkMax.FaultID # value = FaultID.kIWDTReset
        kMotorFault: rev._rev.CANSparkMax.FaultID # value = FaultID.kMotorFault
        kOtherFault: rev._rev.CANSparkMax.FaultID # value = FaultID.kOtherFault
        kOvercurrent: rev._rev.CANSparkMax.FaultID # value = FaultID.kOvercurrent
        kSensorFault: rev._rev.CANSparkMax.FaultID # value = FaultID.kSensorFault
        kSoftLimitFwd: rev._rev.CANSparkMax.FaultID # value = FaultID.kSoftLimitFwd
        kSoftLimitRev: rev._rev.CANSparkMax.FaultID # value = FaultID.kSoftLimitRev
        kStall: rev._rev.CANSparkMax.FaultID # value = FaultID.kStall
        pass
    class IdleMode():
        """
        Members:

          kCoast

          kBrake
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
        __members__: dict # value = {'kCoast': IdleMode.kCoast, 'kBrake': IdleMode.kBrake}
        kBrake: rev._rev.CANSparkMax.IdleMode # value = IdleMode.kBrake
        kCoast: rev._rev.CANSparkMax.IdleMode # value = IdleMode.kCoast
        pass
    class InputMode():
        """
        Members:

          kPWM

          kCAN
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
        __members__: dict # value = {'kPWM': InputMode.kPWM, 'kCAN': InputMode.kCAN}
        kCAN: rev._rev.CANSparkMax.InputMode # value = InputMode.kCAN
        kPWM: rev._rev.CANSparkMax.InputMode # value = InputMode.kPWM
        pass
    class SoftLimitDirection():
        """
        Members:

          kForward

          kReverse
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
        __members__: dict # value = {'kForward': SoftLimitDirection.kForward, 'kReverse': SoftLimitDirection.kReverse}
        kForward: rev._rev.CANSparkMax.SoftLimitDirection # value = SoftLimitDirection.kForward
        kReverse: rev._rev.CANSparkMax.SoftLimitDirection # value = SoftLimitDirection.kReverse
        pass
    def PIDWrite(self, output: float) -> None: ...
    def __init__(self, deviceID: int, type: CANSparkMaxLowLevel.MotorType) -> None: 
        """
        Create a new SPARK MAX Controller

        :param deviceID: The device ID.

        :param type: The motor type connected to the controller. Brushless
                motors must be connected to their matching color and the
                hall sensor plugged in. Brushed motors must be connected
                to the Red and Black terminals only.
        """
    def burnFlash(self) -> CANError: 
        """
        Writes all settings to flash.
        """
    def clearFaults(self) -> CANError: 
        """
        Clears all non-sticky faults.

        Sticky faults must be cleared by resetting the motor controller.
        """
    def disable(self) -> None: 
        """
        Common interface for disabling a motor.
        """
    def disableVoltageCompensation(self) -> CANError: 
        """
        Disables the voltage compensation setting for all modes on the SPARK MAX.

        :returns: CANError Set to CANError.kOK if successful
        """
    def enableSoftLimit(self, direction: CANSparkMax.SoftLimitDirection, enable: bool) -> CANError: 
        """
        Enable soft limits

        :param direction: the direction of motion to restrict

        :param enable: set true to enable soft limits
        """
    def enableVoltageCompensation(self, nominalVoltage: float) -> CANError: 
        """
        Sets the voltage compensation setting for all modes on the SPARK MAX and
        enables voltage compensation.

        :param nominalVoltage: Nominal voltage to compensate output to

        :returns: CANError Set to CANError.kOK if successful
        """
    @typing.overload
    def follow(self, leader: CANSparkMax, invert: bool = False) -> CANError: 
        """
        Causes this controller's output to mirror the provided leader.

        Only voltage output is mirrored. Settings changed on the leader do not
        affect the follower.

        Following anything other than a CAN SPARK MAX is not officially supported.

        :param leader: The motor controller to follow.

        :param invert: Set the follower to output opposite of the leader

        Causes this controller's output to mirror the provided leader.

        Only voltage output is mirrored. Settings changed on the leader do not
        affect the follower.

        Following anything other than a CAN SPARK MAX is not officially supported.

        :param leader: The type of motor controller to follow (Talon SRX, Spark
                Max, etc.).

        :param deviceID: The CAN ID of the device to follow.

        :param invert: Set the follower to output opposite of the leader
        """
    @typing.overload
    def follow(self, leader: CANSparkMax.ExternalFollower, deviceID: int, invert: bool = False) -> CANError: ...
    def get(self) -> float: 
        """
        Common interface for getting the current set speed of a speed controller.

        :returns: The current set speed.  Value is between -1.0 and 1.0.
        """
    def getAlternateEncoder(self, sensorType: CANEncoder.AlternateEncoderType, counts_per_rev: int) -> CANEncoder: 
        """
        Returns an object for interfacing with the encoder connected to the alternate
        data port configured pins. This is defined as:

        Multi-function Pin: Encoder A
        Limit Switch Reverse : Encoder B

        This call will disable the limit switch inputs.
        """
    def getAnalog(self, mode: CANAnalog.AnalogMode = AnalogMode.kAbsolute) -> CANAnalog: 
        """
        Returns an object for interfacing with a connected analog sensor.
        By default, the AnalogMode is set to kAbsolute, thus treating the
        sensor as an absolute sensor.
        """
    def getAppliedOutput(self) -> float: 
        """
        Returns motor controller's output duty cycle.
        """
    def getBusVoltage(self) -> float: 
        """
        Returns the voltage fed into the motor controller.
        """
    def getClosedLoopRampRate(self) -> float: 
        """
        Get the configured closed loop ramp rate

        This is the maximum rate at which the motor controller's output
        is allowed to change.

        :returns: rampte rate time in seconds to go from 0 to full throttle.
        """
    def getEncoder(self, sensorType: CANEncoder.EncoderType = EncoderType.kHallSensor, counts_per_rev: int = 0) -> CANEncoder: 
        """
        Returns an object for interfacing with the encoder connected to the
        encoder pins or front port of the SPARK MAX.

        The default encoder type is assumed to be the hall effect for brushless.
        This can be modified for brushed DC to use an quadrature encoder.
        """
    def getFault(self, faultID: CANSparkMax.FaultID) -> bool: 
        """
        Returns whether the fault with the given ID occurred.
        """
    def getFaults(self) -> int: 
        """
        Returns fault bits.
        """
    def getForwardLimitSwitch(self, polarity: CANDigitalInput.LimitSwitchPolarity) -> CANDigitalInput: 
        """
        Returns an object for interfacing with the integrated forward limit
        switch.

        :param polarity: Whether the limit switch is normally open or normally
                closed.
        """
    def getIdleMode(self) -> CANSparkMax.IdleMode: 
        """
        Gets the idle mode setting for the SPARK MAX.

        This uses the Get Parameter API and should be used infrequently. This
        function uses a non-blocking call and will return a cached value if the
        parameter is not returned by the timeout. The timeout can be changed by
        calling SetCANTimeout(int milliseconds)

        :returns: IdleMode Idle mode setting
        """
    def getInverted(self) -> bool: 
        """
        Common interface for returning the inversion state of a speed controller.

        This call has no effect if the controller is a follower.

        :returns: isInverted The state of inversion, true is inverted.
        """
    def getLastError(self) -> CANError: 
        """
        All device errors are tracked on a per thread basis for all
        devices in that thread. This is meant to be called
        immediately following another call that has the possibility
        of throwing an error to validate if an  error has occurred.

        :returns: the last error that was generated.
        """
    def getMotorTemperature(self) -> float: 
        """
        Returns the motor temperature in Celsius.
        """
    def getOpenLoopRampRate(self) -> float: 
        """
        Get the configured open loop ramp rate

        This is the maximum rate at which the motor controller's output
        is allowed to change.

        :returns: rampte rate time in seconds to go from 0 to full throttle.
        """
    def getOutputCurrent(self) -> float: 
        """
        Returns motor controller's output current in Amps.
        """
    def getPIDController(self) -> CANPIDController: 
        """
        Returns an object for interfacing with the integrated PID controller.
        """
    def getReverseLimitSwitch(self, polarity: CANDigitalInput.LimitSwitchPolarity) -> CANDigitalInput: 
        """
        Returns an object for interfacing with the integrated reverse limit
        switch.

        :param polarity: Whether the limit switch is normally open or normally
                closed.
        """
    def getSoftLimit(self, direction: CANSparkMax.SoftLimitDirection) -> float: 
        """
        Get the soft limit setting in the controller

        :param direction: the direction of motion to restrict

        :returns: position soft limit setting of the controller
        """
    def getStickyFault(self, faultID: CANSparkMax.FaultID) -> bool: 
        """
        Returns whether the sticky fault with the given ID occurred.
        """
    def getStickyFaults(self) -> int: 
        """
        Returns sticky fault bits.
        """
    def getVoltageCompensationNominalVoltage(self) -> float: 
        """
        Get the configured voltage compensation nominal voltage value

        :returns: The nominal voltage for voltage compensation mode.
        """
    def isFollower(self) -> bool: 
        """
        Returns whether the controller is following another controller

        :returns: True if this device is following another controller
                  false otherwise
        """
    def isSoftLimitEnabled(self, direction: CANSparkMax.SoftLimitDirection) -> bool: 
        """
        Returns true if the soft limit is enabled.
        """
    def set(self, speed: float) -> None: 
        """
        Common interface for setting the speed of a speed controller.

        :param speed: The speed to set.  Value should be between -1.0 and 1.0.
        """
    def setCANTimeout(self, milliseconds: int) -> CANError: 
        """
        Sets timeout for sending CAN messages. A timeout of 0 also means that error handling
        will be done automatically by registering calls and waiting for responses, rather
        than needing to call GetLastError().

        :param milliseconds: The timeout in milliseconds.
        """
    def setClosedLoopRampRate(self, rate: float) -> CANError: 
        """
        Sets the ramp rate for closed loop control modes.

        This is the maximum rate at which the motor controller's output
        is allowed to change.

        :param rate: Time in seconds to go from 0 to full throttle.
        """
    def setIdleMode(self, mode: CANSparkMax.IdleMode) -> CANError: 
        """
        Sets the idle mode setting for the SPARK MAX.

        :param mode: Idle mode (coast or brake).
        """
    def setInverted(self, isInverted: bool) -> None: 
        """
        Common interface for inverting direction of a speed controller.

        This call has no effect if the controller is a follower. To invert
        a follower, see the follow() method.

        :param isInverted: The state of inversion, true is inverted.
        """
    def setOpenLoopRampRate(self, rate: float) -> CANError: 
        """
        Sets the ramp rate for open loop control modes.

        This is the maximum rate at which the motor controller's output
        is allowed to change.

        :param rate: Time in seconds to go from 0 to full throttle.
        """
    def setSecondaryCurrentLimit(self, limit: float, limitCycles: int = 0) -> CANError: 
        """
        Sets the secondary current limit in Amps.

        The motor controller will disable the output of the controller briefly
        if the current limit is exceeded to reduce the current. This limit is
        a simplified 'on/off' controller. This limit is enabled by default
        but is set higher than the default Smart Current Limit.

        The time the controller is off after the current limit is reached
        is determined by the parameter limitCycles, which is the number of
        PWM cycles (20kHz). The recommended value is the default of 0 which
        is the minimum time and is part of a PWM cycle from when the over
        current is detected. This allows the controller to regulate the current
        close to the limit value.

        The total time is set by the equation

        @code t = (50us - t0) + 50us * limitCycles
        t = total off time after over current
        t0 = time from the start of the PWM cycle until over current is detected
        @endcode

        :param limit: The current limit in Amps.

        :param limitCycles: The number of additional PWM cycles to turn
                   the driver off after overcurrent is detected.
        """
    @typing.overload
    def setSmartCurrentLimit(self, limit: int) -> CANError: 
        """
        Sets the current limit in Amps.

        The motor controller will reduce the controller voltage output to avoid
        surpassing this limit. This limit is enabled by default and used for
        brushless only. This limit is highly recommended when using the NEO
        brushless motor.

        The NEO Brushless Motor has a low internal resistance, which
        can mean large current spikes that could be enough to cause damage to
        the motor and controller. This current limit provides a smarter
        strategy to deal with high current draws and keep the motor and
        controller operating in a safe region.

        :param limit: The current limit in Amps.

        Sets the current limit in Amps.

        The motor controller will reduce the controller voltage output to avoid
        surpassing this limit. This limit is enabled by default and used for
        brushless only. This limit is highly recommended when using the NEO
        brushless motor.

        The NEO Brushless Motor has a low internal resistance, which
        can mean large current spikes that could be enough to cause damage to
        the motor and controller. This current limit provides a smarter
        strategy to deal with high current draws and keep the motor and
        controller operating in a safe region.

        The controller can also limit the current based on the RPM of the motor
        in a linear fashion to help with controllability in closed loop control.
        For a response that is linear the entire RPM range leave limit RPM at 0.

        :param stallLimit: The current limit in Amps at 0 RPM.

        :param freeLimit: The current limit at free speed (5700RPM for NEO).

        :param limitRPM: RPM less than this value will be set to the stallLimit,
                  RPM values greater than limitRPM will scale linearly to freeLimit
        """
    @typing.overload
    def setSmartCurrentLimit(self, stallLimit: int, freeLimit: int, limitRPM: int = 20000) -> CANError: ...
    def setSoftLimit(self, direction: CANSparkMax.SoftLimitDirection, limit: float) -> CANError: 
        """
        Set the soft limit based on position. The default unit is
        rotations, but will match the unit scaling set by the user.

        Note that this value is not scaled internally so care must
        be taken to make sure these units match the desired conversion

        :param direction: the direction of motion to restrict

        :param limit: position soft limit of the controller
        """
    def setVoltage(self, output: volts) -> None: 
        """
        Sets the voltage output of the SpeedController.  This is equivillant to
        a call to SetReference(output, rev::ControlType::kVoltage). The behavior
        of this call differs slightly from the WPILib documetation for this call
        since the device internally sets the desired voltage (not a compensation value).
        That means that this *can* be a 'set-and-forget' call.

        :param output: The voltage to output.
        """
    def stopMotor(self) -> None: 
        """
        Common interface to stop the motor until Set is called again.
        """
    kAPIVersion = 1573398015
    pass
class ControlType():
    """
    Members:

      kDutyCycle

      kVelocity

      kVoltage

      kPosition

      kSmartMotion

      kCurrent

      kSmartVelocity
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
    __members__: dict # value = {'kDutyCycle': ControlType.kDutyCycle, 'kVelocity': ControlType.kVelocity, 'kVoltage': ControlType.kVoltage, 'kPosition': ControlType.kPosition, 'kSmartMotion': ControlType.kSmartMotion, 'kCurrent': ControlType.kCurrent, 'kSmartVelocity': ControlType.kSmartVelocity}
    kCurrent: rev._rev.ControlType # value = ControlType.kCurrent
    kDutyCycle: rev._rev.ControlType # value = ControlType.kDutyCycle
    kPosition: rev._rev.ControlType # value = ControlType.kPosition
    kSmartMotion: rev._rev.ControlType # value = ControlType.kSmartMotion
    kSmartVelocity: rev._rev.ControlType # value = ControlType.kSmartVelocity
    kVelocity: rev._rev.ControlType # value = ControlType.kVelocity
    kVoltage: rev._rev.ControlType # value = ControlType.kVoltage
    pass
class SparkMax(wpilib._wpilib.PWMSpeedController, wpilib._wpilib.PWM, wpilib._wpilib.MotorSafety, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable, wpilib.interfaces._interfaces.SpeedController, wpilib.interfaces._interfaces.PIDOutput):
    """
    REV Robotics CAN speed controller controlled via PWM.
    """
    def __init__(self, channel: int) -> None: 
        """
        Constructor for a Spark Max.

        :param channel: The PWM channel that the Spark is attached to. 0-9 are
               on-board, 10-19 are on the MXP port
        """
    pass
