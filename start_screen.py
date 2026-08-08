import customtkinter as ctk
from game_screen import GameScreen
import webbrowser
class StartScreen:

    def __init__(self):

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title("Sudoku Solver Pro")

        self.root.geometry("900x600")

        self.root.resizable(False, False)

        self.create_ui()

    def create_ui(self):

        title = ctk.CTkLabel(
            self.root,
            text="Sudoku Solver Pro",
            font=("Segoe UI", 42, "bold")
        )

        title.pack(pady=(80, 15))

        subtitle = ctk.CTkLabel(
            self.root,
            text="Play • Solve • Learn",
            font=("Segoe UI", 20)
        )

        subtitle.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self.root,
            text="▶ Start Game",
            width=220,
            height=55,
            font=("Segoe UI",18,"bold"),
            command=self.start_game
        )

        self.start_button.pack(pady=50)

        

        self.about_button = ctk.CTkButton(
            self.root,
            text="ℹ About",
            width=220,
            height=45,
            font=("Segoe UI", 16),
            command=self.show_about
        )

        self.about_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(
            self.root,
            text="Exit",
            width=220,
            height=45,
            fg_color="#B22222",
            hover_color="#8B0000",
            command=self.root.destroy
        )

        self.exit_button.pack(pady=40)
    def show_about(self):

    # Hide first screen
        self.root.withdraw()

        about = ctk.CTkToplevel(self.root)
        about.title("About Sudoku Solver Pro")
        about.geometry("650x720")
        about.resizable(False, False)

        about.transient(self.root)
        about.grab_set()

    # Back function
        def go_back():
            about.grab_release()
            about.destroy()
            self.root.deiconify()

    # Back button - TOP LEFT
        ctk.CTkButton(
            about,
            text="← Back",
        width=90,
        height=32,
        corner_radius=8,
        font=("Segoe UI", 13, "bold"),
        command=go_back
        ).place(
        x=20,
        y=15
        )

    # Main frame
        main_frame = ctk.CTkFrame(
            about,
            corner_radius=18
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(55, 15)
        )

    # Title
        ctk.CTkLabel(
        main_frame,
        text="About Sudoku Solver Pro",
        font=("Segoe UI", 25, "bold"),
        text_color="#4EA8FF"
    ).pack(pady=(20, 12))

    # What is Sudoku?
        ctk.CTkLabel(
        main_frame,
        text="What is Sudoku?",
        font=("Segoe UI", 17, "bold"),
        text_color="#F44336"
        ).pack(
        anchor="w",
        padx=25,
        pady=(5, 5)
        )

        ctk.CTkLabel(
            main_frame,
         text=(
            "Sudoku is a number puzzle played on a 9×9 grid.\n"
            "The goal is to fill every empty cell with numbers\n"
            "from 1 to 9."
        ),
        font=("Segoe UI", 13),
        justify="left",
        anchor="w"
        ).pack(
        anchor="w",
        padx=25
    )

    # How to Play
        ctk.CTkLabel(
        main_frame,
        text="How to Play",
        font=("Segoe UI", 17, "bold"),
        text_color="#F44336"
    ).pack(
        anchor="w",
        padx=25,
        pady=(12, 5)
    )

        ctk.CTkLabel(
         main_frame,
        text=(
            "• Each row must contain 1–9 without repetition.\n"
            "• Each column must contain 1–9 without repetition.\n"
            "• Each 3×3 box must contain 1–9 without repetition.\n"
            "• Enter numbers in empty cells to solve the puzzle."
        ),
        font=("Segoe UI", 13),
        justify="left",
        anchor="w"
    ).pack(
        anchor="w",
        padx=25
    )

    # Game Features
        ctk.CTkLabel(
        main_frame,
        text="Game Features",
        font=("Segoe UI", 17, "bold"),
        text_color="#F44336"
    ).pack(
        anchor="w",
        padx=25,
        pady=(12, 5)
    )

        ctk.CTkLabel(
        main_frame,
        text=(
            "• Easy, Medium & Hard difficulty\n"
            "• 3 Lives\n"
            "• Limited Hints\n"
            "• Timer\n"
            "• Remaining Number Progress\n"
            "• Rating after completing a puzzle\n"
            "• Sound Effects"
        ),
        font=("Segoe UI", 13),
        justify="left",
        anchor="w"
    ).pack(
        anchor="w",
        padx=25
    )

    # Tip
        ctk.CTkLabel(
        main_frame,
        text="Tip",
        font=("Segoe UI", 17, "bold"),
        text_color="#F44336"
    ).pack(
        anchor="w",
        padx=25,
        pady=(12, 5)
    )

        ctk.CTkLabel(
        main_frame,
        text=(
            "Use logic and check the row, column and 3×3 box\n"
            "before entering a number."
        ),
        font=("Segoe UI", 13),
        justify="left",
        anchor="w"
    ).pack(
        anchor="w",
        padx=25
    )

    # Developer
        ctk.CTkLabel(
        main_frame,
        text="Developed by\nROJOT KAIRY RAJ",
        font=("Segoe UI", 15, "bold"),
        text_color="#4EA8FF"
    ).pack(
        pady=(10, 2)
    )

    # Red symbol
        ctk.CTkLabel(
        main_frame,
        text="(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
        font=("Segoe UI", 15, "bold"),
        text_color="#F44336"
    ).pack(
        pady=(0, 2)
    )

    # Version
        ctk.CTkLabel(
        main_frame,
        text="Sudoku Solver Pro  •  Version 1.0",
        font=("Segoe UI", 11),
        text_color="#A0A0A0"
    ).pack(
        pady=(0, 5)
    )

    # GitHub
        ctk.CTkButton(
        main_frame,
        text="GitHub",
        width=180,
        height=35,
        corner_radius=10,
        font=("Segoe UI", 14, "bold"),
        command=lambda: webbrowser.open(
            "https://github.com/Rojot-Kairy-Raj"
        )
    ).pack(
        pady=(3, 5)
    )

    # Back button
        def go_back():

            about.grab_release()
            about.destroy()

            self.root.deiconify()

        ctk.CTkButton(
            main_frame,
            text="Back",
            width=180,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 14, "bold"),
            command=go_back
        ).pack(pady=(3, 8))

    def start_game(self):

        self.root.withdraw()

        game = GameScreen()

        game.run()

        self.root.destroy()
    
    def run(self):
        self.root.mainloop()