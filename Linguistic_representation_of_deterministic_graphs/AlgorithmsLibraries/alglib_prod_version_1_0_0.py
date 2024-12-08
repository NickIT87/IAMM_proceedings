"""
IAMM - Graphs - ASP Work production version 1.0.0
Authors:
    Oleksiy S. Senchenko,
    Mykola I. Prytula

Linguistic presentation of Deterministic graph
"""

from typing import Tuple, List, Union, Dict
from collections import defaultdict
from math import ceil, sqrt

import networkx as nx  # type: ignore


_deleted_paths = set()


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
    return ValueError("Incorrect data. Graph is not exists!\n" + error_message)


def get_leaf_nodes_from_dgraph(dgraph: nx.Graph) -> Dict[int, str]:
    """helper for the AP alg. for checking leafs nodes"""
    leaf_nodes = [node for node, degree in dgraph.degree() if degree == 1]
    node_labels = [dgraph.nodes[node_id]["label"] for node_id in leaf_nodes]
    return dict(zip(leaf_nodes, node_labels))


def find_neighbors_with_the_same_labels(
    neighbors: List[int], labels: List[str]
) -> Dict[str, List[int]]:
    """Helper for the AR reduction algorithm."""
    element_positions: Dict[str, List[int]] = {}
    for index, element in enumerate(labels):
        element_positions.setdefault(element, []).append(neighbors[index])
    equal_elements: Dict[str, List[int]] = {
        element: positions
        for element, positions in element_positions.items()
        if len(positions) > 1
    }
    return equal_elements


def get_node_id_by_word(graph: nx.Graph, word: str, root_node: int) -> int:
    """Get the last node ID by label (word) path in the graph."""
    current_node = root_node
    for symbol_index, symbol in enumerate(word[1:], start=1):
        neighbors = list(graph.neighbors(current_node))
        labels = {graph.nodes[node_id]["label"]: node_id for node_id in neighbors}
        try:
            current_node = labels[symbol]
        except KeyError as exc:
            raise service_error(
                f"No vertex with symbol {symbol} in word {word} "
                + f"at position {symbol_index + 1}. {exc}\n"
            ) from exc
    return current_node


def validate_defining_pair(
    c_tuple: Tuple[str, ...], l_tuple: Tuple[str, ...], root: str
) -> bool:
    """Validate rules for using a pair of words in an algorithm."""
    if not (c_tuple or l_tuple):
        return False
    if c_tuple and not all(
        c_word[0] == c_word[-1] == root and len(c_word) >= 3 for c_word in c_tuple
    ):
        return False
    if l_tuple and not all(
        l_word[0] == root and len(l_word) >= 2 for l_word in l_tuple
    ):
        return False
    return True


def verify_deterministic_graph(
    dgraph: nx.Graph, cycles: Tuple[str, ...], leaves: Tuple[str, ...], root: int
) -> None:
    """Checkers for steps 3, 4, 5 in the AP algorithm."""
    all_leafs: Dict[int, str] = get_leaf_nodes_from_dgraph(dgraph)
    all_leafs.pop(root, None)
    for l_word in leaves:
        checked_node: int = get_node_id_by_word(dgraph, l_word, root)
        if dgraph.degree(checked_node) != 1:
            raise service_error(
                f"Word: {l_word} in the L set does not" + " end with a leaf vertex.\n"
            )
        if checked_node == root:
            raise service_error(
                f"The last vertex: {dgraph.nodes[checked_node]['label']}"
                + f" in the word: {l_word} "
                + f"is a root: {dgraph.nodes[root]['label']}.\n"
            )
        all_leafs.pop(checked_node, None)
    if all_leafs:
        raise service_error(f"Vertex id/label: {all_leafs} is not in the scope of L.")
    for c_word in cycles:
        if get_node_id_by_word(dgraph, c_word, root) != root:
            raise service_error(f"Word: {c_word} does not end with a root label.")


def min_word_using_special_order(word1: str, word2: str) -> str:
    """compare words by acrobatics '<' order"""
    if len(word1) > len(word2):
        return word2
    if len(word1) < len(word2):
        return word1
    if len(word1) == len(word2):
        if word1 > word2:
            return word2
    return word1


