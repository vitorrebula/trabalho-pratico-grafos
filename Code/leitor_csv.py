import csv
from grafo import Grafo

def carregar_grafo_de_csv(caminho_arquivo):
    grafo = Grafo()
    
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)
        for linha in leitor:
            source = linha['source']
            source_x = float(linha['source_x'])
            source_y = float(linha['source_y'])

            target = linha['target']
            target_x = float(linha['target_x'])
            target_y = float(linha['target_y'])

            capacidade = float(linha['capacity_m3_day'])/1000  # novo nome da coluna
            distancia = float(linha['distance_km'])       # novo nome da coluna
            direcao = linha['direction'].strip().lower()

            grafo.adicionar_aresta(
                source, source_x, source_y,
                target, target_x, target_y,
                capacidade, distancia, direcao
            )

    return grafo


if __name__ == "__main__":
    caminho = 'rede.csv'  # Substitua pelo caminho do seu arquivo
    grafo = carregar_grafo_de_csv(caminho)
    print(grafo)
    grafo.exibir_grafo()
