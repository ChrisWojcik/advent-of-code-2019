import sys
from PIL import Image

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
RELATIVE_BASE_OFFST_OP = 9
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
      elif op_code == RELATIVE_BASE_OFFST_OP:
        value = self.read(param_1_mode, i + 1)

        self._relative_base += int(value)

        i += 2
      elif op_code == HALT_OP:
        return

program = sys.stdin.read()
computer = Computer(program)

painted_panels = {}
current_panel = (0,0)
robot_direction = 'UP'
painted_panels[current_panel] = '1'
pixels = []

max_x = 0
max_y = 0
min_x = 0
min_y = 0

while True:
  x,y = current_panel
  current_color = painted_panels.get(current_panel) or '0'
  new_color = computer.run(current_color)

  if not new_color:
    break

  movement_instruction = computer.run()

  if not movement_instruction:
    break

  painted_panels[current_panel] = new_color

  if movement_instruction == '0':
    if robot_direction == 'UP':
      robot_direction = 'LEFT'
      current_panel = (x - 1, y)
    elif robot_direction == 'LEFT':
      robot_direction = 'DOWN'
      current_panel = (x, y - 1)
    elif robot_direction == 'DOWN':
      robot_direction = 'RIGHT'
      current_panel = (x + 1, y)
    elif robot_direction == 'RIGHT':
      robot_direction = 'UP'
      current_panel = (x, y + 1)
  elif movement_instruction == '1':
    if robot_direction == 'UP':
      robot_direction = 'RIGHT'
      current_panel = (x + 1, y)
    elif robot_direction == 'LEFT':
      robot_direction = 'UP'
      current_panel = (x, y + 1)
    elif robot_direction == 'DOWN':
      robot_direction = 'LEFT'
      current_panel = (x - 1, y)
    elif robot_direction == 'RIGHT':
      robot_direction = 'DOWN'
      current_panel = (x, y - 1)

  x,y = current_panel
  max_x = max(max_x, x)
  min_x = min(min_x, x)
  max_y = max(max_y, y)
  min_y = min(min_y, y)

WIDTH = (max_x - min_x) + 1 # include (0,0)
HEIGHT = (max_y - min_y) + 1 # include (0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
pixels = []

start_x = min_x
start_y = max_y

for i in range(HEIGHT):
  for j in range(WIDTH):
    pixel = painted_panels.get((start_x + j, start_y - i))

    if pixel == '1':
      pixels.append(WHITE)
    else:
      pixels.append(BLACK)

img = Image.new('RGB', (WIDTH,HEIGHT))
img.putdata(pixels)
img.save('registration-identifier.png')
