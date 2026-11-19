# Monta a página /portfolio reaproveitando tokens, menu e rodapé da página da API.
import io, re, json

BASE = 'C:/Users/delll/OneDrive/Documentos/Heavex/'
fonte = io.open(BASE + 'api-whatsapp.html', encoding='utf-8').read()

def bloco_css(nome, proximo):
    ini = fonte.find('/* \u2500\u2500 ' + nome)
    fim = fonte.find('/* \u2500\u2500 ' + proximo) if proximo else fonte.find('</style>')
    assert ini > 0 and fim > ini, nome
    return fonte[ini:fim].rstrip() + '\n'

# tokens + reset: do :root até a navegação
ini_root = fonte.find(':root{')
css_tokens = fonte[ini_root:fonte.find('/* \u2500\u2500 Navega')].rstrip() + '\n'
css_nav = bloco_css('Navega\u00e7\u00e3o', 'Base')
css_base = bloco_css('Base', 'Hero')
css_rodape = bloco_css('Rodap\u00e9', None)
# o bloco do rodapé termina antes do @media de movimento reduzido
corte = css_rodape.find('@media (prefers-reduced-motion')
if corte > 0:
    css_rodape = css_rodape[:corte].rstrip() + '\n'

nav = fonte[fonte.find('<header class="nav"'):fonte.find('</header>') + len('</header>')]
lista_velha = '''<ul class="nav-links">
          <li><a href="/#quem-somos">Quem somos</a></li>
          <li><a href="/#o-que-fazemos">O que fazemos</a></li>
          <li><a href="/#resultados">Resultados</a></li>
          <li><a href="/">Voltar ao site</a></li>
        </ul>'''
lista_nova = '''<ul class="nav-links">
          <li><a href="/#quem-somos">Quem somos</a></li>
          <li><a href="/#o-que-fazemos">O que fazemos</a></li>
          <li><a href="/portfolio" aria-current="page">Portfólio</a></li>
          <li><a href="/api-whatsapp">API do WhatsApp</a></li>
          <li><a href="/">Voltar ao site</a></li>
        </ul>'''
assert lista_velha in nav, 'lista do menu nao encontrada'
nav = nav.replace(lista_velha, lista_nova)
rodape = fonte[fonte.find('<footer class="foot"'):fonte.find('</footer>') + len('</footer>')]

# ─────────────────────────────────────────────────────────────── projetos
ICONES = {
 'sistema': '<path d="M3 5.5A2.5 2.5 0 0 1 5.5 3h13A2.5 2.5 0 0 1 21 5.5v13a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 18.5Z"/><path d="M3 8.5h18M7 12.5h6M7 16h9"/>',
 'lp': '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 8h18M7 12h10M7 15.5h6"/><rect x="14" y="14.5" width="4.5" height="2.5" rx="1.25"/>',
 'automacao': '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/><circle cx="12" cy="12" r="3.4"/>',
 'bot': '<rect x="4" y="7.5" width="16" height="12" rx="3"/><path d="M12 3v4.5M8.5 13h.01M15.5 13h.01M9.5 16.5h5"/>',
 'fiscal': '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2Z"/><path d="M9.5 8h5M9.5 12h5M9.5 15.5h3"/>',
 'mapa': '<path d="m3 6.5 6-2.5 6 2.5 6-2.5v13L15 19.5 9 17l-6 2.5Z"/><path d="M9 4v13M15 6.5v13"/>',
 'dados': '<ellipse cx="12" cy="6" rx="8" ry="3.2"/><path d="M4 6v12c0 1.8 3.6 3.2 8 3.2s8-1.4 8-3.2V6"/><path d="M4 12c0 1.8 3.6 3.2 8 3.2s8-1.4 8-3.2"/>',
 'chat': '<path d="M21 12a8 8 0 1 1-3.3-6.5"/><path d="M21 4v5h-5"/><path d="M8.5 11h7M8.5 14.5h4"/>',
 'loja': '<path d="M4 8h16l-1 11.5a2 2 0 0 1-2 1.8H7a2 2 0 0 1-2-1.8Z"/><path d="M8.5 8V6a3.5 3.5 0 0 1 7 0v2"/>',
 'saude': '<path d="M5 4.5h14v15l-7-3-7 3Z"/><path d="M12 9v5M9.5 11.5h5"/>',
}

def card(cat, icone, titulo, texto, tags, entregue=False, link=None, img=None):
    return dict(cat=cat, icone=icone, titulo=titulo, texto=texto, tags=tags, entregue=entregue, link=link, img=img)

