class testAction(Action):
	def __init__(self, domain):
		super().__init__(domain)
		self.param_types = ["Type1", "Type2"]

	@checkParams
	def checkPredicates(self, state, b1_name: str, b2_name: str):
		

	@checkParams
	def doAction(self, state, b1_name: str, b2_name: str):
		


# #This class is a subclass of the State class
# #It contains all information about the world state including global variables like totalweight
# #As well as the current state of every object in the domain
# class testDomainState(State):
# 	def __init__(self):
# 		super().__init__()
# 		#This method addObject is used to add an object to a state
# 		self.addObject(ExampleObj(0,1,2))

# 	#This function returns true when the world state satisfies the goal
# 	def isGoalSatisfied(self):
# 		return True

# #This class is a subclass of the Domain class
# #It contains all of the possible actions of a problem and the current state of the domain 
# class testDomain(Domain):
# 	def __init__(self):
# 		#We first super the Domain Specific state object
# 		super().__init__(testDomainState())

# 		#This attaches the action to the domain so one could call domain.testAction.doAction manually
# 		#It is not nessecary to enumerate through actions in the planner it is just for convenience
# 		self.testAction = testAction(self)