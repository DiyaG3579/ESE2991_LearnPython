import matplotlib.pyplot as plt
import numpy as num
from matplotlib.path import Path
from matplotlib.patches import Wedge
import matplotlib.patches as patches
import random

coordinates = []
def regular_polygon(n, radius=1, center=(0, 0)):
    cx, cy = center
    angles = num.linspace(0, 2*num.pi, n+1, endpoint=True)

    return [
        (cx + radius*num.cos(a), cy + radius*num.sin(a))
        for a in angles
    ]

def ring(cx, cy, oradius, iradius):
    return Wedge(center = (cx,cy),r = oradius, theta1 = 0, theta2 = 360, width = oradius-iradius, facecolor = 'blue', edgecolor = 'black')

def square(c1x, c1y, c2x, c2y, c3x, c3y, c4x, c4y, fc, ec):
    square = ((c1x, c1y),
           (c2x, c2y),
           (c3x, c3y),
           (c4x, c4y),
           (c1x, c1y))
    square_path = Path(square)
    return patches.PathPatch(square_path, facecolor = fc, edgecolor = ec)

def testerx(xi):
    upper = max(9.0, xi + 1.0)
    lower = min(-9.0, xi - 1.0)
    x = round(random.uniform(lower, upper),3)
    return x
def testery(yi):
    uppery = max(9.0, yi + 1.0)
    lowery = min(-9.0, yi - 1.0)
    y = round(random.uniform(lowery, uppery),3)
    return y

def euclidean(x, y, coordinates):
    distance2 = 100
    for coordinate in coordinates:
        point1 = num.array([x, y])
        point2 = num.array(coordinate)

        distance = num.linalg.norm(point1-point2)
        
        if distance < distance2:
            distance2 = distance
            current = coordinate

    return current

def line_hits_obstacle(p1, p2, paths, samples=20):
    xs = num.linspace(p1[0], p2[0], samples)
    ys = num.linspace(p1[1], p2[1], samples)

    for x, y in zip(xs, ys):
        for path in paths:
            if path.contains_point((x, y), radius=0.05):
                return True
    return False

square = square(-9, -9, 9, -9, 9, 9, -9, 9, 'lightblue', 'black')
septagon_info = [(7, 3, (6, -6)), (7, 1, (-8, 0)), (7, 2, (3, 5)), (7, 1.5, (-1, -1))]

septagon_paths = []
septagon_patches = []

for n, r, center in septagon_info:
    path = Path(regular_polygon(n, r, center))
    patch = patches.PathPatch(path, facecolor = 'blue', edgecolor = "black")
    septagon_paths.append(path)
    septagon_patches.append(patch)

xi = -7.5
yi = -7.5
xt = -1 
yt = 7

coordinates.append([xi,yi])

fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.add_patch(square)
for septagon in septagon_patches:
    ax.add_patch(septagon)
ax.plot(xi, yi, 'o',color = 'red')
ax.plot(xt, yt, 'o', color = 'green')


inside = False
i = 0
while ((abs(xi - xt) > 0.25) or (abs(yi - yt) > 0.25)) and i <= 1000:
    xi = testerx(xi)
    yi = testery(yi)
    for path in septagon_paths:
        if path.contains_point((xi, yi), radius = 0.1):
            inside = True
    if inside == False:
        pointc = euclidean(xi, yi, coordinates)
        pointb = [xi, yi]
        if not line_hits_obstacle(pointb, pointc, septagon_paths):
            ax.plot(xi, yi, '.', color = 'black')
            ax.plot([pointb[0], pointc[0]],[pointb[1], pointc[1]],'-',color='black')
            ax.plot(xi, yi, '.', color = 'black')
            coordinates.append([xi,yi])
    else:
        inside = False
    i=i+1

ax.set_aspect('equal')
ax.set_title("Enviorment Test 1")

plt.show()
