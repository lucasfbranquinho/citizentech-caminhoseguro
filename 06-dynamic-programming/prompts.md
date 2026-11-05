# Registro de uso de IA — Dynamic Programming

IA usada como copiloto para aprender, escrever e revisar. Cada integrante sabe explicar o código.
(O registro completo da equipe, com as outras disciplinas, está no `prompts.md` do repositório.)

| Data | Ferramenta | Prompt (resumo) | Para que serviu |
|---|---|---|---|
| 05/11/2026 | Claude | Criar projeto Python de DP para a CitizenTech: grafo de bairro fictício com rota segura/acessível (Dijkstra, Floyd-Warshall em tabulação, memoização com limite de trechos), mochila 0/1 de orçamento (memoização e tabulação), main.py, testes e README | Primeira versão do código, dos dados simulados e dos testes |
| 05/11/2026 | Claude | Refazer e completar o projeto para nota máxima: reler o enunciado, adaptar ao tema CaminhoSeguro (Bela Vista), adicionar rota com parada, ponto de apoio ideal, indicadores antes/depois, menu, benchmarks de escalabilidade, 21 testes e README com Ficha, ODS e as seis perguntas | Versão final do código e do README |
| 05/11/2026 | Claude | Revisar o projeto e corrigir o que poderia custar nota (acentos nos dados, prompts.md no ZIP, diagrama, limitações) | Acabamento final |
| 05/11/2026 | Claude | Revisão final: testar os comandos do README e entradas inválidas | Orçamento e limite de trechos negativos passam a ser recusados (antes quebravam), menu sai sem erro no fim da entrada; 2 testes novos (23 no total) |
| 05/11/2026 | Claude | Terceira revisão: valores extremos e outro arquivo de dados | Limite de trechos e orçamento enormes ajustados ao máximo útil (antes estouravam), --parada sem --rota avisa, arquivo de dados ausente ou inválido dá mensagem clara, exemplos não quebram com outro bairro |
