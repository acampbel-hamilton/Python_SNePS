from psneps import *
net = Network.Network()
net.assert_wft("Isa([Ben, John, Seamus], [SNwiz, Student])")
net.define_slot("?test", "Propositional")
net.print_graph()
