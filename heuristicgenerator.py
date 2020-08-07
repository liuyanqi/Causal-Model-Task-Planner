import numpy as np
from causalmodel import CausalModel, sampleProbs
import math

class HeuristicGenerator():
	def __init__(self, domain):
		self._domain = domain

	def _stack_heuristic(self, action):
		predicates = self.causal.getPredicates(action)
		stackability = predicates["stackability"]
		# print("Stackability: " + str(stackability))
		tot_weight = action.state.get(action.parameters[0]).weight + action.state.get(action.parameters[1]).weight

		#SHOULD DO INDEPENDANT NORMALIZATION HERE
		#Might work better if do weight normalization, then stackability will work
		# print(stackability + tot_weight)
		return stackability + tot_weight

	@staticmethod
	def normalize(array):
		#WHOOPS SAME AS SOFTMAX
		acc = 0
		for x in range(0, len(array)):
			array[x] = math.exp(array[x])
			acc += array[x]
		for x in range(0, len(array)):
			array[x] = array[x] / acc
		return array

	def _normalized_stack_heuristic(self, actionslist):
		weight_array = []
		stackability_array = []
		for action in actionslist:
			# print(str(type(action.action).__name__) + " " + str(action.parameters))
			# if action.parameters[1] == "a":
			# 	stackability_array.append(-2)
			# 	weight_array.append(-2)
			# else:
			predicates = self._domain.causal_models[type(action.action).__name__].runModel(action)
			stackability = predicates["stackable"]
			weight = action.state.get(action.parameters[0]).weight + action.state.get(action.parameters[1]).weight
			stackability_array.append(stackability)
			weight_array.append(weight)

		# print(stackability_array)
		stackability_array = softmax(np.array(stackability_array))
		# print(stackability_array)
		# print(weight_array)
		weight_array = softmax(np.array(weight_array))
		# print(weight_array)


		vals = []
		for x in range(0, len(stackability_array)):
			vals.append((20*stackability_array[x]) + (0.1*weight_array[x]))

		# print(softmax(np.array(vals)))

		return softmax(np.array(vals))


		# print(stackability_array)
		# print(softmax(np.array(stackability_array)))
		# print(HeuristicGenerator.normalize(stackability_array))
		# print(weight_array)
		# print(softmax(np.array(weight_array)))
		# print(HeuristicGenerator.normalize(weight_array))
		# return 


	def _unstack_heuristic(self, action):
		# predicates = self.causal.getPredicates(action)
		# stackability = predicates["stackability"]
		# print("Stackability: " + str(stackability))
		# tot_weight = action.state.get(action.parameters[0]).weight + action.state.get(action.parameters[1]).weight

		# SHOULD DO INDEPENDANT NORMALIZATION HERE
		return 3



	def _getVisualProbabilities(self, actionslist, debug):
		#For each action get the stackability of the blocks
		#Get their weights as well
		heur_array = []

		# print(actionslist)

		# for action in actionslist:
		# 	name = type(action.action).__name__
		# 	if name == "stack":
		# 		heur_array.append(self._stack_heuristic(action))
		# 	elif name == "unstack":
		# 		heur_array.append(self._unstack_heuristic(action))

		# ret = softmax(np.array(heur_array))
		ret = self._normalized_stack_heuristic(actionslist)

		if debug:
			# retstr = "["
			# for a in actionslist:
			# 	retstr += type(a.action).__name__ + str(a.parameters) + ", "

			# retstr += "]"
			# print("Current possible actions: ")
			# print(retstr)
			# print("Probabilities of those actions: ")
			# print(str(ret) + "\n")
			pass

		return ret


	def chooseNextAction(self, actionslist):
		probs = self._getVisualProbabilities(actionslist, False)
		x = sampleProbs(probs)
		return actionslist[x]


def softmax(xs):
	return np.exp(xs) / sum(np.exp(xs))
