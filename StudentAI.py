#Author: Toluwanimi Salako
from collections import defaultdict
import random
import sys
import time
sys.path.append(r'\ConnectKSource_python')
import ConnectKSource_python.board_model as boardmodel

team_name = "StudentAI-Default" #TODO change me
DIRECTIONS = [(1,0), (1,1), (0,1), (-1,1)]
# STREAKPOINTS = {4:300000, 3:3000, 2:650, 1:}

def oppoPlayer(player):
	return 1 if player == -1 else -1

def distanceSort(center, pos)->int:
	# A sort function that gives a high proprity to those pieces are close to the center
	return max(abs(pos[0]-center[0]), abs(pos[1]-center[1]))

class StudentAI():
	def __init__(self, player, state):
		self.last_move = state.get_last_move()
		self.model = state
		self.width = self.model.get_width()
		self.height = self.model.get_height()
		self.player = player
		self.k = self.model.get_k_length()

	#
	# def getPieceScore(self, gameboard, move_x, move_y, piece, steps):
	# 	if(self.inGameboard((piece[0] + move_x*steps, piece[1] + move_y*steps)) != None):
	# 		return gameboard.get(piece[0] + move_x*steps, piece[1] + move_y*steps)
	# 	else:
	# 		# out of boundary
	# 		return 10
	#
	def getPiece(self, move_x, move_y, piece, steps):
		if(self.inGameboard((piece[0] + move_x*steps, piece[1] + move_y*steps))):
			return (piece[0] + move_x*steps, piece[1] + move_y*steps)
		return None

	# def _eval(self, gameboard, player, direction, m, visited):
	# 	score = 0
	# 	numOfTwoStreak = 0
	# 	numOfThreeStreak = 0
	# 	numOfFourStreak = 0
	# 	# pos direction:
	# 	for x, y in [(direction[0], direction[1]), (-direction[0], -direction[1])]:
	# 		# *11110
	# 		if(self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, 2) == player and self.getPieceScore(gameboard,x, y, m, 3) == self.player and self.getPieceScore(gameboard,x, y, m, 4) == player and self.getPieceScore(gameboard,x, y, m, 5) == 0):
	# 			score += 300000
	# 			numOfFourStreak += 1
	# 		# *11112
	# 		elif(self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, 2) == player and self.getPieceScore(gameboard,x, y, m, 3) == self.player and self.getPieceScore(gameboard,x, y, m, 4) == player and (self.getPieceScore(gameboard,x, y, m, 5) == oppoPlayer(player) or self.getPieceScore(gameboard,x, y, m, 5) == 10)):
	# 			score += 250000
	# 			numOfFourStreak += 1
	# 		# 1*1110
	# 		elif(self.getPieceScore(gameboard,x, y, m, -1) == player and self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, 2) == self.player and self.getPieceScore(gameboard,x, y, m, 3) == player):
	# 			score += 240000
	# 			numOfFourStreak += 1
	# 		# 11*11
	# 		elif(self.getPieceScore(gameboard,x, y, m, -1) == player and self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, -2) == self.player and self.getPieceScore(gameboard,x, y, m, 2) == player):
	# 			score += 230000
	# 			numOfFourStreak += 1
	#
	# 		# *111
	# 		elif(self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, 2) == player and self.getPieceScore(gameboard,x, y, m, 3) == self.player):
	# 			# 0*1110
	# 			if(self.getPieceScore(gameboard,x, y, m, -1) == 0 and self.getPieceScore(gameboard,x, y, m, 4) == 0):
	# 					score += 3900
	# 					numOfThreeStreak += 1
	# 			# 0*1112
	# 			elif (self.getPieceScore(gameboard,x, y, m, -1) == 0 and (self.getPieceScore(gameboard,x, y, m, 4) == 10 or self.getPieceScore(gameboard,x, y, m, 4) == oppoPlayer(player))):
	# 					score += 750
	# 			# 2*1110
	# 			elif (self.getPieceScore(gameboard,x, y, m, -1) == 10 or self.getPieceScore(gameboard,x, y, m, -1) == oppoPlayer(player)) and self.getPieceScore(gameboard,x, y, m, 4) == 0:
	# 					score += 500
	# 		# 1*11
	# 		elif(self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, 2) == player and self.getPieceScore(gameboard,x, y, m, -1) == player):
	# 			if(self.getPieceScore(gameboard,x, y, 3) == 0 and self.getPieceScore(gameboard,x, y, m, -2) == 0):
	#
	# 				score += 3750
	# 				numOfThreeStreak += 1
	# 			elif(self.getPieceScore(gameboard,x, y, m, 3) == oppoPlayer(player) or self.getPieceScore(gameboard,x, y, m, 3) == 10) and (self.getPieceScore(gameboard,x, y, i, -2) == oppoPlayer(player) or self.getPieceScore(gameboard,x, y, i, -2) == 10):
	#				210112 or 211012
	# 				score += 0
	# 			else:
	# 				score += 1350
	# 		# 0*110
	# 		elif(self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, 2) == player and (self.getPieceScore(gameboard,x, y, m, 3) != oppoPlayer(player) or self.getPieceScore(gameboard,x, y, m, 3) != 10) and self.getPieceScore(gameboard,x, y, m, -1) == 0):
	# 			pieces = [piece for piece in self.getPiece(x, y, m, i) for i in range(1,2)]
	# 			if(any(visited[direction][piece] == False for piece in pieces)):
	# 				for i in pieces:
	# 					visited[direction][i] == True
	# 				score += 600
	# 				numOfTwoStreak += 1
	# 		# 01*10
	# 		elif(self.getPieceScore(gameboard,x, y, m, -1) == player and self.getPieceScore(gameboard,x, y, m, 1) == player and self.getPieceScore(gameboard,x, y, m, -2) == 0 and self.getPieceScore(gameboard,x, y, m, 2) == 0):
	# 			pieces = [self.getPiece(x, y, m, -1), self.getPiece(x, y, m, 1)]
	# 			if(any(visited[direction][piece] == False for piece in pieces)):
	# 				for i in pieces:
	# 					visited[direction][i] == True
	# 				score += 500
	# 				numOfTwoStreak += 1
	#
	# 		if(numOfTwoStreak >= 2):
	# 			score += 3000
	# 		numOfPiece = 0
	# 		for i in range(4):
	# 			temp = 0
	# 			for j in range(4):
	# 				if(self.getPieceScore(gameboard, x, y, m, i+1) == player):
	# 					temp += 1
	# 				elif (self.getPieceScore(gameboard, x, y, m, i+1) == 10 or self.getPieceScore(gameboard, x, y, m, i+1) == oppoPlayer(player)):
	# 					temp = 0
	# 					break
	# 			numOfPiece += temp
	# 		score += numOfPiece*15
	# 	return score

	def Eval(self, gameboard):
		# score = [0, 0]
		# visited_piece_with_dir = dict()
		# for d in DIRECTIONS:
		# 	visited_piece_with_dir[d] = defaultdict(bool)
		# for m in gameboard:
		# 	if gameboard[m] != 0:
		# 		player = gameboard[m]
		# 		for x,y in DIRECTIONS:
		# 			streak = 0
		# 			space1 = 0
		# 			space2 = 0
		# 			if visited_piece_with_dir[(x, y)][m] == False:
		# 				visited_piece_with_dir[(x, y)][m] = True
		# 				next1 = (m[0]+x, m[1]+y)
		# 				next2 = (m[0]-x, m[1]-y)
		# 				while(self.inGameboard(next1) and gameboard.get(next1) == player):
		# 					streak += 1
		# 					visited_piece_with_dir[(x, y)][next1] = True
		# 					next1 = (next1[0]+x, next1[1]+y)
		# 				while(self.inGameboard(next1) and gameboard.get(next1) == 0):
		# 					space1 += 1
		# 					next1 = (next1[0]+x, next1[1]+y)
		# 				while(self.inGameboard(next2) and gameboard.get(next2) == player):
		# 					streak += 1
		# 					visited_piece_with_dir[(x, y)][next2] = True
		# 					next2 = (next2[0]-x, next2[1]-y)
		# 				while(self.inGameboard(next2) and gameboard.get(next2) == 0):
		# 					space2 += 1
		# 					next2 = (next2[0]-x, next2[1]-y)
		# 				# 011110
		# 				# if streak >= 4 and space1 > 0 and space2 >0:
		# 				# 	score
		# 				if player == self.player:
		# 					score[0] += pow(10, streak) if (streak + space1 + space2 >= 4) else 0
		# 				else:
		# 					score[1] += pow(10, streak) if (streak + space1 + space2 >= 4) else 0
		# return score[0] - score[1]
		mscore = 0
		tscore = 0
		visited_piece_with_dir = dict()
		for d in DIRECTIONS:
			visited_piece_with_dir[d] = defaultdict(bool)
		for m in gameboard:
			if gameboard[m] != 0:
				player = gameboard[m]
				numOfTwo = 0
				for x,y in DIRECTIONS:
					streak = 1
					space1 = 0
					space2 = 0
					if visited_piece_with_dir[(x, y)][m] == False:
						visited_piece_with_dir[(x, y)][m] = True
						next1 = (m[0]+x, m[1]+y)
						next2 = (m[0]-x, m[1]-y)
						while(self.inGameboard(next1) and gameboard.get(next1) == player):
							streak += 1
							visited_piece_with_dir[(x, y)][next1] = True
							next1 = (next1[0]+x, next1[1]+y)
						while(self.inGameboard(next1) and gameboard.get(next1) == 0):
							space1 += 1
							next1 = (next1[0]+x, next1[1]+y)
						while(self.inGameboard(next2) and gameboard.get(next2) == player):
							streak += 1
							visited_piece_with_dir[(x, y)][next2] = True
							next2 = (next2[0]-x, next2[1]-y)
						while(self.inGameboard(next2) and gameboard.get(next2) == 0):
							space2 += 1
							next2 = (next2[0]-x, next2[1]-y)
						#
						if streak >= 4:
							if space1 > 0 and space2 > 0:
							# 011110
								if player == self.player:
									mscore += 300000
								else:
									tscore += 300000
							elif (space1 > 0 or space2 > 0):
								# 011112 or 211110
								if player == self.player:
									mscore += 250000
								else:
									tscore += 250000
						elif streak == 3:
							# 111
							if (space1 == 1 and gameboard.get(next1) == player) or (space2 == 0 and gameboard.get(next2) == player):
								# 11101 or 011101 or 10111 or 010111
								if space1 == 1 and gameboard.get(next1) == player:
									visited_piece_with_dir[(x, y)][next1] = True
								else:
									visited_piece_with_dir[(x, y)][next2] = True

								if player == self.player:
									mscore += 240000
								else:
									tscore += 240000
							elif space1 > 0 and space2 > 0:
								# 01110
								if (space1 == 1 and gameboard.get(next1) != 0) or (space2 == 0 and gameboard.get(next2) != 0):
									# 201110 or 011102
									if player == self.player:
										mscore += 500
									else:
										tscore += 500
								else:
									# 01110
									if player == self.player:
										mscore += 3900
									else:
										tscore += 3900
							elif space1 > 0 or space2 > 0 and streak + space1 + space2 >= 5:
								# 11100 or 00111
								mscore += 750 if player == self.player else 0
								tscore += 750 if player != self.player else 0
						elif streak == 2 and ((space1 == 1 and gameboard.get(next1) == player)or (space2 == 1 and gameboard.get(next2))):
							# 1011 or 1101
							if space1 == 1 and gameboard.get(next1) == player:
								visited_piece_with_dir[(x, y)][next1] = True
							else:
								visited_piece_with_dir[(x, y)][next2] = True
							if (space1 == 1 and gameboard.get(next1) == player and gameboard.get(self.getPiece(x, y, next1, 1)) == player):
								# 11011
								visited_piece_with_dir[(x, y)][self.getPiece(x, y, next1, 1)] = True
								if player == self.player:
									mscore += 230000
								else:
									tscore += 230000
							elif (space2 == 1 and gameboard.get(next2) == player and gameboard.get(self.getPiece(x, y, next2, -1)) == player):
								# 11011
								visited_piece_with_dir[(x, y)][self.getPiece(x, y, next2, -1)] = True
								if player == self.player:
									mscore += 230000
								else:
									tscore += 230000
							elif space1 == 1 and space2 > 0 and gameboard.get(next1) == player and gameboard.get(self.getPiece(x, y, next1, 1)) ==0:
								# 011010
								if player == self.player:
									mscore += 3750
								else:
									tscore += 3750
							elif space2 == 1 and space1 > 0 and gameboard.get(next2) == player and gameboard.get(self.getPiece(x, y, next2, -1)) == 0:
								# 010110
								if player == self.player:
									mscore += 3750
								else:
									tscore += 3750
							elif space1 == 1 and gameboard.get(next1) == player and space2 == 0 and (gameboard.get(self.getPiece(x, y, next1, 1)) == oppoPlayer(player) or self.inGameboard(self.getPiece(x, y, next1, 1)) == False):
								# 211012
								pass
							elif space2 == 1 and space1 == 0 and gameboard.get(next2) == player and (gameboard.get(self.getPiece(x, y, next2, -1)) == oppoPlayer(player) or self.inGameboard(self.getPiece(x, y, next2, -1)) == False):
								# 210112
								pass
							else:
								if player == self.player:
									mscore += 1350
								else:
									tscore += 1350
						elif streak == 2 and space1 > 0 and space2 > 0 and streak + space1 + space2 >= 5:
							# 00110
							numOfTwo += 1
							if player == self.player:
								mscore += 600
							else:
								tscore += 600
						elif streak == 2 and (space1 > 0 or space2 > 0) and streak + space1 + space2 >= 5:
							if player == self.player:
								mscore += 300
							else:
								tscore += 300
						elif streak == 1 and ((space1 == 1 and gameboard.get(next1) == player) or (space2 == 1 and gameboard.get(next2) == player)):
							# 101
							if space1 == 1 and gameboard.get(next1) == player:
								visited_piece_with_dir[(x, y)][next1] = True
							else:
								visited_piece_with_dir[(x, y)][next2] = True
							if space2 > 0 and space1 == 1 and gameboard.get(next1) == player and gameboard.get(self.getPiece(x, y, next1, 1)) == player and gameboard.get(self.getPiece(x, y, next1, 2)) == 0:
								# 010110
								visited_piece_with_dir[(x, y)][self.getPiece(x, y, next1, 1)] = True
								if player == self.player:
									mscore += 3750
								else:
									tscore += 3750
							elif space1 > 0 and space2 == 1 and gameboard.get(next2) == player and gameboard.get(self.getPiece(x, y, next2, -1)) == player and gameboard.get(self.getPiece(x, y, next2, -2)) == 0:
							# 011010
								visited_piece_with_dir[(x, y)][self.getPiece(x, y, next2, -1)] = True
								if player == self.player:
									mscore += 3750
								else:
									tscore += 3750
							elif space1 == 0 and space2 == 1 and gameboard.get(next2) == player and gameboard.get(self.getPiece(x, y, next2, -1)) == player and (gameboard.get(self.getPiece(x, y, next2, -2)) == oppoPlayer(player) or self.inGameboard(self.getPiece(x, y, next2, -2)) == False):
								pass
								# 211012
							elif space1 == 1 and space2 == 0 and gameboard.get(next1) == player and gameboard.get(self.getPiece(x, y, next1, 1)) == player and (gameboard.get(self.getPiece(x, y, next1, 2)) == oppoPlayer(player) or self.inGameboard(self.getPiece(x, y, next1, 2)) == False):
								pass
								# 210112
							elif ((space1 == 1 and gameboard.get(next1) == player and gameboard.get(self.getPiece(x, y, next1, 1)) == player) or (space2 == 1 and gameboard.get(next2) == player and gameboard.get(self.getPiece(x, y, next2, -1) == player))):
								if space1 == 1 and gameboard.get(next1) == player:
									visited_piece_with_dir[(x, y)][self.getPiece(x, y, next1, 1)] = True
								else:
									visited_piece_with_dir[(x, y)][self.getPiece(x, y, next2, -1)] = True
								# 1101
								if player == self.player:
									mscore += 1350
								else:
									tscore += 1350
							elif (space1 == 1 and gameboard.get(next1) == player and gameboard.get(self.getPiece(x, y, next1, 1)) == 0 and space2 > 0) or (space2 == 1 and space1 > 0 and gameboard.get(next2) == player and gameboard.get(self.getPiece(x, y, next2, -1)) == 0):
								# 01010
								numOfTwo += 1
								if player == self.player:
									mscore += 500
								else:
									tscore += 500
		return mscore - tscore

	def doubleKminusThree(self, piece, gameboard, player):

		streaks = []
		for x, y in DIRECTIONS:
			streak = 0
			next1 = (piece[0] + x, piece[1] + y)
			next2 = (piece[0] - x, piece[1] - y)
			space1 = 0
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
			if(streak >= 2 and space1 > 0 and space2 > 0 and streak + space1 + space2 >= 4):
				streaks.append(streak)
		count = 0
		for i in streaks:
			if i >= 2:
				count+= 1
		return count >= 2

	def needDefense(self, gameboard, moves):
		mstreak = 0
		tstreak = 0
		defense = None
		for piece in moves:
			if(self.doubleKminusThree(piece, gameboard, oppoPlayer(self.player))) and tstreak <= 3:
				defense = piece
				tstreak = 3
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

				if space1 > 0 and space2 > 0 and streak + space1 + space2 >= 4 and streak >= 3:
					# 活K-2
					if(streak > tstreak):
						defense = piece
						tstreak = streak
				elif streak + space1 + space2 >=4 and streak >= 4:
					# 死k-1
					if(streak > tstreak):
						defense = piece
						tstreak = streak

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
					if(streak_p > mstreak):
						mstreak = streak_p
				elif streak_p + space1_p + space2_p >=4 and streak_p >= 4:
					# 死k-1
					if(streak_p > mstreak):
						mstreak = streak_p
		return defense if tstreak > mstreak else None




	def inGameboard(self, pos):
		if not pos:
			return False
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
	def IDS(self, moves, gameboard, timer):
		defense = self.needDefense(gameboard, moves)
		if(defense != None):
			return defense
		else:
			piece = None
			# print(depth)
			i = 1
			while(i <= 50):
				if time.time() - timer > (deadline - 100) / 1000:
					return piece
				print("going to depth :", i)
				if(i != 1):
					moves.sort(key = lambda x: distanceSort(piece, x))
				piece = self.ab_pruning(moves, gameboard, i, timer)
				i += 2
			return piece


	def ab_pruning(self, moves, gameboard, depth, timer):
		alpha = -2147483648
		beta = 2147483647
		piece = None
		index = 0
		for move in moves:
			if time.time() - timer > (deadline - 100) / 1000:
				return piece
			temp = moves[:]
			temp.pop(index)
			gameboard[move] = self.player
			(alpha, piece) = max((alpha, piece), (self.min_value(gameboard, alpha, beta, depth-1, temp, timer), move))
			index += 1
			gameboard[move] = 0
		return piece

	def max_value(self, gameboard, alpha, beta, depth, moves, timer):
		if(depth == 0):
			return self.Eval(gameboard)
		index = 0
		for move in moves:
			if time.time() - timer > (deadline - 100) / 1000:
				return alpha
			temp = moves[:]
			temp.pop(index)
			gameboard[move] = self.player
			alpha = max(alpha, self.min_value(gameboard, alpha, beta, depth - 1, temp, timer))
			index += 1
			gameboard[move] = 0
			if(alpha >= beta):
				return 2147483647
		return alpha

	def min_value(self, gameboard, alpha, beta, depth, moves, timer):
		if(depth == 0):
			return self.Eval(gameboard)
		index = 0
		for move in moves:
			if time.time() - timer > (deadline - 100) / 1000:
				return beta
			temp = moves[:]
			temp.pop(0)
			gameboard[move] = oppoPlayer(self.player)
			beta = min(beta, self.max_value(gameboard, alpha, beta, depth - 1, temp, timer))
			gameboard[move] = 0
			index += 1
			if(alpha >= beta):
				return -2147483647
		return beta

	def make_move(self, deadline):
		'''Write AI Here. Return a tuple (col, row)'''
		timer = time.time()
		width = self.model.get_width()
		height = self.model.get_height()
		spaces = defaultdict(int)

		for i in range(width):
			for j in range(height):
				spaces[(i,j)] = self.model.get_space(i, j)
		moves = [k for k in spaces.keys() if spaces[k] == 0]
		# print(sorted(moves, key = lambda x: distanceSort((4, 4), x)))
		piece = self.IDS(moves, spaces, timer)
		b = time.time()
		print(b-timer)
		return piece



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
	global deadline
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
