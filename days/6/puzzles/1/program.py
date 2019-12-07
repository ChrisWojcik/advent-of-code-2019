import sys

tree = {}

for line in sys.stdin:
  orbitee, orbiter = line.strip().split(')', 1)

  tree.setdefault(orbitee, {})
  tree.setdefault(orbiter, {})
  tree[orbitee].setdefault('parent', None)
  tree[orbitee].setdefault('children', set())
  tree[orbiter].setdefault('parent', None)
  tree[orbiter].setdefault('children', set())

  tree[orbitee]['children'].add(orbiter)
  tree[orbiter]['parent'] = orbitee

def count_edges_to_root(start_node, tree):
  num_edges = 0
  node = start_node

  while tree[node]['parent'] != None:
    node = tree[node]['parent']
    num_edges += 1

  return num_edges

num_orbits = 0

for node in tree:
  num_orbits += count_edges_to_root(node, tree)

print(num_orbits)
