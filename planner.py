import inspect
# import world
import customerrors
import itertools
from copy import deepcopy
import random
from causalmodel import CausalModel 
from abstracttypes import SpecificAction


class Planner():
	class Node():
		def __init__(self, specifiedaction, history):
			self.specifiedaction = specifiedaction
			self.history = history

		def __str__(self):
			return "Action: " + str(self.specifiedaction) + " History: " + str(self.history)

	def __init__(self, domain):
		self.domain = domain
	
	def setAlgo(self, algo):
		self.algo = algo

	def plan(self):
		if self.algo == None:
			raise TypeError("Need to set the planning algo first!")
		return self.algo()

	@staticmethod
	def BFS(self):
		nodes_touched = 0

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
			nodes_touched += 1
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction
			curr_history = curr_node.history

			action.action.doAction(action.state, action.parameters)

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)
			# Planner.printHistory(curr_history)
			addNodes(action.state, curr_history)

			curr_node = next_nodes.pop(0)

		print("Nodes touched: " + str(nodes_touched))

		return curr_node.history

	@staticmethod
	def printHistory(histarr):
		for h in histarr:
			if h.action != None:
				print(str(h.action.name) + " " +str(h.parameters))

	@staticmethod
	def Causal(self, chooseNextAction):
		#This function checks if the current state is a "dead end state" and no more actions can be taken
		#If that is the case, this function recursively backtracks until it finds a state that has valid actions
		#Then it returns those valid actions
		def checkBacktrack(curr_node):
			print("CURRENT NODE")
			print(curr_node.specifiedaction.state)
			print(curr_node.specifiedaction.action)
			next_actions = self.domain.getValidActions(curr_node.specifiedaction.state)

			if (len(next_actions) == 0):# and not curr_node.specifiedaction.state.isGoalSatisfied()):
				print("GOT STUCK!")
				#Update the action
				#Use deepcopy so that if need to backtrack later don't mess stuff up
				print("YYYY")
				print(curr_node.specifiedaction.state)
				curr_node.specifiedaction.state = deepcopy(curr_node.history[-2].state)
				print("YYYYYYYY")
				print(curr_node.specifiedaction.state)
				curr_node.specifiedaction.action = deepcopy(curr_node.history[-2].action)
				#Remove the current action from history
				print("XXX")
				print(len(curr_node.history))
				curr_node.history.pop()
				print("XXXXXXX")
				print(len(curr_node.history))
				return checkBacktrack(curr_node)

			return next_actions

		#Initialization
		print("Initializing Causal planner....")
		nodes_touched = 0

		#Get valid actions copies from a domain so don't need to worry about mutation
		valid_actions = self.domain.getValidActions(self.domain.state)

		#Sanity check
		if len(valid_actions) == 0:
			print("ERROR: No possible actions from initial state!")
			exit(0)

		#Pick first valid action
		curr_action = chooseNextAction(actionslist=valid_actions)

		#Deep copy because if backtrack to initial state, don't want to manipulate states
		#This special first action holds the first initial state before no action has been done
		#This is why its action type is none
		#Effectively each state stored w an action in the history is the state after an action has been applied
		first_specified_action = deepcopy(curr_action)
		first_specified_action.action = None

		#Place into node
		curr_node = self.Node(curr_action, [first_specified_action])

		#While the current state is not the goal state
		while not(curr_node.specifiedaction.state.isGoalSatisfied()):
			nodes_touched += 1
			action = curr_node.specifiedaction

			print("Action: " + str(action.action.name) + str(action.parameters))

			#Perform the perviously defined action
			print(action.parameters)
			action.action.doAction(action.state, action.parameters)
			print("State")
			print(action.state)


			#Record the action and resultant state in the history
			curr_node.history.append(deepcopy(action))

			#Update current node for next loop
			#Check for dead ends and find next actions
			next_actions = checkBacktrack(curr_node)
			curr_node.specifiedaction = chooseNextAction(next_actions)

		print("Nodes touched: " + str(nodes_touched))
		return curr_node.history


	@staticmethod
	def Causal2(self, pickBestAction):
		#Initialization
		nodes_touched = 0

		#Get valid actions copies from a domain so don't need to worry about mutation
		valid_actions = self.domain.getValidActions(self.domain.state)

		#Sanity check
		if len(valid_actions) == 0:
			print("ERROR: No possible actions from initial state!")
			exit(0)

		curr_action = SpecificAction(None, None, deepcopy(self.domain.state))

		#Deep copy because if backtrack to initial state, don't want to manipulate states
		#This special first action holds the first initial state before no action has been done
		#This is why its action type is none
		#Effectively each state stored w an action in the history is the state after an action has been applied
		first_specified_action = deepcopy(curr_action)
		first_specified_action.action = None

		#Place into node
		curr_node = self.Node(curr_action, [first_specified_action])

		#While the current state is not the goal state
		while not(curr_node.specifiedaction.state.isGoalSatisfied()):
	
			next_actions = self.domain.getValidActions(curr_node.specifiedaction.state)
			
			#We are at a "dead end" state
			if len(next_actions) == 0:
				print("Stuck... backtracking")
				#Want to revert state to a previous state, and try and
				#find some new actions
				curr_node.specifiedaction.state = deepcopy(curr_node.history[-2].state)
				curr_node.specifiedaction.action = deepcopy(curr_node.history[-2].action)
				curr_node.history.pop()
				#Restart and try and get new actions from beginning
				continue

			curr_node.specifiedaction = pickBestAction(next_actions)
			
			action = curr_node.specifiedaction

			#Perform the perviously defined action
			nodes_touched += 1
			action.action.doAction(action.state, action.parameters)
			print("-> Performed action: " + str(action.parameters))
			print("New state: ")
			print(action.state)

			#Record the action and resultant state in the history
			curr_node.history.append(deepcopy(action))
			

		print("Nodes touched: " + str(nodes_touched))
		return curr_node.history

