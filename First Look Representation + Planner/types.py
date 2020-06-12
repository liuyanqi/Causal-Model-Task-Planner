class Domain(ABC):
	def __init__():
		self.actions = []

	@abstractmethod
	def isGoalSatisfied():
		pass

class State():
	def __init__(self):
		self.obj_names = []
		self.objs = []

	def addObject(self, obj, name):
		self.objs.append(obj)
		self.obj_names.append(name)

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