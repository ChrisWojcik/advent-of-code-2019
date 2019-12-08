import sys
from itertools import permutations

initial_memory = sys.stdin.read().split(',')

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

def run_program(amplifier):
  i = amplifier['pointer']
  memory = amplifier['memory']
  inputs = amplifier['inputs']
  inputs_pointer = amplifier['inputs_pointer']
  outputs = amplifier['outputs']

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

      outputs.append(value)
      i += 2

      return {
        'memory': memory,
        'pointer': i,
        'inputs': inputs,
        'inputs_pointer': inputs_pointer,
        'outputs': outputs,
        'did_halt': False
      }
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
      return {
        'memory': memory,
        'pointer': i,
        'inputs': inputs,
        'inputs_pointer': inputs_pointer,
        'outputs': outputs,
        'did_halt': True
      }

def get_parameter(mode, pointer, memory):
  if mode == POSITION_MODE:
    position = int(memory[pointer])
    return int(memory[position])
  elif mode == IMMEDIATE_MODE:
    return int(memory[pointer])

test_sequences = permutations(['5', '6', '7', '8', '9'])
max_thruster_signal = 0

for test_sequence in test_sequences:
  thruster_signal = None
  amplifiers = []

  for i in range(len(test_sequence)):
    amplifiers.append({
      'memory': initial_memory.copy(),
      'pointer': 0,
      'inputs': [test_sequence[i]],
      'inputs_pointer': 0,
      'outputs': [],
      'did_halt': False
    })

  amplifiers[0]['inputs'].append('0')

  while not thruster_signal:
    for i in range(len(test_sequence)):
      amplifiers[i] = run_program(amplifiers[i])

      if i == len(test_sequence) - 1 and amplifiers[i]['did_halt']:
        thruster_signal = int(amplifiers[i]['outputs'][-1])
      else:
        next_amplifier = (i + 1) % len(test_sequence)
        amplifiers[next_amplifier]['inputs'].append(amplifiers[i]['outputs'][-1])

  if thruster_signal > max_thruster_signal:
    max_thruster_signal = thruster_signal

print(max_thruster_signal)
