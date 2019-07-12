# Python_SNePS
This is a partial implementation of SNePS (Semantic Network Processing System) in Python. The system currently has the ability to build and represent a network and has an implementation of path-based inference as defined in the SNePS literature to allow for a limited inference capacity. This ReadMe will contain a brief explanation of the SNePS system as a whole (specifically SNePS 3) as well as a description of of the currently implemented user interface.

##SNePS 3 Description

##UI 'User Manual'

### Notes to the User
The user should know a few things about the code before attempting to run it. First, the UI file is configured to be a script run from the command line. As such, the shebang path may need to be changed when this system is run outside of the Hamilton College Gemini Server. Furthermore, the clear command in the Ui is currently configured to use Linux/Unix system command. This will need to be changed to conform to the appropriate system command should your command line differ. If you plan to modify the system, specifically the UI, you should familiarize yourself with the Cmd module, as this UI heavily utilizes that module.

### ask
The ask command should be written in the following format:
		ask [node]
where [node] signifies a molecular node described using the appropriate syntax.
See build for further description of the appropriate syntax. Note however, that the ask command does no accept any recursive evaluation and is thus limited in the scope of appropriate queries. The ask command should trigger forward and backward inference of all types (Subsumption, Slot-based, Path-based, Natural Deduction), though the current implementation only runs forward path-based inference. Support for all other forms of inference is currently missing from the back end.

### assert
The assert command should be written in the following format:
		assert [node]
where [node] signifies a nested molecular node description as specified in build. This command allows the evaluation of nested UI commands.

### build
The build command should be written in the folowing format:
		build [node]
where [node] is either ([caseframe] [filler] ...) or [base]. [filler] is either a set of nodes ([node] ...) or a singleton node [node]. [base] is a represents an atomic item, i.e. a noun, action, or non-propositional relation.

### clear
This command is called without parameters and clears the screen. This will only work on a linux based command line as far as I am aware. This command may require a rewrite if the system is used on another operating system.

### defContext


### defFrame

### defPath

### defSlot

### describe

### dump

### exit

### find

### list

### shell
