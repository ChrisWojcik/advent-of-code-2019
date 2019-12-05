import sys
import math

total_fuel_required = 0

def get_fuel_required_for_module(mass):
  fuel_required = math.floor(mass / 3) - 2

  if fuel_required <= 0:
    return 0
  else:
    return fuel_required + get_fuel_required_for_module(fuel_required)

for line in sys.stdin:
  module_mass = int(line)

  total_fuel_required += get_fuel_required_for_module(module_mass)

print(total_fuel_required)
