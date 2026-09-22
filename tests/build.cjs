const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
execFileSync(process.execPath, [path.join(root, 'scripts/build.mjs')]);
const html = fs.readFileSync(path.join(root, 'dist/index.html'), 'utf8');
assert.ok(!/\/\*(APP_CSS|APP_JS|WORKFLOWS)\*\//.test(html), 'Unexpanded template marker');
assert.ok(!/<script[^>]+src=|<link[^>]+rel=["']stylesheet/i.test(html), 'Unexpected external dependency');
assert.equal((html.match(/<script\b/g) || []).length, 2, 'Unexpected script tag boundary');
const workflowText = html.match(/<script id="workflow-library" type="application\/json">([\s\S]*?)<\/script>/)[1];
assert.equal(JSON.parse(workflowText).length, 10);
const script = html.split('<script>')[1].split('</script>')[0];
new vm.Script(script);
for (const key of ['CAPTURE', 'PACK_CASES', 'CAPTURE_TOUR', 'TOOL_HELP', 'TICKETS']) {
  assert.ok(script.includes(`const ${key}=`), `Missing ${key}`);
}
console.log('Standalone HTML build, embedded JSON, and script syntax checks passed.');
