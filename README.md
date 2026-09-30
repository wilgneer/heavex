# Heavex — Landing page / site institucional

HTML, CSS e JS puros. Nenhum framework, nenhuma fonte web e nenhuma requisição a terceiros.

## Rodar local

```bash
node scripts/serve.js
```

Abre em http://localhost:4330 (com brotli e Range requests, como na Vercel).

## Seções

Hero (vídeo) → Quem nós somos? → O que a Heavex faz → Nosso método → O que nós resolvemos? → Como funciona? → Resultados → Com nossos clientes → Rodapé

**O que a Heavex faz** é um acordeão com as 5 unidades (Experience, Mobility Intelligence, Business Systems + Heavex Connect, Academy, Security). Usa `<details name="unidade">`: abre uma e fecha a anterior, sem JavaScript. O conteúdo fechado não é renderizado, então as 5 unidades não pesam na abertura da página.

Todos os CTAs abrem o WhatsApp **(31) 99989-5589** (`wa.me/5531999895589`), cada um com uma mensagem inicial própria.

## Páginas

| URL | Arquivo | O que é |
|---|---|---|
| `/` | `index.html` | Landing page + site institucional |
| `/api-whatsapp` | `api-whatsapp.html` | Página do **Heavex Connect** — API oficial do WhatsApp |

O botão **API do WhatsApp** fica no menu do topo da página inicial (e dentro do menu, no celular), ao lado do "Fale conosco". Também há link no bloco Heavex Connect e no rodapé.

As duas páginas compartilham `assets/` e `assets/js/main.js`, mas cada uma tem o próprio CSS inline (é o que mantém uma requisição só por página). Mexeu no menu, no rodapé ou nos tokens de cor? Replique nas duas.

O caminho sem `.html` funciona por `cleanUrls` na Vercel; o `scripts/serve.js` faz o mesmo no local.

## Estrutura

| Caminho | O que é |
|---|---|
| `index.html` | Página inicial, com o CSS crítico inline |
| `api-whatsapp.html` | Página da API oficial do WhatsApp (CSS inline próprio) |
| `assets/js/main.js` | Menu, vídeo, reveals, galerias do celular, risco das dores, mapa |
| `assets/videos/hero-{desktop,mobile}.{av1,h264}.mp4` | Loop do hero (2s → 9s do bruto) |
| `assets/images/poster-*.{avif,webp}` | Primeiro quadro do loop, que também é o LCP |
| `assets/images/projetos/<slug>-{480,800}.{avif,webp}` | Fotos dos cards de Resultados (16:10) |
| `assets/images/clientes/` | (criar) fotos com clientes, 4:5 |
| `scripts/build-media.ps1` | Regera vídeos, posters e logo a partir dos arquivos brutos |
| `vercel.json` | Cache imutável em `/assets`, CSP e headers de segurança |

## Trocar a foto de um projeto

Gere uma imagem 16:10 e salve com o mesmo nome em `assets/images/projetos/`: `<slug>-800` e `<slug>-480`, cada uma em `.avif` e `.webp`. Os slugs são `lq-professional`, `destrave-sua-voz`, `evolution`, `dra-ana-carolina`, `master-education` e `maison-alto-valor`.

## Publicar fotos com clientes

Na seção `#clientes` do `index.html`, troque o `<div class="shot-empty">…</div>` de cada espaço por:

```html
<img src="assets/images/clientes/cliente-01.webp" width="800" height="1000" alt="Descreva a foto" loading="lazy" decoding="async">
```

Use formato retrato 4:5, com cerca de 800×1000 px e até ~120 KB.

## Regerar mídia do hero

```bash
powershell -ExecutionPolicy Bypass -File scripts/build-media.ps1
```

Depois, suba o `?v=` nas referências (os assets usam cache de 1 ano).

## Performance (Lighthouse 12, 3 rodadas cada, vídeo começando no carregamento)

| Perfil | Performance | Acessib. | Boas práticas | SEO | LCP |
|---|---|---|---|---|---|
| `/` mobile (Slow 4G, CPU 4×) | 99 | 100 | 100 | 100 | 1,2 s |
| `/` desktop | 100 | 100 | 100 | 100 | 0,3 s |
| `/api-whatsapp` mobile | 100 | 100 | 100 | 100 | 0,9 s |
| `/api-whatsapp` desktop | 100 | 100 | 100 | 100 | 0,3 s |

Fluidez no celular (390 px, DPR 3, CPU 4× mais lenta, rolagem da página inteira): ~58 fps de média e p95 de 16,8 ms por quadro. É o mesmo resultado da página sem animação nenhuma.

O mobile ficou em 99 (e não 100) depois da seção das unidades: o HTML passou de 10,7 para 14,6 KB comprimidos e o FCP simulado subiu de 1,0 s para 1,2 s. Para recuperar o 100 seria preciso tirar o CSS de baixo da dobra do documento e carregá-lo à parte — troca 1 ponto por um risco de conteúdo sem estilo ao rolar rápido, então mantive o arquivo único.

Como a página se mantém rápida:
- O LCP é o poster AVIF (3–7 KB), pré-carregado com `fetchpriority="high"`. O vídeo entra por cima com fade assim que começa a tocar.
- Loops infinitos (bordas dos cards, brilho dos botões, selo) só rodam com o bloco na tela.
- No celular, as bordas dos cards usam feixes pequenos animados só com `transform`. O feixe cônico gigante e o brilho no número ficam só no desktop.
- O risco das dores é um `scaleX` por palavra: roda na GPU, sem repintar texto.
- Header sem `backdrop-filter` no celular.
- O vídeo pausa fora da tela. Se o autoplay for bloqueado (iPhone em economia de energia), ele toca no primeiro toque.

## Pendências

- Domínio: preencher `og:url`, `og:image` e `canonical` (TODO no `<head>`).
- Revisar o texto de "Quem nós somos?" e colocar foto da equipe no lugar da imagem dos cubos.
- Revisar a comparação "API oficial × robô não oficial" e o passo a passo de implantação em `/api-whatsapp` (texto escrito por mim).
- **Heavex Security**: faltam as soluções e o "resultado entregue". Hoje a unidade aparece só com nome e subtítulo, sem abrir (ver TODO no `index.html`).
- Enviar as fotos com clientes.
