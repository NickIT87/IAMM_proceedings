""" IAMM - Graphs - ASP Work """
from typing import Tuple, List, Union, Dict
from collections import defaultdict
from math import ceil, sqrt
import re

import networkx as nx  # type: ignore


num = 101

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
    """Helper for the AR reduction algorithm."""
    element_positions: Dict[str, List[int]] = {}
    for index, element in enumerate(labels):
        element_positions.setdefault(element, []).append(neighbors[index])
    equal_elements: Dict[str, List[int]] = {
        element: positions for element,
        positions in element_positions.items() if len(positions) > 1
    }
    return equal_elements


def get_node_id_by_word(graph: nx.Graph, word: str, root_node: int) -> int:
    """Get the last node ID by label (word) path in the graph."""
    current_node = root_node
    for symbol_index, symbol in enumerate(word[1:], start=1):
        neighbors = list(graph.neighbors(current_node))
        labels = {graph.nodes[node_id]['label']: node_id
                  for node_id in neighbors}
        try:
            current_node = labels[symbol]
        except KeyError as exc:
            raise service_error(
                f"No vertex with symbol {symbol} in word {word} " +
                f"at position {symbol_index + 1}. {exc}\n"
            ) from exc
    return current_node


def validate_defining_pair(c_tuple: Tuple[str, ...],
                           l_tuple: Tuple[str, ...],
                           root: str) -> bool:
    """Validate rules for using a pair of words in an algorithm."""
    if not (c_tuple or l_tuple):
        return False
    if c_tuple and not all(c_word[0] == c_word[-1] == root and
                           len(c_word) >= 3 for c_word in c_tuple):
        return False
    if l_tuple and not all(l_word[0] == root and
                           len(l_word) >= 2 for l_word in l_tuple):
        return False
    return True


def verify_deterministic_graph(dgraph: nx.Graph, cycles: Tuple[str, ...],
                               leaves: Tuple[str, ...], root: int) -> None:
    """Checkers for steps 3, 4, 5 in the AP algorithm."""
    all_leafs: Dict[int, str] = get_leaf_nodes_from_dgraph(dgraph)
    all_leafs.pop(root, None)
    for l_word in leaves:
        checked_node: int = get_node_id_by_word(dgraph, l_word, root)
        if dgraph.degree(checked_node) != 1:
            raise service_error(f"Word: {l_word} in the L set does not" +
                                " end with a leaf vertex.\n")
        if checked_node == root:
            raise service_error(
                f"The last vertex: {dgraph.nodes[checked_node]['label']}" +
                f" in the word: {l_word} " +
                f"is a root: {dgraph.nodes[root]['label']}.\n")
        all_leafs.pop(checked_node, None)
    if all_leafs:
        raise service_error(
            f"Vertex id/label: {all_leafs} is not in the scope of L.")
    for c_word in cycles:
        if get_node_id_by_word(dgraph, c_word, root) != root:
            raise service_error(
                f"Word: {c_word} does not end with a root label.")


def min_word_using_special_order(word1: str, word2: str) -> str:
    """ compare words by acrobatics '<' order """
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
    nodes_shortest_paths: Dict[
        int, Dict[str, Union[str, List[int], None]]
    ] = defaultdict(lambda: {"npl": None, "npid": None})
    glabels: List[str] = sorted(
        [label for node, label in dgraph.nodes(data='label')])
    ids: List[int] = list(dgraph.nodes)
    # cycle variables
    current_array_index = 0
    vertex_count_result = 0
    # STEP 1 get labels paths variables
    shortest_words: List[str] = [root_label]
    nodes_shortest_paths[root]['npl'] = root_label
    # STEP 2 get ids paths variables
    shortest_words_ids: List[List[int]] = [[root]]
    current_node_shortest_paths_by_ids: List[int] = [root]
    nodes_shortest_paths[root]['npid'] = [root]

    while vertex_count_result < len(ids) - 1:
        for letter in sorted(set(glabels)):
            labeled_short_path = shortest_words[current_array_index] + letter
            try:
                obtained_node: int = get_node_id_by_word(
                    dgraph, labeled_short_path, root)
                if nodes_shortest_paths[obtained_node]["npl"] is None \
                        and obtained_node != root:
                    nodes_shortest_paths[
                        obtained_node
                    ]["npl"] = labeled_short_path
                    shortest_words.append(labeled_short_path)

                    result_node_shortest_path_by_ids = list(
                        current_node_shortest_paths_by_ids)
                    result_node_shortest_path_by_ids.append(obtained_node)

                    nodes_shortest_paths[
                        obtained_node
                    ]["npid"] = result_node_shortest_path_by_ids
                    shortest_words_ids.append(
                        result_node_shortest_path_by_ids)

                    vertex_count_result += 1
            except ValueError:
                continue
        current_array_index += 1
        current_node_shortest_paths_by_ids = shortest_words_ids[
            current_array_index
        ]
    return dict(nodes_shortest_paths)


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
                            for v_node in neighbors_of_deleted_node
                            if v_node != not_changeable_node)
                        dgraph.remove_node(vertex)
                trigger = True
                break
    return dgraph


