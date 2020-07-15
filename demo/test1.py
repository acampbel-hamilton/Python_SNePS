from src import *
net = Network()

net.define_context("test")
net.set_current_context("test")

net.assert_wft("nand(a, b, c, d)")
net.assert_wft("2=>([a, b, c, d], [not(e), f, g])")
net.assert_wft("and(a, b)")

snips = Inference(net)
snips.toggle_debug()
snips.ask("e")

print('\n\n')

net.assert_wft("Isa(Fido, Fido)")
net.assert_wft("Isa(Fido, Dog)")
net.assert_wft("Isa(Dog, Animal)")
print(net.paths_from(['Dog'], 'converse(and(irreflexive-restrict([member-, kstar([class, member-]), class]), [member-, class]))'))

net.list_slots()

net.export_graph()
net.print_graph()
