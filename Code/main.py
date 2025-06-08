from leitor_csv import carregar_grafo_de_csv

def main():
    caminho_arquivo = 'rede.csv'  # Altere se o caminho do seu arquivo for diferente
    grafo = carregar_grafo_de_csv(caminho_arquivo)

    print("\n--- Grafo Carregado ---")
    print(grafo)

    print("\n--- Exibindo Grafo Visualmente ---")
    grafo.exibir_grafo()


if __name__ == "__main__":
    main()
