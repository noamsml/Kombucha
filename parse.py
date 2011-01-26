import ply.lex as lex
import ply.yacc as yacc
import contentmodel as c
from cStringIO import StringIO
import os


file_parse_cache = {}

KOMBUCHA_PATH = ["."]


all_tokens = ( 'TAGOPEN', 'TAGCLOSE', 'TAGSTR', 'SLASH', 'NORMSTR', 'HASHVAR', 'INCLUDED',
	'TAG_WS', 'EQUALS', 'QUOTE', 'NONESC', 'ESC', 'STRLIT', 'INTLIT' )
	
def lexer_init():
	tokens = all_tokens
	states = (
		("intag", "exclusive"),
		("quoted", "exclusive")
	)
	
	def t_TAGOPEN(t):
			r'\<@'
			t.lexer.begin("intag")
			return t

	def t_intag_TAGCLOSE(t):
			r'@\>'
			t.lexer.begin("INITIAL")
			return t
			
	t_intag_SLASH = r'/'
	t_HASHVAR = r'@[a-zA-Z0-9_]+@'
	t_INCLUDED = r'%[-a-zA-Z0-9_/.]+%' #IMPROVE THIS --NOAM
	
	def t_intag_TAG_WS(t):
		r'[ \t]+'
		pass
	
	def t_intag_QUOTE(t):
		r'"'
		t.lexer.quoteval = StringIO()
		t.lexer.begin("quoted")
	
	def t_quoted_NONESC(t):
		r'[^"\\]+'
		t.lexer.quoteval.write(t.value)
	
	def t_quoted_ESC(t):
		r'\\.'
		change = {'n' : '\n', 't' : '\t'} #etc
		if t.value[1] in change:
			tval = change[t.value[1]]
		else:
			tval = t.value[1]
		t.lexer.quoteval.write(tval)
	
	def t_quoted_STRLIT(t):
		r'"'
		t.value = t.lexer.quoteval.getvalue()
		t.lexer.begin("intag")
		return t 
	
	def t_intag_INTLIT(t):
		r'[+-]?[0-9]+'
		t.value = int(t.value)
		return t
		
	
	
	t_intag_TAGSTR = r'[a-zA-Z_][a-zA-Z0-9_]*'
	t_NORMSTR = r'(\<[^@]|\<$|[^<@%])+'
	
	t_intag_EQUALS = "="
	
	return lex.lex()
	
def parser_init():
	tokens = all_tokens
	def p_page_init(p):
		'page :'
		p[0] = c.Content()
	
	def p_page_next(p):
		'page : page value'
		p[0] = p[1]
		p[0].addchild(p[2])
	
	def p_value_normstr(p):
		'value : NORMSTR'
		p[0] = c.NormalString(p[1])
	
	def p_value_hashvar(p):
		'value : HASHVAR'
		p[0] = c.HashVar(p[1][1:-1])
	
	def p_value_include(p):
		'value : INCLUDED'
		p[0] = c.Include(p[1][1:-1])
	
	def p_value_emptytag(p):
		'value : TAGOPEN TAGSTR posargs namedargs SLASH TAGCLOSE'
		p[0] = c.Tag(p[2], p[3], p[4], c.Null())
	
	def p_value_fulltag(p):
		'value : TAGOPEN TAGSTR posargs namedargs TAGCLOSE page TAGOPEN SLASH TAGSTR TAGCLOSE'
		if p[2] != p[9]:
			print "DIRE WARNING: MISMATCHED TAGS: %s AND /%s" % (p[2], p[9])
		p[0] = c.Tag(p[2], p[3], p[4], p[6])
	
	def p_posargs_empty(p):
		'posargs : '
		p[0] = []
	
	def p_posargs_value(p):
		"""posargs : posargs STRLIT  
				   | posargs INTLIT"""
		p[0] = p[1]
		p[0].append(c.Value(p[2]))
		
	def p_namedargs_empty(p):
		'namedargs : '
		p[0] = []
	
	def p_namedargs_arg(p):
		'namedargs : namedargs TAGSTR EQUALS argval'
		p[0] = p[1]
		p[0].append( (p[2], p[4]) )
	
	def p_argval_value(p):
		"""argval : STRLIT 
				  | INTLIT"""
		p[0] = c.Value(p[1])
	
	return yacc.yacc()
	
def parse_string(string):
	return parser.parse(string, lexer=tokenizer)
	
def parse_file(fname):
	fname = resolve_file(fname)
	if fname not in file_parse_cache:
		file_parse_cache[fname] =  parser.parse(open(fname).read(), lexer=tokenizer)
	return file_parse_cache[fname]
	
def resolve_file(fname):
	if fname.find("/") != -1:
		return fname
	else:
		fname += ".kbc"
		for elem in KOMBUCHA_PATH:
			fn = os.path.join(elem, fname)
			if os.path.exists(fn):
				return fn
	


tokenizer = lexer_init()
parser = parser_init()
