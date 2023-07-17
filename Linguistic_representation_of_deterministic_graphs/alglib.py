""" IAMM - Graphs - ASP Work """

from typing import Tuple, List, Union, Dict
from math import ceil, sqrt
import random
import copy
import networkx as nx               # type: ignore


def ar_nodes(graph: nx.Graph) -> nx.Graph:
    """ reduction algorithm AR """

    def find_neighbours_with_the_same_labels(nghb: List, lbls: List) -> Dict:
        element_positions: Dict = {}
        for index, element in enumerate(lbls):
            if element in element_positions:
                element_positions[element].append(nghb[index])
            else:
                element_positions[element] = [nghb[index]]
        equal_elements: Dict = {
            element: positions for element,
            positions in element_positions.items() if len(positions) > 1
        }
        return equal_elements

    G_ = copy.deepcopy(graph)
    trigger = True
    while trigger:
        trigger = False
        for node in G_.nodes:
            neighbors = list(G_.neighbors(node))
            labels = [G_.nodes[id]['label'] for id in neighbors]
            equals_labels = find_neighbours_with_the_same_labels(neighbors, labels)
            if equals_labels:
                for key_lbl, neighbours_ids in equals_labels.items():
                    not_changeble_node = min(neighbours_ids)
                    neighbours_ids.remove(not_changeble_node)
                    for vertex in neighbours_ids:
                        nghb_of_del_node = list(G_.neighbors(vertex))
                        nghb_of_del_node.remove(node)
                        for v_node in nghb_of_del_node:
                            G_.add_edge(v_node, not_changeble_node)
                        G_.remove_node(vertex)
                trigger = True
                break
    return G_


def ap_graph(C:tuple, L:tuple, x_='1') -> Union[nx.Graph, str]:
    """ build graph on pair of words, algorithm AP """

    def random_color():
        red = random.randint(100, 255)
        green = random.randint(100, 255)
        blue = random.randint(100, 255)
        hex_color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
        return hex_color

    def counter():
        if not hasattr(counter, 'count'):
            counter.count = 0
        counter.count += 1
        return counter.count

    def get_all_leaf_nodes_from_graph(G: nx.Graph) -> dict:
        leaf_nodes = [node for node, degree in G.degree() if degree == 1]
        node_labels = [G.nodes[id]['label'] for id in leaf_nodes]
        return dict(zip(leaf_nodes, node_labels))

    # STEP 0
    q: Dict = {}
    trash: Dict = {}
    root = 0
    check_leaf_node = None
    G = nx.Graph()
    G.add_node(root, label=x_, color="red")

    # STEP 1
    for word in C:
        for i, l in enumerate(word[1:-1], start=1):
            #print("C1: ", i, l)
            custom_id = counter()
            #print("C1: ", id)
            G.add_node(custom_id, label=l, color=random_color())
            if i == 1:
                G.add_edge(root, custom_id)
            else:
                G.add_edge(custom_id - 1, custom_id)
            if i == len(word) - 2:
                G.add_edge(custom_id, root)
        G = ar_nodes(G)

    # STEP 2
    q = get_all_leaf_nodes_from_graph(G)
    print(q)

    # STEP 3
    for word in L:
        for i, l in enumerate(word[1:], start=1):
            node_id = counter()
            G.add_node(node_id, label=l, color=random_color())
            if i == 1:
                G.add_edge(root, node_id)
            else:
                G.add_edge(node_id - 1, node_id)
            if i == len(word) - 1:
                check_leaf_node = node_id
        G = ar_nodes(G)
        if G.has_node(check_leaf_node):
            if G.degree(check_leaf_node) != 1:
                raise ValueError("Incorrect data. Graph is not exists!")
        all_leafs = get_all_leaf_nodes_from_graph(G)
        for key_id, val_label in all_leafs.items():
            if val_label != word[-1] \
                    and key_id not in q and key_id not in trash:
                q[key_id] = val_label
            else:
                trash[key_id] = val_label

    # STEP 4
    for key_id, val_label in q.items():
        all_paths = list(nx.all_simple_paths(G, source=root, target=key_id))
        all_paths_labels = ["".join([G.nodes[id]['label'] for id in path]) for path in all_paths]
        print(key_id, val_label, all_paths_labels)
        checked = False
        for w in all_paths_labels:
            for p in L:
                if w in p:
                    checked = True
        if not checked:
            print("Incorrect data. Graph is not exists!")

    return G


def ak_pair(graph: nx.Graph) -> Union[Tuple[List[str], List[str]], int, str]:
    """ get canonical pair of words, algorithm AK """

    if len(graph.nodes) == 0:
        return 0
    if len(graph.nodes) == 1:
        try:
            return graph.nodes[0]['label']
        except KeyError:
            return list(graph.nodes)[0]

    root = list(graph.nodes)[0]
    sigma_g: List = []
    lambda_g: List = []
    reachability_basis: Dict = {}

    # Find reachability basis in the graph and fill lambda_g
    ms_tree = nx.minimum_spanning_tree(graph)
    for node in ms_tree.nodes:
        node_path_id = nx.shortest_path(ms_tree, source=root, target=node)
        node_path_labels = [ms_tree.nodes[id]['label'] for id in node_path_id]
        reachability_basis[''.join(node_path_labels)] = node_path_id
        if graph.degree(node) == 1 and node != root:
            lambda_g.append(''.join(node_path_labels))

    # create ni var as reachibility basis list without lambda_g values
    ni = [w for w in reachability_basis if w not in lambda_g]
    ni.pop(root)

    # Find cycles by ni and fill sigma_g
    for i, p in enumerate(ni):
        for q in ni[i+1:]:
            if p not in q[:len(p)]:
                if graph.has_edge(
                    reachability_basis[p][-1],
                    reachability_basis[q][-1]
                ) is False:
                    continue
                pqr = p + q[::-1]
                qpr = q + p[::-1]
                if pqr < qpr:
                    sigma_g.append(pqr)
                else:
                    sigma_g.append(qpr)

    return (sigma_g, lambda_g)


def get_pair_metrics(n: int, m: int) -> Dict:
    """ find canonical pair metrics """
    mat = ceil(3/2 + sqrt(9/4 - 2 * n + 2 * m))
    result = 2 * (m - n + 1) * (n - mat + 2)
    return {"mat": mat, "result": result}
