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

monitoring_station = (26, 28)

def angle_between(p1, p2):
  x1,y1 = p1
  x2,y2 = p2

  return math.atan2(x2 - x1, y2 - y1) # flip x and y because grid is rotated

def distance_between(p1, p2):
  x1,y1 = p1
  x2,y2 = p2

  return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

angles = []
by_angle = {}

for asteroid in asteroids:
  if asteroid != monitoring_station:
    r = distance_between(monitoring_station, asteroid)
    theta = angle_between(monitoring_station, asteroid)

    if not by_angle.get(theta):
      angles.append(theta)

    by_angle.setdefault(theta, [])
    by_angle[theta].append((asteroid, r))
    by_angle[theta] = sorted(by_angle[theta], key = lambda _: _[1], reverse = True)

angles = sorted(angles, reverse = True)
last_asteroid_vaporized = None
vaporized_count = 0
i = 0

while i < len(angles):
  angle = angles[i]
  vaporized_asteroid = by_angle[angle].pop()

  if vaporized_asteroid:
    last_asteroid_vaporized = vaporized_asteroid[0]
    vaporized_count += 1

  i += 1 % len(angles)

  if vaporized_count == 200:
    break

print(last_asteroid_vaporized[0] * 100 + last_asteroid_vaporized[1])