def get_nodes_shortest_paths_of_dgraph(
    dgraph: nx.Graph, root: int, root_label
) -> Dict[int, Dict[str, Union[str, List[int], None]]]:
    """
    Get shortest labeled path for each node
    by labels and ids, using acrobatics '<' order.
    """
    # initial values
    nodes_shortest_paths: Dict[int, Dict[str, Union[str, List[int], None]]] = (
        defaultdict(lambda: {"npl": None, "npid": None})
    )
    glabels: List[str] = sorted([label for node, label in dgraph.nodes(data="label")])
    ids: List[int] = list(dgraph.nodes)
    # cycle variables
    current_array_index = 0
    vertex_count_result = 0
    # STEP 1 get labels paths variables
    shortest_words: List[str] = [root_label]
    nodes_shortest_paths[root]["npl"] = root_label
    # STEP 2 get ids paths variables
    shortest_words_ids: List[List[int]] = [[root]]
    current_node_shortest_paths_by_ids: List[int] = [root]
    nodes_shortest_paths[root]["npid"] = [root]

    while vertex_count_result < len(ids) - 1:
        for letter in sorted(set(glabels)):
            labeled_short_path = shortest_words[current_array_index] + letter
            try:
                obtained_node: int = get_node_id_by_word(
                    dgraph, labeled_short_path, root
                )
                if (
                    nodes_shortest_paths[obtained_node]["npl"] is None
                    and obtained_node != root
                ):
                    nodes_shortest_paths[obtained_node]["npl"] = labeled_short_path
                    shortest_words.append(labeled_short_path)

                    result_node_shortest_path_by_ids = list(
                        current_node_shortest_paths_by_ids
                    )
                    result_node_shortest_path_by_ids.append(obtained_node)

                    nodes_shortest_paths[obtained_node][
                        "npid"
                    ] = result_node_shortest_path_by_ids
                    shortest_words_ids.append(result_node_shortest_path_by_ids)

                    vertex_count_result += 1
            except ValueError:
                continue
        current_array_index += 1
        current_node_shortest_paths_by_ids = shortest_words_ids[current_array_index]
    return dict(nodes_shortest_paths)


# ======================== ALGORITHMS REALIZATION ============================
def ar_nodes(graph: nx.Graph) -> nx.Graph:
    """reduction algorithm AR"""
    dgraph: nx.Graph = nx.Graph(graph)
    trigger: bool = True
    while trigger:
        trigger = False
        for node in dgraph.nodes:
            neighbors: List[int] = list(dgraph.neighbors(node))
            labels: List[str] = [
                dgraph.nodes[node_id]["label"] for node_id in neighbors
            ]
            equals_labels: Dict[str, List[int]] = find_neighbors_with_the_same_labels(
                neighbors, labels
            )
            if equals_labels:
                for neighbours_ids in equals_labels.values():
                    not_changeable_node: int = min(neighbours_ids)
                    neighbours_ids.remove(not_changeable_node)
                    for vertex in neighbours_ids:
                        neighbors_of_deleted_node: List[int] = list(
                            dgraph.neighbors(vertex)
                        )
                        neighbors_of_deleted_node.remove(node)
                        dgraph.add_edges_from(
                            (v_node, not_changeable_node)
                            for v_node in neighbors_of_deleted_node
                            if v_node != not_changeable_node
                        )
                        dgraph.remove_node(vertex)
                trigger = True
                break
    return dgraph


# @profile    # python -m memory_profiler main.py
def ap_graph(
    cycles: Tuple[str, ...], leaves: Tuple[str, ...], root_label: str = "1"
) -> nx.Graph:
    """build graph on pair of words, algorithm AP"""
    # ===================== STEP 0 initial definitions =======================
    if not validate_defining_pair(cycles, leaves, root_label):
        raise service_error("Invalid defining pair.")
    root: int = 0
    custom_id: int
    id_generator: IDsGenerator = IDsGenerator()
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
    # ================ STEPS 3,4,5 Check each word in (C, L) =================
    verify_deterministic_graph(dgraph_g, cycles, leaves, root)
    return dgraph_g


def ac_pair(
    graph: nx.Graph,
) -> Union[Tuple[Tuple[str, ...], Tuple[str, ...]], int, str]:
    """get canonical pair of words, algorithm AK"""
    # ============================ base checks ===============================
    if len(graph.nodes) == 0:
        return 0
    if len(graph.nodes) == 1:
        try:
            return graph.nodes[0]["label"]
        except KeyError:
            return list(graph.nodes)[0]
    # ========================= local definitions ============================
    root: int = list(graph.nodes)[0]
    sigma_g: List[str] = []
    lambda_g: List[str] = []
    reachability_basis: Dict[str, List[int]] = {}
    # ======== Find reachability basis in the graph and fill lambda_g ========
    # ms_tree = graph.edge_subgraph(list(nx.bfs_edges(graph, source=root)))
    ms_tree = get_nodes_shortest_paths_of_dgraph(
        graph, root=root, root_label=graph.nodes[0]["label"]
    )
    # for node in ms_tree.nodes:
    for node, data in ms_tree.items():
        node_path_id: List[int] = data["npid"]  # type: ignore
        node_path_labels: List[str] = list(data["npl"])  # type: ignore
        reachability_basis["".join(node_path_labels)] = node_path_id
        if graph.degree(node) == 1 and node != root:
            lambda_g.append("".join(node_path_labels))
    # === create ni var as reachibility basis list without lambda_g values ===
    ni: List[str] = [w for w in reachability_basis if w not in lambda_g]
    ni.pop(root)
    # =============== Find cycles by ni and fill sigma_g =====================
    for index, p_path in enumerate(ni):
        for q_path in ni[index + 1 :]:
            if p_path not in q_path[: len(p_path)]:
                if not graph.has_edge(
                    reachability_basis[p_path][-1], reachability_basis[q_path][-1]
                ):
                    continue
                pqr: str = p_path + q_path[::-1]
                qpr: str = q_path + p_path[::-1]
                if pqr < qpr:
                    sigma_g.append(pqr)
                elif pqr > qpr:
                    sigma_g.append(qpr)
    return tuple(sigma_g), tuple(lambda_g)


