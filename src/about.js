// Project overview shown once after unlock, and on demand from the floating button.
// Buttons reuse the app's own data-action handlers, so routing stays in one place.
(function () {
  const about = document.getElementById('about');
  const reopen = document.getElementById('about-open');
  if (!about || !reopen) return;
  const SEEN_KEY = 'brightspace-support-about-seen';

  const open = () => {
    about.hidden = false;
    reopen.hidden = true;
    document.body.classList.add('about-open');
    about.scrollTop = 0;
    const card = about.querySelector('.about-card');
    if (card) card.focus({ preventScroll: true });
  };
  const close = () => {
    about.hidden = true;
    reopen.hidden = false;
    document.body.classList.remove('about-open');
    try { sessionStorage.setItem(SEEN_KEY, '1'); } catch (err) {}
  };

  about.addEventListener('click', event => {
    if (event.target === about || event.target.closest('[data-about-close], button[data-action]')) close();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !about.hidden) close();
  });
  reopen.addEventListener('click', open);

  // Show after the gate unlocks; the gate removes itself from the page on success.
  const showWhenUnlocked = () => {
    if (document.getElementById('gate')) return false;
    let seen = false;
    try { seen = sessionStorage.getItem(SEEN_KEY) === '1'; } catch (err) {}
    if (seen) { reopen.hidden = false; } else { open(); }
    return true;
  };
  if (!showWhenUnlocked()) {
    const watcher = new MutationObserver(() => { if (showWhenUnlocked()) watcher.disconnect(); });
    watcher.observe(document.body, { childList: true });
  }
})();
