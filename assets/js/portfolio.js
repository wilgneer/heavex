/* Heavex — portfólio: filtro por categoria. */
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
