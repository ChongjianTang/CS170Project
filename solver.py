import copy
import random
import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import os


def get_leaves(mst):
    leaves = []
    for vertex in mst.nodes:
        if mst.degree[vertex] == 1:
            leaves.append(vertex)
    return leaves


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    # if no edges, return G
    if not nx.number_of_edges(G):
        return G

    # Version 1.0

    mst = nx.minimum_spanning_tree(G)
    best_G = copy.deepcopy(mst)
    best_cost = average_pairwise_distance_fast(best_G)
    loop_num = 2
    while loop_num > 1:
        leaves = get_leaves(mst)
        leaves.sort(reverse=True, key=lambda x: list(mst.edges(x, data='weight'))[0][2])
        loop_num = 0
        need_more_removal = True
        while need_more_removal:
            need_more_removal = False
            new_leaves = []
            for leaf in leaves:
                edges = mst.edges(leaf, data='weight')
                if edges:
                    e = list(edges)[0]
                    mst.remove_node(leaf)
                    if not nx.is_dominating_set(G, mst.nodes):
                        mst.add_node(leaf)
                        mst.add_edge(e[0], e[1], weight=e[2])
                        new_leaves.append(leaf)
                    else:
                        cost = average_pairwise_distance_fast(mst)
                        if cost < best_cost:
                            best_G = copy.deepcopy(mst)
                            best_cost = cost
                        need_more_removal = True
            leaves = new_leaves
            loop_num += 1
    mst = best_G

    # Version 2.0

    mst_decreased = nx.minimum_spanning_tree(G)
    loop_num = 2
    while loop_num > 1:
        leaves = get_leaves(mst_decreased)
        leaves.sort(reverse=True, key=lambda x: list(mst_decreased.edges(x, data='weight'))[0][2])
        loop_num = 0
        need_more_removal = True
        while need_more_removal:
            need_more_removal = False
            new_leaves = []
            for leaf in leaves:
                edges = mst_decreased.edges(leaf, data='weight')
                if edges:
                    e = list(edges)[0]
                    cost = average_pairwise_distance_fast(mst_decreased)
                    mst_decreased.remove_node(leaf)
                    new_cost = average_pairwise_distance_fast(mst_decreased)
                    if new_cost > cost or not nx.is_dominating_set(G, mst_decreased.nodes):
                        mst_decreased.add_node(leaf)
                        mst_decreased.add_edge(e[0], e[1], weight=e[2])
                        new_leaves.append(leaf)
                    else:
                        need_more_removal = True
            leaves = new_leaves
            loop_num += 1

    print("mst = " + str(average_pairwise_distance_fast(mst)))
    print("mst_decreased = " + str(average_pairwise_distance_fast(mst_decreased)))

    if average_pairwise_distance_fast(mst)<average_pairwise_distance_fast(mst_decreased):
        return mst
    else:
        return mst_decreased


# To run: python3 solver.py inputs


if __name__ == '__main__':
    assert len(sys.argv) == 2
    p = sys.argv[1]
    assert os.path.isdir(p)
    for path in os.listdir(p):
        G = read_input_file(p + '/' + path)
        T = solve(G)
        assert is_valid_network(G, T)
        print("Average pairwise distance: {}".format(average_pairwise_distance_fast(T)))
        out = 'outputs/' + path[:len(path) - 3] + '.out'
        write_output_file(T, out)
