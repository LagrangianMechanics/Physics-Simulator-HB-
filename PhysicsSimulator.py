import tkinter as tk

Obj = (1, )

Info = ((0.5,), )

X = (
    (0, 5, 8, 4),
)

Y = (
    (0, 5, 0, -8),
)

Time = (
    (0, 4, 5, 8),
)

n = 100
delta = 2 / n

f = 2 / n

X = [[]]
Y = [[]]
Time = [[]]
for p in range(n + 1):
    x = -1 + delta * p
    X[0].append(x)
    Y[0].append((1 - x ** 2) ** 0.5)
    Time[0].append(f * p)

class Application:
    def __init__(self, master = None):
        self.master = tk.Tk() if master == None else master

        self.canvas = tk.Canvas(self.master, highlightthickness = 0)
        self.canvas.pack(fill = "both", expand = True)

        self.canvas.create_text(0, 0, text = "Press 'q' to start animation\nPress 'a' to reset", tag = "prompt", font = (None, 35))

        self.W = 0
        self.H = 0

        self.Sx = 150
        self.Sy = 150

        self.FPS = 30
        self.frame = 0

        self.canvas.create_line(0, 0, 0, 0, fill = "blue", tag = "L")

        for i in range(len(Obj)):
            self._draw_body_on_canvas(i)

        self.canvas.create_line(0, 0, 0, 0, fill = "black", tag = "x")
        self.canvas.create_line(0, 0, 0, 0, fill = "black", tag = "y")

        self.x = 0
        self.y = 0
        self.canvas.create_text(0, 0, text = f"({self.x}, {self.y})", fill = "white", tag = "point")

        self.canvas.bind("<Configure>", self.RedrawCoordinateAxes)
        self.master.bind("<Key>", self.OnKeyPress)

        self.canvas.tag_raise("prompt")
        self.canvas.bind("<MouseWheel>", self.OnMouseWheel)
    def play(self):
        self.frame += 1
        for i in range(len(Obj)):
            self._set_body(i)
        self.master.after(int(1 / self.FPS * 1000), self.play)
    def RedrawCoordinateAxes(self, event = None):
        global X, Y

        if event == None:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
        else:
            width = event.width
            height = event.height

        self.canvas.coords("prompt", width / 2, 0.08 * height)

        self.W = width / 2
        self.H = height / 2

        p = []
        for i, x in enumerate(X[0]):
            y = Y[0][i]
            X1, Y1 = self.xy_to_XY(x, y)
            p.append(X1)
            p.append(Y1)
        self.canvas.coords("L", *p)


        self.canvas.coords("x", self.W, 0, self.W, height)
        self.canvas.coords("y", 0, self.H, width, self.H)

        X1, Y1 = self.xy_to_XY(self.x, self.y)
        self.canvas.coords("point", X1, Y1)

        for i in range(len(Obj)):
            self._set_body(i)
    def xy_to_XY(self, x, y):
        return (self.Sx * x + self.W, self.H - self.Sy * y)
    def OnKeyPress(self, event):
        key = event.keysym

        if key == "Up":
            self.MovePoint(0, 1)
        elif key == "Left":
            self.MovePoint(-1, 0)
        elif key == "Right":
            self.MovePoint(1, 0)
        elif key == "Down":
            self.MovePoint(0, -1)
        elif key == "space":
            self.frame += 1
            print(self.frame, 1 / self.FPS * self.frame)
            for i in range(len(Obj)):
                self._set_body(i)
        elif key == "a":
            self.frame = 0
            self._set_body(0)
        elif key == "q":
            self.play()
        elif key == "e":
            print(self.compute_position(0))
    def MovePoint(self, dx, dy):
        self.x += dx
        self.y += dy

        self.canvas.itemconfigure("point", text = f"({self.x}, {self.y})")

        X, Y = self.xy_to_XY(self.x, self.y)
        self.canvas.coords("point", X, Y)
    def _draw_body_on_canvas(self, index):
        Id = Obj[index]
        if Id == 1:
            self.canvas.create_oval(0, 0, 0, 0, tag = f"P{index}", width = 0, fill = "red")
    def _set_body(self, index):
        Id = Obj[index]
        args = Info[index]
        xy_pos = self.compute_position(index)
        XY_pos = self.xy_to_XY(*xy_pos)

        if Id == 1:
            rx = args[0] * self.Sx
            ry = args[0] * self.Sy
            self.canvas.coords(f"P{index}", XY_pos[0] - rx, XY_pos[1] - ry, XY_pos[0] + rx, XY_pos[1] + ry)
    def compute_position(self, index):
        T = Time[index]
        R = (1 / self.FPS) * self.frame
        for j, t in enumerate(T[0:-1]):
            if t <= R <= T[j + 1]:
                x1 = X[index][j]
                y1 = Y[index][j]
                x2 = X[index][j + 1]
                y2 = Y[index][j + 1]

                x_pos = x1 + (x2 - x1) * (R - t) / (T[j + 1] - t)
                y_pos = y1 + (y2 - y1) * (R - t) / (T[j + 1] - t)

                return (x_pos, y_pos)
        return (X[index][-1], Y[index][-1])
    def OnMouseWheel(self, event):
        delta = 4 * event.delta
        self.Sx += delta
        self.Sy += delta

        self.RedrawCoordinateAxes()

def main():
    root = tk.Tk()
    Application(root)

if __name__ == "__main__":
    main()
