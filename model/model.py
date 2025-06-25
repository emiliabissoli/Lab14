import copy

import networkx as nx
from networkx.algorithms.traversal import dfs_tree
from networkx.classes import nodes, DiGraph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapOrdini = {}
        self._nodes = []
        self._archi = []
        self._camminoMassimo = []
        self._bestPath = []
        self._bestScore = 0


    def getBestPath(self, partenza):
        self._bestPath = []
        self._bestScore = 0
        source = self._idMapOrdini[int(partenza)]

        parziale = [source] #devo partire da questo nodo
        for n in self._graph.successors(source): #prendo i suoi successori e ci faccio la ricorsione
            parziale.append(n)
            self.ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore


    def ricorsione(self, parziale):
        if self.calcolaPeso(parziale) > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.calcolaPeso(parziale)

        for s in self._graph.successors(parziale[-1]):
            if s not in parziale and self._graph[parziale[-1]][s]["weight"] < self._graph[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(s)
                self.ricorsione(parziale)
                parziale.pop()


    def calcolaPeso(self, parziale):
        peso = 0
        for i in range(0, len(parziale)-1):
            peso += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return peso


    def getAllStore(self):
        return DAO.getAllStore()

    def getAllNodes(self):
        return list(self._graph.nodes)

    def buildGraph(self, store, nMax):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(store)
        self._graph.add_nodes_from(self._nodes)
        self._idMapOrdini = {}
        for n in self._nodes:
            self._idMapOrdini[n.order_id] = n
        self.addAllArchi(store, nMax)

    def addAllArchi(self, store, nMax):
        self._archi = DAO.getAllArchi(store, nMax, self._idMapOrdini)
        for a in self._archi:
            ordine0 = a[0]
            ordine1 = a[1]
            peso = a[2]
            self._graph.add_edge(ordine0, ordine1, weight=peso)

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def camminoMassimo(self, nodo):
        source = self._idMapOrdini[int(nodo)]
        self._camminoMassimo = []
        cammino = []

        #calcola tutti i nodi raggiungibili dal nodo di partenza "nodo"
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for n in tree.nodes:
            cammino = [n]

            while cammino[0] != source:
                pred= nx.predecessor(tree, source, cammino[0]) #trova il predecessore di source tra source e cammino[0]
                cammino.insert(0, pred[0])

            if len(cammino) > len(self._camminoMassimo):
                self._camminoMassimo = copy.deepcopy(cammino)

        return self._camminoMassimo


