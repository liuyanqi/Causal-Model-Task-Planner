from blockworld import BlockTower
from planner import Planner
import functools
from causalmodel import CausalModel
from visualmodel import BlockVisualModel
from blockworld import Goal
from riverworld import RiverWorld


#TODO
#Try w unreasonable goal, and find out why crashes/ encode terminal state
#

if __name__ == "__main__":
	# #------Block Domain----------
	domain = BlockTower()
	myPlan = Planner(domain, Goal(height=4))

	#Uncomment to run BFS
	# viz = BlockVisualModel(domain)
	# myPlan.setAlgo(functools.partial(myPlan.BFS, self=myPlan))

	# #Uncomment to run naive Causal model w no visual model
	# viz = BlockVisualModel(domain)
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=CausalModel.chooseNextAction))

	# #Uncomment to run Causal model with visual model
	viz = BlockVisualModel(domain)
	viz_func = functools.partial(CausalModel.chooseNextActionVisual, viz=viz, domain=domain, debug=False)
	myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=viz_func))

	Planner.printHistory(myPlan.plan())
	# myPlan.collectStats(1000)
	print()
	print(viz.flatness_vals)

	#--------------River Domain----------------------
	# domain = RiverWorld()
	# planner = Planner(domain, None)
	# planner.setAlgo(functools.partial(planner.BFS, self=planner))
	# Planner.printHistory(planner.plan())
	# domain.cross.doAction(domain.state, ["Boat"])
	# domain.state.get("Boat").inside = "wolf"
	# domain.cross.doAction(domain.state, ["Boat"])
	# print(domain.state)
