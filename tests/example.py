from psneps import *
net = Network.Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Entity")
net.define_slot("happy", "Entity", path="converse(has)")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy"])
net.assert_wft("if(Has(Dog, Bone), Happy(Dog))")
net.assert_wft("if(not(Has(Dog, Bone)), not(Happy(Dog)))")
net.assert_wft("iff(Has(Dog, Bone), Happy(Dog))")
net.assert_wft("Equiv([wft7, and(wft6, wft3)])")
net.print_graph()
