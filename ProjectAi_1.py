import heapq
from collections import deque

class IceHockeyField:
    def __init__(self, grid):
        """
        کلاس IceHockeyField برای تعریف زمین بازی هاکی روی یخ.

        ورودی:
        - grid: ماتریسی که نشان‌دهنده زمین بازی است.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.player_pos = self.find_position('P')  # موقعیت بازیکن
        self.goals = self.find_all_positions('G')  # لیست موقعیت‌های گل‌ها
        self.pucks = self.find_all_positions('B')  # لیست موقعیت‌های توپ‌ها
        self.obstacles = self.find_all_positions('X')  # لیست موقعیت‌های موانع

    def find_position(self, char):
        """
        پیدا کردن اولین موقعیت یک کاراکتر خاص در ماتریس.

        ورودی:
        - char: کاراکتری که باید جستجو شود.

        خروجی:
        - موقعیت کاراکتر به صورت (i, j) یا None در صورت نبود آن.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == char:
                    return (i, j)
        return None