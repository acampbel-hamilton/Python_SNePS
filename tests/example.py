from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])


net.assert_wft("2=>([a, b, c, d], [not(e), f, g])")
# net.assert_wft("1=>([Has(every(x, Isa(x, Dog)), Food), Has(x, Bone), Has(x, Philosophy)], Happy(x))")
net.assert_wft("and(b, a)")

snips = Inference(net)
snips.ask("e")

net.export_graph()
net.print_graph()
