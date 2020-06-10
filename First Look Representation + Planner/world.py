import customerrors as err
import planner

def getType(obj):
		return type(obj).__name__

def checkType(obj, expected):
	objType = getType(obj)
	if objType != expected:
		raise err.WrongInputType(objType, expected)

def checkPredicateTrue(lambd, obj):
	if not(lambd(obj)):
		raise err.PredicateFailed()


class Domain():
	def __init__(self):
		#Initialize a,b,c
		#Define the goal
		self.a = Block("a", False, 1)
		print(type(self.a))
		self.b = Block("b",True, 1)
		self.c = Block("c",True, 3)
		self.floor = Block("floor", True, 0, True, True)
		self.objects = ["a", "b", "c", "floor"]

		self.total_weight = 0

	def a_stack(self, b1, b2):
		checkType(b1, "Block")
		checkType(b2, "Block")

		#Predicates, maybe should move them
		stacked = (lambda x: x.stacked)
		notstacked = (lambda x: not(x.stacked))
		top = (lambda x: x.top)

		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(notstacked, b2)
		checkPredicateTrue(stacked, b1)
		checkPredicateTrue(top, b1)

		#Effects
		b1.top = False
		b2.top = True
		b2.stacked = True
		self.total_weight += b2.weight


	# def a_unstack(self, b1, b2):
	# 	assert b1.stacked == True and b2.stacked == True and b2.top == True
	# 	b2.stacked = False
	# 	b2.top = False
	# 	b1.top = True
	# 	self.total_weight -= b2.weight

	def print_state(self):
		print(self.total_weight)
		for x in self.objects:
			print(str(x))


class Block():
	def __init__(self, name: str, stackable: bool, weight: int, stacked: bool = False, top: bool = False):
		self.name = name
		self.stacked = stacked
		self.top = top
		self.stackable = stackable
		self.weight = weight

	def __str__(self):
		return "Block " + str(self.name) + "\nStacked: " + str(self.stacked) + " Top: " + str(self.top) + " Stackable: " + str(self.stackable) + " Weight: " + str(self.weight)

if __name__ == "__main__":
	domain = Domain()
	planner.Planner(domain)
