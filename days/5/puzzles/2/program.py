import sys

memory = sys.stdin.read().split(',')

POSITION_MODE = 0
IMMEDIATE_MODE = 1
DEFAULT_MODE = 0
ADDITION_OP = 1
MULTIPLY_OP = 2
INPUT_OP = 3
OUTPUT_OP = 4
JUMP_IF_TRUE_OP = 5
JUMP_IF_FALSE_OP = 6
LESS_THAN_OP = 7
EQUALS_OP = 8
HALT_OP = 99

def run_program(memory, inputs):
  i = 0
  outputs = []
  inputs_pointer = 0

  while i < len(memory):
    instruction = memory[i]
    op_code = int(instruction[-2:])
    param_modes = instruction[:-2][::-1]
    param_1_mode = int(param_modes[0]) if len(param_modes) else DEFAULT_MODE
    param_2_mode = int(param_modes[1]) if len(param_modes) > 1 else DEFAULT_MODE

    if op_code == ADDITION_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      param_2 = get_parameter(param_2_mode, i + 2, memory)

      memory[int(memory[i + 3])] = str(param_1 + param_2)

      i += 4
    elif op_code == MULTIPLY_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      param_2 = get_parameter(param_2_mode, i + 2, memory)

      memory[int(memory[i + 3])] = str(param_1 * param_2)

      i += 4
    elif op_code == INPUT_OP:
      value = inputs[inputs_pointer]
      inputs_pointer += 1
      param_1 = int(memory[i + 1])

      memory[param_1] = value

      i += 2
    elif op_code == OUTPUT_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      value = str(param_1)

      print(value)
      outputs.append(value)

      i += 2
    elif op_code == JUMP_IF_TRUE_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      param_2 = get_parameter(param_2_mode, i + 2, memory)

      if param_1 != 0:
        i = param_2
      else:
        i += 3
    elif op_code == JUMP_IF_FALSE_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      param_2 = get_parameter(param_2_mode, i + 2, memory)

      if param_1 == 0:
        i = param_2
      else:
        i += 3
    elif op_code == LESS_THAN_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      param_2 = get_parameter(param_2_mode, i + 2, memory)

      memory[int(memory[i + 3])] = '1' if param_1 < param_2 else '0'

      i += 4
    elif op_code == EQUALS_OP:
      param_1 = get_parameter(param_1_mode, i + 1, memory)
      param_2 = get_parameter(param_2_mode, i + 2, memory)

      memory[int(memory[i + 3])] = '1' if param_1 == param_2 else '0'

      i += 4
    elif op_code == HALT_OP:
      return outputs

def get_parameter(mode, pointer, memory):
  if mode == POSITION_MODE:
    position = int(memory[pointer])
    return int(memory[position])
  elif mode == IMMEDIATE_MODE:
    return int(memory[pointer])

run_program(memory, '5')
