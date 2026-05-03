class GameLogic:
    def __init__(self, board):
        self.board = board
    
    def check_win(self, player):
        """
        Check if player has 6 in a row (horizontal, vertical, or diagonal)
        Returns: True if player wins, False otherwise
        """
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal \
            (1, -1)   # diagonal /
        ]
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.board.grid[row][col] == player:
                    # Check all 4 directions
                    for dr, dc in directions:
                        if self._count_line(row, col, dr, dc, player) >= 6:
                            return True
        return False
    
    def _count_line(self, row, col, dr, dc, player):
        """Count consecutive stones in a direction"""
        count = 0
        r, c = row, col
        
        # Count in positive direction
        while (0 <= r < self.board.size and 
               0 <= c < self.board.size and 
               self.board.grid[r][c] == player):
            count += 1
            r += dr
            c += dc
        
        return count
    
    def is_board_full(self):
        """Check if board is completely filled"""
        return len(self.board.get_empty_cells()) == 0
    
    def get_game_state(self):
        """
        Returns: 'player1_win', 'player2_win', 'draw', or 'ongoing'
        """
        if self.check_win(1):
            return 'player1_win'
        elif self.check_win(2):
            return 'player2_win'
        elif self.is_board_full():
            return 'draw'
        else:
            return 'ongoing'