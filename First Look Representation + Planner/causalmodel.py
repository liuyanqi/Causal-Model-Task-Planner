import random

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
		if scount != 0:
			sprob =  1 / scount
		else: 
			scount = 0

		if ucount != 0:
			uprob =  1 / ucount
		else: 
			ucount = 0

		probs = []
		for action in actionslist:
			if action.action.name == "stack":
				probs.append(sprob)
			else:
				probs.append(uprob)

		return probs

	@staticmethod
	def chooseNextAction(specifiedactions):
		#Returns the index of the probability distro defined by the array
		#That was sampled
		def sampleProbs(probabilities):
			r = random.random()
			for x in range(len(probabilities)):
				r = r - probabilities[x]
				if r <= 0:
					return x

		probs = CausalModel.__getActionProbabilities(specifiedactions)
		next_action = specifiedactions[sampleProbs(probs)]
		return next_action


