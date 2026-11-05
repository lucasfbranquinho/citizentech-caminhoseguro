# Divisão Lucas + Vitor

## DIVISÃO FINAL (combinada no WhatsApp, 04/11/2026 19h16) — vale esta
| Vitor | Lucas |
|---|---|
| 04 Database | 03 Data Science |
| 05 DDD Java | 06 Dynamic Programming |
| 01 Agile | 07 Network |
| 02 AR-VR | |

Os pares fortes ficaram juntos (Database+DDD e Agile+AR-VR, todos com o Vitor).
Lucas só depende de terceiros para: Ficha da CitizenTech (página do servidor no Network) e o tema/problema.
A proposta antiga abaixo ficou só como histórico.

---
# Proposta antiga (substituída)

## O que liga com o quê
| Ligação | Força | Por quê |
|---|---|---|
| 04 Database ↔ 05 DDD Java | **FORTE** | A API usa as mesmas tabelas no Oracle FIAP; o DER do Database entra no PDF do DDD. Mesma pessoa. |
| 01 Agile ↔ 02 AR-VR | **FORTE** | Os dois são vídeo no YouTube e contam a solução; o vídeo 3D do AR-VR pode entrar no pitch do Agile. Mesma pessoa. |
| 01 Agile → 05 DDD Java | média | As 3+ telas do protótipo do Agile servem como "protótipos de tela" do PDF do DDD. Agile entrega as telas, DDD reaproveita. |
| 01 Agile ↔ 04 Database | média | Casos de uso e backlog definem quais dados o banco guarda. Combinar escopo cedo. |
| 03 Data Science ↔ 06 Dynamic Programming | fraca | Os dois são Python e podem usar a mesma base CSV, mas não dependem um do outro. |
| 07 Network | independente | Só precisa da Ficha da CitizenTech (página HTTP do servidor) e do número da equipe. |

## Esforço estimado (1 = leve, 5 = pesado)
DDD Java 5 (deploy Render vale 30 pts) · Agile 4 · Database 3 · Data Science 3 · Network 3 · AR-VR 2 · DP 2

## Proposta
| Lucas (backend + algoritmo) | Vitor (produto + visual + dados) |
|---|---|
| 04 Database | 01 Agile |
| 05 DDD Java | 02 AR-VR |
| 06 Dynamic Programming | 03 Data Science |
| | 07 Network |
| Esforço ≈ 10 | Esforço ≈ 12 |

Motivo: Lucas já fez CP4/CP5 de DDD Java, a freelas-api em Spring Boot e o CP6 de DP, então é mais
rápido nessas. Vitor fica com os blocos de produto/vídeo, que precisam andar juntos.
Se o Vitor for melhor em Python, dá para trocar Data Science ↔ Dynamic Programming sem quebrar nada.

## Juntos, antes de dividir (dias 1–2)
Problema, cidadão, entrevista com uma pessoa real, Ficha da CitizenTech, ODS e escopo do MVP.
Sem isso nenhuma disciplina começa.

## Pontos de troca entre os dois
- Vitor → Lucas: telas do protótipo (Agile) para o PDF do DDD.
- Lucas → Vitor: DER/tabelas para o Agile ficar coerente; dados simulados do banco podem virar o CSV do Data Science.
- Os dois: README com a Ficha, prompts.md, e cada um sabendo explicar o projeto inteiro.
