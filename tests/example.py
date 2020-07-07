from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])


net.assert_wft("2=>([a, b, c, d], [e, f, g])")
net.assert_wft("and(b, a)")

snips = Inference(net)
test = snips.ask_if("g")
print(test)

net.export_graph()
net.print_graph()
