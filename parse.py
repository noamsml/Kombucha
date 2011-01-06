import ply.lex as lex

def OuterTokenizer():
	tokens = ( 'CLOSETAG', 'OPENCLOSETAG', 'TAG', 'HASHVAR', 'NORMSTR' )
	
	t_CLOSETAG = r'\<@\W*/\W*[a-zA-Z0-9_]+\W*@\'\>'
	t_OPENCLOSETAG = r'\<@\W*[a-zA-Z0-9_]+\W*/\W*@\>'
	t_TAG = r'\<@\W*[a-zA-Z0-9_]+\W*@\>' #for now
	t_HASHVAR = r'@[a-zA-Z0-9_]+@'
	t_NORMSTR = r'(\<[^@]|\<$|[^<@])+'
	
	return lex.lex()


