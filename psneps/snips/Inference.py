from ..Network import *

"""
This is the main file of the SNIPS package. In here, we define the Inference class.
Authors: Ben Kallus, John Madigan, and Seamus Wiseman
"""

class Inference:
    def __init__(self, net: Network):
        self.net = net

    def ask(self, wft_str: str):
        wft = wft_parser(wft_str, self.net)[0]
        not_wft = wft_parser('not({})'.format(wft.name), self.net)[0]
