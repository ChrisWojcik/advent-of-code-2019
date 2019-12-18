import sys

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2
DEFAULT_MODE = 0
ADDITION_OP = 1
MULTIPLY_OP = 2
INPUT_OP = 3
OUTPUT_OP = 4
JUMP_IF_TRUE_OP = 5
JUMP_IF_FALSE_OP = 6
LESS_THAN_OP = 7
EQUALS_OP = 8
RELATIVE_BASE_OFFSET_OP = 9
HALT_OP = 99

class Computer():
  def __init__(self, program):
    self._program = program
    self.reset_memory()

  def _modeless_read(self, pointer):
    return self._memory.get(int(pointer)) or '0'

  def read(self, mode, pointer):
    if mode == POSITION_MODE:
      position = int(self._modeless_read(pointer))
      return self._modeless_read(position)
    elif mode == IMMEDIATE_MODE:
      return self._modeless_read(pointer)
    elif mode == RELATIVE_MODE:
      offset = int(self._modeless_read(pointer))
      return self._modeless_read(offset + self._relative_base)

  def write(self, mode, pointer, value):
    if mode == POSITION_MODE or mode == IMMEDIATE_MODE:
      address = int(self._modeless_read(pointer))
    if mode == RELATIVE_MODE:
      address = int(self._modeless_read(pointer)) + self._relative_base

    self._memory[address] = str(value)

  def reset_memory(self):
    instructions = self._program.split(',')
    memory = {}

    for i in range(len(instructions)):
      memory[i] = instructions[i]

    self._memory = memory
    self._pointer = 0
    self._relative_base = 0

  def run(self, input_value = None):
    i = self._pointer

    while True:
      instruction = self._modeless_read(i)
      op_code = int(instruction[-2:])
      param_modes = instruction[:-2][::-1]
      param_1_mode = int(param_modes[0]) if len(param_modes) else DEFAULT_MODE
      param_2_mode = int(param_modes[1]) if len(param_modes) > 1 else DEFAULT_MODE
      param_3_mode = int(param_modes[2]) if len(param_modes) > 2 else DEFAULT_MODE

      if op_code == ADDITION_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, int(value_1) + int(value_2))

        i += 4
      elif op_code == MULTIPLY_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, int(value_1) * int(value_2))

        i += 4
      elif op_code == INPUT_OP:
        value = input_value
        #print(value)

        self.write(param_1_mode, i + 1, value)

        i += 2
      elif op_code == OUTPUT_OP:
        value = self.read(param_1_mode, i + 1)
        #print(value)

        i += 2

        self._pointer = i
        return value
      elif op_code == JUMP_IF_TRUE_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        if int(value_1) != 0:
          i = int(value_2)
        else:
          i += 3
      elif op_code == JUMP_IF_FALSE_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        if int(value_1) == 0:
          i = int(value_2)
        else:
          i += 3
      elif op_code == LESS_THAN_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, '1' if int(value_1) < int(value_2) else '0')

        i += 4
      elif op_code == EQUALS_OP:
        value_1 = self.read(param_1_mode, i + 1)
        value_2 = self.read(param_2_mode, i + 2)

        self.write(param_3_mode, i + 3, '1' if value_1 == value_2 else '0')

        i += 4
      elif op_code == RELATIVE_BASE_OFFSET_OP:
        value = self.read(param_1_mode, i + 1)

        self._relative_base += int(value)

        i += 2
      elif op_code == HALT_OP:
        return

program = sys.stdin.read()
droid = Computer(program)
cardinal_direction = { 1:(0, 1), 2:(0, -1), 3:(-1, 0), 4:(1, 0) }
reverse_direction = { 1:2, 2:1, 3:4, 4:3 }

def explore_maze():
  maze = {}
  explored_nodes = {}
  walls = {}
  start_node = (0,0)
  end_node = None
  current_node = start_node
  current_path = [(start_node, None)]

  while len(current_path) > 0:
    current_node = current_path[-1][0]
    explored_nodes[current_node] = True
    new_direction = None
    x, y = current_node

    for i in range(1,5):
      dx, dy = cardinal_direction[i]
      new_node = (x + dx, y + dy)

      if not explored_nodes.get(new_node):
        if not walls.get(new_node):
          result = droid.run(i)

          if result == '0':
            walls[new_node] = True
          else:
            maze.setdefault(current_node, set())
            maze.setdefault(new_node, set())
            maze[current_node].add(new_node)

            if result == '2':
              end_node = new_node

            new_direction = i
            current_path.append((new_node, i))
            break
      else:
        maze[current_node].add(new_node)

    if not new_direction:
      current_node, current_direction = current_path.pop()

      if current_direction:
        new_direction = reverse_direction[current_direction]
        droid.run(new_direction)

  return (maze, start_node, end_node)

def calc_fill_time(maze, start_node):
  timer = 0
  visited_nodes = {}
  nodes_to_visit = [start_node]

  while len(nodes_to_visit) > 0:
    nodes_filling_on_this_step = nodes_to_visit
    nodes_to_visit = []

    for node in nodes_filling_on_this_step:
      visited_nodes[node] = True

      for neighbor in maze[node]:
        if not visited_nodes.get(neighbor):
          nodes_to_visit.append(neighbor)

    timer += 1

  return timer - 1

maze, start_node, end_node = explore_maze()
print(calc_fill_time(maze, end_node))
