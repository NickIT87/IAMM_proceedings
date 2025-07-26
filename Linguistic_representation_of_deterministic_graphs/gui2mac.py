import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import warnings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from networkx.drawing.nx_pydot import to_pydot

from AlgorithmsLibraries.debug_helpers import random_color
from AlgorithmsLibraries.alglib_prod_version_1_0_0 import *

warnings.filterwarnings("ignore", category=DeprecationWarning, module="networkx")

def on_closing():
    print("Window is being closed...")
    root.quit()

def get_info():
    c_string = c_text.get()
    l_string = l_text.get()
    return (tuple(c_string.split()), tuple(l_string.split()), r_text.get(), fsp_text.get())

def update_text_area(graph=None, message=None):
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)
    if graph:
        data = get_canonical_pair_metrics_from_dgraph(graph)
        text_area.insert(tk.END, data)
    elif message:
        text_area.insert(tk.END, message)
    text_area.config(state=tk.DISABLED)

def build_graph():
    clear_output()
    global G
    data = get_info()
    try:
        G = ap_graph(data[0], data[1], data[2])
        labels = nx.get_node_attributes(G, 'label')

        try:
            node_colors = [G.nodes[node]['color'] for node in G.nodes]
        except KeyError:
            node_colors = [random_color() for _ in range(len(G.nodes) - 1)]
            node_colors.insert(0, "red")

        T = nx.minimum_spanning_tree(G)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4))

        # pos = nx.spring_layout(G)
        # nx.draw_networkx(G, pos, labels=labels, node_color=node_colors, ax=ax1)
        # ax1.set_title('Original Graph')
        # ax1.axis('off')
        #
        # pos = nx.spring_layout(T)
        # nx.draw_networkx(T, pos, node_color=node_colors, ax=ax2)
        # ax2.set_title('Minimum Spanning Tree')
        # ax2.axis('off')

        # Draw the original graph on the first subplot (ax1)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax1)  # type: ignore
        nx.draw_networkx_edges(G, pos, edge_color='b', ax=ax1)
        nx.draw_networkx_labels(G, pos, labels, ax=ax1)
        ax1.set_title('Original Graph')
        # Draw the minimum spanning tree on the second subplot (ax2)
        pos = nx.spring_layout(T)  # positions for the nodes
        nx.draw_networkx_nodes(T, pos, node_color=node_colors, ax=ax2)  # type: ignore
        nx.draw_networkx_edges(T, pos, edge_color='b', ax=ax2)
        nx.draw_networkx_labels(T, pos, ax=ax2)
        ax2.set_title('Minimum Spanning Tree')
        # Remove the axis ticks and labels
        ax1.axis('off')
        ax2.axis('off')

        if hasattr(build_graph, 'canvas'):
            build_graph.canvas.get_tk_widget().destroy()
        build_graph.canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        build_graph.canvas.get_tk_widget().pack(padx=10, pady=10)
        build_graph.canvas.draw()

        if hasattr(build_graph, 'toolbar'):
            build_graph.toolbar.destroy()
        build_graph.toolbar = NavigationToolbar2Tk(build_graph.canvas, graph_frame)
        build_graph.toolbar.update()
        build_graph.toolbar.pack(padx=10, pady=5)

        update_text_area(graph=G)
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def compress_pair():
    data = get_info()
    compressed_pair = compression(data[0], data[1], no_gdp=False)
    fsp_result = find_shortest_path_by_word(data[3], list(compressed_pair['compressed_pair'][0]))
    result = f"{compressed_pair} \n Shortest path by word compression: {fsp_result}"
    update_text_area(message=result)

def save_graph_to_file():
    global G
    try:
        file_path = 'outputData/example.gml'
        nx.write_gml(G, file_path)
        dot_graph = to_pydot(G)
        dot_graph.write_dot("outputData/graph.dot")
        with open('outputData/simple.dot', 'w') as file:
            file.write(dot_graph.to_string())
        update_text_area(message="Graph successfully written to files.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_info():
    data = text_area.get("1.0", tk.END)
    try:
        with open('outputData/info.txt', 'w') as file:
            file.write(data)
        update_text_area(message="Data successfully written to file.")
    except IOError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_output():
    plt.close()
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)
    text_area.config(state=tk.DISABLED)
    if hasattr(build_graph, 'canvas'):
        build_graph.canvas.get_tk_widget().destroy()
    if hasattr(build_graph, 'toolbar'):
        build_graph.toolbar.destroy()

def create_widgets(parent):
    global text_area, graph_frame, c_text, l_text, r_text, fsp_text, G
    text_field_width = 70
    button_distance = 10

    label_frame = tk.Frame(parent)
    label_frame.pack(fill="x", padx=10, pady=10)

    r_label = tk.Label(label_frame, text="root label:")
    r_label.grid(row=0, column=0, padx=5, pady=5)
    r_text = tk.Entry(label_frame, width=1)
    r_text.insert(0, "1")
    r_text.grid(row=0, column=1, padx=5, pady=5)

    fsp_label = tk.Label(label_frame, text="FSP word:")
    fsp_label.grid(row=0, column=2, padx=5, pady=5)
    fsp_text = tk.Entry(label_frame, width=50)
    fsp_text.grid(row=0, column=3, columnspan=2, padx=5, pady=5)

    c_label = tk.Label(label_frame, text="Sigma G:")
    c_label.grid(row=1, column=0, padx=5, pady=5)
    c_text = tk.Entry(label_frame, width=text_field_width)
    c_text.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="we")

    l_label = tk.Label(label_frame, text="Lambda G:")
    l_label.grid(row=2, column=0, padx=5, pady=5)
    l_text = tk.Entry(label_frame, width=text_field_width)
    l_text.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="we")

    button_frame = tk.Frame(parent)
    button_frame.pack(fill="x", padx=10, pady=10)
    tk.Button(button_frame, text="Build Graph", command=build_graph).pack(side="left", padx=button_distance)
    tk.Button(button_frame, text="Compress pair", command=compress_pair).pack(side="left", padx=button_distance)
    tk.Button(button_frame, text="Save graph to file", command=save_graph_to_file).pack(side="left", padx=button_distance)
    tk.Button(button_frame, text="Save info to file", command=save_info).pack(side="left", padx=button_distance)
    tk.Button(button_frame, text="Clear output", command=clear_output).pack(side="left", padx=button_distance)

    text_frame = tk.Frame(parent)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)
    info_label = tk.Label(text_frame, text="Info output:")
    info_label.pack(anchor="w")
    text_area = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 16), state=tk.DISABLED, height=7, width=70)
    text_area.pack(fill="both", expand=True)

    graph_frame = tk.Frame(parent)
    graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

def main():
    global root
    root = tk.Tk()
    root.title("Linguistic Representation of Deterministic Graphs")

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    create_widgets(scrollable_frame)

    root.geometry("800x870")
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
