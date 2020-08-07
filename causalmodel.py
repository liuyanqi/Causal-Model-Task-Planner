import random
from visualmodel import BlockVisualModel 
import numpy as np
from abc import ABC, abstractmethod
import sys
sys.path.append('./pypddl_parser/pypddl_parser')
import pypddl_parser.pypddl_parser as parser
from abstracttypes import SpecificAction

class CausalPredicate(ABC):
	def __init__(self, name, funct_str):
		self._name = name
		self._func = funct_str

	def getPredicates(self, action):
		ns = {"ret": [], "action":action}
		exec(self._func, ns)
		return ns["ret"]

class CausalModel(ABC):
	def __init__(self, name, causalModel):
		self.causalModel = causalModel



	@abstractmethod
	def getPredicates(self, action):
		pass
		# if len(action.parameters) == 2:
		# 	x = action.parameters[0]
		# 	y = action.parameters[1]
		
		# 	return {"stackability": self.viz.getFlatnessVals(x)["top"] * self.viz.getFlatnessVals(y)["bottom"]}
		# else:
		# 	return {"stackability": self.viz.getFlatnessVals(action.parameters[0])["top"]}


def sampleProbs(probabilities):
		r = random.random()
		for x in range(len(probabilities)):
			r = r - probabilities[x]
			if r <= 0:
				return x

def generateCausalModel(domain_path, domain):
	valid_relation_words = ["and", "or"]
	# print(parser.torun.run(domain_path))

	causalGraphClasses = parser.torun.run(domain_path).causals
	for graph in causalGraphClasses:
		print("Graph name: " + graph.name )

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


			funcstr = "vals = []\nname=\"" + graph.name + "\""
			
			count = 0
			for prop in node.related:
				checkAttributeValueExists(domain, prop, graph.params, action_params)
				prop_word = str(prop).split("(")[0]

				if prop_word == "flat_bottom":
					prop_word = "flatness[\"bottom\"]"
				elif prop_word == "flat_top":
					prop_word = "flatness[\"top\"]"


				funcstr += "\nvals.append(action.state.get(action.parameters[" + str(count) + "])." + prop_word + ")"
				count += 1
			if node.relation_word == "and":
				funcstr += "\nvals = all(vals)"
			elif node.relation_word == "or":
				funcstr += "\nvals = any(vals)"

			funcstr += "\nret = {\"" + node.name + "\": vals}"

			sa = SpecificAction(domain.stack, ["a", "b"], domain.state)

			cp = CausalPredicate(node.name, funcstr)
			cp.getPredicates(sa)

			

			ns = {"ret": [], "action":sa}
			codeObject = compile(funcstr, 'string', 'exec')
			exec(funcstr, ns)
			print(ns["ret"])
			



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

				





