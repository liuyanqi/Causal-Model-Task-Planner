from abstracttypes import Action, Domain, State, getType, checkPredicateTrue
from blockworld import checkParams
import customerrors as err
from copy import deepcopy

#This entire state representation is messed
#This doesn't work as required yet


"""
Atually not sure how no params is gonna go...
"""

class RiverState(State):
	def __init__(self):
		super().__init__()
		self.addObject(Item("wolf"))
		self.addObject(Item("sheep"))
		self.addObject(Item("cabbage"))
		self.addObject(Boat("Boat"))
		# self.addObject(Rocket("Rocket"))

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

	# def __eq__(self, other):
		#TO IMPLEMENT

class Item():
	def __init__(self, name):
		self.name = name
		self.left = True
		self.eaten = False

	def __str__(self):
		return self.name + " \n Left: " + str(self.left) + "\n Eaten: " + str(self.eaten)

class Boat():
	def __init__(self, name):
		self.name = name
		self.left = True
		self.inside = None

	def __str__(self):
		return self.name + "\n Left: " + str(self.left) + "\n Inside: " + str(self.inside)

class Rocket():
	def __init__(self, name):
		self.name = name
		self.left = True

	def __str__(self):
		return "Rocket Left: " + str(self.left)

class cross(Action):
	def __init__(self, state, name = "cross"):
		super().__init__(state, name)
		self.param_types = ["Boat"]

	@staticmethod
	def _get_obj_sides(state):
		sides = {}

		for obj in state.obj_types["Item"]:
			try:
				sides[state.get(obj).left].append(state.get(obj).name)
			except KeyError as e:
				#We have no record of that type yet
				sides[state.get(obj).left] = [state.get(obj).name]

		return sides


	@checkParams
	def checkPredicates(self, state, b_name: str):
		#There are no predicates to having the boat cross the river
		test_state = deepcopy(state)

		#First move the items over
		if test_state.get("Boat").inside != None:
			state.get(test_state.get("Boat").inside).left = not(state.get(test_state.get("Boat").inside).left)

		#The eating checking happens here
		for s in self._get_obj_sides(state).values():
			if ("wolf" in s and "sheep" in s):
				raise err.PredicateFailed()

			elif ("sheep" in s and "cabbage" in s):
				raise err.PredicateFailed()



		pass

	@checkParams
	def doAction(self, state, b_name: str):
		boat = state.get(b_name)

		#First move the items over
		if boat.inside != None:
			state.get(boat.inside).left = not(state.get(boat.inside).left)

		#The only effect on the Boat that occurs is that it's .left param is switched
		boat.left = not(boat.left)

		#The eating checking happens here
		for s in self._get_obj_sides(state).values():

			if ("wolf" in s and "sheep" in s):
				state.get("sheep").eaten = True

			elif ("sheep" in s and "cabbage" in s):
				state.get("cabbage").eaten = True


class load(Action):
	def __init__(self, state, name="load"):
		super().__init__(state, name)
		self.param_types = ["Item"]
	
	@checkParams
	def checkPredicates(self, state, i_name: str):
		#Check that the item and the boat are on the same side of the river
		#Also check that the boat isn't already full
		item = state.get(i_name)

		if state.get("Boat").inside != None:
			raise err.PredicateFailed("Boat already full")

		if state.get("Boat").left != item.left:
			raise err.PredicateFailed("Boat and item on different sides")


	@checkParams
	def doAction(self, state, i_name: str):
		state.get("Boat").inside = i_name

class unload(Action):
	def __init__(self, state, name="unload"):
		super().__init__(state, name)
		self.param_types = []
	
	@checkParams
	def checkPredicates(self, state):

		if state.get("Boat").inside == None:
			raise err.PredicateFailed("Boat empty")


	@checkParams
	def doAction(self, state):
		#Set the .left of the item to be the same as the current of the boat
		item = state.get(state.get("Boat").inside)

		item.left = state.get("Boat").left
		

class launch(Action):
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
		self.cross = cross(self)
		# self.launch = launch(self)
		self.load = load(self)
		self.unload = unload(self)

