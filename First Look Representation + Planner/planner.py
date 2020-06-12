import inspect
import world
import customerrors
import itertools
from copy import deepcopy
import random

class Planner():
	def __init__(self, domain):
		self.domain = domain

	def plan(self):
		def addNodes(state):
			for action in self.domain.getValidActions(state):
				next_nodes.append((action, deepcopy(state)))

		#Initialization
		print("Initializing planner....")
		#A node is an action and a state tuple
		#(action, state)

		#This stores all actions the BFS should go through
		#Can use it as a queue, just append,then pop(0)
		next_nodes = []
		#Add all current possible actions to BFS
		addNodes(self.domain.state)
		print("Current nodes array: ")
		print(next_nodes)

		curr_node = next_nodes.pop(0)

		while not(curr_node[1].isGoalSatisfied()):
			# print("Currently at node:")
			# print(curr_node)
			# print(type(curr_node))

			# if (curr_node in seen):
			# 	#We have already been at this state and done this action
			# 	#Exit to avoid an infinite loop
			# 	print("We have seen this node before, stopping")
			# 	continue
			# #Add the current node to the seen set
			# seen.add(curr_node)

			#Unpack the node into action and parameters
			curr_action_arr = curr_node[0]
			curr_act_func = curr_action_arr[0]
			curr_p1 = curr_action_arr[2]
			curr_p2 = curr_action_arr[3]
			curr_state = curr_node[1]

			# print("Action: ")
			# print(curr_act_func)
			# print("PRE State: ")
			# print(curr_state)

			print(curr_act_func.name + " " + curr_p1 + " " + curr_p2)

			curr_act_func.doAction(curr_state, curr_p1, curr_p2)

			# print("POST State: ")
			# print(curr_state)

			#Here is where I would have the causal step

			#Now find all the next possible actions and add them to the actions list
			addNodes(curr_state)

			curr_node = next_nodes.pop(0)


