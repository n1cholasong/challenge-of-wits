import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CSVGraphPlotter:
    def __init__(self, file_path, coordinates):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path, index_col=0)
        self.x_coords = self.df.columns.values.astype(float)
        self.y_coords = self.df.index.values.astype(float)
        self.z_coords = self.df.values.astype(float)
        self.path_x, self.path_y, self.path_z = zip(*coordinates)
        self.src_coord = self.path_x[0], self.path_y[0], self.path_z[0]
        self.dest_coord = self.path_x[-1], self.path_y[-1], self.path_z[-1]

    def plot_graph(self):
        try:
            df = pd.read_csv(self.file_path, index_col=0)

            x_coords = df.columns.values.astype(float)
            y_coords = df.index.values.astype(float)
            height_data = df.values.astype(float)

            X, Y = np.meshgrid(x_coords, y_coords)

            # Create a 3D plot
            plt.figure(figsize=(12, 10))
            # graph = fig.add_subplot(111, projection='3d')

            # # Plot the surface
            # graph.plot_surface(X, Y, height_data, cmap='viridis')

            # # Set axis labels
            # graph.set_xlabel('X Coordinate')
            # graph.set_ylabel('Y Coordinate')
            # graph.set_zlabel('Elevation')

            # # Show the plot
            # plt.show()

            # 2D Contour Map
            cp = plt.contour(X, Y, height_data, cmap='viridis')
            plt.colorbar(cp)

            plt.scatter(self.x_coords, self.y_coords, color='red', label='Path')
            plt.legend()

            # Labels
            plt.xlabel('X Coordinates')
            plt.ylabel('Y Coordinates')
            plt.title('Contour Map')
            plt.show()

        except Exception as e:
            print(f"Error plotting graph: {str(e)}")

    def plot_2D_map(self):
        plt.figure(figsize=(10, 8))

        x, y = np.meshgrid(self.x_coords, self.y_coords)
        contour = plt.contour(x, y, self.z_coords, cmap='viridis', antialiased=True)
        plt.colorbar(contour)

        plt.plot(self.path_x, self.path_y, color='red',
                 linestyle='-', linewidth=2, label='Path')
        # plt.scatter(path_x, path_y, color='red')

        start_label = f"Start {self.path_x[0], self.path_y[0]}"
        end_label = f"End {self.path_x[-1], self.path_y[-1]}"
        plt.text(self.path_x[0], self.path_y[0], start_label, fontsize=12,
                 ha='right', color='black', fontweight='bold')
        plt.text(self.path_x[-1], self.path_y[-1], end_label, fontsize=12,
                 ha='left', color='black', fontweight='bold')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('2D Contour Map')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_3D_map(self):
        fig = plt.figure(figsize=(10, 8))

        ax = fig.add_subplot(projection='3d')
        
        
        # X, Y, Z = axes3d.get_test_data(0.2)
        
        X, Y = np.meshgrid(self.x_coords, self.y_coords)
        Z = self.z_coords
        
        ax.plot_wireframe(X, Y, Z, zorder=1, alpha=0.7, antialiased=True, linewidth=1)
        ax.plot(self.path_x, self.path_y, self.path_z, color='red', linestyle='-', linewidth=2, label='Path', zorder=3)
        
        start_label = f"Start {self.src_coord}"
        end_label = f"End {self.dest_coord}"
        ax.text(*self.src_coord, start_label, fontsize=12,
                 ha='right', color='black', fontweight='bold')
        ax.text(*self.dest_coord, end_label, fontsize=12,
                 ha='left', color='black', fontweight='bold')
        
        ax.set_zlabel('Z Coordinate')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('3D Contour Map')
        ax.legend()
        plt.tight_layout()
        plt.show()
