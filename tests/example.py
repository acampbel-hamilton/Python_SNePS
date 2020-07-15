from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_context("test")
net.set_current_context("test")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])

# net.assert_wft("and(Isa(some(x(g), Isa([x, every(g, Isa(g, Test))], Human)), Animal), Isa(some(y(z), Isa([y, every(z, Isa(z, Test))], Human)), Being))")
# net.assert_wft("and(Isa(some(x(g), Isa([x, every(g, Isa(g, Test))], Human)), Animal), Isa(some(y(z), Isa([y, every(z, Isa(z, Test))], Human)), Being))")
# # net.assert_wft("nand(a, b, c, d)")
#
# # net.assert_wft("2=>([a, b, c, d], [not(e), f, g])")
# # net.assert_wft("and(a, b)")
#
# snips = Inference(net)
# snips.toggle_debug()
# snips.ask("Isa(some(x(g), Isa([x, every(g, Isa(g, Test))], Human)), Animal)")
#
# print('\n\n')

# net.assert_wft("if(Equiv(test1, test2), Equiv(test1, test2))")
# net.assert_wft("Isa(test1, test2)")
# net.define_path('member', '[!, member, kstar(member-, !, class)]')
net.assert_wft("Isa(Fido, Fido)")
net.assert_wft("Isa(Fido, Dog)")
net.assert_wft("Isa(Dog, Animal)")
print(net.paths_from(['Dog'], 'converse(and(irreflexive-restrict([member-, kstar([class, member-]), class]), [member-, class]))'))

# net.list_contexts()
# net.list_slots()
# net.list_caseframes()
# net.list_terms()
# net.list_types()

net.export_graph()
net.print_graph()
