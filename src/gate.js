// Access gate. The password ships in the page, so this only deters casual
// visitors; use Vercel Deployment Protection for an enforced control.
(function () {
  const PASSWORD = 'amarah';
  const REMEMBER_KEY = 'brightspace-support-unlocked';
  const gate = document.getElementById('gate');
  const app = document.getElementById('app');
  if (!gate || !app) return;
  const form = document.getElementById('gate-form');
  const input = document.getElementById('gate-input');
  const error = document.getElementById('gate-error');

  const unlock = () => {
    gate.remove();
    app.hidden = false;
    document.body.classList.remove('locked');
    window.dispatchEvent(new Event('resize'));
  };

  // Storage is unavailable in some privacy modes; the gate still works without it.
  let remembered = false;
  try {
    remembered = sessionStorage.getItem(REMEMBER_KEY) === '1';
  } catch (err) {}
  if (remembered) {
    unlock();
    return;
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    if (input.value.trim().toLowerCase() !== PASSWORD) {
      error.hidden = false;
      input.value = '';
      input.focus();
      return;
    }
    try {
      sessionStorage.setItem(REMEMBER_KEY, '1');
    } catch (err) {}
    unlock();
  });
  input.focus();
})();
