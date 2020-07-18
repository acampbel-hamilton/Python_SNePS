from src import *
net = Network()

net.define_type("Agent", ["Thing"])
net.define_slot("agent", "Agent")

net.define_slot("beats", "Thing")
net.define_caseframe("Beats", "Act", ["agent", "beats"])

net.define_slot("farmer", "Agent")
net.define_caseframe("Farmer", "Proposition", ["farmer"])

net.define_slot("donkey", "Thing")
net.define_caseframe("Donkey", "Proposition", ["donkey"])

net.define_slot("owner", "Agent")
net.define_slot("owns", "Thing")
net.define_caseframe("Owns", "Proposition", ["owner", "owns"])

net.assert_wft("Beats(every(x, [Farmer(x), Owns(x, some(y(x), Donkey(y)))]), y)")

net.export_graph("donkey")
net.display_graph()
