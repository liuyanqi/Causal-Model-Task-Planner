import numpy as np
#from causalmodel import CausalModel, sampleProbs
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
		height_array = []
		score = []
		normalized_score = []
		weight_sum = 0
		height_sum = 0
		goal_weight = self._domain.goal.weight
		goal_height = self._domain.goal.height

		for action in actionslist:

			# print("ACTION:", str(type(action.action).__name__) + " " + str(action.parameters))
			# if action.parameters[1] == "a":
			# 	stackability_array.append(-2)
			# 	weight_array.append(-2)
			# else:
			# predicates = self._domain.causal_models[type(action.action).__name__].runModel(action)
			# stackability = predicates["stackable"]
			weight = action.state.get(action.parameters[0]).weight + action.state.get(action.parameters[1]).weight
			height = action.state.get(action.parameters[0]).height + action.state.get(action.parameters[1]).height

			weight_sum += weight/goal_weight
			height_sum += height/goal_height
			weight_array.append(weight/goal_weight)
			height_array.append(height/goal_height)

		score_sum = 0
		for i in range(len(weight_array)):
			score.append(weight_array[i]/weight_sum  * height_array[i]/height_sum)
			score_sum += score[i]
		normalized_score = [score[i] / sum(score) for i in range(len(score))]


		# print(softmax(np.array(vals)))

		return normalized_score


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
		return actionslist[x], probs


def softmax(xs):
	return np.exp(xs) / sum(np.exp(xs))
