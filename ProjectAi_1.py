class IceHockeyField:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.player_pos = self.find_position('p')
        self.goals = self.find_all_positions('g')
        self.pucks = self.find_all_positions('b')
        self.obstacles = self.find_all_positions('x')

    def find_position(self, char):
        for i in range(self.rows):
            for j in range(self.cols):
                if char in self.grid[i][j]:
                    return (i, j)
        return None

    def find_all_positions(self, char):
        positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if char in self.grid[i][j]:
                    positions.append((i, j))
        return positions

    def is_valid_move(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and 'x' not in self.grid[x][y]

    def move_cost(self, x, y):
        try:
            return int(self.grid[x][y][0])
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
        queue.sort()
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


def best_first_search(field):
    def heuristic(pos):
        return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in field.goals)

    queue = [(0, field.player_pos, [])]
    visited = set()
    while len(queue) > 0:
        queue.sort()
        h_cost, current_pos, path = queue.pop(0)
        if current_pos in field.goals:
            return path, len(path), len(visited)
        if current_pos in visited:
            continue
        visited.add(current_pos)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y):
                queue.append((heuristic((new_x, new_y)), (new_x, new_y), path + [(dx, dy)]))
    return None, float('inf'), len(visited)


def ida_star(field):
    def heuristic(pos):
        return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in field.goals)

    def search(path, g_cost, bound):
        current_pos = path[-1]
        f_cost = g_cost + heuristic(current_pos)
        if f_cost > bound:
            return f_cost
        if current_pos in field.goals:
            return path, g_cost
        min_cost = float('inf')
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if field.is_valid_move(new_x, new_y) and (new_x, new_y) not in path:
                path.append((new_x, new_y))
                result = search(path, g_cost + field.move_cost(new_x, new_y), bound)
                if isinstance(result, tuple):
                    return result
                min_cost = min(min_cost, result)
                path.pop()
        return min_cost

    bound = heuristic(field.player_pos)
    path = [field.player_pos]
    while True:
        result = search(path, 0, bound)
        if isinstance(result, tuple):
            return result[0], result[1], len(path)
        if result == float('inf'):
            return None, float('inf'), len(path)
        bound = result


def print_results(algo_name, path, total_cost, search_depth):
    if len(path) > 50:
        path_to_print = path[:50]
        print(f"{algo_name} Path (first 50 moves):", path_to_print, "...")
    else:
        print(f"{algo_name} Path:", path)
    print("Total Cost:", total_cost)
    print("Search Depth:", search_depth)
    print("-" * 40)


def test_algorithms(field, algorithms):
    for algo in algorithms:
        path, total_cost, search_depth = algo(field)
        print_results(algo.__name__, path, total_cost, search_depth)


if __name__ == "__main__":
    input_matrix1 = [
        ["1", "3", "0", "x", "1"],
        ["0p", "1b", "0", "0", "1g"],
        ["0", "4", "0", "x", "1"],
        ["0", "0", "0", "0", "1"],
    ]

    input_matrix2 = [
        ["1", "3", "1", "1"],
        ["0p", "1b", "0b", "1g"],
        ["0", "4", "1", "1"],
        ["0", "0", "1", "1"],
        ["1", "1g", "1", "1"],
        ["1", "1", "1", "1"],
    ]

    input_matrix3 = [
        ["1p", "3"],
        ["0b", "3"],
        ["0", "x"],
        ["0", "0"],
        ["1g", "1"],
        ["1", "1"],
    ]

    algorithms = [bfs, dfs, ucs, a_star, best_first_search, ida_star]

    for i, matrix in enumerate([input_matrix1, input_matrix2, input_matrix3], start=1):
        print(f"\n--- Testing Input Matrix {i} ---\n")
        field = IceHockeyField(matrix)
        test_algorithms(field, algorithms)
