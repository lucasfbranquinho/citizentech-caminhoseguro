# Network — plano da rede (Lucas)

> **Estado (05/11/2026):** rede montada e testada no Packet Tracer com **X = 1 (confirmado pela equipe)**
> (`citizentech-rede.pkt`, prints em `prints/`, PDF em `GS-Network-CitizenTech.pdf`).
> Segurança reforçada: SSH só da VLAN Equipe (access-class), SW1 com senhas/SSH/IP de gerência .131 e portas sem uso desligadas.
> Ficha "CaminhoSeguro" (Bela Vista/SP) publicada no .pkt e no PDF (05/11/2026); pendente só o link do GitHub.
> `configs/*.txt` usam `X` literal (originais); `configs/x1/` são as cópias já com X = 1.

## Mapa da pasta
| Item | O que é |
|---|---|
| `citizentech-rede.pkt` + `GS-Network-CitizenTech.pdf` | **Os dois arquivos da entrega** |
| `PLANO.md`, `REQUISITOS.md` | Plano da rede e resumo do enunciado |
| `configs/` e `configs/x1/` | Configs de SW1, R1 e ISP (com `X` e com X = 1) |
| `index.html` | Página da Ficha publicada no HTTP do Server-Solucao |
| `prints/` | `topologia`, `teste1`…`teste7` (+ `teste2b-laptop`, `teste6b-acl`) e `fisico-*` |
| `gerador-pdf/` | `dados.json` (nº da equipe e Ficha) e `gerar_pdf.py` que monta o PDF |

## Dicas de montagem (aprendidas na prática)
- Ao ligar cabos no Packet Tracer, a lista de portas **só mostra as livres**: confira a porta escolhida
  (`show interfaces status` / `show vlan brief`) antes de seguir.
- Colar `R1.txt`, `ISP.txt` e `SW1.txt` em **duas partes**: até `crypto key generate rsa`, digitar `1024`, e então o resto (no SW1 a chave está no meio do arquivo).
- Reabrir o `.pkt` reinicia os roteadores com a startup-config: o console pede a senha (`Gs2026@con`).
- Se um dispositivo ficar sem IP depois de mexer em cabos, rodar `ipconfig /renew` nele.

## Se o número da equipe (X) mudar
Trocar `192.168.1.` pelo novo prefixo em R1/SW1/ISP, no IP, gateway e DNS do Server-Solucao, nos registros A do DNS
e refazer os prints; depois ajustar `equipe_numero` em `gerador-pdf/dados.json` e rodar `python gerar_pdf.py`.

## Topologia (dispositivos)
| Dispositivo | Modelo PT | Liga em |
|---|---|---|
| R1 (roteador da solução) | 2911 | G0/0 → SW1 G0/1 (trunk) · G0/1 → ISP G0/0 |
| ISP (provedor) | 2911 | G0/0 → R1 G0/1 · G0/1 → Server-Internet |
| SW1 | 2960-24TT | Fa0/1–2 PCs Equipe · Fa0/3 AP · Fa0/4 Server-Solucao · G0/1 → R1 |
| PC-Equipe1, PC-Equipe2 | PC-PT | SW1 Fa0/1, Fa0/2 (VLAN 10, DHCP) |
| AP-Cidadao | AccessPoint-PT | SW1 Fa0/3 (VLAN 20) — SSID `CitizenTech-Publico`, WPA2-PSK |
| Laptop-Cidadao | Laptop-PT + placa WPC300N | Wi-Fi do AP (DHCP) |
| Server-Solucao | Server-PT | SW1 Fa0/4 (VLAN 30, IP fixo) — DNS + HTTP |
| Server-Internet | Server-PT | ISP G0/1 — HTTP (simula a internet) |

Cabos: cobre direto (straight) em tudo; R1↔ISP também direto (2911 faz auto-MDIX).

## Plano de endereçamento — 192.168.X.0/24 dividida em 4 sub-redes /26
| VLAN | Setor | Rede | Gateway (R1) | Faixa DHCP | Broadcast |
|---|---|---|---|---|---|
| 10 | EQUIPE | 192.168.X.0/26 | 192.168.X.1 | .6 – .62 | .63 |
| 20 | CIDADAO (Wi-Fi público) | 192.168.X.64/26 | 192.168.X.65 | .70 – .126 | .127 |
| 30 | SERVIDORES/SENSORES | 192.168.X.128/26 | 192.168.X.129 | .136 – .190 | .191 |
| — | reserva (crescimento) | 192.168.X.192/26 | — | — | .255 |

