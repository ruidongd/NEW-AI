#Author: Toluwanimi Salako
from collections import defaultdict
import math
import random
import sys
sys.path.append(r'\ConnectKSource_python')
import ConnectKSource_python.board_model as boardmodel
import time


team_name = "Federer18AI" #TODO change me

class StudentAI():
	def __init__(self, player, state):
		#self.last_move = state.get_last_move()
		self.model = state
		self.player = player
		self.start = time.time()
		self.occupied_pieces=[];

	def make_move(self, deadline):
		'''Write AI Here. Return a tuple (col, row)'''

		return self.IDS(self.model,self.player,self.player)

		# value = max(move.values())
		# for i in move:
		# 	if move[i] == value:
		# 		return i


	def isPossible(self,state,move):
		return state.get_space(move[0],move[1]) == 0

	def isEmpty(self,state):
		for i in range(state.get_width()):
			for j in range(state.get_height()):
				if state.get_space(i,j) != 0:
					return False
		return True

	def isUseful(self,state,col,row):

		if state.get_space(min(col+1,state.get_width()-1),min(state.get_height()-1,row+1)) != 0:
			return True

		if state.get_space(max(col-1,state.get_width()-1),min(state.get_height()-1,row+1)) != 0:
			return True

		if state.get_space(min(state.get_width()-1,col+1),max(state.get_height()-1,row-1)) != 0:
			return True

		if state.get_space(max(state.get_width()-1,col-1),max(state.get_height()-1,row-1)) != 0:
			return True

		else:
			return False

	def movesLeft(self, state):
		moves_list = []
		for i in range(state.get_width()):
			for j in range(state.get_height()):
				if state.get_space(i,j) == 0:
					moves_list.append((i,j))
				else:
					self.occupied_pieces.append((i,j))			#save time here by recording occupied places
		return moves_list

	def occupied(self, state):
		moves_list = []
		for i in range(state.get_width()):
			for j in range(state.get_height()):
				if state.get_space(i,j) != 0:
					moves_list.append((i,j))
		return moves_list

	def IDS(self,state,player,original):
		depth = 1


		best = -math.inf
		place = None
		depth = 1
		moves = self.movesLeft(state)
		state_list = []
		for i in moves:
			num = 0
			temp = self.model.clone().place_piece(i,self.player)
			num = self.search(1,temp,-player,player,-math.inf,math.inf)
			state_list.append(temp)
			if (num > best):
		# 		# print(str(i) + " =>"+ str(num))
				place = temp
				best = num
		state_list.remove(place)
		depth = 3
		score = 0

		new = None

		best_score =  self.search(depth,place, -player, player,-math.inf,math.inf)

		for i in state_list:

			score = self.search(depth,i, -player, player,-math.inf,math.inf)

			if (score > best_score):
				new = i
				best_score = score

		if (new != None):
			state_list.append(place)
			state_list.remove(new)
			place = new

		return place.get_last_move()

	def search(self, depth, state, player,original,alpha,beta):

		moves_left = self.movesLeft(state)

		children = []
		scores = []

		if depth == 0:
			return self.totalValue(state,original,depth)


		if state.has_moves_left() == False:

			return self.totalValue(state,player,original)

		for i in moves_left:


			temp = state.clone().place_piece(i,player)

			children.append(temp)


		if player == -1:

			for i in children:
				beta = min(beta, self.search(depth-1,i,-player,original,alpha,beta))
				if alpha >= beta:
					break;

			# print(scores)

			return beta


		elif player == 1:

			for i in children:
				alpha = max(alpha, self.search(depth-1,i,-player,original,alpha,beta))

				if alpha >= beta:
					break;

			return alpha


	# def totalValue(self, state, player,original,depth):

	# 	# return 2
	# 	player = original

	# 	# my_fives = self.checkForStreak(state,player,5)
	# 	# my_fours = self.checkForStreak(state,player,4)
	# 	# my_threes = self.checkForStreak(state,player,3)
	# 	# my_twos = self.checkForStreak(state,player,2)

	# 	# opp_fives = self.checkForStreak(state,-player,5)
	# 	# opp_fours = self.checkForStreak(state,-player,4)
	# 	# opp_threes = self.checkForStreak(state,-player,3)
	# 	# opp_twos = self.checkForStreak(state,-player,2)

	# 	# if opp_fours > 0:
	# 	# 	return -10000

	# 	return self.checkForStreak(state,player,depth)

	def totalValue(self, state,color,depth):
		print(color)
		opp_fours = self.checkForStreak(state, -color, 4)
		opp_threes = self.checkForStreak(state, -color, 3)
		opp_twos = self.checkForStreak(state, -color, 2)
		my_fours = self.checkForStreak(state, color, 4)
		my_threes = self.checkForStreak(state, color, 3)
		my_twos = self.checkForStreak(state, color, 2)

		if opp_fours > 0:

			return -100000 - depth
		else:
			return my_fours*100000 + my_threes*100 + my_twos - (100*opp_threes + 10*opp_twos) + depth

	def checkForStreak(self, state, color, streak):
		count = 0

		for i in range(state.get_width()):
			for j in range(state.get_height()):

				if state.get_space(i,j) == color:
					count += self.verticalStreak(i, j, state, streak)
					count += self.horizontalStreak(i, j, state, streak)
					count += self.diagonalCheck(i, j, state, streak)

		return count



##Github heuristic

	def verticalStreak(self, col, row, state, streak):
		consecutiveCount = 0

		for i in range(row, state.get_height()):
			if state.get_space(col,i) == state.get_space(col,row):
				consecutiveCount += 1
			else:
				break;

		if consecutiveCount >= streak:
			return 1
		else:
			return 0

	def horizontalStreak(self, col, row, state, streak):
		consecutiveCount = 0

		for i in range(col, state.get_width()):
			if state.get_space(i,row) == state.get_space(col,row):
				consecutiveCount += 1
			else:
				break;

		if consecutiveCount >= streak:
			return 1
		else:
			return 0

	def diagonalCheck(self, col, row, state, streak):

		total = 0
		consecutiveCount = 0

		j = col

		for i in range(row, state.get_height()):

		 	if j > state.get_height():
		 		break

		 	elif state.get_space(j,i) == state.get_space(col,row):
		 		consecutiveCount += 1

		 	else:
		 		break

		 	j+=1

		if consecutiveCount >= streak:



			total += 1

		consecutiveCount = 0


		j = col

		for i in range(row, -1,-1):

		 	if j > state.get_height():
		 		break

		 	elif state.get_space(j,i) == state.get_space(col,row):
		 		consecutiveCount += 1

		 	else:
		 		break
		 	j+=1

		if consecutiveCount >= streak:


			total += 1

		return total








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
