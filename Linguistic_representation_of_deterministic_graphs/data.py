import networkx as nx               # type: ignore
import random


colors = [
    'lightcoral',
    'lightblue',
    'lightgreen',
    'yellow',
    'orange',
    'magenta',
    'pink',
    'cyan'
]

def random_color():
    red = random.randint(100, 255)
    green = random.randint(100, 255)
    blue = random.randint(100, 255)
    hex_color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
    return hex_color


G = nx.Graph()

# TEST DATA 1
# G.add_node(0, label='0', color="lightblue")
# G.add_node(1, label='1', color="lightblue")
# G.add_node(2, label='2', color="lightblue")
# G.add_node(3, label='3', color="lightblue")
# G.add_node(4, label='4', color="lightblue")
# G.add_node(5, label='5', color="lightblue")
# G.add_node(6, label='6', color="lightblue")
#
# G.add_edge(0, 1)
# G.add_edge(1, 2)
# G.add_edge(1, 3)
# G.add_edge(1, 4)
# G.add_edge(1, 5)
# G.add_edge(2, 3)
# G.add_edge(2, 4)
# G.add_edge(2, 5)
# G.add_edge(2, 6)
# G.add_edge(3, 4)
# G.add_edge(3, 5)
# G.add_edge(3, 6)
# G.add_edge(4, 5)
# G.add_edge(4, 6)
# G.add_edge(5, 6)

# TEST DATA 2
# G.add_node(0, label='1', color='lightcoral')
# G.add_node(1, label='2', color='lightblue')
# G.add_node(2, label='3', color='lightgreen')
# G.add_node(3, label='4', color='yellow')
# G.add_node(4, label='1', color='orange')
# G.add_node(5, label='2', color='magenta')
# G.add_node(6, label='5', color='pink')
# G.add_node(7, label='3', color='cyan')
#
# G.add_edge(0, 1)
# G.add_edge(1, 2)
# G.add_edge(1, 3)
# G.add_edge(2, 3)
# G.add_edge(2, 4)
# G.add_edge(3, 4)
# G.add_edge(4, 5)
# G.add_edge(4, 6)
# G.add_edge(6, 7)

# TEST REDUCTION DATA
# G.add_node(0, label='1', color='red')
# G.add_node(1, label='5', color='lightgreen')
# G.add_node(2, label='3', color='yellow')
# G.add_node(3, label='6', color='magenta')
# G.add_node(4, label='2', color='cyan')
# G.add_node(5, label='5', color='orange')
# G.add_node(6, label='5', color='orange')
#
# G.add_edge(0, 1)
# G.add_edge(1, 2)
# G.add_edge(2, 5)
# G.add_edge(2, 6)
# G.add_edge(5, 3)
# G.add_edge(3, 4)
# G.add_edge(4, 0)

# TEST PAIR DATA ON FLOWER GRAPH
G.add_node(0, label="0")
G.add_node(1, label="1")
G.add_node(2, label="2")
G.add_node(3, label="3")
G.add_node(4, label="4")
G.add_node(5, label="5")
G.add_node(6, label="6")

G.add_edge(0, 1)
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 4)
G.add_edge(2, 3)
G.add_edge(2, 4)
G.add_edge(2, 5)
G.add_edge(2, 6)
G.add_edge(3, 4)
G.add_edge(3, 5)
G.add_edge(3, 6)
G.add_edge(4, 5)
G.add_edge(4, 6)
G.add_edge(5, 6)


# TEST DATA
# =============================================================================
testC1 = ("153521", "152431")
testL1 = ("1342531", "123241", "13412", "1523")
# 1 2 3 4 5
# a b c d e
testC1a = ("aeceba", "aebdca")
testL1a = ("acdbeca", "abcbdab", "acdab", "aebc")

testC2 = ("124231",)
testL2 = ("13537",
          #"137",
          #"124",
          #"135"
)

testC3 = ('1251', '12431')
testL3 = ('1531', '123', '12412')

testC4 = ('1231',)
testL4 = ('56',)

tgc = ('012310', '012410', '012710', '012810', '012910', '012a10', '013410', '0125310', '0126310', '013710', '013810', '013910', '013a10', '0125410', '0126410', '014710', '014810', '014910', '014a10', '01256210', '0125710', '0125810', '0125910', '0125a10', '0126710', '0126810', '0126910', '0126a10', '017810', '017910', '017a10', '018910', '018a10', '019a10')
tgl = ()
# =============================================================================