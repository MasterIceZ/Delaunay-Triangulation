import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys

if len(sys.argv) != 2:
  print('Usage: python mcv.py <input_file>')
  sys.exit(1)

edges = []
point_set = set()

with open(sys.argv[1], 'r') as file:
  for line in file:
    line = line.strip()
    if line:
      points = line.split(' - ')
      point1 = tuple(map(float, points[0].strip('()').split(',')))
      point2 = tuple(map(float, points[1].strip('()').split(',')))
      point_set.add(point1)
      point_set.add(point2)
      edges.append((point1, point2))

points = np.array(list(point_set))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for edge in edges:
  edge_points = np.array(edge)
  ax.plot(edge_points[:, 0], edge_points[:, 1], edge_points[:, 2], color='black')

ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='b')

triangles = []
edge_dict = {}
for edge in edges:
  p1, p2 = edge
  if p1 not in edge_dict:
    edge_dict[p1] = set()
  if p2 not in edge_dict:
    edge_dict[p2] = set()
  edge_dict[p1].add(p2)
  edge_dict[p2].add(p1)

for p1 in edge_dict:
  for p2 in edge_dict[p1]:
    for p3 in edge_dict[p2]:
      if p3 in edge_dict[p1] and p1 != p2 and p2 != p3 and p1 != p3:
        triangle = sorted([p1, p2, p3])
        if triangle not in triangles:
          triangles.append(triangle)

for triangle in triangles:
  vertices = np.array(triangle)
  poly = Poly3DCollection([vertices], edgecolor='black', facecolors='cyan', alpha=0.5)
  ax.add_collection3d(poly)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()