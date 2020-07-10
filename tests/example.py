from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])

net.assert_wft("2=>([every(y, Isa(y, Dog)), b, c, d], [not(e), f, g])")
net.assert_wft("and(every(y, Isa(y, Dog)), b)")
net.assert_wft("e")

snips = Inference(net)
snips.toggle_debug()
snips.ask("e")

net.export_graph()
net.print_graph()
