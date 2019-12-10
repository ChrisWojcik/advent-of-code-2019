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
RELATIVE_BASE_OFFST_OP = 9
HALT_OP = 99

class Computer():
  def __init__(self, program):
    self._program = program
    self.reset_memory()

  def read(self, pointer):
    return self._memory.get(int(pointer)) or '0'

  def write(self, pointer, value):
    self._memory[int(pointer)] = str(value)

  def reset_memory(self):
    instructions = self._program.split(',')
    memory = {}

    for i in range(len(instructions)):
      memory[i] = instructions[i]

    self._memory = memory
    self._relative_base = 0

  def _read_by_parameter(self, mode, pointer):
    if mode == POSITION_MODE:
      position = int(self.read(pointer))
      return int(self.read(position))
    elif mode == IMMEDIATE_MODE:
      return int(self.read(pointer))
    elif mode == RELATIVE_MODE:
      offset = int(self.read(pointer))
      return int(self.read(offset + self._relative_base))

  def _get_write_address(self, mode, pointer):
    if mode == POSITION_MODE or mode == IMMEDIATE_MODE:
      return int(self.read(pointer))
    if mode == RELATIVE_MODE:
      return int(self.read(pointer)) + self._relative_base

  def run(self, inputs = []):
    i = 0
    inputs_pointer = 0
    outputs = []

    while True:
      instruction = self.read(i)
      op_code = int(instruction[-2:])
      param_modes = instruction[:-2][::-1]
      param_1_mode = int(param_modes[0]) if len(param_modes) else DEFAULT_MODE
      param_2_mode = int(param_modes[1]) if len(param_modes) > 1 else DEFAULT_MODE
      param_3_mode = int(param_modes[2]) if len(param_modes) > 2 else DEFAULT_MODE

      if op_code == ADDITION_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        param_2 = self._read_by_parameter(param_2_mode, i + 2)
        write_address = self._get_write_address(param_3_mode, i + 3)

        self.write(write_address, param_1 + param_2)

        i += 4
      elif op_code == MULTIPLY_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        param_2 = self._read_by_parameter(param_2_mode, i + 2)
        write_address = self._get_write_address(param_3_mode, i + 3)

        self.write(write_address, param_1 * param_2)

        i += 4
      elif op_code == INPUT_OP:
        value = inputs[inputs_pointer]
        inputs_pointer += 1
        write_address = self._get_write_address(param_1_mode, i + 1)

        self.write(write_address, value)

        i += 2
      elif op_code == OUTPUT_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        value = str(param_1)

        outputs.append(value)

        i += 2
      elif op_code == JUMP_IF_TRUE_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        param_2 = self._read_by_parameter(param_2_mode, i + 2)

        if param_1 != 0:
          i = param_2
        else:
          i += 3
      elif op_code == JUMP_IF_FALSE_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        param_2 = self._read_by_parameter(param_2_mode, i + 2)

        if param_1 == 0:
          i = param_2
        else:
          i += 3
      elif op_code == LESS_THAN_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        param_2 = self._read_by_parameter(param_2_mode, i + 2)
        write_address = self._get_write_address(param_3_mode, i + 3)

        self.write(write_address, '1' if param_1 < param_2 else '0')

        i += 4
      elif op_code == EQUALS_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)
        param_2 = self._read_by_parameter(param_2_mode, i + 2)
        write_address = self._get_write_address(param_3_mode, i + 3)

        self.write(write_address, '1' if param_1 == param_2 else '0')

        i += 4
      elif op_code == RELATIVE_BASE_OFFST_OP:
        param_1 = self._read_by_parameter(param_1_mode, i + 1)

        self._relative_base += param_1

        i += 2
      elif op_code == HALT_OP:
        return outputs

program = sys.stdin.read()
computer = Computer(program)

print(computer.run('2')[0])
