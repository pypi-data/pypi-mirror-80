import unittest
from functools import partial

from graph_algorithms.search import dfs, bfs
from graph.graph import Graph


class TestStack(unittest.TestCase):
    def setUp(self):
        self.path = []
        # self.func = lambda node: self.path.append(node)
        def f(path, node):
            path.append(node)

        self.func = partial(f, self.path)

        graph_adj_list = {
            0: {1:{}, 2:{}, 3:{}},
            1: {4:{}, 5:{}},
            2: {5:{}},
            3: {6:{}},
            4: {6:{}},
            5: {7:{}},
            6: {6:{}}
        }
        digraph_adj_list = {
            0: {1:{}, 2:{}, 3:{}},
            1: {0:{}, 4:{}, 5:{}},
            2: {5:{}},
            3: {0:{}, 6:{}},
            4: {1:{}, 6:{}},
            5: {7:{}},
            6: {},
            7: {7:{}}
        }
        
        self.graph = Graph[int](graph_adj_list, directed=False)
        self.digraph = Graph[int](digraph_adj_list, directed=True)

    def test_dfs_graph(self):
        dfs(self.graph, 0, self.func)
        self.assertEqual(self.path, [0, 1, 4, 6, 3, 5, 2, 7])

    def test_dfs_digraph(self):
        dfs(self.digraph, 0, self.func)
        self.assertEqual(self.path, [0, 1, 4, 6, 5, 7, 2, 3])

    def test_dfs_missing_graph(self):
        self.assertRaises(KeyError, dfs, self.graph, 8, self.func)

    def test_dfs_missing_digraph(self):
        self.assertRaises(KeyError, dfs, self.digraph, 8, self.func)

    def test_bfs_graph(self):
        bfs(self.graph, 0, self.func)
        self.assertEqual(self.path, [0, 1, 2, 3, 4, 5, 6, 7])

    def test_bfs_digraph(self):
        bfs(self.digraph, 0, self.func)
        self.assertEqual(self.path, [0, 1, 2, 3, 4, 5, 6, 7])

    def test_bfs_missing_graph(self):
        self.assertRaises(KeyError, bfs, self.graph, 8, self.func)

    def test_bfs_missing_digraph(self):
        self.assertRaises(KeyError, bfs, self.digraph, 8, self.func)