# @profile    # python -m memory_profiler main.py
def ap_graph(cycles: Tuple[str, ...], leaves: Tuple[str, ...],
             root_label: str = '1') -> nx.Graph:
    """ build graph on pair of words, algorithm AP """
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
    # ms_tree = graph.edge_subgraph(list(nx.bfs_edges(graph, source=root)))
    ms_tree = get_nodes_shortest_paths_of_dgraph(
        graph, root=root, root_label=graph.nodes[0]['label'])
    # for node in ms_tree.nodes:
    for node, data in ms_tree.items():
        # node_path_id: List[int] = nx.shortest_path(ms_tree, source=root, target=node)
        node_path_id: List[int] = data["npid"]  # type: ignore
        # node_path_labels: List[str] = [ms_tree.nodes[node_id]['label'] for node_id in node_path_id]
        node_path_labels: List[str] = list(data["npl"])  # type: ignore
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
                elif pqr > qpr:
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


# ============================ COMPRESSION ===================================
def find_reverse_sequences(word: str) -> List[str]:
    """ Helper for the compression alg
    find sequences of kind 'xyx' in word """
    sequences = []
    for i in range(len(word) - 2):
        if word[i] == word[i + 2]:  # and string[i] != string[i + 1]:
            sequences.append(word[i:i + 3])
    return sequences


def get_modified_word(word: str) -> str:
    """operation 3: find sequences of kind 'xyx' in word
    and return modified word xyx -> x """
    modified_word = word
    for i in range(len(word) - 2):
        if word[i] == word[i + 2]:  # and string[i] != string[i + 1]:
            modified_word = word[:i+1] + word[i+3:]
    return modified_word


