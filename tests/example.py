from psneps import *
net = Network.Network()
net.define_caseframe("Has", "Propositional", ["member", "member"])
net.define_caseframe("Happy", "Propositional", ["member"])
net.assert_wft("if(Has(Dog, Bone), Happy(Dog))")
net.print_graph()
