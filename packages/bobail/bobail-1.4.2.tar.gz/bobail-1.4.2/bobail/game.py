from .board import Board

class Game:

	def __init__(self):
		self.board = Board()
		self.moves = []

	def move(self, move):
		if move not in self.get_possible_moves():
			raise ValueError('The provided move is not possible')

		self.board = self.board.create_new_board_from_move(move)
		self.moves.append(move)

		return self

	def move_limit_reached(self):
		return 

	def is_over(self):
		row_ending = True if self.board.bobail_row in [0,4] else False
		bobail_ending = False if self.board.get_possible_moves() else True
		return  row_ending or bobail_ending

	def get_winner(self):
		if self.board.bobail_row == 0:
			return 1
		elif self.board.bobail_row == 4:
			return 2
		else:
			if not self.board.get_possible_moves():
				if self.board.player_turn == 1:
					return 2
				elif self.board.player_turn == 2:
					return 1
			else:
				return None

	def get_possible_moves(self):
		return self.board.get_possible_moves()

	def whose_turn(self):
		return self.board.player_turn
