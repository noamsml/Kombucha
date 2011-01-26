from cStringIO import StringIO
import parse

class Content:
	def __init__(self):
		self.children = []
	def addchild(self, child):
		self.children.append(child)
	def render(self, state):
		buf = StringIO()
		for child in self.children:
			buf.write(child.render(state))
		return buf.getvalue()

class NormalString:
	def __init__(self, str):
		self.value = str
	def render(self, state):
		return self.value

class HashVar:
	def __init__(self, str):
		self.value = str
	def render(self, state):
		return state.getvar(self.value)

class Include:
	def __init__(self, str):
		self.value = str
	def render(self, state):
		return parse.parse_file(self.value).render(state) #OPTIMIZE THIS
		
class Tag:
	def __init__(self, tagname, posarg, hasharg, content):
		self.tagname = tagname
		self.posarg = posarg
		self.hasharg = hasharg
		self.content = content
	def render(self, state):
		return state.runfunc(self.tagname, self.posarg, self.hasharg, self.content)



class Value:
	def __init__(self, val):
		self.val = val
	def resolve(self, state):
		return self.val


class NullContent:
	def render(self, state):
		return ""
		

Null = NullContent()
