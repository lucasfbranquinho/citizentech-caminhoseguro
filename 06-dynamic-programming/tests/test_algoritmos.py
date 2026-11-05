"""Testes automáticos (unittest). Rodar na pasta do projeto: python -m unittest -v"""
import itertools
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import indicadores  # noqa: E402
from eficiencia import gerar_grafo_grade, gerar_melhorias  # noqa: E402
from grafo import Grafo, Trecho, carregar_dados, montar_grafo  # noqa: E402
from orcamento import (aplicar_melhorias, mochila_memoizacao,  # noqa: E402
                       mochila_sem_memoizacao, mochila_tabulacao)
from rotas import (INFINITO, caminho_floyd, dijkstra, floyd_warshall,  # noqa: E402
                   melhor_rota, menor_custo_com_limite, ranking_pontos_de_apoio,
                   rota_com_parada)


def grafo_pequeno():
    """A-B (1), B-C (1), A-C (5): o melhor de A até C passa por B (custo 2).
    C-D só existe com acessivel=False, para testar o perfil acessível."""
    g = Grafo(["A", "B", "C", "D"])
    g.adicionar_trecho("A", "B", Trecho(1, 0, True))
    g.adicionar_trecho("B", "C", Trecho(1, 0, True))
    g.adicionar_trecho("A", "C", Trecho(5, 0, True))
    g.adicionar_trecho("C", "D", Trecho(2, 0, False))
    return g


class TestRotas(unittest.TestCase):
    def test_dijkstra_caso_conhecido(self):
        custo, caminho = melhor_rota(grafo_pequeno(), "A", "C", "rapida")
        self.assertEqual(custo, 2)
        self.assertEqual(caminho, ["A", "B", "C"])

    def test_perfil_acessivel_bloqueia_trecho(self):
        g = grafo_pequeno()
        self.assertEqual(melhor_rota(g, "A", "D", "rapida")[0], 4)
        custo, caminho = melhor_rota(g, "A", "D", "acessivel")
        self.assertEqual(custo, INFINITO)
        self.assertIsNone(caminho)

    def test_floyd_igual_dijkstra_no_bairro(self):
        grafo = montar_grafo(carregar_dados())
        for perfil in ("rapida", "segura", "acessivel"):
            dist, proximo = floyd_warshall(grafo, perfil)
            for origem in grafo.locais:
                custos, _ = dijkstra(grafo, origem, perfil)
                for destino in grafo.locais:
                    self.assertEqual(dist[origem][destino], custos[destino])

    def test_caminho_floyd_soma_o_custo(self):
        g = grafo_pequeno()
        dist, proximo = floyd_warshall(g, "rapida")
        self.assertEqual(caminho_floyd(proximo, "A", "D"), ["A", "B", "C", "D"])
        self.assertEqual(dist["A"]["D"], 4)

    def test_memoizacao_respeita_limite_de_trechos(self):
        g = grafo_pequeno()
        self.assertEqual(menor_custo_com_limite(g, "A", "C", "rapida", 1), 5)  # só A-C direto
        self.assertEqual(menor_custo_com_limite(g, "A", "C", "rapida", 2), 2)  # A-B-C
        self.assertEqual(menor_custo_com_limite(g, "A", "D", "rapida", 1), INFINITO)
        self.assertEqual(menor_custo_com_limite(g, "A", "D", "rapida", 2), 7)  # A-C-D
        self.assertEqual(menor_custo_com_limite(g, "A", "D", "rapida", 3), 4)  # A-B-C-D

    def test_memoizacao_igual_sem_memoizacao_e_dijkstra(self):
        grafo = montar_grafo(carregar_dados())
        esperado, _ = melhor_rota(grafo, "Casa_Dona_Maria", "Posto_de_Saude", "segura")
        com = menor_custo_com_limite(grafo, "Casa_Dona_Maria", "Posto_de_Saude", "segura", 8, True)
        sem = menor_custo_com_limite(grafo, "Casa_Dona_Maria", "Posto_de_Saude", "segura", 8, False)
        self.assertEqual(com, esperado)
        self.assertEqual(sem, esperado)

    def test_memoizacao_faz_menos_chamadas(self):
        grafo = montar_grafo(carregar_dados())
        c_sem, c_com = [0], [0]
        menor_custo_com_limite(grafo, "Casa_Dona_Maria", "Centro_Comunitario", "segura", 10, False, c_sem)
        menor_custo_com_limite(grafo, "Casa_Dona_Maria", "Centro_Comunitario", "segura", 10, True, c_com)
        self.assertLess(c_com[0] * 10, c_sem[0])


