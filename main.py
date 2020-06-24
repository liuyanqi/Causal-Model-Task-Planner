from blockworld import BlockTower
from planner import Planner
import functools
from causalmodel import CausalModel
from visualmodel import BlockVisualModel


if __name__ == "__main__":
	domain = BlockTower()
	myPlan = Planner(domain)

	viz = BlockVisualModel(domain)

	#Uncomment to run BFS
	# myPlan.setAlgo(functools.partial(myPlan.BFS, self=myPlan))

	#Uncomment to run naive Causal model w no visual model
	# myPlan.setAlgo(functools.partial(myPlan.Causal, self=myPlan, chooseNextAction=CausalModel.chooseNextAction))

	#Uncomment to run Causal model with visual model
	viz_func = functools.partial(CausalModel.chooseNextActionVisual, viz=viz, domain=domain)
	myPlan.setAlgo(functools.partial(myPlan.Causal2, self=myPlan, pickBestAction=viz_func))

	Planner.printHistory(myPlan.plan())
