from line import Line
from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, mu):
        self.__mu: int = mu

    @property
    def mu(self):
        return self.__mu

    @abstractmethod
    def intersect(self, line: Line) -> float:
        """
        Returns length of scanning line and figure.
        """
        pass


class Ellipse(Figure):
    def __init__(self, x0, y0, a, b, mu):
        super().__init__(mu)
        self.x0 = x0
        self.y0 = y0
        self.a = a
        self.b = b

    def intersect(self, line: Line):
        try:
            k, p = line.get_slope_intercept_coefficients()
        except ZeroDivisionError:
            if line.a == 0:
                return 0
            # vertical line: Ax + 0y + C = 0, q = -C / A
            q = -line.c / line.a
            y1 = self.y0 + (self.b ** 2 - (self.b * (q - self.x0) / self.a) ** 2)
            y2 = self.y0 - (self.b ** 2 - (self.b * (q - self.x0) / self.a) ** 2)
            return abs(y2 - y1)

        discriminant = 4 * (self.a * self.b) ** 2 * ((self.y0 - p) * (2 * k * self.x0 - self.y0 + p) + self.b ** 2 + (self.a ** 2 - self.x0 ** 2) * k ** 2)

        a = self.b ** 2 + (self.a * k) ** 2
        b = 2 * (self.a ** 2 * k * p - self.b ** 2 * self.x0 - self.a ** 2 * k * self.y0)
        if discriminant > 0:
            x1 = (-b + discriminant ** (1 / 2)) / 2 / a
            y1 = k * x1 + p
            x2 = (-b - discriminant ** (1 / 2)) / 2 / a
            y2 = k * x2 + p
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)
        return 0


class Rectangle(Figure):
    def __init__(self, x0, y0, a, b, mu):
        super().__init__(mu)
        self.x0 = x0
        self.y0 = y0
        self.a = a
        self.b = b

    def intersect(self, line: Line) -> float:
        point_a = (self.x0 - self.a / 2, self.y0 - self.b / 2)
        point_b = (self.x0 - self.a / 2, self.y0 + self.b / 2)
        point_c = (self.x0 + self.a / 2, self.y0 + self.b / 2)
        point_d = (self.x0 + self.a / 2, self.y0 - self.b / 2)

        # degenerate line: 0x + 0y + 0 = 0, so it is point
        try:
            deviation_a = line.normalize().get_deviation(point_a[0], point_a[1])
            deviation_b = line.normalize().get_deviation(point_b[0], point_b[1])
            deviation_c = line.normalize().get_deviation(point_c[0], point_c[1])
            deviation_d = line.normalize().get_deviation(point_d[0], point_d[1])
        except ZeroDivisionError:
            return 0

        new_points = []
        if deviation_a * deviation_b < 0:
            proportionality_coefficient = abs(deviation_a / deviation_b)
            x = (point_a[0] + proportionality_coefficient * point_b[0]) / (1 + proportionality_coefficient)
            y = (point_a[1] + proportionality_coefficient * point_b[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        if deviation_b * deviation_c < 0:
            proportionality_coefficient = abs(deviation_b / deviation_c)
            x = (point_b[0] + proportionality_coefficient * point_c[0]) / (1 + proportionality_coefficient)
            y = (point_b[1] + proportionality_coefficient * point_c[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        if deviation_c * deviation_d < 0:
            proportionality_coefficient = abs(deviation_c / deviation_d)
            x = (point_c[0] + proportionality_coefficient * point_d[0]) / (1 + proportionality_coefficient)
            y = (point_c[1] + proportionality_coefficient * point_d[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        if deviation_a * deviation_d < 0:
            proportionality_coefficient = abs(deviation_a / deviation_d)
            x = (point_a[0] + proportionality_coefficient * point_d[0]) / (1 + proportionality_coefficient)
            y = (point_a[1] + proportionality_coefficient * point_d[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        # line doesn't cross the rectangle
        if len(new_points) < 2:
            return 0

        point1 = new_points[0]
        point2 = new_points[1]

        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** (1 / 2)


class Triangle(Figure):
    def __init__(self, points, mu):
        super().__init__(mu)
        self.__points = points

    def intersect(self, line: Line) -> float:
        point_a = self.__points[0]
        point_b = self.__points[1]
        point_c = self.__points[2]

        # degenerate line: 0x + 0y + 0 = 0, so it is point
        try:
            deviation_a = line.normalize().get_deviation(point_a[0], point_a[1])
            deviation_b = line.normalize().get_deviation(point_b[0], point_b[1])
            deviation_c = line.normalize().get_deviation(point_c[0], point_c[1])
        except ZeroDivisionError:
            return 0

        # line goes throw a vertex of triangle
        for point in self.__points:
            if line.contains_point(point[0], point[1]):
                other_points = list(set(self.__points) - {point})
                intersection_point = line.intersect_with_line(Line(other_points[0][0],
                                                                   other_points[0][1],
                                                                   other_points[1][0],
                                                                   other_points[1][1]))
                return ((point[0] + intersection_point[0]) ** 2 + (point[1] + intersection_point[1]) ** 2) ** (1 / 2)

        # the line goes throw two sides of triangle
        new_points = []
        if deviation_a * deviation_b < 0:
            proportionality_coefficient = abs(deviation_a / deviation_b)
            x = (point_a[0] + proportionality_coefficient * point_b[0]) / (1 + proportionality_coefficient)
            y = (point_a[1] + proportionality_coefficient * point_b[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        if deviation_a * deviation_c < 0:
            proportionality_coefficient = abs(deviation_a / deviation_c)
            x = (point_a[0] + proportionality_coefficient * point_c[0]) / (1 + proportionality_coefficient)
            y = (point_a[1] + proportionality_coefficient * point_c[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        if deviation_b * deviation_c < 0:
            proportionality_coefficient = abs(deviation_b / deviation_c)
            x = (point_b[0] + proportionality_coefficient * point_c[0]) / (1 + proportionality_coefficient)
            y = (point_b[1] + proportionality_coefficient * point_c[1]) / (1 + proportionality_coefficient)
            new_points.append((x, y))

        # the line doesn't cross triangle
        if len(new_points) < 2:
            return 0

        point1 = new_points[0]
        point2 = new_points[1]

        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** (1 / 2)


