from maze_generator import gen_maze
from maze_solver import solve_maze
from maze_generator import check_pattern

RESET = "\033[0m"

COLORS = {
    "white": "\033[37m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

BACKGROUND_COLORS = {
    "white": "\033[47m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
}


def render_maze(
    maze: list[list[str]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: list[tuple[int, int]],
    pattern_positions: set[tuple[int, int]],
    show_path: bool = False,
    wall_color: str = "white",
    path_color: str = "red",
    pattern_color: str = "cyan",

) -> None:
    color = COLORS[wall_color]
    path_col = COLORS["white"]
    path_background = BACKGROUND_COLORS[path_color]
    pattern_background = BACKGROUND_COLORS[pattern_color]

    path_indexes = {
        position: index
        for index, position in enumerate(path)
    }

    for y, row in enumerate(maze):
        # Print north walls
        for cell in row:
            value = int(cell, 16)
            north = bool(value & 1)

            print(f"{color}+{RESET}", end="")

            if north:
                print(f"{color}---{RESET}", end="")
            else:
                print("   ", end="")

        print(f"{color}+{RESET}")

        # Print west/east walls and contents
        for x, cell in enumerate(row):
            value = int(cell, 16)
            west = bool(value & 8)

            if west:
                print(f"{color}|{RESET}", end="")
            else:
                print(" ", end="")

            position = (x, y)

            if show_path and position in path_indexes:
                index = path_indexes[position]

                if position == entry:
                    content = " S "
                elif position == exit_pos:
                    content = " E "
                else:
                    content = get_path_symbol(path, index)

                print(
                    f"{path_background}{path_col}"
                    f"{content}{RESET}",
                    end="",
                )

            elif position == entry:
                print(" S ", end="")

            elif position == exit_pos:
                print(" E ", end="")

            elif position in pattern_positions:
                print(
                    f"{pattern_background}   {RESET}",
                    end="",
                )

            else:
                print("   ", end="")

        # East wall of last cell
        last_value = int(row[-1], 16)
        east = bool(last_value & 2)

        if east:
            print(f"{color}|{RESET}")
        else:
            print(" ")

    # South walls of final row
    for cell in maze[-1]:
        value = int(cell, 16)
        south = bool(value & 4)

        print(f"{color}+{RESET}", end="")

        if south:
            print(f"{color}---{RESET}", end="")
        else:
            print("   ", end="")

    print(f"{color}+{RESET}")


def get_path_symbol(
    path: list[tuple[int, int]],
    index: int,
) -> str:
    current_x, current_y = path[index]

    directions: set[str] = set()

    if index > 0:
        prev_x, prev_y = path[index - 1]

        if prev_x < current_x:
            directions.add("west")
        elif prev_x > current_x:
            directions.add("east")
        elif prev_y < current_y:
            directions.add("north")
        elif prev_y > current_y:
            directions.add("south")

    if index < len(path) - 1:
        next_x, next_y = path[index + 1]

        if next_x < current_x:
            directions.add("west")
        elif next_x > current_x:
            directions.add("east")
        elif next_y < current_y:
            directions.add("north")
        elif next_y > current_y:
            directions.add("south")

    if directions == {"west", "east"}:
        return "───"

    if directions == {"north", "south"}:
        return " │ "

    if directions == {"west", "south"}:
        return "─┐ "

    if directions == {"east", "south"}:
        return " ┌─"

    if directions == {"west", "north"}:
        return "─┘ "

    if directions == {"east", "north"}:
        return " └─"

    return "   "


def display_error(message: str) -> None:
    print()
    print("=== A-MAZE-ING ===")
    print()
    print(f"Error: {message}")
    print()


def run_display(
    maze: list[list[str]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    is_perfect: bool,
    pattern: str,
    pattern_error: str | None,
    seed: int | None,
) -> None:

    path = solve_maze(maze, entry, exit_pos)
    show_path = False
    wall_color = "white"
    pattern_color = "cyan"
    path_color = "red"
    pattern_positions: set[tuple[int, int]] = set()

    if pattern_error is None:
        positions = check_pattern(maze, pattern)
        pattern_positions = {
            (y, x)
            for x, y in positions
        }

    while True:
        render_maze(
            maze,
            entry,
            exit_pos,
            path,
            pattern_positions,
            show_path=show_path,
            wall_color=wall_color,
            path_color=path_color,
            pattern_color=pattern_color,
        )
        if pattern_error is not None:
            print()
            print(f"{COLORS["red"]}Warning: {pattern_error}{RESET}")

        print()
        print("[R] Regenerate maze")
        print("[P] Show/hide path")
        print("[C] Change wall colour")
        print("[S] Change solution path colour")
        print("[T] Change pattern colour")
        print("[Q] Quit")

        command = input("> ").lower()

        if command == "r":
            print("[N] Generate new maze")
            print("[S] Regenerate using seed")

            regenerate = input("> ").lower()

            if regenerate == "n":
                regenerate_seed = None
            elif regenerate == "s":
                regenerate_seed = seed
            else:
                continue

            if pattern_error is not None:
                maze = gen_maze(
                    height,
                    width,
                    is_perfect,
                    None,
                    regenerate_seed,
                )
            else:
                maze = gen_maze(
                    height,
                    width,
                    is_perfect,
                    pattern,
                    regenerate_seed,
                )

            path = solve_maze(maze, entry, exit_pos)

        elif command == "p":
            show_path = not show_path

        elif command == "c":
            print("Available colours:")
            print(", ".join(COLORS))

            new_color = input("> ").lower()

            if new_color in COLORS:
                wall_color = new_color

        elif command == "s":
            print("Available colours:")
            print(", ".join(BACKGROUND_COLORS))

            new_color = input("> ").lower()

            if new_color in BACKGROUND_COLORS:
                path_color = new_color

        elif command == "t":
            print("Available colours:")
            print(", ".join(BACKGROUND_COLORS))

            new_color = input("> ").lower()

            if new_color in BACKGROUND_COLORS:
                pattern_color = new_color

        elif command == "q":
            break
