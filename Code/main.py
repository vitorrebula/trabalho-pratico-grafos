import tkinter as tk
from tkinter import messagebox
from leitor_csv import carregar_grafo_de_csv

# Define os pontos fixos
origem = "Source_Spring_Gamma"
destino = "Demand_Agriculture"

# Carrega o grafo uma vez
grafo = carregar_grafo_de_csv('rede.csv')

def exibir_grafo():
    grafo.exibir_grafo()

def calcular_fluxo():
    fluxoValor, _ = grafo.calcular_fluxo_maximo(origem, destino)
    grafo.exibir_fluxo_maximo(origem, destino)
    messagebox.showinfo("Fluxo Máximo", f"Fluxo máximo de '{origem}' para '{destino}': {fluxoValor}")

def exibir_residual():
    _, fluxoDict = grafo.calcular_fluxo_maximo(origem, destino)
    grafo.desenhar_rede_residual(grafo, fluxoDict)

def sugerir_cano():
    sugestao = grafo.exibir_fluxo_e_gargalo(origem, destino)

def sair():
    root.destroy()

# Interface Tkinter
root = tk.Tk()
root.title("Análise de Rede de Fluxo")
root.geometry("400x300")

label = tk.Label(root, text="Escolha uma opção:", font=("Arial", 14))
label.pack(pady=20)

botao_a = tk.Button(root, text="A - Exibir Grafo", width=30, command=exibir_grafo)
botao_b = tk.Button(root, text="B - Calcular Fluxo Máximo", width=30, command=calcular_fluxo)
botao_c = tk.Button(root, text="C - Exibir Rede Residual", width=30, command=exibir_residual)
botao_d = tk.Button(root, text="D - Sugerir Cano para Aumentar Capacidade", width=30, command=sugerir_cano)
botao_e = tk.Button(root, text="Sair", width=30, command=sair)

for botao in [botao_a, botao_b, botao_c, botao_d, botao_e]:
    botao.pack(pady=5)

root.mainloop()