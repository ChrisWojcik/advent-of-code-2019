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

scaffolding = {}
program = sys.stdin.read()
robot = Computer(program)
x = 0
y = 0

output = ''

while True:
  next_output = robot.run()

  if next_output != None:
    ascii_chr = chr(int(next_output))
    output += ascii_chr

    if ascii_chr == '\n':
      x = 0
      y += 1
    else:
      if ascii_chr == '#' or ascii_chr == '^' or ascii_chr == 'v' or ascii_chr == '<' or ascii_chr == '>':
        scaffolding[(x,y)] = set()

        if (x - 1, y) in scaffolding:
          scaffolding[(x, y)].add((x - 1, y))
          scaffolding[(x - 1, y)].add((x, y))

        if (x, y - 1) in scaffolding:
          scaffolding[(x, y)].add((x, y - 1))
          scaffolding[(x, y - 1)].add((x, y))

      x += 1
  else:
    break

print(output)
camera_calibration = 0

for node in scaffolding:
  if len(scaffolding[node]) == 4:
    x, y = node
    camera_calibration += x * y

print(camera_calibration)
