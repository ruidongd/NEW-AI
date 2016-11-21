#Author: Toluwanimi Salako
from collections import defaultdict
import random
import sys
sys.path.append(r'\ConnectKSource_python')
import ConnectKSource_python.board_model as boardmodel

team_name = "StudentAI-Default" #TODO change me

class StudentAI():
	def __init__(self, player, state):
		self.last_move = state.get_last_move()
		self.model = state
		self.player = player

	def Eval(self, gameboard):
		score = [0, 0]
		visited_piece_with_dir = dict()
		directions = [(1,0), (1,1), (0,1), (-1,1)]
		for m in gameboard:
			player = gameboard[m]
			if gameboard[m] != 0:
				for x,y in directions:
					streak = 0
					if (m not in visited_piece_with_dir or (x, y) not in visited_piece_with_dir[m]):
						if m not in visited_piece_with_dir:
							visited_piece_with_dir[m] = [(x, y)]
						else:
							visited_piece_with_dir[m] += (x, y)
						next1 = (m[0]+x, m[1]+y)
						next2 = (m[0]-x, m[1]-y)
						while(next1 in gameboard and gameboard[next1] == player):
							streak += 1
							next1 = (next1[0]+x, next1[1]+y)
						while(next2 in gameboard and gameboard[next2] == player):
			 				streak += 1
			 				next2 = (next2[0]-x, next2[1]-y)
						score[player-1] += pow(10, streak)
		return score[0] - score[1] if self.player == 1 else score[1] - score[0]

	def ab_pruning(self, moves, gameboard, depth):
		alpha = -2147483648
		beta = 2147483647
		piece = None
		count = 0
		while count < len(moves):
		# 	# print(moves[0])
			move = moves.pop(0)
			gameboard[move] = self.player
			(alpha, piece) = max((alpha, piece), (self.min_value(gameboard, alpha, beta, depth - 1, moves), move) if depth != 0 else (self.Eval(gameboard), move))
			gameboard[move] = 0
			moves.append(move)
			count += 1
		return piece

	def min_value(self, gameboard, alpha, beta, depth, moves):
		count = 0
		while count < len(moves):
			move = moves.pop(0)
			gameboard[move] = self.player
			alpha = max(alpha, self.min_value(gameboard, alpha, beta, depth - 1, moves)) if depth != 0 else self.Eval(gameboard)
			gameboard[move] = 0
			moves.append(move)
			count += 1
			if alpha > beta: return 2147483647
		return alpha
	def IDS_search(gameboard):
		for depth in range(5):
			pass

	def max_value(self, gameboard, alpha, beta, depth, moves):
		count = 0
		while count < len(moves):
			move = moves.pop(0)
			gameboard[move] = self.player
			beta = min(beta, self.max_value(gameboard, alpha, beta, depth - 1, moves)) if depth != 0 else self.Eval(gameboard)
			gameboard[move] = 0
			moves.append(move)
			count += 1
			if alpha > beta: return -2147483648
		return beta

	def make_move(self, deadline):
		'''Write AI Here. Return a tuple (col, row)'''
		width = self.model.get_width()
		height = self.model.get_height()
		spaces = defaultdict(int)

		for i in range(width):
			for j in range(height):
				spaces[(i,j)] = self.model.get_space(i, j)

		moves = [k for k in spaces.keys() if spaces[k] == 0]
		return self.ab_pruning(moves, spaces, 2)


'''===================================
DO NOT MODIFY ANYTHING BELOW THIS LINE
==================================='''

is_first_player = False
deadline = 0

def make_ai_shell_from_input():
	'''
	Reads board state from input and returns the move chosen by StudentAI
	DO NOT MODIFY THIS
	'''
	global is_first_player
	ai_shell = None
	begin =  "makeMoveWithState:"
	end = "end"

	go = True
	while (go):
		mass_input = input().split(" ")
		if (mass_input[0] == end):
			sys.exit()
		elif (mass_input[0] == begin):
			#first I want the gravity, then number of cols, then number of rows, then the col of the last move, then the row of the last move then the values for all the spaces.
			# 0 for no gravity, 1 for gravity
			#then rows
			#then cols
			#then lastMove col
			#then lastMove row.
			#then deadline.
			#add the K variable after deadline.
			#then the values for the spaces.
			#cout<<"beginning"<<endl;
			gravity = int(mass_input[1])
			col_count = int(mass_input[2])
			row_count = int(mass_input[3])
			last_move_col = int(mass_input[4])
			last_move_row = int(mass_input[5])

			#add the deadline here:
			deadline = -1
			deadline = int(mass_input[6])
			k = int(mass_input[7])
			#now the values for each space.


			counter = 8
			#allocate 2D array.
			model = boardmodel.BoardModel(col_count, row_count, k, gravity)
			count_own_moves = 0

			for col in range(col_count):
				for row in range(row_count):
					model.pieces[col][row] = int(mass_input[counter])
					if (model.pieces[col][row] == 1):
						count_own_moves += model.pieces[col][row]
					counter+=1

			if (count_own_moves % 2 == 0):
				is_first_player = True

			model.last_move = (last_move_col, last_move_row)
			ai_shell = StudentAI(1 if is_first_player else 2, model)

			return ai_shell
		else:
			print("unrecognized command", mass_input)
		#otherwise loop back to the top and wait for proper _input.
	return ai_shell

def return_move(move):
	'''
	Prints the move made by the AI so the wrapping shell can input it
	DO NOT MODIFY THIS
	'''
	made_move = "ReturningTheMoveMade";
	#outputs made_move then a space then the row then a space then the column then a line break.
	print(made_move, move[0], move[1])

def check_if_first_player():
	global is_first_player
	return is_first_player

if __name__ == '__main__':
	'''
	DO NOT MODIFY THIS
	'''
	print ("Make sure this program is ran by the Java shell. It is incomplete on its own. :")
	go = True
	while (go): #do this forever until the make_ai_shell_from_input function ends the process or it is killed by the java wrapper.
		ai_shell = make_ai_shell_from_input()
		moveMade = ai_shell.make_move(deadline)
		return_move(moveMade)
		del ai_shell
		sys.stdout.flush()
