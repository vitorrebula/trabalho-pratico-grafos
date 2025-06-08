from collections import deque, defaultdict

def fluxo_maximo_edmonds_karp(self, origem, destino):
    # Constrói o grafo residual com capacidades e fluxo
    capacidade = defaultdict(dict)
    for vertice in self.vertices.values():
        for aresta in vertice.arestas:
            u, v = aresta.origem.nome, aresta.destino.nome
            capacidade[u][v] = capacidade[u].get(v, 0) + aresta.capacidade
            if v not in capacidade or u not in capacidade[v]:
                capacidade[v][u] = capacidade[v].get(u, 0)  # reversa com 0 capacidade inicial

    fluxo = defaultdict(lambda: defaultdict(int))

    def bfs():
        pai = {}
        visitado = set()
        fila = deque([origem])
        visitado.add(origem)
        while fila:
            u = fila.popleft()
            for v in capacidade[u]:
                if v not in visitado and capacidade[u][v] - fluxo[u][v] > 0:
                    pai[v] = u
                    visitado.add(v)
                    if v == destino:
                        return pai
                    fila.append(v)
        return None

    fluxo_total = 0
    while True:
        caminho = bfs()
        if not caminho:
            break

        # Determina o gargalo do caminho
        v = destino
        gargalo = float('inf')
        while v != origem:
            u = caminho[v]
            gargalo = min(gargalo, capacidade[u][v] - fluxo[u][v])
            v = u

        # Atualiza fluxo ao longo do caminho
        v = destino
        while v != origem:
            u = caminho[v]
            fluxo[u][v] += gargalo
            fluxo[v][u] -= gargalo
            v = u

        fluxo_total += gargalo

    return fluxo_total, fluxo
