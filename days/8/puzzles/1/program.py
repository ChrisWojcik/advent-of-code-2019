import sys

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT

all_layers = sys.stdin.read()
fewest_0_digits = float('inf')
result = 0

for i in range(0, len(all_layers), LAYER_SIZE):
  layer = all_layers[i:i+LAYER_SIZE]
  num_0_digits = 0
  num_1_digits = 0
  num_2_digits = 0

  for digit in layer:
    if digit == '0':
      num_0_digits += 1
    if digit == '1':
      num_1_digits += 1
    if digit == '2':
      num_2_digits += 1

  if num_0_digits < fewest_0_digits:
    fewest_0_digits = num_0_digits
    result = num_1_digits * num_2_digits

print(result)
