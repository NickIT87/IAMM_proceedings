""" simple graph traversal agent """

import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from AlgorithmsLibraries.alglib_version_02_current import *
from DataBenchmarks.data import publication_sample


# === 1. GraphAPI ===
class GraphAPI:
    def __init__(self, graph, start_node):
        self._graph = graph
        self._current_position = start_node

    def get_position(self):
        return self._current_position

    def get_neighbors(self):
        return list(self._graph.neighbors(self._current_position))

    def move_to(self, node):
        if node in self.get_neighbors():
            self._current_position = node
            return True
        return False


# === 2. Agent ===
class Agent:
    def __init__(self, api):
        self.api = api

    def move(self):
        neighbors = self.api.get_neighbors()
        if neighbors:
            self.api.move_to(random.choice(neighbors))

    def get_position(self):
        return self.api.get_position()


# === 3. Animation functions ===
def init():
    ax.clear()
    agent_pos = agent.get_position()
    print(f"[init] Agent in {agent_pos}")

    raw_labels = nx.get_node_attributes(G, 'label')
    labels = {node: f"{raw_labels.get(node, '')}\n{node}" for node in G.nodes}

    try:
        node_colors = [G.nodes[node]['color'] for node in G.nodes]
    except KeyError:
        node_colors = ['lightgray'] * len(G.nodes)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=9)
    nx.draw_networkx_nodes(G, pos, nodelist=[agent_pos], node_color="red", node_size=500, ax=ax)

    ax.set_title(f"Step 0, Agent in {agent_pos}")
    ax.set_axis_off()

    return []


def update(frame):
    """animation step"""
    ax.clear()
    agent_pos = agent.get_position()
    print(f"Step {frame}, Agent in {agent_pos}")

    raw_labels = nx.get_node_attributes(G, 'label')
    labels = {node: f"{raw_labels.get(node, '')}\n{node}" for node in G.nodes}

    try:
        node_colors = [G.nodes[node]['color'] for node in G.nodes]
    except KeyError:
        node_colors = ['lightgray'] * len(G.nodes)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=9)
    nx.draw_networkx_nodes(G, pos, nodelist=[agent_pos], node_color="red", node_size=500, ax=ax)

    ax.set_title(f"Step {frame}, Agent in {agent_pos}")
    ax.set_axis_off()

    agent.move()

    return []


# === 4. start animation ===
G = ap_graph(publication_sample.C, publication_sample.L, "0")
start_node = 0
api = GraphAPI(G, start_node)
agent = Agent(api)

pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(6, 6))
ani = FuncAnimation(fig, update, frames=20, init_func=init, interval=1000, repeat=False)
plt.show()


# # LIVE DRAW
# # === Отрисовка одного шага (в одном окне) ===
# def draw_step_live(G, pos, agent, step_number, ax):
#     ax.clear()
#
#     # Получение подписей вида label\nid
#     raw_labels = nx.get_node_attributes(G, 'label')
#     labels = {node: f"{raw_labels.get(node, '')}\n{node}" for node in G.nodes}
#
#     # Цвета узлов
#     try:
#         node_colors = [G.nodes[node]['color'] for node in G.nodes]
#     except KeyError:
#         node_colors = ['lightgray'] * len(G.nodes)
#
#     # Рисуем граф
#     nx.draw_networkx_nodes(G, pos, node_color=node_colors, edgecolors='black', ax=ax)
#     nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
#     nx.draw_networkx_labels(G, pos, labels, font_size=9, ax=ax)
#
#     # Агент
#     agent_pos = agent.get_position()
#     nx.draw_networkx_nodes(G, pos, nodelist=[agent_pos], node_color='red', node_size=500, ax=ax)
#
#     ax.set_title(f"Шаг {step_number + 1}, Агент в {agent_pos}")
#     ax.set_axis_off()
#     print(f"[Шаг {step_number + 1}] Агент находится в: {agent.get_position()}")
#     plt.pause(2)
#
#
# # === Симуляция движения агента ===
# steps = 20
# for i in range(steps):
#     draw_step_live(G, pos, agent, i, ax)
#     agent.move()


# # MANUAL CLOSING
# # === Параметры ===
# steps = 20
#
# # === Отрисовка одного кадра ===
# def draw_step(G, pos, agent, step_number):
#     # Получение лейблов
#     raw_labels = nx.get_node_attributes(G, 'label')
#     labels = {node: f"{raw_labels.get(node, '')}\n{node}" for node in G.nodes}
#
#     # Цвета узлов
#     try:
#         node_colors = [G.nodes[node]['color'] for node in G.nodes]
#     except KeyError:
#         node_colors = ['lightgray'] * len(G.nodes)
#
#     # Создание и отрисовка графа
#     plt.figure(figsize=(6, 6))
#     nx.draw_networkx_nodes(G, pos, node_color=node_colors, edgecolors='black')
#     nx.draw_networkx_edges(G, pos, edge_color='gray')
#     nx.draw_networkx_labels(G, pos, labels, font_size=9)
#
#     # Агент
#     agent_pos = agent.get_position()
#     nx.draw_networkx_nodes(G, pos, nodelist=[agent_pos], node_color='red', node_size=500)
#
#     plt.title(f"Шаг {step_number + 1}, Агент в {agent_pos}")
#     plt.axis('off')
#     plt.tight_layout()
#     plt.show()
#
# # === Симуляция ===
# for i in range(steps):
#     draw_step(G, pos, agent, i)
#     agent.move()
