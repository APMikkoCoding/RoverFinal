import Finder

def generate_paths(height, width, known_points: list  = []):
    finder = Finder.Path()
    paths = []
    for i in range(height):
        print(i)
        if i % 2 == 0:
            paths.append(finder.find_path(height=height, width=width, points=known_points, goal=(width-1, i), start=(0, i)))
        else:
            paths.append(finder.find_path(height=height, width=width, points=known_points, goal=(0, i), start=(width-1, i)))
    return paths