def scanner (rule):
	if rule == 'ws': return 'ws'
	if rule == 'id': return 'ID'
	if rule == 'number': return 'NUMBER'
	if rule == ';': return 'SEMICOLON'
	if rule == ':=': return 'ASSIGNOP'
	if rule == '<': return 'LT'
	if rule == '=': return 'EQ'
	if rule == '&': return 'PLUS'
	if rule == '-': return 'MINUS'
	if rule == '^': return 'TIMES'
	if rule == '/': return 'DIV'
	if rule == '(': return 'LPAREN'
	if rule == ')': return 'RPAREN'
	if rule == 'error': return 'ERROR LEXICO'