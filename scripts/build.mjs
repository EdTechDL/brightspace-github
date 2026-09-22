import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Script } from 'node:vm';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = name => readFileSync(resolve(root, name), 'utf8');
// Inline JSON must not terminate a script tag when future reference text contains HTML.
const json = name => JSON.stringify(JSON.parse(read(name))).replace(/</g, '\\u003c');
const prelude = [
  ['CAPTURE', 'data/capture/d2l-ui-inventory.json'],
  ['PACK_CASES', 'data/capture/calc-test-cases.json'],
  ['CAPTURE_TOUR', 'data/capture/gradebook-lab-msu.tour.json'],
  ['CAPTURE_GS', 'data/capture/gradescope-ui-inventory.json'],
  ['TOUR_GS', 'data/capture/gradescope-lti-handshake.tour.json'],
  ['TOOL_NOTES', 'data/tool-notes.json']
].map(([key, path]) => `const ${key}=${json(path)};`).join('\n');

// These extensions are ordered deliberately: later definitions replace prototype views.
const extensions = ['capture.js', 'grade-ui.js', 'experience.js']
  .map(name => read(`src/${name}`)).join('\n') +
  `\nconst TOOL_HELP=${json('data/tool-help.json')};\n${read('src/explain.js')}` +
  `\nconst TICKETS=${json('data/ticket-library.json')};\n${read('src/support.js')}`;
const entry = read('src/app.js');
const marker = 'render();\n\n// Optional WebMCP';
if (entry.split(marker).length !== 2) throw new Error('Expected exactly one extension insertion marker in src/app.js.');
// The gate runs last so the unlock handler binds after the app has rendered.
const script = `${prelude}\n${entry.replace(marker, () => `${extensions}\n${marker}`)}\n${read('src/gate.js')}`;
new Script(script, { filename: 'brightspace-bundle.js' });
if (/<\/script/i.test(script)) throw new Error('Escape a closing script tag before embedding JavaScript in HTML.');
let html = read('src/shell.html');
for (const [marker, value] of [
  ['/*APP_CSS*/', read('src/app.css')],
  ['/*APP_JS*/', script],
  ['/*WORKFLOWS*/', json('data/workflows.json')]
]) {
  if (html.split(marker).length !== 2) throw new Error(`Expected exactly one ${marker} marker.`);
  html = html.replace(marker, () => value);
}
mkdirSync(resolve(root, 'dist'), { recursive: true });
writeFileSync(resolve(root, 'dist/index.html'), html);
console.log(`Built dist/index.html (${Buffer.byteLength(html).toLocaleString()} bytes). No runtime dependencies.`);
