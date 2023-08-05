import wpilib.controller._controller.controller
import typing
import wpilib._wpilib
import wpilib.controller._controller.trajectory.Trajectory
import wpilib.controller._controller.trajectory.TrapezoidProfile
import wpilib.geometry._geometry
import wpilib.kinematics._kinematics

__all__ = [
    "ArmFeedforward",
    "ElevatorFeedforward",
    "ElevatorFeedforwardFeet",
    "ElevatorFeedforwardMeters",
    "PIDController",
    "ProfiledPIDController",
    "RamseteController",
    "SimpleMotorFeedforward",
    "SimpleMotorFeedforwardFeet",
    "SimpleMotorFeedforwardMeters"
]


class ArmFeedforward():
    """
    A helper class that computes feedforward outputs for a simple arm (modeled as
    a motor acting against the force of gravity on a beam suspended at an angle).
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new ArmFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kCos: The gravity gain, in volts.

        :param kV: The velocity gain, in volt seconds per radian.

        :param kA: The acceleration gain, in volt seconds^2 per radian.
        """
    @typing.overload
    def __init__(self, kS: volts, kCos: volts, kV: volt_seconds_per_radian, kA: volt_seconds_squared_per_radian = 0.0) -> None: ...
    def calculate(self, angle: radians, velocity: radians_per_second, acceleration: radians_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param angle: The angle setpoint, in radians.

        :param velocity: The velocity setpoint, in radians per second.

        :param acceleration: The acceleration setpoint, in radians per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, angle: radians, velocity: radians_per_second) -> radians_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply, a position, and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the arm.

        :param angle: The angle of the arm

        :param velocity: The velocity of the arm.

        :returns: The maximum possible acceleration at the given velocity and angle.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, angle: radians, acceleration: radians_per_second_squared) -> radians_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply,
        a position, and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the arm.

        :param angle: The angle of the arm

        :param acceleration: The acceleration of the arm.

        :returns: The maximum possible velocity at the given acceleration and angle.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, angle: radians, velocity: radians_per_second) -> radians_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply, a position, and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the arm.

        :param angle: The angle of the arm

        :param velocity: The velocity of the arm.

        :returns: The minimum possible acceleration at the given velocity and angle.
        """
    def minAchievableVelocity(self, maxVoltage: volts, angle: radians, acceleration: radians_per_second_squared) -> radians_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply,
        a position, and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the arm.

        :param angle: The angle of the arm

        :param acceleration: The acceleration of the arm.

        :returns: The minimum possible velocity at the given acceleration and angle.
        """
    @property
    def kA(self) -> volt_seconds_squared_per_radian:
        """
        :type: volt_seconds_squared_per_radian
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared_per_radian) -> None:
        pass
    @property
    def kCos(self) -> volts:
        """
        :type: volts
        """
    @kCos.setter
    def kCos(self, arg0: volts) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds_per_radian:
        """
        :type: volt_seconds_per_radian
        """
    @kV.setter
    def kV(self, arg0: volt_seconds_per_radian) -> None:
        pass
    pass
class ElevatorFeedforward():
    """
    A helper class that computes feedforward outputs for a simple elevator
    (modeled as a motor acting against the force of gravity).
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new ElevatorFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kG: The gravity gain, in volts.

        :param kV: The velocity gain, in volt seconds per distance.

        :param kA: The acceleration gain, in volt seconds^2 per distance.
        """
    @typing.overload
    def __init__(self, kS: volts, kG: volts, kV: volt_seconds, kA: volt_seconds_squared = 0.0) -> None: ...
    def calculate(self, velocity: units_per_second, acceleration: units_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param velocity: The velocity setpoint, in distance per second.

        :param acceleration: The acceleration setpoint, in distance per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, velocity: units_per_second) -> units_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param velocity: The velocity of the elevator.

        :returns: The maximum possible acceleration at the given velocity.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, acceleration: units_per_second_squared) -> units_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param acceleration: The acceleration of the elevator.

        :returns: The maximum possible velocity at the given acceleration.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, velocity: units_per_second) -> units_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param velocity: The velocity of the elevator.

        :returns: The minimum possible acceleration at the given velocity.
        """
    def minAchievableVelocity(self, maxVoltage: volts, acceleration: units_per_second_squared) -> units_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param acceleration: The acceleration of the elevator.

        :returns: The minimum possible velocity at the given acceleration.
        """
    @property
    def kA(self) -> volt_seconds_squared:
        """
        :type: volt_seconds_squared
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared) -> None:
        pass
    @property
    def kG(self) -> volts:
        """
        :type: volts
        """
    @kG.setter
    def kG(self, arg0: volts) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds:
        """
        :type: volt_seconds
        """
    @kV.setter
    def kV(self, arg0: volt_seconds) -> None:
        pass
    pass
