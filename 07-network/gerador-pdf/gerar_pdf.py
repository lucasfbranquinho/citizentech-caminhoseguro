"""Gera o PDF de entrega da disciplina Network (CitizenTech).

Uso (dentro desta pasta):  python gerar_pdf.py

Lê `dados.json` (número da equipe e Ficha), os configs de `../configs/x1` e os prints de
`../prints`, monta um HTML temporário e converte para PDF com o Chrome (ou Edge) em modo
headless. O resultado é `../GS-Network-CitizenTech.pdf`. Nenhum arquivo intermediário fica
no projeto.
"""
import base64
import html
import json
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
PRINTS = RAIZ / "prints"
CONFIGS = RAIZ / "configs" / "x1"
SAIDA_PDF = RAIZ / "GS-Network-CitizenTech.pdf"
EQUIPE_DOS_PRINTS = 1  # os prints e o .pkt foram feitos com X = 1

NAVEGADORES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
)
NAVEGADOR = next((p for p in NAVEGADORES if Path(p).exists()), None)

dados = json.loads((AQUI / "dados.json").read_text(encoding="utf-8"))
X = dados["equipe_numero"]
BASE = f"192.168.{X}"
ficha = dados["ficha"]
pendentes = []


def esc(texto):
    return html.escape(str(texto))


def campo(valor, nome):
    """Mostra o valor; se ainda for placeholder (começa com '['), destaca e anota como pendente."""
    if str(valor).strip().startswith("["):
        pendentes.append(nome)
        return f'<span class="pend">{esc(valor)}</span>'
    return esc(valor)


def img(nome, legenda):
    b64 = base64.b64encode((PRINTS / nome).read_bytes()).decode()
    return (f'<figure><img src="data:image/png;base64,{b64}" alt="{esc(legenda)}">'
            f"<figcaption>{esc(legenda)}</figcaption></figure>")


def trecho(arquivo, primeira, ultima, titulo, deve_comecar_com):
    """Linhas `primeira`..`ultima` (1-based) de um config. Confere a primeira linha para
    avisar se o arquivo mudou e os números ficaram desatualizados."""
    linhas = (CONFIGS / arquivo).read_text(encoding="utf-8").splitlines()
    recorte = linhas[primeira - 1:ultima]
    if not recorte or not recorte[0].strip().startswith(deve_comecar_com):
        sys.exit(f"{arquivo}: a linha {primeira} não começa com '{deve_comecar_com}'. "
                 "Atualize os números do trecho em gerar_pdf.py.")
    return f"<h4>{esc(titulo)}</h4><pre>{esc(chr(10).join(recorte))}</pre>"


integrantes = "".join(
    f"<li>{esc(i['nome'])} – RM {esc(i['rm'])}</li>" for i in dados["integrantes"])
definido = dados["equipe_numero_definido"]
aviso_equipe = "" if definido else (
    f'<p class="aviso">Número da equipe ainda não definido: usado X = {X} provisoriamente '
    f"(rede {BASE}.0/24).</p>")

CSS = """
@page { size: A4; margin: 16mm 15mm; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 11pt; color: #111; line-height: 1.4; }
h1 { font-size: 24pt; margin: 0 0 6px; color: #0b3d6e; }
h2 { font-size: 16pt; color: #0b3d6e; border-bottom: 2px solid #0b3d6e; padding-bottom: 3px; margin-top: 0; }
h3 { font-size: 12.5pt; color: #0b3d6e; margin: 14px 0 4px; }
h4 { font-size: 11pt; margin: 12px 0 3px; break-after: avoid; }
section { page-break-before: always; }
section.capa { page-break-before: auto; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 10.5pt; }
th, td { border: 1px solid #555; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #e4ecf5; }
pre { background: #f3f3f3; border: 1px solid #ccc; padding: 5px 8px; font-size: 8.3pt;
      line-height: 1.22; white-space: pre-wrap; margin: 2px 0 5px; break-inside: avoid; }
figure { margin: 8px 0 12px; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; }
figcaption { font-size: 9.5pt; color: #333; margin-top: 3px; }
.pend { background: #fff3a0; padding: 0 3px; }
.aviso { background: #fff3a0; border: 1px solid #c9b200; padding: 6px 9px; }
.ok { color: #0a6b2d; font-weight: bold; }
.capa { text-align: center; padding-top: 70px; }
.capa h1 { font-size: 28pt; }
.capa ul { list-style: none; padding: 0; font-size: 13pt; }
.duas { display: flex; gap: 10px; } .duas figure { flex: 1; }
.grade { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 14px; }
.cel { break-inside: avoid; }
.cel h3 { margin: 6px 0 2px; font-size: 11.5pt; }
.cel p { margin: 2px 0 4px; font-size: 9.8pt; }
.cel figure { margin: 3px 0 8px; }
"""

