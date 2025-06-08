from collections import deque

def edmonds_karp(grafo, origem, destino):
    capacidade = {}
    for aresta in grafo.arestas:
        capacidade[(aresta.origem, aresta.destino)] = aresta.capacidade
        capacidade[(aresta.destino, aresta.origem)] = 0  # aresta reversa

    fluxo_maximo = 0

    while True:
        pai = {v: None for v in grafo.vertices}
        fila = deque()
        fila.append(origem)

        while fila:
            u = fila.popleft()
            for v in grafo.vertices:
                if v != u and (u, v) in capacidade and capacidade[(u, v)] > 0 and pai[v] is None:
                    pai[v] = u
                    fila.append(v)
                    if v == destino:
                        break

        if pai[destino] is None:
            break

        caminho_fluxo = float('inf')
        v = destino
        while v != origem:
            u = pai[v]
            caminho_fluxo = min(caminho_fluxo, capacidade[(u, v)])
            v = u

        v = destino
        while v != origem:
            u = pai[v]
            capacidade[(u, v)] -= caminho_fluxo
            capacidade[(v, u)] += caminho_fluxo
            v = u

        fluxo_maximo += caminho_fluxo

    # Retorna fluxo máximo e grafo residual
    return fluxo_maximo, capacidade
