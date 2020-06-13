import inspect
import world
import customerrors
import itertools
from copy import deepcopy
import random
import causalmodel

class Planner():
	class Node():
		def __init__(self, specifiedaction, history):
			self.specifiedaction = specifiedaction
			self.history = history

	def __init__(self, domain):
		self.domain = domain

	def plan(self):
		def addNodes(state, history):
			for specifiedaction in self.domain.getValidActions(state):
				next_nodes.append(self.Node(deepcopy(specifiedaction), deepcopy(history)))

		#Initialization
		print("Initializing planner....")
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

			#Here is where I would have the causal step

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)
			addNodes(action.state, curr_history)

			curr_node = next_nodes.pop(0)

		# print("Success")
		# for step in curr_node.history:
		# 	print(step)
		return curr_node.history
		



