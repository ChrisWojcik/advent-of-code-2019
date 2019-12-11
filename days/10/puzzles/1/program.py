import sys

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

def collinear(p1, p2, p3):
  x1,y1 = p1
  x2,y2 = p2
  x3,y3 = p3

  return (x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2)) == 0

def between(p1, p2, p3):
  x1,y1 = p1
  x2,y2 = p2
  x3,y3 = p3

  if x1 != x2:
    return x1 <= x3 <= x2 or x2 <= x3 <= x1
  else:
    return y1 <= y3 <= y2 or y2 <= y3 <= y1

visible_asteroids = {}
monitoring_station_location = None
max_visible_asteroids = 0

for p1 in asteroids:
  visible_asteroids[p1] = set()

  for p2 in asteroids:
    if p2 != p1:
      has_line_of_sight = True
      for p3 in asteroids:
        if p1 != p2 and p2 != p3 and p3 != p1:
          if collinear(p1, p2, p3) and between(p1, p2, p3):
            has_line_of_sight = False
            break
      if has_line_of_sight:
        visible_asteroids[p1].add(p2)

  num_visible_asteroids = len(visible_asteroids[p1])

  if num_visible_asteroids > max_visible_asteroids:
    max_visible_asteroids = num_visible_asteroids
    monitoring_station_location = p1

print(monitoring_station_location)
print(max_visible_asteroids)
