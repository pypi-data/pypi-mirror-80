#! python3

'''
Dummy test for FLY Graph IO functionality
'''

# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from urllib.request import urlopen
from fly.graph.graph import Graph

nodes = ["a", "b", "c", "d", "e", "f"]

print("\nUNDIRECTED GRAPH")
graph = Graph(node_set=nodes)
graph.addEdge("a", "b")
graph.addEdge("a", "c")
graph.addEdge("b", "c")
graph.addEdge("b", "e")
graph.addEdge("c", "d")
graph.addEdge("d", "e")
print(f"Undirected graph: {graph}")

print("\nREPRESENTATION")
print(f"Graph representation: {repr(graph)}")
repr_graph = eval(repr(graph))
print(f"Graph from representation: {repr_graph} of type {type(repr_graph)}")
