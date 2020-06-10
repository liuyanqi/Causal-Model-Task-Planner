import inspect
import world
import customerrors
import itertools

class Planner():
	def __init__(self, domain):
		self.domain = domain
		self.actions = [ m for m in dir(self.domain) if m.startswith("a_")]
		self.getValidActions()
		# self.pickRandomBlocks()

	def getValidActions(self):
		#Generate all possible inputs
		possible_inputs = list(itertools.combinations(self.domain.objects, 2))
		
		for action in self.actions:
			for i in possible_inputs:
				b1 = "self.domain." + i[0]
				b2 = "self.domain." + i[1]
				print(b1 + "  " + b2)
				funcstr = f'self.domain.{action}({b1}, {b2})'
				try:
					print("Calling: " + str(funcstr))
					eval(funcstr)
				except customerrors.PredicateFailed as e:
					print(e)
				print("SUCCESS: " + funcstr)

		# for obj in self.domain.objects:
				# blocks = self.pickRandomBlocks()
				# b1 = blocks[0]
				# b2 = blocks[1]
				# funcstr = f'self.domain.{action}({b1}, {b2})'
				# try:
				# 	print("Calling: " + str(funcstr))
				# 	eval(funcstr)
				# except customerrors.PredicateFailed as e:
				# 	print(e)

