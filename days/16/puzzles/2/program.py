import sys
from itertools import accumulate

NUM_PHASES = 100
CHARACTERS_TO_KEEP = 8

original_input_string = sys.stdin.read()
offset = int(original_input_string[:7])
input_string = original_input_string * 10000
input_digits = [int(i) for i in input_string[offset:][::-1]]

for _ in range(NUM_PHASES):
  input_digits = [n % 10 for n in accumulate(input_digits)]

message = ''.join([str(i) for i in input_digits])[::-1][:CHARACTERS_TO_KEEP]
print(message)
