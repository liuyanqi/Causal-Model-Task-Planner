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

		if scount != 0 and ucount != 0:
			s_cum_prob = 0.8
			u_cum_prob = 0.2
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


