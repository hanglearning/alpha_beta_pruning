# alpha, beta value ref - https://www.youtube.com/watch?v=xBXHtz4Gbdo
# another ref - https://www.youtube.com/watch?v=zp3VMe0Jpf8

import sys

# get user input
user_input_numbers = sys.argv[2].split(' ')
# used to store the nodes to be pruned. Note: may not be the terminal nodes
prune_list = []

# we treat MIN and MAX nodes as two different agents
class Agent:

    def __init__(self, parent=None):
        self.val = None
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.is_max = None
        self.children = []
        self.is_terminal = False
        self.parent = parent
        self.prune = False

    # init a max agent
    def init_max(self):
        self.is_max = True
        self.val = float('-inf')

    # init a min agent
    def init_min(self):
        self.is_max = False
        self.val = float('inf')

    # init a terminal agent
    def init_terminal(self, val):
        self.val = val
        self.is_terminal = True

    # used for node to pass down alpha and beta values to its children
    def accept_pass_down_values(self, alpha=None, beta=None):
        self.alpha = alpha
        self.beta = beta

    # MAX agent's jobs
    def do_max(self, passed_up_val):
        parent = self.parent
        prune = False
        # 1) compare the val of this MAX agent with the passed in val from its children and update is necessary
        if passed_up_val > parent.val:
            parent.val = passed_up_val
        # 2) decide if prune by comparing beta, which is the value the MIN node above would force at this moment
        if parent.val > parent.beta:
            prune = True
        # 3) decide if update alpha
        if parent.val > parent.alpha:
            parent.alpha = parent.val
        # mark all the followed siblings in its parent's children list as prunable if prune==True 
        if prune:
            this_node_index = parent.children.index(self)
            GameTree.mark_prune(parent.children, this_node_index)      
    
    # MIN agent's jobs
    def do_min(self, passed_in_val):
        parent = self.parent
        prune = False
        # 1) compare val
        if passed_in_val < parent.val:
            parent.val = passed_in_val
        # 2) decide if prune by comparing alpha, which is the value the MAX would force
        if parent.val < parent.alpha:
            prune = True
        # 3) decide if update beta
        if parent.val < parent.beta:
            parent.beta = parent.val
        # mark prune
        if prune:
            this_node_index = parent.children.index(self)
            GameTree.mark_prune(parent.children, this_node_index)
    

class GameTree:

    # entry point of the algorithm - recursively using DFS to pass up val and pass down alpha and beta, and decide if prune by the agent type
    @staticmethod
    def run_minimax_prune(root):
        global prune_list
        if root.is_terminal:
            return root.val
        else:
            if root.children:
                for child_iter in range(len(root.children)):
                    child = root.children[child_iter]
                    if child.prune:
                        # if this node has been marked as prune, stop exploring and return its parent val to pass up
                        prune_list.append(child)
                        return root.val
                    else:
                        # node accept alpha and beta from parent
                        child.accept_pass_down_values(alpha=root.alpha, beta=root.beta)
                        # recursive DFS to pass up val
                        passed_up_val = GameTree.run_minimax_prune(child)
                        # do MAX or MIN jobs based on parent agent type
                        child.do_max(passed_up_val) if root.is_max else child.do_min(passed_up_val)
                        # if all the children nodes have been explored, which means their parent is done explored, pass up its parent val
                        if child_iter == len(root.children) - 1:
                            return root.val

    # mark followed siblings as prunable
    @staticmethod
    def mark_prune(children, this_child_index):
        # if this_child_index != len(children) - 1: should not be necessary
        for node in children[this_child_index+1:]:
            node.prune = True

''' Tree Construction '''
# construct the root node
root_agent = Agent()
root_agent.init_max()

# add 3 MIN children to root agent
for _ in range(3):
    second_layer_agent = Agent(parent=root_agent)
    second_layer_agent.init_min()
    root_agent.children.append(second_layer_agent)

# add 2 MAX children to each child of the root MAX agent
for min_child in root_agent.children:
    for _ in range(2):
        third_layer_agent = Agent(parent=min_child)
        third_layer_agent.init_max()
        min_child.children.append(third_layer_agent)

# helper var to extract the indexes of the pruned terminal nodes at line 166
terminal_nodes = []
# add 2 terminal nodes with the input value to each of the third layer MAX agent, and also add these terminal nodes to the fringe
terminal_node_index = 0
for min_child in root_agent.children:
    for max_child in min_child.children:
        for _ in range(2):
            terminal_node = Agent(parent=max_child)
            terminal_node.init_terminal(int(user_input_numbers[terminal_node_index]))
            max_child.children.append(terminal_node)
            terminal_node_index += 1
            terminal_nodes.append(terminal_node)

# run the algorithm
GameTree.run_minimax_prune(root_agent)

# used to record the terminal nodes get pruned
pruned_terminal_nodes = set()

# DFS pre_order_traversal to extract pruned_terminal_nodes from nodes in prune_list
def pre_order_traversal(node):
    global pruned_terminal_nodes
    if node.is_terminal:
        pruned_terminal_nodes.add(node)
        return
    for child in node.children:
        pre_order_traversal(child)

def get_all_prune_terminal_indexes():    
    for node in prune_list:
        pre_order_traversal(node)
    # after pruned_terminal_nodes is filled, extract the indexes of the pruned terminal nodes
    prune_indexes = []
    for node in pruned_terminal_nodes:
        prune_indexes.append(terminal_nodes.index(node))
    print(' '.join(str(v) for v in sorted(prune_indexes)))

# print the result
get_all_prune_terminal_indexes()