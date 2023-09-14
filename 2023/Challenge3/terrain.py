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
        self.x_coordinate, self.y_coordinate, self.contour_matrix = self.analyze_terrain()

    def analyze_terrain(self):
        try:
            df = pd.read_csv(self.contour_map, header=None)

            x_coordinate = df.iloc[0, 1:].values
            y_coordinate = df.iloc[1:, 0].values
            contour_matrix = df.iloc[1:, 1:].values
            print(f"Terrain Map Created!")
            return x_coordinate, y_coordinate, contour_matrix
        except Exception as e:
            print(f"Error: {str(e)}")

    def valid_coordinate(self, x, y):
        x_sequence = eval_axis_sequence(self.x_coordinate_offset, x)
        y_sequence = eval_axis_sequence(self.y_coordinate_offset, y)

        if x_sequence < 0:
            x_sequence = None
            # print("X-axis is out of bound!")
        if y_sequence < 0:
            y_sequence = None
            # print("X-axis is out of bound!")

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


class CSVGraphPlotter:
    def __init__(self, file_path):
        self.file_path = file_path

    def plot_graph(self):
        try:
            # Read the CSV file
            df = pd.read_csv(self.file_path)

            # Extract the coordinates (X and Y) and height values
            x_coords = df.columns[1:-1].values  # Exclude the first column (header)
            y_coords = df.iloc[:, 0].values  # Exclude the first row (header)
            height_data = df.iloc[1:, 1:-1].values
            # Create a meshgrid for X and Y coordinates
            X, Y = np.meshgrid(x_coords, y_coords)

            # Create a 3D plot
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Plot the surface
            ax.plot_surface(X, Y, height_data, cmap='viridis')

            # Set axis labels
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Y Coordinate')
            ax.set_zlabel('Elevation')

            # Show the plot
            plt.show()
        except Exception as e:
            print(f"Error plotting graph: {str(e)}")

# if __name__ == "__main__":
#     # Example usage of the CSVGraphPlotter class
#     csv_file_path = "Elevation.csv"
#     graph_plotter = CSVGraphPlotter(csv_file_path)
#
#     # Plot the 3D graph
#     graph_plotter.plot_graph()
