from math import sqrt, log
import copy, random
from randplay import *
import numpy as np

class State:
    def __init__(self, grid, player):
        self.grid = grid
        self.piece = player
        self.children = []          #Actual Children
        self.untriedActions = []    #Unexpanded children
        self.parent = None
        self.simulations = 0
        self.grid_count = 19
        self.wins = 0
        self.maxrc = len(grid)-1
        self.game_over = False 
        self.visited = False
        self.prevMove = None

    def getPotential(self, totalSimulations):
        return (self.wins/self.simulations) + 2*(sqrt((2*log(totalSimulations))/self.simulations))

    def initUnexplored(self):
        neighbors = self.get_options(self.grid)
        self.visited = True
        #Iterate through neighbors and add unexpanded states, should only be called once.
        for i,j in neighbors:
            newGrid = copy.deepcopy(self.grid)
            newGrid[i][j] = self.piece
            child = State(newGrid, self.nextMove())
            child.parent = self
            child.prevMove = (i,j)
            child.game_over = self.check_win(i,j, child)
            #Check win here and set game_over status
            self.children.append(child)
            self.untriedActions.append(child)

    def get_options(self, grid):
        #collect all occupied spots
        current_pcs = []
        for r in range(len(grid)):
            for c in range(len(grid)):
                if grid[r][c] == 'b':   #Create a rectangle around black pieces
                    current_pcs.append((r,c))
        #At the beginning of the game, curernt_pcs is empty
        if not current_pcs:
            return [(int(self.maxrc/2), int(self.maxrc/2))]
        #Reasonable moves should be close to where the current pieces are
        #Think about what these calculations are doing
        #min(list, key=lambda x: x[0]) picks the element with the min value on the first dimension
        min_r = max(0, min(current_pcs, key=lambda x: x[0])[0]-1)
        max_r = min(self.maxrc, max(current_pcs, key=lambda x: x[0])[0]+1)
        min_c = max(0, min(current_pcs, key=lambda x: x[1])[1]-1)
        max_c = min(self.maxrc, max(current_pcs, key=lambda x: x[1])[1]+1)
        #Options of reasonable next step moves
        options = []
        for i in range(min_r, max_r+1):
            for j in range(min_c, max_c+1):
                if (not (i, j) in current_pcs) and grid[i][j] == '.':
                    options.append((i,j))
        if len(options) == 0:
            #In the unlikely event that no one wins before board is filled
            #Make white win since black moved first
            self.game_over = True
        return options

    def nextMove(self):
        curPlayer = self.piece
        if curPlayer == 'b':
            curPlayer = 'w'
        else:
            curPlayer = 'b'
        return curPlayer

    def expand(self):
        if self.untriedActions:
            return self.untriedActions.pop()
        print("ERROR, Should have unexpanded children")
        return False

    def isExpanded(self):
        #If untriedActions is empty then fully expanded
        if len(self.untriedActions) == 0:
            return True
        return False

    def check_win(self, r, c, state):
        n_count = self.get_continuous_count(r, c, -1, 0, state)
        s_count = self.get_continuous_count(r, c, 1, 0, state)
        e_count = self.get_continuous_count(r, c, 0, 1, state)
        w_count = self.get_continuous_count(r, c, 0, -1, state)
        se_count = self.get_continuous_count(r, c, 1, 1, state)
        nw_count = self.get_continuous_count(r, c, -1, -1, state)
        ne_count = self.get_continuous_count(r, c, -1, 1, state)
        sw_count = self.get_continuous_count(r, c, 1, -1, state)
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            return True
        return False

    def get_continuous_count(self, r, c, dr, dc, state):
        piece = state.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < state.grid_count and 0 <= new_c < state.grid_count:
                if state.grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result

class MCTS:

    def __init__(self, grid, player):
        self.grid = grid
        self.piece = player
        self.root = None
        
    def uct_search(self):
        if self.root is None:
            self.root = State(copy.deepcopy(self.grid), self.piece)
        for i in range(0, 100): #Computational budget
            candidate = self.tree_policy(self.root)
            winner = self.default_policy(candidate)
            self.backup(candidate, winner)
        bestChild = self.best_child(self.root)
        return bestChild.prevMove

    def tree_policy(self, state):
        curState = state
        while not curState.game_over:  
            #Not visited so initialize all children  
            if not curState.visited:
                curState.initUnexplored()     
            #Unexpanded child is most interesting                     
            if not curState.isExpanded():
                return curState.expand()
            else:
                curState = self.best_child(curState)
        return curState

    #Returns winner of random simulation starting at state
    def default_policy(self, state):
        randSim = Randplay(copy.deepcopy(state.grid), state.piece)
        while not randSim.isOver():
            r,c = randSim.make_move()
            randSim.set_piece(r, c)
            randSim.check_win(r, c)
        return randSim.winner

    def backup(self, state, winner):
        curState = state
        while curState:
            curState.simulations+=1
            #Check if state is a winner
            if winner == curState.piece:
                curState.wins+=1
            curState = curState.parent

    def best_child(self, state):
        bestState = None
        for child in state.children:
            #Haven't simulated this child so most interesting
            if child.simulations == 0:
                return child
            if bestState is None:
                bestState = child
                continue
            if child.getPotential(state.simulations) > bestState.getPotential(state.simulations):
                bestState = child
        #This should only happen if board is completely filled
        if bestState is None:
            print("ERROR!")
            return state
        return bestState