class TestFuncionalidadesExtras(unittest.TestCase):
    def test_rota_com_parada(self):
        g = grafo_pequeno()
        dist, proximo = floyd_warshall(g, "rapida")
        custo, caminho = rota_com_parada(dist, proximo, "A", "B", "D")
        self.assertEqual(custo, 4)
        self.assertEqual(caminho, ["A", "B", "C", "D"])
        # Parada fora do caminho obriga o desvio: A -> C (2) + C -> B (1) + B -> D (3)
        custo, caminho = rota_com_parada(dist, proximo, "A", "D", "B")
        self.assertEqual(custo, 4 + 3)
        self.assertEqual(caminho, ["A", "B", "C", "D", "C", "B"])

    def test_rota_com_parada_inalcancavel(self):
        g = grafo_pequeno()
        dist, proximo = floyd_warshall(g, "acessivel")  # D fica isolado
        self.assertEqual(rota_com_parada(dist, proximo, "A", "D", "C"), (INFINITO, None))

    def test_ranking_pontos_de_apoio(self):
        # Em A-B-C (linha), o meio (B) é o mais central; D isolado no perfil acessível
        # é ignorado, pois não alcança os outros.
        g = grafo_pequeno()
        dist, _ = floyd_warshall(g, "rapida")
        ranking = ranking_pontos_de_apoio(dist, g.locais)
        self.assertEqual(ranking[0][1], "B")
        dist_ac, _ = floyd_warshall(g, "acessivel")
        locais = [local for _, local in ranking_pontos_de_apoio(dist_ac, g.locais)]
        self.assertNotIn("D", locais)

    def test_indicadores_antes_e_depois(self):
        dados = carregar_dados()
        grafo = montar_grafo(dados)
        rampa = [m for m in dados["melhorias"] if "Rampa na escadaria" in m["nome"]]
        depois = aplicar_melhorias(grafo, rampa)
        antes_pct = indicadores.percentual_trechos_acessiveis(grafo)
        depois_pct = indicadores.percentual_trechos_acessiveis(depois)
        self.assertAlmostEqual(antes_pct, 85.0)       # 17 de 20 trechos
        self.assertAlmostEqual(depois_pct, 90.0)      # 18 de 20 trechos
        self.assertLess(indicadores.custo_medio_rota_acessivel(depois),
                        indicadores.custo_medio_rota_acessivel(grafo))

    def test_pares_com_rota_acessivel_em_grafo_pequeno(self):
        # 4 locais = 12 pares ordenados; D só liga por trecho não acessível
        # -> sobram os 6 pares entre A, B e C.
        self.assertAlmostEqual(
            indicadores.percentual_pares_com_rota_acessivel(grafo_pequeno()), 50.0)

    def test_montar_grafo_rejeita_dados_invalidos(self):
        base = {"locais": ["A", "B"],
                "trechos": [{"a": "A", "b": "Z", "tempo": 1, "risco": 1, "acessivel": True}]}
        with self.assertRaises(ValueError):
            montar_grafo(base)  # local inexistente
        base["trechos"][0].update(b="B", tempo=-1)
        with self.assertRaises(ValueError):
            montar_grafo(base)  # tempo negativo

    def test_grafo_desconexo_nao_tem_rota(self):
        g = Grafo(["A", "B"])
        self.assertEqual(melhor_rota(g, "A", "B", "rapida"), (INFINITO, None))
        self.assertEqual(melhor_rota(g, "A", "A", "rapida"), (0, ["A"]))

    def test_grafo_sintetico_floyd_igual_dijkstra(self):
        g = gerar_grafo_grade(5)
        dist, _ = floyd_warshall(g, "segura")
        for origem in ("0,0", "2,3", "4,4"):
            custos, _ = dijkstra(g, origem, "segura")
            self.assertEqual(custos, dist[origem])

    def test_mochila_sintetica_memo_igual_tabulacao(self):
        itens = gerar_melhorias(15)
        self.assertEqual(mochila_memoizacao(itens, 60)[0], mochila_tabulacao(itens, 60)[0])
        self.assertEqual(mochila_sem_memoizacao(itens, 60), mochila_tabulacao(itens, 60)[0])


