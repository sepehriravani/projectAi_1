class IceHockeyField:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.player_pos = self.find_position('P')
        self.goals = self.find_all_positions('G')
        self.pucks = self.find_all_positions('B')
        self.obstacles = self.find_all_positions('X')

    def find_position(self, char):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == char:
                    return (i, j)
        return None

    def find_all_positions(self, char):
        positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == char:
                    positions.append((i, j))
        return positions

    def is_valid_move(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != 'X'

    def move_cost(self, x, y):
        try:
            return int(self.grid[x][y])
        except ValueError:
            return 1


def bfs(field):
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
    def heuristic(pos):
        return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in field.goals)

    queue = [(0, field.player_pos, 0, [])]
    visited = set()

    while len(queue) > 0:
        queue.sort()  # مرتب‌سازی دستی
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
    algorithms = [bfs, dfs, ucs, a_star]

    for algo in algorithms:
        path, total_cost, search_depth = algo(field)
        print(f"{algo.__name__} Path:", path)
        print("Total Cost:", total_cost)
        print("Search Depth:", search_depth)
        print("-" * 40)
