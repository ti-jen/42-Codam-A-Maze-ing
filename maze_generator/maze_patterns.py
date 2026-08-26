
def patterns(pat: str) -> list[list[int]] | None:
    patdict = {
        '42': [[1, 0, 0, 0, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 0, 1, 1, 1],
               [0, 0, 1, 0, 1, 0, 0],
               [0, 0, 1, 0, 1, 1, 1]],
        'star': [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                 [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                 [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                 [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                 [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]],

        'circle': [[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
                   [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                   [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                   [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
                   [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                   [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                   [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
                   [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]],

        'smiley': [[0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                   [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                   [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                   [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0],
                   [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]],

    }
    if pat in patdict:
        return patdict[pat]
    else:
        return None


class PatternError(Exception):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)


class PatternErrorinput(PatternError):
    def __init__(self, args: str) -> None:
        super().__init__(f"pattern '{args}' does not exist")


class PatternErrorsize(PatternError):
    def __init__(self, x_grid: int, y_grid: int,
                 x_pat: int, y_pat: int) -> None:
        super().__init__(f"pattern[x:{x_pat}][y:{y_pat}]"
                         f" does not fit in grid[x:{x_grid}][y:{y_grid}]")


def check_pattern(maze: list[list[str]],
                  pat: str) -> list[tuple[int, int]]:
    pattern = patterns(pat)
    if pattern is None:
        raise PatternErrorinput(pat)
    x_grid = len(maze)
    y_grid = len(maze[0])
    x_pat = len(pattern)
    y_pat = len(pattern[0])

    x_check = int(x_grid / 2) - int(x_pat / 2)
    y_check = int(y_grid / 2) - int(y_pat / 2)

    if (x_check < 0 or y_check < 0) or (x_grid < x_pat or y_grid < y_pat):
        raise PatternErrorsize(x_grid, y_grid, x_pat, y_pat)

    result = []
    for y in pattern:
        for c in y:
            if c == 1:
                result.append((x_check, y_check))
            y_check += 1
        x_check += 1
        y_check = int(y_grid / 2) - int(y_pat / 2)
    return result


def gen_grid(axis_x: int,
             axis_y: int) -> list[list[str]]:
    grid = [['f' for _ in range(axis_y)] for _ in range(axis_x)]
    return grid


def main() -> None:
    check_pattern(gen_grid(11, 12), '42')


if __name__ == "__main__":
    main()
