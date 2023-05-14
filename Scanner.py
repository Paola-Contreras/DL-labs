def scanner (rule):
	if rule == 'ws': return 'ws'
	if rule == 'id': return 'ID'
	if rule == '&': return 'PLUS'
	if rule == '^': return 'TIMES'
	if rule == '(': return 'LPAREN'
	if rule == ')': return 'RPAREN'
	if rule == 'error': return 'ERROR LEXICO'