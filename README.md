# Python_SNePS
> SNePS 3 in Python

## Section 0: Preliminary Reading

1. [&ldquo;A Logic of Arbitrary and Indefinite Objects&rdquo;](https://www.aaai.org/Papers/KR/2004/KR04-059.pdf) by Stuart Shapiro
    * This paper outlines the logic of SNePS. We have transformed SNePS's grammar to be more Pythonic in our project, but the general concepts from this paper are important.

2. [&ldquo;An Introduction to SNePS 3&rdquo;](https://cse.buffalo.edu/~shapiro/Papers/sneps3intro.pdf) by Stuart Shapiro
    * This paper explains the different semantic and syntactic types as well as the different inference methods (not written yet).

3. [&ldquo;Visually Interacting with a Knowledge Base Using Frames, Logic, and Propositional Graphs&rdquo;](https://cse.buffalo.edu/~shapiro/Papers/schsha2011b.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * This paper gives great working definitions for the various terms used in SNePS3.

4. [&ldquo;SNePS 3 User&rsquo;s Manual&rdquo;](https://cse.buffalo.edu/sneps/Projects/sneps3manual.pdf) by Stuart Shapiro
    * Reference this paper to understand the user commands. The pseudo-yacc rules are defunct in Python_SNePS.

5. [&ldquo;Types in SNePS 3&rdquo;](https://cse.buffalo.edu/~shapiro/Talks/TypesInSneps3.pdf) by Stuart Shapiro
    * This paper clearly explains the relationship between caseframes and slots. Note that slots are called relations in the paper.

6. [&ldquo;Concurrent Resoning in Inference Graphs&rdquo;](https://cse.buffalo.edu/~shapiro/Papers/schsha13e.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * Explains much of the induction work done in the SNiPS package (Note that this is not all complete in CSNePS)

## Section 1: Structure

### Nodes

A node is a unique syntactic object, consisting of the following:
1. Name
2. Semantic Type
3. Up Cableset (An array of frames)
4. Docstring

and sometimes:

5. Frame

Nodes are typecast to syntactic types. Syntactic types are represented by classes.

![Syntactic Types](https://raw.githubusercontent.com/acampbel-hamilton/Python_SNePS/master/assets/syntactic.svg)

MinMaxOpNodes are created by thresh and andor.

### Frames

A frame is a unique object, consisting of the following tuple:
1. Caseframe
2. Filler Set (An ordered list of fillers)

Each Fillers instance must correspond to a slot in the caseframe (i.e. their semantic types must be compatible)
Each molecular node has a single frame.

### Fillers

A filler is a non-unique object that contains an array of nodes.

### Caseframes

A caseframe is a unique object, consisting of the following:
1. Name
2. Semantic Type
3. Semantic Hierarchy (Of the parent network)
4. Docstring
5. Slots (An ordered list of slots)
6. Aliases (An array of strings also referring to this frame)

### Slots

Slots are &ldquo;relations.&rdquo; A slot is a unique object, consisting of the following:
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

## Section 2: Using Python SNePS's Functions

Create a network object:

```python
from psneps import *
net = Network()
```

The following methods are defined:

```python
# Defines a term with a name and optional semantic type.
# The default semantic type is Entity.
net.define_term("Ben", sem_type_name="Agent")

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
net.define_slot("class", "Category",
                docstring="Points to a Category that some Entity is a member of.",
                pos_adj="none", neg_adj="reduce", min=1, max=0, path='')

# Lists all slots
net.list_slots()

# Defines a new caseframe with a name, semantic type, list of slots,
# and optional docstring
net.define_caseframe("Isa", "Propositional", ["member", "class"],
                     docstring="Epistemic relationship for class membership")

# Lists all caseframes or find a specific caseframe
net.list_caseframes()
net.find_caseframe("Isa")

# Passes wft followed by optional parameter "inf" for
# triggering forward inference
net.assert_wft("Isa(Dog, Pet)", inf=False)

# Prints out a visual representation of the knowledge base
net.print_graph()
```

## Section 3: Using Python SNePS's Well Formed Terms (wfts)

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
    |        'some' '(' atomicName '(' atomicName ')' ',' argument ')'
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

## Section 4: Viewing Graphs

Viewing graphs requires some extra Python modules. If you want to visualize small graphs, run:
```bash
pip install networkx matplotlib
```
If you want draggable graphs, then also run:
```bash
pip install netgraph
```
If you want the graphs to be exported as a dot file:
```bash
pip install pydot
```
