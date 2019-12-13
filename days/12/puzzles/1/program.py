import sys

STEP_COUNT = 1000
moons = []

def apply_gravity(moon1, moon2):
  for d in range(3):
    pos1 = moon1[0][d]
    pos2 = moon2[0][d]

    if pos1 != pos2:
      moon1[1][d] += 1 if pos1 < pos2 else -1

def apply_velocity(moon):
  for d in range(3):
    moon[0][d] += moon[1][d]

for line in sys.stdin:
  position = list(map(lambda  _: int(_.split('=')[1]), line.strip()[:-1].split(',')))
  velocity = [0,0,0]
  moon = (position, velocity)
  moons.append(moon)

for i in range(STEP_COUNT):
  for moon1 in moons:
    for moon2 in moons:
      if moon1 != moon2:
        apply_gravity(moon1, moon2)

  for moon in moons:
    apply_velocity(moon)

total_energy = sum([sum(map(abs, moon[0])) * sum(map(abs, moon[1])) for moon in moons])
print(total_energy)
