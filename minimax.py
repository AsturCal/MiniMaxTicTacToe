#Tic-Tac-Toe Minimax. 
#Plays player vs. Player or Player vs. COmputer. 
#used to study traversing the tree... 

class GAME:

	def __init__(self):
		''' Initialize board , moves  stack and winner.'''

		self.board = ['-' for i in range(0,9)]
		self.lastmoves = []   #breadcrum
		self.winner = None

	def print_board(self):
		'''Print the current game board'''
		print('Current Board: ')
		gboard = ""

		for j in range (0,9,3):
			for i in range(3):
				if self.board[j+i] == '-':
					gboard += "{} |".format(j+i)
				else:
					gboard += "{} |".format(self.board[i+j])
			gboard = gboard[:-1] #remove last bar
			gboard += "\n"
			gboard += "-"*8
			gboard += "\n"
		print(gboard)

	def _set_board(self, boardstring):
		''' Set a board for testing... eg.XOX---0X0 
			X  O  X 
			-  -  -
			O  X  O 
		'''
		if len(boardstring) != 9:
			print("Invalid board...")
			return
		#Clean stuff. 
		for i, c in enumerate(boardstring):
			if c in ['X','x','O','o']:
				self.board[i] = c.upper()
			else:
				self.board[i] = '-'



	def get_free_positions(self):
		'''Get list of available positions'''
		moves = []
		for idx, val in enumerate(self.board):
			if val == '-':
				moves.append(idx)
		return moves

	def mark(self,marker, position):
		''' mark X or O and add positon to moves. .. no need for value'''
		self.board[position] = marker
		self.lastmoves.append(position)

	def revert_last_move(self):
		'''Get last index, remove position from board and breadcrum and remove winner'''
		self.board[self.lastmoves.pop()] = '-'
		self.winner = None

	def is_game_over(self):
		''' Test for ended game or winner. '''
		win_positions = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

		for i,j,k in win_positions:
			if self.board[i] == self.board[j] == self.board[k] and self.board[i] != '-':
				self.winner = self.board[i]
				return True
			if '-' not in self.board:
				self.winner = '-'
				return True
		return False

	def play(self,player1,player2):
		"play game"

		self.p1 = player1
		self.p2 = player2

		for i in range (9):
			self.print_board()
			if i % 2 == 0:
				if self.p1.type == 'H':
					print("\t\t[P1 - {}'s Move]".format(self.p1.name))
				else:
					print("\t\t[P1 - {}'s Move]".format(self.p1.name))

				self.p1.move(self)
			else:
				if self.p2.type == 'H':
					print("\t\t[P2 - {}'s Move]".format(self.p2.name))
				else:
					print("\t\t[P2 - {}'s Move]".format(self.p2.name))

				self.p2.move(self)

			if self.is_game_over():
				self.print_board()
				if self.winner == '-':
					print("\nGame over with Draw")
				else:
					print("\nWinner: {} ".format(self.winner))
				return

class Human:
	'''for human players only no minimax'''
	def __init__(self,marker):
		self.marker = marker
		self.type = 'H'
		print("Please Enter your name: ")
		self.name = input()

	def move(self,gameinstance):
		
		while True:
			m = input("Input Position:")

			try:
				m = int(m)
			except:
				m = -1

			if m not in gameinstance.get_free_positions():
				print("Not a valid move - please retry")
			else:
				break
		gameinstance.mark(self.marker,m)

class AI: 
	def __init__(self,marker):
		self.marker = marker
		self.type = 'C'
		self.name = 'Hal'
		if self.marker == 'X':
			self.opponentmarker = 'O'
		else:
			self.opponentmarker = 'X'

	def move(self,gameinstance):
		#for self it is always start with MAX
		move_position, score = self.maximized_move(gameinstance)
		gameinstance.mark(self.marker,move_position)

	def maximized_move(self,gameinstance):
		''' Max move, maximize move'''
		bestscore = None
		bestmove = None

		#for every free posiont get the score
		for m in gameinstance.get_free_positions():
			#try the move
			gameinstance.mark(self.marker, m)
			#if game over (leaf) get score, else get minimized instance
			if gameinstance.is_game_over():
				score = self.get_score(gameinstance)
			else:
				move_position, score = self.minimized_move(gameinstance)
			#revert last move because we are using the actual game
			gameinstance.revert_last_move()

			if bestscore == None or score > bestscore:
				bestscore = score
				bestmove = m

		return bestmove, bestscore

	def minimized_move(self, gameinstance):
		bestscore = None
		bestmove = None

		for m in gameinstance.get_free_positions():
			#this time opponent marker... we need to make sure we minimize opponent.
			gameinstance.mark(self.opponentmarker, m)
			if gameinstance.is_game_over():
				score = self.get_score(gameinstance)
			else:
				move_position, score = self.maximized_move(gameinstance)

			gameinstance.revert_last_move()

			if bestscore == None or score < bestscore:
				bestscore = score
				bestmove = m

		return bestmove, bestscore

	def get_score(self,gameinstance):
		if gameinstance.is_game_over():
			if gameinstance.winner == self.marker:
				return 1 # wond
			elif gameinstance.winner == self.opponentmarker:
				return -1 #lost
		return 0 #draw


if __name__ == '__main__':
	''' 
	game = GAME()
	game.print_board()
	print(game.get_free_positions())
	game._set_board('xXo-o-x--')
	game.print_board()
	print(game.get_free_positions())
	'''
	print("Create Game")
	game = GAME()
	print("Create Human X")
	player1 = Human("X")

	#print("Create Human O")
	#player2 = Human("O")
	print("Create Computer O")
	player2 = AI("O")
	game.play(player1, player2)

	
