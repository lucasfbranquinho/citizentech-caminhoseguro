"""
Gera a base SIMULADA trechos_bela_vista.csv (CaminhoSeguro, Bela Vista, São Paulo/SP).

- Seed fixa (SEED = 2026): rodar de novo gera exatamente o mesmo arquivo.
- Nenhum dado pessoal e nenhuma medição real: tudo é inventado por regras simples.
- Os 20 trechos entre locais vêm do mesmo bairro.json da matéria de Dynamic Programming
  (cópia dos números de "risco" e "acessivel" embutida abaixo, para o script rodar sozinho).
- Os limites de largura e declividade se inspiram na NBR 9050 (acessibilidade em calçadas):
  faixa livre mínima de 1,20 m e inclinação longitudinal até 8,33% (rampa 1:12).

Como rodar:  python gerar_base.py
"""
import numpy as np
import pandas as pd

SEED = 2026
SEGMENTOS_POR_TRECHO = 30          # 20 trechos x 30 = 600 linhas
rng = np.random.default_rng(SEED)

# (local_a, local_b, risco 1-10, acessivel) -> mesmos valores do bairro.json (06-dynamic-programming)
TRECHOS = [
    ("Casa_Dona_Maria", "Praca_14_Bis", 2, True),
    ("Casa_Dona_Maria", "Escola", 6, False),
    ("Casa_Dona_Maria", "Viaduto", 8, True),
    ("Praca_14_Bis", "Posto_de_Saude", 1, True),
    ("Praca_14_Bis", "Mercado", 2, True),
    ("Praca_14_Bis", "Biblioteca", 3, True),
    ("Escola", "Mercado", 4, True),
    ("Escola", "Metro_Brigadeiro", 5, False),
    ("Viaduto", "Metro_Brigadeiro", 7, True),
    ("Mercado", "Metro_Brigadeiro", 3, True),
    ("Mercado", "Ponto_de_Apoio", 1, True),
    ("Posto_de_Saude", "Ponto_de_Apoio", 1, True),
    ("Biblioteca", "Centro_Comunitario", 2, True),
    ("Ponto_de_Apoio", "Centro_Comunitario", 2, True),
    ("Posto_de_Saude", "Centro_Comunitario", 6, False),
    ("Metro_Brigadeiro", "Centro_Comunitario", 2, True),
    ("FIAP_Paulista", "Metro_Brigadeiro", 2, True),
    ("FIAP_Paulista", "Biblioteca", 3, True),
    ("FIAP_Paulista", "Farmacia", 1, True),
    ("Farmacia", "Mercado", 2, True),
]

# distância média do trecho até a UBS (Posto_de_Saude), em metros (inventada)
DIST_UBS_BASE = [450, 520, 700, 150, 380, 330, 560, 900, 1100, 640,
                 300, 180, 520, 420, 250, 800, 1000, 760, 880, 700]


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


