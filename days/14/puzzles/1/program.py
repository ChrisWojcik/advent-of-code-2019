import sys
import math

reactions = {}

for line in sys.stdin:
  inputs, output = line.strip().split('=>')
  inputs = list(map(lambda _: tuple(_.split(' ')), inputs.strip().split(', ')))
  inputs = list(map(lambda _: (int(_[0]), _[1]), inputs))
  output = tuple(output.strip().split(' '))
  output = (int(output[0]), output[1])

  reactions[output[1]] = (output[0], inputs)

def produce(product, amount, factory):
  amount_required = amount

  if factory[product] > amount_required:
    factory[product] -= amount_required
    amount_required = 0
  elif amount_required > factory[product]:
    amount_required -= factory[product]
    factory[product] = 0
  else:
    amount_required = 0
    factory[product] = 0

  if amount_required == 0:
    return (0, factory)

  if product == 'ORE':
    return (amount_required, factory)
  else:
    amount_produced_per_reaction, reactants = reactions[product]
    reactions_required = math.ceil(amount_required / amount_produced_per_reaction)

    ore_required = 0

    for reactant in reactants:
      amount_produced_of_chemical, chemical = reactant
      ore_used, factory = produce(chemical, amount_produced_of_chemical * reactions_required, factory)
      ore_required += ore_used

    amount_produced = amount_produced_per_reaction * reactions_required
    factory[product] += amount_produced - amount_required

    return (ore_required, factory)

factory = { output:0 for output in reactions }
factory['ORE'] = 0

ore_required, factory = produce('FUEL', 1, factory)
print(ore_required)
