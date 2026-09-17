/* Heavex — interações da landing page.
   Sem dependências. Loops de animação só rodam com o elemento na tela. */
(() => {
  'use strict';

  const d = document;
  const hasIO = 'IntersectionObserver' in window;
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));

  /** Chama onEnter/onLeave quando o elemento entra (na fração pedida) ou sai da tela. */
  function watch(targets, { onEnter, onLeave, once = false, threshold = 0, rootMargin = '0px' }) {
    const list = [...targets].filter(Boolean);
    if (!list.length) return;
    if (!hasIO) { list.forEach((el) => onEnter(el)); return; }
    // isIntersecting é true com 1px visível; a entrada exige a fração pedida.
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting && e.intersectionRatio >= threshold) {
          onEnter(e.target);
          if (once) io.unobserve(e.target);
        } else if (!e.isIntersecting && onLeave) {
          onLeave(e.target);
        }
      }
    }, { threshold: threshold > 0 ? [0, threshold] : 0, rootMargin });
    list.forEach((el) => io.observe(el));
  }

  /* ── Navegação: fundo sólido após o topo + menu mobile ───────────── */
  const nav = d.querySelector('[data-nav]');
  const toggle = d.querySelector('[data-nav-toggle]');
  const sentinel = d.querySelector('[data-nav-sentinel]');

  if (nav && sentinel && hasIO) {
    new IntersectionObserver(([e]) => nav.classList.toggle('is-solid', !e.isIntersecting)).observe(sentinel);
  }

  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  }
  if (nav && toggle) {
    toggle.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
    nav.addEventListener('click', (e) => { if (e.target.closest('.nav-menu a')) setMenu(false); });
    d.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); toggle.focus(); }
    });
  }

  /* ── Vídeo do hero: começa assim que a página abre ───────────────── */
  const hero = d.querySelector('[data-hero]');
  const video = d.querySelector('[data-hero-video]');
  const videoBtn = d.querySelector('[data-video-toggle]');

  if (video && videoBtn && video.canPlayType('video/mp4')) {
    let userPaused = false;

    const loadVideo = () => {
      if (video.src) return true;
      const variant = matchMedia('(orientation: portrait)').matches ? 'mobile' : 'desktop';
      const candidates = [
        [`assets/videos/hero-${variant}.av1.mp4?v=1`, 'video/mp4; codecs="av01.0.08M.08"'],
        [`assets/videos/hero-${variant}.h264.mp4?v=1`, 'video/mp4; codecs="avc1.640028"'],
      ];
      const pick = candidates.find(([, type]) => video.canPlayType(type) === 'probably')
        || candidates.find(([, type]) => video.canPlayType(type) !== '');
      if (!pick) return false;
      // Tamanho intrínseco declarado antes: a chegada dos metadados não refaz layout.
      video.width = variant === 'mobile' ? 364 : 1256;
      video.height = 648;
      video.src = pick[0];
      return true;
    };

    // Autoplay bloqueado (ex.: iPhone em modo de economia de energia):
    // tenta de novo no primeiro toque/clique/tecla da pessoa.
    const retryOnGesture = () => {
      const go = () => {
        ['touchend', 'click', 'keydown'].forEach((t) => d.removeEventListener(t, go, true));
        if (!userPaused) video.play().catch(() => {});
      };
      ['touchend', 'click', 'keydown'].forEach((t) => d.addEventListener(t, go, { capture: true, passive: true }));
    };
    const play = () => {
      const p = video.play();
      if (p && p.catch) p.catch(retryOnGesture);
    };

    const syncBtn = () => {
      const playing = Boolean(video.src) && !video.paused;
      videoBtn.classList.toggle('is-paused', !playing);
      videoBtn.setAttribute('aria-label', playing ? 'Pausar vídeo de fundo' : 'Reproduzir vídeo de fundo');
    };

    video.addEventListener('playing', () => video.classList.add('is-playing'), { once: true });
    video.addEventListener('play', syncBtn);
    video.addEventListener('pause', syncBtn);
    videoBtn.hidden = false;
    videoBtn.addEventListener('click', () => {
      if (video.src && !video.paused) { userPaused = true; video.pause(); return; }
      userPaused = false;
      if (loadVideo()) play();
    });

    // Só não começa sozinho quando a pessoa ativou economia de dados.
    const conn = navigator.connection;
    if (!(conn && conn.saveData) && loadVideo()) play();
    syncBtn();

    // Pausa fora da tela (bateria/CPU) e retoma ao voltar.
    watch([hero], {
      onEnter: () => { if (video.src && video.paused && !userPaused) play(); },
      onLeave: () => { if (video.src) video.pause(); },
    });
  }

  /* ── Revelação ao rolar ──────────────────────────────────────────── */
  watch(d.querySelectorAll('.reveal'), {
    onEnter: (el) => el.classList.add('is-in'),
    once: true, threshold: 0.12, rootMargin: '0px 0px -6% 0px',
  });

  /* ── Cards do método: animações rodam só enquanto visíveis ───────── */
  watch(d.querySelectorAll('[data-live]'), {
    onEnter: (el) => el.classList.add('is-live'),
    onLeave: (el) => el.classList.remove('is-live'),
  });

  /* ── O que resolvemos: risca todas as palavras ao mesmo tempo ────── */
  watch(d.querySelectorAll('[data-pains]'), {
    onEnter: (el) => el.classList.add('is-in'),
    once: true, threshold: 0.3,
  });

  /* ── Galerias com deslize (celular): indicador de posição ────────── */
  d.querySelectorAll('[data-rail]').forEach((rail) => {
    const dots = d.querySelector(`[data-rail-dots="${rail.id}"]`);
    if (!dots || !hasIO) return;
    const items = [...rail.children];
    const marks = items.map((_, i) => {
      const m = dots.appendChild(d.createElement('i'));
      if (i === 0) m.classList.add('is-on');
      return m;
    });
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const idx = items.indexOf(e.target);
        marks.forEach((m, k) => m.classList.toggle('is-on', k === idx));
      }
    }, { root: rail, threshold: 0.6 });
    items.forEach((it) => io.observe(it));
  });

  /* ── Como funciona: mapa com cada etapa sendo concluída ──────────── */
  const flow = d.querySelector('[data-flow]');
  if (flow) {
    const nodes = [...flow.querySelectorAll('.mnode')];
    const statusEl = flow.querySelector('[data-hud-status]');
    const pctEl = flow.querySelector('[data-hud-pct]');
    const barEl = flow.querySelector('[data-hud-bar]');
    const railEl = flow.querySelector('[data-rail-fill]');
    const replay = flow.querySelector('[data-flow-replay]');
    const titles = nodes.map((n) => n.querySelector('.mnode-title').textContent.trim());
    const STEP = 1000;   // tempo de cada etapa "em andamento"
    const LINK = 600;    // tempo da linha até a próxima etapa
    let run = 0;         // token: incrementa para cancelar uma execução em andamento
    let pct = 0;
    let state = 'idle';  // idle | running | done

    const setState = (node, label) => { node.querySelector('[data-state]').textContent = label; };

    function tweenPct(to) {
      const from = pct;
      const t0 = performance.now();
      const token = run;
      const tick = (now) => {
        if (token !== run) return;
        const k = Math.min(1, (now - t0) / 600);
        pct = Math.round(from + (to - from) * (1 - (1 - k) ** 3));
        pctEl.textContent = String(pct);
        if (k < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      barEl.style.setProperty('--p', to / 100);
    }

    function reset() {
      run += 1;
      pct = 0;
      state = 'idle';
      flow.classList.remove('is-running', 'is-live');
      nodes.forEach((n) => { n.classList.remove('is-active', 'is-done'); setState(n, 'Aguardando'); });
      flow.querySelectorAll('.seg').forEach((s) => s.classList.remove('is-drawn'));
      pctEl.textContent = '0';
      barEl.style.setProperty('--p', 0);
      railEl.style.setProperty('--p', 0);
      statusEl.textContent = 'Aguardando';
    }

    async function play() {
      reset();
      const token = run;
      state = 'running';
      flow.classList.add('is-running');
      const last = nodes.length - 1;

      for (let i = 0; i <= last; i += 1) {
        const node = nodes[i];
        node.classList.add('is-active');
        setState(node, 'Em andamento');
        statusEl.textContent = titles[i];
        await wait(STEP);
        if (token !== run) return;

        node.classList.remove('is-active');
        node.classList.add('is-done');
        setState(node, i === last ? 'Em produção' : 'Concluído');
        tweenPct(Math.round(((i + 1) / nodes.length) * 100));

        if (i < last) {
          flow.querySelectorAll(`[data-seg="${i}"] .seg`).forEach((s) => s.classList.add('is-drawn'));
          railEl.style.setProperty('--p', (i + 1) / last);
          await wait(LINK);
          if (token !== run) return;
        }
      }
      statusEl.textContent = 'Em produção';
      flow.classList.remove('is-running');
      flow.classList.add('is-live');
      state = 'done';
    }

    watch([flow.querySelector('.map')], {
      onEnter: () => { if (state === 'idle') play(); },
      onLeave: () => { if (state !== 'idle') reset(); },
      threshold: 0.3,
    });
    replay.addEventListener('click', play);
  }
})();
