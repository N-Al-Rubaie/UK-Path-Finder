import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from PIL import Image


# Define the map of the UK
uk_map = {
    'Manchester': {'Liverpool': 40, 'Carlisle': 120, 'York': 70, 'Newcastle': 140},
    'Liverpool': {'Manchester': 40, 'Holyhead': 90},
    'York': {'Manchester': 70, 'Newcastle': 80, 'Carlisle': 100},
    'Carlisle': {'Manchester': 120, 'Glasgow': 100, 'York': 100, 'Edinburgh': 120},
    'Newcastle': {'York': 80, 'Edinburgh': 110, 'Carlisle': 90},
    'Glasgow': {'Carlisle': 100, 'Edinburgh': 50, 'Oban': 100, 'Aberdeen': 140, 'Inverness': 170, 'Newcastle': 120},  # Glasgow is connected to Carlisle, Edinburgh, Oban, Aberdeen, Inverness, and Newcastle
    'Edinburgh': {'Glasgow': 50, 'Newcastle': 110, 'Manchester': 220, 'Aberdeen': 140},
    'Oban': {'Glasgow': 100, 'Inverness': 110},
    'Aberdeen': {'Inverness': 110, 'Glasgow': 140, 'Edinburgh': 140},
    'Inverness': {'Oban': 110, 'Aberdeen': 110, 'Glasgow': 170},
    'Holyhead': {'Liverpool': 90}
}


# Define the haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Define cities and coordinates
cities = ['Manchester', 'Holyhead', 'Liverpool', 'York', 'Carlisle', 'Newcastle', 'Glasgow', 'Edinburgh', 'Oban', 'Aberdeen', 'Inverness']
city_coordinates = {
    'Manchester': (53.4808, -2.2426),
    'Holyhead': (53.3086, -4.6318),
    'Liverpool': (53.4084, -2.9916),
    'York': (53.9590, -1.0819),
    'Carlisle': (54.8924, -2.9326),
    'Newcastle': (54.9783, -1.6178),
    'Glasgow': (55.8642, -4.2518),
    'Edinburgh': (55.9533, -3.1883),
    'Oban': (56.4151, -5.4714),
    'Aberdeen': (57.1497, -2.0943),
    'Inverness': (57.4778, -4.2247)
}

