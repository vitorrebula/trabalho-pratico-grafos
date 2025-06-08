import csv
import os
import re
from grafo import Grafo

class Linha:
    def __init__(self, dados: dict):
        self.geometria = dados.get("GEOMETRIA", "")
        self.vertices = self.extrair_vertices(self.geometria)

    def extrair_vertices(self, geometria: str):
        if not geometria.startswith("LINESTRING"):
            return []
        coords = re.findall(r"\((.*?)\)", geometria)
        if not coords:
            return []
        pts = [tuple(map(float, p.strip().split())) for p in coords[0].split(",")]
        return pts

def build_graph_from_csv(nome_arquivo: str) -> Grafo:
    grafo = Grafo()
    caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)

    # carrega todas as linhas para podermos contar, se quiser
    with open(caminho, newline='', encoding='utf-8') as f:
        todas = list(csv.DictReader(f))

    for idx, row in enumerate(todas, start=1):
        input(f"\nPressione Enter para processar Linha {idx}/{len(todas)}...")
        linha = Linha(row)
        print(f"Processando Linha {idx}:")
        # exibe subnames e coords
        for vidx, (x, y) in enumerate(linha.vertices, start=1):
            subname = f"v{idx}_{vidx}"
            print(f"  {subname} -> ({x:.2f}, {y:.2f})")

        # adiciona vértices e arestas
        for (x1, y1), (x2, y2) in zip(linha.vertices, linha.vertices[1:]):
            id1 = f"{x1:.2f},{y1:.2f}"
            id2 = f"{x2:.2f},{y2:.2f}"

            if id1 not in grafo.vertices:
                grafo.adicionar_vertice(id1, x1, y1)
                print(f"    Vértice criado: {id1}")
            else:
                print(f"    Vértice já existe: {id1}")

            if id2 not in grafo.vertices:
                grafo.adicionar_vertice(id2, x2, y2)
                print(f"    Vértice criado: {id2}")
            else:
                print(f"    Vértice já existe: {id2}")

            grafo.adicionar_aresta(id1, id2, capacidade=0)
            print(f"    Aresta criada: {id1} -> {id2} (cap=0)")

    return grafo

if __name__ == "__main__":
    g = build_graph_from_csv("rede.csv")
    print(f"\nGrafo construído: {len(g.vertices)} vértices, {len(g.arestas)} arestas")
    # para visualizar, descomente:
    # g.desenhar()
