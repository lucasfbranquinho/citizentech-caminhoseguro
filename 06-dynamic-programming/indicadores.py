"""Indicadores de impacto (pergunta 6 da CitizenTech: como medir o impacto?).

Comparam o bairro ANTES e DEPOIS das melhorias escolhidas na mochila.
"""
from rotas import INFINITO, floyd_warshall


def percentual_trechos_acessiveis(grafo):
    """% dos trechos de rua que podem ser usados por cadeirante/idoso."""
    trechos = {}
    for a in grafo.locais:
        for b, trecho in grafo.adj[a].items():
            trechos[frozenset((a, b))] = trecho  # cada trecho conta uma vez
    if not trechos:
        return 0.0
    return 100 * sum(t.acessivel for t in trechos.values()) / len(trechos)


def percentual_pares_com_rota_acessivel(grafo):
    """% dos pares de locais (A, B), A != B, ligados por alguma rota acessível."""
    dist, _ = floyd_warshall(grafo, "acessivel")
    locais = grafo.locais
    pares = [(a, b) for a in locais for b in locais if a != b]
    if not pares:
        return 0.0
    ok = sum(1 for a, b in pares if dist[a][b] != INFINITO)
    return 100 * ok / len(pares)


def custo_medio_rota_acessivel(grafo):
    """Custo médio (tempo + 3 x risco) das rotas acessíveis que existem."""
    dist, _ = floyd_warshall(grafo, "acessivel")
    custos = [dist[a][b] for a in grafo.locais for b in grafo.locais
              if a != b and dist[a][b] != INFINITO]
    return sum(custos) / len(custos) if custos else INFINITO


def resumo(grafo):
    """Dicionário com os três indicadores."""
    return {
        "trechos_acessiveis_%": percentual_trechos_acessiveis(grafo),
        "pares_com_rota_acessivel_%": percentual_pares_com_rota_acessivel(grafo),
        "custo_medio_rota_acessivel": custo_medio_rota_acessivel(grafo),
    }
