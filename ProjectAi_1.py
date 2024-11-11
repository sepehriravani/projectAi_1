class IceHockeyField:
    def __init__(self, grid):
        """
        کلاس IceHockeyField برای تعریف زمین بازی هاکی روی یخ.

        پارامتر:
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
    الگوریتم جستجوی اول سطح (BFS) برای پیدا کردن مسیر بهینه.
    """
    queue = [(field.player_pos, 0, [])]
    visited = set()

    while len(queue) > 0:
        current_pos, current_cost, path = queue.pop(0)
        if current_pos in field.goals:
            return path, current_cost, len(visited)

        if current_pos in visited:
            continue
        visited.add(current_pos)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y):
                new_cost = current_cost + field.move_cost(new_x, new_y)
                queue.append(((new_x, new_y), new_cost, path + [(dx, dy)]))

    return None, float('inf'), len(visited)


def dfs(field):
    """
    الگوریتم جستجوی اول عمق (DFS) برای پیدا کردن مسیر بهینه.
    """
    stack = [(field.player_pos, 0, [])]
    visited = set()

    while len(stack) > 0:
        current_pos, current_cost, path = stack.pop()
        if current_pos in field.goals:
            return path, current_cost, len(visited)

        if current_pos in visited:
            continue
        visited.add(current_pos)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y):
                new_cost = current_cost + field.move_cost(new_x, new_y)
                stack.append(((new_x, new_y), new_cost, path + [(dx, dy)]))

    return None, float('inf'), len(visited)


def ucs(field):
    """
    الگوریتم جستجوی یکسان-هزینه (UCS).
    """
    queue = [(0, field.player_pos, [])]
    visited = set()

    while len(queue) > 0:
        queue.sort()  # مرتب‌سازی دستی برای پیدا کردن کم‌هزینه‌ترین مسیر
        current_cost, current_pos, path = queue.pop(0)
        if current_pos in field.goals:
            return path, current_cost, len(visited)

        if current_pos in visited:
            continue
        visited.add(current_pos)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y):
                new_cost = current_cost + field.move_cost(new_x, new_y)
                queue.append((new_cost, (new_x, new_y), path + [(dx, dy)]))

    return None, float('inf'), len(visited)


def a_star(field):
    """
    الگوریتم جستجوی آگاهانه (A*) برای پیدا کردن مسیر بهینه.
    """
    def heuristic(pos):
        return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in field.goals)

    queue = [(0, field.player_pos, 0, [])]
    visited = set()

    while len(queue) > 0:
        queue.sort()
        f_cost, current_pos, g_cost, path = queue.pop(0)
        if current_pos in field.goals:
            return path, g_cost, len(visited)

        if current_pos in visited:
            continue
        visited.add(current_pos)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y):
                new_g_cost = g_cost + field.move_cost(new_x, new_y)
                f_cost = new_g_cost + heuristic((new_x, new_y))
                queue.append((f_cost, (new_x, new_y), new_g_cost, path + [(dx, dy)]))

    return None, float('inf'), len(visited)


def print_results(algo_name, path, total_cost, search_depth):
    """
    تابعی برای چاپ نتایج الگوریتم‌ها با توجه به شرایط خواسته شده در پروژه.
    """
    if len(path) > 50:
        path_to_print = path[:50]
        print(f"{algo_name} Path (first 50 moves):", path_to_print, "...")
    else:
        print(f"{algo_name} Path:", path)

    print("Total Cost:", total_cost)
    print("Search Depth:", search_depth)
    print("-" * 40)


def test_algorithms(field, algorithms):
    """
    تابع تست الگوریتم‌ها و چاپ نتایج آن‌ها.
    """
    for algo in algorithms:
        path, total_cost, search_depth = algo(field)
        print_results(algo.__name__, path, total_cost, search_depth)


if __name__ == "__main__":
    # تعریف نقشه بازی
    grid = [
        ['1', 'P', '1', '1', '0', 'X', '1', '1', '1', '1'],
        ['0', 'X', '1', '1', '0', '0', '0', '1', '0', 'X'],
        ['0', '0', '1', '2', 'B', '2', '2', 'B', '1', '0'],
        ['1', '1', '0', 'X', 'X', '2', '2', '1', 'G', '1'],
        ['1', '1', '0', '0', '0', '2', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '1', 'G', '1', '1', '1', '1']
    ]
    field = IceHockeyField(grid)

    # لیست الگوریتم‌ها
    algorithms = [bfs, dfs, ucs, a_star]

    # اجرای تست برای الگوریتم‌ها
    test_algorithms(field, algorithms)
