import customtkinter as ctk
from solver import SudokuSolver
from generator import SudokuGenerator


class SudokuGUI:

    def __init__(self):
    
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title("Sudoku Solver Pro")

        self.root.geometry("1200x800")

        self.root.minsize(1000,700)

        self.root.grid_columnconfigure(0,weight=3)
        self.root.grid_columnconfigure(1,weight=1)

        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_rowconfigure(1,weight=0)

        self.cells=[]
        self.original_board = None
        self.max_lives = 3
        self.lives = 3
        self.solution_board = None
        self.create_ui()


    def create_ui(self):

        self.left_frame=ctk.CTkFrame(
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

        self.right_frame=ctk.CTkFrame(
            self.root,
            width=250,
            corner_radius=15
        )

        self.right_frame.grid(
            row=0,
            column=1,
            padx=(0,20),
            pady=20,
            sticky="ns"
        )

        title=ctk.CTkLabel(
            self.left_frame,
            text="Sudoku Solver Pro",
            font=("Segoe UI",28,"bold")
        )

        title.pack(pady=20)

        self.grid_frame=ctk.CTkFrame(
            self.left_frame,
            fg_color="transparent"
        )

        self.grid_frame.pack(expand=True)

        for r in range(9):

            row=[]

            for c in range(9):

                cell=ctk.CTkEntry(
                    self.grid_frame,
                    width=50,
                    height=50,
                    justify="center",
                    font=("Segoe UI",18)
                )

                padx=(
                    4 if c%3==0 else 1,
                    4 if c%3==2 else 1
                )

                pady=(
                    4 if r%3==0 else 1,
                    4 if r%3==2 else 1
                )

                cell.grid(
                    row=r,
                    column=c,
                    padx=padx,
                    pady=pady
                )

                row.append(cell)

            self.cells.append(row)

        buttons=[
            "Solve",
            "Generate",
            "Check",
            "Hint",
            "Clear",
            "Save",
            "Load"
        ]

        for text in buttons:

            command = None

            if text == "Generate":
                command = self.generate_board

            elif text == "Solve":
                command = self.solve_board

            elif text == "Clear":
                command = self.clear_board

            button = ctk.CTkButton(
                self.right_frame,
                text=text,
                width=180,
                height=42,
                command=command
            )

            button.pack(
                fill="x",
                padx=20,
                pady=8
            )

            self.buttons[text] = button

        button.pack(
                fill="x",
                padx=20,
                pady=8
            )

        # ---------- Lives ----------
        self.life_label = ctk.CTkLabel(
            self.right_frame,
            text="❤️❤️❤️",
            font=("Segoe UI", 22, "bold")
        )

        self.life_label.pack(
            pady=(15, 20)
        )

        # ---------- Status ----------
        self.status = ctk.CTkLabel(
            self.root,
            text="Status : Ready",
            anchor="w"
        )

        self.status.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(0, 10)
        )
    def get_board(self):

         board=[]

         for row in self.cells:

            current=[]

            for cell in row:

                value=cell.get().strip()

                if value=="":
                    current.append(0)

                else:
                    try:
                        current.append(int(value))
                    except ValueError:
                        current.append(0)

            board.append(current)

         return board


    def update_board(self, board):

     for r in range(9):
        for c in range(9):

            cell = self.cells[r][c]

            cell.configure(state="normal")

            cell.delete(0, "end")

            if board[r][c] != 0:
                cell.insert(0, str(board[r][c]))
                cell.configure(state="disabled")
            else:
                cell.configure(state="normal")

     self.root.update_idletasks()


    def solve_board(self):

        board=self.get_board()

        solver=SudokuSolver(board)

        if solver.solve():

            self.update_board(board)

            self.status.configure(
                text="Status : Solved Successfully"
            )

        else:

            self.status.configure(
                text="Status : No Solution Found"
            )


    def clear_board(self):

     if self.original_board is None:
        return

     self.update_board(self.original_board)

     self.status.configure(
        text="Status : Cleared"
    )

    def generate_board(self):

      self.lives = self.max_lives
      self.update_lives()

      generator = SudokuGenerator()

      puzzle = generator.generate("medium")

      self.original_board = [row[:] for row in puzzle]

      solved_board = [row[:] for row in puzzle]

      solver = SudokuSolver(solved_board)

      if solver.solve():
        self.solution_board = [row[:] for row in solver.board]
      else:
        self.solution_board = None

      self.update_board(self.original_board)

      self.status.configure(
        text="Status : New Puzzle Generated"
    )


    def validate_input(self,value):

        if value=="":
            return True

        if len(value)>1:
            return False

        return value in "123456789"
    def generate_board(self):

     self.status.configure(
        text="Generate Button Clicked"
    )


def solve_board(self):

    self.status.configure(
        text="Solve Button Clicked"
    )


def clear_board(self):

    self.status.configure(
        text="Clear Button Clicked"
    )

    def run(self):

        self.root.mainloop()