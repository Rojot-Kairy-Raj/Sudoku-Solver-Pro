import random


class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num):

        # Row
        for x in range(9):
            if self.board[row][x] == num:
                return False

        # Column
        for x in range(9):
            if self.board[x][col] == num:
                return False

        # 3x3 Box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def fill_board(self):

        for row in range(9):
            for col in range(9):

                if self.board[row][col] == 0:

                    numbers = list(range(1, 10))
                    random.shuffle(numbers)

                    for num in numbers:

                        if self.is_valid(row, col, num):

                            self.board[row][col] = num

                            if self.fill_board():
                                return True

                            self.board[row][col] = 0

                    return False

        return True
    def remove_numbers(self, difficulty="medium"):

        if difficulty == "easy":
            filled_count = random.randint(45, 50)

        elif difficulty == "hard":
            filled_count = random.randint(28, 30)

        else:
            filled_count = random.randint(35, 40)

        remove_count = 81 - filled_count

        while remove_count > 0:

            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                self.board[row][col] = 0
                remove_count -= 1

    def generate(self, difficulty="medium"):
        print("NEW GENERATOR RUNNING")
        # Reset board
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        # Generate complete valid board
        self.fill_board()

        # Remove numbers
        self.remove_numbers(difficulty)

        # Return a copy
        return [row[:] for row in self.board]