linhas = []
for i, ((a, b, risco, acessivel), dist_base) in enumerate(zip(TRECHOS, DIST_UBS_BASE)):
    n = SEGMENTOS_POR_TRECHO
    ruim = 0 if acessivel else 1                       # trechos inacessíveis são piores em tudo
    ped_base = rng.uniform(80, 350)                    # fluxo de pedestres típico do trecho

    # --- características físicas do segmento (ruído por segmento) ---
    declividade = np.abs(rng.normal(2.0 + 0.6 * risco + 3.0 * ruim, 2.0, n))
    largura = np.clip(rng.normal(1.95 - 0.08 * risco - 0.30 * ruim, 0.40, n), 0.6, 3.5)
    escore_piso = rng.normal(0.4 * risco - 0.3 + 0.8 * ruim, 1.0, n)
    piso = np.where(escore_piso < 1.2, "bom", np.where(escore_piso < 2.6, "regular", "ruim"))
    rampa = rng.random(n) < np.clip(0.92 - 0.08 * risco - 0.30 * ruim, 0.05, 0.95)
    iluminacao = np.clip(np.round(rng.normal(4.4 - 0.30 * risco, 0.8, n)), 1, 5)
    fluxo_veic = rng.gamma(4.0, (60 + 25 * risco) / 4.0, n)          # veículos por hora
    fluxo_ped = rng.gamma(5.0, ped_base / 5.0, n)                     # pedestres por hora
    dist_ubs = np.clip(rng.normal(dist_base, 110, n), 40, None)       # metros
    semaforo = rng.random(n) < 0.40
    obstaculos = rng.random(n) < np.clip(0.08 + 0.04 * risco, 0, 0.6)  # poste, ambulante, entulho

    # alguns erros de medição / pontos extremos (ladeiras muito íngremes)
    extremos = rng.random(n) < 0.015
    declividade = np.where(extremos, declividade * 2.2, declividade)

    p_ruim = (piso == "ruim").astype(float)
    p_reg = (piso == "regular").astype(float)

    # --- alvo numérico: ocorrências registradas pela comunidade por mês ---
    # Inclui um viés de notificação: onde passa mais gente, mais gente registra.
    log_lambda = (-1.2 + 0.10 * declividade + 0.90 * p_ruim + 0.40 * p_reg
                  + 0.55 * (~rampa) + 0.55 * obstaculos - 0.25 * (largura - 1.5)
                  - 0.20 * (iluminacao - 3) + 0.0015 * fluxo_veic + 0.0030 * fluxo_ped
                  + rng.normal(0, 0.30, n))
    ocorrencias = np.minimum(rng.poisson(np.exp(log_lambda)), 20)   # teto de 20 registros/mês por segmento

    # --- alvo binário: segmento inacessível para cadeira de rodas (vistoria simulada) ---
    z = (-3.4 + 0.30 * (declividade - 5) + 2.2 * (largura < 1.2) + 1.1 * p_ruim + 0.5 * p_reg
         + 1.7 * (~rampa) + 1.0 * obstaculos + rng.normal(0, 0.9, n))
    inacessivel = (rng.random(n) < sigmoide(z)).astype(int)

    for k in range(n):
        linhas.append({
            "id_segmento": f"T{i + 1:02d}-S{k + 1:02d}",
            "local_inicio": a, "local_fim": b,
            "declividade_pct": round(float(declividade[k]), 1),
            "largura_calcada_m": round(float(largura[k]), 2),
            "estado_piso": piso[k],
            "rampa_esquina": int(rampa[k]),
            "iluminacao_nota": int(iluminacao[k]),
            "fluxo_veiculos_h": int(round(fluxo_veic[k])),
            "fluxo_pedestres_h": int(round(fluxo_ped[k])),
            "dist_ubs_m": int(round(dist_ubs[k])),
            "semaforo_pedestres": int(semaforo[k]),
            "obstaculos_calcada": int(obstaculos[k]),
            "ocorrencias_mes": int(ocorrencias[k]),
            "inacessivel_cadeira": int(inacessivel[k]),
        })

df = pd.DataFrame(linhas)

# --- valores faltantes (sensor/vistoria que não preencheu), em posições sorteadas ---
faltas = {"declividade_pct": 0.06, "largura_calcada_m": 0.05, "estado_piso": 0.04,
          "rampa_esquina": 0.03, "iluminacao_nota": 0.05, "dist_ubs_m": 0.03,
          "fluxo_veiculos_h": 0.04}
for col, frac in faltas.items():
    idx = rng.choice(df.index, size=int(frac * len(df)), replace=False)
    df[col] = df[col].astype(object)
    df.loc[idx, col] = np.nan

df.to_csv("trechos_bela_vista.csv", index=False, encoding="utf-8")
print(f"Gerado trechos_bela_vista.csv com {len(df)} linhas e {df.shape[1]} colunas")
print(f"% inacessível: {df['inacessivel_cadeira'].mean():.1%} | ocorrências/mês médias: {df['ocorrencias_mes'].mean():.2f}")
