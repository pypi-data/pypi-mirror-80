#! python3

'''
Dummy test for metrics in FLY graph
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

print("\nUNDIRECTED GRAPH")
print(f"Undirected graph: {graph}")
print(f"Graph nodes: {graph.nodeSet()}")
print(f"Graph edges: {graph.edgeSet()}")
print(f"Shortest path from 'a' to 'c': {graph.shortestPath('a', 'c')}")
print(f"Shortest path from 'a' to 'd': {graph.shortestPath('a', 'd')}")
print(f"Shortest path from 'a' to 'f': {graph.shortestPath('a', 'f')}")
graph.removeNode("f")
print(f"Graph diameter: {graph.getDiameter()}")
print(f"Graph radius: {graph.getRadius()}")
graph.addNode("f")
print(f"Clustering coefficient of node 'a': {graph.getNodeClusteringCoefficient('a')}")
print(f"Clustering coefficient of node 'b': {graph.getNodeClusteringCoefficient('b')}")
print(f"Average clustering coefficient for graph: {graph.getAverageClusteringCoefficient()}")
print(f"Global clustering coefficient for graph: {graph.getGlobalClusteringCoefficient()}")
print(f"Number of triangles for node 'a': {graph.getNumberOfTriangles('a')}")
print(f"Total number of triangles in graph: {graph.getNumberOfTriangles()}")
print(f"Number of triplets for node 'a': {graph.getNumberOfTriplets('a')}")
print(f"Total number of triplets in graph: {graph.getNumberOfTriplets()}")
