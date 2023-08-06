#! python3

from fly.graph.graph import Graph

class DiameterAndAPL():
    @classmethod
    def run(cls):
        """
        """
        _nodes = ['a', 'b', 'c', 'd', 'e']
        _num_nodes = len(_nodes)
        _graph = Graph(node_set=_nodes)
        _graph.addEdge('a', 'b')
        _graph.addEdge('a', 'c')
        _graph.addEdge('b', 'c')
        _graph.addEdge('b', 'e')
        _graph.addEdge('c', 'd')
        _exp_diameter = _graph.getDiameter()

        print(f"Graph: {_graph}")
        # longest distance is between 'd' and 'e':
        # it takes {c, d}, {b, c} and {b, e} edges
        print(f"\nExpected diameter: {_exp_diameter}")

        # by definition, graph diameter is the maximum distance
        # between two graph nodes, whathever the two graph nodes are
        # so, in order to find graph diameter, we have to build
        # a matrix of distances, useful for APL as well
        distances_length = [[0.0 for x in range(_num_nodes)] for y in range(_num_nodes)]
        for row in range(_num_nodes):
            # we only calculate upper triangle except diagonal
            for col in range(row + 1, _num_nodes):
                source = _nodes[row]
                target = _nodes[col]
                distances_length[row][col] = len(_graph.shortestPath(source, target))

        # diameter is the maximum distance in upper triangle
        diameter = distances_length[0][1]
        current = 0.0
        for row in range(1, _num_nodes):
            for col in range(row, _num_nodes):
                current = distances_length[row][col]
                if current > diameter:
                    diameter = current

        print(f"Found graph diameter: {diameter}")

        # Average Path Length (APL for its friends) is
        # the average length of distances among nodes
        lengths_sum = 0.0
        for row in range(_num_nodes):
            for col in range(row + 1, _num_nodes):
                lengths_sum += distances_length[row][col]

        _apl = lengths_sum / ((1.0 * len(_nodes)) * (1.0 * len(_nodes) - 1.0))
        print(f"\nAverage path length: {_apl}")

if __name__ == '__main__':
    DiameterAndAPL.run()