from blockworld import BlockTower
from planner import Planner
import functools
import causalmodel
from visualmodel import BlockVisualModel
from blockworld import Goal, BlockTowerState
from riverworld import RiverWorld
from heuristicgenerator import HeuristicGenerator
from visualizer import runSim
from customerrors import SimulationOver
from abstracttypes import SpecificAction

# from pypddlparser.pddlparser import PDDLParser
# from pypddlparser import main
# import pypddl_parser.pypddl_parser.pddlparser
# import pypddl_parser.pypddl_parser.main

def runSimulation(myplanner):
	# temp_state = BlockTowerState()
	# temp_state.get("a").on = "b"
	# temp_state.get("b").on = "d"
	# temp_state.get("d").on = "c"
	# temp_state.total_weight = 2



	res = myplanner.plan()
	Planner.printHistory(res)
	try:
		# myplanner.domain.state = temp_state
		runSim(res, myplanner)
	except SimulationOver as e:
		print(type(e.message))
		if e.message == None:
			print("Sucess! Goal acheived")
		else:
			domain.state = e.message
			runSimulation(myplanner)
		


if __name__ == "__main__":

	domain = BlockTower()
	myPlan = Planner(domain)
	causalmodel.generateCausalModels("./pypddl_parser/pypddl_parser/pddl/tower/domain.pddl", domain)
	# print(cm[0].runModel(SpecificAction(domain.stack, ["a", "b"], domain.state)))


	heur = HeuristicGenerator(domain)
	myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, pickBestAction=heur.chooseNextAction))
	runSimulation(myPlan)

	print(domain.causal_models)
	
	'''
	Add causal models to a domain
	For each action search through the causal models to find one who matches in name
	If no matches, raise error
	Or could do model completeness checking earlier
	'''


	# print(cm.getPredicates(SpecificAction(domain.stack, ["a", "b"], domain.state)))

	'''
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
	runSimulation(myPlan)



	# print(domain.state)
	# myPlan.collectStats(1000)
	# res = myPlan.plan()
	# Planner.printHistory(res)
	# simret = runSim(res, myPlan)
	# if simret != None:
	# 	domain.state = copy.deepcopy(simret)




	#--------------River Domain----------------------
	# domain = RiverWorld()
	# planner = Planner(domain, None)
	# planner.setAlgo(functools.partial(planner.BFS, self=planner))
	# Planner.printHistory(planner.plan())
	# domain.cross.doAction(domain.state, ["Boat"])
	# domain.state.get("Boat").inside = "wolf"
	# domain.cross.doAction(domain.state, ["Boat"])
	# print(domain.state)
	'''
