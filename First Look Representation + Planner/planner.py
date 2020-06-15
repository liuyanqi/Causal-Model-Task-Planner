import inspect
import world
import customerrors
import itertools
from copy import deepcopy
import random
from causalmodel import CausalModel 

class Planner():
	class Node():
		def __init__(self, specifiedaction, history):
			self.specifiedaction = specifiedaction
			self.history = history

		def __str__(self):
			return "Action: " + str(self.specifiedaction) + " History: " + str(Planner.strHistory(self.history))

	def __init__(self, domain):
		self.domain = domain

	def planBFS(self):
		def addNodes(state, history):
			for specifiedaction in self.domain.getValidActions(state):
				next_nodes.append(self.Node(deepcopy(specifiedaction), deepcopy(history)))

		#Initialization
		print("Initializing BFS planner....")
		#A node is an action and a state tuple
		#(action, state)

		#This stores all actions the BFS should go through
		#Can use it as a queue, just append,then pop(0)
		next_nodes = []
		#Add all current possible actions to BFS
		addNodes(self.domain.state, [])

		curr_node = next_nodes.pop(0)

		while not(curr_node.specifiedaction.state.isGoalSatisfied()):
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction
			curr_history = curr_node.history

			action.action.doAction(action.state, action.parameters[0], action.parameters[1])

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)
			addNodes(action.state, curr_history)

			curr_node = next_nodes.pop(0)

		return curr_node.history

	@staticmethod
	def strHistory(histarr):
		ret = []
		for h in histarr:
			ret.append(str(h))

		return ret


	def planCausal(self):
		#Initialization
		print("Initializing Causal planner....")
		#A node is an action and a state tuple
		#(action, state)

		#In order to get out of dead end states, should just be able to traverse
		#back up the history chain??

		#Deepcopy so dont mutate passed in state
		curr_node = self.Node(deepcopy(CausalModel.chooseNextAction(self.domain.getValidActions(self.domain.state))), [])

		while not(curr_node.specifiedaction.state.isGoalSatisfied()):
			print(curr_node)
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction
			curr_history = curr_node.history

			action.action.doAction(action.state, action.parameters[0], action.parameters[1])

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)

			#Update current node
			curr_node.history = curr_history
			curr_node.specifiedaction = CausalModel.chooseNextAction(self.domain.getValidActions(action.state))

		print("Final plan:")	
		print(Planner.strHistory(curr_node.history))
		return curr_node.history

