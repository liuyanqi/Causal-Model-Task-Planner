from abc import ABC, abstractmethod
import itertools
import customerrors

class Domain():
	def __init__(self, state):
		#Is a list of action classes that are possible
		self.actions = []
		#Stores a current state object
		self.state = state

	def getValidActions(self, state):
		actions = []
		possible_inputs = list(itertools.combinations(state.obj_names, 2))
		for i in range(len(possible_inputs)):
			possible_inputs.append(possible_inputs[i][::-1])
	
		for action in self.actions:
			for i in possible_inputs:
				b1 = i[0]
				b2 = i[1]
				try:
					action.checkPredicates(state, b1, b2)
				except customerrors.PredicateFailed as e:
					continue
				actions.append(SpecificAction(action, [b1,b2], state))
		return actions


# This superclass maintains a list of objects and their names in a domain state
class State(ABC):
	def __init__(self):
		self.obj_dict = {}
		self.obj_names = []
		self.objects = []

	def addObject(self, obj):
		self.obj_dict[obj.name] = obj
		self.obj_names = list(self.obj_dict.keys())
		self.objects = list(self.obj_dict.values())

	def get(self, name):
		return self.obj_dict[name]

	@abstractmethod
	def isGoalSatisfied(self):
		pass

#Abstract action class
#This ensures that an action follows the correct function pattern
#and has its names stored correctly for enumeration by the planner
class Action(ABC):
	def __init__(self, domain, name):
		self.domain = domain
		self.domain.actions.append(self)
		self.name = name

	@abstractmethod
	def checkPredicates(self, state):
		pass

	@abstractmethod
	def doAction(self, state):
		pass

	@abstractmethod
	def checkTypes(self, state):
		pass

class SpecificAction():
	def __init__(self, action, parameters, state):
		self.action = action
		self.parameters = parameters
		self.state = state

	def __str__(self):
		return str(self.action.name) + " (" + str(self.parameters) + ")"

