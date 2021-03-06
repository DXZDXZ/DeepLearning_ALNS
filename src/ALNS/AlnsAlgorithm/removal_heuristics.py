import copy

import numpy as np
import networkx as nx

import src.ALNS.settings as settings

degree_of_destruction = settings.DEGREE_OF_DESTRUCTION
DETERMINISM = settings.DETERMINISM


def is_served_by_same_vehicle(state, node, second_node):
    successor = next(state.instance.neighbors(node))
    while not (state.instance.nodes[successor]['isDepot']):
        if successor == second_node:
            return 1
        successor = next(state.instance.neighbors(successor))

    predecessor = next(state.instance.predecessors(node))
    while not (state.instance.nodes[predecessor]['isDepot']):
        if predecessor == second_node:
            return 1
        predecessor = next(state.instance.predecessors(predecessor))

    return 0


def compute_relatedness(state, node, second_node):
    return 1 / (state.distances[node][second_node] + is_served_by_same_vehicle(state, node, second_node))


def rank_nodes_using_relatedness(state, list_of_nodes, node):
    relatedness_values = {}
    for other_node in list_of_nodes:
        relatedness_values[other_node] = compute_relatedness(state, node, other_node)

    ranked_nodes = sorted(relatedness_values, key=relatedness_values.get)

    return ranked_nodes


def compute_number_of_clients_to_remove(state):
    number_of_clients_to_remove = np.random.randint(min(state.size, 1), min(state.size * degree_of_destruction, 100))
    return number_of_clients_to_remove


def select_related_nodes(state, random_state):
    # We create a list containing the indexes of the client nodes
    # Their indexes start after their indexes of the depots by construction
    list_of_nodes = [i + state.number_of_depots for i in range(state.size)]

    selected_nodes = []
    first_deleted_node = random_state.choice(list_of_nodes, size=None, replace=False)
    selected_nodes.append(first_deleted_node)
    list_of_nodes.remove(first_deleted_node)

    number_of_clients_to_remove = compute_number_of_clients_to_remove(state)

    for i in range(number_of_clients_to_remove - 1):
        random_deleted_node = random_state.choice(selected_nodes, size=None, replace=False)
        sorted_list_of_nodes = rank_nodes_using_relatedness(state, list_of_nodes, random_deleted_node)
        random_number = random_state.random()

        deleted_node = sorted_list_of_nodes[int(len(sorted_list_of_nodes) * (random_number ** DETERMINISM))]
        selected_nodes.append(deleted_node)
        list_of_nodes.remove(deleted_node)

    return selected_nodes


def remove_nodes(state, nodes_to_destroy):
    destroyed_state = state.copy()  # deepcopy
    # The removal of a node N_i consists in removing the edge (N_i-1, N_i) and (N_i, N_i+1)
    # and adding the edge (N_i-1, N_i+1)
    for node in nodes_to_destroy:
        # We find the neighboring nodes
        next_node = next(destroyed_state.instance.neighbors(node))
        previous_node = next(destroyed_state.instance.predecessors(node))
        destroyed_state.instance.remove_edge(previous_node, node)
        destroyed_state.instance.remove_edge(node, next_node)
        # Avoiding useless routes
        if next_node != previous_node:
            destroyed_state.instance.add_edge(previous_node, next_node)

    # We collect the value of the objective function and the existing edges in case we want stats
    if state.collect_alns_statistics:
        state.statistics['destroyed_nodes'].append(nodes_to_destroy)
        list_of_edges = nx.to_edgelist(destroyed_state.instance)
        state.statistics['list_of_edges'].append(list_of_edges)

    return destroyed_state


def removal_heuristic(state, random_state):
    # We choose the clients we want to remove from the instance
    nodes_to_destroy = select_related_nodes(state, random_state)

    return remove_nodes(state, nodes_to_destroy)
