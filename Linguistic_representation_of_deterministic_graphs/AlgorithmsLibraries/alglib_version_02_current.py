""" IAMM - Graphs - ASP Work """
from typing import Tuple, List, Union, Dict
from dataclasses import dataclass
from math import ceil, sqrt
import re
import networkx as nx  # type: ignore


# =========================== HELPERS FUNCTIONS ===============================
@dataclass
class Counter:
    """ data Class for counter function """
    count: int = 0


def counter(reset: bool = False) -> int:
    """Helper for AP alg. Generates IDs for nodes."""
    if reset:
        Counter.count = 0
    else:
        Counter.count += 1
    return Counter.count


def service_error(error_message: str = "") -> ValueError:
    """helper for AP alg. Generate ValueError if Graph is not exists"""
    return ValueError("Incorrect data. Graph is not exists!\n" + error_message)


def get_leaf_nodes_from_dgraph(G: nx.Graph) -> dict:
    """helper for AP alg. for checking leafs nodes"""
    leaf_nodes = [node for node, degree in G.degree() if degree == 1]
    node_labels = [G.nodes[id]['label'] for id in leaf_nodes]
    return dict(zip(leaf_nodes, node_labels))


def find_neighbours_with_the_same_labels(nghb: List, lbls: List) -> Dict:
    """ helper for AR reduction algorithm """
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


def get_node_id_by_word(graph: nx.Graph,
                 word: str,
                 root_node: int) -> int:
    """ get last node id by label (word) path in graph """
    current_node = root_node
    for symbol in word[1:]:
        neighbors = list(graph.neighbors(current_node))
        labels = [graph.nodes[id]['label'] for id in neighbors]
        try:
            next_node = neighbors[labels.index(symbol)]
        except Exception as exc:
            raise ValueError(
                f"{exc} Invalid data. No symbol as label. Graph is not exists!"
            ) from exc
        current_node = next_node
    return current_node


def word_pair_data_validation(c_tuple: Tuple[str],
                              l_tuple: Tuple[str],
                              root: str) -> bool:
    """ rules for using a pair of words in an algorithm """
    pattern = r"(.)\1"
    if not c_tuple and not l_tuple:
        return False
    if c_tuple:
        for c_word in c_tuple:
            if c_word[0] != c_word[-1] and c_word[0] != root:
                return False
            if bool(re.search(pattern, c_word)):
                return False
    if l_tuple:
        for l_word in l_tuple:
            if l_word[0] != root:
                return False
            if bool(re.search(pattern, l_word)):
                return False
    return True


# ======================== ALGORITHMS REALIZATION =============================
def ar_nodes(graph: nx.Graph) -> nx.Graph:
    """ reduction algorithm AR """
    G_ = graph.copy()
    trigger = True
    while trigger:
        trigger = False
        for node in G_.nodes:
            neighbors = list(G_.neighbors(node))
            labels = [G_.nodes[id]['label'] for id in neighbors]
            equals_labels = find_neighbours_with_the_same_labels(neighbors, labels)
            if equals_labels:
                for neighbours_ids in equals_labels.values():
                    not_changeable_node = min(neighbours_ids)
                    neighbours_ids.remove(not_changeable_node)
                    for vertex in neighbours_ids:
                        nghb_of_del_node = list(G_.neighbors(vertex))
                        nghb_of_del_node.remove(node)
                        G_.add_edges_from((v_node, not_changeable_node)
                                          for v_node in nghb_of_del_node)
                        G_.remove_node(vertex)
                trigger = True
                break
    return G_


