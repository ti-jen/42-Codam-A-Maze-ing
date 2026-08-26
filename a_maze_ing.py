from pydantic import BaseModel, Field, ValidationError
from enum import Enum
from maze_generator import gen_maze, PatternError
import configparser
import sys
from maze_display import run_display
from maze_solver import solve_maze


def path_to_directions(path: list[tuple[int, int]]) -> str:
    directions = ""

    for current, next_pos in zip(path, path[1:]):
        x, y = current
        next_x, next_y = next_pos

        if next_y < y:
            directions += "N"
        elif next_x > x:
            directions += "E"
        elif next_y > y:
            directions += "S"
        elif next_x < x:
            directions += "W"

    return directions


def write_maze(output_file: str,
               maze: list[list[str]],
               entry: tuple[int, int],
               exit: tuple[int, int]) -> None:
    result = ''
    for x in maze:
        for y in x:
            result += y
        result += '\n'
    result += '\n'
    result += f"{entry[0]},{entry[1]}\n"
    result += f"{exit[0]},{exit[1]}\n"

    path = solve_maze(maze, entry, exit)
    directions = path_to_directions(path)
    result += directions + "\n"

    with open(output_file, 'w') as file:
        file.write(result)


class Patterns(Enum):
    STAR = 'star'
    P42 = '42'
    CIRCLE = 'circle'
    SMILEY = 'smiley'


class maze_configs(BaseModel):
    height: int = Field(ge=1)
    width: int = Field(ge=1)
    is_perfect: bool
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    pattern: Patterns
    seed: int = Field(ge=0)


def parse_coords(value: str) -> tuple[int, int]:
    parts = value.split(',')

    if len(parts) != 2:
        raise ValueError("Coordinates must contain exactly two values")

    return (int(parts[0]), int(parts[1]))


def main() -> None:
    if len(sys.argv) != 2:
        print('> python a_maze_ing.py [example.txt]')
        exit()

    file = configparser.ConfigParser()
    file.read(sys.argv[1])
    try:
        config = maze_configs(height=file.getint('MAZE', 'HEIGHT'),
                              width=file.getint('MAZE', 'WIDTH'),
                              is_perfect=file.getboolean('MAZE', 'PERFECT'),
                              entry=parse_coords(file.get('CORDS', 'ENTRY')),
                              exit=parse_coords(file.get('CORDS', 'EXIT')),
                              output_file=file.get('OUTPUT', 'OUTPUT_FILE'),
                              pattern=Patterns(file.get('EXTRA', 'PATTERN')),
                              seed=file.getint('EXTRA', 'SEED'))

        if config.entry == config.exit:
            raise ValueError("entry and exit can't be on the same place")
        if (config.entry[1] >= config.height or config.entry[1] < 0 or
                config.entry[0] >= config.width or
                config.entry[0] < 0):
            raise ValueError("entry point is outside of maze")
        if (config.exit[1] >= config.height or config.exit[1] < 0 or
                config.exit[0] >= config.width or
                config.exit[0] < 0):
            raise ValueError("exit point is outside of maze")
    except ValidationError as exc:
        er = exc.errors()
        for e in er:
            print(e["msg"])
        exit()
    except ValueError as e:
        print(e)
        exit()
    except configparser.Error as e:
        print(e)
        exit()

    pattern_error: str | None = None
    try:
        maze = gen_maze(config.height,
                        config.width,
                        config.is_perfect,
                        config.pattern.value,
                        config.seed)
        if maze[config.entry[1]][config.entry[0]] == 'f':
            raise ValueError("entry can't be placed on pattern")
        if maze[config.exit[1]][config.exit[0]] == 'f':
            raise ValueError("exit can't be placed on pattern")
    except ValueError as e:
        print(e)
        exit()
    except PatternError as e:
        pattern_error = str(e)

        maze = gen_maze(config.height,
                        config.width,
                        config.is_perfect,
                        None,
                        config.seed)
    try:
        write_maze(config.output_file,
                   maze,
                   config.entry,
                   config.exit)
    except OSError as e:
        print(e)
        exit()
    run_display(
        maze,
        config.width,
        config.height,
        (config.entry[0], config.entry[1]),
        (config.exit[0], config.exit[1]),
        config.is_perfect,
        config.pattern.value,
        pattern_error,
        config.seed,
    )


if __name__ == "__main__":
    main()
