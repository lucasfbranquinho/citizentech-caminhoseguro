# Progresso da GS — prazo 19/11/2026 23h55

Atualizado em: 05/11/2026

## Enunciados (04/11/2026)
- `enunciados/GS-CitizenTech-2ES-2026.pdf`: o enunciado COMPLETO, com as 7 disciplinas (já resumido nos REQUISITOS.md).
- `enunciados/GS-lancamento-motivacional-2026.pdf`: só os slides de lançamento (inspiração, exemplos, QR "CitizenTech Studio"). Sem regras novas. Não precisa reler.
- Falta só: critérios de nota do AR-VR (perguntar ao professor) e o número da equipe (Network).

## Decisões da equipe (pendente)
- [ ] Integrantes (nome + RM, ordem alfabética) e nome da equipe
- [ ] Número da equipe (X da rede 192.168.X.0/24 em Network)
- [ ] Problema escolhido + cidade/bairro + pessoa real entrevistada
- [ ] Nome da CitizenTech e frase do problema
- [ ] ODS conectados
- [ ] Repositório GitHub criado

## Disciplinas
| Disciplina | Responsável | Status | Próximo passo |
|---|---|---|---|
| 01 Agile | Vitor | não iniciado | depende da ideia |
| 02 AR-VR | Vitor | não iniciado | aguardando detalhes do professor |
| 03 Data Science | Lucas | não iniciado | achar base CSV pública ligada ao problema |
| 04 Database | Vitor | não iniciado | depende da ideia |
| 05 DDD Java | Vitor | não iniciado | depende do modelo de dados (04) |
| 06 Dynamic Programming | Lucas | feito no tema CaminhoSeguro/Bela Vista (dados simulados): 21 testes OK, `main.py` OK, `entrega-dp.zip` atualizado | só enviar o ZIP no Teams (um integrante) até 19/11 23h55; se a equipe trocar de tema/bairro, editar `dados/bairro.json`, regerar o ZIP e rodar `python -m unittest`. Estudar para a defesa: Dijkstra, Floyd-Warshall (tabulação), memoização em `menor_custo_com_limite`, mochila 0/1 (as duas versões), rota com parada, indicadores e por que a memoização reduz as chamadas |
| 07 Network | Lucas | feito com X=1 (confirmado): .pkt + PDF + 7 testes OK + segurança reforçada + Ficha preenchida (CaminhoSeguro, Bela Vista/SP) | só o link do GitHub na Ficha e o envio (ver "Network — detalhes") |

## Ordem sugerida (dependências)
Ideia/Ficha → 04 Database (modelo) → 05 DDD Java (usa as mesmas tabelas) → resto em paralelo.
Deploy no Render (05) vale 30 pts: não deixar para o último dia.

## Network — detalhes (atualizado em 05/11/2026)
- **Pronto:** `07-network/citizentech-rede.pkt` (rede montada, aba Physical organizada em 2 prédios com salas),
  `07-network/GS-Network-CitizenTech.pdf` (12 págs), prints em `07-network/prints/`, configs em `07-network/configs/x1/`.
- **Decisões tomadas pelo Claude a pedido do Lucas (05/11/2026):** tema **CaminhoSeguro** (calçadas acessíveis e rotas
  seguras), bairro **Bela Vista (São Paulo/SP)**, equipe **1**, persona fictícia dona Maria (72). Aplicado em `dados.json`,
  `index.html`, HTTP do Server-Solucao (`.pkt`), `teste3.png`, PDF, README da raiz e README do Dynamic Programming.
  Os outros integrantes/disciplinas devem usar o mesmo tema e bairro.
- **Falta:**
  1. Criar o repositório no GitHub e colar o link na Ficha (README da raiz e `dados.json`; no PDF fica em amarelo até lá).
     Se mudar a Ficha: editar `dados.json` e `index.html`, colar o HTML em Server-Solucao → Services → HTTP → index.html
     (Save → Yes), refazer o print do teste 3, salvar o `.pkt` e rodar `python gerar_pdf.py` na pasta `gerador-pdf`.
  2. A exigência de "pessoa real" do enunciado: conversar com alguém do bairro e trocar a persona fictícia.
  3. Um integrante envia `.pkt` + PDF no Teams/Portal até 19/11/2026 23h55.

