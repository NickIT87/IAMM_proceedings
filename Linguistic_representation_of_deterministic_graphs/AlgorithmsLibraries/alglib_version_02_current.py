""" IAMM - Graphs - ASP Work """
from typing import Tuple, List, Union, Dict
from math import ceil, sqrt
import re
import networkx as nx  # type: ignore


# =========================== HELPERS FUNCTIONS ==============================
class IDsGenerator:
    """helper for the AP alg. Generate custom id for each node"""
    def __init__(self) -> None:
        self._counter: int = 0

    def get_id(self) -> int:
        """get the id number as counter function"""
        self._counter += 1
        return self._counter

    def reset(self) -> None:
        """reset counter to 0"""
        self._counter = 0


def service_error(error_message: str = "") -> ValueError:
    """helper for the AP alg. Generate ValueError if Graph is not exists"""
    return ValueError(
        "Incorrect data. Graph is not exists!\n" + error_message)


def get_leaf_nodes_from_dgraph(dgraph: nx.Graph) -> Dict[int, str]:
    """helper for the AP alg. for checking leafs nodes"""
    leaf_nodes = [node for node, degree in dgraph.degree() if degree == 1]
    node_labels = [dgraph.nodes[node_id]['label'] for node_id in leaf_nodes]
    return dict(zip(leaf_nodes, node_labels))


def find_neighbors_with_the_same_labels(neighbors: List[int],
                                        labels: List[str]
                                        ) -> Dict[str, List[int]]:
    """ helper for the AR reduction algorithm """
    element_positions: Dict[str, List[int]] = {}
    for index, element in enumerate(labels):
        if element in element_positions:
            element_positions[element].append(neighbors[index])
        else:
            element_positions[element] = [neighbors[index]]
    equal_elements: Dict[str, List[int]] = {
        element: positions for element,
        positions in element_positions.items() if len(positions) > 1
    }
    return equal_elements


def get_node_id_by_word(graph: nx.Graph, word: str, root_node: int) -> int:
    """ get last node id by label (word) path in graph """
    current_node: int = root_node
    for symbol in word[1:]:
        neighbors: List[int] = list(graph.neighbors(current_node))
        labels: List[str] = [graph.nodes[node_id]['label']
                             for node_id in neighbors]
        try:
            next_node: int = neighbors[labels.index(symbol)]
        except Exception as exc:
            raise ValueError(
                f"{exc} Invalid data. No symbol as label.\n" +
                "Graph is not exists!"
            ) from exc
        current_node = next_node
    return current_node


def word_pair_data_validation(c_tuple: Tuple[str, ...],
                              l_tuple: Tuple[str, ...],
                              root: str) -> bool:
    """ rules for using a pair of words in an algorithm """
    search_pattern: str = r"(.)\1"
    if not c_tuple and not l_tuple:
        return False
    if c_tuple:
        for c_word in c_tuple:
            if c_word[0] != c_word[-1] and c_word[0] != root:
                return False
            if bool(re.search(search_pattern, c_word)):
                return False
    if l_tuple:
        for l_word in l_tuple:
            if l_word[0] != root:
                return False
            if bool(re.search(search_pattern, l_word)):
                return False
    return True


# ======================== ALGORITHMS REALIZATION ============================
def ar_nodes(graph: nx.Graph) -> nx.Graph:
    """ reduction algorithm AR """
    dgraph: nx.Graph = nx.Graph(graph)
    trigger: bool = True
    while trigger:
        trigger = False
        for node in dgraph.nodes:
            neighbors: List[int] = list(dgraph.neighbors(node))
            labels: List[str] = [dgraph.nodes[node_id]['label']
                                 for node_id in neighbors]
            equals_labels: Dict[str, List[int]] = \
                find_neighbors_with_the_same_labels(neighbors, labels)
            if equals_labels:
                for neighbours_ids in equals_labels.values():
                    not_changeable_node: int = min(neighbours_ids)
                    neighbours_ids.remove(not_changeable_node)
                    for vertex in neighbours_ids:
                        neighbors_of_deleted_node: List[int] = list(
                            dgraph.neighbors(vertex))
                        neighbors_of_deleted_node.remove(node)
                        dgraph.add_edges_from(
                            (v_node, not_changeable_node)
                            for v_node in neighbors_of_deleted_node)
                        dgraph.remove_node(vertex)
                trigger = True
                break
    return dgraph


