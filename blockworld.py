import customerrors as err
from abstracttypes import Action, Domain, State, getType, checkPredicateTrue, checkParams
import random

class stack(Action):
	def __init__(self, state, name = "stack"):
		super().__init__(state, name)
		self.param_types = ["Block", "Block"]

	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		#Predicates, maybe should move them
		# stacked = (lambda x: x.stacked)
		notstacked = (lambda x: not(x.stacked))
		top = (lambda x: x.top)

		checkPredicateTrue(top, b1)
		checkPredicateTrue(notstacked, b2)

		if b1_name == b2_name:
			raise err.PredicateFailed("Can't stack block on self")


		# Non deterministic stacking
		# print("[" + b1_name + ", " + b2_name + "]")
		# print("Probability of stacking: " + str(state.visual.flatness_vals[b1_name]))
		# if random.random() > state.visual.flatness_vals[b1_name]:
		# 	#Stack should fail
		# 	print("Stacking failed")
		# 	raise err.PredicateFailed("Not stackable enough!")
		# print("Stacking succeeded")

		if state.visual.getStackability(b1_name, b2_name) < 0.3:
			print("Not stackable enough")
			raise err.PredicateFailed("Not stackable enough!")



	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		# self.checkPredicates(state, [b1_name, b2_name])

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		if b1.on == None:
			b1.on = "floor"
			state.total_weight += b1.weight
			state.total_height += b1.height

		b1.top = False
		b2.top = True
		b2.stacked = True
		b1.stacked = True
		b2.on = b1_name
		state.total_weight += b2.weight
		state.total_height += b2.height

class unstack(Action):
	def __init__(self, domain, name = "unstack"):
		super().__init__(domain, name)
		self.param_types = ["Block", "Block"]

	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		stacked = (lambda x: x.stacked)
		top = (lambda x: x.top)
		on = (lambda x, y: x.on == y.name)

		if not on(b2, b1):
			raise err.PredicateFailed()

		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(stacked, b2)
		checkPredicateTrue(top, b2)


	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		self.checkPredicates(state, [b1_name, b2_name])

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		b2.stacked = False
		b2.top = False
		b1.top = True
		b2.on = None
		state.total_weight -= b2.weight


class BlockTowerState(State):
	def __init__(self):
		super().__init__()
		self.addObject(Block("a", 1, 1))
		self.addObject(Block("b", 1, 2))
		self.addObject(Block("c", 3, 2))
		self.total_weight = 0
		self.total_height = 0

	def __eq__(self, other):
		for objname in self.objname:
			if self.get(objname) == other.get(objname):
				pass
			else:
				return False

		return self.total_weight == other.total_weight


	def __str__(self):
		ret = "Weight: " + str(self.total_weight) + "\n"
		
		for x in self.objects:
			ret += str(x)
		return ret

	def isGoalSatisfied(self):
		return self.total_weight > 4

class BlockTower(Domain):
	def __init__(self):
		super().__init__(BlockTowerState())
		self.stack = stack(self)
		# self.unstack = unstack(self) 

class Block():
	def __init__(self, name, weight, height, stacked = False, top = True):
		self.name = name
		self.stacked = stacked
		self.top = top
		self.weight = weight
		self.on = None
		self.height = height

	def __str__(self):
		return "(" + self.name + ") " + "Stacked: " + str(self.stacked) + " Top: " + str(self.top) + " On: " + str(self.on) + " Weight: " + str(self.weight) + "\n"

	def __eq__(self, other):
		return (((self.stacked == other.stacked) 
		and self.top == other.top)
		and self.weight == other.weight)

class Goal():
	def __init__(self, weight=None, height=None):
		self.weight = weight
		self.height = height

	def isSatisfied(self, state):
		w = False
		h = False

		if self.weight != None:
			if state.total_weight > self.weight:
				w = True
		else:
			w = True

		if self.height != None:
			if state.total_height > self.height:
				h = True
		else:
			h = True

		return (h and w)




