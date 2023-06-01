# Path Finder

Uses Pygame to create an interactive visualization for the A* search algorithm

## Description

Path Finder allows users to interactively create a maze, set the start and end points, and visualize the process of finding the shortest path using algorithms like A* and breadth-first search. Users can drag and draw walls, watch as the algorithm explores the maze, and see the shortest path highlighted, Incase no path is found - the application shows "No Solution".

## Usage

1. Run the `main.py` file using Python.
2. Click to set the start and end points on the grid.
3. Drag the mouse to create walls or obstacles.
4. Press Enter to start the pathfinding algorithm.
5. Watch as the algorithm explores the maze and finds the shortest path.
6. Press Enter again to reset the grid and start a new pathfinding process.

## A* Algorithm

The A* (A-star) algorithm is a popular pathfinding algorithm that combines the benefits of Dijkstra's algorithm (uniform cost search) and greedy best-first search. It uses heuristics to estimate the cost from the current node to the goal and makes informed decisions about which nodes to explore.

- A* considers the cost to reach a node from the start (g-score) and the estimated cost to reach the goal from that node (f-score).
- The f-score of a node is the sum of its g-score and h-score.
- A* explores the nodes with the lowest f-score first, prioritizing the most promising paths.
- By using a heuristic function (such as Manhattan distance), A* is able to find the shortest path efficiently.


## Screenshots

![Maze Generated](https://github.com/Shady2kOver/pathfinder-astar/blob/master/screenshots/maze_generated.png?raw=true)

![Maze Generated](https://github.com/Shady2kOver/pathfinder-astar/blob/master/screenshots/path_found.png?raw=true)

## License 
This project is licensed under the **MIT License**.