PROJETOS = [
 # ── entregues (reais) ───────────────────────────────────────────────────
 card('sistemas', 'loja', "L'Q Professional",
      'E-commerce completo de produtos profissionais de beleza, integrado a ERP, pagamento e frete em tempo real.',
      ['Bling', 'PagBank', 'Melhor Envio'], True, 'https://lqprofessional.com.br', 'lq-professional'),
 card('landing', 'lp', 'Destrave sua Voz',
      'P\u00e1gina da imers\u00e3o em orat\u00f3ria, com venda de ingressos, capta\u00e7\u00e3o de leads e painel de gest\u00e3o.',
      ['Ingressos', 'Leads', 'Painel'], True, 'https://destravesuavozbh.com.br', 'destrave-sua-voz'),
 card('sistemas', 'sistema', 'Evolution',
      'Plataforma de eventos e campeonatos de Jiu-Jitsu: inscri\u00e7\u00f5es, chaveamento, pesagem e resultados.',
      ['React', 'Node', 'Supabase'], True, None, 'evolution'),
 card('sistemas', 'saude', 'Cl\u00ednica Dra. Ana Carolina',
      'Gest\u00e3o cl\u00ednica completa: agenda, atendimentos, anamnese digital, financeiro e estoque por lote.',
      ['React', 'Firebase', 'TypeScript'], True, None, 'dra-ana-carolina'),
 card('landing', 'lp', 'Master Education',
      'P\u00e1gina de alta convers\u00e3o para evento high ticket, leve e r\u00e1pida no celular.',
      ['HTML', 'CSS', 'Performance'], True, None, 'master-education'),
 card('landing', 'lp', 'Maison Alto Valor',
      'Site de posicionamento com capta\u00e7\u00e3o de leads para consultoria B2B.',
      ['HTML', 'Leads', 'GTM'], True, None, 'maison-alto-valor'),

 # ── soluções: reforma tributária ────────────────────────────────────────
 card('fiscal', 'fiscal', 'Simulador de Impacto da Reforma',
      'Compara a carga atual com CBS e IBS por produto, servi\u00e7o e cen\u00e1rio, para a empresa enxergar o efeito no pre\u00e7o e na margem antes da virada.',
      ['CBS/IBS', 'Simula\u00e7\u00e3o', 'Margem']),
 card('fiscal', 'fiscal', 'Motor de C\u00e1lculo CBS e IBS',
      'API de c\u00e1lculo com al\u00edquotas por UF e munic\u00edpio, regimes diferenciados e apura\u00e7\u00e3o de cr\u00e9dito, pronta para plugar no ERP ou no checkout.',
      ['API', 'Al\u00edquotas', 'Cr\u00e9dito']),
 card('fiscal', 'fiscal', 'Painel de Transi\u00e7\u00e3o Tribut\u00e1ria',
      'Acompanha o per\u00edodo em que os tributos antigos e os novos convivem, com o paralelo dos dois regimes lado a lado e a proje\u00e7\u00e3o por ano.',
      ['Dashboard', 'Transi\u00e7\u00e3o', 'Proje\u00e7\u00e3o']),
 card('fiscal', 'dados', 'Revisor de Cadastro Fiscal',
      'Audita NCM, CST e CFOP dos itens, aponta diverg\u00eancias e prepara a base para a virada, porque cadastro errado vira imposto errado.',
      ['NCM', 'CST', 'Auditoria']),
 card('fiscal', 'automacao', 'Conciliador de Split Payment',
      'Concilia o recolhimento feito na liquida\u00e7\u00e3o com pedidos e receb\u00edveis, apontando diverg\u00eancia por transa\u00e7\u00e3o.',
      ['Concilia\u00e7\u00e3o', 'Receb\u00edveis', 'Fiscal']),

 # ── soluções: robôs e bots ──────────────────────────────────────────────
 card('bots', 'chat', 'Bot de Atendimento no WhatsApp',
      'Atende pela API oficial: faz triagem, responde o que se repete, registra o contato e passa para um humano no ponto certo.',
      ['API oficial', 'Triagem', 'Handoff']),
 card('bots', 'bot', 'Rob\u00f4 de Portais e Documentos',
      'Entra em portais p\u00fablicos e privados, consulta, baixa documentos e organiza tudo, com registro de cada execu\u00e7\u00e3o.',
      ['RPA', 'Agendado', 'Log']),
 card('bots', 'dados', 'Rob\u00f4 de Concilia\u00e7\u00e3o Banc\u00e1ria',
      'Importa extratos, casa lan\u00e7amentos com o financeiro e separa o que sobrou para olho humano.',
      ['OFX', 'Financeiro', 'Regras']),
 card('bots', 'chat', 'Bot de Agendamento',
      'Agenda, confirma, lembra e remarca sozinho, direto no WhatsApp, com a agenda da empresa como fonte da verdade.',
      ['Agenda', 'Lembretes', 'Confirma\u00e7\u00e3o']),
 card('bots', 'bot', 'Monitor de Pre\u00e7os e Concorr\u00eancia',
      'Varre p\u00e1ginas e marketplaces em hor\u00e1rios definidos, guarda o hist\u00f3rico e avisa quando algo muda.',
      ['Monitoramento', 'Hist\u00f3rico', 'Alertas']),

 # ── soluções: automações ────────────────────────────────────────────────
 card('automacoes', 'automacao', 'Integrador ERP e Loja',
      'Mant\u00e9m produto, estoque, pre\u00e7o e pedido em sincronia entre o ERP e a loja ou o marketplace, sem redigita\u00e7\u00e3o.',
      ['ERP', 'Estoque', 'Pedidos']),
 card('automacoes', 'automacao', 'Automa\u00e7\u00e3o de Propostas e Contratos',
      'Gera o documento a partir dos dados do neg\u00f3cio, envia para assinatura, acompanha o status e arquiva.',
      ['Documentos', 'Assinatura', 'Arquivo']),
 card('automacoes', 'chat', 'Alertas Operacionais',
      'Transforma evento do sistema em aviso: estoque no limite, pedido parado, prazo vencendo, falha de integra\u00e7\u00e3o.',
      ['Regras', 'WhatsApp', 'E-mail']),
 card('automacoes', 'dados', 'Rotina de Backup e Integridade',
      'C\u00f3pia autom\u00e1tica em nuvem, teste peri\u00f3dico de restaura\u00e7\u00e3o e verifica\u00e7\u00e3o de integridade do banco.',
      ['Backup', 'Nuvem', 'Restaura\u00e7\u00e3o']),
 card('automacoes', 'dados', 'Relat\u00f3rio Autom\u00e1tico de Fechamento',
      'Consolida os n\u00fameros do per\u00edodo e entrega o relat\u00f3rio pronto no dia e na hora combinados.',
      ['BI', 'Agendado', 'PDF']),

 # ── soluções: sistemas ──────────────────────────────────────────────────
 card('sistemas', 'sistema', 'Sistema de Ordens de Servi\u00e7o',
      'Ordem aberta no escrit\u00f3rio, executada em campo pelo celular mesmo sem internet, com assinatura na tela e hist\u00f3rico.',
      ['Offline-first', 'Assinatura', 'Campo']),
 card('sistemas', 'mapa', 'Gest\u00e3o de Frota e Rotas',
      'Mostra onde a equipe est\u00e1, qual rota faz sentido, quanto se gasta por trajeto e onde est\u00e3o os gargalos no mapa.',
      ['Geolocaliza\u00e7\u00e3o', 'Rotas', 'BI geogr\u00e1fico']),
 card('sistemas', 'sistema', 'CRM Sob Medida',
      'Funil do jeito que a empresa vende de verdade, com hist\u00f3rico de contato, tarefas e integra\u00e7\u00e3o com o WhatsApp.',
      ['Funil', 'Hist\u00f3rico', 'WhatsApp']),
 card('sistemas', 'sistema', 'Portal do Cliente',
      '\u00c1rea onde o cliente acompanha pedido, contrato, documento e segunda via, sem precisar ligar para a empresa.',
      ['Autoatendimento', 'Documentos', 'Acesso']),
 card('sistemas', 'dados', 'Painel de Indicadores',
      'Os n\u00fameros que decidem o dia em uma tela s\u00f3, atualizados pela pr\u00f3pria opera\u00e7\u00e3o, sem planilha no meio.',
      ['Dashboard', 'Tempo real', 'Dados']),

 # ── soluções: landing pages ─────────────────────────────────────────────
 card('landing', 'lp', 'Landing Page de Capta\u00e7\u00e3o',
      'P\u00e1gina focada em uma a\u00e7\u00e3o, com formul\u00e1rio ou WhatsApp, feita para carregar r\u00e1pido no celular.',
      ['Convers\u00e3o', 'Performance', 'Mobile']),
 card('landing', 'lp', 'Landing Page Edit\u00e1vel',
      'A equipe troca texto, imagem e oferta por um painel, sem depender de desenvolvedor para cada ajuste.',
      ['Painel', 'Autonomia', 'CMS']),
 card('landing', 'lp', 'P\u00e1gina de Evento com Ingressos',
      'Programa\u00e7\u00e3o, lotes, inscri\u00e7\u00e3o e pagamento na mesma p\u00e1gina, com controle de vagas.',
      ['Ingressos', 'Lotes', 'Pagamento']),
]

