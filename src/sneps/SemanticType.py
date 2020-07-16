from math import inf
from .SNError import SNError
from re import match
from typing import List

# =====================================
# ------------- GLOBALS ---------------
# =====================================

class SemError(SNError):
    pass

# =====================================
# ---------- SEMANTIC TYPE ------------
# =====================================

class SemanticType:
    """ An object in the Network's semantic hierarchy. """

    def __init__(self, name: str):
        self.name = name
        self.parents = []
        self.children = []

    def __hash__(self) -> int:
        return hash(self.name) # Unique by name

    def __str__(self) -> str:
        return self.name

    def add_parent(self, parent) -> None:
        """ Adds parent to list of parents. """
        self.parents.append(parent)

    def add_child(self, child) -> None:
        """ Adds child to list of children. """
        self.children.append(child)

    def subtype(self, potential_child):
        """ Determines if given SemanticType is a subtype of self. """
        return any(child is potential_child or child.subtype(potential_child) for child in self.children)

    def __str__(self) -> str:
        return self.name

# =====================================
# -------- SEMANTIC HIERARCHY ---------
# =====================================

class SemanticHierarchy:
    """ Contains tree-like structure for semantic types (Entity, Individual, etc.) """

    def __init__(self) -> None:
        self.root_node = SemanticType("Entity")
        self.sem_types = {} # Maps strings to SemanticType objects
        self.sem_types["Entity"] = self.root_node

    def add_type(self, type_name: str, parent_names: List[str] = None) -> None:
        """ Adds a new semantic type to the hierarchy. This will be another function called by users. """
        parent_names = [] if parent_names is None else parent_names

        # Ensures uniqueness. If node already exists, adds any new parents.
        if type_name in self.sem_types:
            self.add_parents(type_name, parent_names)
            return

        # Create new type in hierarchy
        self.sem_types[type_name] = SemanticType(type_name)

        # If type provides parents, connect to these nodes in tree.
        for name in parent_names:
            self.sem_types[type_name].add_parent(self.sem_types[name])
            self.sem_types[name].add_child(self.sem_types[type_name])

        # If no parents provided, set as child of Entity
        if parent_names == []:
            self.sem_types[type_name].add_parent(self.root_node)
            self.root_node.add_child(self.sem_types[type_name])

        return self.sem_types[type_name]

    def assert_proposition(self, node):
        """ Casts a given node to a Proposition """
        self.respecify(node.name, node.sem_type, self.sem_types['Proposition'])

    def respecify(self, term_name: str, current_type: SemanticType, new_type: SemanticType) -> SemanticType:
        """ Given new and old semantic type for a node, returns a computed new type
            e.g. CASSIE is a Human and a Robot, therefore CASSIE is a Cyborg """

        # If no recasting necessary
        if current_type is new_type:
            return new_type

        # Returns greatest common subtype (one which derives from both new and old type)
        gcs = self.greatest_common_subtype(term_name, current_type, new_type)
        if gcs is not None:
            return gcs

        # If variable cannot be recast
        raise SemError('WARNING: Could not retypecast "' + term_name + '" from ' + current_type.name + " to " + new_type.name)
        return current_type

    def greatest_common_subtype(self, term_name: str, type1: SemanticType, type2: SemanticType):
        """ Finds the greatest common subtype of type1 and type2. If type1 is a
            subtype of type2, or vice versa, then that type is returned. If this
            isn't the case, then this function returns the type that derives
            from type1 and type2 has the minimum sum of shortest paths to type1
            and type2. """

        # Tracks to avoid infinite recursion
        visited = {}
        def dfs_depth_map(node, depth):
            if node not in visited:
                visited[node] = depth
                for child in node.children:
                    dfs_depth_map(child, depth + 1)

        dfs_depth_map(type1, 0)
        v1 = visited  # Visited set from root 1. Maps nodes to depths with respect to v1
        visited = {}
        dfs_depth_map(type2, 0)
        v2 = visited # Visited set from root 2. Maps nodes to depths with respect to v2

        if type2 in v1: # type2 is a descendant of type1
            gcds = [type2]
        elif type1 in v2: # type1 is a descendent of type2
            gcds = [type1]
        else:
            # This could be made faster by changing the second dfs to not add nodes deeper than the smallest gcd depth so far.
            # We still need to look at them to detect direct lineages, though.
            gcds = []
            target_depth = inf
            for node in set(v1) & set(v2): # For each type reachable from both type1 and type2
                if v1[node] + v2[node] < target_depth:
                    gcds = [node]
                    target_depth = v1[node] + v2[node]
                elif v1[node] + v2[node] == target_depth:
                    gcds.append(node)

        if gcds == []:
            return None

        # Allows user to select one if multiple greatest common subtypes
        if len(gcds) > 1:
            for i, gcd in enumerate(gcds, 0):
                print(i, '. ', gcd, sep='')
            while True:
                selection = input("Please select a new type for " + term_name + ": ")
                if not selection.isdecimal() or int(selection) not in range(len(gcds)):
                    print("Selection must be an integer between 0 and " + str(len(gcds) - 1) + ", inclusive.")
                    continue
                break

            return gcds[int(selection)]

        return gcds[0]

    def get_type(self, type_name: str):
        """ Returns the type in the hierarchy with the given name. """
        if type_name in self.sem_types:
            return self.sem_types[type_name]
        else:
            raise SemError('ERROR: Type "' + type_name + '" does not exist')

    def add_parents(self, type_name: str, parent_names: List[str]) -> None:
        """ Adds the parents named in the list to the type with name type_name. """
        type = self.sem_types[type_name]
        for parent_name in parent_names:
            parent = self.sem_types[parent_name]
            # Ensures duplicates not added
            if type not in parent.children:
                type.add_parent(parent)
                parent.add_child(type)

    def fill_slot(self, node, slot_type) -> None:
        """ Respecifies a node to a new type so it can fit in a slot for that type node """
        filler_type = node.sem_type
        if filler_type is not slot_type and not slot_type.subtype(filler_type):
                node.sem_type = self.respecify(node.name, filler_type, slot_type)

    def __str__(self) -> str:
        return ", ".join(self.sem_types.keys())

# =====================================
# -------------- MIXIN ----------------
# =====================================

class SemanticMixin:
    """ Provides functions related to semantic types to network """

    def __init__(self):
        if type(self) is SemanticMixin:
            raise NotImplementedError("Mixins can't be instantiated.")

        self.sem_hierarchy = SemanticHierarchy()

    def define_type(self, name: str, parent_names: List[str] = None):
        """ Adds a term to the semantic hierarchy. This is another important
            function for interacting with SNePS. """

        if not match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
            raise NodeError("ERROR: The semantic type name '{}' is not allowed.".format(name))

        parent_names = [] if parent_names is None else parent_names
        self.sem_hierarchy.add_type(name, parent_names)

    def list_types(self):
        """ Prints a string representation of each type in the semantic hierarchy. """
        print("[{}]".format(self.sem_hierarchy))
