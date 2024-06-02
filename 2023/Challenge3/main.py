import heapq
from terrain import *
from node import Node
from plotter import CSVGraphPlotter
from dotenv import load_dotenv
import os

load_dotenv()
map_data_path = os.getenv("MAP_DATA_PATH")
t = Terrain(map_data_path)
x_coord, y_coord, contour_matrix = t.analyze_terrain()


def is_valid_coord(x, y):
    if (x_coord[0] <= x <= x_coord[-1]) and (y_coord[-1] <= y <= y_coord[0]):
        return True


def is_destination(x, y, dest):
    return x == dest[0] and y == dest[1]


# Calculate the heuristic based on Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5


def contour_to_node_matrix(x_coords, y_coords, contour_matrix):
    node_matrix = []
    for i, x in enumerate(x_coords):
        row = []
        for j, y in enumerate(y_coords):
            z = contour_matrix[j][i]
            node = Node(x, y, z, i, j)
            row.append(node)
        node_matrix.append(row)
    return node_matrix


def normalize_coordinate(x: float, y: float, top_left_origin: tuple, map_area: tuple) -> tuple[int, int]:
    x_shift = -top_left_origin[0]
    y_shift = -top_left_origin[1]

    x_norm = x + x_shift
    y_norm = abs(y + y_shift)  # Flipping Y to the positive region

    if (x_norm < map_area[0]) or (y_norm < map_area[1]):
        return x_norm.__int__(), y_norm.__int__()


# Trace the path from source to destination
def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]
    height = cell_details[row][col].z

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_x == row and cell_details[row][col].parent_y == col):
        path.append((row, col, height))
        temp_row = cell_details[row][col].parent_x
        temp_col = cell_details[row][col].parent_y
        temp_height = cell_details[row][col].parent_z
        row = temp_row
        col = temp_col
        height = temp_height

    # Add the source cell to the path
    path.append((row, col, height))
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    # print("The Path is: ")
    # for i in path:
    #     print("->", i, end=" ")
    # print( )
    return path


start = (1, 1)
end = (90, 50)
# node_area = contour_to_node_matrix(x_coord, y_coord, contour_matrix)
top_left_origin = (x_coord[0], y_coord[0])
map_size = contour_matrix.shape
ROW, COL = map_size[0], map_size[1]


def a_star_search(src, dest):
    if not is_valid_coord(*src) or not is_valid_coord(*dest):
        print("Source or destination is invalid.")
        return

    if is_destination(*src, dest):
        print("Target found!")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Node(contour_matrix[col][row].astype(float)) for col in range(COL)] for row in range(ROW)]
    
    x = src[0]
    y = src[1]
    norm_x, norm_y = normalize_coordinate(x, y, top_left_origin, map_size)
    z = cell_details[norm_x][norm_y].z
    cell_details[x][y].f = 0
    cell_details[x][y].g = 0
    cell_details[x][y].h = 0
    cell_details[x][y].parent_x = x
    cell_details[x][y].parent_y = y
    cell_details[x][y].parent_z = z
    steps = 0

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, x, y, z))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)
        print(f"Raw path: {p}")
        # Mark the cell as visited
        x = p[1]
        y = p[2]
        z = p[3]
        closed_list[x][y] = True

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_x = x + dir[0]
            new_y = y + dir[1]
            norm_x, norm_y = normalize_coordinate(new_x, new_y, top_left_origin, map_size)
            new_z = cell_details[norm_x][norm_y].z

            if is_valid_coord(new_x, new_y) and not closed_list[new_x][new_y]:
                # If the successor is the destinationc
                if is_destination(new_x, new_y, dest):
                    # Set the parent of the destination cell
                    cell_details[new_x][new_y].parent_x = x
                    cell_details[new_x][new_y].parent_y = y
                    cell_details[new_x][new_y].parent_z = z
                    print(f"The destination is found in {steps} moves")
                   
                    # Trace the path from source to destination
                    path = trace_path(cell_details, dest)
                    
                    plotter = CSVGraphPlotter(map_data_path, path)
                    plotter.plot_2D_map()
                    plotter.plot_3D_map()
                    
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    new_g = cell_details[x][y].g + 1.0
                    new_h = calculate_h_value(new_x, new_y, dest)
                    new_f = new_g + new_h

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_x][new_y].f == float('inf') or cell_details[new_x][new_y].f > new_f:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (new_f, new_x, new_y, new_z))
                        # Update the cell details
                        cell_details[new_x][new_y].f = new_f
                        cell_details[new_x][new_y].g = new_g
                        cell_details[new_x][new_y].h = new_h
                        cell_details[new_x][new_y].parent_x = x
                        cell_details[new_x][new_y].parent_y = y
                        cell_details[new_x][new_y].parent_z = z

                norm_start_coord = normalize_coordinate(
                    start[0], start[1], top_left_origin, map_size)
                norm_end_coord = normalize_coordinate(
                    end[0], end[1], top_left_origin, map_size)
                # print(f"Normalized: {norm_coord}")
                #
                # row, col = norm_coord[0], norm_coord[1]
                # a = node_area[row][col].get_index_coords()
                # b = node_area[row][col].get_xyz()

            # else:
            #     raise Exception(f"Error: {new_x, new_y} is invalid! Please ensure the coordinates are within the map area.")

        if not found_dest:
            steps += 1
            # print("Failed to find the destination cell")


def main():
    src = (0, 0)
    dest = (50, 90)

    a_star_search(src, dest)


if __name__ == "__main__":
    main()
