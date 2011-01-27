import parse
import contentmodel

class Module:
	def __init__(self, d):
		for k in d:
			setattr(self, k, d[k])

class DefaultTags:
	kombucha_version = "0.000<snip>1"
	def with_vars(self, state, content, **dict):
		return state.render_with(content, dict)

class Template:
	def __init__(self, source, type="file"):
		if type == "file":
			self.parsedata = parse.parse_file(source)
		elif type == "string":
			self.parsedata = parse.parse_string(source)
		else:
			raise Exception("Programmer Error: Wrong source-type")
			
			
		self.varstack = [DefaultTags()] # for now
		
	def render(self, data = None):
		if data == None:
			data = self.parsedata
		return data.render(self)
	
	def getvar(self, s):
		return self.var_of(self.resolve(s))
		
	def resolve(self,s):
		for i in range(len(self.varstack)-1, -1, -1):
			if hasattr(self.varstack[i],s):
				return getattr(self.varstack[i],s)
		raise Exception("Variable Not Found: %s" % s)
	
	def var_of(self, val):
		if type(val) == str:
			return val
		elif callable(val):
			return val(self, contentmodel.Null) #for now
		else:
			raise Exception("Not a variable: %s", val)
	
	def __setitem__(self, s, val):
		self.addvar(s,val)
	
	def __getitem__(self, s):
		return self.resolve(s)
	
	def push_module(self, module):
		if type(module) == dict:
			module = Module(module)
		self.varstack.append(module)
	
	def pop_module(self):
		self.varstack.pop()
		
	def render_with(self, content, *modules):
		for mod in modules:
			self.push_module(mod)
		s = self.render(content)
		for mod in modules:
			self.pop_module()
		return s
	
	def runfunc(self, tagname, posarg, hasharg, content):
		func = self.resolve(tagname)
		posarg = self.resolve_posargs(posarg)
		hasharg = self.resolve_hashargs(hasharg)
		return func(self, content, *posarg, **hasharg)
	
	def resolve_posargs(self, posarg):
		return [p.resolve(self) for p in posarg]
	
	def resolve_hashargs(self, hasharg):
		return dict( ((p[0], p[1].resolve(self)) for p in hasharg) )
		

