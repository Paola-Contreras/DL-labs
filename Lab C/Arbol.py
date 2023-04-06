'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

class ExpressionTree:
    # Metodod constructor 
    def __init__(self, name, value):
        # Atributos del arbol
        self.name = name
        self.value = value
        self.left = None
        self.right = None


    # Metodo para mostrar arbol en forma de lista
    def show_tree(self,list_el = []):
            if self.left:
                self.left.show_tree()
            list_el.append([self.name,self.value])
            #print(self.name, self.value)
            if self.right:
                self.right.show_tree()
            
            return list_el
    
    def postorder_traversal(self):
        if self is None:
            return []

        result = []
        if self.left is not None:
            result.extend(self.left.postorder_traversal())

        if self.right is not None:
            result.extend(self.right.postorder_traversal())

        result.append((self.name, self.value))

        return result
    
        # Metodo para generar la representación DOT del árbol
    def to_dot(self):
        dot = 'digraph ExpressionTree {\n'
        dot += self._to_dot()
        dot += '}\n'
        return dot
    
    def _to_dot(self):
        dot = ''
        if self.left:
            dot += f'"{id(self)}" -> "{id(self.left)}"\n'
            dot += self.left._to_dot()
        if self.right:
            dot += f'"{id(self)}" -> "{id(self.right)}"\n'
            dot += self.right._to_dot()
        dot += f'"{id(self)}" [label="{self.value}"]\n'
        return dot
        
def make_tree(postfix):
    operadores = {"*":"Kleene",".":"Concatenacion","|":"Union","+":"Kleen Positiva","?":"Opcional"}
    stack = []
    for i in postfix:
        if i == "|":
            leaf = ExpressionTree(operadores[i],i)
            leaf.right = stack.pop()
            leaf.left = stack.pop()
            stack.append(leaf)
        elif i == ".":
            leaf = ExpressionTree(operadores[i],i)
            leaf.right = stack.pop()
            leaf.left = stack.pop()
            stack.append(leaf)
        elif (i == "*") or (i == "+") or (i == "?"):
            leaf = ExpressionTree(operadores[i],i)
            leaf.left = stack.pop()
            stack.append(leaf)
        else:
            leaf = ExpressionTree("Simbolo",i)
            stack.append(leaf)
    return stack[0]
