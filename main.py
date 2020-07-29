from blockworld import BlockTower
from planner import Planner
import functools
from causalmodel import CausalModel
from visualmodel import BlockVisualModel
from blockworld import Goal
from riverworld import RiverWorld
from heuristicgenerator import HeuristicGenerator
from visualizer import runSim
from customerrors import SimulationOver


if __name__ == "__main__":
	# #------Block Domain----------
	domain = BlockTower()
	myPlan = Planner(domain)

	#Uncomment to run BFS
	# viz = BlockVisualModel(domain)
	# myPlan.setAlgo(functools.partial(myPlan.BFS, self=myPlan))

	# #Uncomment to run naive Causal model w no visual model
	# viz = BlockVisualModel(domain)
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=CausalModel.chooseNextAction))

	# #Uncomment to run Causal model with visual model
	# viz = BlockVisualModel(domain)
	# viz_func = functools.partial(CausalModel.chooseNextActionVisual, viz=viz, domain=domain, debug=False)
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=viz_func))

	# Planner.printHistory(myPlan.plan())
	# # myPlan.collectStats(1000)
	# print()
	# print(viz.flatness_vals)

	#------------------Entirelly new domain----------
	viz = BlockVisualModel(domain)
	causal = CausalModel(viz)
	heur = HeuristicGenerator(causal)
	myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=heur.chooseNextAction))
	print(domain.state)
	# myPlan.collectStats(1000)
	res = myPlan.plan()
	Planner.printHistory(res)
	runSim(res, myPlan)


	#--------------River Domain----------------------
	# domain = RiverWorld()
	# planner = Planner(domain, None)
	# planner.setAlgo(functools.partial(planner.BFS, self=planner))
	# Planner.printHistory(planner.plan())
	# domain.cross.doAction(domain.state, ["Boat"])
	# domain.state.get("Boat").inside = "wolf"
	# domain.cross.doAction(domain.state, ["Boat"])
	# print(domain.state)
