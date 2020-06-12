from sys import stderr

class SemanticHierarchy:
    # Contains tree-like structure for semantics (Entity, individual, etc.)
    def __init__(self):
        self.root_node = SemanticType("Entity")
        self.sem_types = {}
        self.sem_types["Entity"] = self.root_node

    def add_type(self, type_name, parent_names):
        assert type_name not in self.sem_types

        self.sem_types[type_name] = SemanticType(type_name)

        for name in parent_names:
            self.sem_types[type_name].add_parent(self.sem_types[name])
            self.sem_types[name].add_child(self.sem_types[type_name])

        return self.sem_types[type_name]

    def respecification(self, term_name, current_type, new_type):
        # Given new and old semantic type for a node, returns a computed new type
        # e.g. Cassie is a human and a robot, therefore Cassie is a cyborg
        if current_type is new_type:
            return new_type

        gcd = self.greatest_common_subtype(term_name, current_type, new_type)
        if gcd is not None:
            return gcd

        print('WARNING: Did not retypecast', term_name, file=stderr)
        return current_type

    def greatest_common_subtype(self, term_name, type1, type2):
        # This is a double-rooted DFS
        v1 = set() # Visited set from root 1
        v2 = set() # Visited set from root 2
        d1 = 0 # Depth for root 1
        d2 = 0 # Depth for root 2
        q1 = [(type1, d1)] # Queue for root 1
        q2 = [(type2, d2)] # Queue for root 2

        target_depth = -1

        # Finds greatest common subtypes in tree-like-structure
        gcds = []
        while q1 or q2:
            if q1 and (d1 <= d2 or q2 == []): # If the queue isn't empty and we haven't looked too deep (or the other search is over)
                n1, d1 = q1.pop(0)
                if d1 > d2 and q2 != []: # If we go too deep, just undo (this is gross nasty)
                    q1.insert(0, (n1, d1))
                elif n1 in v2 and (target_depth == -1 or d1 <= target_depth): # Found a common descendant
                    gcds.append(n1)
                    target_depth = d1
                elif n1 not in v1 and (target_depth == -1 or d1 + 1 <= target_depth): # Found something new
                    v1.add(n1)
                    q1 += [(child, d1 + 1) for child in n1.children]
            if q2 and (d2 <= d1 or q1 == []): # If the queue isn't empty and we haven't looked too deep (or the other search is over)
                n2, d2 = q2.pop(0)
                if d2 > d1 and q1 != []: # If we go too deep, just undo (this is gross nasty)
                    q2.insert(0, (n2, d2))
                elif n2 in v1 and (target_depth == -1 or d2 <= target_depth): # Found a common descendant
                    gcds.append(n2)
                    target_depth = d2
                elif n2 not in v2 and (target_depth == -1 or d2 + 1 <= target_depth): # Found something new
                    v2.add(n2)
                    q2 += [(child, d2 + 1) for child in n2.children]

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
