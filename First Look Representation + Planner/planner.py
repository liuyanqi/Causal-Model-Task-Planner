import inspect
import world
import customerrors
import itertools

class Planner():
	def __init__(self, domain):
		self.domain = domain
		self.getValidActions()

		# self.domain.stack.doAction(self.domain.floor, self.domain.a)
		# print("----------------------")
		# self.getValidActions()

		self.domain.stack.doAction(self.domain.floor, self.domain.b)
		print("----------------------")
		self.getValidActions()

	def getValidActions(self):
		#Generate all possible inputs
		possible_inputs = list(itertools.combinations(self.domain.objects, 2))
		for i in range(len(possible_inputs)):
			possible_inputs.append(possible_inputs[i][::-1])
		
		for action in self.domain.actions:
			print("NEW ACTION!")
			print(action)
			for i in possible_inputs:
				b1 = "self.domain." + i[0]
				b2 = "self.domain." + i[1]
				funcstr = f'self.domain.{action}.checkPredicates({b1}, {b2})'
				try:
					eval(funcstr)
				except customerrors.PredicateFailed as e:
					# print(e)
					continue
				print("SUCCESS: " + funcstr)

