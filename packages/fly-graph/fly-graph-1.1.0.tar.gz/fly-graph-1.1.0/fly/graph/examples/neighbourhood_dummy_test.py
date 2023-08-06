#! python3

'''
Dummy test for neighbourhood in FLY graph
'''

from fly.graph.graph import Graph

graph = Graph()

nodes = ["a", "b", "c", "d", "e", "f"]

graph.addNodes(nodes)

graph.addEdge("a", "b")
graph.addEdge("a", "c")
graph.addEdge("b", "c")
graph.addEdge("b", "e")
graph.addEdge("c", "d")
graph.addEdge("d", "e")

print("\nUNDIRECTED GRAPH")
print(f"Undirected graph: {graph}")
print(f"Graph nodes: {graph.nodeSet()}")
print(f"Graph edges: {graph.edgeSet()}")
print(f"Neighbourhood of 'a': {graph.neighbourhood('a')}")
