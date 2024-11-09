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
