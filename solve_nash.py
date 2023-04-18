import numpy as np
import argparse

def find_pure_ne(payoffs):
	""" Finds pure Nash equilibria for a 2 player, 2 action
		game by iteratively verifying that each cell is/isn't
		dominant for each player in the respective situation. 
		For each cell, the row player's payoff must be greater
		or equal to the cell below/above it, and the column
		player's payoff should be greater or equal to the cells
		to the left/right of itself.
	"""

	possible_nes = [(0,0), (0,1), (1,0), (1,1)]
	found_nes = []

	# reshape the payoff matrix
	# new shape of payoff matrix: rows, columns, payoffs
	new_payoffs = np.empty((payoffs[0].size + payoffs[1].size,))
	new_payoffs[0::2] = payoffs[0]
	new_payoffs[1::2] = payoffs[1]
	payoffs = new_payoffs.reshape(-1,2,2)
	
	# loop over all cells
	for p_ne in possible_nes:
		p1, p2 = payoffs[p_ne]
		# get cells to compare the current cell to
		p1_comp = payoffs[:,p_ne[1],0]
		p2_comp = payoffs[p_ne[0],:,1]
		# verify the current cell is dominant
		if p1 == np.max(p1_comp) and p2 == np.max(p2_comp):
			found_nes.append(p_ne)

	return found_nes

def get_ne_outcome(num, den):
	""" Checks mixed NE computation for bad probability form,
		i.e. den < 0, and 0<=num/den<=1. 
	""" 
	if den == 0: # no mixed strategy exists
		return None

	if 0 <= num/den <= 1: # mixed strategy exists
		return abs(num/den) # abs for the py repr of '-0'

	else: # no mixed strategy exists
		return None
 
def find_mixed_ne(payoffs):
	""" Finds mixed Nash equilibria from payoff
		matrix by solving for each player's 
		probability of play, assuming what the other
		player does makes them indifferent to what
		they play.
	"""
	a,b,c,d = payoffs[0]
	e,f,g,h = payoffs[1]

	num_p = h-g
	den_p = e-f-g+h
	p = get_ne_outcome(num_p, den_p)

	num_q = d-b
	den_q = a-c-b+d
	q = get_ne_outcome(num_q, den_q)

	if p is None or q is None:
		return None, None

	return p, q

def parse_game(inp_str):
	""" Parses a string of ints such as a,b,c,d,e,f,g,h
		to a matrix of payoffs [[a b c d] [e f g h]]
	"""
	payoffs = [int(x) for x in inp_str.split(",")]
	payoffs = np.array(payoffs).reshape(2,4)

	return payoffs

def print_table(test_str):
	a,b,c,d,e,f,g,h = test_str.split(",")
	table = f""" Table form:
		| {a}\\{e} | {b}\\{f} |
		|-----|-----|
		| {c}\\{g} | {d}\\{h} |
	"""
	print(table)

def compute_all(test_str):
	""" Computes and prints finitely many Nash equilibria 
		for a 2 player, 2 action game. 
	"""
	print("Payoffs:", test_str)
	print_table(test_str)
	parsed = parse_game(test_str)
	pure = find_pure_ne(parsed)
	print("Pure Nash equilibium :", pure)
	mixed = find_mixed_ne(parsed)
	if None in mixed:
		mixed = "None found!"
	print("Mixed Nash equilibium:", mixed)

def run_tests():
	# a few tests with known NE to test the system
	test = "5,6,2,9,9,3,2,5"
	compute_all(test)
	test = "4,6,6,1,7,3,3,3"
	compute_all(test)
	test = "4,6,6,1,3,7,0,1"
	compute_all(test)
	test = "4,6,6,1,3,7,1,1"
	compute_all(test)
	test = "1,5,0,2,1,0,5,2"
	compute_all(test)

parser = argparse.ArgumentParser()
parser.add_argument("payoffs")

if __name__ == '__main__':
	args = parser.parse_args()
	compute_all(args.payoffs)