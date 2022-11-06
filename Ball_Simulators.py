import tkinter as tk
import random
import copy

#Number of Balls
N = 9

#Size of Balls
Re = 40

class Application:
    def __init__(self, master = None):
        self.master = tk.Tk() if master == None else master
        self.master.title("Ball Simulator")

        self.canvas = tk.Canvas(self.master, highlightthickness = 0, bg = "#5E5E5E")
        self.canvas.pack(fill = "both", expand = True)

        self.width = 1000
        self.height = 1000

        self.ball_coords = []
        self.ball_vel = []
        self.radii = []
        #self.radius = 10

        fps = 60
        step = int(1 / fps * 1000) 
        dt = .5

        self.CreateBalls(N)

        self.canvas.bind("<Configure>", self.onWindowChange)
        self.master.bind("<space>", lambda event: self.timeStep(dt))
        self.master.bind("<a>", lambda event: self.play(step, dt))
        self.master.bind("<w>", lambda event: print(self.width, self.height))
        self.master.bind("<s>", lambda event: print("Coords: ", self.ball_coords, "Vel: ", self.ball_vel))
    def CreateBalls(self, n):
        for i in range(n):
            radius = Re #random.randint(4, 15)

            x = random.randint(radius, self.width - radius)
            y = random.randint(radius, self.height - radius)

            vx = random.randint(-30, 40)
            vy = random.randint(-45, 30)

            self.ball_coords.append([x, y])
            self.ball_vel.append([vx, vy])
            self.radii.append(radius)

            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill = "cyan", width = 1, outline = "dark cyan", tag = f"B{i}")
    def onWindowChange(self, event):
        self.width = event.width
        self.height = event.height
    def timeStep(self, dt):
        for i, pos in enumerate(self.ball_coords):
            vx, vy = self.ball_vel[i]
            x, y = pos
            radius = self.radii[i]

            dx = vx * dt
            dy = vy * dt

            X = x + dx
            Y = y + dy

            while True:
                if X - radius <= 0:
                    T = (radius - x) / vx
                    vx *= -1
                    X = radius + vx * (dt - T)
                    self.ball_vel[i][0] = vx
                    x = radius
                    continue
                if X + radius >= self.width:
                    T = (self.width - radius - x) / vx
                    vx *= -1
                    X = self.width - radius + vx * (dt - T)
                    self.ball_vel[i][0] = vx
                    x = self.width - radius
                    continue
                break

            while True:
                if Y - radius <= 0:
                    T = (radius - y) / vy
                    vy *= -1
                    Y = radius + vy * (dt - T)
                    self.ball_vel[i][1] = vy
                    y = radius
                    continue
                if Y + radius >= self.height:
                    T = (self.height - radius - y) / vy
                    vy *= -1
                    Y = self.height - radius + vy * (dt - T)
                    self.ball_vel[i][1] = vy
                    y = self.height - radius
                    continue
                break

            self.ball_coords[i] = [X, Y]
            self.canvas.coords(f"B{i}", X - radius, Y - radius, X + radius, Y + radius)

        W = self.master.winfo_width() / 2
        H = self.master.winfo_height() / 2
        for i, B1 in enumerate(self.ball_coords):
            for j, B2 in enumerate(self.ball_coords):
                if i == j:
                    continue

                R1 = self.radii[i]
                R2 = self.radii[j]
                
                x1, y1 = B1
                x2, y2 = B2

                if (x2 - x1) ** 2 + (y2 - y1) ** 2 > (R2 + R1) ** 2:
                    continue

                v1_x, v1_y = self.ball_vel[i]
                v2_x, v2_y = self.ball_vel[j]

                xx1 = x1 - W
                yy1 = H - y1
                xx2 = x2 - W
                yy2 = H - y2

                if xx2 != xx1:
                    m = (yy2 - yy1) / (xx2 - xx1)
                else:
                    m = 0

                c1_X = (v1_x + v1_y * m) / (1 + m ** 2)
                c1_Y = (c1_X * m - v1_y)

                c2_X = (v2_x + v2_y * m) / (1 + m ** 2)
                c2_Y = (c2_X * m - v2_y)

                c1_X *= -1
                c2_X *= -1

                V1_x = c1_X + c1_Y * m
                V1_y = c1_X * m - c1_Y

                V2_x = c2_X + c2_Y * m
                V2_y = c2_X * m - c2_Y

                old_x1 = x1 - v1_x * dt
                old_y1 = y1 - v1_y * dt

                old_x2 = x2 - v1_x * dt
                old_y2 = y2 - v1_y * dt

                beta = old_x2 - old_x1
                gamma = old_y2 - old_y1
                delta = v2_x - v1_x
                nu = v2_y - v1_y
                eta = (R1 + R2) ** 2

                a = nu ** 2 + delta ** 2
                b = 2 * (gamma * nu + beta * delta)
                c = beta ** 2 + gamma ** 2 - eta

                Tp = (-b + (b ** 2 - 4 * a * c) ** .5) / (2 * a)
                Tm = (-b - (b ** 2 - 4 * a * c) ** .5) / (2 * a)

                w = (dt - Tm)
                
                X1 = old_x1 + V1_x * w
                Y1 = old_y1 + V1_y * w

                X2 = old_x2 + V2_x * w
                Y2 = old_y2 + V2_y * w

                self.ball_coords[i] = [X1, Y1]
                self.ball_coords[j] = [X2, Y2]

                self.ball_vel[i] = [V1_x, V1_y]
                self.ball_vel[j] = [V2_x, V2_y]

                self.canvas.coords(f"B{i}", X1 - R1, Y1 - R1, X1 + R1, Y1 + R1)
                self.canvas.coords(f"B{j}", X2 - R2, Y2 - R2, X2 + R2, Y2 + R2)
    def play(self, step, dt):
        self.timeStep(dt)
        self.master.after(step, self.play, step, dt)

def main():
    root = tk.Tk()
    app = Application(root)

if __name__ == "__main__":
    main()