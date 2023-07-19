""" IAMM - Graphs - ASP Work """
from typing import Tuple, List, Union, Dict
from math import ceil, sqrt
import networkx as nx # type: ignore

# =========================== HELPERS FUNCTIONS ===============================
def counter():
    """helper for AP alg. generate IDs for nodes"""
    if not hasattr(counter, 'count'):
        counter.count = 0
    counter.count += 1
    return counter.count


def get_all_leaf_nodes_from_graph(G: nx.Graph) -> dict:
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


def walk_by_word( graph: nx.Graph,
          word: str,
          root_node: int ) -> int:
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


def ap_graph(C:tuple, L:tuple, x_='1') -> Union[nx.Graph, str]:
    """ build graph on pair of words, algorithm AP """
    # =============================== STEP 0 ======================================
    q: Dict = {}
    trash: Dict = {}
    root = 0
    check_leaf_node = None
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
    # =============== STEP 2 Get all leaf nodes from the graph ====================
    q = get_all_leaf_nodes_from_graph(G)
    # ============= STEP 3 Add nodes for L and check if the graph is valid ========
    for l_word in L:
        if l_word[0] != x_:
            raise ValueError("Incorrect data. Graph is not exists!")
        for index, label in enumerate(l_word[1:], start=1):
            node_id = counter()
            G.add_node(node_id, label=label)
            if index == 1:
                G.add_edge(root, node_id)
            else:
                G.add_edge(node_id - 1, node_id)
            if index == len(l_word) - 1:
                check_leaf_node = node_id
        G = ar_nodes(G)
        if G.has_node(check_leaf_node):
            if G.degree(check_leaf_node) != 1:
                raise ValueError("Incorrect data. Graph is not exists!")
        all_leafs = get_all_leaf_nodes_from_graph(G)
        for key_id, val_label in all_leafs.items():
            if val_label != l_word[-1] \
                    and key_id not in q and key_id not in trash:
                q[key_id] = val_label
            else:
                trash[key_id] = val_label
    # =================== STEP 4 Check if the graph is valid ======================
    for key_id, val_label in q.items():
        all_paths = list(nx.all_simple_paths(G, source=root, target=key_id))
        all_paths_labels = ["".join([G.nodes[id]['label'] for id in path]) for path in all_paths]
        print(key_id, val_label, all_paths_labels)
        checked = False
        for path in all_paths_labels:
            for word in L:
                if path in word:
                    checked = True
        if not checked:
            print("Incorrect data. Graph is not exists!")
    # ========== STEP 5 Check if each word in L ends with a hanging vertex ========
    for p_word_index, p_word in enumerate(L):
        checked_node = walk_by_word(G, p_word, root)
        if G.degree(checked_node) != 1:
            print(f"""Incorrect data, invalid pair.
            \nWord {p_word_index + 1} in the set L does not end with a hanging vertex.
            \nGraph is not exists!""")

    return G


def ak_pair(graph: nx.Graph) -> Union[Tuple[List[str], List[str]], int, str]:
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
        for q_path in ni[index+1:]:
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

# ================ CANONICAL PAIR METRICS DEV IN PROGRESS =====================
def get_pair_metrics(n: int, m: int) -> Dict:
    """ find canonical pair metrics """
    mat = ceil(3/2 + sqrt(9/4 - 2 * n + 2 * m))
    result = 2 * (m - n + 1) * (n - mat + 2)
    return {"mat": mat, "result": result}
