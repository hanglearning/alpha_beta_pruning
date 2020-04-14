import sys

# get user input terminal values
user_inputs = sys.argv[1].split(' ')

class MinimaxNode:

	# alpha beta initialization reference - https://www.youtube.com/watch?v=xBXHtz4Gbdo
    def __init__(self, value=None, alpha=float('-inf'), beta=float('inf'), parent=None, is_max=None, is_terminal=False):
        self.value = value
        self.alpha = alpha
        self.beta = beta
        self.parent = parent
        self.is_max = is_max
        self.is_terminal = is_terminal
        self.children = []
        self.prunable = False

    # function for max node
    def max_prune(self, passed_back_val, child_iter):
    	prune = False
    	# max node chooses the larger value between the passed_back_val and the value it records(max by far)
    	self.value = max(self.value, passed_back_val)
    	# check if prune the followed siblings by comparing its value with beta
    	prune = True if self.value > self.beta else False
    	# update alpha if passed_back_val is larger than alpha
    	self.alpha = max(self.alpha, passed_back_val)
    	# if prune is identified as True above, prune the siblings
    	if prune:
    		for child in self.children[child_iter+1:]:
    			child.prunable = True

    # function for min node, the counterpart of max_prune
    def min_prune(self, passed_back_val, child_iter):
    	prune = False
    	# min node chooses the lower value between the passed_back_val and the value it records(min by far)
    	self.value = min(self.value, passed_back_val)
    	# check if prune the followed siblings by comparing its value with alpha
    	prune = True if self.value < self.alpha else False
    	# update beta if passed_back_val is lower than beta
    	self.beta = min(self.beta, passed_back_val)
    	# if prune is identified as True above, prune the siblings
    	if prune:
    		for child in self.children[child_iter+1:]:
    			child.prunable = True

''' construct the tree '''
root_max_node = MinimaxNode(value=float('-inf'), is_max=True)

# add 3 min nodes to the root_max_node
for _ in range(3):
	root_max_node.children.append(MinimaxNode(value=float('inf'), is_max=False, parent=root_max_node))

# add 2 max nodes to each of the second layer min nodes
for child in root_max_node.children:
	for _ in range(2):
		child.children.append(MinimaxNode(value=float('-inf'), is_max=True, parent=child))

# add 2 terminal nodes with specified values to each of the third layer max nodes
user_input_value_iter = 0
# helper variable to record all terminal nodes for get_prunable_node_terminal_node_indexes() later
terminal_nodes = []
for root_child in root_max_node.children:
	for grand_root_child in root_child.children:
		for _ in range(2):
			terminal_node = MinimaxNode(value=int(user_inputs[user_input_value_iter]), is_terminal=True, parent=grand_root_child)
			grand_root_child.children.append(terminal_node)
			terminal_nodes.append(terminal_node)
			user_input_value_iter += 1

''' Done construct the tree '''

# recursively use DFS to prune nodes based on alpha beta pruning
# it should acceipt a root node and return the value to pass back
# reference - https://www.youtube.com/watch?v=zp3VMe0Jpf8
def alpha_beta_prune(node):
	# base case - return the value to be passed back if a terminal node is met
	if node.is_terminal:
		return node.value
	else:
		if node.children:
			for child_iter in range(len(node.children)):
				child = node.children[child_iter]
				# if this node is marked prunable during comparison with alpha or beta by a MIN or MAX node, stop exploring the siblings and pass back the value of its parent node
				if child.prunable:
					get_prunable_node_terminal_node_indexes(child)
					return node.value
				# pass down alpha and beta
				child.alpha, child.beta = node.alpha, node.beta
				# pass up the value
				passed_back_val = alpha_beta_prune(child)
				node.max_prune(passed_back_val, child_iter) if node.is_max else node.min_prune(passed_back_val, child_iter)
				# if all the children nodes have been dealt with, pass up its parent value
				if child_iter == len(node.children) - 1:
					return node.value

# list to store the indexes of the pruned terminal nodes
pruned_terminal_nodes_indexes = set()

# using DFS to retrieve pruned terminal nodes indexes
def get_prunable_node_terminal_node_indexes(node):
	global pruned_terminal_nodes_indexes
	if node.is_terminal:
		pruned_terminal_nodes_indexes.add(terminal_nodes.index(node))
		return
	else:
		for child in node.children:
			get_prunable_node_terminal_node_indexes(child)

# run alpha beta pruning
alpha_beta_prune(root_max_node)
print(' '.join(str(ind) for ind in sorted(pruned_terminal_nodes_indexes)))
