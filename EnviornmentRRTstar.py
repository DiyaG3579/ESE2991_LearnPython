import matplotlib.pyplot as plt
import numpy as num
from matplotlib.path import Path
from matplotlib.patches import Wedge
import matplotlib.patches as patches
import random

coordinates = []
parents = {}
cost = {}

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
    x = round(random.uniform(-9.0, 9.0),3)
    return x
def testery(yi):
    y = round(random.uniform(-9.0, 9.0),3)
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

def distance(p1, p2):
    p1 = num.array(p1)
    p2 = num.array(p2)
    return num.linalg.norm(p1 - p2)

def line_hits_obstacle(p1, p2, paths, samples=20):
    xs = num.linspace(p1[0], p2[0], samples)
    ys = num.linspace(p1[1], p2[1], samples)

    for x, y in zip(xs, ys):
        for path in paths:
            if path.contains_point((x, y), radius=0.05):
                return True
    return False

def near_nodes(p_new, coordinates, radius):
    neighbors = []
    for node in coordinates:
        if distance(node, p_new) <= radius:
            neighbors.append(tuple(node))
    return neighbors 

def steer(pEucl, pRand, epsilon):
    pEucl = num.array(pEucl)
    pRand = num.array(pRand)

    direction = pRand - pEucl
    dist = num.linalg.norm(direction)

    if dist == 0:
        return p_near.tolist()

    direction = direction / dist   # normalize

    p_new = pEucl + epsilon * direction

    return p_new.tolist()

square = square(-9, -9, 9, -9, 9, 9, -9, 9, 'lightblue', 'black')

septagon_info = [(7, 3, (6, -6)), 
                 (7, 1, (-8, 0)), 
                 (7, 2, (3, 5)), 
                 (7, 1.5, (-1, -1)), 
                 (7, 2, (-4, 4)), 
                 (7, 1.5, (-4, -4.5)), 
                 (7, 2, (4, 0)), 
                 #(3, 0.5, (-4,0)),
                 (8, 1.5, (7, 7))]

septagon_paths = []
septagon_patches = []

for n, r, center in septagon_info:
    path = Path(regular_polygon(n, r, center))
    patch = patches.PathPatch(path, facecolor = 'blue', edgecolor = "black")
    septagon_paths.append(path)
    septagon_patches.append(patch)

xi = -7.5
yi = -7.5
xt = -5
yt = 7
epsilon = 0.5
radius = 1.5

coordinates.append([xi,yi])
parents[(xi, yi)] = None
cost[(xi, yi)] = 0

fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.add_patch(square)
for septagon in septagon_patches:
    ax.add_patch(septagon)
ax.plot(xi, yi, 'o',color = 'red')
ax.plot(xt, yt, 'o', color = 'green')

#Instead of straight to line, move via epsillon on that line

inside = False
insideout = False
i = 0
while ((abs(xi - xt) > 0.25) or (abs(yi - yt) > 0.25)) and i <= 2000:
    xi = testerx(xi)
    yi = testery(yi)
    for path in septagon_paths:
        if path.contains_point((xi, yi), radius = 0.1):
            inside = True
    if inside == False:
        pointc = euclidean(xi, yi, coordinates)
        pointb = [xi, yi]
        pointa = steer(pointc, pointb, epsilon)
        for path in septagon_paths:
            if path.contains_point(pointa, radius = 0.1):
                insideout = True
        if not line_hits_obstacle(pointc, pointa, septagon_paths) and insideout == False:
            xi = pointa[0]
            yi = pointa[1]
            node_new = (xi, yi)
            neighbors = near_nodes(node_new, coordinates, radius)
            parent_s = tuple(pointc)
            c_cost = cost[parent_s] + distance(parent_s, node_new)

            for neighbor in neighbors:
                if not line_hits_obstacle(neighbor, node_new, septagon_paths):
                    new_cost = cost[neighbor] + distance(neighbor, node_new)
                    if new_cost < c_cost:
                        c_cost = new_cost
                        parent_s = neighbor
            coordinates.append([xi, yi])
            parents[node_new] = parent_s
            cost[node_new] = c_cost
        else:
            insideout = False
    else:
        inside = False
    i=i+1

for node in parents:
    parent = parents[node]
    if parent is not None:
        ax.plot(
            [node[0], parent[0]],
            [node[1], parent[1]],
            '-',
            color='black'
        )
for node in parents:
    ax.plot(node[0], node[1], '.', color='black')

ax.set_aspect('equal')
ax.set_title("Enviorment Test 2")

plt.show()
