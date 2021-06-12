import inspect
import customerrors
import itertools
from copy import deepcopy
import random
#from causalmodel import CausalModel
from abstracttypes import SpecificAction
import time
import statistics
import numpy as np
import math
from graphviz import Digraph



class Planner():
	class Node():
		def __init__(self, specifiedaction, history):
			self.specifiedaction = specifiedaction
			self.history = history #list of specific action

		def __str__(self):
			return "Action: " + str(self.specifiedaction) + " History: " + str(self.history)

	def __init__(self, domain):
		self.domain = domain
		self.init_state = domain.state

	def setAlgo(self, algo):
		self.algo = algo

	def plan(self):
		if self.algo == None:
			raise TypeError("Need to set the planning algo first!")
		return self.algo()[0]

	MDP = dict() #mdp[s][a] = [prob, next_state, reward, done]
	value_graph = Digraph(format="png")
	policy_graph = Digraph(format="png")

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

		while not(self.domain.isGoalSatisfied(curr_node.specifiedaction.state)):
		# for i in range(2):
			if len(next_nodes) == 0:
				print("failed to generate a plan...")
				break
			curr_node = next_nodes.pop(0)

			# if debug:
			# 	#print(type(curr_node.specifiedaction.action).__name__ + " " + str(curr_node.specifiedaction.parameters))
			# 	print(curr_node.specifiedaction.state)

			nodes_touched += 1
			#Unpack the node into action and parameters
			action = curr_node.specifiedaction
			curr_history = curr_node.history

			action.action.doAction(action.state, action.parameters)

			#Now find all the next possible actions and add them to the actions list
			curr_history.append(action)
			if debug:
				for curr in curr_history:
					print(curr)
				print(curr_node.specifiedaction.state)
			# Planner.printHistory(curr_history)
			addNodes(action.state, curr_history)
			# for nodes in next_nodes:
			# 	print("next nodes")
			# 	print(str(type(nodes.specifiedaction.action).__name__) + " " +str(nodes.specifiedaction.parameters))
			# 	print(nodes.specifiedaction.state)

		print("Nodes touched: " + str(nodes_touched))
		time_taken = time.time() - start_time
		print("--- BFS Planner took %s seconds ---" % (time_taken))
		return [tuple(curr_node.history), nodes_touched, 0, time_taken]

	@staticmethod
	def printHistory(histarr):
		for h in histarr:
			if h.action != None:
				print(str(type(h.action).__name__) + " " +str(h.parameters))

	@staticmethod
	def HistoryString(histarr):
		string = ''
		for h in histarr:
			if h.action != None:
				string += str(type(h.action).__name__) + " " +str(h.parameters) + "\n"
		return string
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

	def MDP_Init(self):
		queue = []
		queue.append([self.domain.state, None, None])
		done = False
		while(len(queue) > 0):
			state, prev_action, prev_score = queue.pop(0)
			# print("state: " ,state)
			self.value_graph.node(str(state), label=str(state) + str(prev_score))
			self.MDP[state] = dict()
			valid_actions = self.domain.getValidActions(state)
			done = self.domain.isGoalSatisfied(state)
			score = state.causal_graph.getScore()
			# if done:
			# 	print("done")
			# 	print(state)

			if len(valid_actions) ==0 :
				if not done:
					self.MDP[state][0] = [1, 0, -10, 0]
					self.value_graph.node(str(state), label=str(state) + str(-10))
				else:
					self.MDP[state][0] = [1, 0, 10, 1]
					self.value_graph.node(str(state), label=str(state) + str(10))

				continue

			for action in valid_actions:
				# print("valid action: ", action)
				score = action.state.causal_graph.runModel(action.state, action)
				done = self.domain.isGoalSatisfied(action.state)
				#print(action, action.state.causal_graph, done)
				action.action.doAction(action.state, action.parameters)
				self.value_graph.edge(str(state), str(action.state))

				#next_valid_actions = self.domain.getValidActions(action.state)
				#print(len(next_valid_actions), action.state	)
				if done:
					score = 10
				self.MDP[state][action] = [1, action.state, score, done ]
				# if not (action.state in self.MDP):
				queue.append([action.state, action, score])
			#print("\n")
		#self.value_graph.render("image", view=True)


		#TESTING:
		# for state, action_next_state in self.MDP.items():
		# 	print(state.causal_graph)
		# 	for action, next_state in self.MDP[state].items():
		# 		[prob, ns, reward, done] = next_state
		# 		print(action, prob, reward, done)


	def policy_iteration(self):
		v_old = dict() #dict[state] = value
		discount_factor = 0.4
		#initilize value
		for state, _ in self.MDP.items():
			v_old[state] = 0

		while True:
			delta = 0
			v_new = dict()
			for state , action_next_state in self.MDP.items():
				v_f = 0
				v_list = []
				for action, next_state in self.MDP[state].items():
					[prob, ns, reward, done] = next_state
					if ns not in v_old.keys(): # termination state
						v_f = prob * (reward)
					else:
						v_f = prob * (reward + discount_factor * v_old[ns])
					v_list.append(v_f)
				delta = max(delta, abs(max(v_list) - v_old[state]))
				v_new[state] = max(v_list)
			v_old = v_new
			if(delta < 0.2):
				break;

		#TEST:
		# for state, value in v_old.items():
		# 	print(state, value)
		#FIND POLICY //value iteration:
		policy = []
		done = False
		current_state = self.init_state
		while (not done):
		#for i in range(0):
			best_action = None
			max_score = -100
			next_s = None
			score_list = []
			next_state_list = []

			for action, next_state in self.MDP[current_state].items():
				[prob, ns, reward, done] = next_state
				if ns not in v_old.keys():
					continue
				else:
					score = prob * (reward + discount_factor * v_old[ns])
					score_list.append(score)
					next_state_list.append((action, ns, done))
					# print(action, score)
			if len(score_list) !=0:
				for idx, s in enumerate(score_list):
					a, _, _ = next_state_list[idx];
				picked_idx = self.sampleProbs(score_list)
				best_action, next_s, done = next_state_list[picked_idx]
				#print(best_action, next_s, done)
				# print("best_action: ", best_action)

			if best_action is not None:
				policy.append(type(best_action.action).__name__ +": "+ ",".join(best_action.parameters))
				#print(best_action)
			if next_s == None and done !=True:
				done = True
				print("failed to generate a plan. The current plan is as follows: ")
			current_state = next_s

		return policy

	def sampleProbs(self, score):

		for idx, s in enumerate(score):
			if s < 0:
				score[idx] = 0;
		#print(score)
		cdf = np.cumsum(np.array(score))
		cdf_norm = cdf/cdf[-1]
		#print(cdf_norm)
		r = random.uniform(0, 1)
		for idx, c in enumerate(cdf_norm):
			if c > r:
				return idx
		return len(score)-1;

	@staticmethod
	def Causal(self, pickBestAction, repick=None):
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
		# print("In planner")
		# print(self.domain.state)

		#Deep copy because if backtrack to initial state, don't want to manipulate states
		#This special first action holds the first initial state before no action has been done
		#This is why its action type is none
		#Effectively each state stored w an action in the history is the state after an action has been applied
		first_specified_action = deepcopy(curr_action)
		first_specified_action.action = None

		#Place into node
		curr_node = self.Node(curr_action, [first_specified_action])

		#While the current state is not the goal state
		done=False
		while not(self.domain.isGoalSatisfied(curr_node.specifiedaction.state)):
		# while not(self.goal.isSatisfied(curr_node.specifiedaction.state)):

			next_actions = self.domain.getValidActions(curr_node.specifiedaction.state)
			#implement look-ahead step where the next action will result in a dead-end state

			print("current state", curr_node.specifiedaction.state)
			print("current causal", curr_node.specifiedaction.state.causal_graph)

			#We are at a "dead end" state
			if len(next_actions) == 0:
				if debug:
					print("Stuck... backtracking")
				backtracks += 1
				#Want to revert state to a previous state, and try and
				#find some new actions
				curr_node.specifiedaction.state = deepcopy(curr_node.history[-2].state)
				curr_node.specifiedaction.action = deepcopy(curr_node.history[-2].action)
				# print("unsuccess attemp")
				# self.printHistory(curr_node.history)
				curr_node.history.pop()
				#Restart and try and get new actions from beginning
				continue

			curr_node.specifiedaction, all_probs = pickBestAction(next_actions)
			if debug:
				print("picked action: ", type(curr_node.specifiedaction.action).__name__,  curr_node.specifiedaction.parameters)
				print("show current available action prob")
				for i in range(len(next_actions)):
					print("potential action", type(next_actions[i].action).__name__,  next_actions[i].parameters, all_probs[i])

			action = curr_node.specifiedaction

			#Perform the perviously defined action
			nodes_touched += 1

			action.action.doAction(action.state, action.parameters)
			curr_node.specifiedaction.state.causal_graph.runModel(curr_node.specifiedaction.state, action)
			print(curr_node.specifiedaction.state.causal_graph)
			#add one look-ahead step, not needed for this appplication yet:

			potential_next_actions = self.domain.getValidActions(action.state)
			while((len(potential_next_actions) ==0 and not self.domain.isGoalSatisfied(action.state))):
				#curr_node.specifiedaction.state = deepcopy(curr_node.history[-1].state)
				#curr_node.specifiedaction.action = deepcopy(curr_node.history[-1].action)
				repick_indx = next_actions.index(curr_node.specifiedaction)
				next_actions.remove(curr_node.specifiedaction)

				if len(next_actions) == 0:
					done = True
					print("Failed generating a plan")
					break
				curr_node.specifiedaction =  repick(picked_idx=repick_indx)
				print("look ahead found dead-end, repick action...", type(curr_node.specifiedaction.action).__name__,  curr_node.specifiedaction.parameters)

				action = curr_node.specifiedaction
				action.action.doAction(action.state, action.parameters)

				potential_next_actions = self.domain.getValidActions(action.state)


			if done:
				break

			if debug:
				# print("-> Performed action: " + str(type(action.action).__name__) + " " + str(action.parameters))
				# print("New state: ")
				# print(action.state)
				pass

			#Record the action and resultant state in the history
			curr_node.history.append(deepcopy(action))

		time_taken = (time.time() - start_time)

		if debug:
			# print("Nodes touched: " + str(nodes_touched))
			# print("Backtracks taken: " + str(backtracks))
			# print("--- Causal Planner took %s seconds ---" % time_taken)
			pass
		return [tuple(curr_node.history), nodes_touched, backtracks, time_taken]
