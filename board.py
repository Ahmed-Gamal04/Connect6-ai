class Board:
    def __init__(self, size=19):
        """Initialize empty board"""
        self.size = size
        # Pure Python 2D list instead of numpy
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.move_count = 0
    
    def is_valid_move(self, row, col):
        """Check if position is valid and empty"""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col] == 0
        return False
    
    def place_stone(self, row, col, player):
        """Place a stone on the board"""
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            self.move_count += 1
            return True
        return False
    
    def get_empty_cells(self):
        """Return list of empty cell coordinates"""
        empty = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    empty.append((i, j))
        return empty
    
    def copy(self):
        """Create a deep copy of the board"""
        new_board = Board(self.size)
        # Deep copy the 2D list
        new_board.grid = [row[:] for row in self.grid]
        new_board.move_count = self.move_count
        return new_board
    
    def reset(self):
        """Clear the board"""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.move_count = 0