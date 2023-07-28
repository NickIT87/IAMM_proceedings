import networkx as nx
import matplotlib.pyplot as plt


def create_flower_graph(num_vertices):
    G = nx.Graph()
    # Add vertices from 0 to num_vertices + 1
    G.add_nodes_from(range(num_vertices + 2))
    # Add 'label' attribute to each vertex with the string value of the vertex number
    for i in range(num_vertices + 2):
        G.nodes[i]['label'] = str(i)
    # Create edges to form the path from 0 to num_vertices + 1
    for i in range(num_vertices + 1):
        G.add_edge(i, i + 1)
    # Create a complete graph starting from vertex 2
    G.add_edges_from((i, j) for i in range(2, num_vertices + 2) for j in range(i + 1, num_vertices + 2))
    return G


def create_custom_graph(num_vertices):
    G = nx.Graph()
    # Add vertices from 0 to num_vertices
    G.add_nodes_from(range(num_vertices + 1))
    for i in range(num_vertices + 1):
        G.nodes[i]['label'] = str(i)
    # Create edges from vertex 0 to vertex 1
    G.add_edge(0, 1)
    # Create a complete graph starting from vertex 1
    G.add_edges_from((i, j) for i in range(1, num_vertices) for j in range(i + 1, num_vertices + 1))
    return G

# num_vertices = 6
# custom_graph = create_custom_graph(num_vertices)
#custom_graph = create_flower_graph(num_vertices)

# Draw the graph
# plt.figure(figsize=(12, 8))
# pos = nx.spring_layout(custom_graph, seed=42)  # Adjust the layout for better visualization
# nx.draw(custom_graph, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=8, font_weight='bold')
# plt.title("Custom Graph with 50 vertices")
# plt.show()
