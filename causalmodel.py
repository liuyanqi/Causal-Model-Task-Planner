import random
from visualmodel import BlockVisualModel 
import numpy as np

class CausalModel():
	@staticmethod
	def __getActionProbabilities(actionslist):
		scount = 0
		ucount = 0
		for action in actionslist:
			if action.action.name == "stack":
				scount += 1
			else:
				ucount += 1

		if scount != 0 and ucount != 0:
			s_cum_prob = 0.9
			u_cum_prob = 0.1
		elif scount != 0:
			s_cum_prob = 1
			u_cum_prob = 0
		elif ucount != 0:
			s_cum_prob = 0
			u_cum_prob = 1
		else:
			print("NO VALID ACTIONS???")

		if scount != 0:
			sprob =  s_cum_prob / scount
		else:
			sprob = 0

		if ucount != 0:
			uprob =  u_cum_prob / ucount
		else:
			uprob = 0

		probs = []
		for action in actionslist:
			if action.action.name == "stack":
				probs.append(sprob)
			else:
				probs.append(uprob)

		return probs

	@staticmethod
	def sampleProbs(probabilities):
			r = random.random()
			for x in range(len(probabilities)):
				r = r - probabilities[x]
				if r <= 0:
					return x

	@staticmethod
	def chooseNextAction(actionslist):
		#Returns the index of the probability distro defined by the array
		#That was sampled
		probs = CausalModel.__getActionProbabilities(actionslist)
		next_action = actionslist[CausalModel.sampleProbs(probs)]
		return next_action

	@staticmethod
	def chooseUniformAction(specifiedactions):
		return random.choice(specifiedactions)

	@staticmethod
	def _getVisualProbabilities(actionslist, viz_model, domain):
		#For each action get the stackability of the blocks
		#Get their weights as well
		heur_array = []

		for action in actionslist:
			stackability = viz_model.getStackability(action.parameters[0], action.parameters[1])
			tot_weight = domain.state.get(action.parameters[0]).weight + domain.state.get(action.parameters[1]).weight

			heur_array.append(stackability + tot_weight)

		retstr = "["
		for a in actionslist:
			retstr += a.action.name + str(a.parameters) + ", "

		retstr += "]"
		print("Current possible actions: ")
		print(retstr)
		ret = softmax(np.array(heur_array))
		print("Probabilities of those actions: ")
		print(str(ret) + "\n")

		return ret

	@staticmethod
	def chooseNextActionVisual(actionslist, viz, domain):
		probs = CausalModel._getVisualProbabilities(actionslist, viz, domain)
		x = CausalModel.sampleProbs(probs)
		viz.update(domain.state)
		return actionslist[x]

def softmax(xs):
    return np.exp(xs) / sum(np.exp(xs))

