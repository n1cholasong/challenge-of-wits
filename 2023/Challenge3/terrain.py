import pandas as pd
import numpy as np
import math
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def eval_axis_sequence(offset, axis):
    if -offset <= 0:
        return abs(offset) + axis
    else:
        return abs(offset) - axis


def euclidean_distance(point_a, point_b):
    if len(point_a) != len(point_b):
        raise ValueError("Both points must have the same number of dimensions!")

    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point_a, point_b)))


class Terrain:
    def __init__(self, contour_map):
        self.contour_map = contour_map
        self.x_coordinate_offset = 80
        self.y_coordinate_offset = -130
        # self.x_coordinate, self.y_coordinate, self.contour_matrix = self.analyze_terrain()

    def analyze_terrain(self):
        try:
            df = pd.read_csv(self.contour_map, index_col=0)
            # print(df)
            x_coordinate = df.columns.values.astype(float)
            y_coordinate = df.index.values.astype(float)
            contour_matrix = df.values.astype(float)
            print(f"Terrain Map Created!")
            return x_coordinate, y_coordinate, contour_matrix
        except Exception as e:
            print(f"Error: {str(e)}")

    def valid_coordinate(self, x, y):
        x_sequence = eval_axis_sequence(self.x_coordinate_offset, x)
        y_sequence = eval_axis_sequence(self.y_coordinate_offset, y)

        if x_sequence < 0:
            x_sequence = None
            print("X-axis is out of bound!")
        if y_sequence < 0:
            y_sequence = None
            print("X-axis is out of bound!")

        return x_sequence, y_sequence

    def elevation(self, x, y):
        coord = self.valid_coordinate(x, y)
        if all(points is not None for points in coord):
            return self.contour_matrix[coord[1], coord[0]]
        else:
            return "Coordinate does not exists!"

    def adjacent_nodes(self, x, y):
        return [(a, b) for a, b in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)) if
                (a, b) != (x, y) and all(points is not None for points in self.valid_coordinate(a, b))]

    def energy_cost(self, point_a, point_b):
        energy = euclidean_distance(point_a, point_b)
        current_elevation = self.elevation(point_a[0], point_a[1])
        next_elevation = self.elevation(point_b[0], point_b[1])

        if current_elevation < next_elevation:
            energy *= 10

        return energy


class CoordinateSystemConverter:
    def __init__(self, x_offset: float, y_offset: float):
        self.x_offset = x_offset
        self.y_offset = y_offset

    def data_to_matrix(self, x: float, y: float) -> tuple[float, float]:
        """Convert data coordinates to matrix coordinates."""
        matrix_x = abs(self.x_offset) + x if self.x_offset < 0 else x - abs(self.x_offset)
        matrix_y = abs(self.y_offset) + y if self.y_offset < 0 else y - abs(self.y_offset)
        return matrix_x.__abs__(), matrix_y.__abs__()

    def matrix_to_data(self, matrix_x: float, matrix_y: float) -> tuple[float, float]:
        """Convert matrix coordinates to data coordinates."""
        x = matrix_x - abs(self.x_offset) if self.x_offset < 0 else matrix_x + abs(self.x_offset)
        y = matrix_y - abs(self.y_offset) if self.y_offset < 0 else matrix_y + abs(self.y_offset)
        return x, y


class Node:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.parent_x = None
        self.parent_y = None
        self.index_row = None
        self.index_col = None
        self.f = float("inf")  # Total cost of the cell (g + h)
        self.g = float("inf")  # Cost from start to this cell
        self.h = 0  # Heuristics cost from this cell to destination

    def get_xyz(self):
        return self.x, self.y, self.z

    def get_index_coords(self):
        return self.index_row, self.index_col


class CSVGraphPlotter:
    def __init__(self, file_path):
        self.file_path = file_path

    def plot_graph(self):
        try:

            df = pd.read_csv(self.file_path, index_col=0)
            # Extract the coordinates (X and Y) and height values
            x_coords = df.columns.values.astype(float)  # Exclude the first column (header)
            y_coords = df.index.values.astype(float)  # Exclude the first row (header)
            height_data = df.values.astype(float)
            # Create a meshgrid for X and Y coordinates
            X, Y = np.meshgrid(x_coords, y_coords)

            # Create a 3D plot
            fig = plt.figure(figsize=(12, 10))
            graph = fig.add_subplot(111, projection='3d')

            # Plot the surface
            graph.plot_surface(X, Y, height_data, cmap='viridis')

            # Set axis labels
            graph.set_xlabel('X Coordinate')
            graph.set_ylabel('Y Coordinate')
            graph.set_zlabel('Elevation')

            # Show the plot
            plt.show()

            # 2D Contour Map
            # cp = plt.contour(X, Y, height_data, cmap='viridis')
            # plt.colorbar(cp)
            # plt.xlabel('X Coordinates')
            # plt.ylabel('Y Coordinates')
            # plt.title('Contour Map')
            # plt.show()

        except Exception as e:
            print(f"Error plotting graph: {str(e)}")


if __name__ == "__main__":
    # Example usage of the CSVGraphPlotter class
    csv_file_path = "Elevation.csv"
    graph_plotter = CSVGraphPlotter(csv_file_path)

    # Plot the 3D graph
    graph_plotter.plot_graph()
