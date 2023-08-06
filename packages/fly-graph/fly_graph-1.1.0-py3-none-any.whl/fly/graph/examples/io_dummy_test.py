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
graph = Graph()
graph.addNodes(nodes)
graph.addEdge("a", "b")
graph.addEdge("a", "c")
graph.addEdge("b", "c")
graph.addEdge("b", "e")
graph.addEdge("c", "d")
graph.addEdge("d", "e")
print(f"Undirected graph: {graph}")

print("\nWEIGHTED GRAPH")
wgraph = Graph(is_weighted=True)
wgraph.addNodes(nodes)
wgraph.removeNode("f")
wgraph.addEdge("a", "b")
wgraph.addEdge("a", "c")
wgraph.addEdge("b", "c")
wgraph.addEdge("b", "e")
wgraph.addEdge("c", "d")
wgraph.addEdge("d", "e")
wgraph.addEdge("a", "e")
wgraph.addEdge("b", "d")
wgraph.setEdgeWeight("a", "b", 2.0)
print(f"Weight of edge ('a', 'b'): {wgraph.getEdgeWeight('a', 'b')}")
wgraph.setEdgeWeight("a", "c", 3.0)
wgraph.setEdgeWeight("b", "c", 1.0)
wgraph.setEdgeWeight("b", "e", 4.0)
wgraph.setEdgeWeight("c", "d", 2.0)
wgraph.setEdgeWeight("d", "e", 5.0)
wgraph.setEdgeWeight("a", "e", 2.0)
wgraph.setEdgeWeight("b", "d", 3.0)
print(f"Weighted graph: {graph}")

print("\nDIRECTED GRAPH")
digraph = Graph(is_directed=True)
digraph.addNodes(nodes)
digraph.removeNode("f")
digraph.addEdge("a", "b")
digraph.addEdge("a", "c")
digraph.addEdge("b", "c")
digraph.addEdge("b", "e")
digraph.addEdge("c", "d")
digraph.addEdge("d", "e")
print(f"Directed graph: {digraph}")

print("\nDIRECTED WEIGHTED GRAPH")
wdgraph = Graph(is_directed=True, is_weighted=True)
wdgraph.addNodes(nodes)
wdgraph.removeNode("f")
wdgraph.addEdge("a", "b")
wdgraph.addEdge("a", "c")
wdgraph.addEdge("b", "c")
wdgraph.addEdge("b", "e")
wdgraph.addEdge("c", "d")
wdgraph.addEdge("d", "e")
wdgraph.addEdge("a", "e")
wdgraph.addEdge("b", "d")
wdgraph.setEdgeWeight("a", "b", 2.0)
wdgraph.setEdgeWeight("a", "c", 3.0)
wdgraph.setEdgeWeight("b", "c", 1.0)
wdgraph.setEdgeWeight("b", "e", 4.0)
wdgraph.setEdgeWeight("c", "d", 2.0)
wdgraph.setEdgeWeight("d", "e", 5.0)
wdgraph.setEdgeWeight("a", "e", 2.0)
wdgraph.setEdgeWeight("b", "d", 3.0)
print(f"Weighted directed graph: {wdgraph}")

print("\nIMPORT/EXPORT")
data_path = "./fly/graph/resources/"
graph_path = data_path + "graph.py.edgelist"
dgraph_path = data_path + "digraph.py.edgelist"
wgraph_path = data_path + "wgraph.py.edgelist"
wdgraph_path = data_path + "wdgraph.py.edgelist"
igraph = Graph.importGraph(graph_path, ' ')
idgraph = Graph.importGraph(dgraph_path, ' ', is_directed=True)
iwgraph = Graph.importGraph(wgraph_path, ' ', is_weighted=True)
iwdgraph = Graph.importGraph(wdgraph_path, ' ', is_directed=True, is_weighted=True)
print(f"Undirected graph: {igraph}")
print(f"Directed graph: {idgraph}")
print(f"Weighted graph: {iwgraph}")
print(f"Weight of (a, e) edge from weighted graph: {iwgraph.getEdgeWeight('a', 'e')}")
print(f"Directed weighted graph: {iwdgraph}")
print(f"Weight of (a, e) edge from weighted directed graph: {iwdgraph.getEdgeWeight('a', 'e')}")
del igraph
del idgraph
del iwgraph
del iwdgraph
Graph.exportGraph(graph, graph_path, ' ')
Graph.exportGraph(digraph, dgraph_path, ' ')
Graph.exportGraph(wgraph, wgraph_path, ' ')
Graph.exportGraph(wdgraph, wdgraph_path, ' ')
del graph
remote_file = urlopen("https://raw.githubusercontent.com/bissim/FLY-graph/master/data/graph.py.edgelist")
graph = Graph.importGraph(remote_file, ' ')
print(f"Remote graph: {graph}")
