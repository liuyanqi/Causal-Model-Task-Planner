import random

class BlockVisualModel():
	def __init__(self, domain):
		self.domain = domain
		self.domain.state.visual = self
		self.blocks = domain.state.obj_types["Block"]

		self.flatness_vals = {}

		#Binary
		self.flatness_vals["a"] = {"top": 0, "bottom": 1}
		self.flatness_vals["b"] = {"top": 1, "bottom": 1}
		self.flatness_vals["c"] = {"top": 1, "bottom": 1}
		self.flatness_vals["d"] = {"top": 1, "bottom": 1}

		for bname, flatness_dict in self.flatness_vals.items():
			self.domain.state.get(bname).flatness = flatness_dict

		# Normal
		# self.flatness_vals["a"] = {"top": random.randrange(0, 20)/100, "bottom": random.randrange(0, 20)/100}
		# self.flatness_vals["b"] = {"top": random.randrange(50, 90)/100, "bottom": random.randrange(50, 90)/100}
		# self.flatness_vals["c"] = {"top": random.randrange(50, 90)/100, "bottom": random.randrange(50, 90)/100}
		
		# Reflective of Triangle
		# self.flatness_vals["a"] = {"top": 0.05, "bottom": 0.9}
		# self.flatness_vals["b"] = {"top": 0.5, "bottom": 0.9}
		# self.flatness_vals["c"] = {"top": 0.9, "bottom": 0.9}

		#T1
		# self.flatness_vals["a"] = {"top": 0.05, "bottom": 0.9}
		# self.flatness_vals["b"] = {"top": 0.5, "bottom": 0.9}
		# self.flatness_vals["c"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["d"] = {"top": 0.05, "bottom": 0.9}
		# self.flatness_vals["e"] = {"top": 0.05, "bottom": 0.9}
		# self.flatness_vals["f"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["g"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["h"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["i"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["j"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["k"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["l"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["m"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["n"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["o"] = {"top": 0.9, "bottom": 0.9}
		# self.flatness_vals["p"] = {"top": 0.9, "bottom": 0.9}

		

		# print("Initial flatness values: ")
		# print(str(self.flatness_vals) + "\n")

		self.total_weight = 0
		self.total_height = 0


	#This function is no longer nessecary because the visual properties of the blocks do not change
	def update(self, state):
		pass

	#This function updates the visual properties of the world based on
	#information about the world state
	# def update(self, state):
	# 	#Flatness is a value that each block in the system has
	# 	#1 being the max, 0 being the worst
	# 	#This value gets reupdated based on the block configuration as well as
	# 	#What actions have been taken

	# 	"""
	# 	A triangle at the base of the tower, has a much worse flatness than (0.1)
	# 	A triangle on the middle or top of the tower (0.5)
	# 	Squares have a decent flatness, that is randomly distributed between
	# 	0.6 and 1
	# 	"""

	# 	#A is the triangle
	# 	#B and C are squares


	# 	'''
	# 	Make sure that when anything is stacked on a their flatness decreases for sure
	# 	'''

	# 	for i in range(len(self.blocks)):
	# 		block = self.blocks[i]

	# 		if block == "a":
	# 			if self.domain.state.get("a").on == "floor":
	# 				self.flatness_vals["a"] = random.randrange(0, 10)/100
	# 			elif ((self.domain.state.get("a").on != "floor" 
	# 				and 
	# 				self.domain.state.get("a").on != None) 
	# 				and 
	# 				self.domain.state.get(self.domain.state.get("a").on).on == None):
    #
	# 				self.flatness_vals["a"] = random.randrange(10, 40)/100
	# 			elif self.domain.state.get("a").on == None:
	# 				pass
	# 			else:
	# 				self.flatness_vals["a"] = random.randrange(40, 70)/100
	# 		elif block == "b" or block == "c":
	# 			if self.domain.state.get(block).on == "a":
	# 				tot = random.randrange(20, int(self.flatness_vals[block]*100) - 10)/100
	# 				self.flatness_vals[block] = tot
	# 		else:
	# 			print("ERROR IN VISUALMODEL! IDK THIS BLOCK: " + str(block))

	def getFlatnessVals(self, obj_name):
		return self.flatness_vals[obj_name]

	# def getStackability(self, a, b):
	# 	return (self.flatness_vals[a]["top"] + self.flatness_vals[b]["bottom"])/2


