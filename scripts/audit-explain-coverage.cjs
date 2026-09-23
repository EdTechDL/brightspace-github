// Explain-clicks coverage audit for the Brightspace practice simulator.
// Usage (from the repo root):  npm run build && npx -y playwright@1 --version && node scripts/audit-explain-coverage.cjs
// Requires Playwright + Chromium (dev only; the shipped app stays dependency free).
// Writes coverage-report.json and prints a per-view summary. Exits 1 if any visible
// control on any view, dialog, menu, or captured screen has no teaching card.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const FILE = 'file://' + path.resolve(process.cwd(), 'dist/index.html');
const STRICT = !process.argv.includes('--report-only');

// Classifies every visible control under root.
//   taught        = explanationFor() returned a real teaching card
//   capture-note  = only the capture metadata fallback ("Read the recorded control...")
//   none          = nothing happens when clicked in Explain mode
const CLASSIFY = `(root)=>{
  const out=[];
  const els=[...root.querySelectorAll('button,input,select,summary,a,textarea,[role=button],[role=tab],[role=menuitem],[role=radio],[role=checkbox]')];
  for(const el of els){
    if(el.closest('#click-explanation,#walkthrough-box,.training-launcher,[data-audit-ignore]'))continue;
    const r=el.getBoundingClientRect(); if(!(r.width>0&&r.height>0))continue;
    let ctx=null; try{ctx=explanationFor(el)}catch(e){}
    let cls='none';
    if(ctx){const s=ctx.info?.steps?.[0]||''; cls=s.startsWith('Read the recorded control')?'capture-note':'taught';}
    const kind=el.tagName==='INPUT'?('input:'+(el.type||'text')):el.tagName.toLowerCase();
    const label=(el.dataset.label||el.getAttribute('aria-label')||el.closest('label')?.textContent||el.textContent||el.name||'').replace(/\\s+/g,' ').trim().slice(0,80);
    out.push({kind,label,name:el.name||'',action:el.dataset.action||'',helpId:el.dataset.help||'',disabled:!!el.disabled,cls});
  }
  return out;
}`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  await page.addInitScript(() => { try { sessionStorage.setItem('brightspace-support-unlocked', '1'); } catch (e) {} });
  await page.goto(FILE);
  await page.waitForTimeout(400);
  await page.evaluate(() => { state.explainClicks = true; });
  const meta = await page.evaluate(() => ({ routes: ROUTES, screens: CAPTURE.screens.map(s => s.id) }));
  const views = [];
  for (const r of meta.routes) views.push({ key: 'route:' + r, go: `navigate(${JSON.stringify(r)})` });
  for (const t of ['enter', 'manage', 'personal', 'display', 'calculation', 'wizard', 'schemes', 'finals'])
    views.push({ key: 'grades:' + t, go: `navigate('grades',${JSON.stringify(t)})` });
  for (const s of meta.screens) views.push({ key: 'capture:' + s, go: `openCapture(${JSON.stringify(s)})` });

  const results = {};
  for (const v of views) {
    await page.evaluate(`(()=>{const d=document.getElementById('dialog');if(d.open)d.close();${v.go}})()`);
    await page.waitForTimeout(60);
    results[v.key] = await page.evaluate(`(${CLASSIFY})(document.getElementById('main'))`);
    if (v.key.startsWith('capture:')) continue;
    // Open every dialog reachable from a button on this view and audit it too.
    const n = await page.evaluate(() => document.querySelectorAll('#main button[data-action]').length);
    for (let i = 0; i < n; i++) {
      await page.evaluate(v.go);
      const info = await page.evaluate(i => {
        const b = [...document.querySelectorAll('#main button[data-action]')][i];
        if (!b || b.disabled || /delete|reset|tour|walk/i.test(b.dataset.action)) return null;
        const was = state.explainClicks; state.explainClicks = false; b.click(); state.explainClicks = was;
        const d = document.getElementById('dialog');
        return d.open ? (d.querySelector('h1,h2')?.textContent || b.textContent).trim() : null;
      }, i);
      if (info && !results[`dialog:${v.key}:${info}`]) {
        results[`dialog:${v.key}:${info}`] = await page.evaluate(`(${CLASSIFY})(document.getElementById('dialog'))`);
        await page.evaluate(() => document.getElementById('dialog').close());
      }
    }
  }
  await browser.close();

  let total = 0, taught = 0, failing = [];
  for (const [k, items] of Object.entries(results)) {
    const t = items.filter(i => i.cls === 'taught').length;
    total += items.length; taught += t;
    console.log(`${k.padEnd(60)} ${String(t).padStart(4)}/${String(items.length).padEnd(4)} taught`);
    for (const i of items) if (i.cls !== 'taught') failing.push({ view: k, ...i });
  }
  fs.writeFileSync('coverage-report.json', JSON.stringify({ total, taught, failing, results }, null, 1));
  console.log(`\nTOTAL ${taught}/${total} controls taught (${(100 * taught / total).toFixed(1)}%). Untaught: ${failing.length}. Details in coverage-report.json`);
  if (STRICT && failing.length) process.exit(1);
})();
