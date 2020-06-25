# Python_SNePS
> SNePS 3 in Python

## Section 0: Preliminary Reading
1. ["A Logic of Arbitrary and Indefinite Objects"](https://www.aaai.org/Papers/KR/2004/KR04-059.pdf) by Stuart Shapiro
    * This will outline the logic of SNePS. While we have transformed the grammar to be more like Python, the general concepts are necessary to understand.

2. ["An Introduction to SNePS 3"](https://cse.buffalo.edu/~shapiro/Papers/sneps3intro.pdf) by Stuart Shapiro
    * This will explain the different semantic and syntactic types as well as the different inference methods (not written yet).

3. ["Visually Interacting with a Knowledge Base Using Frames, Logic, and Propositional Graphs"](https://cse.buffalo.edu/~shapiro/Papers/schsha2011b.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * This paper gives the best working definitions for the various terms used in SNePS3.

4. ["SNePS 3 USER’S MANUAL"](https://cse.buffalo.edu/sneps/Projects/sneps3manual.pdf) by Stuart Shapiro
    * Only use this for understanding the user commands. The pseudo-yacc file is defunct in Python_SNePS.

5. ["Types in SNePS 3"](https://cse.buffalo.edu/~shapiro/Talks/TypesInSneps3.pdf) by Stuart Shapiro
    * Clearly explains the relationship between caseframes and slots (called relations in the paper)

## Section 1: Structure

### Nodes

A node is a unique syntactic object, consisting of the following tuple:
1. Name
2. Semantic Type
3. Up Cableset (An array of frames)
4. Docstring

and sometimes:

5. Frame

Nodes are typecast to syntactic types. Syntactic types are represented by classes.

![Syntactic Types](https://raw.githubusercontent.com/acampbel-hamilton/Python_SNePS/master/assets/syntactic.svg)

MinMaxOpNodes are created by thresh and andor

### Frames

A frame is a unique object, consisting of the following tuple:
1. Caseframe
2. Filler Set (An ordered list of fillers)

Each Fillers instance must correspond to a slot in the caseframe (i.e. their semantic types must be compatible)
Each molecular node has a single frame.

### Fillers

A filler is a non-unique object that contains an array of nodes.

### Caseframes

A caseframe is a unique object, consisting of the following tuple:
1. Name
2. Semantic Type
3. Semantic Hierarchy (Of the parent network)
4. Docstring
5. Slots (An ordered list of slots)
6. Aliases (An array of strings also referring to this frame)

### Slots

Slots are "relations". A slot is a unique object, consisting of the following tuple:
1. Name
2. Docstring
3. Semantic Type
4. Positive adjustment rule (expand, reduce, or none)
5. Negative adjustment rules (expand, reduce, or none)
6. Minimum number of fillers
7. Maximum number of fillers
8. Path

### Semantic Types

Semantic types tell a user the type of ontological entity a node represents (e.g. agent, action).

Because certain slots require certain types of entities, semantic types ensure ontological consistency. For example, a person can perform an action, but a person cannot perform an agent.

![Semantic Types](https://raw.githubusercontent.com/acampbel-hamilton/Python_SNePS/master/assets/semantic.svg)

### Paths

## Section 2: Using Python SNePS

Create a network object:

```python
from psneps import *
net = Network.Network()
```

The following methods are defined:

```python
# Prints out a visual representation of the knowledge base
net.print_graph()

# Passes wft followed by optional parameter asserting
# "hyp" for hypothetical or "true" for true
net.assert_wft("Isa(Dog, Pet)", value="hyp")

# Defines a term with a name, optional semantic type, and docstring
net.("Ben", sem_type_name="Agent", docstring="Ben is a human being.")

# List all terms or find a specific term
net.list_terms()
net.find_term("Ben")

# Defines a semantic type, with a given name, followed by an
# optional array of parent types
net.define_type("Action", ["Thing"])

# List all types
net.list_types()

# Defines a slot corresponding to a type
# Name, followed by semantic type, with optional
# docstring, adjustment rules, min, max, and path
net.define_slot("class", "Category", docstring="Points to a Category that some Entity is a member of.", pos_adj="none", neg_adj="reduce", min=1, max=0, path=None)

# Lists all slots
net.list_slots()

# Defines a new caseframe with a name, semantic type, docstring, and list of slots
define_caseframe(self, name, sem_type_name, docstring="")
```

