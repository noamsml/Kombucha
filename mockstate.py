class DummyState:
	def __init__(self, vars):
		self.vars = vars
	def getvar(self, s):
		return self.vars[s]
