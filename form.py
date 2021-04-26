import tkinter as tk
import matplotlib.pyplot as plt

from scanner import Scanner
from figures import *
from functools import reduce


class Form:
    def __init__(self, width, height):
        self.objects = []
        self.scanning_lines = []
        self.radius_of_scannig = 295

        # initialization:
        self.window = tk.Tk()
        self.window.geometry(f"{width}x{height}")

        self.canvas = tk.Canvas(width=width, height=height)
        self.canvas.create_oval(5, 5, 590, 590, width=5)
        self.canvas.pack()

        # checkbuttons
        base_x, base_y = 770, 360

        # ellipse
        self.is_ellipse = tk.IntVar()
        self.ellipse_checkbutton = tk.Checkbutton(text="Ellipse",
                                                  variable=self.is_ellipse,
                                                  font=("helvetica", 15),
                                                  onvalue=1, offvalue=0)
        self.ellipse_checkbutton.place(x=base_x, y=base_y + 30)

        # rectangle
        self.is_rectangle = tk.IntVar()
        self.rectangle_checkbutton = tk.Checkbutton(text="Rectangle",
                                                    variable=self.is_rectangle,
                                                    font=("helvetica", 15),
                                                    onvalue=1, offvalue=0)
        self.rectangle_checkbutton.place(x=base_x, y=base_y + 75)

        # triangle
        self.is_triangle = tk.IntVar()
        self.triangle_checkbutton = tk.Checkbutton(text="Triangle",
                                                   variable=self.is_triangle,
                                                   font=("helvetica", 15),
                                                   onvalue=1, offvalue=0)
        self.triangle_checkbutton.place(x=base_x, y=base_y + 120)

        # Entry:
        self.object_parameters_entry = tk.Entry(font=("helvetica", 15))
        self.object_parameters_entry.place(x=base_x, y=base_y + 200)

        self.set_angle = tk.Entry(font=("helvetica", 10),
                                  width=8)
        self.set_angle.place(x=base_x + 70, y=130)

        self.scanner_parameters_entry = tk.Entry(font=("helvetica", 15))
        self.scanner_parameters_entry.place(x=base_x, y=base_y - 15)

        # mouse events:
        self.window.bind('<Motion>', self.mouse_move)
        self.window.bind('<Button-1>', self.mouse_left_click)
        self.window.bind('<Button-3>', self.mouse_right_click)

        # buttons:
        self.clear_button = tk.Button(text="Clear",
                                      command=self.clear_screen,
                                      font=("helvetica", 15),
                                      width=5)
        self.clear_button.place(x=base_x + 70, y=10)

        self.scan_button = tk.Button(text='Scan',
                                     command=self.scan,
                                     font=("helvetica", 15),
                                     width=5)
        self.scan_button.place(x=base_x + 70, y=50)

        self.draw_lines_button = tk.Button(text="Draw lines",
                                           command=self.draw_lines,
                                           font=("helvetica", 14),
                                           width=8)
        self.draw_lines_button.place(x=base_x + 50, y=180)

        # labels
        self.set_angle_label = tk.Label(text="Set angle",
                                        font=("helvetica", 14))
        self.set_angle_label.place(x=base_x + 70, y=100)

        self.object_parameters_label = tk.Label(text="Object parameters",
                                                font=("helvetica", 14))
        self.object_parameters_label.place(x=base_x, y=base_y + 170)

        self.scanner_parameters_label = tk.Label(text="Scanner parameters\n(distance, angles)",
                                                 font=("helvetica", 14))
        self.scanner_parameters_label.place(x=base_x, y=base_y - 70)

        self.window.mainloop()

    def mouse_left_click(self, event):
        figure_variables = [self.is_ellipse,
                            self.is_rectangle, self.is_triangle]
        point_condition = (event.x - 300) ** 2 + (event.y - 300) ** 2 < 295 ** 2

        if sum([variable.get() for variable in figure_variables]) == 1 and point_condition:
            parameters = self.object_parameters_entry.get().split(' ')
            parameters = list(map(int, parameters))

            # ellipse
            if self.is_ellipse.get():
                a, b, mu = parameters[0], parameters[1], parameters[2]
                self.objects.append(Ellipse(event.x, event.y, a, b, mu))
                self.canvas.create_oval(event.x - a, event.y - b,
                                        event.x + a, event.y + b,
                                        fill="#%02x%02x%02x" % (255 - mu, 255 - mu, 255 - mu))

            # rectangle
            elif self.is_rectangle.get():
                a, b, mu = parameters[0], parameters[1], parameters[2]
                self.objects.append(Rectangle(event.x, event.y, a, b, mu))
                self.canvas.create_rectangle(event.x - a / 2, event.y - b / 2,
                                             event.x + a / 2, event.y + b / 2,
                                             fill="#%02x%02x%02x" % (255 - mu, 255 - mu, 255 - mu))

            # triangle
            elif self.is_triangle.get():
                mu = parameters[0]
                self.objects.append(Triangle(Form.triangle_points, mu))
                self.canvas.create_polygon(reduce(lambda t1, t2: t1 + t2, Form.triangle_points),
                                           fill="#%02x%02x%02x" % (255 - mu, 255 - mu, 255 - mu),)
                Form.triangle_points = []

    triangle_points = []

    def mouse_right_click(self, event):
        if self.is_triangle.get() and (event.x - 300) ** 2 + (event.y - 300) ** 2 < 295 ** 2:
            Form.triangle_points.append((event.x, event.y))

    def mouse_move(self, event):
        self.window.title(f"{event.x};{event.y}")

    def clear_screen(self):
        self.canvas.delete('all')
        self.canvas.create_oval(5, 5, 590, 590, width=5)
        self.objects = []

    def scan(self):
        scanner_parameters = self.scanner_parameters_entry.get().split(' ')
        scanner_parameters = list(map(int, scanner_parameters))

        distance, angles = scanner_parameters[0], scanner_parameters[1]

        scanner = Scanner(radius=self.radius_of_scannig, distance=distance, angles=angles)

        self.scanning_lines = scanner.lines
        intensivities = scanner.scan(self.objects)

        angle = int(self.set_angle.get())
        max_index = int((scanner.amount_of_sensors - 1) / 2)

        arguments = list(range(-max_index, max_index + 1))
        values = intensivities[angle]

        plt.plot(arguments, values)
        plt.show()

    def draw_lines(self):
        lines = self.scanning_lines
        for line in [val for sublist in lines for val in sublist]:
            points = line.points
            self.canvas.create_line([point + 300 for point in points])


form = Form(1000, 600)


