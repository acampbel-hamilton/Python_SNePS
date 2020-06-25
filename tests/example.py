from psneps import *
net = Network.Network()
net.assert_wft("Isa([Ben, John, Seamus], [SNwiz, Student])")
net.define_caseframe("?test", "Propositional", ["member"])
net.print_graph()
