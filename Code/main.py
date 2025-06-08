# main.py
# ---------------------------------------------------------------------------
# Interface simples em linha de comando
# 1) escolhe quantos trechos do CSV carregar
# 2) calcula fluxo máximo (Edmonds-Karp) entre dois vértices
# 3) exibe grafo residual
# ---------------------------------------------------------------------------

from pathlib import Path
from readcsv import build_graph_from_csv        # já lê, filtra e monta Grafo
from fluxoMaximo import edmonds_karp
from grafo import Grafo

CSV_DEFAULT = Path(__file__).with_name("rede.csv")


def criar_grafo() -> Grafo:
    csv_path = input(f"⮞ CSV [{CSV_DEFAULT}]: ").strip() or CSV_DEFAULT
    while True:
        try:
            n = int(input("⮞ Quantos trechos carregar (0 = todos): "))
            break
        except ValueError:
            print("Digite um número inteiro.")
    g = build_graph_from_csv(csv_path, None if n == 0 else n)
    print(f"[OK] Grafo com {len(g.vertices)} vértices e {len(g.arestas)} arestas.")
    return g


def escolher_vertice(g: Grafo, label: str) -> str:
    """
    Solicita ao usuário o id do vértice.
    • Digite “listar” para exibir todos os ids disponíveis.
    """
    while True:
        v = input(f"⮞ Id do vértice {label} (ou 'listar'): ").strip()
        if v.lower() == "listar":
            print("\nIds disponíveis:")
            for vid in g.vertices:
                print("  ", vid)
            continue
        if v in g.vertices:
            return v
        print("Id inexistente – tente de novo.")


def mostrar_menu():
    print("\n=== MENU ===")
    print("1  Criar/recargar grafo")
    print("2  Estatísticas rápidas")
    print("3  Desenhar grafo")
    print("4  Fluxo máximo + grafo residual")
    print("0  Sair")


def main():
    grafo: Grafo | None = None
    residual = None

    while True:
        mostrar_menu()
        op = input("Opção: ").strip()

        if op == "1":
            grafo = criar_grafo()
            residual = None

        elif op == "2":
            if not grafo:
                print("Crie o grafo primeiro.")
                continue
            print(f"Vértices: {len(grafo.vertices)} | Arestas: {len(grafo.arestas)}")

        elif op == "3":
            if not grafo:
                print("Crie o grafo primeiro.")
                continue
            grafo.desenhar()

        elif op == "4":
            if not grafo:
                print("Crie o grafo primeiro.")
                continue
            src = escolher_vertice(grafo, "origem")
            dst = escolher_vertice(grafo, "destino")
            fluxo, residual = edmonds_karp(grafo, src, dst)
            print(f"Fluxo máximo de {src} → {dst}: {fluxo}")
            # desenha grafo residual, se seu Grafo tiver esse método
            if hasattr(grafo, "desenhar_com_residual"):
                grafo.desenhar_com_residual(residual, src, dst)

        elif op == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
