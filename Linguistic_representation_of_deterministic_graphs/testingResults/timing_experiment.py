import sys
import time
from pathlib import Path
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from DataBenchmarks.data import TestCases as T
from AlgorithmsLibraries.lpdg_dev import *
from agent import GraphAPI, Agent

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
    print(f"FSP path: {spath}")
    print(f"FSP timing: {elapsed:.8f} sec")
    return spath


def ap_and_bfs_timing_estimate(dC, dL, dR):
    start = time.perf_counter()
    G = ap_graph(dC, dL, dR)
    sp = nx.shortest_path(G, source=0, target=34)
    elapsed = time.perf_counter() - start
    print(f"AP timing: {elapsed:.8f} sec")
    print(sp)


def get_target(dGraph, fsp_word, start_node=0):
    api = GraphAPI(dGraph, start_node)
    agent = Agent(api)
    target = agent.walk_by_word(fsp_word)
    print(f"Visited nodes by agent: {agent.visited_by_walk}")
    return target


def universal_timing_estimate(dC, dL, dR, dW):
    
    start = time.perf_counter()
    G = ap_graph(dC, dL, dR)
    ap_timing = time.perf_counter() - start
    print(f"AP timing: {ap_timing:.8f} sec")
    
    trgt = get_target(
        dGraph=G,
        fsp_word=fsp_timing_estimate(dC, dL, dW)
    )
    
    start = time.perf_counter()
    sp = nx.shortest_path(G, source=0, target=trgt)
    bfs_timing = time.perf_counter() - start
    print(f"Shortest path by BFS: {sp}")
    print(f"BFS timing: {bfs_timing:.8f} sec")
    elapsed = ap_timing + bfs_timing
    print(f"AP & BFS total timing: {elapsed:.8f} sec")
    

 
if __name__ == "__main__":
    universal_timing_estimate(T.shortPathCase.defining_pair.C, T.shortPathCase.defining_pair.L, "0", '03115241130210530120311423')
    # ap_and_bfs_timing_estimate(T.shortPathCase.defining_pair.C, T.shortPathCase.defining_pair.L, "0")
    # fsp_timing_estimate(T.shortPathCase.defining_pair.C, T.shortPathCase.defining_pair.L, '03115241130210530120311423')