# @profile    # python -m memory_profiler main.py
def ap_graph(C: Tuple[str], L: Tuple[str], x_='1') -> Union[nx.Graph, str]:
    """ build graph on pair of words, algorithm AP """
    # ===================== STEP 0 initial definitions ============================
    if not word_pair_data_validation(C, L, x_):
        raise service_error()
    root = 0
    custom_id: int
    G = nx.Graph()
    G.add_node(root, label=x_)
    # ================= STEP 1 Construct the graph for C ==========================
    for c_word in C:
        for index, label in enumerate(c_word[1:-1], start=1):
            custom_id = counter()
            G.add_node(custom_id, label=label)
            if index == 1:
                G.add_edge(root, custom_id)
            else:
                G.add_edge(custom_id - 1, custom_id)
            if index == len(c_word) - 2:
                G.add_edge(custom_id, root)
        G = ar_nodes(G)
    # ======================= STEP 2 Add nodes for L ==============================
    for l_word in L:
        for index, label in enumerate(l_word[1:], start=1):
            custom_id = counter()
            G.add_node(custom_id, label=label)
            if index == 1:
                G.add_edge(root, custom_id)
            else:
                G.add_edge(custom_id - 1, custom_id)
        G = ar_nodes(G)
    # ======== STEPS 3 - 4 Check each word in L end each leaf vertex =========
    all_leafs: Dict = get_leaf_nodes_from_dgraph(G)
    if root in all_leafs:
        all_leafs.pop(root)
    for p_word_index, p_word in enumerate(L):
        checked_node: int = get_node_id_by_word(G, p_word, root)
        if G.degree(checked_node) != 1:
            print(service_error(
                f"Invalid pair. Word: {L[p_word_index]} " +
                "in the L set does not end with a leaf vertex."))
        if checked_node in all_leafs:
            all_leafs.pop(checked_node)
    if len(all_leafs) > 0:
        print(service_error(f"Vertex id/label: {all_leafs} not in scope."))
    # =========== STEP 3 Check if each word in L ends with a leaf vertex ==========
    # for p_word_index, p_word in enumerate(L):
    #     if G.degree(get_node_id_by_word(G, p_word, root)) != 1:
    #         print(service_error(f"Invalid pair. Word: {L[p_word_index]} " +
    #                             "in the L set does not end with a leaf vertex."))
    # ===================== STEP 4 check each leaf vertex =========================
    # all_leafs = get_leaf_nodes_from_dgraph(G)
    # if root in all_leafs:
    #     all_leafs.pop(root)
    # for vertex_id, vertex_label in all_leafs.items():
    #     trigger = False
    #     for checked_word in tuple(word for word in L if word.endswith(vertex_label)):
    #     #for checked_word in tuple(filter(lambda word: word.endswith(vertex_label), L)):
    #         if vertex_id == get_node_id_by_word(G, checked_word, root):
    #             trigger = True
    #     if not trigger:
    #         print(service_error(f"Vertex label: {vertex_label} not in scope.TRIGGER"))
    return G


def ac_pair(graph: nx.Graph) -> Union[Tuple[List[str], List[str]], int, str]:
    """ get canonical pair of words, algorithm AK """
    # =============================== base checks =================================
    if len(graph.nodes) == 0:
        return 0
    if len(graph.nodes) == 1:
        try:
            return graph.nodes[0]['label']
        except KeyError:
            return list(graph.nodes)[0]
    # =========================== local definitions ===============================
    root = list(graph.nodes)[0]
    sigma_g: List[str] = []
    lambda_g: List[str] = []
    reachability_basis: Dict[str, List[int]] = {}
    # =========== Find reachability basis in the graph and fill lambda_g ==========
    ms_tree = nx.minimum_spanning_tree(graph)
    for node in ms_tree.nodes:
        node_path_id = nx.shortest_path(ms_tree, source=root, target=node)
        node_path_labels = [ms_tree.nodes[id]['label'] for id in node_path_id]
        reachability_basis[''.join(node_path_labels)] = node_path_id
        if graph.degree(node) == 1 and node != root:
            lambda_g.append(''.join(node_path_labels))
    # ====== create ni var as reachibility basis list without lambda_g values =====
    ni = [w for w in reachability_basis if w not in lambda_g]
    ni.pop(root)
    # =================== Find cycles by ni and fill sigma_g ======================
    for index, p_path in enumerate(ni):
        for q_path in ni[index + 1:]:
            if p_path not in q_path[:len(p_path)]:
                if not graph.has_edge(reachability_basis[p_path][-1],
                                      reachability_basis[q_path][-1]):
                    continue
                pqr = p_path + q_path[::-1]
                qpr = q_path + p_path[::-1]
                if pqr < qpr:
                    sigma_g.append(pqr)
                else:
                    sigma_g.append(qpr)

    return (sigma_g, lambda_g)


# ======================== CANONICAL PAIR METRICS =============================
def get_canonical_pair_metrics_from_dgraph(graph: nx.Graph) -> dict:
    """ find canonical pair metrics by graph values"""
    canonical_pair: Union[Tuple[List[str], List[str]], int, str] = ac_pair(graph)
    total_pair_count = 0
    if isinstance(canonical_pair, tuple):
        for c_word in canonical_pair[0]:
            total_pair_count += len(c_word)
        for l_word in canonical_pair[1]:
            total_pair_count += len(l_word)
    else:
        raise ValueError("Incorrect data. Graph is not exists!")
    n_nodes = graph.number_of_nodes()
    m_edges = graph.number_of_edges()
    delta = ceil(3 / 2 + sqrt(9 / 4 - 2 * n_nodes + 2 * m_edges))
    result = 2 * (m_edges - n_nodes + 1) * (n_nodes - delta + 2)
    mu_mn = ceil(delta * (delta - 1) / 2 - (m_edges - n_nodes + delta))
    power_of_sigma_g = ceil((delta - mu_mn - 1) * (delta - mu_mn - 2) * (n_nodes - delta + 2) + \
                            mu_mn * (mu_mn - 1) * (n_nodes - delta + 3) + \
                            mu_mn * (delta - mu_mn - 2) * (2 * n_nodes - 2 * delta + 5))
    return {
        "n": n_nodes,
        "m": m_edges,
        "delta": delta,
        "formula_result": result,
        "total_p_count": total_pair_count,
        "mu": mu_mn,
        "power_sigma_G": power_of_sigma_g,
        "canonical_pair": canonical_pair
    }