corpo = f"""
<section class="capa">
  <p>FIAP – Global Solution 2026.2 – Engenharia de Software – Turma {esc(dados['turma'])}</p>
  <h1>Network Architect Solutions</h1>
  <h2 style="border:none">CitizenTech: {campo(ficha['nome_citizentech'], 'Nome da CitizenTech')}</h2>
  <p>Rede do local físico da solução no Cisco Packet Tracer 9.0</p>
  <h3>Integrantes</h3>
  <ul>{integrantes}</ul>
  <p>Equipe número {X}{'' if definido else ' (provisório)'}</p>
  {aviso_equipe}
  <p style="margin-top:50px">Arquivo da rede: <b>citizentech-rede.pkt</b></p>
</section>

<section>
  <h2>1. Ficha da CitizenTech</h2>
  <table>
    <tr><th style="width:30%">Cidade e bairro</th><td>{campo(ficha['cidade_bairro'], 'Cidade e bairro')}</td></tr>
    <tr><th>Cidadão beneficiado</th><td>{campo(ficha['cidadao_beneficiado'], 'Cidadão beneficiado')}</td></tr>
    <tr><th>Problema, em uma frase</th><td>{campo(ficha['problema'], 'Problema')}</td></tr>
    <tr><th>Como funciona</th><td>{campo(ficha['como_funciona'], 'Como funciona')}</td></tr>
    <tr><th>O que cada parte faz</th><td><b>Network (esta entrega):</b> conecta a equipe, o Wi-Fi público do
      cidadão e o servidor da solução, com setores isolados por VLAN, saída para a internet e segurança
      por ACL, SSH e WPA2. {campo(ficha['demais_partes'], 'Demais partes')}</td></tr>
    <tr><th>Repositório</th><td>{campo(ficha['repositorio'], 'Repositório')}</td></tr>
    <tr><th>Indicador de impacto</th><td>{campo(ficha['indicador'], 'Indicador de impacto')}</td></tr>
    <tr><th>ODS conectados</th><td>{campo(ficha['ods'], 'ODS')}</td></tr>
  </table>
  <p>Esta mesma Ficha fica publicada na página HTTP do Server-Solucao
     (<code>http://citizentech.local</code>), como pede o enunciado.</p>
</section>

<section>
  <h2>2. Topologia</h2>
  {img('topologia.png', 'Topologia lógica no Packet Tracer: PCs da equipe e servidor da solução no SW1, AP do Wi-Fi público, R1 (router-on-a-stick, DHCP, NAT, ACL, SSH), ISP e servidor da internet simulada.')}
  <table>
    <tr><th>Dispositivo</th><th>Modelo</th><th>Liga em</th></tr>
    <tr><td>R1</td><td>Cisco 2911</td><td>G0/0 ↔ SW1 G0/1 (trunk); G0/1 ↔ ISP G0/0</td></tr>
    <tr><td>ISP</td><td>Cisco 2911</td><td>G0/0 ↔ R1 G0/1; G0/1 ↔ Server-Internet</td></tr>
    <tr><td>SW1</td><td>Catalyst 2960-24TT</td><td>Fa0/1–2 PCs da Equipe, Fa0/3 AP, Fa0/4 Server-Solucao, G0/1 ↔ R1</td></tr>
    <tr><td>PC-Equipe1, PC-Equipe2</td><td>PC-PT</td><td>SW1 Fa0/1 e Fa0/2 (VLAN 10, DHCP)</td></tr>
    <tr><td>AP-Cidadao</td><td>AccessPoint-PT</td><td>SW1 Fa0/3 (VLAN 20), SSID CitizenTech-Publico, WPA2-PSK</td></tr>
    <tr><td>Laptop-Cidadao</td><td>Laptop-PT + WPC300N</td><td>Wi-Fi do AP (DHCP)</td></tr>
    <tr><td>Server-Solucao</td><td>Server-PT</td><td>SW1 Fa0/4 (VLAN 30, IP fixo), DNS + HTTP</td></tr>
    <tr><td>Server-Internet</td><td>Server-PT</td><td>ISP G0/1, HTTP (simula a internet)</td></tr>
  </table>
</section>

<section>
  <h2>2.1 Organização física (aba Physical)</h2>
  <p>O local físico foi modelado em dois prédios: o <b>Centro Comunitário CitizenTech</b> (a base comunitária da Bela Vista, local físico da solução)
     (sala de rede com R1 e SW1, sala da equipe, sala de servidores e espaço do cidadão com o AP e o laptop) e o
     <b>Provedor ISP</b> (ISP e servidor da internet), ligados por um cabo na cidade.</p>
  <div class="duas">
    {img('fisico-cidade.png', 'Cidade: prédio da CitizenTech e prédio do provedor, ligados por cabo.')}
    {img('fisico-centro.png', 'Prédio da CitizenTech: salas e dispositivos.')}
  </div>
  {img('fisico-centro-zoom.png', 'Planta do Centro Comunitário: sala de rede (R1 e SW1), sala da equipe, sala de servidores e espaço do cidadão (AP e laptop).')}
</section>

<section>
  <h2>3. Plano de endereçamento</h2>
  <p>Faixa <b>{BASE}.0/24</b> dividida em quatro sub-redes /26 (64 endereços cada). Uma VLAN por setor.</p>
  <table>
    <tr><th>VLAN</th><th>Setor</th><th>Rede</th><th>Gateway (R1)</th><th>Faixa DHCP</th><th>Broadcast</th></tr>
    <tr><td>10</td><td>EQUIPE</td><td>{BASE}.0/26</td><td>{BASE}.1</td><td>.6 a .62</td><td>{BASE}.63</td></tr>
    <tr><td>20</td><td>CIDADÃO (Wi-Fi público)</td><td>{BASE}.64/26</td><td>{BASE}.65</td><td>.70 a .126</td><td>{BASE}.127</td></tr>
    <tr><td>30</td><td>SERVIDORES / SENSORES</td><td>{BASE}.128/26</td><td>{BASE}.129</td><td>.136 a .190</td><td>{BASE}.191</td></tr>
    <tr><td>–</td><td>Reserva (crescimento)</td><td>{BASE}.192/26</td><td>–</td><td>–</td><td>{BASE}.255</td></tr>
  </table>
  <table>
    <tr><th>Link / host</th><th>Endereço</th></tr>
    <tr><td>R1 G0/1 ↔ ISP G0/0</td><td>200.0.0.1/30 ↔ 200.0.0.2/30</td></tr>
    <tr><td>ISP G0/1 (rede "internet")</td><td>8.8.8.1/24</td></tr>
    <tr><td>Server-Internet</td><td>8.8.8.8/24, gateway 8.8.8.1</td></tr>
    <tr><td>Server-Solucao</td><td>{BASE}.130/26, gateway {BASE}.129, DNS {BASE}.130</td></tr>
  </table>
  <p>Excluídos do DHCP: {BASE}.1–.5, {BASE}.65–.69 e {BASE}.129–.135 (gateways e servidor).</p>
  <h3>DNS do Server-Solucao</h3>
  <table>
    <tr><th>Nome</th><th>Tipo</th><th>Endereço</th></tr>
    <tr><td>citizentech.local</td><td>A</td><td>{BASE}.130</td></tr>
    <tr><td>internet.com</td><td>A</td><td>8.8.8.8</td></tr>
  </table>
</section>

<section>
  <h2>4. Configuração (trechos)</h2>
  <p>Trechos da configuração aplicada nos equipamentos (o <code>show running-config</code> do R1 foi conferido
     no Packet Tracer e confere com estes trechos).</p>
  {trecho('SW1.txt', 3, 27, 'SW1 – VLANs, portas de acesso e trunk 802.1Q', 'hostname')}
  {trecho('R1.txt', 19, 37, 'R1 – router-on-a-stick (subinterfaces dot1Q)', 'interface g0/0')}
  {trecho('R1.txt', 38, 43, 'R1 – interface para o provedor (NAT outside)', 'interface g0/1')}
  {trecho('R1.txt', 44, 59, 'R1 – DHCP: um pool por VLAN, com exclusões', 'ip dhcp excluded-address')}
  {trecho('R1.txt', 60, 62, 'R1 – NAT/PAT (overload) e rota padrão', 'access-list 1')}
  {trecho('R1.txt', 63, 72, 'R1 – ACL estendida do Wi-Fi do cidadão (aplicada em g0/0.20, entrada)', 'ip access-list extended')}
  {trecho('R1.txt', 4, 18, 'R1 – acesso seguro: enable secret, usuário, SSH v2 e linhas', 'enable secret')}
  {trecho('R1.txt', 73, 81, 'R1 – SSH só a partir da VLAN Equipe (access-class) e timeout', 'ip access-list standard')}
  {trecho('SW1.txt', 28, 55, 'SW1 – reforço: senhas, SSH, IP de gerência na VLAN 30 e portas sem uso desligadas', 'crypto key')}
  {trecho('ISP.txt', 3, 26, 'ISP – provedor (mesmo padrão de SSH e senhas)', 'hostname')}
</section>

<section>
  <h2>5. Segurança</h2>
  <table>
    <tr><th>Controle</th><th>Como foi feito</th></tr>
    <tr><td>ACL estendida CIDADAO-IN</td><td>Na entrada de G0/0.20: o Wi-Fi do cidadão só acessa DNS (UDP 53) e HTTP (TCP 80)
        do Server-Solucao e a internet. Bloqueia a VLAN Equipe, o resto da VLAN Servidores e a reserva. Libera o DHCP (UDP 67).</td></tr>
    <tr><td>Roteadores só por SSH</td><td>SSH v2, <code>login local</code> e <code>transport input ssh</code> nas linhas vty do R1 e do ISP; o telnet é encerrado.</td></tr>
    <tr><td>SSH só da VLAN Equipe</td><td>No R1, <code>access-class SSH-ADMIN</code> nas linhas vty libera a administração só para a rede da Equipe
        ({BASE}.0/26). Console e vty têm <code>exec-timeout</code> de 10 minutos.</td></tr>
    <tr><td>Switch protegido</td><td>O SW1 também tem <code>enable secret</code>, usuário, senha de console e SSH v2, acessível pelo IP de
        gerência {BASE}.131 (VLAN 30). Portas sem uso (Fa0/5–24 e Gi0/2) ficam desligadas.</td></tr>
    <tr><td>Senhas</td><td><code>enable secret</code>, usuário <code>admin</code> com <code>secret</code>, senha de console e
        <code>service password-encryption</code>.</td></tr>
    <tr><td>Wi-Fi com WPA2</td><td>AP-Cidadao e laptop com WPA2-PSK (criptografia AES), SSID CitizenTech-Publico.</td></tr>
    <tr><td>Segmentação</td><td>Equipe, Cidadão e Servidores em VLANs separadas; só o R1 roteia entre elas.</td></tr>
  </table>
  <h3>Credenciais de laboratório (somente Packet Tracer)</h3>
  <table>
    <tr><th>Item</th><th>Valor</th></tr>
    <tr><td>Usuário SSH</td><td>admin / Gs2026@ssh</td></tr>
    <tr><td>Enable secret</td><td>Gs2026@en</td></tr>
    <tr><td>Console</td><td>Gs2026@con</td></tr>
    <tr><td>Wi-Fi WPA2-PSK</td><td>CitizenTech2026</td></tr>
  </table>
</section>

<section>
  <h2>6. Testes</h2>
  <p>Cada teste foi executado no Packet Tracer e prova um requisito. O primeiro ping de cada teste pode
     expirar enquanto o ARP aprende os endereços.</p>
  <div class="grade">
    <div class="cel"><h3>Teste 1 – Ping entre VLANs</h3>
      <p>PC-Equipe1 (VLAN 10) faz ping em {BASE}.130 (Server-Solucao, VLAN 30): 4 de 4 respostas, TTL 127,
         ou seja, passou pelo R1. <span class="ok">Passou.</span></p>
      {img('teste1.png', 'Teste 1: ping de PC-Equipe1 até Server-Solucao.')}</div>
    <div class="cel"><h3>Teste 2a – DHCP no PC da Equipe</h3>
      <p>PC-Equipe1 recebeu {BASE}.6/26, gateway {BASE}.1 e DNS {BASE}.130. <span class="ok">Passou.</span></p>
      {img('teste2.png', 'Teste 2a: ipconfig /all no PC-Equipe1.')}</div>
    <div class="cel"><h3>Teste 2b – DHCP no Wi-Fi</h3>
      <p>O laptop recebeu {BASE}.71/26, gateway {BASE}.65 e DNS {BASE}.130. <span class="ok">Passou.</span></p>
      {img('teste2b-laptop.png', 'Teste 2b: ipconfig /renew no Laptop-Cidadao.')}</div>
    <div class="cel"><h3>Teste 3 – Página pelo nome</h3>
      <p>O laptop abre <code>http://citizentech.local</code> e a Ficha aparece (DNS e HTTP do servidor).
         <span class="ok">Passou.</span></p>
      {img('teste3.png', 'Teste 3: navegador do laptop em http://citizentech.local.')}</div>
    <div class="cel"><h3>Teste 4 – Acesso à internet</h3>
      <p>O laptop abre <code>http://internet.com</code> e a página do Server-Internet (8.8.8.8) aparece, passando
         por NAT e pelo ISP. <span class="ok">Passou.</span></p>
      {img('teste4.png', 'Teste 4: navegador do laptop em http://internet.com.')}</div>
    <div class="cel"><h3>Teste 5 – NAT/PAT</h3>
      <p><code>show ip nat translations</code> no R1 logo após o teste 4: {BASE}.71 aparece traduzido para
         200.0.0.1. <span class="ok">Passou.</span></p>
      {img('teste5.png', 'Teste 5: show ip nat translations no R1.')}</div>
    <div class="cel"><h3>Teste 6a – Acesso barrado pela ACL</h3>
      <p>O laptop do Wi-Fi faz ping no PC da Equipe ({BASE}.6): bloqueado, "Destination host unreachable" vindo
         do gateway {BASE}.65. <span class="ok">Passou.</span></p>
      {img('teste6.png', 'Teste 6a: ping do laptop para o PC da Equipe, barrado.')}</div>
    <div class="cel"><h3>Teste 6b – Acertos na ACL</h3>
      <p><code>show access-lists</code> no R1 mostra os acertos nas regras <code>deny</code> e nas regras de
         DNS e HTTP. <span class="ok">Passou.</span></p>
      {img('teste6b-acl.png', 'Teste 6b: show access-lists com os matches.')}</div>
    <div class="cel"><h3>Teste 7 – SSH nos roteadores</h3>
      <p>Do PC-Equipe1: <code>ssh -l admin {BASE}.1</code> pede a senha e entra no R1; <code>show ip ssh</code>
         mostra SSH v2. O telnet para o R1 é encerrado. <span class="ok">Passou.</span></p>
      {img('teste7.png', 'Teste 7: SSH aceito e telnet encerrado.')}</div>
    <div class="cel"><h3>Teste 7b – SSH no switch</h3>
      <p>Do PC-Equipe1: <code>ssh -l admin {BASE}.131</code> entra no SW1 (IP de gerência na VLAN 30).
         <code>show ip interface brief</code> mostra Vlan30 com {BASE}.131 e as portas sem uso desligadas.
         <span class="ok">Passou.</span></p>
      {img('teste7b-sw1.png', 'Teste 7b: SSH no SW1 e portas sem uso em administratively down.')}</div>
  </div>
</section>
"""

documento = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
             f"<title>Network – CitizenTech</title><style>{CSS}</style></head><body>{corpo}</body></html>")

if not NAVEGADOR:
    sys.exit("Chrome ou Edge não encontrado.")

with tempfile.TemporaryDirectory() as tmp:
    arquivo_html = Path(tmp) / "relatorio.html"
    arquivo_html.write_text(documento, encoding="utf-8")
    subprocess.run([NAVEGADOR, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={SAIDA_PDF}", arquivo_html.as_uri()], check=True, timeout=120)

print("PDF gerado:", SAIDA_PDF)
if pendentes:
    print("PENDENTE (placeholders na Ficha):", ", ".join(sorted(set(pendentes))))
if not definido:
    print(f"PENDENTE: número real da equipe (usando {X} provisoriamente)")
if X != EQUIPE_DOS_PRINTS:
    print(f"ATENÇÃO: os prints e o .pkt foram feitos com X = {EQUIPE_DOS_PRINTS}. "
          "Refaça a rede e os prints com o novo X antes de entregar.")
