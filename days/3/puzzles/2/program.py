import sys

wires = []
intersections = []
grid = {}

for line in sys.stdin:
  wires.append(line)

def follow_wire(starting_position, instruction, wire, steps_taken):
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

    steps_taken += 1

    grid.setdefault(new_position, {})
    grid[new_position].setdefault(wire, steps_taken)

    for other_wire in grid[new_position]:
      if other_wire != wire:
        intersections.append(grid[new_position])
        break

    i += 1

  return (new_position, steps_taken)

def signal_delay(position):
  return sum(position.values())

for wire in wires:
  current_position = (0,0)
  steps_taken = 0
  instructions = wire.split(',')

  for instruction in instructions:
    current_position, steps_taken = follow_wire(current_position, instruction, wire, steps_taken)

lowest_signal_delay = min(map(signal_delay, intersections))
print(lowest_signal_delay)
