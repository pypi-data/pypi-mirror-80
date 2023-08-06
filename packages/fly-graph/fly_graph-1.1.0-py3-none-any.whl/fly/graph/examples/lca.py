#! python3

from fly.graph.graph import Graph

class LowestCommonAncestor():
    @classmethod
    def run(cls):
        """
        """
        _NODES = ['a', 'b', 'c', 'd', 'e']
        _EDGES = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'e'), ('c', 'd')]
        _DAG = Graph(node_set=_NODES, edge_set=_EDGES, is_directed=True)
        _FIRST = 'd'
        _SECOND = 'e'
        _EXPECTED_LCA = _DAG.getLCA(_FIRST, _SECOND)

        print(f"Graph: {_DAG}")
        print(f"\nExpected LCA of 'd' and 'e': {_EXPECTED_LCA}")

        _DAG_R = LowestCommonAncestor.edge_reversed(_DAG)
        # print(f"Reversed graph: {_DAG_R}")
        set_first = LowestCommonAncestor.ancestors(_DAG_R, _FIRST)
        # print(f"Ancestors of '{_FIRST}': {set_first}")
        set_second = LowestCommonAncestor.ancestors(_DAG_R, _SECOND)
        # print(f"Ancestors of '{_SECOND}': {set_second}")

        common_ancestors = LowestCommonAncestor.intersect(set_first, set_second)
        # print(f"Common ancestors of '{_FIRST}' and '{_SECOND}': {common_ancestors}")

        _LEAVES = LowestCommonAncestor.find_leaves(_DAG, common_ancestors)
        # print(f"Leaves in common ancestor set: {_LEAVES}")

        _LCA = None if len(_LEAVES) == 0 else next(iter(_LEAVES))

        print(f"Found LCA of '{_FIRST}' and '{_SECOND}': {_LCA}")

    @staticmethod
    def edge_reversed(graph: object) -> object:
        """
        """
        edgeReversed = Graph(node_set=graph.nodeSet(), is_directed=True)
        _EDGES = graph.edgeSet()

        for pos in range(len(_EDGES)):
            source = graph.getEdgeSource(_EDGES[pos])
            target = graph.getEdgeTarget(_EDGES[pos])
            edgeReversed.addEdge(target, source)

        return edgeReversed

    @staticmethod
    def ancestors(graph: object, start: object) -> set:
        """
        """
        _BFS_NODES = graph.bfsNodes(start)
        return set(_BFS_NODES)

    @staticmethod
    def intersect(a: set, b: set) -> set:
        """
        """
        if len(a) < len(b):
            return a.intersection(b)
        else:
            return b.intersection(a)

    @staticmethod
    def find_leaves(digraph: object, nodes: set) -> set:
        """
        """
        leaves = set()

        for ancestor in nodes: # TODO fix
            isLeaf = True
            for edge in digraph.nodeOutEdges(ancestor):
                target = digraph.getEdgeTarget(edge)
                if target in nodes:
                    isLeaf = False
                    break
            if isLeaf:
                leaves.add(ancestor)

        return leaves

if __name__ == '__main__':
    LowestCommonAncestor.run()