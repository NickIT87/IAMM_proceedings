import sys
import time
from pathlib import Path
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from DataBenchmarks.data import TestCases as T
from AlgorithmsLibraries.lpdg_dev import *

def fsp_timing_estimate(dC, dL, dW):
    canonical_pair = compression(
        dC,
        dL
    )
    canonical_pair = list(canonical_pair['compressed_pair'][0])
    start = time.perf_counter()
    spath = find_shortest_path_by_word(
        dW,
        canonical_pair
    )
    elapsed = time.perf_counter() - start
    print(spath)
    print(f"FSP timing: {elapsed:.8f} sec")


def ap_and_bfs_timing_estimate(dC, dL, dR):
    start = time.perf_counter()
    G = ap_graph(dC, dL, dR)
    sp = nx.shortest_path(G, source=0, target=34)
    elapsed = time.perf_counter() - start
    print(f"AP timing: {elapsed:.8f} sec")
    print(sp)
    

ap_and_bfs_timing_estimate(T.shortPathCase.defining_pair.C, T.shortPathCase.defining_pair.L, "0")
fsp_timing_estimate(T.shortPathCase.defining_pair.C, T.shortPathCase.defining_pair.L, '03115241130210530120311423')