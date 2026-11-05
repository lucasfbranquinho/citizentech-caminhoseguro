# CaminhoSeguro

## Ficha da CitizenTech
| Campo | Resposta |
|---|---|
| Nome da CitizenTech | CaminhoSeguro |
| Cidade e bairro | São Paulo/SP, bairro Bela Vista (perto do campus FIAP Paulista) |
| Cidadão beneficiado | Pessoas com mobilidade reduzida e idosos que moram ou circulam na Bela Vista. Personagem: dona Maria, 72 anos, que mora na Bela Vista e quer ir sozinha à UBS e ao mercado (personagem fictícia, sem dados pessoais reais) |
| Problema, em uma frase | Calçadas irregulares, ladeiras e travessias de risco fazem moradores com mobilidade reduzida desistirem de sair de casa ou correrem risco no caminho. |
| Como funciona | O morador pede uma rota entre dois pontos do bairro e recebe o caminho mais rápido, o mais seguro ou o mais acessível. Os trechos problemáticos são registrados pela comunidade e entram no cálculo das rotas (dados simulados nesta fase). |
| O que cada parte faz | Agile: organiza a equipe e o pitch / AR-VR: simula a rota e as barreiras da calçada / Data Science: analisa as ocorrências por trecho / Database: guarda locais, trechos e ocorrências / DDD Java: API de rotas e ocorrências no Render / Dynamic Programming: calcula as rotas (Dijkstra, Floyd-Warshall) e as melhorias com orçamento (mochila) / Network: conecta equipe, Wi-Fi público e servidor com VLANs, NAT, ACL e SSH |
| Link do repositório | https://github.com/lucasfbranquinho/citizentech-caminhoseguro |
| Indicador de impacto | Percentual de trechos do bairro acessíveis e número de rotas acessíveis consultadas por semana |
| ODS conectados | 11 (cidades e comunidades sustentáveis), 10 (redução das desigualdades), 3 (saúde e bem-estar) |

## As seis perguntas do briefing
| Pergunta | Resposta |
|---|---|
| 1. Quem é o cidadão beneficiado? | Pessoas com mobilidade reduzida e idosos da Bela Vista (personagem: dona Maria, 72 anos, fictícia) |
| 2. Qual problema será resolvido? | Calçadas irregulares, ladeiras e travessias de risco fazem esses moradores desistirem de sair de casa |
| 3. Como a solução funcionará? | O morador pede uma rota e recebe o caminho mais rápido, o mais seguro ou o mais acessível; a comunidade registra os trechos problemáticos |
| 4. Quais tecnologias serão empregadas? | Python (grafos, Dijkstra, Floyd-Warshall, programação dinâmica), banco de dados relacional, API em Java (DDD) no Render, análise de dados em notebook, simulação AR-VR e rede segmentada no Packet Tracer (VLANs, NAT, ACL, SSH, Wi-Fi WPA2) |
| 5. Quem participará do ecossistema? | Moradores e idosos (usuários), a comunidade que registra ocorrências, a UBS e o Centro Comunitário (pontos de apoio e Wi-Fi público), a subprefeitura (responsável por calçadas e rampas) e a equipe de desenvolvimento |
| 6. Como o impacto será medido e ampliado? | % de trechos acessíveis e rotas acessíveis consultadas por semana; ampliar para outros bairros trocando só os dados dos locais e trechos |

## Integrantes
| Nome | RM |
|---|---|
| Lucas Branquinho | 562262 |
| Vitor Bordalo | 561592 |

## Estrutura
Uma pasta por disciplina (01-agile … 07-network). Prompts de IA usados: `prompts.md`.