class ElevatorFeedforwardFeet():
    """
    A helper class that computes feedforward outputs for a simple elevator
    (modeled as a motor acting against the force of gravity).
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new ElevatorFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kG: The gravity gain, in volts.

        :param kV: The velocity gain, in volt seconds per distance.

        :param kA: The acceleration gain, in volt seconds^2 per distance.
        """
    @typing.overload
    def __init__(self, kS: volts, kG: volts, kV: volt_seconds_per_feet, kA: volt_seconds_squared_per_feet = 0.0) -> None: ...
    def calculate(self, velocity: feet_per_second, acceleration: feet_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param velocity: The velocity setpoint, in distance per second.

        :param acceleration: The acceleration setpoint, in distance per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, velocity: feet_per_second) -> feet_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param velocity: The velocity of the elevator.

        :returns: The maximum possible acceleration at the given velocity.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, acceleration: feet_per_second_squared) -> feet_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param acceleration: The acceleration of the elevator.

        :returns: The maximum possible velocity at the given acceleration.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, velocity: feet_per_second) -> feet_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param velocity: The velocity of the elevator.

        :returns: The minimum possible acceleration at the given velocity.
        """
    def minAchievableVelocity(self, maxVoltage: volts, acceleration: feet_per_second_squared) -> feet_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param acceleration: The acceleration of the elevator.

        :returns: The minimum possible velocity at the given acceleration.
        """
    @property
    def kA(self) -> volt_seconds_squared_per_feet:
        """
        :type: volt_seconds_squared_per_feet
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared_per_feet) -> None:
        pass
    @property
    def kG(self) -> volts:
        """
        :type: volts
        """
    @kG.setter
    def kG(self, arg0: volts) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds_per_feet:
        """
        :type: volt_seconds_per_feet
        """
    @kV.setter
    def kV(self, arg0: volt_seconds_per_feet) -> None:
        pass
    pass
class ElevatorFeedforwardMeters():
    """
    A helper class that computes feedforward outputs for a simple elevator
    (modeled as a motor acting against the force of gravity).
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new ElevatorFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kG: The gravity gain, in volts.

        :param kV: The velocity gain, in volt seconds per distance.

        :param kA: The acceleration gain, in volt seconds^2 per distance.
        """
    @typing.overload
    def __init__(self, kS: volts, kG: volts, kV: volt_seconds_per_meter, kA: volt_seconds_squared_per_meter = 0.0) -> None: ...
    def calculate(self, velocity: meters_per_second, acceleration: meters_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param velocity: The velocity setpoint, in distance per second.

        :param acceleration: The acceleration setpoint, in distance per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, velocity: meters_per_second) -> meters_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param velocity: The velocity of the elevator.

        :returns: The maximum possible acceleration at the given velocity.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, acceleration: meters_per_second_squared) -> meters_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param acceleration: The acceleration of the elevator.

        :returns: The maximum possible velocity at the given acceleration.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, velocity: meters_per_second) -> meters_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param velocity: The velocity of the elevator.

        :returns: The minimum possible acceleration at the given velocity.
        """
    def minAchievableVelocity(self, maxVoltage: volts, acceleration: meters_per_second_squared) -> meters_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the elevator.

        :param acceleration: The acceleration of the elevator.

        :returns: The minimum possible velocity at the given acceleration.
        """
    @property
    def kA(self) -> volt_seconds_squared_per_meter:
        """
        :type: volt_seconds_squared_per_meter
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared_per_meter) -> None:
        pass
    @property
    def kG(self) -> volts:
        """
        :type: volts
        """
    @kG.setter
    def kG(self, arg0: volts) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds_per_meter:
        """
        :type: volt_seconds_per_meter
        """
    @kV.setter
    def kV(self, arg0: volt_seconds_per_meter) -> None:
        pass
    pass