FILTROS = [('todos','Todos'),('sistemas','Sistemas'),('landing','Landing pages'),
           ('automacoes','Automa\u00e7\u00f5es'),('bots','Rob\u00f4s e bots'),('fiscal','Reforma tribut\u00e1ria')]

def html_card(p):
    tags = ''.join('<li>%s</li>' % t for t in p['tags'])
    selo = ('<span class="selo selo-ok">Entregue</span>' if p['entregue']
            else '<span class="selo">Solu\u00e7\u00e3o</span>')
    if p['img']:
        s = p['img']
        media = ('<picture class="pcard-media">'
                 f'<source type="image/avif" srcset="assets/images/projetos/{s}-480.avif 480w, assets/images/projetos/{s}-800.avif 800w" sizes="(min-width:1024px) 380px, (min-width:640px) 46vw, 92vw">'
                 f'<img src="assets/images/projetos/{s}-800.webp" srcset="assets/images/projetos/{s}-480.webp 480w, assets/images/projetos/{s}-800.webp 800w" sizes="(min-width:1024px) 380px, (min-width:640px) 46vw, 92vw" width="800" height="500" alt="{p["titulo"]}" loading="lazy" decoding="async">'
                 '</picture>')
    else:
        media = ('<div class="pcard-art" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                 'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">' + ICONES[p['icone']] + '</svg></div>')
    link = (f'<a class="pcard-link" href="{p["link"]}" target="_blank" rel="noopener noreferrer">'
            f'{p["link"].replace("https://","")}<span aria-hidden="true">\u2197</span>'
            '<span class="sr-only"> (abre em nova aba)</span></a>') if p['link'] else ''
    return f"""        <article class="pcard" data-cat="{p['cat']}">
          {media}
          <div class="pcard-body">
            {selo}
            <h3 class="pcard-title">{p['titulo']}</h3>
            <p class="pcard-desc">{p['texto']}</p>
            <div class="pcard-foot">
              <ul class="tags">{tags}</ul>
              {link}
            </div>
          </div>
        </article>"""

cards = '\n'.join(html_card(p) for p in PROJETOS)
chips = '\n'.join(
    f'          <button class="chip{" is-on" if k=="todos" else ""}" type="button" data-filtro="{k}" aria-pressed="{"true" if k=="todos" else "false"}">{r}</button>'
    for k, r in FILTROS)
entregues = sum(1 for p in PROJETOS if p['entregue'])
solucoes = len(PROJETOS) - entregues

CSS_PAGINA = """/* ── Portfólio ───────────────────────────────────────── */
.ph{position:relative;isolation:isolate;overflow:hidden;padding:calc(var(--nav-h) + 56px) 0 8px}
.ph::before{content:"";position:absolute;inset:0;z-index:-2;background:radial-gradient(70% 55% at 20% 0%,rgba(53,229,95,.16),transparent 62%)}
.ph::after{content:"";position:absolute;inset:0;z-index:-1;opacity:.4;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:64px 64px;-webkit-mask-image:radial-gradient(70% 70% at 30% 20%,#000,transparent 75%);mask-image:radial-gradient(70% 70% at 30% 20%,#000,transparent 75%)}
.h1{margin-top:20px;font-size:clamp(2.25rem,9vw,4.5rem);font-weight:700;line-height:.95;letter-spacing:-.045em;text-transform:uppercase;text-wrap:balance;background:linear-gradient(180deg,#fff 40%,#b9c4bd 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.resumo{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.resumo span{display:inline-flex;align-items:center;gap:9px;padding:9px 15px;border:1px solid var(--line-2);border-radius:999px;background:rgba(0,0,0,.4);font:500 .75rem/1 var(--mono);letter-spacing:.1em;color:#dfe6e1}
.resumo b{font-weight:600;color:var(--green)}
.filtros{position:sticky;top:calc(var(--nav-h) + env(safe-area-inset-top));z-index:20;margin-top:40px;padding:14px 0;background:rgba(3,5,4,.92)}
.filtros-in{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin-inline:calc(var(--gutter) * -1);padding-inline:var(--gutter)}
.filtros-in::-webkit-scrollbar{display:none}
.chip{flex:none;min-height:42px;padding:0 16px;border:1px solid var(--line-2);border-radius:999px;font-size:.875rem;font-weight:500;color:var(--muted);white-space:nowrap;transition:color .2s,border-color .2s,background-color .2s}
.chip.is-on{border-color:var(--green);background:rgba(53,229,95,.12);color:#eafff0}
@media (hover:hover){.chip:hover{color:#fff;border-color:rgba(53,229,95,.5)}}
.grade{display:grid;gap:16px;padding:24px 0 clamp(72px,10vw,120px)}
@media (min-width:640px){.grade{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1024px){.grade{grid-template-columns:repeat(3,1fr);gap:20px}}
.pcard{position:relative;display:flex;flex-direction:column;border:1px solid var(--line);border-radius:22px;background:linear-gradient(180deg,#070a08,#000);overflow:hidden;transition:border-color .3s var(--ease),transform .3s var(--ease),box-shadow .3s var(--ease)}
.pcard[hidden]{display:none}
.pcard-media{display:block;aspect-ratio:16/10;border-bottom:1px solid var(--line);background:#050605;overflow:hidden}
.pcard-media img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.pcard-art{display:grid;place-items:center;aspect-ratio:16/7;border-bottom:1px solid var(--line);color:var(--green);background:radial-gradient(70% 90% at 50% 120%,rgba(53,229,95,.16),transparent 70%),linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px) 0 0/22px 22px,linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px) 0 0/22px 22px}
.pcard-art svg{width:40px;height:40px;transition:transform .4s var(--ease)}
.pcard-body{display:flex;flex:1;flex-direction:column;padding:20px}
.selo{align-self:flex-start;padding:5px 10px;border:1px solid var(--line-2);border-radius:999px;font:600 .5625rem/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.selo-ok{border-color:rgba(53,229,95,.4);background:rgba(53,229,95,.1);color:#9df0b4}
.pcard-title{margin-top:12px;font-size:1.25rem;font-weight:600;letter-spacing:-.02em;line-height:1.2}
.pcard-desc{margin-top:8px;color:var(--muted);font-size:.9375rem;line-height:1.5;text-wrap:pretty}
.pcard-foot{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-top:auto;padding-top:18px}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tags li{padding:5px 9px;border:1px solid var(--line-2);border-radius:999px;font:500 .625rem/1 var(--mono);letter-spacing:.06em;color:#c3cbc6}
.pcard-link{display:inline-flex;align-items:center;gap:6px;min-height:44px;font:500 .75rem/1 var(--mono);color:#fff}
.pcard-link::after{content:"";position:absolute;inset:0}
@media (hover:hover){
  .pcard:hover{border-color:rgba(53,229,95,.45);transform:translateY(-4px);box-shadow:0 24px 60px -30px rgba(53,229,95,.45)}
  .pcard:hover .pcard-media img{transform:scale(1.04)}
  .pcard:hover .pcard-art svg{transform:scale(1.12)}
  .pcard-link:hover{color:var(--green)}
}
.vazio{padding:40px 0;text-align:center;color:var(--muted)}
.final{position:relative;overflow:hidden;margin-bottom:clamp(72px,10vw,120px);padding:clamp(44px,7vw,68px) clamp(24px,5vw,56px);border:1px solid var(--line-2);border-radius:28px;background:radial-gradient(80% 90% at 0% 0%,rgba(53,229,95,.14),transparent 60%),linear-gradient(180deg,#070a08,#000)}
.final h2{font-size:clamp(1.625rem,5vw,2.5rem);font-weight:700;letter-spacing:-.035em;line-height:1.05;text-wrap:balance}
.final p{margin-top:14px;max-width:56ch;color:#c9d1cc;line-height:1.55}
.final .btn{margin-top:26px}
@media (max-width:519.98px){.final .btn{width:100%;justify-content:center}}
"""

CSS_REDUZIDO = """@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .btn-green::after{display:none}
  .pcard,.pcard-media img,.pcard-art svg{transition:none}
}
"""

pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Portf\u00f3lio — Heavex</title>
<meta name="description" content="Projetos entregues e solu\u00e7\u00f5es que a Heavex desenvolve: sistemas, landing pages, automa\u00e7\u00f5es, rob\u00f4s e bots e sistemas para a reforma tribut\u00e1ria.">
<meta name="theme-color" content="#030504">
<meta name="color-scheme" content="dark">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="https://heavex.com.br/portfolio">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Heavex">
<meta property="og:title" content="Portf\u00f3lio — Heavex">
<meta property="og:description" content="Projetos entregues e solu\u00e7\u00f5es que a Heavex desenvolve.">
<meta property="og:url" content="https://heavex.com.br/portfolio">
<meta property="og:image" content="https://heavex.com.br/assets/images/og-heavex.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Heavex — o futuro que melhora processos">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/images/favicon.svg?v=1" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png?v=1">
<script>document.documentElement.classList.add('js')</script>
<style>
{css_tokens}
{css_nav}
{css_base}
{CSS_PAGINA}
{css_rodape}
{CSS_REDUZIDO}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Portf\u00f3lio — Heavex","url":"https://heavex.com.br/portfolio","about":{{"@type":"Organization","name":"Heavex","legalName":"HEAVEX SOLUTIONS TECH LTDA","taxID":"69.138.557/0001-90"}}}}</script>
<script src="assets/js/portfolio.js?v=1" defer></script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conte\u00fado</a>

{nav}

<main id="conteudo">

  <section class="ph" aria-labelledby="ph-title">
    <div class="wrap">
      <p class="kicker">Portf\u00f3lio</p>
      <h1 class="h1" id="ph-title">O que a Heavex constr\u00f3i</h1>
      <p class="lead">Projetos no ar e solu\u00e7\u00f5es que desenvolvemos sob medida — de uma landing page a um sistema inteiro de opera\u00e7\u00e3o.</p>
      <div class="resumo">
        <span><b>{entregues}</b> projetos entregues</span>
        <span><b>{solucoes}</b> solu\u00e7\u00f5es no cat\u00e1logo</span>
        <span><b>5</b> frentes de atua\u00e7\u00e3o</span>
      </div>
    </div>
  </section>

  <div class="filtros">
    <div class="wrap">
      <div class="filtros-in" role="group" aria-label="Filtrar por tipo">
{chips}
      </div>
    </div>
  </div>

  <div class="wrap">
    <h2 class="sr-only">Projetos entregues e soluções</h2>
    <div class="grade" id="grade">
{cards}
    </div>
    <p class="vazio" hidden data-vazio>Nenhum item nesta categoria.</p>

    <section class="final" aria-labelledby="final-title">
      <h2 id="final-title">Tem um processo que precisa virar sistema?</h2>
      <p>Conte como funciona hoje. A gente desenha o fluxo, mostra o caminho e coloca no ar.</p>
      <a class="btn btn-green" href="https://wa.me/5531999895589?text=Ol%C3%A1!%20Vim%20pelo%20portf%C3%B3lio%20da%20Heavex." target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>
        Falar com a Heavex<span class="sr-only"> pelo WhatsApp (abre em nova aba)</span>
      </a>
    </section>
  </div>

</main>

{rodape}
</body>
</html>
"""

io.open(BASE + 'portfolio.html', 'w', encoding='utf-8').write(pagina)

JS = """/* Heavex — portfólio: filtro por categoria. */
(() => {
  'use strict';
  const chips = [...document.querySelectorAll('[data-filtro]')];
  const cards = [...document.querySelectorAll('.pcard')];
  const vazio = document.querySelector('[data-vazio]');
  if (!chips.length || !cards.length) return;

  function filtrar(cat) {
    let visiveis = 0;
    for (const c of cards) {
      const mostra = cat === 'todos' || c.dataset.cat === cat;
      c.hidden = !mostra;
      if (mostra) visiveis += 1;
    }
    if (vazio) vazio.hidden = visiveis > 0;
    for (const ch of chips) {
      const on = ch.dataset.filtro === cat;
      ch.classList.toggle('is-on', on);
      ch.setAttribute('aria-pressed', String(on));
    }
    history.replaceState(null, '', cat === 'todos' ? location.pathname : '#' + cat);
  }

  chips.forEach((ch) => ch.addEventListener('click', () => filtrar(ch.dataset.filtro)));

  // abre já filtrado quando a URL traz a categoria (ex.: /portfolio#fiscal)
  const inicial = location.hash.slice(1);
  if (inicial && chips.some((c) => c.dataset.filtro === inicial)) filtrar(inicial);
})();
"""
io.open(BASE + 'assets/js/portfolio.js', 'w', encoding='utf-8').write(JS)

print('portfolio.html gerado:', len(pagina), 'caracteres |', len(PROJETOS), 'cards |', entregues, 'entregues |', solucoes, 'solucoes')
