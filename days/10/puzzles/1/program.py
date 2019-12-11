import sys
import math

x = 0
y = 0
asteroids = []

for line in sys.stdin:
  locations = list(line.strip())
  x = 0

  for location in locations:
    if location == '#':
      asteroids.append((x,y))
    x += 1

  y += 1

def angle_between(p1, p2):
  x1,y1 = p1
  x2,y2 = p2

  return math.atan2(x2 - x1, y2 - y1) # flip x and y because grid is rotated

unique_line_of_sight_angles = {}
monitoring_station_location = None
max_visible_asteroids = 0

for p1 in asteroids:
  unique_line_of_sight_angles[p1] = set()

  for p2 in asteroids:
    if p2 != p1:
      theta = angle_between(p1, p2)
      unique_line_of_sight_angles[p1].add(theta)

  num_visible_asteroids = len(unique_line_of_sight_angles[p1])

  if num_visible_asteroids > max_visible_asteroids:
    max_visible_asteroids = num_visible_asteroids
    monitoring_station_location = p1

print(monitoring_station_location)
print(max_visible_asteroids)
