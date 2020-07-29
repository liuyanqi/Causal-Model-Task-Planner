import random
from visualmodel import BlockVisualModel 
import numpy as np

class CausalModel():
	def __init__(self, viz):
		self.viz = viz

	def getPredicates(self, action):
		if len(action.parameters) == 2:
			x = action.parameters[0]
			y = action.parameters[1]
		
			return {"stackability": self.viz.getFlatnessVals(x)["top"] * self.viz.getFlatnessVals(y)["bottom"]}
		else:
			return {"stackability": self.viz.getFlatnessVals(action.parameters[0])["top"]}
	

	# @staticmethod
	# def __getActionProbabilities(actionslist):
	# 	scount = 0
	# 	ucount = 0
	# 	for action in actionslist:
	# 		if action.action.name == "stack":
	# 			scount += 1
	# 		else:
	# 			ucount += 1

	# 	if scount != 0 and ucount != 0:
	# 		s_cum_prob = 0.9
	# 		u_cum_prob = 0.1
	# 	elif scount != 0:
	# 		s_cum_prob = 1
	# 		u_cum_prob = 0
	# 	elif ucount != 0:
	# 		s_cum_prob = 0
	# 		u_cum_prob = 1
	# 	else:
	# 		print("NO VALID ACTIONS???")

	# 	if scount != 0:
	# 		sprob =  s_cum_prob / scount
	# 	else:
	# 		sprob = 0

	# 	if ucount != 0:
	# 		uprob =  u_cum_prob / ucount
	# 	else:
	# 		uprob = 0

	# 	probs = []
	# 	for action in actionslist:
	# 		if action.action.name == "stack":
	# 			probs.append(sprob)
	# 		else:
	# 			probs.append(uprob)

	# 	return probs

	@staticmethod
	def sampleProbs(probabilities):
			r = random.random()
			for x in range(len(probabilities)):
				r = r - probabilities[x]
				if r <= 0:
					return x

	# @staticmethod
	# def chooseNextAction(actionslist):
	# 	#Returns the index of the probability distro defined by the array
	# 	#That was sampled
	# 	probs = CausalModel.__getActionProbabilities(actionslist)
	# 	next_action = actionslist[CausalModel.sampleProbs(probs)]
	# 	return next_action

	# @staticmethod
	# def chooseUniformAction(specifiedactions):
	# 	return random.choice(specifiedactions)



