import random
from collections import defaultdict

from utils import numToString

import networkx as nx
import pylab
from colorsys import hls_to_rgb


class SCC:  # TODO get dict not list?
    def __init__(self, comp):
        assert type(comp) == list
        assert all(type(x) == list for x in comp)
        V = [v for x in comp for v in x]
        assert all(i == j or V[i] != V[j]
                   for i in range(len(V)) for j in range(len(V)))
        self.V = sorted(V)
        self.comp = sorted([sorted(x) for x in comp])

    def __str__(self):
        return f'SCC ( V: {self.V} / COMP : {self.comp} )'

    def __len__(self):
        return len(self.comp)

    def __eq__(self, other):
        assert type(other) == SCC
        return self.comp == other.comp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        return self.comp[index]

    def __iter__(self):
        self.iterCnt = 0
        return self

    def __next__(self):
        if self.iterCnt >= self.__len__():
            raise StopIteration
        item = self.__getitem__(self.iterCnt)
        self.iterCnt += 1
        return item


class BCC:
    def __init__(self, comp):  # TODO defaultdict because of point with degree 0
        assert type(comp) == list
        assert all(type(x) == list for x in comp)
        assert all(type(e) == tuple and len(e) == 2 for x in comp for e in x)
        assert all((j, i) in x for x in comp for i, j in x)
        self.E = sorted([e for x in comp for e in x])
        assert all(self.E[i] != self.E[j] for i in range(len(self.E))
                   for j in range(len(self.E)) if i != j)
        self.comp = sorted(sorted(x) for x in comp)
        # TODO check validation according to the definition of BCC

    def __str__(self):
        return f'BCC ( COMP : {self.comp} )'

    def __len__(self):
        return len(self.comp)

    def __eq__(self, other):
        assert type(other) == BCC
        return self.comp == other.comp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        return self.comp[index]


class Graph:
    def __init__(self, V, E, isDirected, scc=None, bcc=None):
        assert type(V) == list
        assert type(E) == dict
        assert all(V[i] != V[j] for i in range(len(V))
                   for j in range(len(V)) if i != j)
        assert all(v in V and all(adjV in V for adjV in e)
                   for v, e in E.items())
        # TODO check validation of isDirected <-> E
        self.V = V
        self.E = E

        self.V.sort()
        for v in self.V:
            self.E[v].sort()

        self.isDirected = isDirected

        self.scc = scc
        self.bcc = bcc

    def __str__(self):
        return f'G ( V : {self.V} / E : {self.E} )'

    def __eq__(self, other):
        assert type(other) == Graph
        return self.V == other.V and self.E == other.E

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        # TODO How about using copy.deepcopy?
        return Graph(self.V[:], {v: self.E[v][:] for v in self.V}, self.isDirected)

    def setSCC(self, scc):
        assert type(scc) == SCC
        assert scc.V == self.V
        # TODO check validation
        self.scc = scc

    def setBCC(self, bcc):
        assert type(bcc) == BCC
        assert(len(bcc.E) == sum(len(e) for e in self.E.values()))
        # TODO check validation
        self.bcc = bcc

    def transpose(self):
        if not self.isDirected:
            return self.copy()
        else:
            ET = {v: [] for v in self.V}
            for v in self.V:
                for adjV in self.E[v]:
                    ET[adjV].append(v)
            return Graph(self.V[:], ET, self.isDirected)

    def show(self, size=500, width=2):
        strV = [str(v) for v in self.V]
        strE = [(str(v), str(adjV)) for v in self.V for adjV in self.E[v]]
        G = nx.DiGraph()
        G.add_nodes_from(strV)
        G.add_edges_from(strE)

        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos, nodelist=[], edgelist=[], node_color='gray', node_size=size)
        nx.draw_networkx_labels(G, pos)

        title = 'Graph'
        if self.scc is not None:
            title += 'with SCC'
            for i in range(len(self.scc)):
                V = self.scc[i]
                color = hls_to_rgb(i / len(self.scc), 0.6, 0.6)
                nodeColor = [color for _ in range(len(V))]
                nodeStr = [str(v) for v in V]
                nx.draw_networkx_nodes(G, pos, nodelist=nodeStr,
                                       node_color=nodeColor, node_size=size)
        else:
            nx.draw_networkx_nodes(G, pos, node_color='gray', node_size=size)
        if self.bcc is not None:
            title += 'with BCC'
            for i in range(len(self.bcc)):
                E = self.bcc[i]
                strE = [(str(i), str(j)) for i, j in E]
                color = hls_to_rgb(i / len(self.bcc), 0.4, 0.4)
                edgeColor = [color for _ in range(len(E))]
                nx.draw_networkx_edges(G, pos, edgelist=strE,
                                       edge_color=edgeColor, width=width)
        else:
            nx.draw_networkx_edges(G, pos, edge_color='black', width=width)
        pylab.title(title)
        pylab.show()


def randomGraph(size=10, prob=0.4, isDirected=True, useAlphabet=False):
    if not useAlphabet:
        V = list(range(size))
    else:  # useAlphabet
        V = [numToString(i) for i in range(size)]
    E = {v: [] for v in V}
    if isDirected:
        for i in range(size):
            for j in range(size):
                if i != j and random.random() < prob:
                    E[V[i]].append(V[j])
    else:  # undirected
        for i in range(size - 1):
            for j in range(i + 1, size):
                if random.random() < prob:
                    E[V[i]].append(V[j])
                    E[V[j]].append(V[i])
    return Graph(V, E, isDirected)


if __name__ == "__main__":
    G = randomGraph(size=7, prob=0.5, isDirected=True, useAlphabet=True)
    print(G.transpose().transpose() == G)
    while not input("Enter -> continue | Otherwise -> quit"):
        G = randomGraph(size=7, prob=0.5, isDirected=True, useAlphabet=True)
        print(G)
        G.show()
        G.transpose().show()
