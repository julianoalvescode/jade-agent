// Header shadow, mobile menu and copy buttons. No dependencies.
(() => {
  const header = document.querySelector('[data-header]');
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const toggle = document.querySelector('[data-nav-toggle]');
  const links = document.querySelector('[data-nav-links]');
  const setOpen = (open) => {
    links.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
  };
  toggle.addEventListener('click', () => setOpen(!links.classList.contains('is-open')));
  links.addEventListener('click', (event) => { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setOpen(false); });

  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const code = button.parentElement.querySelector('code').innerText;
      try {
        await navigator.clipboard.writeText(code);
        button.textContent = 'Copied';
      } catch {
        button.textContent = 'Press Ctrl+C';
      }
      setTimeout(() => { button.textContent = 'Copy'; }, 2000);
    });
  });
})();
