import sys

memory = sys.stdin.read().split(',')

memory[1] = '12'
memory[2] = '2'

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
    break

  i += 4

print(memory[0])
