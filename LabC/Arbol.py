'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

class ExpressionTree:
    # Metodod constructor 
    def __init__(self, name, value,  position=None):
        # Atributos del arbol
        self.name = name
        self.value = value
        self.left = None
        self.right = None


        # Atributos teniendo en cuenta que el metodo es directo
        self.position = position
        self.listL = None
        self.label = {'firstpos':[],'lastpos':[],'followpos':[],'nullable':[]}
    
    def __iter__(self):
        yield from self._iter_postorder()

    def _iter_postorder(self):
        if self.left:
            yield from self.left._iter_postorder()
        if self.right:
            yield from self.right._iter_postorder()
        yield self

    def postorder_traversal(self):
        if self is None:
            return []

        result = []
        if self.left is not None:
            result.extend(self.left.postorder_traversal())

        if self.right is not None:
            result.extend(self.right.postorder_traversal())
        
        left_value = self.left.value if self.left is not None else None
        right_value = self.right.value if self.right is not None else None
        
        
        #result.append((self.name, self.value,left_value,right_value,self.position))
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


    def maked_tree(postfix,position=None,rule = None, ):
        '''EL rule es nombre del token que se roconocio cuando se llega a un estado de aceptacion'''
        operadores = {"*":"Kleene","·":"Concatenacion","|":"Union","+":"Kleen Positiva","?":"Opcional"}
        stack = []
        tree_leafs = []
        position = position 
        for i in postfix:
            if i == "·":
                leaf = ExpressionTree(operadores[i],i)
                leaf.right = stack.pop()
                leaf.left = stack.pop()
                stack.append(leaf)
                tree_leafs.append(leaf)
            
            elif i == "|":
                leaf = ExpressionTree(operadores[i],i)
                leaf.right = stack.pop()
                leaf.left = stack.pop()
                stack.append(leaf)
                tree_leafs.append(leaf)
            elif (i == "*") or (i == "+") or (i == "?"):
                leaf = ExpressionTree(operadores[i],i)
                leaf.left = stack.pop()
                stack.append(leaf)
                tree_leafs.append(leaf)
            else:
                if i == "ε":
                    leaf = ExpressionTree("Simbolo",i)
                    stack.append(leaf)
                    tree_leafs.append(leaf)
                else:
                    leaf = ExpressionTree("Simbolo",i,position)
                    stack.append(leaf)
                    tree_leafs.append(leaf)
                    position += 1

        return stack[0],tree_leafs

    def unir(left,right,symbol):
            stack=[]
            tree_leafs = []
            if symbol == '|':
                leaf = ExpressionTree('Union',symbol)
                leaf.right =right
                leaf.left = left
                stack.append(leaf)
                tree_leafs.append(leaf)
            return stack[0],tree_leafs

