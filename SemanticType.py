from sys import stderr
from math import inf

class SemanticHierarchy:
    # Contains tree-like structure for semantics (Entity, individual, etc.)
    def __init__(self):
        self.root_node = SemanticType("Entity")
        self.sem_types = {}
        self.sem_types["Entity"] = self.root_node

    def add_type(self, type_name, parent_names=[]):
        # Must be unique
        assert type_name not in self.sem_types

        # Crreate new type in hierarchy
        self.sem_types[type_name] = SemanticType(type_name)

        # If type provides parents, connect to these nodes in tree
        for name in parent_names:
            self.sem_types[type_name].add_parent(self.sem_types[name])
            self.sem_types[name].add_child(self.sem_types[type_name])

        # If no parents provided, set as child of 'Entity'
        if parent_names == []:
            self.sem_types[type_name].add_parent(self.root_node)
            self.root_node.add_child(self.sem_types[type_name])

        return self.sem_types[type_name]

    def respecification(self, term_name, current_type, new_type):
        # Given new and old semantic type for a node, returns a computed new type
        # e.g. Cassie is a human and a robot, therefore Cassie is a cyborg
        if current_type is new_type or current_type.subtype(new_type):
            return new_type

        gcd = self.greatest_common_subtype(term_name, current_type, new_type)
        if gcd is not None:
            return gcd

        print('WARNING: Did not retypecast', term_name, file=stderr)
        return current_type

    def greatest_common_subtype(self, term_name, type1, type2):
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
        v2 = visited

        if type2 in v1:
            gcds = [type2]
        elif type1 in v2:
            gcds = [type1]
        else:
            # This could be made faster by changing the second dfs to not add nodes deeper than the smallest gcd depth so far. We still need to look at them to detect direct lineages, though.
            gcds = []
            target_depth = inf
            for node in set(v1) & set(v2):
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

class SemanticType:
    # Node in semantic hierarchy
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_child(self, child):
        self.children.append(child)

    def compatible(self, other_type):
        return other_type is self or other_type.subtype(self)

    def subtype(self, potential_child):
        # Determines if given node is actually a child of self
        for child in self.children:
            if child is potential_child or child.subtype(potential_child):
                return True
        return False

if __name__ == "__main__":
    hierarchy = SemanticHierarchy()
    Human = hierarchy.add_type("Human")
    Robot = hierarchy.add_type("Robot")
    Human2 = hierarchy.add_type("Human2", ["Human"])
    Robot2 = hierarchy.add_type("Robot2", ["Robot"])
    Cyborg1 = hierarchy.add_type("Cyborg1", ["Human", "Robot2"])
    Cyborg2 = hierarchy.add_type("Cyborg2", ["Human2", "Robot"])


    print(hierarchy.respecification('CASSIE', Human, Robot))