class PIDController(wpilib._wpilib.Sendable):
    """
    Implements a PID control loop.
    """
    def __init__(self, Kp: float, Ki: float, Kd: float, period: seconds = 0.02) -> None: 
        """
        Allocates a PIDController with the given constants for Kp, Ki, and Kd.

        :param Kp: The proportional coefficient.

        :param Ki: The integral coefficient.

        :param Kd: The derivative coefficient.

        :param period: The period between controller updates in seconds. The
              default is 20 milliseconds.
        """
    def _getContinuousError(self, error: float) -> float: 
        """
        Wraps error around for continuous inputs. The original error is returned if
        continuous mode is disabled.

        :param error: The current error of the PID controller.

        :returns: Error for continuous inputs.
        """
    def atSetpoint(self) -> bool: 
        """
        Returns true if the error is within the tolerance of the error.

        This will return false until at least one input value has been computed.
        """
    @typing.overload
    def calculate(self, measurement: float) -> float: 
        """
        Returns the next output of the PID controller.

        :param measurement: The current measurement of the process variable.

        Returns the next output of the PID controller.

        :param measurement: The current measurement of the process variable.

        :param setpoint: The new setpoint of the controller.
        """
    @typing.overload
    def calculate(self, measurement: float, setpoint: float) -> float: ...
    def disableContinuousInput(self) -> None: 
        """
        Disables continuous input.
        """
    def enableContinuousInput(self, minimumInput: float, maximumInput: float) -> None: 
        """
        Enables continuous input.

        Rather then using the max and min input range as constraints, it considers
        them to be the same point and automatically calculates the shortest route
        to the setpoint.

        :param minimumInput: The minimum value expected from the input.

        :param maximumInput: The maximum value expected from the input.
        """
    def getD(self) -> float: 
        """
        Gets the differential coefficient.

        :returns: differential coefficient
        """
    def getI(self) -> float: 
        """
        Gets the integral coefficient.

        :returns: integral coefficient
        """
    def getP(self) -> float: 
        """
        Gets the proportional coefficient.

        :returns: proportional coefficient
        """
    def getPeriod(self) -> seconds: 
        """
        Gets the period of this controller.

        :returns: The period of the controller.
        """
    def getPositionError(self) -> float: 
        """
        Returns the difference between the setpoint and the measurement.
        """
    def getSetpoint(self) -> float: 
        """
        Returns the current setpoint of the PIDController.

        :returns: The current setpoint.
        """
    def getVelocityError(self) -> float: 
        """
        Returns the velocity error.
        """
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def reset(self) -> None: 
        """
        Reset the previous error, the integral term, and disable the controller.
        """
    def setD(self, Kd: float) -> None: 
        """
        Sets the differential coefficient of the PID controller gain.

        :param Kd: differential coefficient
        """
    def setI(self, Ki: float) -> None: 
        """
        Sets the integral coefficient of the PID controller gain.

        :param Ki: integral coefficient
        """
    def setIntegratorRange(self, minimumIntegral: float, maximumIntegral: float) -> None: 
        """
        Sets the minimum and maximum values for the integrator.

        When the cap is reached, the integrator value is added to the controller
        output rather than the integrator value times the integral gain.

        :param minimumIntegral: The minimum value of the integrator.

        :param maximumIntegral: The maximum value of the integrator.
        """
    def setP(self, Kp: float) -> None: 
        """
        Sets the proportional coefficient of the PID controller gain.

        :param Kp: proportional coefficient
        """
    def setPID(self, Kp: float, Ki: float, Kd: float) -> None: 
        """
        Sets the PID Controller gain parameters.

        Sets the proportional, integral, and differential coefficients.

        :param Kp: Proportional coefficient

        :param Ki: Integral coefficient

        :param Kd: Differential coefficient
        """
    def setSetpoint(self, setpoint: float) -> None: 
        """
        Sets the setpoint for the PIDController.

        :param setpoint: The desired setpoint.
        """
    def setTolerance(self, positionTolerance: float, velocityTolerance: float = inf) -> None: 
        """
        Sets the error which is considered tolerable for use with AtSetpoint().

        :param positionTolerance: Position error which is tolerable.

        :param velociytTolerance: Velocity error which is tolerable.
        """
    pass
