#Author: Toluwanimi Salako
from collections import defaultdict
import random
import sys
sys.path.append(r'\ConnectKSource_python')
import ConnectKSource_python.board_model as boardmodel

team_name = "StudentAI-Default" #TODO change me
DIRECTIONS = [(1,0), (1,1), (0,1), (-1,1)]
# STREAKPOINTS = {4:300000, 3:3000, 2:650, 1:}

def oppoPlayer(player):
	return 1 if player == -1 else -1

class StudentAI():
	def __init__(self, player, state):
		self.last_move = state.get_last_move()
		self.model = state
		self.width = self.model.get_width()
		self.height = self.model.get_height()
		self.player = player

	def Eval(self, gameboard, move):
		score = [0, 0]
		visited_piece_with_dir = dict()
		for m in gameboard:
			player = gameboard[m]
			if gameboard[m] != 0:
				for x,y in DIRECTIONS:
					streak = 0
					spaces = 0
					if (m not in visited_piece_with_dir or (x, y) not in visited_piece_with_dir[m]):
						if m not in visited_piece_with_dir:
							visited_piece_with_dir[m] = [(x, y)]
						else:
							visited_piece_with_dir[m] += (x, y)
						next1 = (m[0]+x, m[1]+y)
						next2 = (m[0]-x, m[1]-y)
						while(self.inGameboard(next1) and gameboard.get(next1) == player):
							streak += 1
							next1 = (next1[0]+x, next1[1]+y)
						while(self.inGameboard(next1) and gameboard.get(next1) == 0):
							spaces += 1
							next1 = (next1[0]+x, next1[1]+y)
						while(self.inGameboard(next2) and gameboard.get(next2) == player):
			 				streak += 1
			 				next2 = (next2[0]-x, next2[1]-y)
						while(self.inGameboard(next2) and gameboard.get(next2) == 0):
			 				spaces += 1
			 				next2 = (next2[0]-x, next2[1]-y)
						score[player-1] += pow(10, streak) if (streak + spaces >= 4) else 0
		return score[0] - score[1] if self.player == 1 else score[1] - score[0]
	# def Eval(self, gameboard, move):
	# 	opp_fours = self.checkForStreak(gameboard, -self.player, 4)
	# 	opp_threes = self.checkForStreak(gameboard, -self.player, 3)
	# 	opp_twos = self.checkForStreak(gameboard, -self.player, 2)
	# 	my_fours = self.checkForStreak(gameboard, self.player, 4)
	# 	my_threes = self.checkForStreak(gameboard, self.player, 3)
	# 	my_twos = self.checkForStreak(gameboard, self.player, 2)
	#
	# 	if opp_fours > 0:
	# 		return -100000
	# 	else:
	# 		return my_fours*100000 + my_threes*100 + my_twos - (100*opp_threes + 10*opp_twos)
	#
	# def checkForStreak(self, gameboard, player, streak):
	# 	count = 0
	# 	for pos in gameboard.keys():
	# 		if gameboard.get(pos) == player:
	# 			count += self.verticalStreak(pos, gameboard, streak)
	# 			count += self.horizontalStreak(pos, gameboard, streak)
	# 			count += self.diagonalStreak(pos, gameboard, streak)
	# 	return count
	# def verticalStreak(self, pos, gameboard, streak):
	# 	pass
	# def horizontalStreak(self, pos, gameboard, streak):
	# 	pass
	# def diagonalStreak(self, pos, gameboard, streak):
	# 	pass

	def needDefense(self, gameboard, moves):
		streaks = [0, 0]
		defense = None
		for piece in moves:
			s = []
			for x, y in DIRECTIONS:
				# defense detect
				streak = 0
				next1 = (piece[0] + x, piece[1] + y)
				space1 = 0
				next2 = (piece[0] - x, piece[1] - y)
				space2 = 0

				while(self.inGameboard(next1) and gameboard.get(next1) == oppoPlayer(self.player)):
					streak += 1
					next1 = (next1[0]+x, next1[1]+y)
				while(self.inGameboard(next1) and gameboard.get(next1) == 0):
					space1 += 1
					next1 = (next1[0]+x, next1[1]+y)

				while(self.inGameboard(next2) and gameboard.get(next2) == oppoPlayer(self.player)):
					streak += 1
					next2 = (next2[0]-x, next2[1]-y)
				while(self.inGameboard(next2) and gameboard.get(next2) == 0):
					space2 += 1
					next2 = (next2[0]-x, next2[1]-y)
				s.append(streak)
				if space1 > 0 and space2 > 0 and streak + space1 + space2 >= 4 and streak >= 3:
					# 活K-2
					print("三三")
					if(streak > streaks[1]):
						defense = piece
						streaks[1] = streak
				elif streak + space1 + space2 >=4 and streak >= 4:
					# 死k-1
					print("四")
					if(streak > streaks[1]):
						defense = piece
						streaks[1] = streak
				streak_p = 0
				next1_p = (piece[0] + x, piece[1] + y)
				space1_p = 0
				next2_p = (piece[0] - x, piece[1] - y)
				space2_p = 0
				while(self.inGameboard(next1_p) and gameboard.get(next1_p) == (self.player)):
					streak_p += 1
					next1_p = (next1_p[0]+x, next1_p[1]+y)
				while(self.inGameboard(next1_p) and gameboard.get(next1_p) == 0):
					space1_p += 1
					next1_p = (next1_p[0]+x, next1_p[1]+y)
				while(self.inGameboard(next2_p) and gameboard.get(next2_p) == (self.player)):
					streak_p += 1
					next2_p = (next2_p[0]-x, next2_p[1]-y)
				while(self.inGameboard(next2_p) and gameboard.get(next2_p) == 0):
					space2_p += 1
					next2_p = (next2_p[0]-x, next2_p[1]-y)
				if streak_p >= 4:
					return piece
				if space1_p > 0 and space2_p > 0 and streak_p + space1_p + space2_p >= 4 and streak_p >= 3:
					# 活K-2
					if(streak_p > streaks[1]):
						streaks[0] = streak_p
				elif streak + space1 + space2 >=4 and streak >= 4:
					# 死k-1
					if(streak > streaks[1]):
						streaks[0] = streak_p
			if(s.count(2) >= 2):
				# need revise
				streaks[1] = 3
				defense = piece
		return defense if streaks[1] > streaks[0] else None




	def inGameboard(self, pos):
		if(pos[0] < 0 or pos[1] < 0 or pos[0] > self.width-1 or pos[1] > self.height-1):
			return False
		return True

	def hasWinner(self, gameboard, player):
		for m in gameboard:
			if(gameboard[m] == player):
				for x,y in DIRECTIONS:
					streak = 0
				next1 = (m[0]+x, m[1]+y)
				next2 = (m[0]-x, m[1]-y)
				while(self.inGameboard(next1) and gameboard.get(next1) == player):
					streak += 1
					next1 = (next1[0]+x, next1[1]+y)
				while(self.inGameboard(next2) and gameboard.get(next2) == player):
					streak += 1
					next2 = (next2[0]-x, next2[1]-y)
				if streak == 4:
					return True
		return False


	def ab_pruning(self, moves, gameboard, depth):
		alpha = -2147483648
		beta = 2147483647
		piece = None
		index = 0
		defense = self.needDefense(gameboard, moves)
		if(defense != None):
			return defense
		for move in moves:
			temp = moves[:]
			temp.pop(index)
			gameboard[move] = self.player
			(alpha, piece) = max((alpha, piece), (self.min_value(gameboard, alpha, beta, depth-1, temp, move), move))
			index += 1
			gameboard[move] = 0
		return piece

	def max_value(self, gameboard, alpha, beta, depth, moves, m):
		if(depth == 0):
			return self.Eval(gameboard, m)
		index = 0
		for move in moves:
			temp = moves[:]
			temp.pop(index)
			gameboard[move] = self.player
			alpha = max(alpha, self.min_value(gameboard, alpha, beta, depth - 1, temp, move))
			index += 1
			gameboard[move] = 0
			if(alpha >= beta):
				return 2147483647
		return alpha

	def min_value(self, gameboard, alpha, beta, depth, moves, m):
		if(depth == 0):
			return self.Eval(gameboard, m)
		index = 0
		for move in moves:
			temp = moves[:]
			temp.pop(0)
			gameboard[move] = oppoPlayer(self.player)
			beta = min(beta, self.max_value(gameboard, alpha, beta, depth - 1, temp, move))
			gameboard[move] = 0
			index += 1
			if(alpha >= beta):
				return -2147483647
		return beta

	def make_move(self, deadline):
		'''Write AI Here. Return a tuple (col, row)'''
		width = self.model.get_width()
		height = self.model.get_height()
		spaces = defaultdict(int)

		for i in range(width):
			for j in range(height):
				spaces[(i,j)] = self.model.get_space(i, j)
		moves = sorted([k for k in spaces.keys() if spaces[k] == 0])
		return self.ab_pruning(moves, spaces, 3)



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
