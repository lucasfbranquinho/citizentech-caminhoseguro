# Network Architect Solutions

Rede no **Packet Tracer** do local físico da solução (posto, escola, cooperativa ou base comunitária),
com setores isolados, Wi-Fi público e saída para a internet.

## Requisitos mínimos
- **Endereçamento/VLANs**: faixa 192.168.X.0/24 (X = número da equipe) dividida em pelo menos 3
  sub-redes: Equipe, Cidadão (Wi-Fi público), Servidores/Sensores. Uma VLAN por setor, trunk 802.1Q,
  router-on-a-stick.
- **Serviços**: DHCP com um pool por VLAN (excluindo gateway e servidor). NAT/PAT até um roteador
  provedor com servidor externo simulando a internet. Servidor da solução com DNS e HTTP (página com
  a Ficha da CitizenTech).
- **Segurança**: ACL estendida — Wi-Fi do cidadão acessa só HTTP e DNS do servidor e a internet,
  nada da VLAN Equipe. Roteador só por SSH, com senhas e enable secret. Wi-Fi com WPA2.
- **Testes no PDF (prints)**: ping entre VLANs, PC recebendo IP por DHCP, página abrindo pelo nome,
  `show ip nat translations` e um acesso barrado pela ACL.

## Entregáveis
`.pkt` + PDF com Ficha da CitizenTech, topologia, plano de endereçamento, trechos de
`show running-config` e prints dos testes. Um envio por equipe, Teams ou Portal até 19/11 23h55.

## Nota (0–10)
Arquitetura e endereçamento 3; configuração 3; segurança 2; testes 2.
