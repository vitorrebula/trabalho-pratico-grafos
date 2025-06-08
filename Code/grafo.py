##############################################################################
# grafo.py (somente as partes que mudaram)                                   #
##############################################################################
import math
import matplotlib.pyplot as plt

class Vertice:
    def __init__(self, id, x=0.0, y=0.0):
        self.id = id
        self.x_real = x            # coordenada original (só para registro)
        self.y_real = y
        # coordenadas de desenho poderão ser atribuídas depois
        self.x_draw = None
        self.y_draw = None

class Aresta:                     #  ← Faltava esta classe
    def __init__(self, origem, destino, capacidade):
        self.origem     = origem
        self.destino    = destino
        self.capacidade = capacidade
        self.fluxo      = 0       # opcional, se precisar de fluxo


class Grafo:
    def __init__(self):
        self.vertices = {}         # id -> Vertice
        self.arestas  = []         # lista de Aresta

    def adicionar_vertice(self, id, x=0.0, y=0.0):
        self.vertices[id] = Vertice(id, x, y)

    def adicionar_aresta(self, origem, destino, capacidade):
        self.arestas.append(Aresta(origem, destino, capacidade))

    # --------------------------------------------------------------------- #
    # Novo desenho ABSTRATO: ignora as coordenadas originais.               #
    # Coloca os vértices igualmente espaçados num círculo.                  #
    # --------------------------------------------------------------------- #
    def desenhar(self):
        if not self.vertices:
            print("Grafo vazio.")
            return

        # layout em círculo
        n   = len(self.vertices)
        ids = list(self.vertices.keys())
        raio = 10                               # raio arbitrário

        for i, vid in enumerate(ids):
            ang               = 2 * math.pi * i / n
            self.vertices[vid].x_draw = raio * math.cos(ang)
            self.vertices[vid].y_draw = raio * math.sin(ang)

        # ----- plota -----
        fig, ax = plt.subplots(figsize=(7, 7))

        # arestas
        for ar in self.arestas:
            if ar.origem not in self.vertices or ar.destino not in self.vertices:
                print(f"Vértice ausente: {ar.origem} ou {ar.destino}")
                continue
            v1, v2 = self.vertices[ar.origem], self.vertices[ar.destino]
            ax.plot([v1.x_draw, v2.x_draw], [v1.y_draw, v2.y_draw], 'k-', lw=0.7)

        # vértices
        for v in self.vertices.values():
            ax.plot(v.x_draw, v.y_draw, 'ro', ms=4)
            ax.text(v.x_draw + 0.3, v.y_draw + 0.3, str(v.id), fontsize=8)

        ax.set_aspect('equal', 'box')
        ax.set_axis_off()
        plt.title("Grafo abstrato (coordenadas reais só para deduplicação)")
        plt.show()

    def desenhar_com_residual(self, residual, origem, destino):
        if not self.vertices:
            print("Grafo vazio.")
            return

        # 1) garanta coordenadas de desenho (x_draw / y_draw)
        if any(v.x_draw is None for v in self.vertices.values()):
            n = len(self.vertices)
            raio = 10
            for i, vid in enumerate(self.vertices):
                ang = 2 * math.pi * i / n
                v   = self.vertices[vid]
                v.x_draw = raio * math.cos(ang)
                v.y_draw = raio * math.sin(ang)

        # helper para obter coordenadas robustamente
        def xy(v):
            return (getattr(v, "x_draw", getattr(v, "x_real", 0.0)),
                    getattr(v, "y_draw", getattr(v, "y_real", 0.0)))

        fig, ax = plt.subplots(figsize=(7, 7))

        # 2) desenha arestas residuais (capacidade > 0)
        for (u, v), cap in residual.items():
            if cap <= 0 or u not in self.vertices or v not in self.vertices:
                continue
            vu, vv = self.vertices[u], self.vertices[v]
            x1, y1 = xy(vu)
            x2, y2 = xy(vv)
            ax.plot([x1, x2], [y1, y2], 'grey', lw=0.6, alpha=0.6)
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my, f"{cap:.1f}", fontsize=6, color='blue')

        # 3) vértices
        for vid, vert in self.vertices.items():
            x, y = xy(vert)
            cor = 'green' if vid == origem else ('red' if vid == destino else 'black')
            ax.plot(x, y, 'o', ms=5, color=cor)
            ax.text(x+0.3, y+0.3, vid, fontsize=7)

        ax.set_aspect('equal', 'box')
        ax.set_axis_off()
        plt.title("Grafo residual (capacidades restantes)")
        plt.show()
