# import cProfile
# import pstats

# import networkx as nx

from DataBenchmarks.data import print_data, sample, TestCases as T
from DataBenchmarks.flowerGraph import *
from AlgorithmsLibraries.alglib_version_02_current import *
# from AlgorithmsLibraries.debug_helpers import *
# import scipy


# Run function
def run_test_flow():
    # G = ap_graph(T.sample.defining_pair.C, T.sample.defining_pair.L, T.sample.root_label)
    # F = ap_graph(T.sample.canonical_pair.C, T.sample.canonical_pair.L, T.sample.root_label)
    # print(ac_pair(G))
    # print(ac_pair(F))
    # G.name = "G (dpair)"
    # F.name = "F (canonical)"
    # print("=======SPANING TREEE=========")
    # print(get_nodes_shortest_paths_of_dgraph(G, root=0, root_label="0"))
    #
    # isomorphic = nx.is_isomorphic(G, F)
    # mst_edges_g = list(nx.dfs_edges(G, source=list(G.nodes)[0]))
    # mst_edges_f = list(nx.dfs_edges(F, source=list(F.nodes)[0]))
    #
    # Gt = G.edge_subgraph(mst_edges_g)
    # Ft = F.edge_subgraph(mst_edges_f)
    # isomorphic_t = nx.is_isomorphic(Gt, Ft)
    #
    # print(isomorphic, isomorphic_t)
    # ================= COMPRESSION =======================
    print(
        "\n==== DEBUG COMPRESSION ====\nCANONICAL PAIR:\n",
        T.sample.canonical_pair.C,
        T.sample.canonical_pair.L,
        "\n"
    )
    print(
        "\nRETURNED DATA: \n",
        compression(T.sample.defining_pair.C, T.sample.defining_pair.L),
        "\nCANONICAL PAIR: ",
        T.sample.canonical_pair.C,
        T.sample.canonical_pair.L,
        "\n"
    )


# =============================================================================
if __name__ == "__main__":
    #run_test_flow()
    G = ap_graph(sample[0], sample[1], "1")
    acpair = ac_pair(G)
    compressed_pair = compression(sample[0], sample[1])

    #print_data(G)
    print("AC pair: ", acpair)
    print("Compression: ", compressed_pair)

    print(acpair == compressed_pair)

    # ============================= PAIR METRICS ==============================
    # print(get_canonical_pair_metrics_from_dgraph(G))
    # # print_data(G)
    #
    # MyGraph = create_custom_graph(6)
    # print(get_canonical_pair_metrics_from_dgraph(MyGraph))
    # # print_data(MyGraph)
    #
    # edges_to_remove = [(1, 5), (1, 6)]
    # MyGraph.remove_edges_from(edges_to_remove)
    # print(get_canonical_pair_metrics_from_graph(MyGraph))
    # # print_data(MyGraph)
    #
    # BigG = create_custom_graph(9)
    # e_to_r = [(1, 5), (1, 6)]
    # BigG.remove_edges_from(e_to_r)
    # print(get_canonical_pair_metrics_from_graph(BigG))
    # # print_data(BigG)
    #
    # BigG2 = create_custom_graph(50)
    # e_to_r2 = [(1, 5), (1, 6)]
    # BigG2.remove_edges_from(e_to_r2)
    # print(get_canonical_pair_metrics_from_graph(BigG2))
    # print_data(BigG2)

    # BigG3 = create_flower_graph(num_vertices=50, path=5)
    # # e_to_r3 = [(1, 5), (1, 6)]
    # e_to_r3 = [(5, 7), (5, 18), (5, 31)]
    # BigG3.remove_edges_from(e_to_r3)
    # print(get_canonical_pair_metrics_from_graph(BigG3))
    # print_data(BigG3)
    # ============================== C PROFILER ===============================
    # G = ap_graph(testC1, testL1)
    # cProfile.run('ap_graph(testC1, testL1)', filename='testingResults/cprofile_results/ap_profile_results')
    # cProfile.run('ac_pair(G)', filename='ac_profile_results')
    # stats1 = pstats.Stats('testingResults/cprofile_results/ac_profile_results')
    # stats2 = pstats.Stats('testingResults/cprofile_results/ap_profile_results')
    # stats1.strip_dirs().sort_stats('time').print_stats()
    # stats2.strip_dirs().sort_stats('time').print_stats()
