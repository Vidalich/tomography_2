class Line:
    def __init__(self, x1=None, y1=None, x2=None, y2=None, a=None, b=None, c=None):
        if a is None and b is None and c is None:
            self.__a = y1 - y2
            self.__b = x2 - x1
            self.__c = x1 * y2 - x2 * y1
            self.__points = [x1, y1, x2, y2]
        else:
            self.__a = a
            self.__b = b
            self.__c = c

    def __repr__(self):
        return f"{self.__a}X + {self.__b}Y + {self.__c}"

    @property
    def a(self): return self.__a

    @property
    def b(self): return self.__b

    @property
    def c(self): return self.__c

    @property
    def points(self): return self.__points

    def normalize(self):
        """
        Returns the normalized line: Ax + By + C = 0 -> xcos(a) + ysin(a) - s = 0.
        """
        normalize_coefficient = 1 / (self.__a ** 2 + self.__b ** 2) ** (1 / 2)

        self.__a *= normalize_coefficient
        self.__b *= normalize_coefficient
        self.__c = self.__c * normalize_coefficient if self.__c < 0 else self.__c * (-normalize_coefficient)

        return Line(a=self.__a, b=self.__b, c=self.__c)

    def get_slope_intercept_coefficients(self) -> tuple:
        """
        Returns k and b in slope-intercept conception of the line: y = kx + b
        """
        return -self.__a / self.__b, -self.__c / self.__b

    def get_deviation(self, x0: float, y0: float) -> float:
        """
        Returns deviation of point (x0, y0) from the normalized line:
        d = x0cos(a) + y0sin(a) - s
        """
        return x0 * self.__a + y0 * self.__b + self.__c

    def intersect_with_line(self, line) -> tuple:
        """
        Returns intersection point of two lines.
        """
        det = (self.a * line.b - self.b * line.a)
        det_x = (-self.c * line.b + self.b * line.c)
        det_y = (-self.a * line.c + self.c * line.a)

        if det == 0:
            return None
        return det_x / det, det_y / det

    def contains_point(self, x0, y0) -> bool:
        """
        Returns True if point (x0, y0) belongs to line.
        """
        return self.__a * x0 + self.__b * y0 + self.__c == 0







