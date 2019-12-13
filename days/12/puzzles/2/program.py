import sys
from math import gcd
from copy import deepcopy

moons = []

def lcm(a,b):
  if a == 0 and b == 0:
    return 0
  else:
    return (a * b) // gcd(a,b)

def apply_gravity(moon1, moon2, d):
  pos1 = moon1[0][d]
  pos2 = moon2[0][d]

  if pos1 != pos2:
    moon1[1][d] += 1 if pos1 < pos2 else -1

def apply_velocity(moon, d):
  moon[0][d] += moon[1][d]

for line in sys.stdin:
  position = list(map(lambda  _: int(_.split('=')[1]), line.strip()[:-1].split(',')))
  velocity = [0,0,0]
  moon = (position, velocity)
  moons.append(moon)

period_lengths = []
initial_state = deepcopy(moons)

for d in range(3):
  i = 0

  while True:
    for moon1 in moons:
      for moon2 in moons:
        if moon1 != moon2:
          apply_gravity(moon1, moon2, d)

    for moon in moons:
      apply_velocity(moon, d)

    i += 1

    cycle_found = True

    for j in range(len(moons)):
      if moons[j][0][d] != initial_state[j][0][d] or moons[j][1][d] != initial_state[j][1][d]:
        cycle_found = False
        break

    if cycle_found:
      period_lengths.append(i)
      break

print(lcm(period_lengths[0], lcm(period_lengths[1], period_lengths[2])))
