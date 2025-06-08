import networkx as nx
import matplotlib.pyplot as plt

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
        self.origem = origem  # objeto Vertice
        self.destino = destino  # objeto Vertice
        self.capacidade = capacidade
        self.distancia = distancia
        self.direcao = direcao  # "unidirectional" ou "bidirectional"

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
            # Se já existe, atualiza posição se ainda não foi definida
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

        # Aplica escala multiplicando as coordenadas para espaçar mais os vértices
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
        
    def to_networkx(self):
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

    def calcular_fluxo_maximo(self, origem, destino):
        G = self.to_networkx()
        fluxo_valor, fluxo_dict = nx.maximum_flow(G, origem, destino)
        return fluxo_valor, fluxo_dict

    def exibir_fluxo_maximo(self, origem, destino):
        fluxo_valor, fluxo_dict = self.calcular_fluxo_maximo(origem, destino)
        print(f"Fluxo máximo de {origem} para {destino}: {fluxo_valor} m³/dia")

        G = self.to_networkx()
        pos = {
            nome: (v.x, v.y)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        plt.figure(figsize=(12, 8))

        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
        nx.draw_networkx_labels(G, pos, font_size=10)

        edge_colors = []
        edge_labels_fluxo = {}       # fluxo/capacidade (vermelho)
        edge_labels_capacidade = {}  # 0/capacidade (cinza)

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

        # Depois desenha os rótulos vermelhos (sobrepõe visualmente)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_fluxo, font_color='red', font_size=10)

        plt.title(f"Fluxo Máximo de {origem} para {destino}: {fluxo_valor} m³/dia")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def __repr__(self):
        return '\n'.join(f"{v.nome}: {v.arestas}" for v in self.vertices.values())
