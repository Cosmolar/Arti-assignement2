# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *
import math


PACM_TILE	= '$'
FOOD_TILE	= '@'
WALL_TILE	= 'x'
FREE_TILE	= ' '

#################
# Problem class #
#################
class Pacmen(Problem):
	def successor(self, state):
		for possibility in [convert_to_base(i, 4, len(state.pacmens)) for i in range(0, 4**len(state.pacmens))]:
			new_pacmens = state.update_pacmens(possibility)
			if(state.can_move(new_pacmens)):
				yield (possibility, state.update_state(new_pacmens))

	def goal_test(self, state):
		return len(state.foods) == 0


###############
# State class #
###############
class State:
	def __init__(self, grid, pacmens=None, foods=None):
		self.nbr = len(grid)
		self.nbc = len(grid[0])
		self.grid = grid
		if pacmens:	self.pacmens = pacmens
		else:		self.pacmens = self.list_tiles(PACM_TILE)
		if foods:	self.foods = foods
		else:		self.foods = self.list_tiles(FOOD_TILE)
		
	def list_tiles(self, type):
		results = []
		for x in range(0, self.nbc):
			for y in range(0, self.nbr):
				if self.grid[y][x] == type:
					results.append((x, y))
		return results
					
					
	def update_pacmens(self, moves):
		deltas = self.compute_deltas(moves)
		return [(self.pacmens[i][0] + deltas[i][0], self.pacmens[i][1] + deltas[i][1]) for i in range(0, len(deltas))]
	
	def compute_deltas(self, moves):
		deltas = []
		for move in moves:
			if		move == 0: deltas.append((0, -1)) # up
			elif	move == 1: deltas.append((1, 0)) # right
			elif	move == 2: deltas.append((0, 1)) # down
			elif	move == 3: deltas.append((-1, 0)) # left
		return deltas
		
	def can_move(self, new_pacmens):
		for new_pacmen in new_pacmens:
			if		new_pacmen[0] < 0 or new_pacmen[0] >= self.nbc or new_pacmen[1] < 0 or new_pacmen[1] >= self.nbr: return False
			elif	self.grid[new_pacmen[1]][new_pacmen[0]] == WALL_TILE: return False
		return True
		
	def update_state(self, new_pacmens):
		new_grid = [row[:] for row in self.grid]
		new_foods = [food for food in self.foods]
		for old_pacmen, new_pacmen in zip(self.pacmens, new_pacmens):
			if new_grid[new_pacmen[1]][new_pacmen[0]] == FOOD_TILE:
				new_foods.remove(new_pacmen)
			new_grid[old_pacmen[1]][old_pacmen[0]] = FREE_TILE
			new_grid[new_pacmen[1]][new_pacmen[0]] = PACM_TILE
		return State(new_grid, new_pacmens, new_foods)

		
	def __str__(self):
		s = ""
		for a in range(nsharp):
			s = s+"#"
		s = s + '\n'
		for i in range(0, self.nbr):
			s = s + "# "
			for j in range(0, self.nbc):
				s = s + str(self.grid[i][j]) + " "
			s = s + "#"
			if i < self.nbr:
				s = s + '\n'
		for a in range(nsharp):
			s = s+"#"
		return s

	def __eq__(self, other_state):
		return self.pacmens == other_state.pacmens and self.foods == other_state.foods

	def __hash__(self):
		return hash(str(self.pacmens)) + hash(str(self.foods))



######################
# Auxiliary function #
######################
def readInstanceFile(filename):
	lines = [[char for char in line.rstrip('\n')[1:][:-1]] for line in open(filename)]
	nsharp = len(lines[0]) + 2
	lines = lines[1:len(lines)-1]
	n = len(lines)
	m = len(lines[0])
	grid_init = [[lines[i][j] for j in range(1, m, 2)] for i in range(0, n)]
	return grid_init,nsharp
	
def convert_to_base(value, base, size):
	results = [0 for x in range(0, size)]
	pos = 0
	while value > 0:
		results[len(results) - pos - 1] = value % base
		value = value // base
		pos += 1
	return results


######################
# Heuristic function #
######################
def heuristic(node):
	if(len(node.state.foods) == 0):
		return 0.0
	closest_pacmens_dist = [get_closest_pacmen_dist(node.state.pacmens, food) for food in node.state.foods]
	return max(closest_pacmens_dist)

def get_closest_pacmen_dist(pacmens, food):
	return min([math.sqrt((food[0] - pacmen[0])**2 + (food[1] - pacmen[1])**2) for pacmen in pacmens])

#####################
# Launch the search #
#####################
grid_init,nsharp = readInstanceFile(sys.argv[1])
init_state = State(grid_init)

problem = Pacmen(init_state)

node = astar_graph_search(problem,heuristic)

# example of print
path = node.path()
path.reverse()

print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()