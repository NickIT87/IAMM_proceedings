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