class ProfiledPIDController(wpilib._wpilib.Sendable):
    """
    Implements a PID control loop whose setpoint is constrained by a trapezoid
    profile.
    """
    def __init__(self, Kp: float, Ki: float, Kd: float, constraints: wpilib.controller._controller.trajectory.TrapezoidProfile.Constraints, period: seconds = 0.02) -> None: 
        """
        Allocates a ProfiledPIDController with the given constants for Kp, Ki, and
        Kd. Users should call reset() when they first start running the controller
        to avoid unwanted behavior.

        :param Kp: The proportional coefficient.

        :param Ki: The integral coefficient.

        :param Kd: The derivative coefficient.

        :param constraints: Velocity and acceleration constraints for goal.

        :param period: The period between controller updates in seconds. The
                   default is 20 milliseconds.
        """
    def atGoal(self) -> bool: 
        """
        Returns true if the error is within the tolerance of the error.

        This will return false until at least one input value has been computed.
        """
    def atSetpoint(self) -> bool: 
        """
        Returns true if the error is within the tolerance of the error.

        Currently this just reports on target as the actual value passes through
        the setpoint. Ideally it should be based on being within the tolerance for
        some period of time.

        This will return false until at least one input value has been computed.
        """
    @typing.overload
    def calculate(self, measurement: float) -> float: 
        """
        Returns the next output of the PID controller.

        :param measurement: The current measurement of the process variable.

        Returns the next output of the PID controller.

        :param measurement: The current measurement of the process variable.

        :param goal: The new goal of the controller.

        Returns the next output of the PID controller.

        :param measurement: The current measurement of the process variable.

        :param goal: The new goal of the controller.

        Returns the next output of the PID controller.

        :param measurement: The current measurement of the process variable.

        :param goal: The new goal of the controller.

        :param constraints: Velocity and acceleration constraints for goal.
        """
    @typing.overload
    def calculate(self, measurement: float, goal: float) -> float: ...
    @typing.overload
    def calculate(self, measurement: float, goal: float, constraints: wpilib.controller._controller.trajectory.TrapezoidProfile.Constraints) -> float: ...
    @typing.overload
    def calculate(self, measurement: float, goal: wpilib.controller._controller.trajectory.TrapezoidProfile.State) -> float: ...
    def disableContinuousInput(self) -> None: 
        """
        Disables continuous input.
        """
    def enableContinuousInput(self, minimumInput: float, maximumInput: float) -> None: 
        """
        Enables continuous input.

        Rather then using the max and min input range as constraints, it considers
        them to be the same point and automatically calculates the shortest route
        to the setpoint.

        :param minimumInput: The minimum value expected from the input.

        :param maximumInput: The maximum value expected from the input.
        """
    def getD(self) -> float: 
        """
        Gets the differential coefficient.

        :returns: differential coefficient
        """
    def getGoal(self) -> wpilib.controller._controller.trajectory.TrapezoidProfile.State: 
        """
        Gets the goal for the ProfiledPIDController.
        """
    def getI(self) -> float: 
        """
        Gets the integral coefficient.

        :returns: integral coefficient
        """
    def getP(self) -> float: 
        """
        Gets the proportional coefficient.

        :returns: proportional coefficient
        """
    def getPeriod(self) -> seconds: 
        """
        Gets the period of this controller.

        :returns: The period of the controller.
        """
    def getPositionError(self) -> float: 
        """
        Returns the difference between the setpoint and the measurement.

        :returns: The error.
        """
    def getSetpoint(self) -> wpilib.controller._controller.trajectory.TrapezoidProfile.State: 
        """
        Returns the current setpoint of the ProfiledPIDController.

        :returns: The current setpoint.
        """
    def getVelocityError(self) -> units_per_second: 
        """
        Returns the change in error per second.
        """
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    @typing.overload
    def reset(self, measuredPosition: float) -> None: 
        """
        Reset the previous error and the integral term.

        :param measurement: The current measured State of the system.

        Reset the previous error and the integral term.

        :param measuredPosition: The current measured position of the system.

        :param measuredVelocity: The current measured velocity of the system.

        Reset the previous error and the integral term.

        :param measuredPosition: The current measured position of the system. The
                        velocity is assumed to be zero.
        """
    @typing.overload
    def reset(self, measuredPosition: float, measuredVelocity: units_per_second) -> None: ...
    @typing.overload
    def reset(self, measurement: wpilib.controller._controller.trajectory.TrapezoidProfile.State) -> None: ...
    def setConstraints(self, constraints: wpilib.controller._controller.trajectory.TrapezoidProfile.Constraints) -> None: 
        """
        Set velocity and acceleration constraints for goal.

        :param constraints: Velocity and acceleration constraints for goal.
        """
    def setD(self, Kd: float) -> None: 
        """
        Sets the differential coefficient of the PID controller gain.

        :param Kd: differential coefficient
        """
    @typing.overload
    def setGoal(self, goal: float) -> None: 
        """
        Sets the goal for the ProfiledPIDController.

        :param goal: The desired unprofiled setpoint.

        Sets the goal for the ProfiledPIDController.

        :param goal: The desired unprofiled setpoint.
        """
    @typing.overload
    def setGoal(self, goal: wpilib.controller._controller.trajectory.TrapezoidProfile.State) -> None: ...
    def setI(self, Ki: float) -> None: 
        """
        Sets the integral coefficient of the PID controller gain.

        :param Ki: integral coefficient
        """
    def setIntegratorRange(self, minimumIntegral: float, maximumIntegral: float) -> None: 
        """
        Sets the minimum and maximum values for the integrator.

        When the cap is reached, the integrator value is added to the controller
        output rather than the integrator value times the integral gain.

        :param minimumIntegral: The minimum value of the integrator.

        :param maximumIntegral: The maximum value of the integrator.
        """
    def setP(self, Kp: float) -> None: 
        """
        Sets the proportional coefficient of the PID controller gain.

        :param Kp: proportional coefficient
        """
    def setPID(self, Kp: float, Ki: float, Kd: float) -> None: 
        """
        Sets the PID Controller gain parameters.

        Sets the proportional, integral, and differential coefficients.

        :param Kp: Proportional coefficient

        :param Ki: Integral coefficient

        :param Kd: Differential coefficient
        """
    def setTolerance(self, positionTolerance: float, velocityTolerance: units_per_second = inf) -> None: 
        """
        Sets the error which is considered tolerable for use with
        AtSetpoint().

        :param positionTolerance: Position error which is tolerable.

        :param velocityTolerance: Velocity error which is tolerable.
        """
    pass