# Search algorithms
def depth_first_search(graph, start, end, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(start)
    path = path + [start]
    if start == end:
        return path
    for neighbor in graph[start]:
        if neighbor not in visited:
            new_path = depth_first_search(graph, neighbor, end, visited, path)
            if new_path:
                return new_path
    return None

def breadth_first_search(graph, start, end):
    queue = [(start, [start])]
    while queue:
        node, path = queue.pop(0)
        for neighbor in graph[node]:
            if neighbor not in path:
                if neighbor == end:
                    return path + [neighbor]
                else:
                    queue.append((neighbor, path + [neighbor]))
    return None

def dijkstra(graph, start, end):
    unvisited = set(graph.keys())
    distances = {node: float('inf') for node in unvisited}
    distances[start] = 0
    previous_node = {}
    while unvisited:
        current = min(unvisited, key=distances.get)
        if distances[current] == float('inf'):
            break
        unvisited.remove(current)
        for neighbor, distance in graph[current].items():
            if neighbor in unvisited:
                new_distance = distances[current] + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_node[neighbor] = current
    if end not in previous_node:
        return None
    path = [end]
    while path[-1] != start:
        path.append(previous_node[path[-1]])
    path.reverse()
    return path

def astar_search(graph, heuristic, start, end):
    queue = [(0, start, [start])]
    visited = set()
    while queue:
        _, node, path = heapq.heappop(queue)
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor, cost in graph[node].items():
                if neighbor not in visited:
                    total_cost = cost + heuristic[neighbor]
                    heapq.heappush(queue, (total_cost, neighbor, path + [neighbor]))
    return None

# GUI Functions
def find_path():
    start_city = start_combobox.get()
    end_city = end_combobox.get()
    algorithm = algorithm_combobox.get()

    if start_city == end_city:
        messagebox.showinfo("Error", "Start and End cities cannot be the same.")
        return

    heuristic = {city: haversine(city_coordinates[city][0], city_coordinates[city][1], city_coordinates[end_city][0], city_coordinates[end_city][1]) for city in cities}

    if algorithm == "Depth-First Search":
        path = depth_first_search(uk_map, start_city, end_city)
    elif algorithm == "Breadth-First Search":
        path = breadth_first_search(uk_map, start_city, end_city)
    elif algorithm == "Dijkstra's Algorithm":
        path = dijkstra(uk_map, start_city, end_city)
    elif algorithm == "A* Search":
        path = astar_search(uk_map, heuristic, start_city, end_city)
    else:
        path = None

    if not path:
        messagebox.showinfo("No Path Found", "No path could be found between the selected cities.")
        return

    result_text.set(f"{algorithm} Path: {' -> '.join(path)}")
    display_map(path)

def display_map(path):
    fig, ax = plt.subplots(figsize=(4.4, 4.4))  # Reduced figure size
    ax.set_title("UK Map")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Load and display the UK map image
    uk_map_image = Image.open("assets/uk_map.jpg")
    ax.imshow(uk_map_image, extent=[-10, 2, 49, 61], aspect='auto')  # Adjust extent based on the map

    # List to store the positions of labels to avoid overlap
    label_positions = {}

    # Plot cities on the map
    for city, coords in city_coordinates.items():
        color = "red" if city in path else "blue"
        ax.scatter(coords[1], coords[0], label=city, s=50, color=color)

        # Set offsets for specific cities to avoid overlap
        offset_x, offset_y = 0, 0.25
        if city == 'Liverpool':  # Move Liverpool text below the dot
            offset_x, offset_y = 0, -0.5
        elif city == 'Manchester':  # Move Manchester text
            offset_x, offset_y = -0.1, 0.3
        elif city == 'Newcastle' or city == 'Edinburgh':  # Move Newcastle and Edinburgh text slightly to the right
            offset_x, offset_y = 0.75, 0.25

        # Avoid overlap by checking existing label positions
        while (coords[1] + offset_x, coords[0] + offset_y) in label_positions:
            offset_x += 0.2  # Adjust offset incrementally
            offset_y += 0.2  # Adjust offset incrementally

        # Add label to the dictionary to track its position
        label_positions[(coords[1] + offset_x, coords[0] + offset_y)] = city

        # Annotate city with adjusted position
        ax.text(coords[1] + offset_x, coords[0] + offset_y, city, fontsize=8, ha="center", color="black")

    # Plot the path
    for i in range(len(path) - 1):
        start_coords = city_coordinates[path[i]]
        end_coords = city_coordinates[path[i + 1]]
        ax.plot([start_coords[1], end_coords[1]], [start_coords[0], end_coords[0]], color="green", linewidth=2)

    # Clear existing widgets in the map frame
    for widget in map_frame.winfo_children():
        widget.destroy()

    # Add the Matplotlib figure to the map frame
    canvas = FigureCanvasTkAgg(fig, master=map_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)




# GUI Setup
root = tk.Tk()
root.title("UK Path Finder")
root.iconbitmap("assets/map_icon.ico")


# Widgets
tk.Label(root, text="Select Start City: ").grid(row=0, column=0, padx=10, pady=5)
start_combobox = ttk.Combobox(root, values=cities, state="readonly")
start_combobox.grid(row=0, column=1, padx=10, pady=5)
start_combobox.current(0)

tk.Label(root, text="Select End City:").grid(row=1, column=0, padx=10, pady=5)
end_combobox = ttk.Combobox(root, values=cities, state="readonly")
end_combobox.grid(row=1, column=1, padx=10, pady=5)
end_combobox.current(1)

tk.Label(root, text="Select Algorithm:   ").grid(row=2, column=0, padx=10, pady=5)
algorithm_combobox = ttk.Combobox(root, values=["Depth-First Search", "Breadth-First Search", "Dijkstra's Algorithm", "A* Search"], state="readonly")
algorithm_combobox.grid(row=2, column=1, padx=10, pady=5)
algorithm_combobox.current(0)

tk.Button(root, text="Find Path", command=find_path).grid(row=3, column=0, columnspan=2, pady=10)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, wraplength=300).grid(row=4, column=0, columnspan=2, pady=5)

map_frame = tk.Frame(root)
map_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the app
root.mainloop()
