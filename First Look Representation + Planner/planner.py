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

	@staticmethod
	def printHistory(histarr):
		ret = []
		for h in histarr:
			print(str(h))

		return ret

	@staticmethod
	def strHistoryMoves(histarr):
		ret = []
		for h in histarr:
			if h.action != None:
				print(str(h.action.name) + " " +str(h.parameters))

		return ret


	def planCausal(self):
		
		def checkBacktrack(curr_node):
			#OK wait this should go back to previous state
			#Something is messed up here

			# print("In backtrack")
			# print("Curr state:")
			# print(curr_node.specifiedaction.state)
			# print("Current history: ")
			Planner.strHistory(curr_node.history)
			next_actions = self.domain.getValidActions(curr_node.specifiedaction.state)
			# print("Next possible actions: ")
			# print(Planner.printHistory(next_actions))
			if len(next_actions) == 0:
				print("GOT STUCK!")
				#We are stuck
				#Remove the current action from history
				#Update the action
				curr_node.specifiedaction.state = deepcopy(curr_node.history[-2].state)
				curr_node.specifiedaction.action = deepcopy(curr_node.history[-2].action)
				curr_node.history.pop()
				return checkBacktrack(curr_node)

			return next_actions



		#Initialization
		print("Initializing Causal planner....")
		#A node is an action and a state tuple
		#(action, state)

		#In order to get out of dead end states, should just be able to traverse
		#back up the history chain??

		#Deepcopy so dont mutate passed in state
		valid_actions = self.domain.getValidActions(self.domain.state)
		if len(valid_actions) == 0:
			print("ERROR: No possible actions from initial state!")
			exit(0)

		
		curr_action = CausalModel.chooseNextAction(valid_actions)
		#Deep copy because if backtrack to initial state, don't want to manipulate states
		first_specified_action = deepcopy(curr_action)
		first_specified_action.action = None

		curr_node = self.Node(curr_action, [first_specified_action])

		while not(curr_node.specifiedaction.state.isGoalSatisfied()):
			# print(curr_node)
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction

			# print("STATE BEFORE")
			print("ACTION: " + str(action))
			action.action.doAction(action.state, action.parameters[0], action.parameters[1])
			# print("STATE AFTER")
			# print(action.state)
			curr_node.history.append(deepcopy(action))

			#Update current node
			next_actions = checkBacktrack(curr_node)

			curr_node.specifiedaction = CausalModel.chooseNextAction(next_actions)

		print("Final plan:")	
		print(Planner.strHistoryMoves(curr_node.history))
		print("DONE")
		return curr_node.history

