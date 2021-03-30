from collections import defaultdict
from basicComponent import Graph, SCC, BCC, randomGraph


class TarjanSCC:
    def __init__(self):
        pass

    def solve(self, G):
        assert type(G) == Graph
        self.V = G.V
        self.E = G.E

        self.time = 0
        self.status = defaultdict(lambda: 'unknown')
        self.dfs = defaultdict(lambda: -1)

        self.stack = []
        self.scc = []

        for v in self.V:
            if self.status[v] == 'unknown':
                self.__DFS(v)
        return SCC(self.scc)

    def __DFS(self, v):
        self.status[v] = 'progress'
        self.dfs[v] = self.time
        low = self.time
        self.time += 1
        self.stack.append(v)

        for adjV in self.E[v]:
            if self.status[adjV] == 'unknown':  # Tree Edge
                lowADJ = self.__DFS(adjV)
                low = min(lowADJ, low)
            elif self.status[adjV] == 'progress':  # Back Edge
                low = min(self.dfs[adjV], low)

        if low == self.dfs[v]:
            comp = []
            popV = None
            while popV != v:
                popV = self.stack.pop()
                comp.append(popV)
                self.status[popV] = 'known'
            self.scc.append(comp)
        return low


class KorsajuSCC:
    def __init__(self):
        pass

    def solve(self, G):
        assert type(G) == Graph
        self.V = G.V
        self.E = G.E
        self.stack = []  # foundStack
        self.scc = []
        self.ET = {v: [] for v in self.V}  # transpose
        for v in self.V:
            for adjV in self.E[v]:
                self.ET[adjV].append(v)

        self.status = defaultdict(bool)
        for v in self.V:
            if not self.status[v]:
                self.__DFS(v)

        self.status = defaultdict(bool)
        while self.stack:
            v = self.stack.pop()
            if not self.status[v]:
                self.comp = []
                self.__DFST(v)
                self.scc.append(self.comp)
        return SCC(self.scc)

    def __DFS(self, v):
        self.status[v] = True
        for adjV in self.E[v]:
            if not self.status[adjV]:
                self.__DFS(adjV)
        self.stack.append(v)

    def __DFST(self, v):  # transpose
        self.status[v] = True
        self.comp.append(v)
        for adjV in self.ET[v]:
            if not self.status[adjV]:
                self.__DFST(adjV)


class TarjanBCC:
    def __init__(self):
        pass

    def solve(self, G):
        assert type(G) == Graph
        self.V = G.V
        self.E = G.E

        self.dfsCnt = 0
        self.stack = []
        self.bcc = []
        self.status = defaultdict(lambda: 'unknown')
        self.dfs = defaultdict(lambda: -1)
        self.tree = defaultdict(lambda: -1)

        for v in self.V:
            if self.status[v] == 'unknown':
                self.__DFS(v, True)
        return BCC(self.bcc)

    def __DFS(self, v, isRoot=False):
        self.status[v] = 'progress'
        self.dfs[v] = self.dfsCnt
        low = self.dfsCnt
        self.dfsCnt += 1

        for adjV in self.E[v]:
            if self.tree[v] == adjV:
                continue
            if self.status[adjV] == 'known':
                low = min(self.dfs[adjV], low)
            elif self.status[adjV] == 'progress':
                low = min(self.dfs[adjV], low)
                self.stack.append((v, adjV))
            else:  # unknown
                self.stack.append((v, adjV))
                self.tree[adjV] = v
                childLow = self.__DFS(adjV)
                low = min(low, childLow)

                if childLow >= self.dfs[v]:
                    comp = []
                    while self.stack:
                        x, y = self.stack.pop()
                        comp.append((x, y))
                        comp.append((y, x))
                        if (x, y) == (v, adjV):
                            break
                    self.bcc.append(comp)
        self.status[v] = 'known'
        return low


if __name__ == "__main__":
    def checkSCC(given=False):
        tarjan = TarjanSCC()
        korsaju = KorsajuSCC()
        if not given:
            while not input("SCC | Enter -> continue | Otherwise -> quit"):
                G = randomGraph(prob=0.2, isDirected=True, useAlphabet=True)
                print(G)
                G.show()
                tarjanSCC = tarjan.solve(G)
                korsajuSCC = korsaju.solve(G)
                if tarjanSCC != korsajuSCC:
                    print(False, tarjanSCC, korsajuSCC)
                else:
                    print(True, korsajuSCC)
                G.setSCC(tarjanSCC)
                G.show()
        else:
            E = {'A': ['B'],
                 'B': ['A', 'C', 'D'],
                 'C': ['A', 'H'],
                 'D': ['G', 'E'],
                 'E': ['D', 'F'],
                 'F': ['F'],
                 'G': ['I', 'H'],
                 'H': ['G'],
                 'I': []}
            V = list(E.keys())
            G = Graph(V, E, isDirected=True)
            print(G)
            G.show()
            tarjanSCC = tarjan.solve(G)
            korsajuSCC = korsaju.solve(G)
            if tarjanSCC != korsajuSCC:
                print(False, tarjanSCC, korsajuSCC)
            else:
                print(True, korsajuSCC)
            G.setSCC(tarjanSCC)
            G.show()

    def checkBCC(given=False):
        tbcc = TarjanBCC()
        if not given:
            while not input("BCC | Enter -> continue | Otherwise -> quit"):
                G = randomGraph(prob=0.25, isDirected=False, useAlphabet=False)
                print(G)
                bcc = tbcc.solve(G)
                print(bcc)
                G.setBCC(bcc)
                G.show()
        else:
            E = {1: [2, 3, 6],
                 2: [1, 3, 4, 5],
                 3: [1, 2],
                 4: [2, 5],
                 5: [2, 4],
                 6: [1]}
            V = list(E.keys())
            G = Graph(V, E, isDirected=False)
            print(G)
            bcc = tbcc.solve(G)
            print(bcc)
            G.setBCC(bcc)
            G.show()

    checkSCC()
    checkBCC()