"""
A little test file.
"""

from Python_SNePS import *

net = Network.Network()

net.assert_wft("or(a, b)")

net.all_terms()
