# Registro de uso de IA (exigido pela GS)

IA usada como copiloto para aprender e revisar. Cada integrante sabe explicar o que foi gerado.

| Data | Disciplina | Ferramenta | Prompt (resumo) | Para que serviu |
|---|---|---|---|---|
| 04/11/2026 | Geral | Claude | Resumir o enunciado da GS e organizar as pastas por disciplina | Organização do projeto |
| 04/11/2026 | 07 Network | Claude | Planejar a rede (VLANs, endereçamento 192.168.X.0/24, DHCP, NAT, ACL, SSH) e escrever os configs de SW1, R1 e ISP | `07-network/PLANO.md` e `07-network/configs/` |
| 05/11/2026 | 07 Network | Claude (Computer use) | Montar no Packet Tracer a rede do PLANO, colar os configs, configurar AP, Wi-Fi, DNS e HTTP, rodar os 7 testes e salvar prints | `citizentech-rede.pkt` e `07-network/prints/` |
| 05/11/2026 | 03 Data Science | Claude | Gerar base simulada de segmentos de calçada da Bela Vista (seed fixa, valores faltantes, parâmetros inspirados na NBR 9050) e montar notebook com Pipeline sem vazamento, regressão linear, regressão logística, gráficos e recomendações com limitações | `03-data-science/` (`gerar_base.py`, CSV, notebook executado, `integrantes.txt`) e `entrega-data-science.zip` |
| 05/11/2026 | 07 Network | Claude | Revisar a rede contra o enunciado e organizar a aba Physical (prédios e salas) | Correções e acabamento do `.pkt` |
| 05/11/2026 | 07 Network | Claude | Gerar o PDF de entrega (Ficha, topologia, endereçamento, trechos de config, prints) | `07-network/gerador-pdf/` e `GS-Network-CitizenTech.pdf` |
| 05/11/2026 | 06 Dynamic Programming | Claude | Criar projeto Python de DP para a CitizenTech: grafo de bairro fictício com rota segura/acessível (Dijkstra, Floyd-Warshall em tabulação, memoização com limite de trechos), mochila 0/1 de orçamento (memoização e tabulação), main.py, testes e README | `06-dynamic-programming/` (código, dados simulados, 12 testes, README e `entrega-dp.zip`) |
| 05/11/2026 | 06 Dynamic Programming | Claude | Refazer e completar o projeto de DP para tirar nota máxima: reler o enunciado, adaptar ao tema CaminhoSeguro (Bela Vista), adicionar rota com parada, ponto de apoio ideal, indicadores antes/depois, menu, benchmarks de escalabilidade, 21 testes e README com Ficha, ODS e as seis perguntas | `06-dynamic-programming/` e `entrega-dp.zip` atualizados |
| 05/11/2026 | 07 Network | Claude (Computer use) | Escrever uma Ficha provisória (CaminhoSeguro), publicar no HTTP do Server-Solucao, refazer o print do teste 3 e regerar o PDF | `index.html`, `dados.json`, `teste3.png`, `.pkt` e PDF atualizados |
| 05/11/2026 | 03, 06 e 07 (revisão) | Claude | Revisar as três entregas contra o enunciado e corrigir o que faltava | Network: nome na Ficha do PDF e trechos de config sem comandos de execução; Data Science: limiar escolhido por validação cruzada no treino (sem olhar o teste), frase sobre as rampas do DP corrigida e `FONTE_DOS_DADOS.txt` no ZIP |
| 05/11/2026 | 03, 06 e 07 (2ª revisão) | Claude | Revisar de novo até não achar erro: testar comandos e entradas inválidas, conferir prints e textos | DP: orçamento e limite negativos recusados (antes quebravam), 23 testes; Network: prints dos testes 1 e 7 recortados para tirar comandos digitados errado; Data Science: duas frases imprecisas corrigidas |
| 05/11/2026 | 03, 06 e 07 (3ª revisão) | Claude | Revisar de novo até não achar erro: ler todo o código do DP, testar valores extremos e outro arquivo de dados; equipe 1 nas entregas | DP: valores enormes ajustados ao máximo útil, mensagens claras para arquivo de dados inválido e --parada sem --rota, exemplos não quebram com outro bairro; DS: gerador salva ao lado do script; número da equipe (1) no README, no DP e no Data Science |

Observação: os testes e prints da Network foram executados e conferidos no Packet Tracer (não são texto gerado).
