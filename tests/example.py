from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_context("test")
net.set_current_context("test")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])

net.assert_wft("and(every(x, andor{1, 3}(x, Human)), every(z, andor{1, 2}(z, Human)), some(y(x, z), Isa(y, Dog)))")
# net.assert_wft("every(x, [and(x, Human), Isa(x, Dog)])")
# net.assert_wft("every(x, [Isa(x, Dog), and(Human, x)])")

net.assert_wft("2=>([a, b, c, d], [not(e), f, g])")
net.assert_wft("and(a, b)")

snips = Inference(net)
snips.toggle_debug()
snips.ask("e")

net.export_graph()
net.print_graph()
