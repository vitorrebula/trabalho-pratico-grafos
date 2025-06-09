import tkinter as tk
from tkinter import messagebox
from leitor_csv import carregar_grafo_de_csv

# Carrega o grafo
grafo = carregar_grafo_de_csv('rede.csv')
todos_vertices = list(grafo.vertices.keys())

# Interface Visual
root = tk.Tk()
root.title("Fluxo de ")
root.geometry("500x400")

label = tk.Label(root, text="Escolha uma opção:", font=("Arial", 14))
label.pack(pady=10)

# Seletor de origem
frame_origem = tk.Frame(root)
tk.Label(frame_origem, text="Origem:").pack(side=tk.LEFT)
var_origem = tk.StringVar(value=todos_vertices[0])
menu_origem = tk.OptionMenu(frame_origem, var_origem, *todos_vertices)
menu_origem.pack(side=tk.LEFT)
frame_origem.pack(pady=5)

# Seletor de destino
frame_destino = tk.Frame(root)
tk.Label(frame_destino, text="Destino:").pack(side=tk.LEFT)
var_destino = tk.StringVar(value=todos_vertices[1])
menu_destino = tk.OptionMenu(frame_destino, var_destino, *todos_vertices)
menu_destino.pack(side=tk.LEFT)
frame_destino.pack(pady=5)

# Funções com origem/destino dinâmicos
def exibir_grafo():
    grafo.exibir_grafo()

def calcular_fluxo():
    origem = var_origem.get()
    destino = var_destino.get()
    fluxoValor, _ = grafo.calcular_fluxo_maximo(origem, destino)
    grafo.exibir_fluxo_maximo(origem, destino)
    messagebox.showinfo("Fluxo Máximo", f"Fluxo máximo de '{origem}' para '{destino}': {fluxoValor} m³/dia")

def exibir_residual():
    origem = var_origem.get()
    destino = var_destino.get()
    _, fluxoDict = grafo.calcular_fluxo_maximo(origem, destino)
    grafo.desenhar_rede_residual(grafo, fluxoDict)

def sugerir_cano():
    origem = var_origem.get()
    destino = var_destino.get()
    grafo.exibir_fluxo_e_gargalo(origem, destino)

def sair():
    root.destroy()

# Botões
botao_a = tk.Button(root, text="A - Exibir Grafo", width=40, command=exibir_grafo)
botao_b = tk.Button(root, text="B - Calcular Fluxo Máximo", width=40, command=calcular_fluxo)
botao_c = tk.Button(root, text="C - Exibir Rede Residual", width=40, command=exibir_residual)
botao_d = tk.Button(root, text="D - Sugerir Cano para Aumentar Capacidade", width=40, command=sugerir_cano)
botao_e = tk.Button(root, text="Sair", width=40, command=sair)

for botao in [botao_a, botao_b, botao_c, botao_d, botao_e]:
    botao.pack(pady=6)

root.mainloop()
