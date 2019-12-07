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

start_node = tree['YOU']['parent']
end_node = tree['SAN']['parent']

def find_shortest_path_length(start_node, end_node):
  distances = {}
  distances[start_node] = 0
  visited_nodes = set()
  nodes_to_visit = [start_node]

  while len(nodes_to_visit) > 0:
    current_node = nodes_to_visit.pop(0)
    visited_nodes.add(current_node)
    distance_to_current_node = distances[current_node]

    children = tree[current_node]['children']
    parent = { tree[current_node]['parent'] } if tree[current_node]['parent'] != None else set()
    neighbors = children.union(parent)

    for neighbor in neighbors:
      my_distance_to_neighbor = distance_to_current_node + 1

      if (not distances.get(neighbor)) or (distances[neighbor] > my_distance_to_neighbor):
        distances[neighbor] = my_distance_to_neighbor

      if neighbor not in visited_nodes:
        nodes_to_visit.append(neighbor)

  return distances[end_node]

print(find_shortest_path_length(start_node, end_node))

