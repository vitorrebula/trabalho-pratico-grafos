# 1. Use Case – Monitoramento da Rede de Água plantuml

"
@startuml
actor "Operador do Sistema" as Operador

rectangle "Sistema de Gerenciamento de Rede" {
    usecase "Escolher Algoritmo de Fluxo Máximo" as UC1
    usecase "Carregar Dados da Rede" as UC2
    usecase "Filtrar Tubulações Inativas" as UC3
    usecase "Simular Falhas na Rede" as UC4
    usecase "Calcular Fluxo Máximo" as UC5
    usecase "Sugerir Rota Alternativa" as UC6
    usecase "Visualizar Resultados" as UC7 
}

Operador --> UC1
Operador --> UC2
Operador --> UC3
Operador --> UC4

UC1 --> UC5 : <<include>>
UC5 --> UC6 : <<extends>>
UC5 --> UC7 : <<extends>>
@enduml
"

======================================================================
# Class Diagram – Estrutura dos Objetos no Grafo plantuml

"
@startuml
' =================== CLASSES PRINCIPAIS ===================
class RedeDeAgua {
  - vertices : List<No>
  - arestas  : List<Tubo>
  + carregar_dados()
  + filtrar_tubos_inativos()
  + construir_grafo()
}

class No {
  + id   : str
  + tipo : str
}

class Tubo {
  + origem     : No
  + destino    : No
  + capacidade : float
  + fluxo      : float
  + status     : string
}

class AlgoritmoFluxoMaximo {
  + calcular_fluxo_maximo(g : RedeDeAgua) : float
  - construir_rede_residual()
  - encontrar_caminho_aumentante()
  - atualizar_fluxos()
  - caminho_disponivel() : bool
}

class RedeResidual {
  - arestas_residuais : List<Tubo>
  + gerar_a_partir(g : RedeDeAgua)
  + obter_caminho(orig : No, dest : No) : List<Tubo>
}

' =================== RELACIONAMENTOS ===================
' Rede → Nós e Tubos
RedeDeAgua "1" o-- "*" No
RedeDeAgua "1" o-- "*" Tubo

' Tubo conecta dois nós
Tubo "1" --* "2" No

' Algoritmo usa a Rede (dependência – seta tracejada)
RedeDeAgua ..> AlgoritmoFluxoMaximo : usa

' Algoritmo compõe uma Rede Residual interna
AlgoritmoFluxoMaximo *-- "1" RedeResidual : constrói

' Rede Residual contém Tubos residuais
RedeResidual "1" o-- "*" Tubo

@enduml

"

======================================================================
# Activity Diagram – Processo de Execução da Solução plantuml

"
@startuml
start

:Importar dados da rede;
:Construir grafo com vértices e arestas;
:Filtrar arestas com status inativo;

if (Rede conectada?) then (sim)
    :Selecionar algoritmo de fluxo máximo;
    :Construir rede residual;

    repeat
        :Encontrar caminho aumentante;
        :Atualizar fluxos na\nrede residual;
      repeat while (Caminho disponível?)

    :Salvar fluxo total;

    :Simular falhas nos tubos críticos;

    if (Existe nova rota?) then (sim)
        :Gerar rede residual\n(após falha);
        :Recalcular fluxo máximo;
        :Comparar impacto da falha;
    else (não)
        :Notificar ruptura crítica;
    endif

    :Visualizar resultados;
else
    :Erro de conectividade;
endif

stop
@enduml

"