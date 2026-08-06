import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Sudoku Solver Pro")
    root.geometry("900x700")
    root.minsize(900, 700)

    label = tk.Label(
        root,
        text="Sudoku Solver Pro",
        font=("Segoe UI", 28, "bold")
    )

    label.pack(pady=30)

    root.mainloop()


if __name__ == "__main__":
    main()