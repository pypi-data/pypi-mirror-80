import wpilib.command._commands_v1
import typing
import CommandGroupEntry
import _pyntcore._ntcore
import wpilib._wpilib
import wpilib.interfaces._interfaces

__all__ = [
    "Button",
    "ButtonScheduler",
    "CancelButtonScheduler",
    "Command",
    "CommandGroup",
    "CommandGroupEntry",
    "ConditionalCommand",
    "HeldButtonScheduler",
    "InstantCommand",
    "InternalButton",
    "JoystickButton",
    "NetworkButton",
    "PIDCommand",
    "PIDSubsystem",
    "POVButton",
    "PressedButtonScheduler",
    "PrintCommand",
    "ReleasedButtonScheduler",
    "Scheduler",
    "StartCommand",
    "Subsystem",
    "TimedCommand",
    "ToggleButtonScheduler",
    "Trigger",
    "WaitCommand",
    "WaitForChildren",
    "WaitUntilCommand"
]


class Trigger(wpilib._wpilib.Sendable):
    """
    This class provides an easy way to link commands to inputs.

    It is very easy to link a polled input to a command. For instance, you could
    link the trigger button of a joystick to a "score" command or an encoder
    reaching a particular value.

    It is encouraged that teams write a subclass of Trigger if they want to have
    something unusual (for instance, if they want to react to the user holding
    a button while the robot is reading a certain sensor input). For this, they
    only have to write the :meth:`.Trigger.Get` method to get the full
    functionality of the Trigger class.
    """
    def __init__(self) -> None: ...
    def cancelWhenActive(self, command: Command) -> None: ...
    def get(self) -> bool: ...
    def grab(self) -> bool: ...
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def toggleWhenActive(self, command: Command) -> None: ...
    def whenActive(self, command: Command) -> None: ...
    def whenInactive(self, command: Command) -> None: ...
    def whileActive(self, command: Command) -> None: ...
    pass
class ButtonScheduler():
    def __init__(self, last: bool, button: Trigger, orders: Command) -> None: ...
    def execute(self) -> None: ...
    def start(self) -> None: ...
    @property
    def _m_button(self) -> Trigger:
        """
        :type: Trigger
        """
    @property
    def _m_command(self) -> Command:
        """
        :type: Command
        """
    @property
    def _m_pressedLast(self) -> bool:
        """
        :type: bool
        """
    @_m_pressedLast.setter
    def _m_pressedLast(self, arg0: bool) -> None:
        pass
    pass
class CancelButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: Command) -> None: ...
    def execute(self) -> None: ...
    pass
