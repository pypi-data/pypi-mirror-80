#! python3

'''
Dummy test for FLY graph functionalities
'''

from fly.graph.graph import Graph

nodes = ["a", "b", "c", "d", "e", "f"]

graph = Graph().addNodes(nodes).addEdge("a", "b").addEdge("a", "c").addEdge("b", "c").addEdge("b", "e").addEdge("c", "d").addEdge("d", "e")

print("\nUNDIRECTED GRAPH")
print(f"Undirected graph: {graph}")
print(f"Graph nodes: {graph.nodeSet()}")
print(f"Number of nodes: {graph.numNodes()}")
print(f"Node 'a' is in graph: {graph.hasNode('a')}")
print(f"Node 'g' is in graph: {graph.hasNode('g')}")
print(f"Graph edges: {graph.edgeSet()}")
print(f"Number of edges: {graph.numEdges()}")
print(f"Edge ('a', 'c') is in graph: {graph.hasEdge('a', 'c')}")
print(f"Edge ('a', 'f') is in graph: {graph.hasEdge('a', 'f')}")
print(f"Degree of node 'a': {graph.nodeDegree('a')}")
print(f"Degree of node 'f': {graph.nodeDegree('f')}")
print(f"Neighbourhood of 'a': {graph.neighbourhood('a')}")

# edge manipulation
edge = graph.getEdge("d", "e")
print(f"Edge: {edge}")
print ("Change edge target from 'e' to 'a'")
graph.setEdgeTarget(edge, "a")
print(f"Graph: {graph}")
edge = graph.getEdge("d", "a")
print(f"Edge: {edge}")
print("Change edge source from 'd' to 'c'")
graph.setEdgeSource(edge, "c")
print(f"Graph: {graph}")

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
print(f"Weighted graph: {wgraph}")

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

print(f"In degree of node 'b': {digraph.nodeInDegree('b')}")
print(f"Out degree of node 'b': {digraph.nodeOutDegree('b')}")
print(f"In star of 'b': {digraph.nodeInEdges('b')}")
print(f"Out star of 'b': {digraph.nodeOutEdges('b')}")

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

print("\nBREADTH FIRST SEARCH")
root_node = "a"
print(f"BFS nodes order: {graph.bfsNodes(root_node)}")
print(f"BFS edges: {graph.bfsEdges(root_node)}")
print(f"BFS tree: {graph.bfsTree(root_node)}")

print("\nDEPTH FIRST SEARCH")
print(f"DFS nodes order: {graph.dfsNodes(root_node)}")
print(f"DFS edges: {graph.dfsEdges(root_node)}")
print(f"DFS tree: {graph.dfsTree(root_node)}")

print("\nCONNECTIVITY")
graph.addNode("g")
graph.addEdge("f", "g")
print(f"Graph: {graph}")
print(f"Graph is connected: {graph.isConnected()}")
print(f"Number of connected components: {graph.numberConnectedComponents()}")
print(f"Connected components: [{graph.connectedComponents()}]")
print(f"Connected component of 'a': {graph.nodeConnectedComponent('a')}")
print(f"Connected component of 'f': {graph.nodeConnectedComponent('f')}")
subgraphs = graph.connectedSubgraphs()
i = 0
for subgraph in subgraphs:
    print(f"Subgraph {i}: {subgraph}")
    i += 1
del subgraphs
#print(f"Connected subgraphs: {graph.connected_subgraphs()}")
print("Removing 'f' and 'g'...")
graph.removeNode("f")
graph.removeNode("g")
print(f"Graph: {graph}")
print(f"Graph is connected: {graph.isConnected()}")
print(f"Number of connected components: {graph.numberConnectedComponents()}")

print("\nSTRONG CONNECTIVITY")
digraph.addEdge("d", "a")
digraph.addNode("f")
digraph.addEdge("e", "f")
digraph.addEdge("f", "e")
print(f"Directed graph: {digraph}")
print(f"Digraph is strongly connected: {digraph.isStronglyConnected()}")
print(f"Connected components: [{digraph.stronglyConnectedComponents()}]")
subgraphs = digraph.stronglyConnectedSubgraphs()
i = 0
for subgraph in subgraphs:
    print(f"Strong subgraph {i}: {subgraph}")
    i += 1
del subgraphs
print("Removing (a, c) and adding (c, a) and (e, c)...")
digraph.removeEdge("a", "c")
digraph.addEdge("c", "a")
digraph.addEdge("e", "c")
print(f"Directed graph: {digraph}")
print(f"Digraph is strongly connected: {digraph.isStronglyConnected()}")


print("\nDAG & TOPOLOGICAL SORT")
digraph.removeNode("f")
digraph.removeEdge("d", "a")
print(f"Digraph: {digraph}")
print(f"Digraph is DAG: {digraph.isDAG()}")
print("Removing edges (c, a) and (e, c)...")
digraph.removeEdge("c", "a")
digraph.removeEdge("e", "c")
print(f"Digraph: {digraph}")
print(f"Digraph is DAG: {digraph.isDAG()}")
print(f"Topological sorting: {digraph.topologicalSort()}")

print("\nMINIMUM SPANNING TREE")
print(f"MST of weighted graph: {wgraph.getMST()}")

print("\nLOWEST COMMON ANCESTOR")
print(f"Lowest common ancestor of nodes 'd' and 'b': {digraph.getLCA('d', 'b')}")
