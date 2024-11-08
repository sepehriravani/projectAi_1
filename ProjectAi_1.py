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

    def find_all_positions(self, char):
        """
        پیدا کردن همه موقعیت‌های یک کاراکتر خاص در ماتریس.

        ورودی:
        - char: کاراکری که باید جستجو شود.

        خروجی:
        - لیستی از موقعیت‌ها.
        """
        positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == char:
                    positions.append((i, j))
        return positions

    def is_valid_move(self, x, y):
        """
        بررسی اینکه آیا یک حرکت معتبر است یا خیر.

        ورودی:
        - x, y: مختصات خانه مقصد.

        خروجی:
        - True اگر حرکت معتبر باشد و False در غیر این صورت.
        """
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != 'X'

    def move_cost(self, x, y):
        """
        محاسبه هزینه حرکت به یک خانه خاص.

        ورودی:
        - x, y: مختصات خانه.

        خروجی:
        - هزینه حرکت به خانه (x, y).
        """
        try:
            return int(self.grid[x][y])
        except ValueError:
            return 1  # هزینه پیش‌فرض برای خانه‌هایی که عددی نیستند.


def bfs(field):
    """
    الگوریتم جستجوی اول سطح (BFS) برای پیدا کردن مسیر کم‌هزینه برای رسیدن به اهداف.

    ورودی:
    - field: شیء IceHockeyField که زمین بازی را نمایش می‌دهد.

    خروجی:
    - مسیر طی شده، هزینه کل و عمق جستجو.
    """
    queue = deque([(field.player_pos, 0, [])])  # (موقعیت فعلی، هزینه کل، مسیر)
    visited = set()  # مجموعه‌ای برای نگهداری موقعیت‌های بازدید شده

    while queue:
        current_pos, current_cost, path = queue.popleft()

        # بررسی اگر به گل رسیده‌ایم
        if current_pos in field.goals:
            return path, current_cost, len(visited)

        if current_pos in visited:
            continue
        visited.add(current_pos)

        # بررسی حرکت به چهار جهت مختلف
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y):
                new_cost = current_cost + field.move_cost(new_x, new_y)
                queue.append(((new_x, new_y), new_cost, path + [(dx, dy)]))

    return None, float('inf'), len(visited)


# مثال استفاده
if __name__ == "__main__":
    grid = [
        ['1', 'P', '1', '1', '0', 'X', '1', '1', '1', '1'],
        ['0', 'X', '1', '1', '0', '0', '0', '1', '0', 'X'],
        ['0', '0', '1', '2', 'B', '2', '2', 'B', '1', '0'],
        ['1', '1', '0', 'X', 'X', '2', '2', '1', 'G', '1'],
        ['1', '1', '0', '0', '0', '2', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', 'G', '1', '1', '1', '1']
    ]
    field = IceHockeyField(grid)
    path, total_cost, search_depth = bfs(field)
    print("مسیر BFS:", path)
    print("هزینه کل:", total_cost)
    print("عمق جستجو:", search_depth)
