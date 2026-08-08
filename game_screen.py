import customtkinter as ctk
from solver import SudokuSolver
from generator import SudokuGenerator
import random
import json
import winsound
import os
class GameScreen:

    def __init__(self):
        
        self.root = ctk.CTk()

        self.root.title("Sudoku Solver Pro")

        self.root.geometry("1200x800")

        self.root.minsize(1000, 700)

        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        self.cells = []

        self.original_board = None
        self.solution_board = None

        self.max_lives = 3
        self.lives = 3
        self.seconds = 0
        self.timer_running = False
        self.timer_job = None
        self.wrong_cells = set()
        self.correct_cells = set()

        self.last_wrong_value = {}

        self.remaining_numbers = {}

        self.auto_check = True
        self.game_over = False

        self.hints_used = 0
        self.max_hints = 3
        self.sound_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "sounds"
        )

        self.wrong_sound = os.path.join(
            self.sound_dir,
            "wrong.wav"
        )

        self.game_over_sound = os.path.join(
            self.sound_dir,
            "game_over.wav"
        )

        self.win_sound = os.path.join(
            self.sound_dir,
            "win.wav"
        )
        self.moves = 0
        self.current_difficulty = "Medium"
        self.game_started = False

        self.buttons = {}

        self.create_ui()
    def play_sound(self, sound_file):

        if os.path.exists(sound_file):

            try:
                winsound.PlaySound(
                    sound_file,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            except Exception:
                pass
    def create_ui(self):

        # ================= LEFT PANEL =================

        self.left_frame = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        self.left_frame.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )

        # ================= RIGHT PANEL =================

        self.right_frame = ctk.CTkFrame(
            self.root,
            width=280,
            corner_radius=18,
            border_width=1,
            border_color="#3A3A3A"
        )

        self.right_frame.grid(
            row=0,
            column=1,
            padx=(0, 40),
            pady=20,
            sticky="nsew"
        )
        self.life_label = ctk.CTkLabel(
            self.right_frame,
            text="❤️❤️❤️",
            font=("Segoe UI", 25, "bold")
        )

        self.life_label.pack(
             pady=(20,5)
        )

        self.timer_label = ctk.CTkLabel(
           self.right_frame,
           text="⏱ 00:00",
           font=("Segoe UI",20,"bold")
        )

        self.timer_label.pack(
             pady=(0,15)
        )
        ctk.CTkLabel(
            self.right_frame,
            text="DIFFICULTY",
            font=("Segoe UI", 13, "bold"),
            text_color="#A0A0A0"
        ).pack(pady=(0, 7))

        self.difficulty = ctk.StringVar(value="Medium")

        self.difficulty_menu = ctk.CTkOptionMenu(
            self.right_frame,
            values=["Easy", "Medium", "Hard"],
            variable=self.difficulty,
            command=self.change_difficulty,
            width=200,
            height=38,
            corner_radius=10,
            font=("Segoe UI", 14, "bold")
        )   
        self.difficulty_menu.pack(
            pady=(0, 15)
        )

        separator = ctk.CTkLabel(
            self.right_frame,
            text="━━━━━━━━━━━━━━"
        )

        separator.pack(
            pady=(0,15)
        )
        # ================= REMAINING =================

        
        # ================= TITLE =================

        title_frame = ctk.CTkFrame(
            self.left_frame,
            fg_color="transparent"
        )

        title_frame.pack(pady=20)

        ctk.CTkLabel(
            title_frame,
            text="Sudoku Solver",
            font=("Segoe UI", 30, "bold"),
            text_color="#4EA8FF"
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text=" ヾ(⌐■_■)ノ♪",
            font=("Segoe UI", 24, "bold"),
            text_color="#F44336"
        ).pack(side="left")

        # ================= GRID FRAME =================

        self.grid_frame = ctk.CTkFrame(
            self.left_frame,
            fg_color="transparent",
            corner_radius=12
        )

        self.grid_frame.pack(expand=True)
    

        # ================= SUDOKU GRID =================

        for r in range(9):

            row = []

            for c in range(9):

                cell = ctk.CTkEntry(
                    self.grid_frame,
                    width=48,
                    height=48,
                    justify="center",
                    font=("Segoe UI", 20, "bold"),
                    corner_radius=12,
                    border_width=1
                )

                padx = (
                    5 if c % 3 == 0 else 1,
                    5 if c % 3 == 2 else 1
                )           

                pady = (
                    5 if r % 3 == 0 else 1,
                    5 if r % 3 == 2 else 1
                )

                cell.grid(
                    row=r,
                    column=c,
                    padx=padx,
                    pady=pady
                )
                row.append(cell)
                cell.bind(
                   "<KeyRelease>",
                    lambda event, r=r, c=c: self.check_cell(r, c)
                )

            self.cells.append(row)
            # ================= BUTTONS =================

        buttons = [
            "Generate",
            "Solve",
            "Hint",
            "Restart"
            
        ]

        for text in buttons:

            command = None

            if text == "Generate":
                command = self.generate_board

            elif text == "Solve":
                command = self.solve_board

            elif text == "Hint":
                command = self.give_hint

            elif text == "Restart":
                command = self.restart_board

            elif text == "Save":
                command = self.save_game

            elif text == "Load":
                command = self.load_game

            button_text = text

            if text == "Hint":
                button_text = f"Hint ({self.max_hints})"

            button = ctk.CTkButton(
                self.right_frame,
                text=button_text,
                width=200,
                height=40,
                corner_radius=10,
                font=("Segoe UI", 14, "bold"),
                command=command
            )

            button.pack(
                fill="x",
                padx=25,
                pady=6
            )

            self.buttons[text] = button

        self.remaining_title = ctk.CTkLabel(
            self.right_frame,
            text="REMAINING NUMBERS",
            font=("Segoe UI", 13, "bold"),
            text_color="#A0A0A0"
        )
       
        self.remaining_title.pack()
       
        self.remaining_frame = ctk.CTkFrame(
             self.right_frame,
             fg_color="transparent"
        )

        self.remaining_frame.pack(
             pady=(5, 0),
             padx=10,
             fill="x"
        )

        self.remaining_labels = {}

        positions = {
            1: (0, 0),
            2: (1, 0),
            3: (2, 0),
            4: (3, 0),
            5: (4, 0),

            6: (0, 1),
            7: (1, 1),
            8: (2, 1),
            9: (3, 1),
        }

        for number, (r, c) in positions.items():

            label = ctk.CTkLabel(
                self.remaining_frame,
                text="",
                font=("Segoe UI", 15, "bold"),
                width=80,
                height=28,
                anchor="w"
            )           

            label.grid(
                row=r,
                column=c,
                padx=12,
                pady=3,
                sticky="w"
            )

            self.remaining_labels[number] = label
       

        # ================= STATUS =================

        self.status = ctk.CTkLabel(
            self.root,
            text="Status : Ready",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
            text_color="#A0A0A0"
        )

        self.status.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )       
        # ================= LIVES =================

    def update_lives(self):

        hearts = "❤️" * self.lives
        empty = "🤍" * (self.max_lives - self.lives)

        self.life_label.configure(
            text=hearts + empty
        )

    # ================= BOARD =================

    def get_board(self):

        board = []

        for row in self.cells:

            current = []

            for cell in row:

                value = cell.get().strip()

                if value == "":

                   current.append(0)

                else:

                    try:
  
                      current.append(int(value))

                    except:

                      current.append(0)

            board.append(current)

        return board


    def update_board(self, board):

       for r in range(9):

        for c in range(9):

            cell = self.cells[r][c]

            cell.configure(
                state="normal",
                text_color="white"
            )

            cell.delete(0, "end")

            if board[r][c] != 0:

                cell.insert(0, str(board[r][c]))

                cell.configure(
                    state="disabled",
                    text_color="#4EA8FF"
                )
            else:

                cell.configure(
                    state="normal",
                    text_color="white"
    )

    # ================= BUTTON METHODS =================

    def generate_board(self):
        self.stop_timer()

        self.seconds = 0

        self.timer_label.configure(
            text="⏱ 00:00"
        )

        self.start_timer()
    # Reset lives
        self.lives = self.max_lives
            # Difficulty
        level = self.difficulty.get().lower()
        self.hints_used = 0
        if level == "easy":
            self.max_hints = 5

        elif level == "medium":
            self.max_hints = 3

        else:
            self.max_hints = 2
        self.update_lives()

    # Generate puzzle
        generator = SudokuGenerator()
        puzzle = generator.generate(level)

    # Save original puzzle
        self.original_board = [row[:] for row in puzzle]
       
    # Create solved board
        solved = [row[:] for row in puzzle]

        solver = SudokuSolver(solved)

        if solver.solve():
           self.solution_board = [row[:] for row in solver.board]
        else:
           self.solution_board = None

    # Show puzzle
        self.update_board(self.original_board)

        self.status.configure(
        text="Status : New Puzzle Generated"
    )         
        print(self.solution_board)       
        self.update_remaining_numbers()
        self.buttons["Hint"].configure(
             text=f"Hint ({self.max_hints - self.hints_used})"
        )
        self.current_difficulty = self.difficulty.get()

        self.game_started = True

    def solve_board(self):

        if self.solution_board is None:

            self.status.configure(
             text="Status : Generate Puzzle First"
            )
            return

        self.stop_timer()

        self.update_board(self.solution_board)

        self.update_remaining_numbers()

        self.status.configure(
            text="Status : Solution Displayed"
        )
    def check_cell(self, row, col):

        if self.solution_board is None:
            return

        cell = self.cells[row][col]

        value = cell.get().strip()

        if value == "":
            cell.configure(text_color="white")
            return

        if not value.isdigit():
            cell.delete(0, "end")
            return

        value = int(value)

        if value < 1 or value > 9:
            cell.delete(0, "end")
            return
        
            # Ignore fixed cells
            
        if self.original_board[row][col] != 0:
            return

        correct = self.solution_board[row][col]
        print(
            "Typed:",
            value,
            "Correct:",
            correct,
            "Cell:",
            row,
            col
)

        if value == correct:

            cell.configure(text_color="#4EA8FF")
            cell.configure(state="disabled")

            self.correct_cells.add((row, col))

            if (row, col) in self.wrong_cells:
                self.wrong_cells.remove((row, col))

            self.update_remaining_numbers()

            self.check_win()

        else:

            cell.configure(
                text_color="red"
            )
            self.play_sound(self.wrong_sound)
            self.lives -= 1

            self.update_lives()

            if self.lives <= 0:
                self.game_over_animation()

  

    def give_hint(self):
        if self.hints_used >= self.max_hints:

            self.status.configure(
            text="Status : No Hints Left"
            )

            return
        if self.solution_board is None:
             return

        empty_cells = []

        for r in range(9):
            for c in range(9):

                if self.original_board[r][c] == 0:

                    if self.cells[r][c].cget("state") != "disabled":

                        empty_cells.append((r, c))

        if not empty_cells:

            self.status.configure(
                text="Status : No Hint Available"
            )
            return

        row, col = random.choice(empty_cells)

        value = self.solution_board[row][col]

        cell = self.cells[row][col]

        cell.delete(0, "end")
        cell.insert(0, str(value))

        cell.configure(
             text_color="#4EA8FF",
             state="disabled"
        )

        self.correct_cells.add((row, col))

        self.hints_used += 1
        remaining = self.max_hints - self.hints_used

        self.buttons["Hint"].configure(
            text=f"Hint ({remaining})")
        self.update_remaining_numbers()

        self.status.configure(
            text=f"Status : Hint Used ({self.hints_used})"
        )

        self.check_win()
        
    def check_win(self):
        print("check_win called")
        if self.solution_board is None:
             return

        for r in range(9):
            for c in range(9):

                if self.cells[r][c].get() != str(self.solution_board[r][c]):
                    return

        self.stop_timer()

        self.show_win_popup()
        print("Opening popup...")
        self.status.configure(
            text="Status : Puzzle Completed"
        )
    def calculate_rating(self):

    # Current difficulty
        difficulty = self.current_difficulty.lower()

    # Time limit অনুযায়ী base score
        if difficulty == "easy":

            if self.seconds < 180:
                score = 5
            elif self.seconds < 300:
                score = 4
            elif self.seconds < 480:
                score = 3
            elif self.seconds < 720:
                score = 2
            else:
                score = 1

        elif difficulty == "medium":

            if self.seconds < 300:
                score = 5
            elif self.seconds < 480:
              score = 4
            elif self.seconds < 720:
                score = 3
            elif self.seconds < 1080:
                score = 2
            else:
                score = 1

        else:  # Hard

            if self.seconds < 480:
                score = 5
            elif self.seconds < 720:
                score = 4
            elif self.seconds < 1080:
                score = 3
            elif self.seconds < 1500:
                score = 2
            else:
                score = 1

    # Lives penalty
        lives_lost = self.max_lives - self.lives

        score -= lives_lost

    # Hint penalty
        score -= self.hints_used

    # Keep score between 1 and 5
        score = max(1, min(5, score))

        return score   

    def show_win_popup(self):
        self.play_sound(self.win_sound)
        stars = self.calculate_rating()

        rating = "★" * stars + "☆" * (5 - stars)

        popup = ctk.CTkToplevel(self.root)
        popup.title("Congratulations")
        popup.geometry("420x360")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Congratulations!",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(25, 8))

        ctk.CTkLabel(
            popup,
            text="You solved the Sudoku puzzle!",
            font=("Segoe UI", 16)
        ).pack(pady=(0, 20))

    # Time
        ctk.CTkLabel(
            popup,
            text=f"Time : {self.timer_label.cget('text')}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)

    # Lives
        ctk.CTkLabel(
            popup,
            text=f"Lives Left : {self.lives}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)

    # Hints
        ctk.CTkLabel(
            popup,
            text=f"Hints Used : {self.hints_used}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            popup,
            text=f"Rating : {rating}",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(10, 5))

    # Buttons
        button_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        button_frame.pack(pady=(25, 10))

        def new_game():

            popup.destroy()

            self.difficulty_menu.configure(
                state="normal"
            )

            self.generate_board()

        def close_popup():

            popup.destroy()

        ctk.CTkButton(
            button_frame,
            text="New Game",
            width=130,
            height=35,
            command=new_game
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        ctk.CTkButton(
            button_frame,
            text="Close",
            width=130,
            height=35,
            command=close_popup
        ).grid(
            row=0,
            column=1,
            padx=8
        )
    def game_over_animation(self):

        self.stop_timer()
        self.play_sound(self.game_over_sound)
        self.game_over = True

        popup = ctk.CTkToplevel(self.root)
        popup.title("Game Over")
        popup.geometry("420x330")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Game Over",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            popup,
            text="You ran out of lives!",
            font=("Segoe UI", 16)
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            popup,
            text=f"Difficulty : {self.current_difficulty}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            popup,
            text=f"Time : {self.timer_label.cget('text')}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            popup,
            text=f"Hints Used : {self.hints_used}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=5)

        button_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        button_frame.pack(pady=20)

        def restart_game():

            popup.destroy()

            self.game_over = False

            self.restart_board()

        def close_game():

           popup.destroy()

        ctk.CTkButton(
            button_frame,
            text="Restart",
            width=130,
            height=35,
            command=restart_game
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        ctk.CTkButton(
            button_frame,
            text="Close",
            width=130,
            height=35,
            command=close_game
        ).grid(
            row=0,
            column=1,
           padx=8
        )
        
    def save_game(self):

        if self.original_board is None:
            self.status.configure(text="Status : Nothing to Save")
            return

        data = {
            "original_board": self.original_board,
            "current_board": self.get_board(),
            "solution_board": self.solution_board,
            "lives": self.lives,
            "seconds": self.seconds,
            "hints_used": self.hints_used
        }

        with open("savegame.json", "w") as file:
            json.dump(data, file)

        self.status.configure(text="Status : Game Saved")

    def load_game(self):
        print("Load")
            # ================= TIMER =================
    # ================= TIMER =================

    def stop_timer(self):

        self.timer_running = False

        if self.timer_job is not None:

            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass

            self.timer_job = None


    def start_timer(self):

    # Prevent multiple timer loops
        self.stop_timer()

        self.timer_running = True

        self.timer_job = self.root.after(
            1000,
            self.update_timer
        )


    def update_timer(self):

        if not self.timer_running:
            return

        if not self.root.winfo_exists():
            return

        mins = self.seconds // 60
        secs = self.seconds % 60

        self.timer_label.configure(
            text=f"⏱ {mins:02}:{secs:02}"
        )

        self.seconds += 1

        self.timer_job = self.root.after(
            1000,
            self.update_timer
        )
            
    def update_remaining_numbers(self):

        if self.solution_board is None:
            return

        remaining = {
            number: 0
            for number in range(1, 10)
        }

    # Count how many cells are still empty
        for r in range(9):
           for c in range(9):

               if self.original_board[r][c] == 0:

                   value = self.cells[r][c].get().strip()

                   if value == "":
                        correct = self.solution_board[r][c]
                        remaining[correct] += 1

        self.remaining_numbers = remaining

    # Update labels
        # Update labels with progress colors

        for number in range(1, 10):

            count = remaining[number]

            if count == 0:
                text = f"{number} : ✓"
                text_color = "#4CAF50"       # Green

            elif count <= 2:
                text = f"{number} : {count}"
                text_color = "#4CAF50"       # Green

            elif count <= 4:
                text = f"{number} : {count}"
                text_color = "#FFD54F"       # Yellow

            elif count <= 6:
                text = f"{number} : {count}"
                text_color = "#FF9800"       # Orange

            else:
                text = f"{number} : {count}"
                text_color = "#F44336"       # Red

            self.remaining_labels[number].configure(
                text=text,
                text_color=text_color
            )
                
    def restart_board(self):

        if self.original_board is None:
            return

        self.stop_timer()

        self.seconds = 0

        self.timer_label.configure(text="⏱ 00:00")

        self.update_board(self.original_board)

        self.wrong_cells.clear()
        self.correct_cells.clear()
        self.last_wrong_value.clear()

        self.lives = self.max_lives
        self.update_lives()

        self.hints_used = 0

        self.buttons["Hint"].configure(
            text=f"Hint ({self.max_hints})"
        )

        self.update_remaining_numbers()

        self.start_timer()

        self.status.configure(
            text="Status : Game Restarted"
        )   
    def change_difficulty(self, value):

        print("Difficulty selected:", value)
        print("Game started:", self.game_started)
        print("Current difficulty:", self.current_difficulty)

    # Same difficulty
        if value == self.current_difficulty:
            return

    # Game hasn't started yet
        if not self.game_started:

            self.current_difficulty = value

            if value == "Easy":
                self.max_hints = 5

            elif value == "Medium":
                self.max_hints = 3

            else:
                self.max_hints = 2

            self.hints_used = 0

            self.buttons["Hint"].configure(
                text=f"Hint ({self.max_hints})"
             )

            return

    # =========================
    # GAME IS RUNNING
    # =========================

        old_difficulty = self.current_difficulty

        popup = ctk.CTkToplevel(self.root)

        popup.title("Change Difficulty")
        popup.geometry("400x230")
        popup.resizable(False, False)
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Change Difficulty?",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            popup,
            text="Your current game will be lost.",
            font=("Segoe UI", 16)
        ).pack(pady=10)

        button_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        button_frame.pack(pady=20)

        def continue_game():

            popup.destroy()

            self.current_difficulty = value
            self.difficulty.set(value)

            self.generate_board()

        def cancel():

            self.difficulty.set(old_difficulty)

            popup.destroy()

        ctk.CTkButton(
            button_frame,
            text="Continue",
            width=120,
            height=35,
            command=continue_game
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=35,
            command=cancel
        ).grid(
            row=0,
            column=1,
            padx=10
        )
        
         # ================= HARD =================  
           
    # ================= RUN =================

    def run(self):

        self.root.mainloop()
        