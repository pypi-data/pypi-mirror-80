#! python3

# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from urllib.request import urlopen
from fly.graph.graph import Graph

remote_file = urlopen("https://raw.githubusercontent.com/bissim/FLY-graph/master/data/digraph.py.edgelist")
digraph = Graph.importGraph(remote_file, ' ', is_directed=True)

print("directed graph: {0}".format(digraph))
print("Digraph type: {0}".format(type(digraph)))
# print("Digraph structure: {0}".format(dir(digraph)))
print("Digraph inner graph type: {0}".format(type(digraph.graph)))
digraph2 = Graph(is_directed=True)
print("Digraph2 inner graph type: {0}".format(type(digraph2.graph)))
