import customerrors as err
from abstracttypes import Action, Domain, State, getType, checkPredicateTrue, checkParams, SpecificAction
import random
from visualmodel import BlockVisualModel
from copy import deepcopy

class stack(Action):
	def __init__(self, domain):
		super().__init__(domain)
		self.param_types = ["Block", "Block"]

	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		b1 = state.get(b1_name)
		b2 = state.get(b2_name)
		specific_action = SpecificAction(self, [b1_name, b2_name], deepcopy(state))

		predicates = self.domain.causal_models[type(specific_action.action).__name__].runModel(specific_action)

		#top basically means clear
		#stacked means
		#Yeah wait with unstack gonna need to change the predicates
		#Stack a on b. Unstack a, now cant stack b on anything because b.stacked is true

		#So you can stack anything that is clear on top of anything that is clear??
		#I think so

		#Predicates, maybe should move them
		# stacked = (lambda x: x.stacked)
		# notstacked = (lambda x: not(x.stacked))
		# top = (lambda x: x.top)
		clear = (lambda x: x.clear)

		checkPredicateTrue(clear, b1)
		checkPredicateTrue(clear, b2)
		if predicates["stackable"]==False:
			raise err.PredicateFailed()


		#Only one tower allowed
		if not(state.no_placement_yet):
			#Check that b1.on != None
			if b1.on == "floor":
				raise err.PredicateFailed("Can only make one tower")

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

		#Normal
		# if state.visual.getStackability(b1_name, b2_name) < 0.3:
		# # if state.visual.getStackability(b1_name, b2_name) < 0.476:
		# 	raise err.PredicateFailed("Not stackable enough!")



	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		# self.checkPredicates(state, [b1_name, b2_name])

		b1 = state.get(b1_name)
		b2 = state.get(b2_name)

		# Multi tower enabled
		if b1.on == "floor":
			state.total_weight += b1.weight
			state.total_height += b1.height
			# Single tower
			state.no_placement_yet = False

		# b1.top = False
		# b2.top = True
		# b2.stacked = True
		# b1.stacked = True
		# b2.on = b1_name
		# state.total_weight += b2.weight
		# state.total_height += b2.height

		b1.clear = False
		b2.clear = True
		b2.on = b1_name
		state.total_weight += b2.weight
		state.total_height += b2.height

class unstack(Action):
	def __init__(self, domain):
		super().__init__(domain)
		self.param_types = ["Block"]

	@checkParams
	def checkPredicates(self, state, b1_name: str):
		b1 = state.get(b1_name)

		# stacked = (lambda x: x.stacked)
		# top = (lambda x: x.top)
		clear = (lambda x: x.clear)

		if b1.on == "floor":
			raise err.PredicateFailed("Can't unstack if on floor already")

		checkPredicateTrue(clear, b1)


	@checkParams
	def doAction(self, state, b1_name: str):
		b1 = state.get(b1_name)
		b2_name = b1.on
		b2 = state.get(b2_name)

		b1.clear = True
		b2.clear = True
		b1.on = "floor"

		if b2.on == "floor":
			state.no_placement_yet = True
			state.total_weight -= b2.weight
			state.total_height -= b2.height

		state.total_weight -= b1.weight
		state.total_height -= b1.height


class BlockTowerState(State):
	def __init__(self):
		super().__init__()
		# #Normal
		self.addObject(Block("a", 3, 3, "triangle"))
		self.addObject(Block("b", 1, 2, "square"))
		self.addObject(Block("c", 3, 4, "square"))
		self.addObject(Block("d", 1, 3, "square"))

		BlockVisualModel().initState(self)

		# T1
		# self.addObject(Block("a", 3, 0))
		# self.addObject(Block("b", 3, 0))
		# self.addObject(Block("c", 3, 0))
		# self.addObject(Block("d", 2, 0))
		# self.addObject(Block("e", 4, 0))
		# self.addObject(Block("f", 3, 0))
		# self.addObject(Block("g", 3, 0))
		# self.addObject(Block("h", 3, 0))
		# self.addObject(Block("i", 3, 0))
		# self.addObject(Block("j", 3, 0))
		# self.addObject(Block("k", 3, 0))
		# self.addObject(Block("l", 3, 0))
		# self.addObject(Block("m", 3, 0))
		# self.addObject(Block("n", 3, 0))
		# self.addObject(Block("o", 3, 0))
		# self.addObject(Block("p", 3, 0))


		self.total_weight = 0
		self.total_height = 0
		self.no_placement_yet = True

	def __eq__(self, other):
		if other == None:
			return False


		for objname in self.obj_names:
			if self.get(objname) == other.get(objname):
				pass
			else:
				return False

		return self.total_weight == other.total_weight


	def __str__(self):
		ret = "Weight: " + str(self.total_weight) + "\n"
		ret  += "no place yet: " + str(self.no_placement_yet) + " \n"

		for x in self.objects:
			ret += str(x)
		return ret

	def getShapeDict(self):
		shapedict = {}
		stackarr = self.obj_types["Block"]

		#stackarr get shapes
		for name in stackarr:
			shapedict[name] = self.get(name).shape

		return shapedict

		#T1
		# return self.total_weight > 8

class BlockTower(Domain):
	def __init__(self):
		super().__init__(BlockTowerState())
		self.stack = stack(self)
		self.goal = Goal(weight=5, height=9)

		# self.unstack = unstack(self)
	def isGoalSatisfied(self, state):
		return self.goal.isSatisfied(state)

class Block():
	def __init__(self, name, weight, height, shape, clear = True):
		self.name = name
		self.clear = clear
		self.weight = weight
		self.on = "floor"
		self.height = height
		self.shape = shape

	def __str__(self):
		return "(" + self.name + ") " + "Clear: " + str(self.clear) + " On: " + str(self.on) + " Weight: " + str(self.weight) + "\n"

	def __eq__(self, other):
		return (((self.on == other.on)
		and self.clear == other.clear)
		and self.weight == other.weight)

class Goal():
	def __init__(self, weight=None, height=None):
		self.weight = weight
		self.height = height

	def isSatisfied(self, state):
		w = False
		h = False

		if self.weight != None:
			if state.total_weight >= self.weight:
				w = True
		else:
			w = True

		if self.height != None:
			if state.total_height >= self.height:
				h = True
		else:
			h = True
		return (h and w)