class Command(wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    """
    The Command class is at the very core of the entire command framework.

    Every command can be started with a call to Start(). Once a command is
    started it will call Initialize(), and then will repeatedly call Execute()
    until the IsFinished() returns true. Once it does,End() will be called.

    However, if at any point while it is running Cancel() is called, then the
    command will be stopped and Interrupted() will be called.

    If a command uses a Subsystem, then it should specify that it does so by
    calling the Requires() method in its constructor. Note that a Command may
    have multiple requirements, and Requires() should be called for each one.

    If a command is running and a new command with shared requirements is
    started, then one of two things will happen. If the active command is
    interruptible, then Cancel() will be called and the command will be removed
    to make way for the new one. If the active command is not interruptible, the
    other one will not even be started, and the active one will continue
    functioning.

    @see CommandGroup
    @see Subsystem
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new command.

        The name of this command will be default.

        Creates a new command with the given name and no timeout.

        :param name: the name for this command

        Creates a new command with the given timeout and a default name.

        :param timeout: the time (in seconds) before this command "times out"
               @see IsTimedOut()

        Creates a new command with the given timeout and a default name.

        :param subsystem: the subsystem that the command requires

        Creates a new command with the given name and timeout.

        :param name: the name of the command

        :param timeout: the time (in seconds) before this command "times out"
               @see IsTimedOut()

        Creates a new command with the given name and timeout.

        :param name: the name of the command

        :param subsystem: the subsystem that the command requires

        Creates a new command with the given name and timeout.

        :param timeout: the time (in seconds) before this command "times out"

        :param subsystem: the subsystem that the command requires @see IsTimedOut()

        Creates a new command with the given name and timeout.

        :param name: the name of the command

        :param timeout: the time (in seconds) before this command "times out"

        :param subsystem: the subsystem that the command requires @see IsTimedOut()
        """
    @typing.overload
    def __init__(self, name: str) -> None: ...
    @typing.overload
    def __init__(self, name: str, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, timeout: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, timeout: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, timeout: float) -> None: ...
    @typing.overload
    def __init__(self, timeout: float, subsystem: Subsystem) -> None: ...
    def _cancel(self) -> None: 
        """
        This works like Cancel(), except that it doesn't throw an exception if it
        is a part of a command group.

        Should only be called by the parent command group.
        """
    def _end(self) -> None: ...
    def _execute(self) -> None: ...
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    def assertUnlocked(self, message: str) -> bool: 
        """
        If changes are locked, then this will generate a CommandIllegalUse error.

        :param message: The message to report on error (it is appended by a default
               message)

        :returns: True if assert passed, false if assert failed.
        """
    def cancel(self) -> None: 
        """
        This will cancel the current command.

        This will cancel the current command eventually. It can be called multiple
        times. And it can be called when the command is not running. If the command
        is running though, then the command will be marked as canceled and
        eventually removed.

        A command can not be canceled if it is a part of a command group, you must
        cancel the command group instead.
        """
    def clearRequirements(self) -> None: 
        """
        Clears list of subsystem requirements.

        This is only used by ConditionalCommand so cancelling the chosen command
        works properly in CommandGroup.
        """
    def doesRequire(self, subsystem: Subsystem) -> bool: 
        """
        Checks if the command requires the given Subsystem.

        :param system: the system

        :returns: whether or not the subsystem is required (false if given nullptr)
        """
    def end(self) -> None: 
        """
        Called when the command ended peacefully.

        This is where you may want to wrap up loose ends, like shutting off a motor
        that was being used in the command.
        """
    def execute(self) -> None: 
        """
        The execute method is called repeatedly until this Command either finishes
        or is canceled.
        """
    def getGroup(self) -> CommandGroup: 
        """
        Returns the CommandGroup that this command is a part of.

        Will return null if this Command is not in a group.

        :returns: The CommandGroup that this command is a part of (or null if not in
                  group)
        """
    def getID(self) -> int: 
        """
        Get the ID (sequence number) for this command.

        The ID is a unique sequence number that is incremented for each command.

        :returns: The ID of this command
        """
    def getName(self) -> str: 
        """
        Gets the name of this Command.

        :returns: Name
        """
    def getRequirements(self) -> set: 
        """
        Returns the requirements (as an std::set of Subsystem pointers) of this
        command.

        :returns: The requirements (as an std::set of Subsystem pointers) of this
                  command
        """
    def getSubsystem(self) -> str: 
        """
        Gets the subsystem name of this Command.

        :returns: Subsystem name
        """
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def initialize(self) -> None: 
        """
        The initialize method is called the first time this Command is run after
        being started.
        """
    def interrupted(self) -> None: 
        """
        Called when the command ends because somebody called Cancel() or another
        command shared the same requirements as this one, and booted it out.

        This is where you may want to wrap up loose ends, like shutting off a motor
        that was being used in the command.

        Generally, it is useful to simply call the End() method within this method,
        as done here.
        """
    def isCanceled(self) -> bool: 
        """
        Returns whether or not this has been canceled.

        :returns: whether or not this has been canceled
        """
    def isCompleted(self) -> bool: 
        """
        Returns whether or not the command has completed running.

        :returns: whether or not the command has completed running.
        """
    def isFinished(self) -> bool: 
        """
        Returns whether this command is finished.

        If it is, then the command will be removed and End() will be called.

        It may be useful for a team to reference the IsTimedOut() method for
        time-sensitive commands.

        Returning false will result in the command never ending automatically.
        It may still be cancelled manually or interrupted by another command.
        Returning true will result in the command executing once and finishing
        immediately. We recommend using InstantCommand for this.

        :returns: Whether this command is finished.
                  @see IsTimedOut()
        """
    def isInitialized(self) -> bool: 
        """
        Returns whether or not the command has been initialized.

        :returns: whether or not the command has been initialized.
        """
    def isInterruptible(self) -> bool: 
        """
        Returns whether or not this command can be interrupted.

        :returns: whether or not this command can be interrupted
        """
    def isParented(self) -> bool: 
        """
        Returns whether the command has a parent.

        :param True: if the command has a parent.
        """
    def isRunning(self) -> bool: 
        """
        Returns whether or not the command is running.

        This may return true even if the command has just been canceled, as it may
        not have yet called Interrupted().

        :returns: whether or not the command is running
        """
    def isTimedOut(self) -> bool: 
        """
        Returns whether or not the TimeSinceInitialized() method returns a number
        which is greater than or equal to the timeout for the command.

        If there is no timeout, this will always return false.

        :returns: whether the time has expired
        """
    def requires(self, s: Subsystem) -> None: 
        """
        This method specifies that the given Subsystem is used by this command.

        This method is crucial to the functioning of the Command System in general.

        Note that the recommended way to call this method is in the constructor.

        :param subsystem: The Subsystem required
                 @see Subsystem
        """
    def run(self) -> bool: 
        """
        The run method is used internally to actually run the commands.

        :returns: Whether or not the command should stay within the Scheduler.
        """
    def setInterruptible(self, interruptible: bool) -> None: 
        """
        Sets whether or not this command can be interrupted.

        :param interruptible: whether or not this command can be interrupted
        """
    def setName(self, name: str) -> None: 
        """
        Sets the name of this Command.

        :param name: name
        """
    def setParent(self, parent: CommandGroup) -> None: 
        """
        Sets the parent of this command. No actual change is made to the group.

        :param parent: the parent
        """
    def setRunWhenDisabled(self, run: bool) -> None: 
        """
        Sets whether or not this Command should run when the robot is disabled.

        By default a command will not run when the robot is disabled, and will in
        fact be canceled.

        :param run: Whether this command should run when the robot is disabled.
        """
    def setSubsystem(self, subsystem: str) -> None: 
        """
        Sets the subsystem name of this Command.

        :param subsystem: subsystem name
        """
    def setTimeout(self, timeout: float) -> None: 
        """
        Sets the timeout of this command.

        :param timeout: the timeout (in seconds)
               @see IsTimedOut()
        """
    def start(self) -> None: 
        """
        Starts up the command. Gets the command ready to start.

        Note that the command will eventually start, however it will not
        necessarily do so immediately, and may in fact be canceled before
        initialize is even called.
        """
    def timeSinceInitialized(self) -> float: 
        """
        Returns the time since this command was initialized (in seconds).

        This function will work even if there is no specified timeout.

        :returns: the time since this command was initialized (in seconds).
        """
    def willRunWhenDisabled(self) -> bool: 
        """
        Returns whether or not this Command will run when the robot is disabled, or
        if it will cancel itself.

        :returns: Whether this Command will run when the robot is disabled, or if it
                  will cancel itself.
        """
    pass
class CommandGroup(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    """
    A CommandGroup is a list of commands which are executed in sequence.

    Commands in a CommandGroup are added using the AddSequential() method and are
    called sequentially. CommandGroups are themselves Commands and can be given
    to other CommandGroups.

    CommandGroups will carry all of the requirements of their Command
    subcommands. Additional requirements can be specified by calling Requires()
    normally in the constructor.

    CommandGroups can also execute commands in parallel, simply by adding them
    using AddParallel().

    @see Command
    @see Subsystem
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new CommandGroup with the given name.

        :param name: The name for this command group
        """
    @typing.overload
    def __init__(self, name: str) -> None: ...
    def _end(self) -> None: ...
    def _execute(self) -> None: ...
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    @typing.overload
    def addParallel(self, command: Command) -> None: 
        """
        Adds a new child Command to the group. The Command will be started after
        all the previously added Commands.

        Instead of waiting for the child to finish, a CommandGroup will have it run
        at the same time as the subsequent Commands. The child will run until
        either it finishes, a new child with conflicting requirements is started,
        or the main sequence runs a Command with conflicting requirements. In the
        latter two cases, the child will be canceled even if it says it can't be
        interrupted.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The command to be added

        Adds a new child Command to the group with the given timeout. The Command
        will be started after all the previously added Commands.

        Once the Command is started, it will run until it finishes, is interrupted,
        or the time expires, whichever is sooner. Note that the given Command will
        have no knowledge that it is on a timer.

        Instead of waiting for the child to finish, a CommandGroup will have it run
        at the same time as the subsequent Commands. The child will run until
        either it finishes, the timeout expires, a new child with conflicting
        requirements is started, or the main sequence runs a Command with
        conflicting requirements. In the latter two cases, the child will be
        canceled even if it says it can't be interrupted.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The command to be added

        :param timeout: The timeout (in seconds)
        """
    @typing.overload
    def addParallel(self, command: Command, timeout: float) -> None: ...
    @typing.overload
    def addSequential(self, command: Command) -> None: 
        """
        Adds a new Command to the group. The Command will be started after all the
        previously added Commands.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The Command to be added

        Adds a new Command to the group with a given timeout. The Command will be
        started after all the previously added commands.

        Once the Command is started, it will be run until it finishes or the time
        expires, whichever is sooner.  Note that the given Command will have no
        knowledge that it is on a timer.

        Note that any requirements the given Command has will be added to the
        group. For this reason, a Command's requirements can not be changed after
        being added to a group.

        It is recommended that this method be called in the constructor.

        :param command: The Command to be added

        :param timeout: The timeout (in seconds)
        """
    @typing.overload
    def addSequential(self, command: Command, timeout: float) -> None: ...
    def end(self) -> None: 
        """
        Can be overridden by teams.
        """
    def execute(self) -> None: 
        """
        Can be overridden by teams.
        """
    def getSize(self) -> int: ...
    def initialize(self) -> None: 
        """
        Can be overridden by teams.
        """
    def interrupted(self) -> None: 
        """
        Can be overridden by teams.
        """
    def isFinished(self) -> bool: 
        """
        Can be overridden by teams.
        """
    def isInterruptible(self) -> bool: ...
    pass
class CommandGroupEntry():
    class Sequence():
        """
        Members:

          kSequence_InSequence

          kSequence_BranchPeer

          kSequence_BranchChild
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
        __members__: dict # value = {'kSequence_InSequence': Sequence.kSequence_InSequence, 'kSequence_BranchPeer': Sequence.kSequence_BranchPeer, 'kSequence_BranchChild': Sequence.kSequence_BranchChild}
        kSequence_BranchChild: wpilib.command._commands_v1.CommandGroupEntry.Sequence # value = Sequence.kSequence_BranchChild
        kSequence_BranchPeer: wpilib.command._commands_v1.CommandGroupEntry.Sequence # value = Sequence.kSequence_BranchPeer
        kSequence_InSequence: wpilib.command._commands_v1.CommandGroupEntry.Sequence # value = Sequence.kSequence_InSequence
        pass
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, command: Command, state: CommandGroupEntry.Sequence, timeout: float = -1.0) -> None: ...
    def isTimedOut(self) -> bool: ...
    @property
    def m_command(self) -> Command:
        """
        :type: Command
        """
    @property
    def m_state(self) -> CommandGroupEntry.Sequence:
        """
        :type: CommandGroupEntry.Sequence
        """
    @m_state.setter
    def m_state(self, arg0: CommandGroupEntry.Sequence) -> None:
        pass
    @property
    def m_timeout(self) -> float:
        """
        :type: float
        """
    @m_timeout.setter
    def m_timeout(self, arg0: float) -> None:
        pass
    pass
class ConditionalCommand(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    """
    A ConditionalCommand is a Command that starts one of two commands.

    A ConditionalCommand uses the Condition method to determine whether it should
    run onTrue or onFalse.

    A ConditionalCommand adds the proper Command to the Scheduler during
    Initialize() and then IsFinished() will return true once that Command has
    finished executing.

    If no Command is specified for onFalse, the occurrence of that condition
    will be a no-op.

    A ConditionalCommand will require the superset of subsystems of the onTrue
    and onFalse commands.

    @see Command
    @see Scheduler
    """
    @typing.overload
    def __init__(self, name: str, onTrue: Command, onFalse: Command = None) -> None: 
        """
        Creates a new ConditionalCommand with given onTrue and onFalse Commands.

        :param onTrue: The Command to execute if Condition() returns true

        :param onFalse: The Command to execute if Condition() returns false

        Creates a new ConditionalCommand with given onTrue and onFalse Commands.

        :param name: The name for this command group

        :param onTrue: The Command to execute if Condition() returns true

        :param onFalse: The Command to execute if Condition() returns false
        """
    @typing.overload
    def __init__(self, onTrue: Command, onFalse: Command = None) -> None: ...
    def _cancel(self) -> None: ...
    def _condition(self) -> bool: 
        """
        The Condition to test to determine which Command to run.

        :returns: true if m_onTrue should be run or false if m_onFalse should be run.
        """
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class HeldButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: Command) -> None: ...
    def execute(self) -> None: ...
    pass
class InstantCommand(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    """
    This command will execute once, then finish immediately afterward.

    Subclassing InstantCommand is shorthand for returning true from IsFinished().
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Creates a new InstantCommand with the given name.

        :param name: The name for this command

        Creates a new InstantCommand with the given requirement.

        :param subsystem: The subsystem that the command requires

        Creates a new InstantCommand with the given name.

        :param name: The name for this command

        :param subsystem: The subsystem that the command requires

        Create a command that calls the given function when run.

        :param func: The function to run when Initialize() is run.

        Create a command that calls the given function when run.

        :param subsystem: The subsystems that this command runs on.

        :param func: The function to run when Initialize() is run.

        Create a command that calls the given function when run.

        :param name: The name of the command.

        :param func: The function to run when Initialize() is run.

        Create a command that calls the given function when run.

        :param name: The name of the command.

        :param subsystem: The subsystems that this command runs on.

        :param func: The function to run when Initialize() is run.
        """
    @typing.overload
    def __init__(self, func: typing.Callable[[], None]) -> None: ...
    @typing.overload
    def __init__(self, name: str) -> None: ...
    @typing.overload
    def __init__(self, name: str, func: typing.Callable[[], None]) -> None: ...
    @typing.overload
    def __init__(self, name: str, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, subsystem: Subsystem, func: typing.Callable[[], None]) -> None: ...
    @typing.overload
    def __init__(self, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, subsystem: Subsystem, func: typing.Callable[[], None]) -> None: ...
    def _initialize(self) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class Button(Trigger, wpilib._wpilib.Sendable):
    """
    This class provides an easy way to link commands to OI inputs.

    It is very easy to link a button to a command.  For instance, you could link
    the trigger button of a joystick to a "score" command.

    This class represents a subclass of Trigger that is specifically aimed at
    buttons on an operator interface as a common use case of the more generalized
    Trigger objects. This is a simple wrapper around Trigger with the method
    names renamed to fit the Button object use.
    """
    def __init__(self) -> None: ...
    def cancelWhenPressed(self, command: Command) -> None: 
        """
        Cancels the specificed command when the button is pressed.

        :param command: The command to be canceled
        """
    def toggleWhenPressed(self, command: Command) -> None: 
        """
        Toggle the specified command when the button is pressed.

        :param command: The command to be toggled
        """
    def whenPressed(self, command: Command) -> None: 
        """
        Specifies the command to run when a button is first pressed.

        :param command: The pointer to the command to run
        """
    def whenReleased(self, command: Command) -> None: 
        """
        Specifies the command to run when the button is released.

        The command will be scheduled a single time.

        :param command: The pointer to the command to run
        """
    def whileHeld(self, command: Command) -> None: 
        """
        Specifies the command to be scheduled while the button is pressed.

        The command will be scheduled repeatedly while the button is pressed and
        will be canceled when the button is released.

        :param command: The pointer to the command to run
        """
    pass
class JoystickButton(Button, Trigger, wpilib._wpilib.Sendable):
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID, buttonNumber: int) -> None: ...
    def get(self) -> bool: ...
    pass
class NetworkButton(Button, Trigger, wpilib._wpilib.Sendable):
    @typing.overload
    def __init__(self, table: _pyntcore._ntcore.NetworkTable, field: str) -> None: ...
    @typing.overload
    def __init__(self, tableName: str, field: str) -> None: ...
    def get(self) -> bool: ...
    pass
class PIDCommand(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable, wpilib.interfaces._interfaces.PIDOutput, wpilib.interfaces._interfaces.PIDSource):
    def PIDGet(self) -> float: ...
    def PIDWrite(self, output: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, period: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, subsystem: Subsystem) -> None: ...
    def _end(self) -> None: ...
    def _initialize(self) -> None: ...
    def _interrupted(self) -> None: ...
    def getPIDController(self) -> None: ...
    def getPosition(self) -> float: ...
    def getSetpoint(self) -> float: ...
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def returnPIDInput(self) -> float: ...
    def setSetpoint(self, setpoint: float) -> None: ...
    def setSetpointRelative(self, deltaSetpoint: float) -> None: ...
    def usePIDOutput(self, output: float) -> None: ...
    pass
class Subsystem(wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    def __init__(self, name: str) -> None: 
        """
        Creates a subsystem with the given name.

        :param name: the name of the subsystem
        """
    @typing.overload
    def addChild(self, child: wpilib._wpilib.Sendable) -> None: 
        """
        Associate a Sendable with this Subsystem.
        Also update the child's name.

        :param name: name to give child

        :param child: sendable

        Associate a {@link Sendable} with this Subsystem.

        :param child: sendable
        """
    @typing.overload
    def addChild(self, name: str, child: wpilib._wpilib.Sendable) -> None: ...
    def getCurrentCommand(self) -> Command: 
        """
        Returns the command which currently claims this subsystem.

        :returns: the command which currently claims this subsystem
        """
    def getCurrentCommandName(self) -> str: 
        """
        Returns the current command name, or empty string if no current command.

        :returns: the current command name
        """
    def getDefaultCommand(self) -> Command: 
        """
        Returns the default command (or null if there is none).

        :returns: the default command
        """
    def getDefaultCommandName(self) -> str: 
        """
        Returns the default command name, or empty string is there is none.

        :returns: the default command name
        """
    def getName(self) -> str: 
        """
        Gets the name of this Subsystem.

        :returns: Name
        """
    def getSubsystem(self) -> str: 
        """
        Gets the subsystem name of this Subsystem.

        :returns: Subsystem name
        """
    def initDefaultCommand(self) -> None: 
        """
        Initialize the default command for this subsystem.

        This is meant to be the place to call SetDefaultCommand in a subsystem and
        will be called on all the subsystems by the CommandBase method before the
        program starts running by using the list of all registered Subsystems
        inside the Scheduler.

        This should be overridden by a Subsystem that has a default Command
        """
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def periodic(self) -> None: 
        """
        When the run method of the scheduler is called this method will be called.
        """
    def setCurrentCommand(self, command: Command) -> None: 
        """
        Sets the current command.

        :param command: the new current command
        """
    def setDefaultCommand(self, command: Command) -> None: 
        """
        Sets the default command. If this is not called or is called with null,
        then there will be no default command for the subsystem.

        **WARNING:** This should **NOT** be called in a constructor if the
        subsystem is a singleton.

        :param command: the default command (or null if there should be none)
        """
    def setName(self, name: str) -> None: 
        """
        Sets the name of this Subsystem.

        :param name: name
        """
    def setSubsystem(self, subsystem: str) -> None: 
        """
        Sets the subsystem name of this Subsystem.

        :param subsystem: subsystem name
        """
    pass
class POVButton(Button, Trigger, wpilib._wpilib.Sendable):
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID, angle: int, povNumber: int = 0) -> None: 
        """
        Creates a POV button for triggering commands.

        :param joystick: The GenericHID object that has the POV

        :param angle: The desired angle in degrees (e.g. 90, 270)

        :param povNumber: The POV number (@see GenericHID#GetPOV)
        """
    def get(self) -> bool: ...
    pass
class PressedButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: Command) -> None: ...
    def execute(self) -> None: ...
    pass
class PrintCommand(InstantCommand, Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    def __init__(self, message: str) -> None: ...
    def initialize(self) -> None: ...
    pass
class ReleasedButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: Command) -> None: ...
    def execute(self) -> None: ...
    pass
class Scheduler():
    def addButton(self, button: ButtonScheduler) -> None: ...
    def addCommand(self, command: Command) -> None: 
        """
        Add a command to be scheduled later.

        In any pass through the scheduler, all commands are added to the additions
        list, then at the end of the pass, they are all scheduled.

        :param command: The command to be scheduled
        """
    @staticmethod
    def addToSmartDashboard(key: str) -> None: 
        """
        This is equivalent to ``wpilib.SmartDashboard.putData(key, Scheduler.getInstance())``.
        Use this instead, as SmartDashboard.putData will fail if used directly

        :param key: the key
        """
    @staticmethod
    def getInstance() -> Scheduler: 
        """
        Returns the Scheduler, creating it if one does not exist.

        :returns: the Scheduler
        """
    def initSendable(self, builder: wpilib._wpilib.SendableBuilder) -> None: ...
    def registerSubsystem(self, subsystem: Subsystem) -> None: 
        """
        Registers a Subsystem to this Scheduler, so that the Scheduler might know
        if a default Command needs to be run.

        All Subsystems should call this.

        :param system: the system
        """
    def remove(self, command: Command) -> None: 
        """
        Removes the Command from the Scheduler.

        :param command: the command to remove
        """
    def removeAll(self) -> None: ...
    def resetAll(self) -> None: 
        """
        Completely resets the scheduler. Undefined behavior if running.
        """
    def run(self) -> None: 
        """
        Runs a single iteration of the loop.

        This method should be called often in order to have a functioning
        Command system. The loop has five stages:

        <ol>
        - Poll the Buttons
        - Execute/Remove the Commands
        - Send values to SmartDashboard
        - Add Commands
        - Add Defaults
        </ol>
        """
    def setEnabled(self, enabled: bool) -> None: ...
    pass
class StartCommand(InstantCommand, Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    def __init__(self, commandToStart: Command) -> None: ...
    def initialize(self) -> None: ...
    pass
class PIDSubsystem(Subsystem, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable, wpilib.interfaces._interfaces.PIDOutput, wpilib.interfaces._interfaces.PIDSource):
    """
    This class is designed to handle the case where there is a Subsystem which
    uses a single PIDController almost constantly (for instance, an elevator
    which attempts to stay at a constant height).

    It provides some convenience methods to run an internal PIDController. It
    also allows access to the internal PIDController in order to give total
    control to the programmer.
    """
    def PIDGet(self) -> float: ...
    def PIDWrite(self, output: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float) -> None: 
        """
        Instantiates a PIDSubsystem that will use the given P, I, and D values.

        :param name: the name

        :param p: the proportional value

        :param i: the integral value

        :param d: the derivative value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        :param name: the name

        :param p: the proportional value

        :param i: the integral value

        :param d: the derivative value

        :param f: the feedforward value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        It will also space the time between PID loop calculations to be equal to
        the given period.

        :param name: the name

        :param p: the proportional value

        :param i: the integral value

        :param d: the derivative value

        :param f: the feedfoward value

        :param period: the time (in seconds) between calculations

        Instantiates a PIDSubsystem that will use the given P, I, and D values.

        It will use the class name as its name.

        :param p: the proportional value

        :param i: the integral value

        :param d: the derivative value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        It will use the class name as its name.

        :param p: the proportional value

        :param i: the integral value

        :param d: the derivative value

        :param f: the feedforward value

        Instantiates a PIDSubsystem that will use the given P, I, D, and F values.

        It will use the class name as its name. It will also space the time
        between PID loop calculations to be equal to the given period.

        :param p: the proportional value

        :param i: the integral value

        :param d: the derivative value

        :param f: the feedforward value

        :param period: the time (in seconds) between calculations
        """
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float) -> None: ...
    @typing.overload
    def __init__(self, name: str, p: float, i: float, d: float, f: float, period: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float) -> None: ...
    @typing.overload
    def __init__(self, p: float, i: float, d: float, f: float, period: float) -> None: ...
    def disable(self) -> None: 
        """
        Disables the internal PIDController.
        """
    def enable(self) -> None: 
        """
        Enables the internal PIDController.
        """
    def getPIDController(self) -> None: 
        """
        Returns the PIDController used by this PIDSubsystem.

        Use this if you would like to fine tune the PID loop.

        :returns: The PIDController used by this PIDSubsystem
        """
    def getPosition(self) -> float: 
        """
        Returns the current position.

        :returns: the current position
        """
    def getRate(self) -> float: 
        """
        Returns the current rate.

        :returns: the current rate
        """
    def getSetpoint(self) -> float: 
        """
        Return the current setpoint.

        :returns: The current setpoint
        """
    def onTarget(self) -> bool: 
        """
        Return true if the error is within the percentage of the total input range,
        determined by SetTolerance().

        This asssumes that the maximum and minimum input were set using SetInput().
        Use OnTarget() in the IsFinished() method of commands that use this
        subsystem.

        Currently this just reports on target as the actual value passes through
        the setpoint. Ideally it should be based on being within the tolerance for
        some period of time.

        :returns: True if the error is within the percentage tolerance of the input
                  range
        """
    def returnPIDInput(self) -> float: ...
    def setAbsoluteTolerance(self, absValue: float) -> None: 
        """
        Set the absolute error which is considered tolerable for use with
        OnTarget.

        :param absValue: absolute error which is tolerable
        """
    def setInputRange(self, minimumInput: float, maximumInput: float) -> None: 
        """
        Sets the maximum and minimum values expected from the input.

        :param minimumInput: the minimum value expected from the input

        :param maximumInput: the maximum value expected from the output
        """
    def setOutputRange(self, minimumOutput: float, maximumOutput: float) -> None: 
        """
        Sets the maximum and minimum values to write.

        :param minimumOutput: the minimum value to write to the output

        :param maximumOutput: the maximum value to write to the output
        """
    def setPercentTolerance(self, percent: float) -> None: 
        """
        Set the percentage error which is considered tolerable for use with
        OnTarget().

        :param percent: percentage error which is tolerable
        """
    def setSetpoint(self, setpoint: float) -> None: 
        """
        Sets the setpoint to the given value.

        If SetRange() was called, then the given setpoint will be trimmed to fit
        within the range.

        :param setpoint: the new setpoint
        """
    def setSetpointRelative(self, deltaSetpoint: float) -> None: 
        """
        Adds the given value to the setpoint.

        If SetRange() was used, then the bounds will still be honored by this
        method.

        :param deltaSetpoint: the change in the setpoint
        """
    def usePIDOutput(self, output: float) -> None: ...
    pass
class TimedCommand(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    """
    A TimedCommand will wait for a timeout before finishing.

    TimedCommand is used to execute a command for a given amount of time.
    """
    @typing.overload
    def __init__(self, name: str, timeout: float) -> None: 
        """
        Creates a new TimedCommand with the given name and timeout.

        :param name: the name of the command

        :param timeout: the time (in seconds) before this command "times out"

        Creates a new WaitCommand with the given timeout.

        :param timeout: the time (in seconds) before this command "times out"

        Creates a new TimedCommand with the given name and timeout.

        :param name: the name of the command

        :param timeout: the time (in seconds) before this command "times out"

        :param subsystem: the subsystem that the command requires

        Creates a new WaitCommand with the given timeout.

        :param timeout: the time (in seconds) before this command "times out"

        :param subsystem: the subsystem that the command requires
        """
    @typing.overload
    def __init__(self, name: str, timeout: float, subsystem: Subsystem) -> None: ...
    @typing.overload
    def __init__(self, timeout: float) -> None: ...
    @typing.overload
    def __init__(self, timeout: float, subsystem: Subsystem) -> None: ...
    def isFinished(self) -> bool: 
        """
        Ends command when timed out.
        """
    pass
class ToggleButtonScheduler(ButtonScheduler):
    def __init__(self, last: bool, button: Trigger, orders: Command) -> None: ...
    def execute(self) -> None: ...
    pass
class InternalButton(Button, Trigger, wpilib._wpilib.Sendable):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, inverted: bool) -> None: ...
    def get(self) -> bool: ...
    def setInverted(self, inverted: bool) -> None: ...
    def setPressed(self, pressed: bool) -> None: ...
    pass
class WaitCommand(TimedCommand, Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    @typing.overload
    def __init__(self, name: str, timeout: float) -> None: 
        """
        Creates a new WaitCommand with the given name and timeout.

        :param name: the name of the command

        :param timeout: the time (in seconds) before this command "times out"

        Creates a new WaitCommand with the given timeout.

        :param timeout: the time (in seconds) before this command "times out"
        """
    @typing.overload
    def __init__(self, timeout: float) -> None: ...
    pass
class WaitForChildren(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    @typing.overload
    def __init__(self, name: str, timeout: float) -> None: ...
    @typing.overload
    def __init__(self, timeout: float) -> None: ...
    def isFinished(self) -> bool: ...
    pass
class WaitUntilCommand(Command, wpilib._wpilib.ErrorBase, wpilib._wpilib.Sendable):
    @typing.overload
    def __init__(self, name: str, time: float) -> None: 
        """
        A WaitCommand will wait until a certain match time before finishing.

        This will wait until the game clock reaches some value, then continue to
        the next command.

        @see CommandGroup
        """
    @typing.overload
    def __init__(self, time: float) -> None: ...
    def isFinished(self) -> bool: 
        """
        Check if we've reached the actual finish time.
        """
    pass
