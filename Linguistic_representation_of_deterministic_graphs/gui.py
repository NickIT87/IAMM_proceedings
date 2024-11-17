import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import warnings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from networkx.drawing.nx_pydot import to_pydot

from DataBenchmarks.data import random_color
from AlgorithmsLibraries.alglib_version_02_current import *


warnings.filterwarnings("ignore", category=DeprecationWarning, module="networkx")

def on_closing():
    # Add any cleanup or save operations here before closing the window
    print("Window is being closed...")
    #root.destroy()
    root.quit()


def get_info():
    c_string = c_text.get()
    l_string = l_text.get()
    return (tuple(c_string.split()), tuple(l_string.split()), r_text.get())


def update_text_area(graph=None, message=None):
    if graph:
        data = get_canonical_pair_metrics_from_dgraph(graph)
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)  # Clear existing text
        text_area.insert(tk.END, data)  # Insert new text
        text_area.config(state=tk.DISABLED)  # Disable editing
    else:
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)  # Clear existing text
        text_area.insert(tk.END, message)  # Insert new text
        text_area.config(state=tk.DISABLED)  # Disable editing


def build_graph():
    clear_output()
    global G
    data = get_info()
    try:
        G = ap_graph(data[0], data[1], data[2])
        # Set the node labels
        labels = nx.get_node_attributes(G, 'label')
        # Get the node colors
        try:
            node_colors = [G.nodes[node]['color'] for node in G.nodes]
        except KeyError:
            node_colors = [random_color() for _ in range(len(G.nodes) - 1)]
            node_colors.insert(0, "red")
        T = nx.minimum_spanning_tree(G)
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4))
        # Draw the original graph on the first subplot (ax1)
        pos = nx.spring_layout(G)  # positions for the nodes
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
        if hasattr(build_graph, 'canvas'):  # Check if canvas already exists and delete it
            build_graph.canvas.get_tk_widget().destroy()
        build_graph.canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        build_graph.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        build_graph.canvas.draw()
        if hasattr(build_graph, 'toolbar'):  # Check if toolbar already exists and delete it
            build_graph.toolbar.destroy()
        build_graph.toolbar = NavigationToolbar2Tk(build_graph.canvas,
                                                   graph_frame,
                                                   pack_toolbar=False)
        build_graph.toolbar.update()
        build_graph.toolbar.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        update_text_area(graph=G)
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


def compress_pair():
    data = get_info()
    compressed_pair = compression(data[0], data[1], no_gdp=False)
    update_text_area(message=compressed_pair)


def save_graph_to_file():
    global G
    try:
        file_path = 'outputData/example.gml'
        nx.write_gml(G, file_path)
        dot_graph = to_pydot(G)
        dot_graph.write_dot("outputData/graph.dot")
        dot_string = dot_graph.to_string()
        try:
            with open('outputData/simple.dot', 'w') as file:
                # Step 2: Write the string to the file
                file.write(dot_string)
            update_text_area(message="Graph successfully written to files.")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred while writing to the file. {e}")
    except NameError as e:
        messagebox.showerror("Error", f"Graph is not exists {e}")


def save_info():
    global text_area
    data = text_area.get("1.0", tk.END)
    try:
        with open('outputData/info.txt', 'w') as file:
            # Step 2: Write the string to the file
            file.write(data)
        update_text_area(message="data successfully written to file.")
    except IOError as e:
        messagebox.showerror("Error", f"An error occurred while writing to the file. {e}")


def clear_output():
    plt.close()
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)
    text_area.config(state=tk.DISABLED)  # Disable editing
    if hasattr(build_graph, 'canvas'):  # Check if canvas already exists and delete it
        build_graph.canvas.get_tk_widget().destroy()
    if hasattr(build_graph, 'toolbar'):  # Check if toolbar already exists and delete it
        build_graph.toolbar.destroy()


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = ((screen_height - height) // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")


def create_widgets(root):
    global text_area, graph_frame, c_text, l_text, r_text, G
    text_field_width = 70
    button_distance = 10
    label_frame = tk.Frame(root)
    label_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    r_label = tk.Label(label_frame, text="root label:")
    r_label.grid(row=0, column=0, padx=10, pady=10)
    r_text = tk.Entry(label_frame, width=1)
    r_text.insert(0, "1")
    r_text.grid(row=0, column=1, padx=10, pady=10)
    c_label = tk.Label(label_frame, text="Sigma G:")
    c_label.grid(row=1, column=0, padx=10, pady=10)
    c_text = tk.Entry(label_frame, width=text_field_width)
    c_text.grid(row=1, column=1, padx=10, pady=10)
    l_label = tk.Label(label_frame, text="Lambda G:")
    l_label.grid(row=2, column=0, padx=10, pady=10)
    l_text = tk.Entry(label_frame, width=text_field_width)
    l_text.grid(row=2, column=1, padx=10, pady=10)
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    # build btn
    build_button = tk.Button(button_frame, text="Build Graph", command=build_graph)
    build_button.grid(row=0, column=0, padx=button_distance)
    # compress btn
    compress_button = tk.Button(button_frame, text="Compress pair", command=compress_pair)
    compress_button.grid(row=0, column=1, padx=button_distance)
    # save btn
    save_button = tk.Button(button_frame, text="Save graph to file", command=save_graph_to_file)
    save_button.grid(row=0, column=2, padx=button_distance)
    # save info btn
    save_info_button = tk.Button(button_frame, text="Save info to file", command=save_info)
    save_info_button.grid(row=0, column=3, padx=button_distance)
    # clear btn
    clear_button = tk.Button(button_frame, text="Clear output", command=clear_output)
    clear_button.grid(row=0, column=4, padx=button_distance)
    text_frame = tk.Frame(root)
    text_frame.grid(row=2, column=0, sticky='W', columnspan=2, padx=10, pady=10)
    info_label = tk.Label(text_frame, text="Info output:")
    info_label.grid(row=0, column=0, padx=10, pady=10)
    text_area = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 15), state=tk.DISABLED, height=5, width=71)
    text_area.grid(row=0, column=1)
    graph_frame = tk.Frame(root)
    graph_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def main():
    global root
    root = tk.Tk()
    root.title("Linguistic Representation of Deterministic Graphs")
    window_width = 800
    window_height = 800
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    center_window(root, window_width, window_height)
    create_widgets(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