# @profile    # python -m memory_profiler main.py
def ap_graph(cycles: Tuple[str, ...], leaves: Tuple[str, ...],
             root_label: str = '1') -> nx.Graph:
    """ build graph on pair of words, algorithm AP """
    # ===================== STEP 0 initial definitions =======================
    if not word_pair_data_validation(cycles, leaves, root_label):
        raise service_error()
    id_generator: IDsGenerator = IDsGenerator()
    root: int = 0
    custom_id: int
    dgraph_g = nx.Graph()
    dgraph_g.add_node(root, label=root_label)
    # ================= STEP 1 Construct the graph for C =====================
    for c_word in cycles:
        for index, label in enumerate(c_word[1:-1], start=1):
            custom_id = id_generator.get_id()
            dgraph_g.add_node(custom_id, label=label)
            match index:
                case 1:
                    dgraph_g.add_edge(root, custom_id)
                case _:
                    dgraph_g.add_edge(custom_id - 1, custom_id)
            if index == len(c_word) - 2:
                dgraph_g.add_edge(custom_id, root)
        dgraph_g = ar_nodes(dgraph_g)
    # ======================= STEP 2 Add nodes for L =========================
    for l_word in leaves:
        for index, label in enumerate(l_word[1:], start=1):
            custom_id = id_generator.get_id()
            dgraph_g.add_node(custom_id, label=label)
            match index:
                case 1:
                    dgraph_g.add_edge(root, custom_id)
                case _:
                    dgraph_g.add_edge(custom_id - 1, custom_id)
        dgraph_g = ar_nodes(dgraph_g)
    # ======== STEPS 3 - 4 Check each word in L end each leaf vertex =========
    all_leafs: Dict = get_leaf_nodes_from_dgraph(dgraph_g)
    if root in all_leafs:
        all_leafs.pop(root)
    for l_word_index, l_word in enumerate(leaves):
        checked_node: int = get_node_id_by_word(dgraph_g, l_word, root)
        if dgraph_g.degree(checked_node) != 1:
            print(service_error(
                f"Invalid pair. Word: {leaves[l_word_index]} " +
                "in the L set does not end with a leaf vertex."))
        if checked_node in all_leafs:
            all_leafs.pop(checked_node)
    if len(all_leafs) > 0:
        print(service_error(
            f"Vertex id/label: {all_leafs} is not in the scope of L."))
    return dgraph_g


def ac_pair(graph: nx.Graph) -> \
        Union[Tuple[Tuple[str, ...], Tuple[str, ...]], int, str]:
    """ get canonical pair of words, algorithm AK """
    # ============================ base checks ===============================
    if len(graph.nodes) == 0:
        return 0
    if len(graph.nodes) == 1:
        try:
            return graph.nodes[0]['label']
        except KeyError:
            return list(graph.nodes)[0]
    # ========================= local definitions ============================
    root: int = list(graph.nodes)[0]
    sigma_g: List[str] = []
    lambda_g: List[str] = []
    reachability_basis: Dict[str, List[int]] = {}
    # ======== Find reachability basis in the graph and fill lambda_g ========
    ms_tree = nx.minimum_spanning_tree(graph)
    for node in ms_tree.nodes:
        node_path_id: List[int] = nx.shortest_path(ms_tree,
                                                   source=root, target=node)
        node_path_labels: List[str] = [ms_tree.nodes[node_id]['label']
                                       for node_id in node_path_id]
        reachability_basis[''.join(node_path_labels)] = node_path_id
        if graph.degree(node) == 1 and node != root:
            lambda_g.append(''.join(node_path_labels))
    # === create ni var as reachibility basis list without lambda_g values ===
    ni: List[str] = [w for w in reachability_basis if w not in lambda_g]
    ni.pop(root)
    # =============== Find cycles by ni and fill sigma_g =====================
    for index, p_path in enumerate(ni):
        for q_path in ni[index + 1:]:
            if p_path not in q_path[:len(p_path)]:
                if not graph.has_edge(reachability_basis[p_path][-1],
                                      reachability_basis[q_path][-1]):
                    continue
                pqr: str = p_path + q_path[::-1]
                qpr: str = q_path + p_path[::-1]
                if pqr < qpr:
                    sigma_g.append(pqr)
                else:
                    sigma_g.append(qpr)
    return tuple(sigma_g), tuple(lambda_g)


# ======================= CANONICAL PAIR METRICS =============================
def get_canonical_pair_metrics_from_dgraph(graph: nx.Graph) -> \
        Dict[str, Union[int, Tuple[Tuple[str, ...], Tuple[str, ...]]]]:
    """ find canonical pair metrics by graph values"""
    canonical_pair: Union[
        Tuple[Tuple[str, ...], Tuple[str, ...]], int, str
    ] = ac_pair(graph)
    total_pair_count: int = 0
    if isinstance(canonical_pair, tuple):
        for c_word in canonical_pair[0]:
            total_pair_count += len(c_word)
        for l_word in canonical_pair[1]:
            total_pair_count += len(l_word)
    else:
        raise ValueError("Incorrect data. Graph is not exists!")
    n_nodes: int = graph.number_of_nodes()
    m_edges: int = graph.number_of_edges()
    delta: int = ceil(3 / 2 + sqrt(9 / 4 - 2 * n_nodes + 2 * m_edges))
    result: int = 2 * (m_edges - n_nodes + 1) * (n_nodes - delta + 2)
    mu_mn: int = ceil(delta * (delta - 1) / 2 - (m_edges - n_nodes + delta))
    power_of_sigma_g: int = ceil(
        (delta - mu_mn - 1) * (delta - mu_mn - 2) * (n_nodes - delta + 2) +
        mu_mn * (mu_mn - 1) * (n_nodes - delta + 3) +
        mu_mn * (delta - mu_mn - 2) * (2 * n_nodes - 2 * delta + 5)
    )
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
