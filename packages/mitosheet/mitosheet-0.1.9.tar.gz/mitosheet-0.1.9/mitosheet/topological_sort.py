#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains function for running a topological sort on a graph with 
the representation {node: set(adj nodes)}. Note that all
nodes must be in the graph, even if they have no adj nodes, and
should just have an empty set in this case.
"""

from .errors import EditError


def visit(column_evaluation_graph, node, visited, finished_order, visited_loop):
    """
    Recursive helper function for topological sort. Throws an 
    EditError('circular_reference_error') if there is a loop.
    """
    # Mark the node as visited
    visited[node] = True

    # And record we visited it during this tree of calls to visit
    visited_loop.add(node)

    for adj_node in column_evaluation_graph[node]:

        if not visited[adj_node]:
            visit(column_evaluation_graph, adj_node, visited, finished_order, visited_loop)
        elif adj_node in visited_loop:
            # If we have visited this node in this subtree, there is a loop
            raise EditError('circular_reference_error')

    # Remove so we can visit again from elsewhere
    visited_loop.remove(node)
    # And mark this node as finished
    finished_order.append(node)

def topological_sort_columns(column_evaluation_graph):
    """
    Topologically sorts by DFSing the graph, recording the finish order, and
    then returning nodes in reversed finish order.
    """
    visited = {node: False for node in column_evaluation_graph}
    finish_order = []
    # Visit each node in the graph
    for node in column_evaluation_graph:
        if not visited[node]:
            # Keep track of the nodes visited during this set
            # of recursive calls, so we can detect cycles
            visited_loop = set()
            visit(
                column_evaluation_graph, 
                node, 
                visited, 
                finish_order, 
                visited_loop
            )

    # Reverse finish order for DFS == topological sort
    finish_order.reverse()
    return finish_order