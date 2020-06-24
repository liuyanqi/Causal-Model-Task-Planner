from abstracttypes import Action, Domain, State, getType, checkPredicateTrue
from blockworld import checkParams
import customerrors

#This entire state representation is messed
#This doesn't work as required yet

class RiverState(State):
	def __init__(self):
		super().__init__()
		self.addObject(Item("wolf"))
		self.addObject(Item("sheep"))
		self.addObject(Item("cabbage"))
		self.addObject(Rocket("Rocket"))

	def __str__(self):
		ret = ""
		for x in self.objects:
			ret += str(x) + "\n"
		return ret

	def isGoalSatisfied(self):
		for obj in self.objects:
			if obj.left:
				return False

		for item in self.obj_types["Item"]:
			if self.get(item).eaten:
				return False

		return True

class Item():
	def __init__(self, name):
		self.name = name
		self.left = True
		self.eaten = False

	def __str__(self):
		return self.name + " Left: " + str(self.left)

class Rocket():
	def __init__(self, name):
		self.name = name
		self.left = True

	def __str__(self):
		return "Rocket Left: " + str(self.left)

class Cross(Action):
	def __init__(self, state, name = "cross"):
		super().__init__(state, name)
		self.param_types = ["Item", "Item"]

	@checkParams
	def checkPredicates(self, state, i1_name: str, i2_name: str):
		i1 = state.get(i1_name)
		i2 = state.get(i2_name)

		#Predicates, maybe should move them
		onleft = (lambda x: x.left)
		
		checkPredicateTrue(onleft, i1)
		checkPredicateTrue(onleft, i2)

		if i1_name == i2_name:
			raise customerrors.PredicateFailed()
		

	@checkParams
	def doAction(self, state, i1_name: str, i2_name: str):
		i1 = state.get(i1_name)
		i2 = state.get(i2_name)

		if (i1_name == "wolf" and i2_name == "sheep"):
			i2.eaten = True

		elif (i1_name == "sheep" and i2_name == "wolf"):
			i1.eaten = True

		elif (i1_name == "sheep" and i2_name == "cabbage"):
			i2.eaten = True

		elif (i1_name == "cabbage" and i2_name == "sheep"):
			i1.eaten = True

		i1.left = False
		i2.left = False

class Launch(Action):
	def __init__(self, state, name = "launch"):
		super().__init__(state, name)
		self.param_types = ["Rocket"]

	@checkParams
	def checkPredicates(self, state, rname: str):
		r = state.get(rname)

		#Predicates, maybe should move them
		onleft = (lambda x: x.left)
		
		checkPredicateTrue(onleft, r)
		

	@checkParams
	def doAction(self, state, rname: str):
		r = state.get(rname)

		r.left = False

class RiverWorld(Domain):
	def __init__(self):
		super().__init__(RiverState())
		self.cross = Cross(self)
		self.launch = Launch(self)

