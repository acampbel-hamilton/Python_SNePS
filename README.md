# Python_SNePS
> SNePS 3 in Python

This repository contains a partial implementation of the SNePS 3 semantic network in Python. A few test files have been included to demonstrate the system's current capabilities.

##### Implemented:
* SNePS module for building a network

##### Not implemented:
* Some tokens in well-formed-terms (See section 5)
* Uniqueness on variables in ‘donkey sentences’ (See section 1, resource 1)
* Inference package
* Belief revision

We would recommend any persons continuing with this project implement the missing features in the order in which they are listed.

## Section 1: Preliminary Reading

1. [“A Logic of Arbitrary and Indefinite Objects”](https://www.aaai.org/Papers/KR/2004/KR04-059.pdf) by Stuart Shapiro
    * This paper outlines the ideas behind the logical language implemented in SNePS 3. We have revised SNePS's grammar to be more Python-like in syntax, but the general concepts from this paper are very important.

2. [“An Introduction to SNePS 3”](https://cse.buffalo.edu/~shapiro/Papers/sneps3intro.pdf) by Stuart Shapiro
    * This paper explains the different semantic and syntactic types, the function of caseframes, frames, and slots (relations), and the different inference methods.

3. [“Visually Interacting with a Knowledge Base Using Frames, Logic, and Propositional Graphs”](https://cse.buffalo.edu/~shapiro/Papers/schsha2011b.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * This paper gives great working definitions for the various terms used in SNePS 3.

4. [“SNePS 3 User&rsquo;s Manual”](https://cse.buffalo.edu/sneps/Projects/sneps3manual.pdf) by Stuart Shapiro
    * Reference this manual to understand the user commands. The pseudo-yacc rules are defunct in Python_SNePS, but redefined below in Section 5 of the README.

5. [“Types in SNePS 3”](https://cse.buffalo.edu/~shapiro/Talks/TypesInSneps3.pdf) by Stuart Shapiro
    * This paper clearly explains the relationship between caseframes and slots. Note that slots are called “relations” in the paper.

6. [“Concurrent Reasoning in Inference Graphs”](https://cse.buffalo.edu/~shapiro/Papers/schsha13e.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * Explains much of the induction work done in the SNIP package (Note that this is not all complete in CSNePS).

7. [“SUNY at Buffalo CSE563 Lecture Notes”](https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf) by Stuart C. Shapiro
    * Lecture notes from Stuart C. Shapiro’s course on knowledge representation. A long read, but explains many of the logical concepts at play beneath SNePS (e.g. andor, thresh, relations). The most thorough tutorial available.

## Section 2: Structure

### 1: Nodes

A node is a unique syntactic object, consisting of the following:
1. Name
2. Semantic Type
3. Up Cableset (An array of frames)

and sometimes:

4. Frame
5. Min
6. Max
7. Bound

Nodes are typecast to syntactic types, which theoretically correspond to the functions performed by certain grammatical structures (e.g. If x then y), and are, in our system, represented by classes.

![Syntactic Types](/assets/syntactic.svg)

### 2: Frames

A frame is a unique object, consisting of the following tuple:
1. Caseframe
2. Filler Set (An ordered list of Fillers)

Each Fillers instance must correspond to a slot in the caseframe (i.e. their semantic types must be compatible with the slot and their number must fall within the range set by the slot's min and max).

Each molecular node has a *single* frame.

### 3: Fillers

A filler is a non-unique object that contains an array of nodes. Fillers are used by frames to fill slots.

### 4. Caseframes

A caseframe is a unique object, consisting of the following:
1. Name
2. Semantic Type
3. Semantic Hierarchy (Of the parent network)
4. Docstring
5. Slots (An ordered list of slots)
6. Aliases (An array of strings also referring to this frame)

Caseframes, like *Isa*, form Molecular nodes and tell the system something about the nodes which are used (via Frames) to fill their slots.

(In the case of *Isa*, fillers in the first slot must be of type Entity (or a subtype) and are designated as *member*, and fillers in the second slot must be of type *Category* (or a subtype) and are designated as *class*)

### 5: Slots

Slots are “relations.” A slot is a unique object, consisting of the following:
1. Name
2. Docstring
3. Semantic Type
4. Positive adjustment rule (expand, reduce, or none)
5. Negative adjustment rules (expand, reduce, or none)
6. Minimum number of fillers
7. Maximum number of fillers
8. Path

### 6: Semantic Types

Semantic types tell a user the type of ontological entity a node represents (e.g. agent, action).

Because certain slots require certain types of entities, semantic types ensure ontological consistency. For example, a person can perform an action, but a person cannot perform an agent.

![Semantic Types](/assets/semantic.svg)

### 7: Paths

Paths, defined on slots, are items of the class Path. Some paths perform functions on child paths, and others perform functions on multiple children. The user should enter paths into functions as strings using the following syntax:

* ∅ is used to indicate that there should be no space between two tokens  
* \+ is used to indicate that there can be one or more of a given token  
* \* is used to indicate that there can be zero or more of a given token

```yacc
path :       slotname                             // e.g. "member"
     |       slotname ∅ '-'                       // Follows slot backward e.g. "member-"
     |       '!'                                  // Node at this point in interpretation
                                                      // must be asserted in the context
     |       'converse' '(' path ')'              // Follows a given path backward
     |       'kplus' '(' path ')'                 // Follows a path one or more times
     |       'kstar' '(' path ')'                 // Follows a path zero or more times
     |       composed
     |       'or' '(' paths ')'                   // Follows all of the paths and returns the
                                                      // set of nodes that at least one of them reaches
     |       'and' '(' paths ')'                  // Follows all of the paths and returns the
                                                      // set of nodes that every one of them reaches
     |       'irreflexive-restrict' '(' path ')'  // Follows the path such that it doesn't wind up
                                                      // where it began

paths :      'path'
      |      'path' ',' 'paths'

composed :   'composed' '(' paths ')'             // Follows each path followed by the next
         |   '[' paths ']'
```

## Section 3: Using Python_SNePS's Functions

##### Create a network object:

```python
from src import *
net = Network()
```

##### Define term:
Defines a base node with a name and optional semantic type. The default semantic type is Entity.
```python
net.define_term("Ben", sem_type_name="Agent")
```

##### Find term:
Returns the term with the name provided.
```python
net.find_term("Fido")
```

##### List terms:
Prints representations of each node in the network.
```python
net.list_terms()
```

##### Define semantic type:
Defines a semantic type, with a given name, followed by an optional array of parent types.
```python
net.define_type("Idea", ["Thing"])
```

##### List types:
Prints representations of each type in the network.
```python
net.list_types()
```

##### Define slot:
Defines a slot with a name, a semantic type, and optional docstring, adjustment rules, min, max, and path.

Max defaults to None, meaning that there is no upper limit on fillers for a slot.
```python
net.define_slot("contemplates", "Idea",
                docstring="Points to an idea contemplated by an agent.",
                pos_adj="none", neg_adj="reduce", min=1, max=None, path='')
```

##### Find slot:
Returns the slot with the name provided.
```python
net.find_slot("class")
```

##### List slots:
Prints representations of each slot in the network.
```python
net.list_slots()
```

##### Define caseframe:
Defines a new caseframe with a name, a semantic type, list of slots, and optional docstring
```python
net.define_caseframe("Contemplates", "Act", ["agent", "contemplates"],
                     docstring="An agent contemplates some idea.")
```

##### Same frame:
Adds a aliases to an existing frame.
```python
net.same_frame(["Farms", "Grows"], "Cultivates")
```

##### Find caseframe:
Returns the caseframe with the name provided.
```python
net.find_slot("Isa")
```

##### List caseframes:
Prints representations of each caseframe in the network.
```python
net.list_caseframes()
```

##### Define context:
Defines a new context, with a name and optional docstring and parent context (uses the default context by default).
```python
net.define_context("magical_realism", docstring="Used for reading Tokarczuk novels.",
                   parent="literary")
```

##### Set the current context:
Sets the current context to the existing context with the name provided.
```python
net.set_current_context("magical_realism")
```

##### List contexts:
Prints representations of each context in the network.
```python
net.list_contexts()
```

##### Define path:
Tells the inference package that the cable formed by the slot (first parameter) exists between two nodes when the given path (second parameter) can be followed from one to the other.
```python
net.define_path("equiv", "compose(!, equiv, kstar(compose(equiv-, !, equiv)))")
```

##### Follow paths:
Given a starting list of node names and a path (as a string), follows the path from each of the nodes and returns the set of nodes derived
```python
net.paths_from(['Fido', 'Fluffy'], 'kstar(!, member)')
```

##### Assert a well formed term:
Passes wft followed by optional parameter inf used for triggering forward inference
```python
net.assert_wft("Isa(Fido, Dog)", inf=False)
```

##### Display a network:
Displays a visual representation of the current context in the network.
```python
net.display_graph()
```

##### Export a network to DOT:
Outputs a representation of the current context in the network in the Graphviz DOT format to network.dot, or an optional user-provided file name.
```python
net.export_graph(file_name="about_fido")
```

## Section 4: Inference

We have implemented a portion of SNIP, the inference package for SNePS, in the snip directory of this repository.

To do inference, instantiate an object in the Instance class, and call its methods. These methods are documented below:

```python
from src import *

net = Network()

# Makes the inference object
inf = Inference(net)

# Tells the network to print out intermediate knowledge as it goes.
inf.toggle_debug()

# This should be a valid wft string, as described in Section 5.
wft_str = "Isa(Fido, Dog)"

# This asks if one or both of the following is asserted or can be derived:
# 1. The statement represented by wft_str
# 2. The rejection of that statement
inf.ask(wft_str)

# This asks if the statement represented by wft_str is asserted or can be derived:
inf.ask_if(wft_str)

# This asks if the rejection of the statement represented by wft_str is asserted or can be derived:
inf.ask_if_not(wft_str)
```

## Section 5: Using Python_SNePS's Well Formed Terms (wfts)

All wft parsing is handled through ply, a Python module that implements lex and yacc. The following yacc-like reduction rules should give an idea of how a wft is parsed.

* ∅ is used to indicate that there should be no space between two tokens  
* \+ is used to indicate that there can be one or more of a given token  
* \* is used to indicate that there can be zero or more of a given token

```yacc
wft :        atomicName                              // e.g. "Dog"
    |        'wft' ∅ i                               // e.g. "wft1"
    |        identifier '(' argument+ ')'            // A function (e.g. "Has(Dog, Bone)")
    |        BinaryOp '(' argument ',' argument ')'  // e.g. "if(Has(Dog, Bone), Happy(Dog))"
    |        NaryOp '(' wft* ')'                     // e.g. "and(a, b, c)"
    |        Param2Op '{' i ',' j '}' '(' wft+ ')'   // e.g. "thresh{1, 2}(a, b, c, d)"
    |        'thresh' '{' i '}' '(' wft+ ')'         // e.g. "thresh{1}(a, b, c)"
    |        'close' '(' atomicNameSet ',' wft ')'
    |        'every' '(' atomicName ',' argument ')'
    |        'some' '(' atomicName '(' atomicNames ')' ',' argument ')'
    |        '?' ∅ atomicName '(' wft* ')'           // e.g. "?John"


BinaryOp :   i ∅ '=>' | 'v=>' | '=>' | 'if'          // 'v=>' does or-implication and
                                                     // "i ∅ '=>'" does and-implication (e.g. "5=>")

NaryOp :     'and' | 'or' | 'not' | 'nor'            // These operators, exclusively, can take
       |     'thnot' | 'thnor' | 'nand'              // any number of parameters
       |     'xor' | 'iff' | '<=>' | Equiv


Param2Op :   'andor' | 'thresh'


atomicName : identifier | i                          // Identifier matches r'[A-Za-z][A-Za-z0-9_]*'
                                                     // i (Integer) matches r'\d+'

argument :   wft
         |   'None'                                  // Equivalent to an empty set
         |   'setof' '(' wfts* ')'                   // Creates a set of filler nodes for a single slot
         |   '[' wfts* ']'                           // Equivalent to 'setof(wfts*)'
```

## Section 6: Imports

To display visual graphs, Python_SNePS requires extra Python modules. For simple graphs, run:
```bash
pip install networkx matplotlib
```

For draggable graphs, also run:
```bash
pip install netgraph
```

To export graphs as dot files, run:
```bash
pip install pydot
```

## Section 7: Older Versions of Python_SNePS

A previous version of Python_SNePS from the summer of 2019 can be found under the Releases tab on GitHub, and may be useful for reference.
