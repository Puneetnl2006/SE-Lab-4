from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves:
            return False, "Invalid command."

        grid_copy = [row[:] for row in self.board.grid]
        score_copy = self.board.score

        changed, score_added = moves[key]()
        if changed:
            self.history = [(grid_copy, score_copy)]
            self.board.add_random_tile()
            self.best_score = max(self.best_score, self.board.score)
            feedback = f"Moved {key.upper()}. Score +{score_added}." if score_added > 0 else f"Moved {key.upper()}."
            return True, feedback
        return False, "Move had no effect."

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            if any(2048 in row for row in self.board.grid):
                print("You reached 2048!")
                return
            if not self.board.can_move():
                print("No legal moves remain.")
                return
            key = input("> ").strip().lower()
            if key == "q":
                print("Goodbye!")
                return
            if key == "u":
                if not self.history:
                    print("Nothing to undo.")
                else:
                    grid_prev, score_prev = self.history.pop()
                    self.board.grid = grid_prev
                    self.board.score = score_prev
                    print("Undo successful.")
                continue
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue

            success, feedback = self.move(key)
            print(feedback)
            if success and any(2048 in row for row in self.board.grid):
                self.display()
                print("You reached 2048!")
                return