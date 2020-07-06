from abc import ABC, abstractmethod
import itertools
import customerrors
from copy import deepcopy

class Domain():
	def __init__(self, state):
		#Is a list of action classes that are possible
		self.actions = []
		#Stores a current state object
		self.state = state

	def getValidActions(self, state):
		actions = []

		#Loop through all the possible actions of the domain
		for a in self.actions:
			list_to_product = []

			#This is making a list of lists of objects that are valid for each parameter
			for param in a.param_types:
				list_to_product.append(state.obj_types[param])

			#Now we have a list of parameters that meet the specified type
			type_valid_params = list(itertools.product(*list_to_product))

			for params in type_valid_params:
				#Now we have to check that the type correct parameters
				#satisfy the predicates before we can consider the action valid
				try:
					a.checkPredicates(state, list(params))
				except customerrors.PredicateFailed as e:
					continue

				#Create a new specific action with the parameters and state
				#Add it to the possible actions list
				actions.append(SpecificAction(a, list(params), deepcopy(state)))

		return actions


# This superclass maintains a list of objects and their names in a domain state
class State(ABC):
	def __init__(self):
		self.obj_dict = {}
		self.obj_names = []
		self.objects = []
		self.obj_types = {}

	def addObject(self, obj):
		self.obj_dict[obj.name] = obj
		self.obj_names = list(self.obj_dict.keys())
		self.objects = list(self.obj_dict.values())
		obj_type = type(obj).__name__

		try:
			self.obj_types[obj_type].append(obj.name)
		except KeyError as e:
			#We have no record of that type yet
			self.obj_types[obj_type] = [obj.name]

	def get(self, name):
		return self.obj_dict[name]

	@abstractmethod
	def isGoalSatisfied(self):
		pass

	# def __eq__(self, obj):
	# 	for o in self.objects:
	# 		if o != obj:
	# 			return False
	# 	return True

#Abstract action class
#This ensures that an action follows the correct function pattern
#and has its names stored correctly for enumeration by the planner
class Action(ABC):
	def __init__(self, domain):
		self.domain = domain
		self.domain.actions.append(self)

	@abstractmethod
	def checkPredicates(self, state):
		pass

	@abstractmethod
	def doAction(self, state):
		pass

class SpecificAction():
	def __init__(self, action, parameters, state):
		self.action = action
		self.parameters = parameters
		self.state = state

	def __str__(self):
		if self.action == None:
			return "None"
		else:
			return str(self.action.name) + " " + str(self.parameters) #+ str(self.state) 

	def __eq__(self, obj):
		return (self.parameters == obj.parameters and self.state == obj.state)

def getType(obj):
		return type(obj).__name__

def checkType(obj, expected):
	objType = getType(obj)
	if objType != expected:
		raise customerrors.WrongInputType(objType, expected)

def checkPredicateTrue(lambd, obj):
	if not(lambd(obj)):
		raise customerrors.PredicateFailed()

def checkParams(func):
	def func_wrapper(self, state, params):
		if len(params) != len(self.param_types):
			raise ValueError("Wrong number of parameters")

		objs = []
		for p in params:
			objs.append(state.get(p))

		for x in range(len(params)):
			correct_type = self.param_types[x]
			passed_type = getType(objs[x])
			if type(correct_type).__name__ != "list":
				#If the type parameter is just a single object
				if correct_type != passed_type:
					raise ValueError("Wrong parameter type. Param number: " + str(x) + " Expected: " + correct_type + " Found: " + passed_type)
			else:
				#If there are multiple valid types that an action can be applied to
				if passed_type not in correct_type:
					raise ValueError("Wrong parameter type. Param number: " + str(x) + " Expected: " + str(correct_type) + " Found: " + passed_type)


		return func(*([self, state] + params))
	return func_wrapper
