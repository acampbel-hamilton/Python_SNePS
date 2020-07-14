from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_context("test")
net.set_current_context("test")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])

net.assert_wft("and(Isa(every(x, Isa(x, Human)), Animal), Isa(every(x, Isa(x, Human)), Being))")
net.assert_wft("nand(a, b, c, d)")

# net.assert_wft("2=>([a, b, c, d], [not(e), f, g])")
# net.assert_wft("and(a, b)")

snips = Inference(net)
snips.toggle_debug()
snips.ask("e")

print(net.find_caseframe("Isa"))
print(net.find_slot("member"))
net.define_path("equiv", "compose(!, equiv, kstar(compose(equiv-, !, equiv)))")
print(net.find_slot("equiv"))


# net.export_graph()
net.print_graph()
