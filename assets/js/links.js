/* Heavex — página de links: botão de copiar o endereço. */
(() => {
  const btn = document.querySelector('[data-copiar]');
  const txt = document.querySelector('[data-copiar-txt]');
  if (!btn || !navigator.clipboard) return;
  const original = txt.textContent;
  btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText('https://heavex.com.br/links');
      txt.textContent = 'Link copiado!';
      btn.classList.add('ok');
      setTimeout(() => { txt.textContent = original; btn.classList.remove('ok'); }, 2200);
    } catch { /* navegador bloqueou: a pessoa copia da barra de endereço */ }
  });
})();
