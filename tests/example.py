from psneps import *
net = Network()
net.define_slot("agent", "Entity")
net.define_slot("has", "Thing")
net.define_slot("happy_thing", "Thing")

net.define_caseframe("Has", "Propositional", ["agent", "has"])
net.define_caseframe("Happy", "Propositional", ["happy_thing"])
# net.assert_wft("if(Has(Dog, Bone), Happy(Dog))")
# net.assert_wft("if(not(Has(Dog, Bone)), not(Happy(Dog)))")
net.assert_wft("=>([Has(every(x, Isa(x, Dog)), Food), Has(x, Bone), Has(x, Philosophy)], Happy(x))")
net.assert_wft("not(Philosophy)")
# net.assert_wft("Equiv([wft7, and(wft6, wft3)])")
#
# net.assert_wft("if( every(x, Isa(x, Dog)) , some(y(x), Dog) )")
#
snips = Inference(net)
snips.ask("Philosophy")
#
# net.assert_wft("Isa( every(x, Isa(x, Dog)) , some(y(x), Isa(y, Dog)) )")

net.export_graph()
net.print_graph()
