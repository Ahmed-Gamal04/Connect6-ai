class Heuristic:
    def __init__(self, board):
        self.board = board
    
    def evaluate(self, player):
        """Evaluate board state for given player"""
        opponent = 3 - player
        
        # Check for immediate wins/losses first
        player_six = self._count_threats(player, 6)
        opponent_six = self._count_threats(opponent, 6)
        
        if player_six > 0:
            return 10000000  # We win!
        if opponent_six > 0:
            return -10000000  # We lose!
        
        # Evaluate threats for both players
        player_score = self._evaluate_all_threats(player)
        opponent_score = self._evaluate_all_threats(opponent)
        
        return player_score - opponent_score
    
    def _evaluate_all_threats(self, player):
        """Comprehensive threat evaluation"""
        score = 0
        
        # Count different threat levels
        five_threats = self._count_threats(player, 5)
        four_threats = self._count_threats(player, 4)
        three_threats = self._count_threats(player, 3)
        two_threats = self._count_threats(player, 2)
        
        # Open sequences (not blocked on either end) are MUCH more valuable
        open_five = self._count_open_threats(player, 5)
        open_four = self._count_open_threats(player, 4)
        open_three = self._count_open_threats(player, 3)
        open_two = self._count_open_threats(player, 2)
        
        # Weights for threats
        score += five_threats * 500000      # Immediate winning threat
        score += open_four * 100000         # Open four is nearly a win
        score += four_threats * 10000       # Four in a row
        score += open_three * 5000          # Open three is very strong
        score += three_threats * 500        # Three in a row
        score += open_two * 100             # Open two
        score += two_threats * 10           # Two in a row
        
        return score
    
    def _count_threats(self, player, length):
        """Count sequences of exactly 'length' consecutive stones"""
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        visited = set()
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.board.grid[row][col] == player:
                    for dr, dc in directions:
                        if (row, col, dr, dc) not in visited:
                            seq_length = self._count_sequence(row, col, dr, dc, player)
                            if seq_length >= length:
                                count += 1
                                # Mark this sequence as visited
                                for i in range(seq_length):
                                    visited.add((row + i*dr, col + i*dc, dr, dc))
        
        return count
    
    def _count_open_threats(self, player, length):
        """Count open-ended sequences (both ends are empty)"""
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        visited = set()
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.board.grid[row][col] == player:
                    for dr, dc in directions:
                        if (row, col, dr, dc) not in visited:
                            seq_length, is_open = self._count_sequence_with_openness(
                                row, col, dr, dc, player
                            )
                            if seq_length >= length and is_open:
                                count += 1
                                for i in range(seq_length):
                                    visited.add((row + i*dr, col + i*dc, dr, dc))
        
        return count
    
    def _count_sequence(self, row, col, dr, dc, player):
        """Count consecutive stones in one direction"""
        count = 0
        r, c = row, col
        
        while (0 <= r < self.board.size and 
               0 <= c < self.board.size and 
               self.board.grid[r][c] == player):
            count += 1
            r += dr
            c += dc
            if count > 6:  # No need to count beyond 6
                break
        
        return count
    
    def _count_sequence_with_openness(self, row, col, dr, dc, player):
        """Count sequence and check if both ends are open"""
        # Count forward
        count = 0
        r, c = row, col
        while (0 <= r < self.board.size and 
               0 <= c < self.board.size and 
               self.board.grid[r][c] == player):
            count += 1
            r += dr
            c += dc
        
        # Check if both ends are empty
        # Check front
        front_open = (0 <= r < self.board.size and 
                     0 <= c < self.board.size and 
                     self.board.grid[r][c] == 0)
        
        # Check back
        back_r = row - dr
        back_c = col - dc
        back_open = (0 <= back_r < self.board.size and 
                    0 <= back_c < self.board.size and 
                    self.board.grid[back_r][back_c] == 0)
        
        is_open = front_open and back_open
        return count, is_open