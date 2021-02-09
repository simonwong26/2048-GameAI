from __future__ import absolute_import, division, print_function
import copy, random, math
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.depth = current_depth
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if len(self.children):
            return False
        return True

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth): 
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth: 
            return 

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)

            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)
            for i in range(4):
                self.simulator.reset(*(node.state))
                moved = self.simulator.move(i)
                if moved:
                    node.children.append((i, Node(self.simulator.get_state(), node.depth+1, CHANCE_PLAYER)))

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            self.simulator.reset(*(node.state))
            tiles = self.simulator.get_open_tiles()
            for tile in tiles:
                curr_state = copy.deepcopy(self.simulator.get_state())
                curr_state[0][tile[0]][tile[1]] = 2 
                node.children.append((None, Node(curr_state, node.depth+1, MAX_PLAYER)))

        # TODO: build a tree for each child of this node
        for child in node.children:
            self.build_tree(child[1])

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return (None, node.state[1])

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            best_value = -math.inf
            for n in node.children:
                _, node_value = self.expectimax(n[1]) 
                if node_value>best_value:
                    best_value = float(node_value)
                    best_dir = n[0]
            return (best_dir, best_value)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0.0
            chance = 1.0/len(node.children)
            for n in node.children:
                _, node_value = self.expectimax(n[1])
                value = value + node_value*chance
            return (None, value)

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    def heuristic(self, node):
        value = 0
        for i in range(self.simulator.board_size):
            for j in range(self.simulator.board_size):
                if i==0:
                    value = value+node.state[0][i][j]*4**(3-j)
                elif i==1:
                    value = value+node.state[0][i][j]*4**(4+j)
                elif i==2:
                    value = value+node.state[0][i][j]*4**(11-j)
                elif i==3:
                    value = value+node.state[0][i][j]*4**(12+j)
        return value

    def expectimax_ec(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0
        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return (None, self.heuristic(node))

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            best_value = -math.inf
            for n in node.children:
                _, node_value = self.expectimax_ec(n[1]) 
                if node_value>best_value:
                    best_value = float(node_value)
                    best_dir = n[0]
            return (best_dir, best_value)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0.0
            chance = 1.0/len(node.children)
            for n in node.children:
                _, node_value = self.expectimax_ec(n[1])
                value = value + node_value*chance
            return (None, value)

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        self.build_tree()
        direction, _ = self.expectimax_ec(self.root)
        return direction
