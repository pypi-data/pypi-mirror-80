from copy import deepcopy
from functools import reduce
from .board_searcher import BoardSearcher
from .board_initializer import BoardInitializer

class Board:

	def __init__(self):
		self.player_turn = 1
		self.width = 5
		self.height = 5
		self.bobail_row = 3
		self.bobail_turn = False
		self.position_count = self.width * self.height
		self.rows_per_user_with_pieces = 1
		self.position_layout = {}
		self.searcher = BoardSearcher()
		BoardInitializer(self).initialize()

	def count_movable_player_pieces(self, player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)), self.searcher.get_pieces_by_player(player_number), 0)

	def get_possible_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		return not (self.searcher.get_piece_by_position(position) or position > self.position_count or position < 1)

	def create_new_board_from_move(self, move):
		new_board = deepcopy(self)
		new_board.perform_move(move)
		return new_board

	def perform_move(self, move):
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		if self.bobail_turn:
			self.bobail_turn = False
		else:
			self.player_turn = 1 if self.player_turn == 2 else 2
			self.bobail_turn = True

	def move_piece(self, move):
		moved_piece = self.searcher.get_piece_by_position(move[0])
		moved_piece.move(move[1])
		if moved_piece.bobail:
			self.bobail_row = moved_piece.get_row()
		self.pieces = sorted(self.pieces, key = lambda piece: piece.position if piece.position else 0)

	def is_valid_row_and_column(self, row, column):
		if row < 0 or row >= self.height:
			return False

		if column < 0 or column >= self.width:
			return False

		return True

	def index_to_position(self, row, column):
		if self.is_valid_row_and_column(row, column):
			return row * self.width + column + 1
		else:
			return -1

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			[piece.reset_for_new_board() for piece in self.pieces]

			self.searcher.build(self)