from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Entity")
net.define_slot("happy", "Entity", path="converse(converse(and(agent, compose(member, class))))", min=0, pos_adj="reduce", neg_adj="expand")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy"])
net.assert_wft("if(Has(Dog, Bone), Happy(Dog))")
net.assert_wft("if(not(Has(Dog, Bone)), not(Happy(Dog)))")
net.assert_wft("iff(Has(Dog, Bone), Happy(Dog))")
net.assert_wft("Equiv([wft7, and(wft6, wft3)])", True)

net.define_slot("happy_thing", "Thing", path="", min=0, pos_adj="expand", neg_adj="reduce")
net.define_caseframe("Happy_Thing", "Propositional", ["happy_thing"])


snips = Inference(net)
snips.ask("iff(Has(Dog, Bone), Happy(Dog))")

net.print_graph()
