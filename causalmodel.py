import random
from visualmodel import BlockVisualModel
import numpy as np
from abc import ABC, abstractmethod
import sys
sys.path.append('./pypddl_parser/pypddl_parser')
import pypddl_parser.pypddl_parser.pddlparser as parser
# import pypddl_parser as p1
from abstracttypes import SpecificAction

class CausalModel():
	def __init__(self, name):
		self._nodes = []
		self._name = name

	def addNode(self, node):
		self._nodes.append(node)

	def runModel(self, action):
		retDict = {}
		for node in self._nodes:
			 retDict = {**retDict, **node.getPredicate(action)}
		return retDict

	def __str__(self):
		retstr = str(self._name) + "\n"
		for node in self._nodes:
			retstr += str(node) + "\n\n"
		return retstr

class CausalNode():
	def __init__(self, name, funct_str):
		self._name = name
		self._func = funct_str

	def getPredicate(self, action):
		ns = {"ret": [], "action":action}
		#print("func:", self._func)
		exec(self._func, ns)
		return ns["ret"]

	def __str__(self):
		return str(self._name) + "\n " + self._func

def sampleProbs(probabilities):
		r = random.random()
		for x in range(len(probabilities)):
			r = r - probabilities[x]
			if r <= 0:
				return x

def generateCausalModels(domain_path, domain):
	valid_relation_words = ["and", "or"]

	models = {}


	causalGraphClasses = parser.PDDLParser.parse(domain_path).causals

	for graph in causalGraphClasses:
		currModel = CausalModel(graph.name)

		#Check the graph name matches an action in the domain
		if not(domain.checkActionExists(graph.name)):
			#This causal model's name matches no actions
			raise ValueError(str(graph.name) + " matches no actions in the given domain. Cannot generate CausalModel.")

		#Check the number of params matches the number of params for that action
		action_params = eval("domain." + graph.name).param_types
		if not(len(action_params) == len(graph.params)):
			raise ValueError("The number of parameters for the " + str(graph.name) + " action is incorrect. Cannot generate CausalModel")

		for node in graph.nodes:
			if node.relation_word not in valid_relation_words:
				raise ValueError("Relation word: " + str(node.relation_word) + " not supported. Cannot generate CausalModel.")


			funcstr = "vals = []\n"

			count = 0
			for prop in node.relation:
				checkAttributeValueExists(domain, prop, graph.params, action_params)
				#example flat_bottom
				prop_word = str(prop).split("(")[0]
				#example (?blockone ?blocktwo)
				qparam = str(prop).split("(")[1].split(")")[0]

				#Need to figure out which parameter for the actual action object corresponds to the qparam
				action_param_number = graph.params.index(qparam)


				if prop_word == "flat_bottom":
					prop_word = "flatness[\"bottom\"]"
				elif prop_word == "flat_top":
					prop_word = "flatness[\"top\"]"

				#This does label independant positoning
				# funcstr += "\nvals.append(action.state.get(action.parameters[" + str(count) + "])." + prop_word + ")"
				funcstr += "\nvals.append(action.state.get(action.parameters[" + str(action_param_number) + "])." + prop_word + ")"
				count += 1
			if node.relation_word == "and":
				funcstr += "\nvals = all(vals)"
			elif node.relation_word == "or":
				funcstr += "\nvals = any(vals)"

			funcstr += "\nret = {\"" + node.name + "\": vals}"

			# sa = SpecificAction(domain.stack, ["a", "b"], domain.state)

			currModel.addNode(CausalNode(node.name, funcstr))

		models[currModel._name] = currModel

	domain.causal_models = models

	for act in domain.actions:
		act_name = type(act).__name__

		if not(act_name in models.keys()):
			raise ValueError("Didn't parse a CausalModel for: " + str(act_name) + ". Cannot generate CausalModel")

	return models


def checkAttributeValueExists(domain, prop, causalparams, action_params):
	#The string ?x or ?y or whatever
	qparam = str(prop).split("(")[1].split(")")[0]
	prop_word = str(prop).split("(")[0]
	#Where in the causal predicates array it is
	param_index = causalparams.index(qparam)
	#What type that parameter should have in the domain
	param_type = action_params[param_index]


	example_obj_name = eval("domain.state.obj_types[\"" + str(param_type) + "\"][0]")
	try:
		if prop_word == "flat_bottom":
			val = domain.state.get(example_obj_name).flatness["bottom"]
		elif prop_word == "flat_top":
			val = domain.state.get(example_obj_name).flatness["top"]
		else:
			val = eval("domain.state.get(example_obj_name)." + prop_word)
	except AttributeError as e:
		return False
	return True


def sampleProbs(probabilities):
		r = random.random()
		for x in range(len(probabilities)):
			r = r - probabilities[x]
			if r <= 0:
				return x
