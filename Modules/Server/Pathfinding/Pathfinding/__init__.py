import Sweep

def find_path(width: int = 10, height: int = 10, start: tuple = (0,0), known_points=[]):
    paths: list = Sweep.generate_paths(width, height, known_points=known_points)
    return paths