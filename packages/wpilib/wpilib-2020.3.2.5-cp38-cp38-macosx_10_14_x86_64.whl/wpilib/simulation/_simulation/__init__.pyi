import wpilib.simulation._simulation
import typing
import wpilib.geometry._geometry

__all__ = [
    "Field2d"
]


class Field2d():
    """
    2D representation of game field (for simulation).

    In non-simulation mode this simply stores and returns the robot pose.

    The robot pose is the actual location shown on the simulation view.
    This may or may not match the robot's internal odometry.  For example, if
    the robot is shown at a particular starting location, the pose in this
    class would represent the actual location on the field, but the robot's
    internal state might have a 0,0,0 pose (unless it's initialized to
    something different).

    As the user is able to edit the pose, code performing updates should get
    the robot pose, transform it as appropriate (e.g. based on simulated wheel
    velocity), and set the new pose.
    """
    def __init__(self) -> None: ...
    def getRobotPose(self) -> wpilib.geometry._geometry.Pose2d: 
        """
        Get the robot pose.

        :returns: 2D pose
        """
    @typing.overload
    def setRobotPose(self, pose: wpilib.geometry._geometry.Pose2d) -> None: 
        """
        Set the robot pose from a Pose object.

        :param pose: 2D pose

        Set the robot pose from x, y, and rotation.

        :param x: X location

        :param y: Y location

        :param rotation: rotation
        """
    @typing.overload
    def setRobotPose(self, x: meters, y: meters, rotation: wpilib.geometry._geometry.Rotation2d) -> None: ...
    pass
