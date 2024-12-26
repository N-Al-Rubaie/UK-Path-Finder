# UK Path Finder


https://github.com/user-attachments/assets/a5492ee1-a589-470e-b9a8-5c17bace07fa

## Overview
The UK Path Finder is a GUI application that enables users to visualise and find the optimal path between cities in the UK using various pathfinding algorithms.

---

## Features
- **Interactive GUI**: Easily select start and end cities, choose a pathfinding algorithm, and dynamically view the results.
- **Pathfinding Algorithms**:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - Dijkstra's Algorithm
  - A* Search
- **Map Visualisation**: Displays UK cities, their connections, and the computed path on a map.
- **Error Handling**: Prevents invalid input, such as selecting the same city as both the start and end point.

---

## Controls
- **Select Start City Dropdown**: Choose the city to start your path.
- **Select End City Dropdown**: Choose the city to end your path.
- **Select Algorithm Dropdown**: Select a pathfinding algorithm from the available options.
- **Find Path Button**: Calculates and displays the optimal path based on the selected parameters.

---

## Usage
1. Launch the application.
2. Select a start city and an end city using the dropdown menus.
3. Choose a pathfinding algorithm.
4. Click **Find Path** to compute and visualise the path on the map.

---

## File Structure
```
UK-Path-Finder/
├── uk_path_finder.py  # UK Path Finder 
├── assets             # Images and icons
├── README.md          # Documentation
