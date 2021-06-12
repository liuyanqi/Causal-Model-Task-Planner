import random
from visualmodel import BlockVisualModel
import sys
import numpy as np
from abc import ABC, abstractmethod
import sys
import json
import collections
from causal_graph import CausalGraph

# import pypddl_parser as p1
from abstracttypes import SpecificAction, Action

# This superclass maintains a list of objects and their names in a domain state
# The model looks like:
# Init -> power_out -> conduct -> produce
# class Function(ABC):
# 	def __init__(self, obj):
# 		if obj is not None:
# 			self.name = obj.function
# 		else:
# 			self.name = "init"
# 		self.objects = []
# 		self.next_func = None
# 	def __str__(self):
# 		ret = "function of " + self.name +" has following objects: \n"
# 		for obj in self.objects:
# 			ret+= obj + ", "
# 		ret += "\n"
# 		return ret
# #THIS CAUSAL MODEL WILL TAKE HUMAN COMMAND AND GENERATE FUNCTIONAL CAUSAL GRAPH FOR THE STATE
# class Function_Causal():
# 	def __init__(self):
# 		self.obj_func = {}
#
# 	def initModel(self, state):
# 		self.obj_func["init"] = Function(None)
# 		for obj in state.objects:
# 			try:
# 				self.obj_func[obj.function].objects.append(obj.name)
# 			except KeyError as e:
# 				self.obj_func[obj.function] = Function(obj)
# 				self.obj_func[obj.function].objects.append(obj.name)
#
# 	def add_connect(self, obj1, obj2):
# 		#human commands combine obj2 to obj1
# 		if self.obj_func["init"].next_func is None:
# 			self.obj_func["init"].next_func = obj1.function
# 		self.obj_func[obj1.function].next_func = obj2.function
#
# 	def __str__(self):
# 		ret = "Function_Causal: \n"
# 		for key, val in self.obj_func.items():
# 			ret += str(val)
# 		return ret


class Function_Causal_Node():
	def __init__(self, name, param=[]):
		self.name = name
		self.causal_function = None
		self.properties = {p: 0 for p in param}
		self.children_node = [] #node_name
		self.value = 0
		# self.latent= latent
	def assign_causal_function(self, func):
		self.causal_function = func
	# def run_causal_function(self, state, parameters):
	# 	#parameter: obj1, obj2..
	# 	properties = state.causal_graph.children_node[self.name].properties
	# 	if state.current_func == "init":
	# 		for param in parameters:
	# 			for func in state.obj_dict[param].function:
	# 				if properties.get(func) is not None:
	# 					properties[func] =1
	# 				else:
	# 					continue
	#
	# 	else:
	# 		for func in state.obj_dict[parameters[1]].function:
	# 			if properties.get(func) is not None:
	# 				properties[func] +=1
	# 			else:
	# 				continue
	# 	#run causal function for latent casal nodes:
	# 	# if self.latent ==True:
	# 	# 	self.value = self.causal_function(properties)
		# self.value = self.causal_function(properties)
		# print(self.name, self.properties, self.value, parameters)
		# return self.value
	def get_causal_score(self, state):
		return self.value


class Function_Causal_Graph():
	def __init__(self, goal):
		self.value = 0
		self.all_graph = []
		self.all_node = {}
		self.coef_map = collections.defaultdict(dict)
		#self.causal_graph = CausalGraph()
		self.goal_name = goal

	def addNode(self, causal_node):
		self.all_node[causal_node.name] = causal_node
	def addCausalGraphFromfile(self, filepath):

		with open(filepath) as f:
			data = json.load(f)
		#self.causal_graph.show(data)
		#swap between parent and children
		# causal_dict = {}
		# for parent, children in data.items():
		# 	for child in children:
		# 		try:
		# 			causal_dict[child].append(parent)
		# 		except KeyError:
		# 			causal_dict[child] = [parent]
		for graph in data:
			causal_graph = {}
			for parent, children in graph.items():
				causal_node = Function_Causal_Node(name=parent);
				print("parent: ", parent)
				for child_pair in children:
					print("child: ", child_pair)
					child, coef = child_pair
					if child not in self.all_node:
						new_node = Function_Causal_Node(name=child);
						self.all_node[new_node.name] = new_node
						causal_graph[new_node.name] = new_node


					self.coef_map[parent][child] = coef;
					causal_node.children_node.append(child)


				# self.addNode(causal_node)
				self.all_node[causal_node.name] = causal_node
				causal_graph[causal_node.name] = causal_node
				self.all_graph.append(causal_graph)
		print(self.coef_map)


	def subtreeUtil(self, root):
		if(len(root.children_node) ==0):
			return root.value;
		value = 1
		all_plus = True
		coef_sum = 0;
		for child in root.children_node:
			coef = self.coef_map[root.name][child]
			if coef !=-1:
				coef_sum += coef

		for child in root.children_node:
			#print("child: ", child.name, child.value)
			coef = self.coef_map[root.name][child]
			if coef == -1:
				value *= self.subtreeUtil(self.all_node[child]);
				all_plus=False;
			elif coef == 1:
				value += self.subtreeUtil(self.all_node[child])
			# 	all_plus=False
			else:
				value += (coef/coef_sum) * self.subtreeUtil(self.all_node[child])
		#print(root.name, value)
		if all_plus:
			root.value = value-1;
		else:
			root.value = value
		return root.value

	def runModel(self, state, action):

		for param in action.parameters:
			for func in state.obj_dict[param].function:
				if func in self.all_node:
					self.all_node[func].value = 1

		for graph in self.all_graph:
			value = self.subtreeUtil(graph[self.goal_name]);
			if(value > self.value):
				self.value = value
		print("run model: ", self.value, action)
		return self.value

	def runModelfromState(self, state):
		for tower_name, tower in state.tower.items():
			for block in tower:
				for func in state.obj_dict[block.name].function:
					if func in self.all_node:
						self.all_node[func].value = 1
		for graph in self.all_graph:
			value = self.subtreeUtil(graph[self.goal_name]);
			if(value > self.value):
				self.value = value;
			# print("run model: ", self.value, action)
		return self.value


	def getScore(self):
		return self.value

	def __str__(self):
		ret = ""
		for graph in self.all_graph:
			for key, nodes in graph.items():
				if len(nodes.children_node) !=0:
					ret += nodes.name + " \t value: " + str(nodes.value) + "\n\t"
				for cn in nodes.children_node:
					ret+=str(graph[cn].name)+ " : " + str(graph[cn].value)  + " coef: " + str(self.coef_map[nodes.name][cn])+ "\n\t"
				ret +="\n"
		return ret
