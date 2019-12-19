import sys

NUM_PHASES = 100
CHARACTERS_TO_KEEP = 8

input_string = sys.stdin.read()
input_digits = [int(i) for i in input_string]
input_length = len(input_digits)

def generate_pattern(n):
  offset_by_1 = True
  base_pattern = [0, 1, 0, -1]
  base_pattern_index = 0

  while True:
    repeats = n if offset_by_1 else n + 1

    for _ in range(repeats):
      yield base_pattern[base_pattern_index]

    offset_by_1 = False
    base_pattern_index = (base_pattern_index + 1) % 4

for _ in range(NUM_PHASES):
  output_digits = []

  for output_position in range(input_length):
    sum_for_position = 0
    pattern = generate_pattern(output_position)

    for i in range(input_length):
      sum_for_position += (input_digits[i] * next(pattern))

    output_digits.append(abs(sum_for_position) % 10)

  input_digits = output_digits

print(''.join([str(i) for i in input_digits])[0:CHARACTERS_TO_KEEP])
