*This project was created as part of the 42 curriculum by marde-bo and tkroon.*
# A-Maze-ing

## Description

This project was created as part of the 42 curriculum. The goal was to build a maze generator, a maze solver, and a visualizer to display the generation and solving process.

The project consists of:

#### Visualizer

A script that visualizes the maze and the different stages of the project. The colors of the various visual elements can be customized.

#### Maze Generator

A script that generates either a perfect or non-perfect maze that can be read by the visualizer.

#### Maze Solver

A script that solves the generated maze and finds the shortest path from the entry point to the exit.

#### Package

A reusable Python package that can be installed and used to generate and solve mazes in other projects.

## Config File

```ini
#----------------------------------------

#░█▀█░░░░░█▄█░█▀█░▀▀█░█▀▀░░░░░▀█▀░█▀█░█▀▀
#░█▀█░▄▄▄░█░█░█▀█░▄▀░░█▀▀░▄▄▄░░█░░█░█░█░█
#░▀░▀░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░░░▀▀▀░▀░▀░▀▀▀

#----------------------------------------

[MAZE]

HEIGHT = 23

WIDTH = 15

PERFECT = False

#----------------------------------------

[COORDS]

ENTRY = 0,0

EXIT = 19,14

#----------------------------------------

[OUTPUT]

OUTPUT_FILE = maze.txt

#----------------------------------------

[EXTRA]

PATTERN = 42

SEED = 0

#----------------------------------------
```

The config file allows you to customize the maze generation.

In the `[MAZE]` section, you can set the size of the maze using `HEIGHT` and `WIDTH`. You can also set `PERFECT` to `True` or `False` to determine whether the generated maze should be perfect.

In the `[COORDS]` section, you can set the entry and exit points of the maze. The coordinates are specified as `height,width`, separated by a comma.

The `[OUTPUT]` section allows you to specify the name of the output file. The generated maze is stored in hexadecimal format, along with its solution using the directions `N`, `E`, `S`, and `W`.

> **Example output:**
> *[Add example here]*

In the `[EXTRA]` section, you can choose between different maze patterns.

Currently available patterns are:

* `42`
* `star`
* `circle`
* `smiley`

You can also set the seed used for maze generation.

* `SEED = 0` generates a different random maze each time.
* Setting `SEED` to a specific number generates the same maze each time, making the result reproducible.

## The Maze Generation Algorithm

For this project, we used a **Depth-First Search (DFS)** algorithm to generate the maze.

First, we create a grid of the specified size containing only walls. The algorithm then selects a starting point and begins breaking down walls in random directions.

When the algorithm reaches a dead end, it backtracks through previously visited cells until it finds another cell where it can continue breaking walls.

This process continues until all reachable cells in the maze have been visited.

If a non-perfect maze is requested, the algorithm can also remove additional walls when it reaches a dead end. This creates loops and multiple possible paths through the maze.

## The Maze Solver Algorithm

For solving the maze, we used a Breadth-First Search (BFS) algorithm.

The solver starts at the maze entry and explores all reachable neighboring cells level by level. BFS uses a queue, meaning that cells are processed in the same order in which they are discovered.

For each cell, the solver checks which neighboring cells can be reached by inspecting the hexadecimal value stored in the maze. Each bit represents one of the four walls:

1 — North wall
2 — East wall
4 — South wall
8 — West wall

If a wall is not present and the neighboring position is still inside the maze, that cell can be visited.

For example:

if y > 0 and not value & 1:
    neighbors.append((x, y - 1))

This checks whether the current cell has no north wall. If the north side is open, the cell above it is added as a possible neighbor.

While searching, the solver stores each visited position in a came_from dictionary. For every discovered cell, this dictionary records the cell from which it was reached:

came_from[neighbor] = current

This serves two purposes:

it prevents the solver from visiting the same cell multiple times;
it allows the final path to be reconstructed.

The search continues until the exit is reached or there are no more cells left to explore.

Because BFS explores all cells at distance 1 before cells at distance 2, then distance 3, and so on, the first time the exit is reached it is guaranteed to have been reached using the shortest possible path in terms of the number of maze cells travelled.

Once the exit has been found, the solver reconstructs the path by starting at the exit and repeatedly following the stored previous positions:

exit -> previous cell -> previous cell -> ... -> entry

This initially creates the path in reverse order, so the list is reversed before being returned:

path.reverse()

The final result is therefore a list of coordinates representing the shortest path from the entry to the exit:

[
    (entry_x, entry_y),
    ...,
    (exit_x, exit_y),
]

If no route to the exit exists, the solver returns an empty list.

## Reusable Code

The maze generator and maze solver were designed to be reusable.

The package contains both the maze generator and maze solver, which can be imported into other Python projects:

```python
import maze_generator
import maze_solver
```

The maze generator provides functions for generating a maze as a `list[list[str]]`.

The maze solver takes a `list[list[str]]` representing the maze and a `tuple[int, int]` representing the starting position. It returns the solution as a `list[tuple[int, int]]`.

The maze generator requires:

* `width`
* `height`
* `isperfect` (`bool`)
* `pattern` (`str`)

The maze solver requires:

* the maze as a `list[list[str]]`
* a position as a `tuple[int, int]`

## Your Team and Project Management With

### The Roles of Each Team Member

**marde-bo:**

* Display / visualizer
* Makefile
* Maze solver
* Integration of the different components

**tkroon:**

* Maze generator
* Config file integration
* Package conversion

### Your Anticipated Planning and How It Evolved Until the End

We expected to finish the project around the planned deadline, and the overall planning went smoothly.

The work was divided between the team members, with each member focusing on their assigned components. Integration was then done to combine everything into a single project.

### What Worked Well and What Could Be Improved

Overall, we managed to complete everything on time and did not encounter any major problems.


### Have You Used Any Specific Tools? Which Ones?

We mainly used **Slack** for communication and **GitHub** for version control and collaboration.

## Instructions


## Resources

* [GeeksforGeeks](https://www.geeksforgeeks.org/) — Used for general programming and algorithm references.
* [W3Schools](https://www.w3schools.com/) — Used for Python and programming references.
* [Maze Generation Explained](https://youtu.be/ioUl1M77hww?is=U9pBIeBEgvW5Ec7k) — Used as a reference for maze generation algorithms.

## AI Usage

We mainly used AI as a tool for debugging, identifying errors, and helping us understand and solve problems encountered during development.

