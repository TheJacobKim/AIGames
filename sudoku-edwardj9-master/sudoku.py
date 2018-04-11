from __future__ import print_function
import random, copy

class Grid:
	def __init__(self, problem):
		self.spots = [(i, j) for i in range(1,10) for j in range(1,10)]
		self.domains = {}
		#Need a dictionary that maps each spot to its related spots
		self.peers = {} 
		self.parse(problem)

	def parse(self, problem):
		for i in range(0, 9):
			for j in range(0, 9):
				c = problem[i*9+j] 
				if c == '.':
					self.domains[(i+1, j+1)] = range(1,10)
				else:
					self.domains[(i+1, j+1)] = [ord(c)-48]
				self.peers.setdefault((i+1,j+1), set([]))

				self.peers[(i+1,j+1)].update([(x,j+1) for x in range(1,10) if x != (i+1)])	#Same row
				self.peers[(i+1,j+1)].update([(i+1,x) for x in range(1,10) if x != (j+1)])	#Same column
				
				if i < 3:
					if j < 3:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(1,4) for z in range(1,4)])
					elif j < 6:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(1,4) for z in range(4,7)])
					else:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(1,4) for z in range(7,10)])
				elif i < 6:
					if j < 3:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(4,7) for z in range(1,4)])
					elif j < 6:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(4,7) for z in range(4,7)])
					else: 
						self.peers[(i+1,j+1)].update([(x,z) for x in range(4,7) for z in range(7,10)])
				elif i < 9:
					if j < 3:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(7,10) for z in range(1,4)])
					elif j < 6:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(7,10) for z in range(4,7)])
					else:
						self.peers[(i+1,j+1)].update([(x,z) for x in range(7,10) for z in range(7,10)])

	def display(self):
		for i in range(0, 9):
			for j in range(0, 9):
				d = self.domains[(i+1,j+1)]
				if len(d) == 1:
					print(d[0], end='')
				else: 
					print('.', end='')
				if j == 2 or j == 5:
					print(" | ", end='')
			print()
			if i == 2 or i == 5:
				print("---------------")

#Solver for task 1
class Solver:
	def __init__(self, grid):
		#sigma is the assignment function
		self.sigma = {}
		self.grid = grid
		self.unassignedVars = []
		self.setup()

	def setup(self):
		for i in range(0, 9):
			for j in range(0, 9):
				if len(self.grid.domains[(i+1, j+1)]) > 1:
					self.unassignedVars.append((i+1, j+1))
				else:
					self.sigma[(i+1, j+1)] = self.grid.domains[(i+1,j+1)][0]

	def solve(self):
		return self.search(self.sigma)

	def search(self, sigma):
		if self.isComplete(sigma):
			self.sigma = sigma
			return sigma

		var = self.getUnassigned(sigma)
		for val in self.grid.domains[var]:
			if self.consistent(var, val, sigma):
				sigma[var] = val
				(inferences, valid) = self.infer(copy.deepcopy(sigma), var, val, {})
				if valid:
					sigma.update(inferences)
					result = self.search(sigma)
					if result:
						return result
					for key in inferences.keys():
						del sigma[key]
				del sigma[var]
		return False

	def getUnassigned(self, sigma):
		#Find first unassigned spot
		for i in range(1, 10):
			for j in range(1, 10):
				if (i,j) not in sigma:
					return (i,j)
		return False


	def consistent(self, spot, value, sigma):
		for peer in self.grid.peers[spot]:
			if ((len(self.grid.domains[peer]) == 1 and self.grid.domains[peer][0] == value) or (peer in sigma and sigma[peer] == value)):
				return False
		return True

	def infer(self, sigma, var, val, inferences):
		#Decrement domains of peers
		for peer in self.grid.peers[var]:
			if peer not in sigma and val in self.grid.domains[peer]:
				domainList = list(self.grid.domains[peer])
				for pPeer in self.grid.peers[peer]:
					if pPeer in sigma and sigma[pPeer] in domainList:
						domainList.remove(sigma[pPeer])
				#We can make an inference
				if len(domainList) == 1:
					peerVal = domainList[0]
					sigma[peer] = peerVal
					inferences[peer] = peerVal
					#Infer and insure valid
					(newInfereces, valid) = self.infer(sigma, peer, peerVal, inferences)
					if not valid:
						return (inferences, False)
				elif len(domainList) < 1:
					return (inferences, False)
		return (inferences, True)

	def isComplete(self, sigma):
		return len(sigma) == 81

	#Print solution
	def displaySolved(self):
		for i in range(0, 9):
			for j in range(0, 9):
				d = self.grid.domains[(i+1,j+1)]
				if len(d) == 1:
					print(d[0], end='')
				elif (i+1,j+1) in self.sigma: 
					print(self.sigma[(i+1,j+1)], end='')
				if j == 2 or j == 5:
					print(" | ", end='')
			print()
			if i == 2 or i == 5:
				print("---------------")

