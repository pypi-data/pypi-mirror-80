import wpilib.controller._controller.constraints
import typing
import TrajectoryConstraint
import wpilib.controller._controller.controller
import wpilib.geometry._geometry
import wpilib.kinematics._kinematics

__all__ = [
    "CentripetalAccelerationConstraint",
    "DifferentialDriveKinematicsConstraint",
    "DifferentialDriveVoltageConstraint",
    "MecanumDriveKinematicsConstraint",
    "SwerveDrive3KinematicsConstraint",
    "SwerveDrive4KinematicsConstraint",
    "SwerveDrive6KinematicsConstraint",
    "TrajectoryConstraint"
]


class TrajectoryConstraint():
    """
    An interface for defining user-defined velocity and acceleration constraints
    while generating trajectories.
    """
    class MinMax():
        """
        Represents a minimum and maximum acceleration.
        """
        def __init__(self) -> None: ...
        @property
        def maxAcceleration(self) -> meters_per_second_squared:
            """
            :type: meters_per_second_squared
            """
        @maxAcceleration.setter
        def maxAcceleration(self, arg0: meters_per_second_squared) -> None:
            pass
        @property
        def minAcceleration(self) -> meters_per_second_squared:
            """
            :type: meters_per_second_squared
            """
        @minAcceleration.setter
        def minAcceleration(self, arg0: meters_per_second_squared) -> None:
            pass
        pass
    def __init__(self) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: 
        """
        Returns the max velocity given the current pose and curvature.

        :param pose: The pose at the current point in the trajectory.

        :param curvature: The curvature at the current point in the trajectory.

        :param velocity: The velocity at the current point in the trajectory before
                 constraints are applied.

        :returns: The absolute maximum velocity.
        """
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: 
        """
        Returns the minimum and maximum allowable acceleration for the trajectory
        given pose, curvature, and speed.

        :param pose: The pose at the current point in the trajectory.

        :param curvature: The curvature at the current point in the trajectory.

        :param speed: The speed at the current point in the trajectory.

        :returns: The min and max acceleration bounds.
        """
    pass
class DifferentialDriveKinematicsConstraint(TrajectoryConstraint):
    def __init__(self, kinematics: wpilib.kinematics._kinematics.DifferentialDriveKinematics, maxSpeed: meters_per_second) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
class DifferentialDriveVoltageConstraint(TrajectoryConstraint):
    """
    A class that enforces constraints on differential drive voltage expenditure
    based on the motor dynamics and the drive kinematics.  Ensures that the
    acceleration of any wheel of the robot while following the trajectory is
    never higher than what can be achieved with the given maximum voltage.
    """
    def __init__(self, feedforward: wpilib.controller._controller.controller.SimpleMotorFeedforwardMeters, kinematics: wpilib.kinematics._kinematics.DifferentialDriveKinematics, maxVoltage: volts) -> None: 
        """
        Creates a new DifferentialDriveVoltageConstraint.

        :param feedforward: A feedforward component describing the behavior of the
                   drive.

        :param kinematics: A kinematics component describing the drive geometry.

        :param maxVoltage: The maximum voltage available to the motors while
                   following the path. Should be somewhat less than the nominal battery
                   voltage (12V) to account for "voltage sag" due to current draw.
        """
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
class MecanumDriveKinematicsConstraint(TrajectoryConstraint):
    def __init__(self, kinematics: wpilib.kinematics._kinematics.MecanumDriveKinematics, maxSpeed: meters_per_second) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
class SwerveDrive3KinematicsConstraint(TrajectoryConstraint):
    def __init__(self, kinematics: wpilib.kinematics._kinematics.SwerveDrive3Kinematics, maxSpeed: meters_per_second) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
class SwerveDrive4KinematicsConstraint(TrajectoryConstraint):
    def __init__(self, kinematics: wpilib.kinematics._kinematics.SwerveDrive4Kinematics, maxSpeed: meters_per_second) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
class SwerveDrive6KinematicsConstraint(TrajectoryConstraint):
    def __init__(self, kinematics: wpilib.kinematics._kinematics.SwerveDrive6Kinematics, maxSpeed: meters_per_second) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
class CentripetalAccelerationConstraint(TrajectoryConstraint):
    """
    A constraint on the maximum absolute centripetal acceleration allowed when
    traversing a trajectory. The centripetal acceleration of a robot is defined
    as the velocity squared divided by the radius of curvature.

    Effectively, limiting the maximum centripetal acceleration will cause the
    robot to slow down around tight turns, making it easier to track trajectories
    with sharp turns.
    """
    def __init__(self, maxCentripetalAcceleration: meters_per_second_squared) -> None: ...
    def maxVelocity(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, velocity: meters_per_second) -> meters_per_second: ...
    def minMaxAcceleration(self, pose: wpilib.geometry._geometry.Pose2d, curvature: radians_per_meter, speed: meters_per_second) -> TrajectoryConstraint.MinMax: ...
    pass
