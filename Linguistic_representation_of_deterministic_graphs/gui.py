import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data import random_color
from alglib import *


def on_closing():
    # Add any cleanup or save operations here before closing the window
    print("Window is being closed...")
    #root.destroy()
    root.quit()


def get_info():
    c_string = c_text.get()
    l_string = l_text.get()
    return (tuple(c_string.split()), tuple(l_string.split()), r_text.get())


def build_graph():
    data = get_info()
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 5))
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


def update_text_area():
    text = "This is a big text area.\n"
    text += "You can display large amounts of text here.\n"
    text += "It supports multiple lines and scrollbars.\n"
    text += "You can add more text programmatically as well."
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)  # Clear existing text
    text_area.insert(tk.END, text)  # Insert new text
    text_area.config(state=tk.DISABLED)  # Disable editing


def clear_output():
    text_area.config(state=tk.NORMAL)
    text_area.delete("1.0", tk.END)
    text_area.config(state=tk.DISABLED)  # Disable editing


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = ((screen_height - height) // 2) - 10
    root.geometry(f"{width}x{height}+{x}+{y}")


def create_widgets(root):
    global text_area, graph_frame, c_text, l_text, r_text
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

    build_button = tk.Button(button_frame, text="Build Graph", command=build_graph)
    build_button.grid(row=0, column=0, padx=button_distance)

    save_button = tk.Button(button_frame, text="Save graph to file", command=get_info)
    save_button.grid(row=0, column=1, padx=button_distance)

    save_button = tk.Button(button_frame, text="Save info to file", command=update_text_area)
    save_button.grid(row=0, column=2, padx=button_distance)

    clear_button = tk.Button(button_frame, text="Clear output", command=clear_output)
    clear_button.grid(row=0, column=3, padx=button_distance)

    text_frame = tk.Frame(root)
    text_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    info_label = tk.Label(text_frame, text="Info output:")
    info_label.grid(row=0, column=0, padx=10, pady=10)

    text_area = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED, height=5)
    text_area.grid(row=0, column=1)

    graph_frame = tk.Frame(root)
    graph_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def main():
    global root
    root = tk.Tk()
    root.title("Linguistic Representation of Deterministic Graphs")
    window_width = 800
    window_height = 850
    root.geometry(f"{window_width}x{window_height}")
    center_window(root, window_width, window_height)

    create_widgets(root)

    # Bind the on_closing function to the window close event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()
