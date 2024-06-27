import heapq

class Path:
    def __init__(self):
        pass
    def create_grid(self, rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]

    def add_point(self, grid, point, value):
        x, y = point
        grid[x][y] = value

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, grid, start, goal):
        rows, cols = len(grid), len(grid[0])
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found
    
    def find_path(self, width: int = 10, height: int = 10, start = (0,0), points=[], goal = (10,10)) -> list: # Points in (x, y format)
        rows, cols = height, width
        self.grid = eval(open('space.ary', 'r').read())
        if self.grid == '':
            self.create_grid(rows, cols)
        self.start = start
        self.goal = goal

        for point in points:
            print(point)
            self.add_point(self.grid, point, 1)

        # Find path
        path = self.a_star(self.grid, self.start, self.goal)
        print(path)
        return path