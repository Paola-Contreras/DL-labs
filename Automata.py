'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''
# ------ Clase automata ------
class Automata():
    def __init__(self, states, start, end, transitions, alphabet):
        self.alfabet = alphabet
        self.states = states
        self.start_state = start
        self.end_state = end
        self.transitions = transitions