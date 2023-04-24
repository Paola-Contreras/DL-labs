def scanner (rule):
	if rule == 'ws': return 'WHITESPACE'
	if rule == 'number': return 'NUMBER'
	if rule == '>': return 'PLUS'
	if rule == '<': return 'TIMES'
	if rule == '(': return 'LPAREN'
	if rule == ')': return 'RPAREN'
	if rule == 'error': return 'ERROR LEXICO'