#Solver for task 2, note that due to implementation details, this is slower than task 1
class Solver2:
	def __init__(self, grid):
		#sigma is the assignment function
		self.sigma = {}
		self.grid = grid
		self.unassignedVars = []
		self.activeDomains = {}
		self.setup()

	#Initialize vars
	def setup(self):
		for i in range(0, 9):
			for j in range(0, 9):
				if len(self.grid.domains[(i+1, j+1)]) > 1:
					self.unassignedVars.append((i+1, j+1))
				else:
					self.sigma[(i+1, j+1)] = self.grid.domains[(i+1,j+1)][0]
		for var in self.unassignedVars:
			currentDomain = list(self.grid.domains[var])
			self.activeDomains[var] = set(currentDomain)

		#Setup active domains
		for var in self.sigma:
			for peer in self.grid.peers[var]:
				if peer in self.unassignedVars:
					self.activeDomains[peer].discard(self.sigma[var])

	def solve(self):
		return self.search(self.sigma)

	#Backtrack
	def search(self, sigma):
		if self.isComplete(sigma):
			self.sigma = sigma
			return sigma

		var = self.getUnassigned(sigma)
		#Copy so can iterate through fixed length set
		for val in copy.copy(self.activeDomains[var]):
			if self.consistent(var, val, sigma):
				sigma[var] = val
				#Prune all peers
				self.pruneDomains(var, val)
				(inferences, valid) = self.infer(copy.deepcopy(sigma), var, val, {})
				if valid:
					sigma.update(inferences)
					result = self.search(sigma)
					if result:
						return result
					for key in inferences.keys():
						del sigma[key]
				del sigma[var]
				#add peers back
				self.unpruneDomains(var, val)
		return False

	def pruneDomains(self, var, val):
		for peer in self.grid.peers[var]:
			if peer in self.activeDomains:
				self.activeDomains[peer].discard(val)

	def unpruneDomains(self, var, val):
		for peer in self.grid.peers[var]:
			if peer in self.activeDomains:
				self.activeDomains[peer].add(val)

	def getUnassigned(self, sigma):
		#Find first unassigned spot
		for i in range(1, 10):
			for j in range(1, 10):
				if (i,j) not in sigma:
					return (i,j)
		return False

	def consistent(self, spot, value, sigma):
		for peer in self.grid.peers[spot]:
			if ((len(self.grid.domains[peer]) == 1 and self.grid.domains[peer][0] == value) or (peer in sigma and sigma[peer] == value)):
				return False
		return True

	def infer(self, sigma, var, val, inferences):
		#Decrement domains of peers
		for peer in self.grid.peers[var]:
			if peer not in sigma and val in self.grid.domains[peer]:
				domainList = list(self.activeDomains[peer])
				for pPeer in self.grid.peers[peer]:
					if pPeer in sigma and sigma[pPeer] in domainList:
						domainList.remove(sigma[pPeer])
				#We can make an inference
				if len(domainList) == 1:
					peerVal = domainList[0]
					sigma[peer] = peerVal
					inferences[peer] = peerVal
					#Infer and insure valid
					(newInfereces, valid) = self.infer(sigma, peer, peerVal, inferences)
					if not valid:
						return (inferences, False)
				elif len(domainList) < 1:
					return (inferences, False)
		return (inferences, True)

	def isComplete(self, sigma):
		return len(sigma) == 81

	#Print solution
	def displaySolved(self):
		for i in range(0, 9):
			for j in range(0, 9):
				d = self.grid.domains[(i+1,j+1)]
				if len(d) == 1:
					print(d[0], end='')
				elif (i+1,j+1) in self.sigma: 
					print(self.sigma[(i+1,j+1)], end='')
				if j == 2 or j == 5:
					print(" | ", end='')
			print()
			if i == 2 or i == 5:
				print("---------------")

#Task 3, SAT Solver
class Solver3:
	def __init__(self, grid):
		#sigma is the assignment function
		self.sigma = {}
		self.grid = grid

	def encodeCNF(self):
		file = open("cnf/encoded.cnf", "w+")
		file.write("p cnf 729 8846\n")
		filledCount = 0
		for i in range(0, 9):
			for j in range(0, 9):
				spot = (i+1, j+1)
				if(len(self.grid.domains[spot]) == 1):
					numKey = ((i*9)+j)
					filledCount+=1
					file.write(str((numKey*9)+self.grid.domains[spot][0]) + " 0\n")
				
		for i in range(0,81):
			for j in range(1, 10):
				file.write(str((9*i)+j)+" ")
			file.write("0\n")
		
		#Constraints on rows
		for i in range(0, 729, 81):
			#Every value for spot in row
			for j in range(i,i+9):
				startPos = j+1
				for k in range(startPos, startPos+81, 9):
					for l in range(k+9, startPos + 81, 9):
						file.write(str(-k) + " " + str(-l) + " 0\n")

		#Constraints on columns
		for i in range(0, 81):
			for j in range(0, 9):
				startPos = i+(j*81)+1
				for k in range(startPos+81, 730, 81):
					file.write(str(-startPos) + " " + str(-k) + " 0\n")

		file.close()

		



		
easy = ["..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..",
"2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3"]

hard = ["4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......",
 "52...6.........7.13...........4..8..6......5...........418.........3..2...87....."]

print("====Problem====")
g = Grid(hard[0])
#Display the original problem
g.display()
s = Solver(g)

if s.solve():
	print("====Solution===")
	#Display the solution
	#Feel free to call other functions to display
	s.displaySolved()
else:
	print("==No solution==")

