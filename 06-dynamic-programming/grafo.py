"""Grafo do bairro: leitura dos dados simulados e custo de cada trecho de rua.

O grafo é NÃO direcionado (dá para andar nos dois sentidos) e ponderado.
Estrutura: lista de adjacência -> {local: {vizinho: Trecho}}.
"""
import json
import os
from dataclasses import dataclass, replace

# Pesos usados para transformar tempo e risco em UM único custo.
# "rapida"    -> só importa o tempo.
# "segura"    -> o risco pesa 3x mais que o tempo.
# "acessivel" -> igual a "segura", mas trechos NÃO acessíveis (escadas, calçada
#                quebrada) são proibidos (cadeirante, idoso, carrinho de bebê).
PERFIS = {
    "rapida":    {"peso_tempo": 1, "peso_risco": 0, "exige_acessivel": False},
    "segura":    {"peso_tempo": 1, "peso_risco": 3, "exige_acessivel": False},
    "acessivel": {"peso_tempo": 1, "peso_risco": 3, "exige_acessivel": True},
}

CAMINHO_PADRAO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "dados", "bairro.json")


@dataclass(frozen=True)
class Trecho:
    """Um trecho de rua entre dois locais."""
    tempo: int        # minutos a pé
    risco: int        # 0 (tranquilo) a 10 (perigoso)
    acessivel: bool   # False = tem escada, degrau ou calçada ruim


def custo_do_trecho(trecho, perfil):
    """Custo do trecho para o perfil. Retorna None se o trecho é proibido."""
    cfg = PERFIS[perfil]
    if cfg["exige_acessivel"] and not trecho.acessivel:
        return None
    return cfg["peso_tempo"] * trecho.tempo + cfg["peso_risco"] * trecho.risco


class Grafo:
    def __init__(self, locais):
        self.locais = list(locais)
        # Cada local começa sem vizinhos.
        self.adj = {local: {} for local in self.locais}

    def adicionar_trecho(self, a, b, trecho):
        """Adiciona o trecho nos dois sentidos."""
        self.adj[a][b] = trecho
        self.adj[b][a] = trecho

    def vizinhos(self, local, perfil):
        """Gera (vizinho, custo) apenas dos trechos permitidos no perfil."""
        for vizinho, trecho in self.adj[local].items():
            custo = custo_do_trecho(trecho, perfil)
            if custo is not None:
                yield vizinho, custo

    def copia(self):
        """Cópia independente (Trecho é imutável, então basta copiar os dicts)."""
        nova = Grafo(self.locais)
        for a in self.locais:
            nova.adj[a] = dict(self.adj[a])
        return nova

    def atualizar_trecho(self, a, b, **mudancas):
        """Troca campos de um trecho (ex.: acessivel=True) nos dois sentidos."""
        novo = replace(self.adj[a][b], **mudancas)
        self.adj[a][b] = novo
        self.adj[b][a] = novo


def carregar_dados(caminho=CAMINHO_PADRAO):
    """Lê o JSON inteiro (locais, trechos, orçamento e melhorias)."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def montar_grafo(dados):
    """Cria o Grafo a partir do dicionário lido do JSON.

    Valida os dados: o algoritmo de Dijkstra exige custos não negativos, e um
    nome de local errado no JSON deve gerar um erro claro, não um KeyError.
    """
    grafo = Grafo(dados["locais"])
    for t in dados["trechos"]:
        for ponta in (t["a"], t["b"]):
            if ponta not in grafo.adj:
                raise ValueError(f"Trecho usa local inexistente: {ponta}")
        if t["tempo"] < 0 or not 0 <= t["risco"] <= 10:
            raise ValueError(f"Tempo/risco inválido no trecho {t['a']}-{t['b']}")
        grafo.adicionar_trecho(t["a"], t["b"],
                               Trecho(t["tempo"], t["risco"], t["acessivel"]))
    return grafo


def nome_legivel(local):
    """'Casa_Dona_Maria' -> 'Casa Dona Maria' (só para exibir)."""
    return local.replace("_", " ")
