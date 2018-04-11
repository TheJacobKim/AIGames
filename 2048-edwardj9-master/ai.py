from __future__ import print_function
import copy, random
MOVES = {0:'up', 1:'left', 2:'down', 3:'right'}

class State:
	"""game state information"""
	#Hint: probably need the tile matrix, which player's turn, score, previous move
	def __init__(self, matrix, player, score, pre_move):
		self.matrix = matrix  
		self.player = player
		self.score = score
		self.pre_move = pre_move
		self.children = []
	def highest_tile(self):
		"""Find max value in 2D matrix"""
		highest = 0;
		for row in self.matrix:
			for val in row:
				highest = max(highest, val)
		return highest 

class Gametree:
	"""main class for the AI"""
	def __init__(self, root, depth): 
		self.root = State(root, 0, 0, 0) #Blank game state
		self.depth = depth
		self.player = 0
	def grow_once(self, state):
		"""Grow the tree one level deeper"""
		#User turn
		if self.player == 0:
			for i in MOVES.keys():	#for every possible move
				nextSim = Simulator(state.matrix, state.score)	
				if(nextSim.move(i)): #If can move in that direction
						nextState = State(nextSim.matrix, 1, nextSim.score, i)
						state.children.append(nextState)
		
		#Computer turn
		else:
			#Look for every blank slate
			for i in range(len(state.matrix)):
				for j in range(len(state.matrix[i])):
					if state.matrix[i][j] == 0:
						nextState = State(copy.deepcopy(matrix), 0, state.score, state)
						nextState.matrix[i][j] = 2
						state.children.append(nextState)
	def grow(self, state, height):
		"""Grow the full tree from root"""
		if height == 0:
			return
		#Create level by level
		self.grow_once(state)
		#Expand every child of current level
		for x in range(len(state.children)):
			self.grow(state.children[x], height-1)
	'''Returns tuple (a,b) with a as highest score and b as resulting move'''
	def minimax(self, state):
		"""Compute minimax values on the tree"""
		if not state.children:
			return (state.score + state.highest_tile(), state.pre_move)
		#If user move/max player
		if state.player == 0:
			best=-1
			move=-1
			#Find best path
			for child in state.children:
				candidate = self.minimax(child)
				if candidate[0] > best:
					best = candidate[0]
					move = candidate[1]
			return (best, move)
		#If computer/chance player
		elif state.player == 1:
			value = 0
			for child in state.children:
				value = value + self.minimax(child)[0]*(1/(len(state.children)))
			return (value, state.pre_move)
	def compute_decision(self):
		"""Derive a decision"""
		self.grow(self.root, self.depth)
		result = self.minimax(self.root)
		decision = result[1]
		#Should also print the minimax value at the root
		print("Minimax Value:" + str(result[0]))
		print(MOVES[decision])
		return decision

class Simulator:
	"""Simulation of the game"""
	def __init__(self, matrix, score):
		self.score = score
		self.matrix = copy.deepcopy(matrix)
		self.board_size = 4
	'''Updated to also return whether or not it moved in that direction'''
	def move(self, direction):
		moved = False
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		if self.canMove():
			self.moveTiles()
			self.mergeTiles()
			moved = True
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()
		return moved
	def moveTiles(self):
		tm = self.matrix
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, self.board_size - 1):
						tm[i][k] = tm[i][k + 1]
					tm[i][self.board_size - 1] = 0
	def mergeTiles(self):
		tm = self.matrix
		for i in range(0, self.board_size):
			for k in range(0, self.board_size - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.score += tm[i][k]
					self.moveTiles()
	def checkIfCanGo(self):
		tm = self.matrix
		for i in range(0, self.board_size ** 2):
			if tm[int(i / self.board_size)][i % self.board_size] == 0:
				return True		
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				if tm[i][j] == tm[i][j + 1]:
					return True
				elif tm[j][i] == tm[j + 1][i]:
					return True
		return False
	def canMove(self):
		tm = self.matrix
		for i in range(0, self.board_size):
			for j in range(1, self.board_size):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False
	def rotateMatrixClockwise(self):	
		tm = self.matrix
		for i in range(0, int(self.board_size/2)):
			for k in range(i, self.board_size- i - 1):
				temp1 = tm[i][k]
				temp2 = tm[self.board_size - 1 - k][i]
				temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
				temp4 = tm[k][self.board_size - 1 - i]
				tm[self.board_size - 1 - k][i] = temp1
				tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
				tm[k][self.board_size - 1 - i] = temp3
				tm[i][k] = temp4
	def convertToLinearMatrix(self):
		m = []
		for i in range(0, self.board_size ** 2):
			m.append(self.matrix[int(i / self.board_size)][i % self.board_size])
		m.append(self.score)
		return m

	def highest_tile(self):
		"""Return the highest tile here (just a suggestion, you don't have to)"""
		highest = 0;
		for row in self.matrix:
			for val in row:
				highest = max(highest, val)
		return highest 
