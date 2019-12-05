import sys
import math

fuel_required = 0

for line in sys.stdin:
  mass = int(line)

  fuel_required += math.floor(mass / 3) - 2

print(fuel_required)
