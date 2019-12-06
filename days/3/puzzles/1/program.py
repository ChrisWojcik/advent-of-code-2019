import sys

wires = []
intersections = []
grid = {}

for line in sys.stdin:
  wires.append(line)

def follow_wire(starting_position, instruction, wire):
  direction = instruction[0]
  distance = int(instruction[1:])

  x = starting_position[0]
  y = starting_position[1]

  i = 1

  while i <= distance:
    if direction == 'U':
      new_position = (x, y + i)
    elif direction == 'D':
      new_position = (x, y - i)
    elif direction == 'R':
      new_position = (x + i, y)
    elif direction == 'L':
      new_position = (x - i, y)

    grid.setdefault(new_position, set()).add(wire)

    for other_wire in grid[new_position]:
      if other_wire != wire:
        intersections.append(new_position)
        break

    i += 1

  return new_position

def manhattan_distance(coordinate):
  return abs(coordinate[0]) + abs(coordinate[1])

for wire in wires:
  current_position = (0,0)
  instructions = wire.split(',')

  for instruction in instructions:
    current_position = follow_wire(current_position, instruction, wire)

shortest_manhattan_distance = min(map(manhattan_distance, intersections))
print(shortest_manhattan_distance)
