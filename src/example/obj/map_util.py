# support coordinates
class Coord:
    def __init__(self, x_cor, y_cor):
        self.x_cor = x_cor
        self.y_cor = y_cor

    def x(self):
        return self.x_cor

    def y(self):
        return self.y_cor

    def set_x(self, x_cor):
        self.x_cor = x_cor

    def set_y(self, y_cor):
        self.y_cor = y_cor

    def __repr__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + ")"

    def __str__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + ")"
