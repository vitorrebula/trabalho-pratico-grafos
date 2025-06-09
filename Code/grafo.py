import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict

class Vertice:
    def __init__(self, nome, x=None, y=None):
        self.nome = nome
        self.x = x
        self.y = y
        self.arestas = []

    def adicionar_aresta(self, aresta):
        self.arestas.append(aresta)

    def __repr__(self):
        return f"Vertice({self.nome}, x={self.x}, y={self.y})"


class Aresta:
    def __init__(self, origem, destino, capacidade, distancia, direcao):
        self.origem = origem  
        self.destino = destino  
        self.capacidade = capacidade
        self.distancia = distancia
        self.direcao = direcao 

    def __repr__(self):
        return (f"Aresta({self.origem.nome} -> {self.destino.nome}, "
                f"capacidade={self.capacidade}, distancia={self.distancia}, direcao={self.direcao})")


class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_vertice(self, nome, x=None, y=None):
        if nome not in self.vertices:
            self.vertices[nome] = Vertice(nome, x, y)
        else:
            vertice = self.vertices[nome]
            if vertice.x is None and x is not None:
                vertice.x = x
            if vertice.y is None and y is not None:
                vertice.y = y
        return self.vertices[nome]

    def adicionar_aresta(self, nome_origem, x_origem, y_origem,
                         nome_destino, x_destino, y_destino,
                         capacidade, distancia, direcao):
        origem = self.adicionar_vertice(nome_origem, x_origem, y_origem)
        destino = self.adicionar_vertice(nome_destino, x_destino, y_destino)

        aresta = Aresta(origem, destino, capacidade, distancia, direcao)
        origem.adicionar_aresta(aresta)

        if direcao == "bidirectional":
            aresta_reversa = Aresta(destino, origem, capacidade, distancia, direcao)
            destino.adicionar_aresta(aresta_reversa)

    def exibir_grafo(self, escala=5):
        G = nx.DiGraph()

        for vertice in self.vertices.values():
            G.add_node(vertice.nome)

        for vertice in self.vertices.values():
            for aresta in vertice.arestas:
                G.add_edge(
                    aresta.origem.nome,
                    aresta.destino.nome,
                    label=f"{aresta.capacidade}"
                )

        pos = {
            nome: (v.x * escala, v.y * escala)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        edge_labels = nx.get_edge_attributes(G, 'label')

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=6)
        plt.title("Rede de Distribuição de Água")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
    def to_networkx(self): #só pra converter pra um grafo da lib que desenha
      G = nx.DiGraph()
      for vertice in self.vertices.values():
          G.add_node(vertice.nome)
      for vertice in self.vertices.values():
          for aresta in vertice.arestas:
              G.add_edge(
                  aresta.origem.nome,
                  aresta.destino.nome,
                  capacity=aresta.capacidade
              )
      return G
    
    @staticmethod
    def fluxo_maximo(grafo, s, t):
        residual = defaultdict(dict)
        flow = defaultdict(dict)

        for u in grafo.vertices.values():
            for v in grafo.vertices.values():
                residual[u.nome][v.nome] = 0
                flow[u.nome][v.nome] = 0

        for vertice in grafo.vertices.values():
            for aresta in vertice.arestas:
                u = aresta.origem.nome
                v = aresta.destino.nome
                capacidade = aresta.capacidade
                residual[u][v] = capacidade
                residual[v][u] = 0

                if aresta.direcao == "bidirectional":
                    residual[v][u] = capacidade

        def bfs(source, sink, parent):
            visited = set()
            queue = deque([source])
            visited.add(source)

            while queue:
                u = queue.popleft()
                for v in residual[u]:
                    if v not in visited and residual[u][v] > 0:
                        visited.add(v)
                        parent[v] = u
                        if v == sink:
                            return True
                        queue.append(v)
            return False

        max_flow = 0
        parent = {}

        while bfs(s, t, parent):
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, residual[u][v])
                v = u

            v = t
            while v != s:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                flow[u][v] += path_flow
                flow[v][u] -= path_flow
                v = u

            max_flow += path_flow
            parent = {}

        flow_dict = {}
        for u in grafo.vertices:
            flow_dict[u] = {}
            for aresta in grafo.vertices[u].arestas:
                v = aresta.destino.nome
                flow_dict[u][v] = flow[u][v]

        return max_flow, flow_dict

    def calcular_fluxo_maximo(self, origem, destino):
        fluxo_valor, fluxo_dict = self.fluxo_maximo(self, origem, destino)
        return fluxo_valor, fluxo_dict

    def exibir_fluxo_maximo(self, origem, destino):
        fluxo_valor, fluxo_dict = self.calcular_fluxo_maximo(origem, destino)
        print(f"Fluxo máximo de {origem} para {destino}: {fluxo_valor} m³/dia")

        G = self.to_networkx() #apenas converte pra um grafo da biblioteca que desenha
        pos = {
            nome: (v.x, v.y)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        plt.figure(figsize=(12, 8))

        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
        nx.draw_networkx_labels(G, pos, font_size=10)

        edge_colors = []
        edge_labels_fluxo = {}       
        edge_labels_capacidade = {} 

        for u, v, data in G.edges(data=True):
            capacidade = int(data['capacity'])
            fluxo = int(fluxo_dict.get(u, {}).get(v, 0))

            if fluxo > 0:
                edge_colors.append('red')
                edge_labels_fluxo[(u, v)] = f"{fluxo}/{capacidade} m³"
            else:
                edge_colors.append('gray')
                edge_labels_capacidade[(u, v)] = f"0/{capacidade} m³"

        # Desenha as arestas
        nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=15, edge_color=edge_colors)

        # Primeiro desenha os rótulos cinza
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_capacidade, font_color='gray', font_size=8)

        # Depois desenha os rótulos vermelhos (sobrepõe visualmente, são os do fluxo máximo)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_fluxo, font_color='red', font_size=10)

        plt.title(f"Fluxo Máximo de {origem} para {destino}: {fluxo_valor} m³/dia")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return '\n'.join(f"{v.nome}: {v.arestas}" for v in self.vertices.values())
