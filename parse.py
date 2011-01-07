import ply.lex as lex

def OuterTokenizer():
	tokens = ( 'TAGOPEN', 'TAGCLOSE', 'TAGNAME', 'SLASH', 'NORMSTR', 'HASHVAR', 'TAG_WS' )
	states = (
		("intag", "exclusive"),
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
	
	def t_intag_TAG_WS(t):
		r'[ \t]+'
		pass
	
	t_intag_TAGNAME = r'[a-zA-Z0-9_]+'
	t_NORMSTR = r'(\<[^@]|\<$|[^<@])+'
	
	return lex.lex()


