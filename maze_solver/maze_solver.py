from collections import deque


def get_neighbors(
    maze: list[list[str]],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    x, y = position

    height = len(maze)
    width = len(maze[0])

    value = int(maze[y][x], 16)

    neighbors: list[tuple[int, int]] = []

    # North
    if y > 0 and not value & 1:
        neighbors.append((x, y - 1))

    # East
    if x + 1 < width and not value & 2:
        neighbors.append((x + 1, y))

    # South
    if y + 1 < height and not value & 4:
        neighbors.append((x, y + 1))

    # West
    if x > 0 and not value & 8:
        neighbors.append((x - 1, y))

    return neighbors


def solve_maze(
    maze: list[list[str]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
) -> list[tuple[int, int]]:
    queue = deque([entry])

    came_from: dict[
        tuple[int, int],
        tuple[int, int] | None,
    ] = {
        entry: None
    }

    while queue:
        current = queue.popleft()

        if current == exit_pos:
            break

        for neighbor in get_neighbors(maze, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if exit_pos not in came_from:
        return []

    path: list[tuple[int, int]] = []
    path_current: tuple[int, int] | None = exit_pos

    while path_current is not None:
        path.append(path_current)
        path_current = came_from[path_current]

    path.reverse()

    return path
