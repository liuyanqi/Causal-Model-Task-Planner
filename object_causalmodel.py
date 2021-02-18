import random
from visualmodel import BlockVisualModel
import numpy as np
from abc import ABC, abstractmethod
import sys
import json

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
		self.children_node = []
		self.value = 0
		# self.latent= latent
	def assign_causal_function(self, func):
		self.causal_function = func
	def run_causal_function(self, state, parameters):
		#parameter: obj1, obj2..
		properties = state.causal_graph.children_node[self.name].properties
		if state.current_func == "init":
			for param in parameters:
				for func in state.obj_dict[param].function:
					if properties.get(func) is not None:
						properties[func] =1
					else:
						continue

		else:
			for func in state.obj_dict[parameters[1]].function:
				if properties.get(func) is not None:
					properties[func] +=1
				else:
					continue
		#run causal function for latent casal nodes:
		# if self.latent ==True:
		# 	self.value = self.causal_function(properties)
		self.value = self.causal_function(properties)
		# print(self.name, self.properties, self.value, parameters)
		return self.value
	def get_causal_score(self, state):
		return self.value


class Function_Causal_Graph():
	def __init__(self):
		self.value = 0
		self.all_node = {}
	def addNode(self, causal_node):
		self.all_node[causal_node.name] = causal_node
	def addCausalGraphFromfile(self, filepath):

		with open(filepath) as f:
			data = json.load(f)
		#swap between parent and children
		causal_dict = {}
		for parent, children in data.items():
			for child in children:
				try:
					causal_dict[child].append(parent)
				except KeyError:
					causal_dict[child] = [parent]

		for parent, children in causal_dict.items():
			causal_node = Function_Causal_Node(name=parent);
			# print("parent: ", parent)
			for child in children:
				# print("child: ", child)
				if child not in self.all_node:
					new_node = Function_Causal_Node(name=child);
					self.addNode(new_node);
					causal_node.children_node.append(new_node)
				else:
					causal_node.children_node.append(self.all_node[child])

			#causal_node.assign_causal_function(causal_func)
			self.addNode(causal_node)


	def subtreeUtil(self, root):
		if(len(root.children_node) ==0):
			return root.value;
		value = 1
		for child in root.children_node:
			# print("child: ", child.name, child.value)
			value *= self.subtreeUtil(child);
		# print(root.name, value)
		root.value = value;
		return root.value

	def runModel(self, state, action):

		for param in action.parameters:
			for func in state.obj_dict[param].function:
				if func in self.all_node:
					self.all_node[func].value = 1
		self.value = self.subtreeUtil(self.all_node["lamp"]);
		# print("run model: ", self.value, action)
		return self.value




	def getScore(self):
		return self.value
	def __str__(self):
		ret = ""
		for key, nodes in self.all_node.items():
			if len(nodes.children_node) !=0:
				ret += nodes.name + " \t value: " + str(nodes.value) + "\n\t"
			for cn in nodes.children_node:
				ret+=str(cn.name)+ " : " + str(cn.value) + "\n\t"
			ret +="\n"
		return ret