# ======================= CANONICAL PAIR METRICS =============================
def get_canonical_pair_metrics_from_dgraph(
    graph: nx.Graph,
) -> Dict[str, Union[int, Tuple[Tuple[str, ...], Tuple[str, ...]]]]:
    """find canonical pair metrics by graph values"""
    canonical_pair: Union[Tuple[Tuple[str, ...], Tuple[str, ...]], int, str] = ac_pair(
        graph
    )
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
        (delta - mu_mn - 1) * (delta - mu_mn - 2) * (n_nodes - delta + 2)
        + mu_mn * (mu_mn - 1) * (n_nodes - delta + 3)
        + mu_mn * (delta - mu_mn - 2) * (2 * n_nodes - 2 * delta + 5)
    )
    return {
        "n": n_nodes,
        "m": m_edges,
        "delta": delta,
        "formula_result": result,
        "total_p_count": total_pair_count,
        "mu": mu_mn,
        "power_sigma_G": power_of_sigma_g,
        "canonical_pair": canonical_pair,
    }


# ============================ COMPRESSION ===================================
def insertion_acrobatics_sort(arr: List[str]):
    """insertion sort by special order"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key == min_word_using_special_order(key, arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def remove_repeating_words_into_pair_component(pair_component: List[str]):
    """operation 1: transform the components of the pair
    into ordered sets without repetitions"""
    pair_component[:] = list(set(pair_component))
    insertion_acrobatics_sort(pair_component)


def remove_reverse_words(pair_component: List[str]):
    """operation 2: remove reverse words from the first component"""
    for index, word in enumerate(pair_component):
        if len(word) == 3 and word[0] == word[2]:
            pair_component.pop(index)


def get_modified_word(idx: int, word: str, no_debug=False) -> str:
    """operation 3 helper: find sequences of kind 'xyx' in word
    and return modified word xyx -> x"""
    global _deleted_paths
    modified_word = word
    for i in range(len(word) - 2):
        if word[i] == word[i + 2]:  # and string[i] != string[i + 1]:
            if idx == 0 and not no_debug:
                _deleted_paths.add(
                    min_word_using_special_order(
                        word[: i + 2], word[::-1][: len(word) - i - 1]
                    )
                )
            elif not no_debug:
                _deleted_paths.add(word[: i + 2])
            modified_word = word[: i + 1] + word[i + 3 :]
            return modified_word
    return modified_word


def remove_reverse_sequence(compressed_pair: List[List[str]], no_debug=False) -> bool:
    """operation 3: find sequences of kind 'xyx' in word
    and return modified word xyx -> x"""
    for index_pair_element, sigma_lambda_element in enumerate(compressed_pair):
        for idx_sl_element, word in enumerate(sigma_lambda_element):
            modified_word = get_modified_word(
                index_pair_element, word, no_debug=no_debug
            )
            if word != modified_word:
                compressed_pair[index_pair_element][idx_sl_element] = modified_word
                return True
    return False


def acrobatic_reverce(c_component: List[str]) -> bool:
    """operation 4: replace lesser word for acrobatic"""
    for idx_element, sigma_word in enumerate(c_component):
        reversed_word = sigma_word[::-1]
        if reversed_word < sigma_word:
            c_component[idx_element] = min_word_using_special_order(
                reversed_word, sigma_word
            )
            return True
    return False


def path_optimization(compressed_pair: List[List[str]]) -> bool:
    """need docstring"""
    for word in compressed_pair[0]:
        left = (len(word) + 1) // 2
        right = ((len(word) + 1) // 2) + 1
        w_left_1 = word[::-1][: int(len(word) / 2) + 1]
        w_left_2 = word[:left]
        w_right_1 = word[:right]
        w_right_2 = word[::-1][: len(word) // 2]
        for idx_cword, cword in enumerate(compressed_pair[0]):
            if cword != word:
                if cword.startswith(w_left_1):
                    compressed_pair[0][idx_cword] = cword.replace(w_left_1, w_left_2, 1)
                    return True
                if cword.startswith(w_right_1):
                    compressed_pair[0][idx_cword] = cword.replace(
                        w_right_1, w_right_2, 1
                    )
                    return True
                if cword.endswith(w_left_1[::-1]):
                    last_entry_index = cword.rfind(w_left_1[::-1])
                    if last_entry_index != -1:
                        compressed_pair[0][idx_cword] = (
                            cword[:last_entry_index]
                            + w_left_2[::-1]
                            + cword[last_entry_index + len(w_left_1) :]
                        )
                        return True
                if cword.endswith(w_right_1[::-1]):
                    last_entry_index = cword.rfind(w_right_1[::-1])
                    if last_entry_index != -1:
                        compressed_pair[0][idx_cword] = (
                            cword[:last_entry_index]
                            + w_right_2[::-1]
                            + cword[last_entry_index + len(w_right_1) :]
                        )
                        return True
        for idx_lword, lword in enumerate(compressed_pair[1]):
            if lword.startswith(w_left_1):
                compressed_pair[1][idx_lword] = lword.replace(w_left_1, w_left_2, 1)
                return True
            if lword.startswith(w_right_1):
                compressed_pair[1][idx_lword] = lword.replace(w_right_1, w_right_2, 1)
                return True
    return False


def ops5_for_check_gdp(word: str, c_component: List[str]) -> str:
    """operation 5 for check gdp function"""
    shortest_word = word
    for c_word in c_component:
        left = (len(c_word) + 1) // 2
        right = ((len(c_word) + 1) // 2) + 1
        w_left_1 = c_word[::-1][: int(len(c_word) / 2) + 1]
        w_left_2 = c_word[:left]
        w_right_1 = c_word[:right]
        w_right_2 = c_word[::-1][: len(c_word) // 2]
        if shortest_word.startswith(w_left_1):
            shortest_word = shortest_word.replace(w_left_1, w_left_2, 1)
            return shortest_word
        if shortest_word.startswith(w_right_1):
            shortest_word = shortest_word.replace(w_right_1, w_right_2, 1)
            return shortest_word
    return shortest_word


def check_global_path_words(word, compressed_pair) -> bool:
    """word minimization in progress"""
    shortest_word = word
    trigger = True
    while trigger:
        if shortest_word != get_modified_word(0, shortest_word, no_debug=True):
            shortest_word = get_modified_word(0, shortest_word, True)
            continue
        if shortest_word != ops5_for_check_gdp(shortest_word, compressed_pair[0]):
            shortest_word = ops5_for_check_gdp(shortest_word, compressed_pair[0])
            continue
        trigger = False
    for cword in compressed_pair[0]:
        if cword.startswith(shortest_word):
            return True
        if cword[::-1].startswith(shortest_word):
            return True
    for lword in compressed_pair[1]:
        if lword.startswith(shortest_word):
            return True
    return False


def compression(
    c_component: Tuple[str, ...], l_component: Tuple[str, ...], no_gdp: bool = False
) -> Dict[str, Union[Tuple[Tuple[str, ...], ...], bool, None]]:
    """in progress"""
    global _deleted_paths
    if not no_gdp:
        _deleted_paths = set()
    compressed_pair: List[List[str]] = [list(c_component), list(l_component)]
    result: Dict[str, Union[Tuple[Tuple[str, ...], ...], bool, None]] = {
        "compressed_pair": None,
        "graph_exists": None,
    }
    trigger = True
    while trigger:
        # operation 1
        for component in compressed_pair:
            insertion_acrobatics_sort(component)
            remove_repeating_words_into_pair_component(component)
        # operation 2
        remove_reverse_words(compressed_pair[0])
        # operation 3
        if remove_reverse_sequence(compressed_pair, no_debug=no_gdp):
            continue
        # operation 4
        if acrobatic_reverce(compressed_pair[0]):
            continue
        # operation 5
        if path_optimization(compressed_pair):
            continue
        trigger = False
    # additional check
    converted_compressed_pair = tuple(tuple(sublist) for sublist in compressed_pair)
    if not no_gdp:
        for gdp_word in _deleted_paths:
            if not check_global_path_words(gdp_word, compressed_pair):
                result["compressed_pair"] = converted_compressed_pair
                result["graph_exists"] = False
                return result
        result["compressed_pair"] = converted_compressed_pair
        result["graph_exists"] = True
    else:
        result["compressed_pair"] = converted_compressed_pair
    return result
