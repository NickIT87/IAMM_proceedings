def print_dgraph(g, name="no name graph"):
    print(f"========={name}===========")
    print("Nodes:", g.nodes)
    print("Edges: ", g.edges)
    try:
        glabels = []
        for node in g.nodes:
            glabels.append(g.nodes[node]['label'])
        print("labels: ", glabels)
    except:
        pass

#
# def get_nodes_shortest_paths_of_labeled_dgraph(
#         dgraph: nx.Graph, root: int, root_label
# ) -> Dict[int, Dict[str, Union[str, List[int], None]]]:
#     """ acrobatic tree IN PROGRESS need to rename function """
#     # DECLARE & INIT VALUES
#     ids: List[int] = list(dgraph.nodes)  # id of each node list
#     glabels: List[str] = []  # labels for graph
#     nodes_shortest_paths: Dict[
#         int, Dict[str, Union[str, List[int], None]]
#     ] = {}  # main object Nodes Shortest Path
#     for node, label in dgraph.nodes(data='label'):
#         nodes_shortest_paths[node] = {"npl": None, "npid": None}
#         glabels.append(label)
#
#     # cycle variables
#     alphabet = list(set(glabels))
#     alphabet.sort()
#     current_array_index: int = 0
#     vertex_count_result: int = 0
#
#     # STEP 1 get labels paths variables
#     labeled_short_path: str
#     shortest_words: List[str] = list()
#     shortest_words.append(root_label)
#     nodes_shortest_paths[root]['npl'] = root_label
#
#     # STEP 2 get ids paths variables
#     shortest_words_ids: List[List[int]] = list()
#     shortest_words_ids.append([root])
#     nodes_shortest_paths[root]['npid'] = [root]
#     current_node_shortest_paths_by_ids: List[int] = [root]
#
#     while vertex_count_result < len(ids) - 1:
#         for j in alphabet:
#             labeled_short_path = shortest_words[current_array_index] + j
#             try:
#                 obtained_node = get_node_id_by_word(dgraph, labeled_short_path, root)
#                 if nodes_shortest_paths[obtained_node]["npl"] is None and obtained_node != root:
#                     nodes_shortest_paths[obtained_node]["npl"] = labeled_short_path
#                     result_node_shortest_path_by_ids = deepcopy(current_node_shortest_paths_by_ids)
#                     result_node_shortest_path_by_ids.append(obtained_node)
#                     shortest_words_ids.append(result_node_shortest_path_by_ids)
#                     nodes_shortest_paths[obtained_node]["npid"] = result_node_shortest_path_by_ids
#                     vertex_count_result += 1
#                     shortest_words.append(labeled_short_path)
#             except ValueError:
#                 continue
#         current_array_index += 1
#         current_node_shortest_paths_by_ids = shortest_words_ids[current_array_index]
#
#     return nodes_shortest_paths