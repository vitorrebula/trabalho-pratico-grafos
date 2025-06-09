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
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.DiGraph()

        for vertice in self.vertices.values():
            G.add_node(vertice.nome)

        capacidades = {}
        for vertice in self.vertices.values():
            for aresta in vertice.arestas:
                u = aresta.origem.nome
                v = aresta.destino.nome
                capacidades[(u, v)] = aresta.capacidade
                G.add_edge(u, v)

        edge_labels = {}
        adicionados = set()

        for (u, v), cap_uv in capacidades.items():
            if (v, u) in capacidades and (v, u) not in adicionados:
                cap_vu = capacidades[(v, u)]
                label = f"→ {cap_uv} | {cap_vu} ←"
                edge_labels[(u, v)] = label
                edge_labels[(v, u)] = ""  # Oculta duplicado
                adicionados.add((u, v))
                adicionados.add((v, u))
            elif (u, v) not in adicionados:
                label = f"{cap_uv}"  # Sem setas se for só em um sentido
                edge_labels[(u, v)] = label
                adicionados.add((u, v))

        pos = {
            nome: (v.x * escala, v.y * escala)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=7)

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
        
    def exibir_fluxo_e_gargalo(self, origem, destino):
        fluxo_valor, fluxo_dict = self.calcular_fluxo_maximo(origem, destino)
        print(f"\n💧 Fluxo máximo de {origem} para {destino}: {fluxo_valor} m³/dia")

        G = self.to_networkx()
        pos = {
            nome: (v.x, v.y)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        # 1. Identifica gargalos
        gargalos = []
        for u, v in G.edges():
            capacidade = int(G[u][v]['capacity'])
            fluxo = int(fluxo_dict.get(u, {}).get(v, 0))
            if fluxo == capacidade and capacidade > 0:
                gargalos.append((u, v, capacidade))

        gargalo_critico = min(gargalos, key=lambda x: x[2]) if gargalos else None

        # 2. Coleta rótulos e classifica arestas
        edge_labels_vermelho = {}
        edge_labels_preto = {}
        fluxo_positivo = []
        sem_fluxo = []

        for u, v in G.edges():
            capacidade = int(G[u][v]['capacity'])
            fluxo = int(fluxo_dict.get(u, {}).get(v, 0))
            label = f"{fluxo}/{capacidade}"

            if fluxo > 0:
                fluxo_positivo.append((u, v))
                edge_labels_vermelho[(u, v)] = label
            else:
                sem_fluxo.append((u, v))
                edge_labels_preto[(u, v)] = label

        # 3. Visualização
        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
        nx.draw_networkx_labels(G, pos, font_size=10)

        # Arestas sem fluxo (cinza)
        nx.draw_networkx_edges(G, pos, edgelist=sem_fluxo, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=15)

        # Arestas com fluxo (vermelho)
        nx.draw_networkx_edges(G, pos, edgelist=fluxo_positivo, edge_color='red', arrows=True, arrowstyle='-|>', arrowsize=15)

        # Gargalo (azul por cima)
        if gargalo_critico:
            u, v, cap = gargalo_critico
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', width=3.5, arrows=True, arrowstyle='-|>', arrowsize=20)
            plt.title("Recomendação: aumentar a capacidade desse cano (linha azul no grafo).")
        else:
            plt.title("Nenhum gargalo detectado — nenhuma aresta totalmente saturada.")

        # Labels: primeiro preto (sem fluxo), depois vermelho, depois o gargalo por cima
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_preto, font_size=9, font_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_vermelho, font_size=9, font_color='red')

        if gargalo_critico:
            u, v, _ = gargalo_critico
            label = edge_labels_vermelho.get((u, v), "")
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label}, font_size=10, font_color='red', font_weight='bold')

        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def desenhar_rede_residual(self, grafo_original, fluxo_dict):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        arestas_originais = set()

        # Marca todas as arestas do grafo original
        for vertice in grafo_original.vertices.values():
            for aresta in vertice.arestas:
                arestas_originais.add((aresta.origem.nome, aresta.destino.nome))

        for vertice in grafo_original.vertices.values():
            for aresta in vertice.arestas:
                u = aresta.origem.nome
                v = aresta.destino.nome
                capacidade = aresta.capacidade
                fluxo = fluxo_dict.get(u, {}).get(v, 0)

                capacidade_residual = capacidade - fluxo

                # Aresta direta residual
                if capacidade_residual > 0:
                    G.add_edge(u, v, capacidade=capacidade, residual=capacidade_residual, cor='green')

                # Aresta reversa (somente se não existir no original)
                if fluxo > 0:
                    if (v, u) not in arestas_originais:
                        G.add_edge(v, u, capacidade=fluxo, residual=fluxo, cor='orange')

        # Posicionamento dos nós
        pos = {
            nome: (v.x, v.y)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        edge_colors = [data['cor'] for _, _, data in G.edges(data=True)]
        edge_labels = {
            (u, v): f"{data['residual']}/{data['capacidade']}"
            for u, v, data in G.edges(data=True)
        }

        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightyellow')
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='-|>', arrowsize=15, width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

        plt.title("Rede Residual (Capacidade restante / Capacidade total)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    
    def __repr__(self):
        return '\n'.join(f"{v.nome}: {v.arestas}" for v in self.vertices.values())
