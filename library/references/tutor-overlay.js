// Temporary page-local tutor overlay for Claude in Chrome (javascript_tool).
// Draws a red outline and a note card next to a visible control. Never submits or edits anything.
// Disappears on navigation. Re-inject on every page. Verified on d2l.msu.edu 2026-09-22.
// D2L notes: navbar/tool buttons are light-DOM custom elements (d2l-button, d2l-dropdown);
// utility buttons such as Settings are <d2l-button-subtle text="Settings"> with the label in shadow DOM,
// so match on text content OR text/aria-label attributes, and walk shadow roots.
// Usage: window.__tut.hl('Visible label', 'WHAT/WHY/TICKET/NEXT text', {title, partial, index, width})
//        window.__tut.clear()
(() => {
  window.__tut = {
    clear() { document.querySelectorAll('.__tut').forEach(n => n.remove()); },
    all(root, acc) { for (const e of root.querySelectorAll('*')) { acc.push(e); if (e.shadowRoot) this.all(e.shadowRoot, acc); } return acc; },
    hl(label, text, o = {}) {
      this.clear();
      const norm = s => (s || '').replace(/\s+/g, ' ').trim();
      const prefer = o.prefer || 'a,button,d2l-button,d2l-button-subtle,d2l-dropdown-button-subtle,[role=menuitem],[role=tab],[role=radio],[role=checkbox],[role=button],input,label,h1,h2,h3';
      const lab = e => norm(e.tagName === 'INPUT' ? (e.value || e.getAttribute('aria-label')) : (e.textContent || e.getAttribute('text') || e.getAttribute('aria-label')));
      const attr = e => norm(e.getAttribute('text') || e.getAttribute('aria-label') || '');
      let c = this.all(document, [])
        .filter(e => !e.closest('.__tut') && !['SCRIPT', 'STYLE', 'HTML', 'BODY'].includes(e.tagName))
        .filter(e => { const t = lab(e), a = attr(e); return o.partial ? (t.includes(label) || a.includes(label)) : (t === label || a === label); })
        .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
      if (!c.length) return { ok: false, reason: 'no visible match', label };
      let pick = c.filter(e => e.matches(prefer));
      if (!pick.length) pick = c.filter(e => !c.some(x => x !== e && e.contains(x)));
      const el = pick[o.index || 0];
      const r0 = el.getBoundingClientRect();
      if (r0.top < 60 || r0.bottom > innerHeight - 60) el.scrollIntoView({ block: 'center' });
      const r = el.getBoundingClientRect();
      const pad = o.pad || 4;
      const box = document.createElement('div'); box.className = '__tut';
      Object.assign(box.style, { position: 'fixed', left: (r.left - pad) + 'px', top: (r.top - pad) + 'px', width: (r.width + 2 * pad) + 'px', height: (r.height + 2 * pad) + 'px', border: '3px solid #c92323', borderRadius: '5px', boxShadow: '0 0 0 3px rgba(201,35,35,.2)', pointerEvents: 'none', zIndex: 2147483646 });
      const card = document.createElement('div'); card.className = '__tut'; card.setAttribute('role', 'note');
      const w = o.width || 400;
      const below = r.bottom + 190 < innerHeight;
      const left = Math.max(8, Math.min(o.cardLeft != null ? o.cardLeft : r.left, innerWidth - w - 12));
      Object.assign(card.style, { position: 'fixed', left: left + 'px', top: (below ? r.bottom + pad + 10 : Math.max(8, r.top - pad - 10 - 170)) + 'px', width: w + 'px', background: '#fff', color: '#1e1e1e', border: '2px solid #c92323', borderRadius: '7px', padding: '9px 12px', font: '13px/1.45 system-ui,Segoe UI,Helvetica,Arial,sans-serif', boxShadow: '0 6px 18px rgba(0,0,0,.28)', zIndex: 2147483647, pointerEvents: 'none' });
      const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
      card.innerHTML = '<div style="font-weight:700;color:#c92323;margin-bottom:4px">' + esc(o.title || label) + '</div>' + esc(text).replace(/\n/g, '<br>');
      document.body.append(box, card);
      return { ok: true, tag: el.tagName, matches: c.length, center: { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) }, rect: { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) } };
    }
  };
  return 'ready';
})();
