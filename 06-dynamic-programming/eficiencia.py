"""Comparação de eficiência: com e sem memoização, tabulação e crescimento do problema.

Mede (1) número de chamadas/células e (2) tempo em milissegundos.
Os grafos e itens "maiores" abaixo são SINTÉTICOS (gerados com semente fixa).
"""
import random
import time

from grafo import Grafo, Trecho
from orcamento import mochila_memoizacao, mochila_sem_memoizacao, mochila_tabulacao
from rotas import dijkstra, floyd_warshall, menor_custo_com_limite


def _medir(funcao):
    """Executa 'funcao' e devolve (resultado, tempo em ms)."""
    inicio = time.perf_counter()
    resultado = funcao()
    return resultado, (time.perf_counter() - inicio) * 1000


# ------------------------------------------------------------ comparações
def comparar_rotas(grafo, origem, destino, perfil, limite):
    """Rota com limite de trechos: recursão pura x memoização."""
    linhas = []
    for nome, usar_memo in (("sem memoização", False), ("com memoização", True)):
        contador = [0]
        custo, ms = _medir(lambda: menor_custo_com_limite(
            grafo, origem, destino, perfil, limite, usar_memo, contador))
        linhas.append((nome, custo, contador[0], ms))
    return linhas


def comparar_mochila(melhorias, orcamento, incluir_sem_memo=True):
    """Mochila: recursão pura x memoização x tabulação."""
    linhas = []
    if incluir_sem_memo:
        c1 = [0]
        r, ms = _medir(lambda: mochila_sem_memoizacao(melhorias, orcamento, c1))
        linhas.append(("sem memoização", r, c1[0], ms))
    c2 = [0]
    (r, _), ms = _medir(lambda: mochila_memoizacao(melhorias, orcamento, c2))
    linhas.append(("com memoização", r, c2[0], ms))
    (r, _), ms = _medir(lambda: mochila_tabulacao(melhorias, orcamento))
    # Na tabulação não há recursão: o "trabalho" é preencher (n+1)*(orçamento+1) células.
    linhas.append(("tabulação", r, (len(melhorias) + 1) * (orcamento + 1), ms))
    return linhas


# ------------------------------------------------- dados sintéticos maiores
def gerar_grafo_grade(lado, semente=1):
    """Grade lado x lado (ruas em quadras), com tempo/risco aleatórios."""
    azar = random.Random(semente)
    locais = [f"{i},{j}" for i in range(lado) for j in range(lado)]
    grafo = Grafo(locais)
    for i in range(lado):
        for j in range(lado):
            for di, dj in ((0, 1), (1, 0)):
                if i + di < lado and j + dj < lado:
                    grafo.adicionar_trecho(f"{i},{j}", f"{i + di},{j + dj}",
                                           Trecho(azar.randint(1, 9), azar.randint(0, 9), True))
    return grafo


def gerar_melhorias(n, semente=1):
    """n melhorias sintéticas com custo 1..15 e benefício 5..50."""
    azar = random.Random(semente)
    return [{"nome": f"m{i}", "custo": azar.randint(1, 15), "beneficio": azar.randint(5, 50)}
            for i in range(n)]


def escalabilidade_grafo(lados=(4, 6, 8, 10)):
    """Floyd-Warshall (todos os pares) x Dijkstra repetido, com o bairro crescendo."""
    linhas = []
    for lado in lados:
        grafo = gerar_grafo_grade(lado)
        _, ms_floyd = _medir(lambda: floyd_warshall(grafo, "segura"))
        _, ms_dijk = _medir(lambda: [dijkstra(grafo, o, "segura") for o in grafo.locais])
        linhas.append((len(grafo.locais), ms_floyd, ms_dijk))
    return linhas


def escalabilidade_mochila(tamanhos=(10, 14, 18, 22), orcamento=100):
    """Mochila com mais e mais melhorias: o 'sem memoização' explode (2^n)."""
    linhas = []
    for n in tamanhos:
        melhorias = gerar_melhorias(n)
        # Acima de 22 itens a recursão pura levaria minutos: não executamos.
        c_sem = [0]
        _, ms_sem = _medir(lambda: mochila_sem_memoizacao(melhorias, orcamento, c_sem))
        c_memo = [0]
        _, ms_memo = _medir(lambda: mochila_memoizacao(melhorias, orcamento, c_memo))
        _, ms_tab = _medir(lambda: mochila_tabulacao(melhorias, orcamento))
        linhas.append((n, c_sem[0], ms_sem, c_memo[0], ms_memo, ms_tab))
    return linhas


# ------------------------------------------------------------- impressão
def imprimir_tabela(titulo, linhas, unidade):
    print(titulo)
    print(f"  {'versão':<16}{'resultado':>10}{unidade:>20}{'tempo (ms)':>13}")
    for nome, resultado, trabalho, ms in linhas:
        print(f"  {nome:<16}{resultado:>10}{trabalho:>20}{ms:>13.3f}")


def imprimir_escala_grafo(linhas):
    print("Quantos locais -> tempo para calcular TODOS os pares (ms):")
    print(f"  {'locais':>7}{'Floyd O(V^3)':>16}{'Dijkstra x V':>16}")
    for v, f, d in linhas:
        print(f"  {v:>7}{f:>16.2f}{d:>16.2f}")


def imprimir_escala_mochila(linhas):
    print("Quantas melhorias -> chamadas e tempo (ms), orçamento 100:")
    print(f"  {'itens':>5}{'chamadas s/ memo':>18}{'ms':>10}{'chamadas memo':>16}{'ms':>9}{'tab. ms':>10}")
    for n, cs, ms_s, cm, ms_m, ms_t in linhas:
        print(f"  {n:>5}{cs:>18}{ms_s:>10.1f}{cm:>16}{ms_m:>9.2f}{ms_t:>10.2f}")
