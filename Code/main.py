from leitor_csv import carregar_grafo_de_csv

def main():
    caminho = 'rede.csv'
    grafo = carregar_grafo_de_csv(caminho)

    origem = "Source_Spring_Gamma"
    destino = "Demand_Agriculture"

    grafo.exibir_fluxo_maximo(origem, destino)  # Desenha grafo com fluxo máximo

if __name__ == "__main__":
    main()
