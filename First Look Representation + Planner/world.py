import customerrors as err
import planner
from abc import ABC, abstractmethod

def getType(obj):
		return type(obj).__name__

def checkType(obj, expected):
	objType = getType(obj)
	if objType != expected:
		raise err.WrongInputType(objType, expected)

def checkPredicateTrue(lambd, obj):
	if not(lambd(obj)):
		raise err.PredicateFailed()

#Abstract action class
class Action(ABC):
	def __init__(self, domain, name):
		self.domain = domain
		self.domain.actions.append(name)

	@abstractmethod
	def checkPredicates(self):
		pass

	@abstractmethod
	def doAction(self):
		pass

	@abstractmethod
	def checkTypes(self):
		pass

class stack(Action):
	def __init__(self, domain, name = "stack"):
		super().__init__(domain, name)

	def checkTypes(self, b1, b2):
		checkType(b1, "Block")
		checkType(b2, "Block")

	def checkPredicates(self, b1, b2):
		#Predicates, maybe should move them
		stacked = (lambda x: x.stacked)
		notstacked = (lambda x: not(x.stacked))
		top = (lambda x: x.top)
		stackable = (lambda x: x.stackable)

		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(notstacked, b2)
		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(top, b1)
		checkPredicateTrue(stackable, b1)

	def doAction(self, b1, b2):
		b1.top = False
		b2.top = True
		b2.stacked = True
		self.domain.total_weight += b2.weight

class unstack(Action):
	def __init__(self, domain, name = "unstack"):
		super().__init__(domain, name)

	def checkTypes(self, b1, b2):
		checkType(b1, "Block")
		checkType(b2, "Block")

	def checkPredicates(self, b1, b2):
		stacked = (lambda x: x.stacked)
		top = (lambda x: x.top)

		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(stacked, b2)
		checkPredicateTrue(top, b2)

	def doAction(self, b1, b2):
		b2.stacked = False
		b2.top = False
		b1.top = True
		self.domain.total_weight -= b2.weight

class BlockTower():
	def __init__(self):
		#Initialize a,b,c
		#Define the goal
		self.a = Block("a", False, 1)
		self.b = Block("b",True, 1)
		self.c = Block("c",True, 3)
		self.floor = Block("floor", True, 0, True, True)
		self.objects = ["a", "b", "c", "floor"]
		self.total_weight = 0
		self.actions = []
		self.stack = stack(self)
		self.unstack = unstack(self)

	# def print_state(self):
	# 	# print(self.total_weight)
	# 	for x in self.objects:
	# 		print(str(x))

class Block():
	def __init__(self, name, stackable, weight, stacked = False, top = False):
		self.name = name
		self.stacked = stacked
		self.top = top
		self.stackable = stackable
		self.weight = weight

	def __str__(self):
		return "Block " + str(self.name) + "\nStacked: " + str(self.stacked) + " Top: " + str(self.top) + " Stackable: " + str(self.stackable) + " Weight: " + str(self.weight)

if __name__ == "__main__":
	domain = BlockTower()
	planner.Planner(domain)
