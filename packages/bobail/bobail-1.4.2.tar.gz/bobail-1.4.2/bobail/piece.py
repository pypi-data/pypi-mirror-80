from math import ceil

class Piece:

	def __init__(self):
		self.player = None
		self.other_player = None
		self.position = None
		self.board = None
		self.bobail = False
		self.reset_for_new_board()

	def reset_for_new_board(self):
		self.possible_moves = None

	def is_movable(self):
		return self.get_possible_moves()

	def move(self, new_position):
		self.position = new_position

	def get_possible_moves(self):
		if self.possible_moves == None:
			self.possible_moves = self.build_possible_moves()
		return self.possible_moves

	def build_possible_moves(self):
		new_positions = list(filter((lambda position: self.board.position_is_open(position)), self.get_adjacent_positions()))

		return self.create_moves_from_new_positions(new_positions)

	def create_moves_from_new_positions(self, new_positions):
		return [[self.position, new_position] for new_position in new_positions]

	def get_column(self):
		return (self.position - 1) % self.board.width

	def get_row(self):
		return self.get_row_from_position(self.position)

	def is_on_enemy_home_row(self):
		return self.get_row() == self.get_row_from_position(1 if self.other_player == 1 else self.board.position_count)

	def get_row_from_position(self, position):
		return ceil(position / self.board.width) - 1

	def get_adjacent_positions(self):
		positions = []
		current_row = self.get_row()
		current_column = self.get_column()
		
		# Check both rows and columns in all adjacent directions
		for column_index in range(-1,2):
			for row_index in range(-1,2):
				newposition = self.board.index_to_position(current_row + row_index, current_column + column_index)
				i = 2
				# if the adjacent position is open keep iterating 
				while self.board.position_is_open(newposition):
					oldposition = newposition
					newposition = self.board.index_to_position(current_row + (i * row_index), current_column + (i * column_index))
					i += 1
					#bobail only moves one spot so don't iterate
					if self.bobail:
						break 
				if i != 2:
					positions.append(oldposition)
		return positions

	def __setattr__(self, name, value):
		super(Piece, self).__setattr__(name, value)

		if name == 'player':
			self.other_player = 1 if value == 2 else 2