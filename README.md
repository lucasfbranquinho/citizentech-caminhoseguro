# CaminhoSeguro

## Ficha da CitizenTech
| Campo | Resposta |
|---|---|
| Nome da CitizenTech | CaminhoSeguro |
| Cidade e bairro | São Paulo/SP, bairro Bela Vista (perto do campus FIAP Paulista) |
| Cidadão beneficiado | Pessoas com mobilidade reduzida e idosos que moram ou circulam na Bela Vista. Persona de exemplo: dona Maria, 72 anos (fictícia nesta entrega) |
| Problema, em uma frase | Calçadas irregulares, ladeiras e travessias de risco fazem moradores com mobilidade reduzida desistirem de sair de casa ou correrem risco no caminho. |
| Como funciona | O morador pede uma rota entre dois pontos do bairro e recebe o caminho mais rápido, o mais seguro ou o mais acessível. Os trechos problemáticos são registrados pela comunidade e entram no cálculo das rotas (dados simulados nesta fase). |
| O que cada parte faz | Agile: organiza a equipe e o pitch / AR-VR: simula a rota e as barreiras da calçada / Data Science: analisa as ocorrências por trecho / Database: guarda locais, trechos e ocorrências / DDD Java: API de rotas e ocorrências no Render / Dynamic Programming: calcula as rotas (Dijkstra, Floyd-Warshall) e as melhorias com orçamento (mochila) / Network: conecta equipe, Wi-Fi público e servidor com VLANs, NAT, ACL e SSH |
| Link do repositório | [criar o repositório e colar aqui] |
| Indicador de impacto | Percentual de trechos do bairro acessíveis e número de rotas acessíveis consultadas por semana |
| ODS conectados | 11 (cidades e comunidades sustentáveis), 10 (redução das desigualdades), 3 (saúde e bem-estar) |

## Integrantes
| Nome | RM |
|---|---|
| Lucas Branquinho | 562262 |
| Vitor Bordalo | 561592 |

## Estrutura
Uma pasta por disciplina (01-agile … 07-network). Prompts de IA usados: `prompts.md`.
