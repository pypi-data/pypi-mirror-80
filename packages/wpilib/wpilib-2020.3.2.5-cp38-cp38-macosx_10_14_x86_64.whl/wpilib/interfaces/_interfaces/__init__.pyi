import wpilib.interfaces._interfaces
import typing
import Accelerometer
import GenericHID
import Hand

__all__ = [
    "Accelerometer",
    "CounterBase",
    "GenericHID",
    "Gyro",
    "PIDOutput",
    "PIDSource",
    "PIDSourceType",
    "Potentiometer",
    "SpeedController"
]


class Accelerometer():
    """
    Interface for 3-axis accelerometers.
    """
    class Range():
        """
        Members:

          kRange_2G

          kRange_4G

          kRange_8G

          kRange_16G
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
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
        __members__: dict # value = {'kRange_2G': Range.kRange_2G, 'kRange_4G': Range.kRange_4G, 'kRange_8G': Range.kRange_8G, 'kRange_16G': Range.kRange_16G}
        kRange_16G: wpilib.interfaces._interfaces.Accelerometer.Range # value = Range.kRange_16G
        kRange_2G: wpilib.interfaces._interfaces.Accelerometer.Range # value = Range.kRange_2G
        kRange_4G: wpilib.interfaces._interfaces.Accelerometer.Range # value = Range.kRange_4G
        kRange_8G: wpilib.interfaces._interfaces.Accelerometer.Range # value = Range.kRange_8G
        pass
    def __init__(self) -> None: ...
    def getX(self) -> float: 
        """
        Common interface for getting the x axis acceleration.

        :returns: The acceleration along the x axis in g-forces
        """
    def getY(self) -> float: 
        """
        Common interface for getting the y axis acceleration.

        :returns: The acceleration along the y axis in g-forces
        """
    def getZ(self) -> float: 
        """
        Common interface for getting the z axis acceleration.

        :returns: The acceleration along the z axis in g-forces
        """
    def setRange(self, range: Accelerometer.Range) -> None: 
        """
        Common interface for setting the measuring range of an accelerometer.

        :param range: The maximum acceleration, positive or negative, that the
             accelerometer will measure. Not all accelerometers support all
             ranges.
        """
    pass
class CounterBase():
    """
    Interface for counting the number of ticks on a digital input channel.

    Encoders, Gear tooth sensors, and counters should all subclass this so it can
    be used to build more advanced classes for control and driving.

    All counters will immediately start counting - Reset() them if you need them
    to be zeroed before use.
    """
    class EncodingType():
        """
        Members:

          k1X

          k2X

          k4X
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
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
        __members__: dict # value = {'k1X': EncodingType.k1X, 'k2X': EncodingType.k2X, 'k4X': EncodingType.k4X}
        k1X: wpilib.interfaces._interfaces.CounterBase.EncodingType # value = EncodingType.k1X
        k2X: wpilib.interfaces._interfaces.CounterBase.EncodingType # value = EncodingType.k2X
        k4X: wpilib.interfaces._interfaces.CounterBase.EncodingType # value = EncodingType.k4X
        pass
    def __init__(self) -> None: ...
    def get(self) -> int: ...
    def getDirection(self) -> bool: ...
    def getPeriod(self) -> float: ...
    def getStopped(self) -> bool: ...
    def reset(self) -> None: ...
    def setMaxPeriod(self, maxPeriod: float) -> None: ...
    pass
