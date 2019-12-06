import sys

TARGET_OUTPUT = '19690720'

initial_memory = sys.stdin.read().split(',')

def run_program(memory, noun, verb):
  memory[1] = noun
  memory[2] = verb

  i = 0

  while i < len(memory):
    op_code = int(memory[i])
    input1_pos = int(memory[i+1])
    input2_pos = int(memory[i+2])
    result_pos = int(memory[i+3])
    input1 = int(memory[input1_pos])
    input2 = int(memory[input2_pos])

    if op_code == 1:
      memory[result_pos] = str(input1 + input2)
    elif op_code == 2:
      memory[result_pos] = str(input1 * input2)
    else:
      return memory[0]

    i += 4

params = [(noun,verb) for noun in range(0,100) for verb in range(0,100)]

for noun,verb in params:
  output = run_program(initial_memory.copy(), str(noun), str(verb))

  if output == TARGET_OUTPUT:
    print(100 * noun + verb)
