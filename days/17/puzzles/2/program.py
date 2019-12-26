import sys
import re

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

  def run(self, input_values = []):
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
        value = input_values.pop(0)
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

scaffolding = {}
program = sys.stdin.read()
robot = Computer(program)
x = 0
y = 0
robot_position = None
robot_facing = None
output = ''

while True:
  next_output = robot.run()

  if next_output != None:
    ascii_chr = chr(int(next_output))
    output += ascii_chr

    if ascii_chr == '\n':
      x = 0
      y -= 1
    else:
      if ascii_chr == '#' or ascii_chr == '^' or ascii_chr == 'v' or ascii_chr == '<' or ascii_chr == '>':
        scaffolding[(x,y)] = set()

        if (x - 1, y) in scaffolding:
          scaffolding[(x, y)].add((x - 1, y))
          scaffolding[(x - 1, y)].add((x, y))

        if (x, y + 1) in scaffolding:
          scaffolding[(x, y)].add((x, y + 1))
          scaffolding[(x, y + 1)].add((x, y))

        if ascii_chr == '^':
          robot_facing = (0, 1)
          robot_position = (x, y)
        if ascii_chr == 'v':
          robot_facing = (0, -1)
          robot_position = (x, y)
        if ascii_chr == '<':
          robot_facing = (-1, 0)
          robot_position = (x, y)
        if ascii_chr == '>':
          robot_facing = (1, 0)
          robot_position = (x, y)

      x += 1
  else:
    break

new_program = '2' + program[1:]

# assumptions:
# "in general" the scaffoling follows a path but loops back on itself, so -
# robot will always go straight for as long as possible, turning only when it's the only option
# when it is forced to turn, there will only be one way to turn
# and if its only movement option is backtracking, it has reached the end
operations = []
steps_in_current_direction = 0
current_node = robot_position
current_direction = robot_facing
reached_end = False

while not reached_end:
  neighbors = scaffolding[current_node]
  x, y = current_node
  dxS, dyS = current_direction
  left = (dyS * -1, dxS)
  right = (dyS, dxS * -1)
  dxL, dyL = left
  dxR, dyR = right

  go_straight = (x + dxS, y + dyS)
  turn_left = (x + dxL, y + dyL)
  turn_right = (x + dxR, y + dyR)

  if go_straight in neighbors:
    steps_in_current_direction += 1
    current_node = go_straight
  elif turn_left in neighbors:
    if steps_in_current_direction > 0:
      operations.append(str(steps_in_current_direction))

    operations.append('L')
    steps_in_current_direction = 0
    current_direction = left
  elif turn_right in neighbors:
    if steps_in_current_direction > 0:
      operations.append(str(steps_in_current_direction))

    operations.append('R')
    steps_in_current_direction = 0
    current_direction = right
  else:
    operations.append(str(steps_in_current_direction))
    reached_end = True

def valid_movement_function(fn):
  unique_operations = set(operations)
  fn_ops = fn.split(',')

  for op in fn_ops:
    if op not in unique_operations:
      return False

  if len(fn) > 20: return False
  if len(fn) < 2: return False
  if fn[0] == ',': return False
  if fn[-1] == ',': return False
  return True

path = ','.join(operations)
movement_functions = [path[i:j] for i in range(len(path)) for j in range(i + 1, len(path) + 1)]
movement_functions = set(filter(valid_movement_function, movement_functions))

# only fns that match the first n characters of the path are candidates for A
a_candidates = [fn for fn in movement_functions if fn == path[0:len(fn)]]

# only fns that match the last n characters of the path are candidates for B
b_candidates = [fn for fn in movement_functions if fn == path[-1 * len(fn):]]

# only fns that match the first n characters of the path when combined with A are candidates for C
c_candidates = [fn for fn in movement_functions for a in a_candidates if ','.join([a, fn]) == path[0:len(fn) + len(a) + 1]]

combinations = [(a,b,c) for a in a_candidates for b in b_candidates for c in c_candidates]

for a,b,c in combinations:
  # A then 0 or more of A|B|C then B
  regex = r"^" + re.escape(a) + r",(?:" + re.escape(a) + r",|" + re.escape(b) + r",|" + re.escape(c) + r",)*" + re.escape(b) + r"$"
  matches = re.fullmatch(regex, path)

  if matches:
    # get the starting index of matches for each of the subroutines
    a_indexes = [(m.start(), m.groupdict()) for m in re.finditer(r"(?P<A>" + re.escape(a) + ")", path)]
    b_indexes = [(m.start(), m.groupdict()) for m in re.finditer(r"(?P<B>" + re.escape(b) + ")", path)]
    c_indexes = [(m.start(), m.groupdict()) for m in re.finditer(r"(?P<C>" + re.escape(c) + ")", path)]

    # sort the names by index then convert to character codes an interleave with commas (44)
    indexes = a_indexes + b_indexes + c_indexes
    main_routine = list(map(lambda _: str(ord(list(_[1].keys())[0])), sorted(indexes, key=lambda _: _[0])))
    main_routine = (',' + str(ord(',')) + ',').join(main_routine).split(',')

    function_a = list(map(lambda _: str(ord(_)), a))
    function_b = list(map(lambda _: str(ord(_)), b))
    function_c = list(map(lambda _: str(ord(_)), c))

    robot = Computer(new_program)
    inputs = main_routine + ['10'] + function_a + ['10'] + function_b + ['10'] + function_c + ['10'] + [str(ord('n'))] + ['10']

    dust_collected = None

    while True:
      output = robot.run(inputs)

      if output:
        dust_collected = output
      else:
        break

    print(dust_collected)
    break
