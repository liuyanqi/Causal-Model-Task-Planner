import numpy as np
#from causalmodel import CausalModel, sampleProbs
import math

class FurnitureHeuristicGenerator():
	def __init__(self, domain):
		self._domain = domain
		self.current_weight_array = []
		self.picked_ind = None
		self.actionslist = []
		#self.function_causal_graph=domain.function_causal_graph

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

	def _normalized_combine_heuristic(self, actionslist):

		#state = actionslist[0].state
		constraint = self._domain.constraint.height
		# current_func = state.current_func
		# next_func = self.function_causal_graph.obj_func[current_func].next_func
		# curr_object = self.function_causal_graph.obj_func[current_func].objects
		# next_object = self.function_causal_graph.obj_func[next_func].objects
		causal_score_array = []
		constraint_score_array = []
		# print("current_func ", current_func, "next_func ", next_func, " next_object ", next_object)
		# for action in actionslist:
		# 	if current_func == "init":
		# 		if action.parameters[0] in next_object:
		# 			weight_array.append(2)
		# 		else:
		# 			weight_array.append(0)
		# 	else:
		# 		if action.parameters[1] in next_object:
		# 			weight_array.append(2)
		# 		elif action.parameters[1] in curr_object:
		# 			weight_array.append(1)
		# 		else:
		# 			weight_array.append(0)
		#
		# normalized_score = self.normalize(weight_array)
		for action in actionslist:
			score = action.state.causal_graph.runModel(action.state, action)
			causal_score_array.append(score)
			current_height = action.state.total_height + action.state.get(action.parameters[1]).height
			if current_height > constraint:
				constraint_score_array.append(1)
			else:
				constraint_score_array.append(0)

		normalized_score = np.array(self.normalize(causal_score_array)) * np.array(self.normalize(constraint_score_array))
		self.current_weight_array = list(normalized_score)
		# print(softmax(np.array(vals)))

		return self.current_weight_array


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
		ret = self._normalized_combine_heuristic(actionslist)

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

	def __pickhighest(self, probs):
		return probs.index(max(probs))

	def chooseNextAction(self, actionslist):
		self.actionslist = actionslist
		probs = self._getVisualProbabilities(actionslist, False)

		x = self.__pickhighest(probs)
		self.picked_ind = x
		return actionslist[x], probs

	def repickNextAction(self, picked_idx=None):
		#print(self.picked_ind)
		if picked_idx is None:
			self.current_weight_array.pop(self.picked_ind)
		else:
			self.current_weight_array.pop(picked_idx)
		print(self.current_weight_array)
		x = self.__pickhighest(self.current_weight_array)
		return self.actionslist[x]

def softmax(xs):
	return np.exp(xs) / sum(np.exp(xs))
