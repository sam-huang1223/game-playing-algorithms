input = [[['A', 'MIN'], ['B', 'MAX'], ['C', 'MAX'], ['D', 'MAX'], ['E', 'MAX'], ['F', 'MIN'], ['G', 'MIN'], ['H', 'MIN'], ['I', 'MIN'], ['J', 'MIN'], ['K', 'MIN'], ['L', 'MIN'], ['M', 'MIN'], ['N', 'MIN'], ['O', 'MIN']], [['A', 'B'], ['A', 'C'], ['A', 'D'], ['A', 'E'], ['B', 'F'], ['B', 'G'], ['B', 'H'], ['C', 'I'], ['C', 'J'], ['D', 'K'], ['D', 'L'], ['E', 'M'], ['E', 'N'], ['E', 'O'], ['F', '6'], ['F', '3'], ['F', '2'], ['G', '5'], ['G', '9'], ['H', '4'], ['H', '1'], ['I', '6'], ['J', '6'], ['J', '12'], ['K', '13'], ['K', '14'], ['L', '6'], ['L', '12'], ['M', '2'], ['M', '5'], ['M', '7'], ['N', '6'], ['N', '7'], ['O', '12'], ['O', '2']]]

'''
This algorithm can be run independently by uncommenting the input above

The input consist of a graph represented as a list of lists of nodes and edges
    The list of nodes is a list of lists in the form of [NODE_NAME, 'MAX'/'MIN']
    The list of edges is a list of lists in the form of [START_NODE_NAME, END_NODE_NAME]
'''

constant = 100000

class Node():
    def __init__(self, index, children, type, alpha=-constant, beta=constant):
        self.index = index
        self.alpha = alpha
        self.beta = beta
        self.type = type
        self.children = children

class Minimax():
    def __init__(self, graph, display):
        self.print_output = []
        self.traversed = []
        self.all_children = []

        self.nodes = {node[0]: Node(index=node[0],children=[],type=node[1]) for node in graph[0]}

        for edge in graph[1]:
            try:
                child = int(edge[1])
            except:
                child = self.nodes[edge[1]]
            self.nodes[edge[0]].children.append(child)
            self.all_children.append(edge[1])

        self.root = self.nodes[self.find_root()]
        self.root_path = [self.root]

        self.root.alpha = self.alpha_beta_search(self.root, alpha=self.root.alpha, beta=self.root.beta)

        self.game_value = self.root.alpha if self.root.type == 'MAX' else self.root.beta
        print('\nThe value of the game is:', self.game_value)

        self.path_to_root(self.root)

        self.minimax_path = []
        seen = set()
        for i in self.root_path:
            if i not in seen:
                self.minimax_path.append(i)
                seen.add(i)

        self.path = [i if isinstance(i, int) else i.index for i in self.minimax_path]
        print('Path: ', self.path)
        print('\nTraversed (count = {count}) '.format(count=len(self.traversed)))

        if display:
            self.print_tree()
            print('Final node values:')
            for element in sorted(self.print_output, key=lambda x: ord(x[5:x.find('type')].strip())):
                print(element)

    def find_root(self):
        for key, node in self.nodes.items():
            if key not in self.all_children:
                return key

    def alpha_beta_search(self, node, alpha, beta):
        if isinstance(node, int):
            self.traversed.append(node)
            return node

        if node.type == 'MAX':
            node.beta = beta
            for child in node.children:
                if self.root.alpha != -constant and self.root.alpha > node.alpha:
                    node.alpha = self.root.alpha
                a = self.alpha_beta_search(child, alpha=node.alpha, beta=node.beta)
                if a > node.alpha:
                    #print('node: {index} - alpha update:\tfrom {before} to {after}'.format(index=node.index, before=node.alpha, after=a))
                    node.alpha = a
                if node.alpha >= node.beta:
                    break
            return node.alpha

        else:
            node.alpha = alpha
            for child in node.children:
                if self.root.beta != constant and self.root.beta < node.beta:
                    node.beta = self.root.beta
                b = self.alpha_beta_search(child, alpha=node.alpha, beta=node.beta)
                if b < node.beta:
                    #print('node: {index} - beta update:\tfrom {before} to {after}'.format(index=node.index, before=node.beta, after=b))
                    node.beta = b
                if node.beta <= node.alpha:
                    break
            return node.beta

    def path_to_root(self, node):
        if node.type == 'MAX':
            for child in node.children:
                if isinstance(child, int):
                    if child == node.alpha:
                        self.root_path.append(child)
                elif child.beta == node.alpha:
                    self.root_path.append(child)
                    self.path_to_root(child)
                    break
        else:
            for child in node.children:
                if isinstance(child, int):
                    if child == node.beta:
                        self.root_path.append(child)
                elif child.alpha == node.beta:
                    self.root_path.append(child)
                    self.path_to_root(child)
                    break


    def print_tree(self):
        for key, node in self.nodes.items():
            self.print_output.append(('node: {index:<}\ttype: {type:<}\talpha: {alpha:<8}\tbeta: {beta:<8}\tchildren: {children}'.format(
                                        index=node.index, type=node.type, alpha=node.alpha, beta=node.beta,
                                        children=[child.index if not isinstance(child, int) else child for child in node.children])))

if __name__ == '__main__':
    Minimax(input, True)
