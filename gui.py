import tkinter as tk
from tkinter import ttk, messagebox
import time
from board import Board
from game_logic import GameLogic
from minimax import Minimax
from alpha_beta import AlphaBeta

class Connect6GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect-6 AI Player")
        
        # Game state
        self.board = None
        self.game_logic = None
        self.current_player = 1
        self.moves_this_turn = 0
        self.max_moves_per_turn = 1  # First move is 1 stone
        self.game_mode = "human_vs_ai"
        self.ai_algorithm = "minimax"
        self.ai_depth = 3
        self.board_size = 15
        
        # Statistics
        self.last_move_time = 0
        self.last_nodes_explored = 0
        self.last_pruned = 0
        
        self.setup_ui()
        self.new_game()
    
    def setup_ui(self):
        """Create all UI elements"""
        
        # THEME COLORS - Change these to customize!
        BG_COLOR = "#2b2b2b"      # Dark gray background
        FG_COLOR = "#ffffff"       # White text
        ACCENT_COLOR = "#3d3d3d"   # Slightly lighter gray for frames
        
        # Set main window background
        self.root.configure(bg=BG_COLOR)
        
        # Control Panel (Top)
        control_frame = tk.Frame(self.root, padx=10, pady=10, bg=BG_COLOR)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Board Size Selection
        tk.Label(control_frame, text="Board Size:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5)
        self.size_var = tk.StringVar(value="15")
        size_combo = ttk.Combobox(control_frame, textvariable=self.size_var, 
                                   values=["13", "15", "19"], width=10, state="readonly")
        size_combo.grid(row=0, column=1, padx=5)
        
        # Algorithm Selection
        tk.Label(control_frame, text="AI Algorithm:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5)
        self.algo_var = tk.StringVar(value="Alpha-Beta Pruning")
        algo_combo = ttk.Combobox(control_frame, textvariable=self.algo_var,
                                  values=["Minimax", "Alpha-Beta Pruning"], 
                                  width=15, state="readonly")
        algo_combo.grid(row=0, column=3, padx=5)
        
        # Difficulty (Depth)
        tk.Label(control_frame, text="Difficulty:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=4, padx=5)
        self.depth_var = tk.StringVar(value="3")
        depth_combo = ttk.Combobox(control_frame, textvariable=self.depth_var,
                                   values=["2", "3", "4"], width=10, state="readonly")
        depth_combo.grid(row=0, column=5, padx=5)
        
        # Game Mode
        tk.Label(control_frame, text="Mode:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="Human vs AI")
        mode_combo = ttk.Combobox(control_frame, textvariable=self.mode_var,
                                  values=["Human vs AI", "AI vs AI"], 
                                  width=15, state="readonly")
        mode_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # New Game Button
        tk.Button(control_frame, text="New Game", command=self.new_game,
                 bg="#4CAF50", fg="white", padx=20, 
                 activebackground="#45a049", relief=tk.RAISED, bd=2).grid(row=1, column=2, padx=5, pady=5)
        
        # Compare Button
        tk.Button(control_frame, text="Compare Algorithms", 
                 command=self.compare_algorithms,
                 bg="#2196F3", fg="white", padx=20,
                 activebackground="#1976D2", relief=tk.RAISED, bd=2).grid(row=1, column=3, padx=5, pady=5)
        
        # Main Game Area
        game_frame = tk.Frame(self.root, bg=BG_COLOR)
        game_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Canvas for board
        self.canvas = tk.Canvas(game_frame, width=600, height=600, bg="burlywood", 
                               highlightthickness=2, highlightbackground=ACCENT_COLOR)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Info Panel (Right side)
        info_frame = tk.Frame(self.root, padx=10, pady=10, bg=BG_COLOR)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Current Player
        tk.Label(info_frame, text="Game Info", font=("Arial", 14, "bold"), 
                bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        self.player_label = tk.Label(info_frame, text="Current Player: Black (1)", 
                                     font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
        self.player_label.pack(pady=5)
        
        # Moves remaining this turn
        self.moves_label = tk.Label(info_frame, text="Moves this turn: 0/1", 
                                    font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
        self.moves_label.pack(pady=5)
        
        # Statistics
        tk.Label(info_frame, text="\nAI Statistics", 
                font=("Arial", 12, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        
        self.stats_text = tk.Text(info_frame, width=30, height=15, font=("Courier", 10),
                                 bg=ACCENT_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR,
                                 relief=tk.SUNKEN, bd=2)
        self.stats_text.pack(pady=5)
        
        # Move History
        tk.Label(info_frame, text="\nMove History", 
                font=("Arial", 12, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        
        self.history_text = tk.Text(info_frame, width=30, height=10, font=("Courier", 9),
                                    bg=ACCENT_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR,
                                    relief=tk.SUNKEN, bd=2)
        self.history_text.pack(pady=5)
    
    def new_game(self):
        """Start a new game"""
        self.board_size = int(self.size_var.get())
        self.ai_algorithm = self.algo_var.get().lower().replace(" ", "_").replace("-", "_")
        self.ai_depth = int(self.depth_var.get())
        self.game_mode = self.mode_var.get().lower().replace(" ", "_")
        
        self.board = Board(self.board_size)
        self.game_logic = GameLogic(self.board)
        self.current_player = 1
        self.moves_this_turn = 0
        self.max_moves_per_turn = 1
        
        self.history_text.delete(1.0, tk.END)
        self.update_stats("Game started!")
        self.draw_board()
        self.update_labels()
        
        # ADD THIS: Start AI vs AI automatically
        if self.game_mode == "ai_vs_ai":
            self.root.after(500, self.ai_move)
    
    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("all")
        
        cell_size = 600 // (self.board_size + 1)
        
        # Draw grid
        for i in range(self.board_size):
            x = (i + 1) * cell_size
            self.canvas.create_line(x, cell_size, x, self.board_size * cell_size, fill="#8B4513", width=2)
            self.canvas.create_line(cell_size, x, self.board_size * cell_size, x, fill="#8B4513", width=2)
        
        # Draw stones
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board.grid[row][col] != 0:
                    x = (col + 1) * cell_size
                    y = (row + 1) * cell_size
                    color = "black" if self.board.grid[row][col] == 1 else "white"
                    self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15,
                                           fill=color, outline="gray20", width=2)
    
    def on_click(self, event):
        """Handle mouse click on board"""
        if self.game_mode == "ai_vs_ai":
            return  # No human input in AI vs AI mode
        
        if self.current_player == 2:  # AI's turn
            return
        
        cell_size = 600 // (self.board_size + 1)
        col = round(event.x / cell_size) - 1
        row = round(event.y / cell_size) - 1
        
        if self.board.is_valid_move(row, col):
            self.make_move(row, col)
    
    def make_move(self, row, col):
        """Make a move on the board"""
        self.board.place_stone(row, col, self.current_player)
        self.moves_this_turn += 1
        
        # Log move
        player_name = "Black" if self.current_player == 1 else "White"
        self.history_text.insert(tk.END, f"{player_name}: ({row}, {col})\n")
        self.history_text.see(tk.END)
        
        self.draw_board()
        
        # Check win
        if self.game_logic.check_win(self.current_player):
            winner = "Black" if self.current_player == 1 else "White"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            return
        
        # Check if turn is over
        if self.moves_this_turn >= self.max_moves_per_turn:
            self.switch_turn()
        else:
            self.update_labels()
    
    def switch_turn(self):
        """Switch to next player"""
        self.current_player = 3 - self.current_player
        self.moves_this_turn = 0
        self.max_moves_per_turn = 2  # After first move, always 2 stones
        self.update_labels()
        
        # If AI's turn, make move
        if self.current_player == 2 or self.game_mode == "ai_vs_ai":
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """Let AI make a move"""
        num_stones = 1 if self.board.move_count == 0 else 2
        
        start_time = time.time()
        
        if self.ai_algorithm == "alpha_beta_pruning":
            ai = AlphaBeta(self.board)
            moves = ai.find_best_move(self.current_player, self.ai_depth, num_stones)
            self.last_nodes_explored = ai.nodes_explored
            self.last_pruned = ai.pruned_count
        else:
            ai = Minimax(self.board)
            moves = ai.find_best_move(self.current_player, self.ai_depth, num_stones)
            self.last_nodes_explored = ai.nodes_explored
            self.last_pruned = 0
        
        self.last_move_time = time.time() - start_time
        
        # Make the moves
        for row, col in moves:
            self.make_move(row, col)
        
        self.update_stats(f"AI ({self.ai_algorithm}) made move")
    
    def update_labels(self):
        """Update UI labels"""
        player_name = "Black" if self.current_player == 1 else "White"
        self.player_label.config(text=f"Current Player: {player_name} ({self.current_player})")
        self.moves_label.config(text=f"Moves this turn: {self.moves_this_turn}/{self.max_moves_per_turn}")
    
    def update_stats(self, message):
        """Update statistics display"""
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"{message}\n")
        self.stats_text.insert(tk.END, f"\n--- Last AI Move ---\n")
        self.stats_text.insert(tk.END, f"Algorithm: {self.ai_algorithm}\n")
        self.stats_text.insert(tk.END, f"Time: {self.last_move_time:.3f}s\n")
        self.stats_text.insert(tk.END, f"Nodes: {self.last_nodes_explored}\n")
        self.stats_text.insert(tk.END, f"Pruned: {self.last_pruned}\n")
        self.stats_text.insert(tk.END, f"Depth: {self.ai_depth}\n")
    
    def compare_algorithms(self):
        """Run both algorithms and compare"""
        messagebox.showinfo("Compare", 
                          "This will run both Minimax and Alpha-Beta on the current position.\n" +
                          "Check the console for detailed comparison.")
        
        # Save current state
        temp_board = self.board.copy()
        num_stones = 1 if self.board.move_count == 0 else 2
        
        # Run Minimax
        print("\n=== ALGORITHM COMPARISON ===")
        start = time.time()
        minimax_ai = Minimax(temp_board)
        minimax_move = minimax_ai.find_best_move(self.current_player, self.ai_depth, num_stones)
        minimax_time = time.time() - start
        
        # Run Alpha-Beta
        start = time.time()
        ab_ai = AlphaBeta(temp_board)
        ab_move = ab_ai.find_best_move(self.current_player, self.ai_depth, num_stones)
        ab_time = time.time() - start
        
        # Display comparison
        print(f"\nMinimax:")
        print(f"  Time: {minimax_time:.3f}s")
        print(f"  Nodes: {minimax_ai.nodes_explored}")
        print(f"  Move: {minimax_move}")
        
        print(f"\nAlpha-Beta Pruning:")
        print(f"  Time: {ab_time:.3f}s")
        print(f"  Nodes: {ab_ai.nodes_explored}")
        print(f"  Pruned: {ab_ai.pruned_count}")
        print(f"  Move: {ab_move}")
        
        speedup = minimax_time / ab_time if ab_time > 0 else 0
        reduction = (1 - ab_ai.nodes_explored/minimax_ai.nodes_explored)*100 if minimax_ai.nodes_explored > 0 else 0
        
        print(f"\nSpeedup: {speedup:.2f}x faster")
        print(f"Node reduction: {reduction:.1f}%")
        
        messagebox.showinfo("Comparison Complete", 
                          f"Minimax: {minimax_time:.3f}s, {minimax_ai.nodes_explored} nodes\n" +
                          f"Alpha-Beta: {ab_time:.3f}s, {ab_ai.nodes_explored} nodes\n" +
                          f"Speedup: {speedup:.2f}x")