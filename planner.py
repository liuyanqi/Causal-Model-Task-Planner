import inspect
import customerrors
import itertools
from copy import deepcopy
import random
from causalmodel import CausalModel 
from abstracttypes import SpecificAction
import time
import statistics


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
		return self.algo()[0]

	def collectStats(self, num_times):
		plans = {}
		nodes = []
		backtracks = []
		time = []

		for _ in range(num_times):
			res = self.algo()
			plan = tuple(map((lambda x: str(x)), res[0]))
			# print(plan)

			try:
				plans[plan] += 1
			except KeyError as e:
				#We have no record of that plan yet
				plans[plan] = 1



			nodes.append(res[1])
			backtracks.append(res[2])
			time.append(res[3])


		### Implement sorter of plans from most popular to least

		sorted_plans = {k: v for k, v in sorted(plans.items(), key=lambda item: item[1], reverse=True)}

		print()
		print("------- Statistics ------- (" + str(num_times) + " runs)")
		print("All plans: " + str(sorted_plans))
		print("Avg nodes touched: " + str(statistics.mean(nodes)))
		print("Avg backtracks: " + str(statistics.mean(backtracks)))
		print("Avg time: " + str(statistics.mean(time)))


	@staticmethod
	def BFS(self):
		debug = True
		start_time = time.time()
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

		curr_node = self.Node(SpecificAction(None, None, self.domain.state), [])

		while not(curr_node.specifiedaction.state.isGoalSatisfied()):
			curr_node = next_nodes.pop(0)

			if debug:
				print(type(curr_node.specifiedaction.action).__name__ + " " + str(curr_node.specifiedaction.parameters))
				print(curr_node.specifiedaction.state)

			nodes_touched += 1
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction
			curr_history = curr_node.history

			action.action.doAction(action.state, action.parameters)

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)

			# Planner.printHistory(curr_history)
			addNodes(action.state, curr_history)


		print("Nodes touched: " + str(nodes_touched))
		time_taken = time.time() - start_time
		print("--- BFS Planner took %s seconds ---" % (time_taken))
		return [tuple(curr_node.history), nodes_touched, 0, time_taken]

	@staticmethod
	def printHistory(histarr):
		for h in histarr:
			if h.action != None:
				print(str(type(h.action).__name__) + " " +str(h.parameters))

	# @staticmethod
	# def getStacks(histarr):
	# 	print(histarr)

	# 	stackarr = []
	# 	if len(histarr) <= 2:
	# 		print("Whoops, histarr too small!")

	# 	stackarr.append(histarr[1].parameters[0])
	# 	stackarr.append(histarr[1].parameters[1])

	# 	for x in range(2, len(histarr)):
	# 		h = histarr[x]
	# 		stackarr.append(h.parameters[1])
		
	# 	return stackarr

	def parseHistorytoList(self, histarr):
		retarr = []
		for h in histarr:
			if h.action != None:
				name = type(h.action).__name__
				retarr.append([type(h.action).__name__, h.parameters])

		return retarr

	@staticmethod
	def Causal(self, pickBestAction):
		debug = True


		#Initialization
		nodes_touched = 0
		backtracks = 0
		start_time = time.time()

		#Get valid actions copies from a domain so don't need to worry about mutation
		valid_actions = self.domain.getValidActions(self.domain.state)

		#Sanity check
		if len(valid_actions) == 0:
			print("ERROR: No possible actions from initial state!")
			exit(0)

		curr_action = SpecificAction(None, None, deepcopy(self.domain.state))
		print("In planner")
		print(self.domain.state)

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
		# while not(self.goal.isSatisfied(curr_node.specifiedaction.state)):
	
			next_actions = self.domain.getValidActions(curr_node.specifiedaction.state)
			
			#We are at a "dead end" state
			if len(next_actions) == 0:
				if debug:
					print("Stuck... backtracking")
				backtracks += 1
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
			print("Old state: ")
			print(action.state)
			action.action.doAction(action.state, action.parameters)

			if debug:
				print("-> Performed action: " + str(type(action.action).__name__) + " " + str(action.parameters))
				print("New state: ")
				print(action.state)

			#Record the action and resultant state in the history
			curr_node.history.append(deepcopy(action))
			
		time_taken = (time.time() - start_time)

		if debug:
			print("Nodes touched: " + str(nodes_touched))
			print("Backtracks taken: " + str(backtracks))
			print("--- Causal Planner took %s seconds ---" % time_taken)
		return [tuple(curr_node.history), nodes_touched, backtracks, time_taken]

