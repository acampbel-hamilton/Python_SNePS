import unittest

import psneps
from psneps import Node, Network, SemanticType

class TestNodeMethods(unittest.TestCase):

    def test_find_term(self):
        n = Network.Network()

        #checks that it raises an error when there is no node
        with self.assertRaises(Node.NodeError):
            n.find_term('John')

        #checks that it returns the node
        n.define_term('John')
        assert(n.find_term('John').name == 'John')

    def test_respecification(self):
        n = Network.Network()
        n.define_type('Human', ['Thing'])
        n.define_type('Robot', ['Thing'])
        n.define_type('Cyborg', ['Human', 'Robot'])

        #check to see that John's type is a human
        n.define_term('John', 'Human')
        assert(n.find_term('John').sem_type.name == 'Human')

        #if John is a human and a robot then he is a cyborg
        n.define_term('John', 'Robot')
        assert(n.find_term('John').sem_type.name == 'Cyborg')

        #check that it raises a semantic error if it cannot be respecified
        n.define_type('Object')
        with self.assertRaises(SemanticType.SemError):
            n.define_term('John', 'Object')


if __name__ == '__main__':
    unittest.main()