def bubble_acrobatics_sort(arr: List[str]):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] != min_word_using_special_order(arr[j], arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def insertion_acrobatics_sort(arr: List[str]):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key == min_word_using_special_order(key, arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def remove_repeating_words_into_pair_component(pair_component: List[str]):
    """ operation 1: transform the components of the pair
    into ordered sets without repetitions """
    global num
    a = pair_component

    print("Bylo: ", len(pair_component))

    pair_component[:] = list(set(pair_component))
    insertion_acrobatics_sort(pair_component)

    print("stalo: ", len(pair_component))

    if a != pair_component:
        print(num, " Operation 1 is performed.\n")
        num = num + 1


def remove_word_of_one_symbol(pair_component: List[str]):
    """operation 2: remove words of length 1 from the first component """
    global num
    for index, word in enumerate(pair_component):
        if len(word) < 2:
            pair_component.pop(index)
            print(num, " Operation 2 is performed.\n")
            num = num + 1


def remove_reverse_sequence(compressed_pair: List[List[str]]) -> bool:
    """ operation 3: remove first sequence from
        each pair component XYX -> X; included (C, L)"""
    global num
    for index_pair_element, sigmaLambda_element in enumerate(compressed_pair):
        for idx_sl_element, word in enumerate(sigmaLambda_element):
            modified_word = get_modified_word(word)
            if word != modified_word:
                compressed_pair[index_pair_element][idx_sl_element] = modified_word
                print(num, f" Operation 3 is performed. word={word}, modified={modified_word} \n")
                num = num + 1
                return True
    return False


def acrobatic_reverce(c_component: List[str]) -> bool:
    """ operation 4: replace lesser word for acrobatic  """
    global num
    for idx_element, sigma_word in enumerate(c_component):
        reversed_word = sigma_word[::-1]
        if reversed_word < sigma_word:
            c_component[idx_element] = min_word_using_special_order(reversed_word, sigma_word)
            print(num, f" Operation 4 is performed. sigma={sigma_word} reversed={reversed_word}.\n")
            num = num + 1
            return True
    return False


def operation5(compressed_pair: List[List[str]]) -> bool:
    global num
    for index_of_word, word in enumerate(compressed_pair[0]):
        left = (len(word) + 1) // 2
        right = ((len(word) + 1) // 2) + 1
        w_left_1 = word[::-1][:int(len(word) / 2) + 1]
        w_left_2 = word[:left]
        w_right_1 = word[:right]
        w_right_2 = word[::-1][:len(word) // 2]
        for idx_cword, cword in enumerate(compressed_pair[0]):
            if (cword != word) and cword.startswith(w_left_1):
                modified_cword = cword.replace(w_left_1, w_left_2, 1)
                print(num, f" Operation 5 is performed. cword={cword}, modified={modified_cword}, w1={w_left_1}, w2={w_left_2} LEFT Begin. word={word} \n")
                num = num + 1
                compressed_pair[0][idx_cword] = modified_cword
                return True
        for idx_lword, lword in enumerate(compressed_pair[1]):
            if lword.startswith(w_left_1):
                modified_lword = lword.replace(w_left_1, w_left_2, 1)
                print(num, f" Operation 5 is performed. lword={lword}, modified={modified_lword} w1={w_left_1}, w2={w_left_2} LEFT Begin. word={word} \n")
                num = num + 1
                compressed_pair[1][idx_lword] = modified_lword
                return True
        for idx_cword, cword in enumerate(compressed_pair[0]):
            if cword != word and cword.endswith(w_left_1[::-1]):
                # rcword = cword[::-1]
                # modified_rcword = rcword.replace(w1[::-1], w2[::-1], 1)
                # modified_cword = modified_rcword[::-1]
                # Найти индекс последнего вхождения w1 в cword
                entry_index = cword.rfind(w_left_1[::-1])
                if entry_index != -1:
                    # Заменить последнее вхождение w1 на w2
                    modified_cword = cword[:entry_index] + w_left_2[::-1] + cword[entry_index + len(w_left_1):]
                    print(num, f" Operation 5 LEFT END: cword={cword}, modified={modified_cword} w1reversed={w_left_1[::-1]}, w2={w_left_2[::-1]} End. word={word} \n")
                    num = num + 1
                    compressed_pair[0][idx_cword] = modified_cword
                return True
        for idx_cword, cword in enumerate(compressed_pair[0]):
            if (cword != word) and cword.startswith(w_right_1):
                modified_cword = cword.replace(w_right_1, w_right_2, 1)
                print(num, f" Operation 5 is performed. cword={cword}, modified={modified_cword}, w1={w_right_1}, w2={w_right_2} RIGHT Begin. word={word} \n")
                num = num + 1
                compressed_pair[0][idx_cword] = modified_cword
                return True
        # for idx_lword, lword in enumerate(compressed_pair[1]):
        #     if lword.startswith(w1):
        #         modified_lword = lword.replace(w1, w2, 1)
        #         print(num, f" Operation 5 is performed. lword={lword}, modified={modified_lword} w1={w1}, w2={w2} RIGHT Begin. word={word} \n")
        #         num = num + 1
        #         compressed_pair[1][idx_lword] = modified_lword
        #         return True
        # for idx_cword, cword in enumerate(compressed_pair[0]):
        #     if cword != word and cword.endswith(w1[::-1]):
        #         entry_index = cword.rfind(w1[::-1])
        #         if entry_index != -1:
        #             # Заменить последнее вхождение w1 на w2
        #             modified_cword = cword[:entry_index] + w2[::-1] + cword[entry_index + len(w1):]
        #             print(num, f" Operation 5 RIGHT END: cword={cword}, modified={modified_cword} w1reversed={w1[::-1]}, w2={w2[::-1]} End. word={word} \n")
        #             num = num + 1
        #             compressed_pair[0][idx_cword] = modified_cword
        #         return True

    return False


def compression(c_component: Tuple[str, ...],
                l_component: Tuple[str, ...]) -> List:
    """ in progress """
    compressed_pair: List[List[str], List[str]] = [
        list(c_component),
        list(l_component)
    ]
    print("UNCOMPRESSED DEFINING PAIR: \n", c_component, l_component)

    trigger = True
    while trigger:
        for component in compressed_pair:
            insertion_acrobatics_sort(component)
            remove_repeating_words_into_pair_component(component)

        #print("\nDEBUG COMPRESSION AFTER 1, 2 STEP (sorting): \n", compressed_pair)

        remove_word_of_one_symbol(compressed_pair[0])

        #print("\nDEBUG COMPRESSION AFTER 3 STEP (remove 1 symbol from C): \n", compressed_pair)

        if remove_reverse_sequence(compressed_pair):
            #print("pair if zamena TRUE: ", compressed_pair)
            continue

        #print("\nDEBUG COMPRESSION AFTER 4 STEP (remove XYX): \n", compressed_pair)

        if acrobatic_reverce(compressed_pair[0]):
            #print("acrobatic reverse if zamena TRUE: ", compressed_pair)
            continue

        if operation5(compressed_pair):
            continue

        #operation5(compressed_pair)

        trigger = False

    #remove_reverse_sequence(compressed_pair[0])
    #remove_reverse_sequence(compressed_pair[1])
    #
    # print("\nDEBUG COMPRESSION AFTER 2 STEP (operation 1): \n", compressed_pair)
    #
    # # operation 2
    # remove_word_of_one_symbol(compressed_pair[0])
    #
    #
    #
    # print("\nSTEP 3 started:\n ")




    ## 3 !!! синее-зеленое pass
    # for index_of_word, word in enumerate(compressed_pair[0]):
    #     # lst_word = list(word)
    #     for index_of_symbol, symbol in enumerate(word):
    #         print(
    #             "\n",
    #             word[:index_of_symbol],
    #             symbol,
    #             # word[index_of_symbol],
    #             word[index_of_symbol:],
    #             word[index_of_symbol:][::-1],
    #             # f"if exists word that begin on: (1){word[index_of_symbol:][::-1]} replace this on {compare_words(word[:index_of_symbol] + symbol, word[index_of_symbol:][::-1])}"
    #             # f"if exists word that begin on: (1){word[index_of_symbol:][::-1]} replace this on (2){word[:index_of_symbol] + symbol} if 2 < 1 {word[:index_of_symbol] + symbol < word[index_of_symbol:][::-1]}"
    #         )
    #         shortest_word = min_word_using_special_order(
    #             word[:index_of_symbol] + symbol,
    #             word[index_of_symbol:][::-1]
    #         )
    #         print(
    #             "Shortest word: ",
    #             shortest_word,
    #             f"\nif shortest_word != word_index_symbol then if exists word that begin on: {word[:index_of_symbol] + symbol} replace this on {min_word_using_special_order(word[:index_of_symbol] + symbol, word[index_of_symbol:][::-1])}",
    #             f"\nif exists word that ended on {''.join(reversed(word[:index_of_symbol] + symbol))} replace this on shortest word"
    #         )
    #         # 3.1
    #         if shortest_word != word[:index_of_symbol] + symbol:
    #             for i, row in enumerate(compressed_pair):
    #                 for j, w in enumerate(row):
    #                     if w == word:
    #                         continue
    #                     if w.startswith(word[:index_of_symbol] + symbol):
    #                         print("ZAMENA 3.1 UDALENO: ", compressed_pair[i][j])
    #                         compressed_pair[i][j] = w.replace(word[:index_of_symbol] + symbol, shortest_word)
    #                         print("ZAMENA 3.1 ZAMENENO: ", compressed_pair[i][j])
    #
    #             # # 3.2
    #             for idx, ww in enumerate(compressed_pair[0]):
    #                 if ww == word:
    #                     continue
    #                 if ww.endswith(''.join(reversed(word[:index_of_symbol] + symbol))):
    #                     print("ZAMENA 3.2 UDALENO: ", compressed_pair[0][idx])
    #                     compressed_pair[0][idx] = ww.replace(
    #                         ''.join(reversed(word[:index_of_symbol] + symbol)),
    #                         shortest_word[::-1]
    #                     )
    #                     print("ZAMENA 3.2 ZAMENENO: ", compressed_pair[0][idx])

            # # 3.2
            # for idx, ww in enumerate(compressed_pair[0]):
            #     if ww == word:
            #         continue
            #     if ww.endswith(''.join(reversed(word[:index_of_symbol] + symbol))):
            #         print("ZAMENA 3.2 UDALENO: ", compressed_pair[0][idx])
            #         compressed_pair[0][idx] = ww.replace(
            #             ''.join(reversed(word[:index_of_symbol] + symbol)),
            #             shortest_word[::-1]
            #         )
            #         print("ZAMENA 3.2 ZAMENENO: ", compressed_pair[0][idx])

            # 1 нужно уточнить операции для каждой компоненти
            # STEP 3
            # 3.1. итериюсь по каждой букве из C .... а проверяю в C L на начала слов
            # для С: проверки начинается(!) С L -> C + L => CL ... п
            #
            # 3.2. проверка конца клиент
            #  0132134510
            # все что заканчивается на 312310 заменяем на 34510 только в клиентах из С
            # ..... заканчивается ???
            # 3 для L: только то что начинается

    # print("\nSTEP 3 stopped:\n ")
    # # 4 (обе компоненты) убираем повторы, оставляем 1 экз.
    # # check each component for words repeating
    # for pair_component in compressed_pair:
    #     pair_component[:] = list(set(pair_component))
    #
    # # check 5 if len(word_c) == 1 then kick this word
    # print("\nDEBUG COMPRESSION AFTER 4 STEP: \n", compressed_pair)
    #
    # # Define a custom sorting key function
    # def custom_sort_key(s):
    #     return len(s), s
    #
    # sorted_list = sorted(compressed_pair[0], key=custom_sort_key)
    # # Print the sorted list
    # print("\nSORTED C: ", sorted_list)

    return compressed_pair
