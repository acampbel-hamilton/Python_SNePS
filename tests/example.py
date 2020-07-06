from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])


net.assert_wft("1=>([Has(John, Food), Has(John, Bone), Has(John, Philosophy)], Happy(John))")
net.assert_wft("Has(John, Food)")

snips = Inference(net)
test = snips.ask_if("Happy(John)")
print(test)

net.export_graph()
net.print_graph()
