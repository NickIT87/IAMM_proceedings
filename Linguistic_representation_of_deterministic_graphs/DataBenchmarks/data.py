import matplotlib.pyplot as plt     # type: ignore
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


def print_data(G):
    # Set the node labels
    labels = nx.get_node_attributes(G, 'label')
    # Get the node colors
    try:
        node_colors = [G.nodes[node]['color'] for node in G.nodes]
    except KeyError:
        node_colors = [random_color() for _ in range(len(G.nodes)-1)]
        node_colors.insert(0, "red")
    T = nx.minimum_spanning_tree(G)
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
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
    # Adjust the spacing between subplots
    plt.tight_layout()
    # Show the graph
    plt.show()


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
# for step 4 AP alg
testC1_4 = ("153521", "152431")
testL1_4 = ("1342531", "12324123", "123241")
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

testC5 = ()
testL5 = ('123',)

cardC = ('abcdefghijklmpa', 'abcpa', 'abcpmla')
cardL = ('abcdeno', 'apg')

# ABCDEFGHIJKLMPA ABCPA ABCPMLA
# ABCDENO APG
#
# 'ABCPA', 'ABCDEFGHIJKLA', 'ALMPA'
# 'ABCDENO', 'APG'

tgc = ('012310', '012410', '012710', '012810', '012910', '012a10', '013410', '0125310', '0126310', '013710', '013810', '013910', '013a10', '0125410', '0126410', '014710', '014810', '014910', '014a10', '01256210', '0125710', '0125810', '0125910', '0125a10', '0126710', '0126810', '0126910', '0126a10', '017810', '017910', '017a10', '018910', '018a10', '019a10')
tgc1 = ('012310', '012410', '012710', '012810', '012910', '012a10', '012b10', '012c10', '012d10', '012e10', '012f10', '012g10', '012h10', '012i10', '012j10', '012k10', '012l10', '012m10', '012n10', '012o10', '012p10', '012q10', '012r10', '012s10', '012t10', '012u10', '012v10', '012w10', '012x10', '012y10', '012z10', '012~10', '01!210', '012@10', '01#210', '01$210', '01%210', '012^10', '01&210', '01*210', '01(210', '01)210', '012_10', '01+210', '012[10', '012]10', '013410', '0125310', '0126310', '013710', '013810', '013910', '013a10', '013b10', '013c10', '013d10', '013e10', '013f10', '013g10', '013h10', '013i10', '013j10', '013k10', '013l10', '013m10', '013n10', '013o10', '013p10', '013q10', '013r10', '013s10', '013t10', '013u10', '013v10', '013w10', '013x10', '013y10', '013z10', '013~10', '01!310', '013@10', '01#310', '01$310', '01%310', '013^10', '01&310', '01*310', '01(310', '01)310', '013_10', '01+310', '013[10', '013]10', '0125410', '0126410', '014710', '014810', '014910', '014a10', '014b10', '014c10', '014d10', '014e10', '014f10', '014g10', '014h10', '014i10', '014j10', '014k10', '014l10', '014m10', '014n10', '014o10', '014p10', '014q10', '014r10', '014s10', '014t10', '014u10', '014v10', '014w10', '014x10', '014y10', '014z10', '014~10', '01!410', '014@10', '01#410', '01$410', '01%410', '014^10', '01&410', '01*410', '01(410', '01)410', '014_10', '01+410', '014[10', '014]10', '01256210', '0125710', '0125810', '0125910', '0125a10', '0125b10', '0125c10', '0125d10', '0125e10', '0125f10', '0125g10', '0125h10', '0125i10', '0125j10', '0125k10', '0125l10', '0125m10', '0125n10', '0125o10', '0125p10', '0125q10', '0125r10', '0125s10', '0125t10', '0125u10', '0125v10', '0125w10', '0125x10', '0125y10', '0125z10', '0125~10', '01!5210', '0125@10', '01#5210', '01$5210', '01%5210', '0125^10', '01&5210', '01*5210', '01(5210', '01)5210', '0125_10', '01+5210', '0125[10', '0125]10', '0126710', '0126810', '0126910', '0126a10', '0126b10', '0126c10', '0126d10', '0126e10', '0126f10', '0126g10', '0126h10', '0126i10', '0126j10', '0126k10', '0126l10', '0126m10', '0126n10', '0126o10', '0126p10', '0126q10', '0126r10', '0126s10', '0126t10', '0126u10', '0126v10', '0126w10', '0126x10', '0126y10', '0126z10', '0126~10', '01!6210', '0126@10', '01#6210', '01$6210', '01%6210', '0126^10', '01&6210', '01*6210', '01(6210', '01)6210', '0126_10', '01+6210', '0126[10', '0126]10', '017810', '017910', '017a10', '017b10', '017c10', '017d10', '017e10', '017f10', '017g10', '017h10', '017i10', '017j10', '017k10', '017l10', '017m10', '017n10', '017o10', '017p10', '017q10', '017r10', '017s10', '017t10', '017u10', '017v10', '017w10', '017x10', '017y10', '017z10', '017~10', '01!710', '017@10', '01#710', '01$710', '01%710', '017^10', '01&710', '01*710', '01(710', '01)710', '017_10', '01+710', '017[10', '017]10', '018910', '018a10', '018b10', '018c10', '018d10', '018e10', '018f10', '018g10', '018h10', '018i10', '018j10', '018k10', '018l10', '018m10', '018n10', '018o10', '018p10', '018q10', '018r10', '018s10', '018t10', '018u10', '018v10', '018w10', '018x10', '018y10', '018z10', '018~10', '01!810', '018@10', '01#810', '01$810', '01%810', '018^10', '01&810', '01*810', '01(810', '01)810', '018_10', '01+810', '018[10', '018]10', '019a10', '019b10', '019c10', '019d10', '019e10', '019f10', '019g10', '019h10', '019i10', '019j10', '019k10', '019l10', '019m10', '019n10', '019o10', '019p10', '019q10', '019r10', '019s10', '019t10', '019u10', '019v10', '019w10', '019x10', '019y10', '019z10', '019~10', '01!910', '019@10', '01#910', '01$910', '01%910', '019^10', '01&910', '01*910', '01(910', '01)910', '019_10', '01+910', '019[10', '019]10', '01ab10', '01ac10', '01ad10', '01ae10', '01af10', '01ag10', '01ah10', '01ai10', '01aj10', '01ak10', '01al10', '01am10', '01an10', '01ao10', '01ap10', '01aq10', '01ar10', '01as10', '01at10', '01au10', '01av10', '01aw10', '01ax10', '01ay10', '01az10', '01a~10', '01!a10', '01@a10', '01#a10', '01$a10', '01%a10', '01^a10', '01&a10', '01*a10', '01(a10', '01)a10', '01_a10', '01+a10', '01[a10', '01]a10', '01bc10', '01bd10', '01be10', '01bf10', '01bg10', '01bh10', '01bi10', '01bj10', '01bk10', '01bl10', '01bm10', '01bn10', '01bo10', '01bp10', '01bq10', '01br10', '01bs10', '01bt10', '01bu10', '01bv10', '01bw10', '01bx10', '01by10', '01bz10', '01b~10', '01!b10', '01@b10', '01#b10', '01$b10', '01%b10', '01^b10', '01&b10', '01*b10', '01(b10', '01)b10', '01_b10', '01+b10', '01[b10', '01]b10', '01cd10', '01ce10', '01cf10', '01cg10', '01ch10', '01ci10', '01cj10', '01ck10', '01cl10', '01cm10', '01cn10', '01co10', '01cp10', '01cq10', '01cr10', '01cs10', '01ct10', '01cu10', '01cv10', '01cw10', '01cx10', '01cy10', '01cz10', '01c~10', '01!c10', '01@c10', '01#c10', '01$c10', '01%c10', '01^c10', '01&c10', '01*c10', '01(c10', '01)c10', '01_c10', '01+c10', '01[c10', '01]c10', '01de10', '01df10', '01dg10', '01dh10', '01di10', '01dj10', '01dk10', '01dl10', '01dm10', '01dn10', '01do10', '01dp10', '01dq10', '01dr10', '01ds10', '01dt10', '01du10', '01dv10', '01dw10', '01dx10', '01dy10', '01dz10', '01d~10', '01!d10', '01@d10', '01#d10', '01$d10', '01%d10', '01^d10', '01&d10', '01*d10', '01(d10', '01)d10', '01_d10', '01+d10', '01[d10', '01]d10', '01ef10', '01eg10', '01eh10', '01ei10', '01ej10', '01ek10', '01el10', '01em10', '01en10', '01eo10', '01ep10', '01eq10', '01er10', '01es10', '01et10', '01eu10', '01ev10', '01ew10', '01ex10', '01ey10', '01ez10', '01e~10', '01!e10', '01@e10', '01#e10', '01$e10', '01%e10', '01^e10', '01&e10', '01*e10', '01(e10', '01)e10', '01_e10', '01+e10', '01[e10', '01]e10', '01fg10', '01fh10', '01fi10', '01fj10', '01fk10', '01fl10', '01fm10', '01fn10', '01fo10', '01fp10', '01fq10', '01fr10', '01fs10', '01ft10', '01fu10', '01fv10', '01fw10', '01fx10', '01fy10', '01fz10', '01f~10', '01!f10', '01@f10', '01#f10', '01$f10', '01%f10', '01^f10', '01&f10', '01*f10', '01(f10', '01)f10', '01_f10', '01+f10', '01[f10', '01]f10', '01gh10', '01gi10', '01gj10', '01gk10', '01gl10', '01gm10', '01gn10', '01go10', '01gp10', '01gq10', '01gr10', '01gs10', '01gt10', '01gu10', '01gv10', '01gw10', '01gx10', '01gy10', '01gz10', '01g~10', '01!g10', '01@g10', '01#g10', '01$g10', '01%g10', '01^g10', '01&g10', '01*g10', '01(g10', '01)g10', '01_g10', '01+g10', '01[g10', '01]g10', '01hi10', '01hj10', '01hk10', '01hl10', '01hm10', '01hn10', '01ho10', '01hp10', '01hq10', '01hr10', '01hs10', '01ht10', '01hu10', '01hv10', '01hw10', '01hx10', '01hy10', '01hz10', '01h~10', '01!h10', '01@h10', '01#h10', '01$h10', '01%h10', '01^h10', '01&h10', '01*h10', '01(h10', '01)h10', '01_h10', '01+h10', '01[h10', '01]h10', '01ij10', '01ik10', '01il10', '01im10', '01in10', '01io10', '01ip10', '01iq10', '01ir10', '01is10', '01it10', '01iu10', '01iv10', '01iw10', '01ix10', '01iy10', '01iz10', '01i~10', '01!i10', '01@i10', '01#i10', '01$i10', '01%i10', '01^i10', '01&i10', '01*i10', '01(i10', '01)i10', '01_i10', '01+i10', '01[i10', '01]i10', '01jk10', '01jl10', '01jm10', '01jn10', '01jo10', '01jp10', '01jq10', '01jr10', '01js10', '01jt10', '01ju10', '01jv10', '01jw10', '01jx10', '01jy10', '01jz10', '01j~10', '01!j10', '01@j10', '01#j10', '01$j10', '01%j10', '01^j10', '01&j10', '01*j10', '01(j10', '01)j10', '01_j10', '01+j10', '01[j10', '01]j10', '01kl10', '01km10', '01kn10', '01ko10', '01kp10', '01kq10', '01kr10', '01ks10', '01kt10', '01ku10', '01kv10', '01kw10', '01kx10', '01ky10', '01kz10', '01k~10', '01!k10', '01@k10', '01#k10', '01$k10', '01%k10', '01^k10', '01&k10', '01*k10', '01(k10', '01)k10', '01_k10', '01+k10', '01[k10', '01]k10', '01lm10', '01ln10', '01lo10', '01lp10', '01lq10', '01lr10', '01ls10', '01lt10', '01lu10', '01lv10', '01lw10', '01lx10', '01ly10', '01lz10', '01l~10', '01!l10', '01@l10', '01#l10', '01$l10', '01%l10', '01^l10', '01&l10', '01*l10', '01(l10', '01)l10', '01_l10', '01+l10', '01[l10', '01]l10', '01mn10', '01mo10', '01mp10', '01mq10', '01mr10', '01ms10', '01mt10', '01mu10', '01mv10', '01mw10', '01mx10', '01my10', '01mz10', '01m~10', '01!m10', '01@m10', '01#m10', '01$m10', '01%m10', '01^m10', '01&m10', '01*m10', '01(m10', '01)m10', '01_m10', '01+m10', '01[m10', '01]m10', '01no10', '01np10', '01nq10', '01nr10', '01ns10', '01nt10', '01nu10', '01nv10', '01nw10', '01nx10', '01ny10', '01nz10', '01n~10', '01!n10', '01@n10', '01#n10', '01$n10', '01%n10', '01^n10', '01&n10', '01*n10', '01(n10', '01)n10', '01_n10', '01+n10', '01[n10', '01]n10', '01op10', '01oq10', '01or10', '01os10', '01ot10', '01ou10', '01ov10', '01ow10', '01ox10', '01oy10', '01oz10', '01o~10', '01!o10', '01@o10', '01#o10', '01$o10', '01%o10', '01^o10', '01&o10', '01*o10', '01(o10', '01)o10', '01_o10', '01+o10', '01[o10', '01]o10', '01pq10', '01pr10', '01ps10', '01pt10', '01pu10', '01pv10', '01pw10', '01px10', '01py10', '01pz10', '01p~10', '01!p10', '01@p10', '01#p10', '01$p10', '01%p10', '01^p10', '01&p10', '01*p10', '01(p10', '01)p10', '01_p10', '01+p10', '01[p10', '01]p10', '01qr10', '01qs10', '01qt10', '01qu10', '01qv10', '01qw10', '01qx10', '01qy10', '01qz10', '01q~10', '01!q10', '01@q10', '01#q10', '01$q10', '01%q10', '01^q10', '01&q10', '01*q10', '01(q10', '01)q10', '01_q10', '01+q10', '01[q10', '01]q10', '01rs10', '01rt10', '01ru10', '01rv10', '01rw10', '01rx10', '01ry10', '01rz10', '01r~10', '01!r10', '01@r10', '01#r10', '01$r10', '01%r10', '01^r10', '01&r10', '01*r10', '01(r10', '01)r10', '01_r10', '01+r10', '01[r10', '01]r10', '01st10', '01su10', '01sv10', '01sw10', '01sx10', '01sy10', '01sz10', '01s~10', '01!s10', '01@s10', '01#s10', '01$s10', '01%s10', '01^s10', '01&s10', '01*s10', '01(s10', '01)s10', '01_s10', '01+s10', '01[s10', '01]s10', '01tu10', '01tv10', '01tw10', '01tx10', '01ty10', '01tz10', '01t~10', '01!t10', '01@t10', '01#t10', '01$t10', '01%t10', '01^t10', '01&t10', '01*t10', '01(t10', '01)t10', '01_t10', '01+t10', '01[t10', '01]t10', '01uv10', '01uw10', '01ux10', '01uy10', '01uz10', '01u~10', '01!u10', '01@u10', '01#u10', '01$u10', '01%u10', '01^u10', '01&u10', '01*u10', '01(u10', '01)u10', '01_u10', '01+u10', '01[u10', '01]u10', '01vw10', '01vx10', '01vy10', '01vz10', '01v~10', '01!v10', '01@v10', '01#v10', '01$v10', '01%v10', '01^v10', '01&v10', '01*v10', '01(v10', '01)v10', '01_v10', '01+v10', '01[v10', '01]v10', '01wx10', '01wy10', '01wz10', '01w~10', '01!w10', '01@w10', '01#w10', '01$w10', '01%w10', '01^w10', '01&w10', '01*w10', '01(w10', '01)w10', '01_w10', '01+w10', '01[w10', '01]w10', '01xy10', '01xz10', '01x~10', '01!x10', '01@x10', '01#x10', '01$x10', '01%x10', '01^x10', '01&x10', '01*x10', '01(x10', '01)x10', '01_x10', '01+x10', '01[x10', '01]x10', '01yz10', '01y~10', '01!y10', '01@y10', '01#y10', '01$y10', '01%y10', '01^y10', '01&y10', '01*y10', '01(y10', '01)y10', '01_y10', '01+y10', '01[y10', '01]y10', '01z~10', '01!z10', '01@z10', '01#z10', '01$z10', '01%z10', '01^z10', '01&z10', '01*z10', '01(z10', '01)z10', '01_z10', '01+z10', '01[z10', '01]z10', '01!~10', '01@~10', '01#~10', '01$~10', '01%~10', '01^~10', '01&~10', '01*~10', '01(~10', '01)~10', '01_~10', '01+~10', '01[~10', '01]~10', '01!@10', '01!#10', '01!$10', '01!%10', '01!^10', '01!&10', '01!*10', '01!(10', '01!)10', '01!_10', '01!+10', '01![10', '01!]10', '01#@10', '01$@10', '01%@10', '01@^10', '01&@10', '01*@10', '01(@10', '01)@10', '01@_10', '01+@10', '01@[10', '01@]10', '01#$10', '01#%10', '01#^10', '01#&10', '01#*10', '01#(10', '01#)10', '01#_10', '01#+10', '01#[10', '01#]10', '01$%10', '01$^10', '01$&10', '01$*10', '01$(10', '01$)10', '01$_10', '01$+10', '01$[10', '01$]10', '01%^10', '01%&10', '01%*10', '01%(10', '01%)10', '01%_10', '01%+10', '01%[10', '01%]10', '01&^10', '01*^10', '01(^10', '01)^10', '01^_10', '01+^10', '01[^10', '01]^10', '01&*10', '01&(10', '01&)10', '01&_10', '01&+10', '01&[10', '01&]10', '01(*10', '01)*10', '01*_10', '01*+10', '01*[10', '01*]10', '01()10', '01(_10', '01(+10', '01([10', '01(]10', '01)_10', '01)+10', '01)[10', '01)]10', '01+_10', '01[_10', '01]_10', '01+[10', '01+]10', '01[]10')
tgl = ()
# =============================================================================
