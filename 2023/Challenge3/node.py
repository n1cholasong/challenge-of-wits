class Node:
    def __init__(self, z):
        self.x = None
        self.y = None
        self.z = z
        self.parent_x = None
        self.parent_y = None
        self.parent_z = None
        self.index_row = None
        self.index_col = None
        self.f = float("inf")  # Total cost of the cell (g + h)
        self.g = float("inf")  # Cost from start to this cell
        self.h = 0  # Heuristics cost from this cell to destination

    def get_xyz(self):
        return self.x, self.y, self.z

    def get_index_coords(self):
        return self.index_row, self.index_col
