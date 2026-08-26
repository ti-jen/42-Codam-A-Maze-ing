import random
from .maze_patterns import check_pattern, PatternError


def gen_grid(axis_x: int,
             axis_y: int) -> list[list[str]]:
    grid = [['f' for _ in range(axis_y)] for _ in range(axis_x)]
    return grid


def is_valid_path(axis_x: int,
                  axis_y: int,
                  maze: list[list[str]],
                  pat: list[tuple[int, int]]) -> list[str]:
    opt = []
    if (axis_x - 1 >= 0
            and maze[axis_x - 1][axis_y] == 'f'
            and not (axis_x - 1, axis_y) in pat):
        opt.append('north')
    if (axis_x + 1 < len(maze)
            and maze[axis_x + 1][axis_y] == 'f'
            and not (axis_x + 1, axis_y) in pat):
        opt.append('south')
    if (axis_y - 1 >= 0
            and maze[axis_x][axis_y - 1] == 'f'
            and not (axis_x, axis_y - 1) in pat):
        opt.append('west')
    if (axis_y + 1 < len(maze[axis_x])
            and maze[axis_x][axis_y + 1] == 'f'
            and not (axis_x, axis_y + 1) in pat):
        opt.append('east')

    return (opt)


def set_bit(value: str, bit: int) -> str:
    return (hex(int(value, 16) & ~(1 << bit))[2:])


def open_path(axis_x: int,
              axis_y: int,
              maze: list[list[str]],
              dir: str = '') -> list[list[str]]:
    if dir == 'north':
        maze[axis_x][axis_y] = set_bit(maze[axis_x][axis_y], 0)
        maze[axis_x - 1][axis_y] = set_bit(maze[axis_x - 1][axis_y], 2)
    elif dir == 'east':
        maze[axis_x][axis_y] = set_bit(maze[axis_x][axis_y], 1)
        maze[axis_x][axis_y + 1] = set_bit(maze[axis_x][axis_y + 1], 3)
    elif dir == 'west':
        maze[axis_x][axis_y] = set_bit(maze[axis_x][axis_y], 3)
        maze[axis_x][axis_y - 1] = set_bit(maze[axis_x][axis_y - 1], 1)
    elif dir == 'south':
        maze[axis_x][axis_y] = set_bit(maze[axis_x][axis_y], 2)
        maze[axis_x + 1][axis_y] = set_bit(maze[axis_x + 1][axis_y], 0)
    return (maze)


def maze_depth_first(axis_x: int,
                     axis_y: int,
                     maze: list[list[str]],
                     pat: list[tuple[int, int]],
                     isper: bool) -> list[list[str]]:
    focus = [(axis_x, axis_y)]
    while focus:
        x = focus[-1][0]
        y = focus[-1][1]
        path_list = is_valid_path(x, y, maze, pat)
        if path_list:
            dir = random.choice(path_list)
            maze = open_path(x, y, maze, dir)
            if dir == 'north':
                focus.append((x - 1, y))
            elif dir == 'east':
                focus.append((x, y + 1))
            elif dir == 'west':
                focus.append((x, y - 1))
            elif dir == 'south':
                focus.append((x + 1, y))
        else:
            if not isper and int(maze[x][y], 16).bit_count() >= 3:
                if (x - 1 >= 0
                        and not (x - 1, y) in pat
                        and (int(maze[x][y], 16) & (1 << 0)) != 0):
                    path_list.append('north')
                if (x + 1 < len(maze)
                        and not (x + 1, y) in pat
                        and (int(maze[x][y], 16) & (1 << 2)) != 0):
                    path_list.append('south')
                if (y - 1 >= 0
                        and not (x, y - 1) in pat
                        and (int(maze[x][y], 16) & (1 << 3)) != 0):
                    path_list.append('west')
                if (y + 1 < len(maze[x])
                        and not (x, y + 1) in pat
                        and (int(maze[x][y], 16) & (1 << 1)) != 0):
                    path_list.append('east')
                if path_list:
                    dir = random.choice(path_list)
                    maze = open_path(x, y, maze, dir)
            del focus[-1]
    return maze


def gen_maze(axis_x: int,
             axis_y: int,
             isper: bool,
             pat: str | None,
             seed: int | None) -> list[list[str]]:

    if seed is not None:
        random.seed(seed)
    maze = gen_grid(axis_x, axis_y)
    if pat is None:
        pattern: list[tuple[int, int]] = []
    else:
        pattern = check_pattern(maze, pat)
    x_start = 0
    isbuild = False
    for x in maze:
        y_start = 0
        for _ in x:
            if (not ((x_start, y_start) in pattern)
                    and maze[x_start][y_start] == 'f'):
                if isbuild:
                    raise PatternError('pattern blocks to make complete maze')
                maze = maze_depth_first(x_start, y_start, maze, pattern, isper)
                isbuild = True
            y_start += 1
        x_start += 1
    return maze


def main() -> None:
    gen_maze(11, 11, True, '42', 0)


if __name__ == "__main__":
    main()
