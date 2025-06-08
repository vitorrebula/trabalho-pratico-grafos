import csv, re
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

from grafo import Vertice, Grafo            # já existem no seu projeto

# ------------------------------ MODELOS ---------------------------------- #
@dataclass
class Trecho:
    _id: int
    id_base_trecho: int
    id_rdagu: int
    larg_inicio: float
    larg_final: float
    lado_rdagu: str
    ind_rdagu: str
    data: Optional[str]
    geometria: str
    vertices: List[Vertice] = field(default_factory=list)

# -------------------- parser do campo GEOMETRIA -------------------------- #
ROUND = 3                                  # arredonda ~1 mm (EPSG 31983)

def _coord_id(x: float, y: float) -> str:
    """ID único por coordenada arredondada (x_y)."""
    return f"{round(x, ROUND)}_{round(y, ROUND)}"

def parse_vertices(geom: str, _prefixo_ignorado: str = "") -> List[Vertice]:
    """Extrai vértices de um LINESTRING evitando duplicatas posteriores."""
    coords_txt = geom[geom.find('(') + 1: geom.rfind(')')]
    pares = [p.strip() for p in coords_txt.split(',') if p.strip()]

    vertices: List[Vertice] = []
    for par in pares:
        x_str, y_str = re.split(r'\s+', par, maxsplit=1)
        x, y = float(x_str), float(y_str)
        vertices.append(Vertice(_coord_id(x, y), x, y))
    return vertices

# -------------------------- leitura do CSV ------------------------------ #
def carregar_trechos_do_csv(arquivo: str | Path) -> List[Trecho]:
    caminho = Path(arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho}")

    trechos: List[Trecho] = []
    with caminho.open(newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["IND_RDAGU"] != "S":
                continue
            
            geom_str   = row["GEOMETRIA"]
            prefixo_id = row["_id"]                      # id como string

            trecho = Trecho(
                _id            = int(prefixo_id),
                id_base_trecho = int(row["ID_BASE_TRECHO"]),
                id_rdagu       = int(row["ID_RDAGU"]),
                larg_inicio    = float(row["LARG_INICIO"] or 0),
                larg_final     = float(row["LARG_FINAL"]  or 0),
                lado_rdagu     = row["LADO_RDAGU"],
                ind_rdagu      = row["IND_RDAGU"],
                data           = row["DATA"] or None,
                geometria      = geom_str,
                vertices       = parse_vertices(geom_str, prefixo_id),
            )
            trechos.append(trecho)
    return trechos

# --------------------- construção (amostragem opcional) ------------------ #
def build_graph_from_csv(csv_path: str | Path,
                         max_trechos: Optional[int] = None) -> Grafo:
    trechos = carregar_trechos_do_csv(csv_path)
    if max_trechos:
        trechos = trechos[:max_trechos]

    g = Grafo()

    for trecho in trechos:
        # 1. nós deduplicados ─ pega x,y se existirem; senão usa 0,0
        for v in trecho.vertices:
            if v.id not in g.vertices:
                x = getattr(v, "x", getattr(v, "x_real", 0.0))
                y = getattr(v, "y", getattr(v, "y_real", 0.0))
                g.adicionar_vertice(v.id, x, y)

        # 2. arestas conforme LADO_RDAGU
        cap = (trecho.larg_inicio + trecho.larg_final) / 2 or trecho.larg_final
        bidirecional = trecho.lado_rdagu.upper() == "A"

        for a, b in zip(trecho.vertices, trecho.vertices[1:]):
            g.adicionar_aresta(a.id, b.id, cap)       # ida
            if bidirecional:                          # volta se 'A'
                g.adicionar_aresta(b.id, a.id, cap)

    return g

# ---------------------------- uso rápido --------------------------------- #
if __name__ == "__main__":
    csv_path = Path(__file__).with_name("rede.csv")

    grafo = build_graph_from_csv(csv_path, 500)  # limite opcional
    print("Vértices:", len(grafo.vertices), "| Arestas:", len(grafo.arestas))
    grafo.desenhar()