| Link / host | Endereço |
|---|---|
| R1 G0/1 ↔ ISP G0/0 | 200.0.0.1/30 ↔ 200.0.0.2/30 |
| ISP G0/1 (rede "internet") | 8.8.8.1/24 |
| Server-Internet | 8.8.8.8/24, gw 8.8.8.1 |
| Server-Solucao | 192.168.X.130/26, gw 192.168.X.129, DNS 192.168.X.130 |

Excluídos do DHCP: .1–.5, .65–.69, .129–.135 (gateways e servidor).

## Segurança
- ACL estendida `CIDADAO-IN` na entrada de G0/0.20: Wi-Fi do cidadão só acessa DNS (53) e HTTP (80) do
  Server-Solucao e a internet; bloqueia VLAN Equipe e o resto da VLAN Servidores.
- R1 e ISP só por SSH v2 (`line vty` com `transport input ssh`), `enable secret`, `service password-encryption`.
- Senhas de laboratório (só Packet Tracer): usuário `admin` / `Gs2026@ssh`; enable secret `Gs2026@en`;
  console `Gs2026@con`; Wi-Fi WPA2 `CitizenTech2026`.

## Passo a passo no Packet Tracer
1. Colocar os dispositivos e cabos da tabela de topologia.
2. Laptop: desligar → arrastar o módulo de rede cabeada para fora → colocar **WPC300N** → ligar.
3. **SW1**: CLI → colar `configs/SW1.txt`.
4. **R1**: CLI → colar `configs/R1.txt` (a geração de chave RSA leva alguns segundos).
5. **ISP**: CLI → colar `configs/ISP.txt`.
6. **AP-Cidadao** → Config → Port 1: SSID `CitizenTech-Publico`, WPA2-PSK, senha `CitizenTech2026`.
7. **Laptop** → Config → Wireless0: mesmo SSID, WPA2-PSK, mesma senha → IP config em DHCP.
8. **PCs Equipe** → Desktop → IP Configuration → DHCP.
9. **Server-Solucao** → Desktop → IP fixo (tabela acima). Services:
   - DNS: ligar; registros A `citizentech.local` → 192.168.X.130 e `internet.com` → 8.8.8.8.
   - HTTP: ligar; editar `index.html` com a Ficha da CitizenTech (quando o tema sair).
10. **Server-Internet** → IP 8.8.8.8/24, gw 8.8.8.1 → Services → HTTP ligado.
11. Salvar como `07-network/citizentech-rede.pkt`.

## Testes (tirar print de cada um para o PDF)
| # | Teste | Onde | Esperado |
|---|---|---|---|
| 1 | Ping entre VLANs | PC-Equipe1 → `ping 192.168.X.130` | responde (VLAN10 → VLAN30) |
| 2 | DHCP | PC-Equipe1 e Laptop → `ipconfig` | IP da faixa certa, gw e DNS .130 |
| 3 | Página pelo nome | Laptop → Web Browser → `http://citizentech.local` | abre a Ficha |
| 4 | Internet | Laptop → Web Browser → `http://internet.com` | abre a página do Server-Internet |
| 5 | NAT | R1 → `show ip nat translations` (logo após o teste 4) | traduções 192.168.X.x → 200.0.0.1 |
| 6 | ACL barrando | Laptop → `ping 192.168.X.6` (PC Equipe) | falha; R1 `show access-lists` mostra os matches |
| 7 | SSH | PC-Equipe1 → `ssh -l admin 192.168.X.1` | pede senha e entra; telnet é recusado |

## Para o PDF (entrega: .pkt + PDF)
Ficha da CitizenTech · print da topologia · tabela de endereçamento (acima) · trechos de
`show running-config` (subinterfaces, DHCP, NAT, ACL, SSH) · prints dos testes 1–7.
Nota: arquitetura/endereçamento 3 · configuração 3 · segurança 2 · testes 2.