class TestOrcamento(unittest.TestCase):
    # Exemplo clássico: capacidade 50 -> escolhe itens 2 e 3 = 220 (e não o 1º+2º = 160).
    CLASSICO = [
        {"nome": "a", "custo": 10, "beneficio": 60},
        {"nome": "b", "custo": 20, "beneficio": 100},
        {"nome": "c", "custo": 30, "beneficio": 120},
    ]

    def test_mochila_classica(self):
        ben_tab, esc_tab = mochila_tabulacao(self.CLASSICO, 50)
        ben_memo, esc_memo = mochila_memoizacao(self.CLASSICO, 50)
        self.assertEqual(ben_tab, 220)
        self.assertEqual(ben_memo, 220)
        self.assertEqual(mochila_sem_memoizacao(self.CLASSICO, 50), 220)
        self.assertEqual([m["nome"] for m in esc_tab], ["b", "c"])
        self.assertEqual(sorted(m["nome"] for m in esc_memo), ["b", "c"])

    def test_orcamento_zero_e_insuficiente(self):
        self.assertEqual(mochila_tabulacao(self.CLASSICO, 0), (0, []))
        self.assertEqual(mochila_tabulacao(self.CLASSICO, 9), (0, []))

    def test_orcamento_negativo_e_recusado(self):
        for funcao in (mochila_tabulacao, mochila_memoizacao, mochila_sem_memoizacao):
            with self.assertRaises(ValueError):
                funcao(self.CLASSICO, -5)

    def test_limite_de_trechos_negativo_e_recusado(self):
        with self.assertRaises(ValueError):
            menor_custo_com_limite(grafo_pequeno(), "A", "C", "rapida", -1)

    def test_forca_bruta_confere_com_dados_reais(self):
        """Testa TODOS os subconjuntos e compara com a mochila."""
        dados = carregar_dados()
        melhorias = dados["melhorias"]
        for orcamento in (0, 10, 25, 50, 200):
            melhor = 0
            for r in range(len(melhorias) + 1):
                for combo in itertools.combinations(melhorias, r):
                    if sum(m["custo"] for m in combo) <= orcamento:
                        melhor = max(melhor, sum(m["beneficio"] for m in combo))
            self.assertEqual(mochila_tabulacao(melhorias, orcamento)[0], melhor)
            self.assertEqual(mochila_memoizacao(melhorias, orcamento)[0], melhor)

    def test_escolhidas_cabem_no_orcamento(self):
        melhorias = carregar_dados()["melhorias"]
        beneficio, escolhidas = mochila_tabulacao(melhorias, 50)
        self.assertLessEqual(sum(m["custo"] for m in escolhidas), 50)
        self.assertEqual(sum(m["beneficio"] for m in escolhidas), beneficio)

    def test_melhoria_abre_rota_acessivel(self):
        dados = carregar_dados()
        grafo = montar_grafo(dados)
        rampa = [m for m in dados["melhorias"] if "Rampa na escadaria" in m["nome"]]
        antes, _ = melhor_rota(grafo, "Casa_Dona_Maria", "Escola", "acessivel")
        depois, caminho = melhor_rota(aplicar_melhorias(grafo, rampa),
                                      "Casa_Dona_Maria", "Escola", "acessivel")
        self.assertEqual(antes, 38)   # volta grande por Praca_14_Bis > Mercado
        self.assertEqual(depois, 22)  # 4 min + 3 * risco 6 pela escadaria com rampa
        self.assertEqual(caminho, ["Casa_Dona_Maria", "Escola"])
        # O grafo original não pode ser alterado.
        self.assertFalse(grafo.adj["Casa_Dona_Maria"]["Escola"].acessivel)


if __name__ == "__main__":
    unittest.main()
