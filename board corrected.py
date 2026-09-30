import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        values = [x for x in line if x]
        result = []
        score_gained = 0
        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged_val = values[i] * 2
                result.append(merged_val)
                score_gained += merged_val
                i += 2
            else:
                result.append(values[i])
                i += 1
        return result + [0] * (SIZE - len(result)), score_gained

    def move_left(self):
        changed = False
        score_added = 0
        for r in range(SIZE):
            old = self.grid[r][:]
            new_line, gained = self.slide_line(old)
            self.grid[r] = new_line
            if old != new_line:
                changed = True
                score_added += gained
        if changed:
            self.score += score_added
        return changed, score_added

    def move_right(self):
        changed = False
        score_added = 0
        for r in range(SIZE):
            old = self.grid[r][:]
            reversed_old = list(reversed(old))
            new_line, gained = self.slide_line(reversed_old)
            new_row = list(reversed(new_line))
            self.grid[r] = new_row
            if old != new_row:
                changed = True
                score_added += gained
        if changed:
            self.score += score_added
        return changed, score_added

    def move_up(self):
        changed = False
        score_added = 0
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new_line, gained = self.slide_line(old)
            for r in range(SIZE):
                self.grid[r][c] = new_line[r]
            new_col = [self.grid[r][c] for r in range(SIZE)]
            if old != new_col:
                changed = True
                score_added += gained
        if changed:
            self.score += score_added
        return changed, score_added

    def move_down(self):
        changed = False
        score_added = 0
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new_line, gained = self.slide_line(list(reversed(old)))
            new_col_vals = list(reversed(new_line))
            for r in range(SIZE):
                self.grid[r][c] = new_col_vals[r]
            new_col = [self.grid[r][c] for r in range(SIZE)]
            if old != new_col:
                changed = True
                score_added += gained
        if changed:
            self.score += score_added
        return changed, score_added

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False