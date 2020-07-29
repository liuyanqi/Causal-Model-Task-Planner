class Error(Exception):
	pass

class WrongInputType(Error):
	def __init__(self, foundtype, expected, message="Error: action received the wrong type!"):
		self.type = foundtype
		self.expected = expected
		self.found = foundtype
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		return f'{self.message} Expected: {self.expected} Found: {self.found}'

class PredicateFailed(Error):
	def __init__(self, message="Error: predicate failed!"):
		super().__init__(message)


class SimulationOver(Error):
	def __init__(self, message):
		self.message = message
		super().__init__(message)