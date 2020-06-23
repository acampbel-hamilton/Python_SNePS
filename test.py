from psneps import *

net = Network.Network()
net.assert_wft("if(a, b)")
net.assert_wft("=>(a, b)")
