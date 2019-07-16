# Python_SNePS
This is a partial implementation of SNePS (Semantic Network Processing System) in Python. The system currently has the ability to build and represent a network and has an implementation of path-based inference as defined in the SNePS literature to allow for a limited inference capacity. This ReadMe will contain a brief explanation of the SNePS system as a whole (specifically SNePS 3) as well as a description of of the currently implemented user interface. It is recommended that the developers read the following papers before editing the source code for this module:
* [An Introduction to SNePS 3](https://cse.buffalo.edu/~shapiro/Papers/sneps3intro.pdf);
* [A Logic of Arbitrary and Indefinite Objects](https://cse.buffalo.edu/~shapiro/Papers/sha04a.pdf);
* [SNePS: A Logic for Natural Language Understanding and Commonsense Reasoning](https://cse.buffalo.edu/~shapiro/Papers/snepslogic.pdf);
* [Visually Interacting with a Knowledge Base Using Frames, Logic, and Propositional Graphs](https://cse.buffalo.edu/~shapiro/Papers/schsha2011b.pdf);
* [A “Natural Logic'' for Natural Language Processing and Knowledge Representation](https://cse.buffalo.edu/sneps/Bibliography/ali94-01.pdf).

## SNePS 3 Description

### Introduction
SNePS (Semantic Network Processing System) is a knowledge representation and reasoning system. It is designed to model the common sense reasoning used in everyday speech. Specifically, SNePS is designed to account for the difficulties that First Order Predicate Logic (FOPL) and other more prevalent logics have in representing every day statements. SNePS contains an inference system, which allows the system to infer only relevant implied statements for the stored information.

### Knowledge Representation
SNePS is a Propositional Semantic Network, which means that every proposition is represented by a node. These nodes are either atomic or molecular. Atomic nodes are divided into two categories, Base Nodes and Variable Nodes. Base Nodes represent non-propositional terms, like nouns, verbs, or adjectives. Variables represent a particular arbitrary object. Variables are repstricted by their associated restriction set, which contains Molecular nodes. Molecular nodes represent propositions, allowing for statements to be made about base nodes, variable nodes, and other molecular nodes. In this implementation, nodes are instantiations of subclasses of the Term class found in [SyntacticTypes.py](./SyntacticTypes.py). These Syntatic Types are related to each other through a built-in class heirarchy rooted at the Term class.

Molecular nodes are given their meaning through their associated caseframe, which defines how nodes are related to each other through a given Molecular node. Each caseframe is defined by a set of slots and an associated Semantic Type. The Semantic Type of a caseframe is used to group the caseframes based on its general properties (See the class docstrings in [SemanticTypes.py](./SemanticTypes.py) for further detail). Each slot (which used to be called relations) is filled by a set of nodes in the molecular node. The slots allow the system to interpret the meaning of the nodes within the caseframe. For instance, the isa caseframe has the slots member and class. The isa caseframe is interpreted as "[member] is a [class]". Thus a molecular node with the isa caseframe which has the [member] slot filled with "Nate" and the [class] slot filled with "student", would be interpreted as "Nate is a student".

### Knowledge Reasoning
SNePS contains an inference system, which allows for reasoning over the knowledge contained in the system. As of now, only path based inference is currently implemented. Other types of inference in the original SNePS 3 include natural deduction, slot based, and subsumption inference. Path based inference relies upon user defined paths of slots to infer a new molecular node relating the terminal points of the path. (This is a terrible description)

## UI 'User Manual'

### Notes to the User
The user should know a few things about the code before attempting to run it. First, the UI file is configured to be a script run from the command line. As such, the shebang path may need to be changed when this system is run outside of the Hamilton College Gemini Server. Furthermore, the clear command in the Ui is currently configured to use Linux/Unix system command. This will need to be changed to conform to the appropriate system command should your command line differ. If you plan to modify the system, specifically the UI, you should familiarize yourself with the Cmd module, as this UI heavily utilizes that module.

### ask
The ask command should be written in the following format:
		ask [node]
where [node] signifies a molecular node described using the appropriate syntax. See build for further description of the appropriate syntax. Note however, that the ask command does no accept any recursive evaluation and is thus limited in the scope of appropriate queries. The ask command should trigger forward and backward inference of all types (Subsumption, Slot-based, Path-based, Natural Deduction), though the current implementation only runs forward path-based inference. Support for all other forms of inference is currently missing from the back end.

### assert
The assert command should be written in the following format:
		assert [node]
where [node] signifies a nested molecular node description as specified in build. This command allows the evaluation of nested UI commands.

### build
The build command should be written in the following format:
		build [node]
where [node] is either ([caseframe] [filler] ...) or [base]. [filler] is either a set of nodes ([node] ...) or a singleton node [node]. [base] is a represents an atomic item, i.e. a noun, action, or non-propositional relation.

### clear
This command is called without parameters and clears the screen. This will only work on a linux based command line as far as I am aware. This command may require a rewrite if the system is used on another operating system.

### defContext
The defContext command should be written in the following format:
		defContext [name] "docstring" ([parents]) ([hyps])
where [name] is the name of the new context, "docstring" is a short description of it, ([parents]) is a set of names of parent contexts, from which this new context will inherit the hypothesis and derived terms, and ([hyps]) which contains the names of any additional terms to be believed in the new context. This currently does not suppose nested UI commands

### defFrame
The defFrame command should be written in the following format:
		defFrame [name] [semantic type] ([slots]) "docstring"
where [name] is the name of the new caseframe, [semantic type] is the semantic type of the given caseframe, ([slots]) is the set of names of slots contained in the caseframe, and "docstring" is a short description of the new caseframe. The command currently does not evaluate nested UI commands, which should be implemented in the future.

### defPath
The defPath command defines a path for use in path based inference.
		defPath [slot] [path]
[path] has its own internal syntax as described below.

 [slot] : the name of a slot to be traverse in the forward direction
			(filler in the down cableset)
 [slot]- : the name of a slot to be traverse in the backward direction
			(filler in the up cableset)
 kstar : the following expression is to be repeated zero or more times

 kplus : the folowing expression is to be repeated one or more times

 converse : the following path traversed in the backwards direction

 ! : an asserted node must exist here

 or : one of the following path expressions must hold

 and : all of the following path expressions must hold

 not : the following path expression must not hold

 Ex:
 defPath member (member (kstar (equiv- ! equiv)))
 defPath member (or member(member (kstar (equiv- ! equiv))))
 defPath class (or class (class (kstar (subclass- superclass))))
 defPath class (class (kstar (subclass- superclass)))

### defSlot
The defSlot command should be called in the following format:
		defSlot [name] [type] "docstring" [positive adjust] [negative adjust] [min] [max]
where [name] is the name of the new slot, [type] is the semantic type of the new slot, "docstring" is a short description of this new slot, [positive adjust] and [negative adjust] are one of reduce, "expand", or "none", which, together with [min] and [max], specify the behavior of the slot under forward and backward subsumption based inference. Arguments after "docstring" are optional, however, the presence of any argument necessitates the presence of those before it in this list as arguments are positionally evaluated.

### describe
This command takes the name of an object as a parameter and prints a sting representation of that object. This command accepts nested UI commands. Consider updating the string representations of objects as they are currently slightly limited in their descriptive power and may not be particular useful to someone who is not familiar with the underlying implementation.

### dump
This command is called without parameters and prints a representation of the current network at present. This should be rewritten at some point to better align with the behavior of the dump command present in the original implementation of SNePS 3.

### exit
This command closes the PySNePS UI.

### find
The find command should be written in the following format:
		find ([node])
where [node] signifies a non-nested molecular description as described in build. This command should be rewritten to handle a nested molecular description. Find has also not been fully tested and may contain unexpected bugs.

### list
The list command is called with a single parameter denoting a particular type of object in the network. (i.e. term slot, semantic type, context, or caseframe). The command then lists all defined instances of the object in the network. (This is technically incorrect as it only lists all semantic type classes defined in the hierarchy and not every instance of a semantic type)

### shell
This command can be called with a line of python code following it. This code is then passed to the eval function and the result printed. This can be abbreviated with '!'. This is most useful for looking at particular objects ad object attributes while debugging. Consider removing this functionality once the system is complete.