class RamseteController():
    """
    Ramsete is a nonlinear time-varying feedback controller for unicycle models
    that drives the model to a desired pose along a two-dimensional trajectory.
    Why would we need a nonlinear control law in addition to the linear ones we
    have used so far like PID? If we use the original approach with PID
    controllers for left and right position and velocity states, the controllers
    only deal with the local pose. If the robot deviates from the path, there is
    no way for the controllers to correct and the robot may not reach the desired
    global pose. This is due to multiple endpoints existing for the robot which
    have the same encoder path arc lengths.

    Instead of using wheel path arc lengths (which are in the robot's local
    coordinate frame), nonlinear controllers like pure pursuit and Ramsete use
    global pose. The controller uses this extra information to guide a linear
    reference tracker like the PID controllers back in by adjusting the
    references of the PID controllers.

    The paper "Control of Wheeled Mobile Robots: An Experimental Overview"
    describes a nonlinear controller for a wheeled vehicle with unicycle-like
    kinematics; a global pose consisting of x, y, and theta; and a desired pose
    consisting of x_d, y_d, and theta_d. We call it Ramsete because that's the
    acronym for the title of the book it came from in Italian ("Robotica
    Articolata e Mobile per i SErvizi e le TEcnologie").

    See <https://file.tavsys.net/control/controls-engineering-in-frc.pdf> section
    on Ramsete unicycle controller for a derivation and analysis.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Construct a Ramsete unicycle controller.

        :param b: Tuning parameter (b > 0) for which larger values make
            convergence more aggressive like a proportional term.

        :param zeta: Tuning parameter (0 < zeta < 1) for which larger values provide
            more damping in response.

        Construct a Ramsete unicycle controller. The default arguments for
        b and zeta of 2.0 and 0.7 have been well-tested to produce desireable
        results.
        """
    @typing.overload
    def __init__(self, b: float, zeta: float) -> None: ...
    def atReference(self) -> bool: 
        """
        Returns true if the pose error is within tolerance of the reference.
        """
    @typing.overload
    def calculate(self, currentPose: wpilib.geometry._geometry.Pose2d, desiredState: wpilib.controller._controller.trajectory.Trajectory.State) -> wpilib.kinematics._kinematics.ChassisSpeeds: 
        """
        Returns the next output of the Ramsete controller.

        The reference pose, linear velocity, and angular velocity should come from
        a drivetrain trajectory.

        :param currentPose: The current pose.

        :param poseRef:   The desired pose.

        :param linearVelocityRef: The desired linear velocity.

        :param angularVelocityRef: The desired angular velocity.

        Returns the next output of the Ramsete controller.

        The reference pose, linear velocity, and angular velocity should come from
        a drivetrain trajectory.

        :param currentPose: The current pose.

        :param desiredState: The desired pose, linear velocity, and angular velocity
                    from a trajectory.
        """
    @typing.overload
    def calculate(self, currentPose: wpilib.geometry._geometry.Pose2d, poseRef: wpilib.geometry._geometry.Pose2d, linearVelocityRef: meters_per_second, angularVelocityRef: radians_per_second) -> wpilib.kinematics._kinematics.ChassisSpeeds: ...
    def setEnabled(self, enabled: bool) -> None: 
        """
        Enables and disables the controller for troubleshooting purposes.

        :param enabled: If the controller is enabled or not.
        """
    def setTolerance(self, poseTolerance: wpilib.geometry._geometry.Pose2d) -> None: 
        """
        Sets the pose error which is considered tolerable for use with
        AtReference().

        :param poseTolerance: Pose error which is tolerable.
        """
    pass
