from math import pi, cos, sin, sqrt, tan
from line import Line


class Scanner:
    def __init__(self, radius, distance, angles):
        self.__radius = radius
        self.__distance = distance
        self.__sensors = 2 * self.__radius / self.__distance + 1
        self.__angles = angles
        self.__lines = []

        max_index = int((self.__sensors - 1) / 2)
        for m in range(self.__angles):
            phi = pi * m / self.__angles
            lines_in_angle = []
            for k in range(-max_index, max_index + 1):
                discriminant = 4 * cos(phi) ** 2 * (self.__radius ** 2 - (k * self.__distance) ** 2)

                x1 = (2 * k * self.__distance * sin(phi) + sqrt(discriminant)) / 2
                y1 = x1 * tan(phi) - k * self.__distance / cos(phi)
                x2 = (2 * k * self.__distance * sin(phi) - sqrt(discriminant)) / 2
                y2 = x2 * tan(phi) - k * self.__distance / cos(phi)

                lines_in_angle.append(Line(x1, y1, x2, y2))
            self.__lines.append(lines_in_angle)

    @property
    def radius_of_scanning(self):
        return self.__radius

    @property
    def distance(self):
        return self.__distance

    @property
    def amount_of_sensors(self):
        return self.__sensors

    @property
    def amount_of_angles(self):
        return self.__angles

    @property
    def lines(self):
        return self.__lines

    def scan(self, figures: list) -> list:
        """
        Returns two-dimensional list with intesivities for each line in each angle.
        """
        intensivities = []
        for lines_in_angle in self.__lines:
            lines_intensivity_in_angle = []
            for line in lines_in_angle:
                intensive = 0
                for figure in figures:
                    intersection = figure.intersect(line)
                    intensive += figure.mu * intersection
                lines_intensivity_in_angle.append(intensive)
            intensivities.append(lines_intensivity_in_angle)
        return intensivities




