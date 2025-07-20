""" helpers functions for alglib debug and IO of functions results"""
import os
import random
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot
import matplotlib.pyplot as plt     # type: ignore


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


def save_graph_to_file(G, output_dir='outputData'):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    try:
        # Save in GML format
        gml_path = os.path.join(output_dir, 'example.gml')
        nx.write_gml(G, gml_path)

        # Convert to DOT format using pydot
        dot_graph = to_pydot(G)

        # Save as .dot file
        dot_path = os.path.join(output_dir, 'graph.dot')
        dot_graph.write_dot(dot_path)

        # Save DOT string explicitly
        dot_string = dot_graph.to_string()
        simple_dot_path = os.path.join(output_dir, 'simple.dot')
        with open(simple_dot_path, 'w') as file:
            file.write(dot_string)

    except (IOError, OSError, nx.NetworkXException, Exception) as e:
        print(f"Error saving graph: {e}")

    finally:
        print("Graph saving process finished.")


def random_color():
    red = random.randint(100, 255)
    green = random.randint(100, 255)
    blue = random.randint(100, 255)
    hex_color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    return hex_color


def print_data(G):
    # Set the node labels
    labels = nx.get_node_attributes(G, 'label')
    id_labels = labels.copy()
    for key, value in labels.items():
        id_labels[key] = f"{value}\n{key}"

    try:
        node_colors = [G.nodes[node]['color'] for node in G.nodes]
    except KeyError:
        node_colors = [random_color() for _ in range(len(G.nodes)-1)]
        node_colors.insert(0, "red")
    #T = nx.minimum_spanning_tree(G)
    mst_edges = list(nx.bfs_edges(G, source=list(G.nodes)[0]))
    T = G.edge_subgraph(mst_edges)
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    # Draw the original graph on the first subplot (ax1)
    pos = nx.spring_layout(G)  # positions for the nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax1)  # type: ignore
    nx.draw_networkx_edges(G, pos, edge_color='b', ax=ax1)
    nx.draw_networkx_labels(G, pos, labels, ax=ax1)
    try:
        ax1.set_title('Original Graph: ' + G.name)
    except:
        ax1.set_title('Original Graph: ' + "No name")

    # Draw the minimum spanning tree on the second subplot (ax2)
    pos = nx.spring_layout(T)  # positions for the nodes
    nx.draw_networkx_nodes(T, pos, node_color=node_colors, ax=ax2)  # type: ignore
    nx.draw_networkx_edges(T, pos, edge_color='b', ax=ax2)
    nx.draw_networkx_labels(T, pos, id_labels, ax=ax2)
    try:
        ax2.set_title('Minimum spanning tree of: ' + T.name)
    except:
        ax2.set_title('Minimum spanning tree of: ' + "No name")
    # Remove the axis ticks and labels
    ax1.axis('off')
    ax2.axis('off')
    # Adjust the spacing between subplots
    plt.tight_layout()
    # Show the graph
    plt.show()
