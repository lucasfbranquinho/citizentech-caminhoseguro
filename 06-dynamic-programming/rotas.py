"""Algoritmos de rota no grafo do bairro.

1. dijkstra               -> menor custo de UM local até todos (fila de prioridade).
2. floyd_warshall         -> TABULAÇÃO (DP): menor custo entre TODOS os pares.
3. menor_custo_com_limite -> MEMOIZAÇÃO (DP): menor custo usando no máximo k trechos.
"""
import heapq

INFINITO = float("inf")


def reconstruir_caminho(anterior, origem, destino):
    """Segue o dicionário 'anterior' de trás para frente e inverte."""
    if destino != origem and destino not in anterior:
        return None  # não existe caminho
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


# ---------------------------------------------------------------- Dijkstra
def dijkstra(grafo, origem, perfil):
    """Retorna (custos, anterior). Custos ficam INFINITO se o local é inalcançável.

    Complexidade: O((V + E) log V) com heap.
    """
    custos = {local: INFINITO for local in grafo.locais}
    anterior = {}
    custos[origem] = 0
    fila = [(0, origem)]  # (custo acumulado, local)
    while fila:
        custo_atual, local = heapq.heappop(fila)
        if custo_atual > custos[local]:
            continue  # entrada velha da fila, já achamos algo melhor
        for vizinho, custo_trecho in grafo.vizinhos(local, perfil):
            novo = custo_atual + custo_trecho
            if novo < custos[vizinho]:
                custos[vizinho] = novo
                anterior[vizinho] = local
                heapq.heappush(fila, (novo, vizinho))
    return custos, anterior


def melhor_rota(grafo, origem, destino, perfil):
    """Atalho: devolve (custo, caminho) ou (INFINITO, None) se não há rota."""
    custos, anterior = dijkstra(grafo, origem, perfil)
    if custos[destino] == INFINITO:
        return INFINITO, None
    return custos[destino], reconstruir_caminho(anterior, origem, destino)


# ----------------------------------------------------------- Floyd-Warshall
def floyd_warshall(grafo, perfil):
    """TABULAÇÃO: preenche a tabela dist[i][j] com o menor custo i -> j.

    Subproblema: dist_k[i][j] = menor custo de i até j usando só os primeiros k
    locais como "pontos de passagem". A recorrência é
        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    Retorna (dist, proximo). 'proximo[i][j]' = primeiro passo de i para chegar a j.
    Complexidade: O(V^3) tempo, O(V^2) espaço.
    """
    locais = grafo.locais
    dist = {i: {j: INFINITO for j in locais} for i in locais}
    proximo = {i: {j: None for j in locais} for i in locais}
    for i in locais:
        dist[i][i] = 0
        for vizinho, custo in grafo.vizinhos(i, perfil):
            dist[i][vizinho] = custo
            proximo[i][vizinho] = vizinho
    for k in locais:          # k = novo ponto de passagem permitido
        for i in locais:
            for j in locais:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    proximo[i][j] = proximo[i][k]
    return dist, proximo


def caminho_floyd(proximo, origem, destino):
    """Reconstrói o caminho usando a tabela 'proximo' do Floyd-Warshall."""
    if origem != destino and proximo[origem][destino] is None:
        return None
    caminho = [origem]
    while caminho[-1] != destino:
        caminho.append(proximo[caminho[-1]][destino])
    return caminho


def rota_com_parada(dist, proximo, origem, parada, destino):
    """Rota origem -> parada -> destino (ex.: passar na farmácia no caminho).

    Aproveita a tabela do Floyd-Warshall: o custo é só dist[o][p] + dist[p][d],
    uma consulta O(1), sem rodar nenhum algoritmo de novo.
    Retorna (custo, caminho) ou (INFINITO, None).
    """
    custo = dist[origem][parada] + dist[parada][destino]
    if custo == INFINITO:
        return INFINITO, None
    ida = caminho_floyd(proximo, origem, parada)
    volta = caminho_floyd(proximo, parada, destino)
    return custo, ida + volta[1:]  # volta[1:] evita repetir a parada


def ranking_pontos_de_apoio(dist, locais):
    """Onde instalar um ponto de apoio (banco, sombra, bebedouro)?

    Pontua cada local pela SOMA dos custos até todos os outros (quanto menor,
    mais central). Ignora locais que não alcançam todos os demais. Usa a tabela
    do Floyd-Warshall. Retorna lista [(soma, local)] do mais ao menos central.
    """
    ranking = []
    for candidato in locais:
        soma = sum(dist[candidato][outro] for outro in locais)
        if soma != INFINITO:
            ranking.append((soma, candidato))
    return sorted(ranking)


# ------------------------------------------- Memoização: limite de trechos
def menor_custo_com_limite(grafo, origem, destino, perfil, max_trechos,
                           usar_memo=True, contador=None):
    """Menor custo de origem até destino usando NO MÁXIMO max_trechos trechos.

    Útil para "não quero uma rota com mais de k esquinas" (idoso, criança).
    Subproblema: f(local, k) = menor custo de 'local' até destino com k trechos.
        f(destino, k) = 0
        f(local, 0)   = INFINITO   (se local != destino)
        f(local, k)   = min sobre vizinhos v de ( custo(local, v) + f(v, k-1) )
    Sem memoização o mesmo (local, k) é recalculado muitas vezes (exponencial);
    com memoização cada par é resolvido uma vez: O(V * k * grau).

    'contador' é uma lista [n] usada só para contar as chamadas (comparação).
    Retorna o custo (INFINITO se impossível nesse limite).
    """
    if max_trechos < 0:
        raise ValueError("o número máximo de trechos não pode ser negativo")
    memo = {}

    def f(local, k):
        if contador is not None:
            contador[0] += 1
        if local == destino:
            return 0
        if k == 0:
            return INFINITO
        if usar_memo and (local, k) in memo:
            return memo[(local, k)]
        melhor = INFINITO
        for vizinho, custo in grafo.vizinhos(local, perfil):
            melhor = min(melhor, custo + f(vizinho, k - 1))
        if usar_memo:
            memo[(local, k)] = melhor
        return melhor

    return f(origem, max_trechos)
