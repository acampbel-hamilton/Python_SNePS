from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])

net.assert_wft("Has(every(x, andor{1, 3}(x, Human)), some(y(x), Isa(y, Dog)))")
net.assert_wft("every(x, andor{2, 2}(x, Human))")
net.assert_wft("every(x, and(Human, x))")

net.assert_wft("2=>([a, b, c, d], [not(e), f, g])")
net.assert_wft("and(a, b)")

snips = Inference(net)
snips.toggle_debug()
snips.ask("e")

net.export_graph()
net.print_graph()
