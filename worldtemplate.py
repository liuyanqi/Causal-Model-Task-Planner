#This is the outline for an example Action
#It is a subclass of the Action class in abstracttypes.py
class testAction(Action):
	def __init__(self, domain):
		#Supering the domain attaches this action to the domain and allows the
		#planner to enumerate possible actions on the domain
		super().__init__(domain)
		#The paramtypes array denotes the number of parameters an action takes and the types that each of the parameters should be
		#This is then used later for type checking and enumerating valid moves
		self.param_types = ["Type1", "Type2"]


	#This decorator wrapper automatically checks the types of the objects input to a specific action
	#It also unpacks checkPredicates(self, state, [obj1, obj2]) to checkPredicates(self, state, obj1, obj2)
	#After the object pass the type checks


	#The objects to perform the function on are passed in via their names as strings
	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		#This function returns nothing if the predicates for the action are valid
		#It throws a custom error PredicateFailed if the predicates are invalid

	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		#This function alters the passed in state with the result of the action


#This class is a subclass of the State class
#It contains all information about the world state including global variables like totalweight
#As well as the current state of every object in the domain
class testDomainState(State):
	def __init__(self):
		super().__init__()
		#This method addObject is used to add an object to a state
		self.addObject(ExampleObj(0,1,2))

	#This function returns true when the world state satisfies the goal
	def isGoalSatisfied(self):
		return True

#This class is a subclass of the Domain class
#It contains all of the possible actions of a problem and the current state of the domain 
class testDomain(Domain):
	def __init__(self):
		#We first super the Domain Specific state object
		super().__init__(testDomainState())

		#This attaches the action to the domain so one could call domain.testAction.doAction manually
		#It is not nessecary to enumerate through actions in the planner it is just for convenience
		self.testAction = testAction(self)