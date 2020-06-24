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

## Section 1: Nodes

A node is a unique syntactic object, consisting of the following tuple:
1. Name
2. Semantic Type
3. Up Cableset (An array of frames)
4. Docstring

and sometime:

5. Frame

Nodes are typecast to syntactic types. Syntactic types are represented by classes.

![Syntactic Types](https://raw.githubusercontent.com/acampbel-hamilton/Python_SNePS/master/assets/syntactic.svg)

## Section 2: Frames

A frame is a unique object, consisting of the following tuple:
1. Caseframe
2. Filler Set (An ordered list of fillers)

Each Fillers instance must correspond to a slot in the caseframe (i.e. their semantic types must be compatible)
Each molecular node has a single frame.

## Section 3: Fillers

A filler is a non-unique object that contains an array of nodes.

## Section 4: Caseframes

A caseframe is a unique object, consisting of the following tuple:
1. Name
2. Semantic Type
3. Semantic Hierarchy (Of the parent network)
4. Docstring
5. Slots (An ordered list of slots)
6. Aliases (An array of strings also referring to this frame)

## Section 5: Slots

Slots are "relations". A slot is a unique object, consisting of the following tuple:
1. Name
2. Docstring
3. Semantic Type
4. Positive adjustment rule (expand, reduce, or none)
5. Negative adjustment rules (expand, reduce, or none)
6. Minimum number of fillers
7. Maximum number of fillers
8. Path

## Section 6: Semantic Types

Semantic types tell a user the type of ontological entity a node represents (e.g. agent, action).

Because certain slots require certain types of entities, semantic types ensure ontological consistency. For example, a person can perform an action, but a person cannot perform an agent.

![Semantic Types](https://raw.githubusercontent.com/acampbel-hamilton/Python_SNePS/master/assets/semantic.svg)

## Section 7: Paths