class SimpleMotorFeedforward():
    """
    A helper class that computes feedforward voltages for a simple
    permanent-magnet DC motor.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new SimpleMotorFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kV: The velocity gain, in volt seconds per distance.

        :param kA: The acceleration gain, in volt seconds^2 per distance.
        """
    @typing.overload
    def __init__(self, kS: volts, kV: volt_seconds, kA: volt_seconds_squared = 0.0) -> None: ...
    def calculate(self, velocity: units_per_second, acceleration: units_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param velocity: The velocity setpoint, in distance per second.

        :param acceleration: The acceleration setpoint, in distance per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, velocity: units_per_second) -> units_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param velocity: The velocity of the motor.

        :returns: The maximum possible acceleration at the given velocity.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, acceleration: units_per_second_squared) -> units_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param acceleration: The acceleration of the motor.

        :returns: The maximum possible velocity at the given acceleration.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, velocity: units_per_second) -> units_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param velocity: The velocity of the motor.

        :returns: The minimum possible acceleration at the given velocity.
        """
    def minAchievableVelocity(self, maxVoltage: volts, acceleration: units_per_second_squared) -> units_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param acceleration: The acceleration of the motor.

        :returns: The minimum possible velocity at the given acceleration.
        """
    @property
    def kA(self) -> volt_seconds_squared:
        """
        :type: volt_seconds_squared
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds:
        """
        :type: volt_seconds
        """
    @kV.setter
    def kV(self, arg0: volt_seconds) -> None:
        pass
    pass
class SimpleMotorFeedforwardFeet():
    """
    A helper class that computes feedforward voltages for a simple
    permanent-magnet DC motor.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new SimpleMotorFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kV: The velocity gain, in volt seconds per distance.

        :param kA: The acceleration gain, in volt seconds^2 per distance.
        """
    @typing.overload
    def __init__(self, kS: volts, kV: volt_seconds_per_feet, kA: volt_seconds_squared_per_feet = 0.0) -> None: ...
    def calculate(self, velocity: feet_per_second, acceleration: feet_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param velocity: The velocity setpoint, in distance per second.

        :param acceleration: The acceleration setpoint, in distance per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, velocity: feet_per_second) -> feet_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param velocity: The velocity of the motor.

        :returns: The maximum possible acceleration at the given velocity.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, acceleration: feet_per_second_squared) -> feet_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param acceleration: The acceleration of the motor.

        :returns: The maximum possible velocity at the given acceleration.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, velocity: feet_per_second) -> feet_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param velocity: The velocity of the motor.

        :returns: The minimum possible acceleration at the given velocity.
        """
    def minAchievableVelocity(self, maxVoltage: volts, acceleration: feet_per_second_squared) -> feet_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param acceleration: The acceleration of the motor.

        :returns: The minimum possible velocity at the given acceleration.
        """
    @property
    def kA(self) -> volt_seconds_squared_per_feet:
        """
        :type: volt_seconds_squared_per_feet
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared_per_feet) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds_per_feet:
        """
        :type: volt_seconds_per_feet
        """
    @kV.setter
    def kV(self, arg0: volt_seconds_per_feet) -> None:
        pass
    pass
