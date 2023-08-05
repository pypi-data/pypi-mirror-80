import unittest

from graph.graph import Graph


class TestStack(unittest.TestCase):
    def setUp(self):
        self.attr_key = 'w'
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
        graph_adj_list_attr = {
            0: {1:{self.attr_key: 1.0}, 2:{self.attr_key: 0.5}, 3:{self.attr_key: 9.7}},
            1: {4:{self.attr_key: 4.2}, 5:{self.attr_key: 4.3}},
            2: {5:{self.attr_key: 8.8}},
            3: {6:{self.attr_key: 1.1}},
            4: {6:{self.attr_key: 4.3}},
            5: {7:{self.attr_key: 0.1}},
            6: {6:{self.attr_key: 9.7}}
        }
        self.graph = Graph[int](graph_adj_list, directed=False)
        self.digraph = Graph[int](digraph_adj_list, directed=True)
        self.graph_attr = Graph[int](graph_adj_list_attr, directed=False)

    def test_construct_graph(self):
        self.assertEqual(self.graph[0], {1: {}, 2: {}, 3: {}})
        self.assertEqual(self.graph[1], {0: {}, 4: {}, 5: {}})
        self.assertEqual(self.graph[2], {0: {}, 5: {}})
        self.assertEqual(self.graph[3], {0: {}, 6: {}})
        self.assertEqual(self.graph[4], {1: {}, 6: {}})
        self.assertEqual(self.graph[5], {1: {}, 2: {}, 7: {}})
        self.assertEqual(self.graph[6], {3: {}, 4: {}, 6: {}})
        self.assertEqual(self.graph[7], {5: {}})

    def test_construct_digraph(self):
        self.assertEqual(self.digraph[0], {1:{}, 2:{}, 3:{}})
        self.assertEqual(self.digraph[1], {0:{}, 4:{}, 5:{}})
        self.assertEqual(self.digraph[2], {5:{}})
        self.assertEqual(self.digraph[3], {0:{}, 6:{}})
        self.assertEqual(self.digraph[4], {1:{}, 6:{}})
        self.assertEqual(self.digraph[5], {7:{}})
        self.assertEqual(self.digraph[6], {})
        self.assertEqual(self.digraph[7], {7:{}})

    def test_construct_graph_attributes(self):
        self.assertEqual(self.graph_attr[0], {1:{self.attr_key: 1.0}, 2: {self.attr_key: 0.5}, 3:{self.attr_key: 9.7}})
        self.assertEqual(self.graph_attr[1], {0:{self.attr_key: 1.0}, 4:{self.attr_key: 4.2}, 5:{self.attr_key: 4.3}})
        self.assertEqual(self.graph_attr[2], {0:{self.attr_key: 0.5}, 5:{self.attr_key: 8.8}})
        self.assertEqual(self.graph_attr[3], {0:{self.attr_key: 9.7}, 6:{self.attr_key: 1.1}})
        self.assertEqual(self.graph_attr[4], {1:{self.attr_key: 4.2}, 6:{self.attr_key: 4.3}})
        self.assertEqual(self.graph_attr[5], {1:{self.attr_key: 4.3}, 2:{self.attr_key: 8.8}, 7:{self.attr_key: 0.1}})
        self.assertEqual(self.graph_attr[6], {3:{self.attr_key: 1.1}, 4:{self.attr_key: 4.3}, 6:{self.attr_key: 9.7}})
        self.assertEqual(self.graph_attr[7], {5:{self.attr_key: 0.1}})

    def test_add_edge_graph(self):
        self.graph.add_edge(2, 3)
        self.assertEqual(self.graph[2], {0:{}, 3:{}, 5:{}})
        self.assertEqual(self.graph[3], {0:{}, 2:{}, 6:{}})
    
    def test_add_edge_digraph(self):
        self.digraph.add_edge(2, 3)
        self.assertEqual(self.digraph[2], {3:{}, 5:{}})
        self.assertEqual(self.digraph[3], {0:{}, 6:{}})

    def test_add_edge_graph_attr(self):
        test_attr_key = 'clr'
        test_attr_val = 'R'
        self.graph_attr.add_edge(2, 3, {self.attr_key: 7.7, test_attr_key: test_attr_val})
        self.assertEqual(self.graph_attr[2], {0:{self.attr_key: 0.5}, 3: {self.attr_key: 7.7, test_attr_key: test_attr_val}, 5:{self.attr_key: 8.8}})
        self.assertEqual(self.graph_attr[3], {0:{self.attr_key: 9.7}, 2: {self.attr_key: 7.7, test_attr_key: test_attr_val}, 6:{self.attr_key: 1.1}})

    def test_add_edge_existing_graph(self):
        self.assertRaises(Exception, self.graph.add_edge, 0, 1)
        self.assertRaises(Exception, self.graph.add_edge, 1, 0)

    def test_add_edge_existing_digraph(self):
        self.assertRaises(Exception, self.digraph.add_edge, 0, 1)

    def test_add_edge_loop_graph(self):
        self.graph.add_edge(0, 0)
        self.assertEqual(self.graph[0], {0:{}, 1:{}, 2:{}, 3:{}})
    
    def test_add_edge_loop_digraph(self):
        self.digraph.add_edge(0, 0)
        self.assertEqual(self.digraph[0], {0:{}, 1:{}, 2:{}, 3:{}})

    def test_add_edge_new_u_vertex_graph(self):
        self.graph.add_edge(8, 0)
        self.assertEqual(self.graph[0], {1:{}, 2:{}, 3:{}, 8:{}})
        self.assertEqual(self.graph[8], {0:{}})

    def test_add_edge_new_u_vertex_digraph(self):
        self.digraph.add_edge(8, 0)
        self.assertEqual(self.digraph[0], {1:{}, 2:{}, 3:{}})
        self.assertEqual(self.digraph[8], {0:{}})

    def test_add_edge_new_v_vertex_graph(self):
        self.graph.add_edge(0, 8)
        self.assertEqual(self.graph[0], {1:{}, 2:{}, 3:{}, 8:{}})
        self.assertEqual(self.graph[8], {0:{}})

    def test_add_edge_new_v_vertex_digraph(self):
        self.digraph.add_edge(0, 8)
        self.assertEqual(self.digraph[0], {1:{}, 2:{}, 3:{}, 8:{}})
        self.assertEqual(self.digraph[8], {})

    def test_add_edges_graph(self):
        self.graph.add_edges(adj_list={
            0: {4: {}, 6: {}},
            2: {3: {}}})
        self.assertEqual(self.graph[0], {1:{}, 2:{}, 3:{}, 4:{}, 6:{}})
        self.assertEqual(self.graph[2], {0:{}, 3:{}, 5:{}})
        self.assertEqual(self.graph[3], {0:{}, 2:{}, 6:{}})
        self.assertEqual(self.graph[4], {0:{}, 1:{}, 6:{}})

    def test_len(self):
        self.assertEqual(len(self.graph), 8)
        self.assertEqual(len(self.digraph), 8)

    def test_delete_vertex_graph(self):
        del self.graph[0]
        self.assertRaises(KeyError, self.graph.__getitem__, 0)
        self.assertEqual(self.graph[1], {4:{}, 5:{}})
        self.assertEqual(self.graph[2], {5:{}})
        self.assertEqual(self.graph[3], {6:{}})

    def test_delete_vertex_digraph(self):
        del self.digraph[0]
        self.assertRaises(KeyError, self.digraph.__getitem__, 0)
        self.assertEqual(self.digraph[1], {4:{}, 5:{}})
        self.assertEqual(self.digraph[3], {6:{}})

    def test_delete_missing_vertex_graph(self):
        self.assertRaises(KeyError, self.graph.__delitem__, 8)

    def test_delete_missing_vertex_digraph(self):
        self.assertRaises(KeyError, self.digraph.__delitem__, 8)
        