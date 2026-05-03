import sys
from heuristic import Heuristic
from game_logic import GameLogic

class Minimax:
    def __init__(self, board):
        self.board = board
        self.nodes_explored = 0
    
    def find_best_move(self, player, depth=3, num_stones=2):
        """Find best move using Minimax with improved move ordering"""
        self.nodes_explored = 0
        opponent = 3 - player
        
        # CRITICAL: Check for immediate wins and blocks first!
        immediate_win = self._find_winning_move(player, num_stones)
        if immediate_win:
            return immediate_win
        
        immediate_block = self._find_winning_move(opponent, num_stones)
        if immediate_block:
            return immediate_block
        
        best_moves = []
        best_score = -sys.maxsize
        
        # Get candidate moves with intelligent ordering
        possible_moves = self._get_candidate_moves(num_stones)
        scored_moves = self._score_moves(possible_moves, player)
        
        # Search the most promising moves first
        for moves, _ in scored_moves[:30]:  # Increased from 10
            temp_board = self.board.copy()
            for row, col in moves:
                temp_board.place_stone(row, col, player)
            
            score = self._minimax(temp_board, depth - 1, False, player)
            
            if score > best_score:
                best_score = score
                best_moves = moves
        
        return best_moves if best_moves else possible_moves[0]
    
    def _minimax(self, board, depth, is_maximizing, player):
        """Minimax with better evaluation"""
        self.nodes_explored += 1
        
        game_logic = GameLogic(board)
        game_state = game_logic.get_game_state()
        
        if depth == 0 or game_state != 'ongoing':
            heuristic = Heuristic(board)
            return heuristic.evaluate(player)
        
        opponent = 3 - player
        
        if is_maximizing:
            max_eval = -sys.maxsize
            moves = self._get_candidate_moves(2)
            scored_moves = self._score_moves(moves, player)
            
            for move_combo, _ in scored_moves[:15]:  # Increased
                temp_board = board.copy()
                for row, col in move_combo:
                    temp_board.place_stone(row, col, player)
                
                eval_score = self._minimax(temp_board, depth - 1, False, player)
                max_eval = max(max_eval, eval_score)
            
            return max_eval
        else:
            min_eval = sys.maxsize
            moves = self._get_candidate_moves(2)
            scored_moves = self._score_moves(moves, opponent)
            
            for move_combo, _ in scored_moves[:15]:  # Increased
                temp_board = board.copy()
                for row, col in move_combo:
                    temp_board.place_stone(row, col, opponent)
                
                eval_score = self._minimax(temp_board, depth - 1, True, player)
                min_eval = min(min_eval, eval_score)
            
            return min_eval
    
    def _find_winning_move(self, player, num_stones):
        """Check if player can win in this turn"""
        candidates = self._get_candidate_moves(num_stones)
        
        for moves in candidates[:100]:  # Check more possibilities for critical moves
            temp_board = self.board.copy()
            for row, col in moves:
                temp_board.place_stone(row, col, player)
            
            # Check if this creates a win
            if self._check_win(temp_board, player):
                return moves
        
        return None
    
    def _check_win(self, board, player):
        """Check if player has 6 in a row"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == player:
                    for dr, dc in directions:
                        count = 0
                        r, c = row, col
                        while (0 <= r < board.size and 
                               0 <= c < board.size and 
                               board.grid[r][c] == player):
                            count += 1
                            if count >= 6:
                                return True
                            r += dr
                            c += dc
        return False
    
    def _score_moves(self, moves_list, player):
        """Score and sort moves by promise (move ordering optimization)"""
        scored = []
        for moves in moves_list:
            temp_board = self.board.copy()
            for row, col in moves:
                temp_board.place_stone(row, col, player)
            
            heuristic = Heuristic(temp_board)
            score = heuristic.evaluate(player)
            scored.append((moves, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    
    def _get_candidate_moves(self, num_stones):
        """Get candidate moves near existing stones"""
        candidates = set()
        
        if self.board.move_count == 0:
            center = self.board.size // 2
            candidates.add((center, center))
            # Add a few near-center positions too
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    candidates.add((center + dr, center + dc))
        else:
            # Expand search radius for better coverage
            for row in range(self.board.size):
                for col in range(self.board.size):
                    if self.board.grid[row][col] != 0:
                        for dr in range(-2, 3):
                            for dc in range(-2, 3):
                                nr, nc = row + dr, col + dc
                                if (0 <= nr < self.board.size and 
                                    0 <= nc < self.board.size and
                                    self.board.grid[nr][nc] == 0):
                                    candidates.add((nr, nc))
        
        candidates = list(candidates)
        
        if num_stones == 1:
            return [[move] for move in candidates[:30]]
        else:
            move_combos = []
            for i, move1 in enumerate(candidates[:20]):  # Increased
                for move2 in candidates[i+1:20]:
                    if move1 != move2:
                        move_combos.append([move1, move2])
            return move_combos[:100]  # Increased for better coverage