class SimpleMotorFeedforwardMeters():
    """
    A helper class that computes feedforward voltages for a simple
    permanent-magnet DC motor.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new SimpleMotorFeedforward with the specified gains.

        :param kS: The static gain, in volts.

        :param kV: The velocity gain, in volt seconds per distance.

        :param kA: The acceleration gain, in volt seconds^2 per distance.
        """
    @typing.overload
    def __init__(self, kS: volts, kV: volt_seconds_per_meter, kA: volt_seconds_squared_per_meter = 0.0) -> None: ...
    def calculate(self, velocity: meters_per_second, acceleration: meters_per_second_squared = 0.0) -> volts: 
        """
        Calculates the feedforward from the gains and setpoints.

        :param velocity: The velocity setpoint, in distance per second.

        :param acceleration: The acceleration setpoint, in distance per second^2.

        :returns: The computed feedforward, in volts.
        """
    def maxAchievableAcceleration(self, maxVoltage: volts, velocity: meters_per_second) -> meters_per_second_squared: 
        """
        Calculates the maximum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param velocity: The velocity of the motor.

        :returns: The maximum possible acceleration at the given velocity.
        """
    def maxAchievableVelocity(self, maxVoltage: volts, acceleration: meters_per_second_squared) -> meters_per_second: 
        """
        Calculates the maximum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param acceleration: The acceleration of the motor.

        :returns: The maximum possible velocity at the given acceleration.
        """
    def minAchievableAcceleration(self, maxVoltage: volts, velocity: meters_per_second) -> meters_per_second_squared: 
        """
        Calculates the minimum achievable acceleration given a maximum voltage
        supply and a velocity. Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the velocity constraint, and this will give you
        a simultaneously-achievable acceleration constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param velocity: The velocity of the motor.

        :returns: The minimum possible acceleration at the given velocity.
        """
    def minAchievableVelocity(self, maxVoltage: volts, acceleration: meters_per_second_squared) -> meters_per_second: 
        """
        Calculates the minimum achievable velocity given a maximum voltage supply
        and an acceleration.  Useful for ensuring that velocity and
        acceleration constraints for a trapezoidal profile are simultaneously
        achievable - enter the acceleration constraint, and this will give you
        a simultaneously-achievable velocity constraint.

        :param maxVoltage: The maximum voltage that can be supplied to the motor.

        :param acceleration: The acceleration of the motor.

        :returns: The minimum possible velocity at the given acceleration.
        """
    @property
    def kA(self) -> volt_seconds_squared_per_meter:
        """
        :type: volt_seconds_squared_per_meter
        """
    @kA.setter
    def kA(self, arg0: volt_seconds_squared_per_meter) -> None:
        pass
    @property
    def kS(self) -> volts:
        """
        :type: volts
        """
    @kS.setter
    def kS(self, arg0: volts) -> None:
        pass
    @property
    def kV(self) -> volt_seconds_per_meter:
        """
        :type: volt_seconds_per_meter
        """
    @kV.setter
    def kV(self, arg0: volt_seconds_per_meter) -> None:
        pass
    pass