class GenericHID():
    """
    GenericHID Interface.
    """
    class HIDType():
        """
        Members:

          kUnknown

          kXInputUnknown

          kXInputGamepad

          kXInputWheel

          kXInputArcadeStick

          kXInputFlightStick

          kXInputDancePad

          kXInputGuitar

          kXInputGuitar2

          kXInputDrumKit

          kXInputGuitar3

          kXInputArcadePad

          kHIDJoystick

          kHIDGamepad

          kHIDDriving

          kHIDFlight

          kHID1stPerson
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
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
        __members__: dict # value = {'kUnknown': HIDType.kUnknown, 'kXInputUnknown': HIDType.kXInputUnknown, 'kXInputGamepad': HIDType.kXInputGamepad, 'kXInputWheel': HIDType.kXInputWheel, 'kXInputArcadeStick': HIDType.kXInputArcadeStick, 'kXInputFlightStick': HIDType.kXInputFlightStick, 'kXInputDancePad': HIDType.kXInputDancePad, 'kXInputGuitar': HIDType.kXInputGuitar, 'kXInputGuitar2': HIDType.kXInputGuitar2, 'kXInputDrumKit': HIDType.kXInputDrumKit, 'kXInputGuitar3': HIDType.kXInputGuitar3, 'kXInputArcadePad': HIDType.kXInputArcadePad, 'kHIDJoystick': HIDType.kHIDJoystick, 'kHIDGamepad': HIDType.kHIDGamepad, 'kHIDDriving': HIDType.kHIDDriving, 'kHIDFlight': HIDType.kHIDFlight, 'kHID1stPerson': HIDType.kHID1stPerson}
        kHID1stPerson: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kHID1stPerson
        kHIDDriving: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kHIDDriving
        kHIDFlight: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kHIDFlight
        kHIDGamepad: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kHIDGamepad
        kHIDJoystick: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kHIDJoystick
        kUnknown: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kUnknown
        kXInputArcadePad: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputArcadePad
        kXInputArcadeStick: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputArcadeStick
        kXInputDancePad: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputDancePad
        kXInputDrumKit: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputDrumKit
        kXInputFlightStick: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputFlightStick
        kXInputGamepad: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputGamepad
        kXInputGuitar: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputGuitar
        kXInputGuitar2: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputGuitar2
        kXInputGuitar3: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputGuitar3
        kXInputUnknown: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputUnknown
        kXInputWheel: wpilib.interfaces._interfaces.GenericHID.HIDType # value = HIDType.kXInputWheel
        pass
    class Hand():
        """
        Members:

          kLeftHand

          kRightHand
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
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
        __members__: dict # value = {'kLeftHand': Hand.kLeftHand, 'kRightHand': Hand.kRightHand}
        kLeftHand: wpilib.interfaces._interfaces.GenericHID.Hand # value = Hand.kLeftHand
        kRightHand: wpilib.interfaces._interfaces.GenericHID.Hand # value = Hand.kRightHand
        pass
    class RumbleType():
        """
        Members:

          kLeftRumble

          kRightRumble
        """
        def __eq__(self, arg0: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
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
        __members__: dict # value = {'kLeftRumble': RumbleType.kLeftRumble, 'kRightRumble': RumbleType.kRightRumble}
        kLeftRumble: wpilib.interfaces._interfaces.GenericHID.RumbleType # value = RumbleType.kLeftRumble
        kRightRumble: wpilib.interfaces._interfaces.GenericHID.RumbleType # value = RumbleType.kRightRumble
        pass
    def __init__(self, port: int) -> None: ...
    def getAxisCount(self) -> int: 
        """
        Get the number of axes for the HID.

        :returns: the number of axis for the current HID
        """
    def getAxisType(self, axis: int) -> int: 
        """
        Get the axis type of a joystick axis.

        :returns: the axis type of a joystick axis.
        """
    def getButtonCount(self) -> int: 
        """
        Get the number of buttons for the HID.

        :returns: the number of buttons on the current HID
        """
    def getName(self) -> str: 
        """
        Get the name of the HID.

        :returns: the name of the HID.
        """
    def getPOV(self, pov: int = 0) -> int: 
        """
        Get the angle in degrees of a POV on the HID.

        The POV angles start at 0 in the up direction, and increase clockwise
        (e.g. right is 90, upper-left is 315).

        :param pov: The index of the POV to read (starting at 0)

        :returns: the angle of the POV in degrees, or -1 if the POV is not pressed.
        """
    def getPOVCount(self) -> int: 
        """
        Get the number of POVs for the HID.

        :returns: the number of POVs for the current HID
        """
    def getPort(self) -> int: 
        """
        Get the port number of the HID.

        :returns: The port number of the HID.
        """
    def getRawAxis(self, axis: int) -> float: 
        """
        Get the value of the axis.

        :param axis: The axis to read, starting at 0.

        :returns: The value of the axis.
        """
    def getRawButton(self, button: int) -> bool: 
        """
        Get the button value (starting at button 1).

        The buttons are returned in a single 16 bit value with one bit representing
        the state of each button. The appropriate button is returned as a boolean
        value.

        :param button: The button number to be read (starting at 1)

        :returns: The state of the button.
        """
    def getRawButtonPressed(self, button: int) -> bool: 
        """
        Whether the button was pressed since the last check. Button indexes begin
        at 1.

        :param button: The button index, beginning at 1.

        :returns: Whether the button was pressed since the last check.
        """
    def getRawButtonReleased(self, button: int) -> bool: 
        """
        Whether the button was released since the last check. Button indexes begin
        at 1.

        :param button: The button index, beginning at 1.

        :returns: Whether the button was released since the last check.
        """
    def getType(self) -> GenericHID.HIDType: 
        """
        Get the type of the HID.

        :returns: the type of the HID.
        """
    def getX(self, hand: GenericHID.Hand = Hand.kRightHand) -> float: ...
    def getY(self, hand: GenericHID.Hand = Hand.kRightHand) -> float: ...
    def setOutput(self, outputNumber: int, value: bool) -> None: 
        """
        Set a single HID output value for the HID.

        :param outputNumber: The index of the output to set (1-32)

        :param value: The value to set the output to
        """
    def setOutputs(self, value: int) -> None: 
        """
        Set all output values for the HID.

        :param value: The 32 bit output value (1 bit for each output)
        """
    def setRumble(self, type: GenericHID.RumbleType, value: float) -> None: 
        """
        Set the rumble output for the HID.

        The DS currently supports 2 rumble values, left rumble and right rumble.

        :param type: Which rumble value to set

        :param value: The normalized value (0 to 1) to set the rumble to
        """
    pass
class Gyro():
    """
    Interface for yaw rate gyros.
    """
    def __init__(self) -> None: ...
    def calibrate(self) -> None: 
        """
        Calibrate the gyro by running for a number of samples and computing the
        center value. Then use the center value as the Accumulator center value for
        subsequent measurements. It's important to make sure that the robot is not
        moving while the centering calculations are in progress, this is typically
        done when the robot is first turned on while it's sitting at rest before
        the competition starts.
        """
    def getAngle(self) -> float: 
        """
        Return the actual angle in degrees that the robot is currently facing.

        The angle is based on the current accumulator value corrected by the
        oversampling rate, the gyro type and the A/D calibration values. The angle
        is continuous, that is it will continue from 360 to 361 degrees. This
        allows algorithms that wouldn't want to see a discontinuity in the gyro
        output as it sweeps past from 360 to 0 on the second time around.

        The angle is expected to increase as the gyro turns clockwise when looked
        at from the top. It needs to follow NED axis conventions in order to work
        properly with dependent control loops.

        :returns: the current heading of the robot in degrees. This heading is based
                  on integration of the returned rate from the gyro.
        """
    def getRate(self) -> float: 
        """
        Return the rate of rotation of the gyro.

        The rate is based on the most recent reading of the gyro analog value.

        The rate is expected to be positive as the gyro turns clockwise when looked
        at from the top. It needs to follow NED axis conventions in order to work
        properly with dependent control loops.

        :returns: the current rate in degrees per second
        """
    def reset(self) -> None: 
        """
        Reset the gyro. Resets the gyro to a heading of zero. This can be used if
        there is significant drift in the gyro and it needs to be recalibrated
        after it has been running.
        """
    pass
class PIDOutput():
    """
    PIDOutput interface is a generic output for the PID class.

    PWMs use this class. Users implement this interface to allow for a
    PIDController to read directly from the inputs.
    """
    def __init__(self) -> None: ...
    def pidWrite(self, output: float) -> None: ...
    pass
class PIDSource():
    """
    PIDSource interface is a generic sensor source for the PID class.

    All sensors that can be used with the PID class will implement the PIDSource
    that returns a standard value that will be used in the PID code.
    """
    def __init__(self) -> None: ...
    def getPIDSourceType(self) -> PIDSourceType: ...
    def pidGet(self) -> float: ...
    def setPIDSourceType(self, pidSource: PIDSourceType) -> None: 
        """
        Set which parameter you are using as a process control variable.

        :param pidSource: An enum to select the parameter.
        """
    @property
    def _m_pidSource(self) -> PIDSourceType:
        """
        :type: PIDSourceType
        """
    @_m_pidSource.setter
    def _m_pidSource(self, arg0: PIDSourceType) -> None:
        pass
    pass
class PIDSourceType():
    """
    Members:

      kDisplacement

      kRate
    """
    def __eq__(self, arg0: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
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
    __members__: dict # value = {'kDisplacement': PIDSourceType.kDisplacement, 'kRate': PIDSourceType.kRate}
    kDisplacement: wpilib.interfaces._interfaces.PIDSourceType # value = PIDSourceType.kDisplacement
    kRate: wpilib.interfaces._interfaces.PIDSourceType # value = PIDSourceType.kRate
    pass
class Potentiometer(PIDSource):
    """
    Interface for potentiometers.
    """
    def __init__(self) -> None: ...
    def get(self) -> float: 
        """
        Common interface for getting the current value of a potentiometer.

        :returns: The current set speed. Value is between -1.0 and 1.0.
        """
    def setPIDSourceType(self, pidSource: PIDSourceType) -> None: ...
    pass
class SpeedController(PIDOutput):
    """
    Interface for speed controlling devices.
    """
    def __init__(self) -> None: ...
    def disable(self) -> None: 
        """
        Common interface for disabling a motor.
        """
    def get(self) -> float: 
        """
        Common interface for getting the current set speed of a speed controller.

        :returns: The current set speed.  Value is between -1.0 and 1.0.
        """
    def getInverted(self) -> bool: 
        """
        Common interface for returning the inversion state of a speed controller.

        :returns: isInverted The state of inversion, true is inverted.
        """
    def set(self, speed: float) -> None: 
        """
        Common interface for setting the speed of a speed controller.

        :param speed: The speed to set.  Value should be between -1.0 and 1.0.
        """
    def setInverted(self, isInverted: bool) -> None: 
        """
        Common interface for inverting direction of a speed controller.

        :param isInverted: The state of inversion, true is inverted.
        """
    def setVoltage(self, output: volts) -> None: 
        """
        Sets the voltage output of the SpeedController.  Compensates for
        the current bus voltage to ensure that the desired voltage is output even
        if the battery voltage is below 12V - highly useful when the voltage
        outputs are "meaningful" (e.g. they come from a feedforward calculation).

        NOTE: This function *must* be called regularly in order for voltage
        compensation to work properly - unlike the ordinary set function, it is not
        "set it and forget it."

        :param output: The voltage to output.
        """
    def stopMotor(self) -> None: 
        """
        Common interface to stop the motor until Set is called again.
        """
    pass
