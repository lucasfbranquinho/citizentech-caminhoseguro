"""Alocação ótima do orçamento da prefeitura/associação: mochila 0/1.

Dado um orçamento (em mil R$) e uma lista de melhorias, cada uma com custo e
benefício (pessoas beneficiadas, simulado), escolher o conjunto de maior
benefício total sem estourar o orçamento. Cada melhoria é feita 0 ou 1 vez.

Duas versões da MESMA recorrência (para comparar):
  - mochila_memoizacao (top-down)
  - mochila_tabulacao  (bottom-up)
Recorrência: melhor(i, c) = maior benefício usando as melhorias i..fim com c de orçamento
    melhor(n, c) = 0
    melhor(i, c) = max( melhor(i+1, c),                               (não faz)
                        b_i + melhor(i+1, c - custo_i) se custo_i<=c ) (faz)
"""


def mochila_memoizacao(melhorias, orcamento, contador=None):
    """Top-down com dicionário. Retorna (benefício, lista de melhorias escolhidas)."""
    memo = {}
    n = len(melhorias)

    def melhor(i, c):
        if contador is not None:
            contador[0] += 1
        if i == n:
            return 0
        if (i, c) in memo:
            return memo[(i, c)]
        resultado = melhor(i + 1, c)  # opção 1: não fazer
        if melhorias[i]["custo"] <= c:  # opção 2: fazer
            resultado = max(resultado,
                            melhorias[i]["beneficio"] + melhor(i + 1, c - melhorias[i]["custo"]))
        memo[(i, c)] = resultado
        return resultado

    total = melhor(0, orcamento)
    # Reconstrução: em cada melhoria, se "fazer" não mudou o valor, ela ficou de fora.
    escolhidas, c = [], orcamento
    for i in range(n):
        if melhor(i, c) != melhor(i + 1, c):
            escolhidas.append(melhorias[i])
            c -= melhorias[i]["custo"]
    return total, escolhidas


def mochila_tabulacao(melhorias, orcamento):
    """Bottom-up com tabela. Retorna (benefício, lista de melhorias escolhidas).

    tabela[i][c] = maior benefício usando só as i primeiras melhorias com orçamento c.
    Tempo e espaço: O(n * orçamento).
    """
    n = len(melhorias)
    tabela = [[0] * (orcamento + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        custo = melhorias[i - 1]["custo"]
        beneficio = melhorias[i - 1]["beneficio"]
        for c in range(orcamento + 1):
            tabela[i][c] = tabela[i - 1][c]  # não fazer
            if custo <= c:                    # fazer, se couber
                tabela[i][c] = max(tabela[i][c], beneficio + tabela[i - 1][c - custo])
    # Reconstrução: anda de trás para frente na tabela.
    escolhidas, c = [], orcamento
    for i in range(n, 0, -1):
        if tabela[i][c] != tabela[i - 1][c]:  # a melhoria i foi usada
            escolhidas.append(melhorias[i - 1])
            c -= melhorias[i - 1]["custo"]
    escolhidas.reverse()
    return tabela[n][orcamento], escolhidas


def mochila_sem_memoizacao(melhorias, orcamento, contador=None):
    """Recursão pura, SEM memoização (até 2^n chamadas). Só para comparar eficiência."""
    def melhor(i, c):
        if contador is not None:
            contador[0] += 1
        if i == len(melhorias):
            return 0
        resultado = melhor(i + 1, c)
        if melhorias[i]["custo"] <= c:
            resultado = max(resultado,
                            melhorias[i]["beneficio"] + melhor(i + 1, c - melhorias[i]["custo"]))
        return resultado
    return melhor(0, orcamento)


def aplicar_melhorias(grafo, melhorias_escolhidas):
    """Devolve um NOVO grafo com os efeitos das melhorias (rampas, iluminação)."""
    novo = grafo.copia()
    for m in melhorias_escolhidas:
        efeito = m.get("efeito")
        if not efeito:
            continue
        if efeito["tipo"] == "tornar_acessivel":
            novo.atualizar_trecho(efeito["a"], efeito["b"], acessivel=True)
        elif efeito["tipo"] == "reduzir_risco":
            novo.atualizar_trecho(efeito["a"], efeito["b"], risco=efeito["novo_risco"])
    return novo
