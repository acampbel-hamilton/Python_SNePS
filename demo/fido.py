from src import *
net = Network()

net.define_type("Agent", ["Thing"])
net.define_slot("agent", "Agent")

net.define_slot("happy", "Agent")
net.define_caseframe("Happy", "Proposition", ["happy"])

net.define_slot("has", "Thing")
net.define_caseframe("Has", "Proposition", ["agent", "has"])

net.assert_wft('''if(   [Has(some(x (), Isa(x, Dog)), some(q (x), Isa(q, Bone))),
                         Has(x, some(y (x), Isa(y, Food))),
                         Has(x, some(z (x), Isa(z, Philosophy)))],
                     Happy(x))''')

net.assert_wft("Isa(Fido, Dog)")

net.export_graph("fido")
net.display_graph()
