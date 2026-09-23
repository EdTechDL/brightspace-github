const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root=__dirname+'/..',base=root+'/data/capture/';
const tour=JSON.parse(fs.readFileSync(base+'gradebook-lab-msu.tour.json'));
const gsTour=JSON.parse(fs.readFileSync(base+'gradescope-lti-handshake.tour.json'));
const inventory=JSON.parse(fs.readFileSync(base+'d2l-ui-inventory.json'));
const gsInventory=JSON.parse(fs.readFileSync(base+'gradescope-ui-inventory.json'));
const code=fs.readFileSync(root+'/src/capture.js','utf8');
const ctx={clone:x=>structuredClone(x),h:s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))};vm.createContext(ctx);vm.runInContext(code.slice(code.indexOf('function validateReplayTour('),code.indexOf('function replayPage(')),ctx);
ctx.validateReplayTour(tour);
for(const step of tour.steps){const html=ctx.renderReplayBlocks(ctx.resolveReplayScreen(tour,step.screen));assert.ok([step.target,'menu:'+step.target,'dialog:'+step.target].some(t=>html.includes('data-replay-label="'+ctx.h(t)+'"')),step.id+' missing target');}
// Every embedded tour must validate and resolve each target, not just the D2L one.
ctx.validateReplayTour(gsTour);
for(const step of gsTour.steps){const html=ctx.renderReplayBlocks(ctx.resolveReplayScreen(gsTour,step.screen));assert.ok([step.target,'menu:'+step.target,'dialog:'+step.target].some(t=>html.includes('data-replay-label="'+ctx.h(t)+'"')),step.id+' missing target');}
// The library picker assumes both inventories share the D2L schema.
assert.equal(gsInventory.schema_version,inventory.schema_version);
for(const s of gsInventory.screens)for(const k of ['id','title','route','controls','transitions','unobserved','notes','page_text'])assert.ok(k in s,s.id+' missing '+k);
// dialogs and menus are optional in supplied packs; normalizeInventory fills them, so the renderer must never see a bare screen.
const normalize=d=>d.screens.map(s=>({controls:[],dialogs:[],menus:[],transitions:[],notes:[],unobserved:[],...s}));
for(const s of normalize(gsInventory))for(const k of ['controls','dialogs','menus','transitions','notes','unobserved'])assert.ok(Array.isArray(s[k]),s.id+' '+k+' not an array after normalize');
const ids=new Set(inventory.screens.map(s=>s.id));
for(const s of gsInventory.screens)assert.ok(!ids.has(s.id),'screen id collides across libraries: '+s.id);
assert.notEqual(tour.tour_id,gsTour.tour_id);
// A transition must never point at a screen the library cannot open.
for(const inv of [inventory,gsInventory]){const has=new Set(inv.screens.map(s=>s.id));
 for(const s of inv.screens)for(const t of s.transitions||[])if(t.result_screen_id)assert.ok(has.has(t.result_screen_id),s.id+' -> unknown screen '+t.result_screen_id);}
// Researched notes must hang off controls that really exist, and never replace observed data.
const toolNotes=JSON.parse(fs.readFileSync(root+'/data/tool-notes.json'));
assert.equal(toolNotes.evidence,'web-research');
assert.ok(toolNotes.disclaimer&&toolNotes.compiled,'notes need a disclaimer and a compiled date');
let noteCount=0;
for(const [screenId,notes] of Object.entries(toolNotes.notes)){
 const screen=[...inventory.screens,...gsInventory.screens].find(s=>s.id===screenId);
 assert.ok(screen,'tool note for unknown screen '+screenId);
 const labels=new Set(screen.controls.map(c=>c.label));
 for(const n of notes){
  noteCount++;
  assert.ok(labels.has(n.label),screenId+': no control labelled '+n.label);
  assert.ok(/^https?:\/\//.test(n.url),n.label+' needs an http(s) source url');
  assert.ok(n.what&&n.what.length>40,n.label+' needs a real description');
  assert.ok(!(screen.unobserved||[]).includes(n.what),n.label+' must not overwrite an observed gap');
 }}
// Every Course Admin link must reach a practice route or a captured screen.
const courseAdmin=inventory.screens.find(s=>s.id==='course-admin');
const dests=Object.fromEntries((courseAdmin.transitions||[]).filter(t=>t.result_screen_id).map(t=>[t.control,t.result_screen_id]));
const practice=new Set(['Assignments','Grades','Quizzes','Classlist','Content','Course Offering Information']);
const linkLabels=courseAdmin.controls.filter(c=>c.kind==='link').map(c=>c.label);
assert.ok(linkLabels.length>40,'expected the full Course Admin directory');
const deadEnds=linkLabels.filter(l=>!practice.has(l)&&!dests[l]);
assert.deepEqual(deadEnds,[],'Course Admin dead ends: '+deadEnds.join(', '));
// The help registry is the teaching content; a malformed card is worse than a visible gap.
const helpDir=root+'/data/help';
const HELP={};
for(const file of fs.readdirSync(helpDir).filter(f=>f.endsWith('.json')&&!f.startsWith('_'))){
 const cards=JSON.parse(fs.readFileSync(helpDir+'/'+file));
 for(const [id,card] of Object.entries(cards)){
  assert.ok(!HELP[id],'duplicate help id '+id);
  HELP[id]=card;
  assert.ok(/^[a-z0-9.-]+$/.test(id),'help id must be a slug: '+id);
  assert.ok(card.title&&card.title.length>2,id+' missing title');
  for(const field of ['where','what','when','verify'])assert.ok(card[field]&&card[field].length>10,id+' missing '+field);
  assert.ok(Array.isArray(card.howTo)&&card.howTo.length,id+' needs howTo steps');
  assert.ok(['captured','documented','simulated'].includes(card.evidence),id+' needs an evidence level');
  if(card.source)assert.ok(/^https?:\/\//.test(card.source),id+' source must be a url');
  for(const o of card.options||[])assert.ok(o.label&&o.effect,id+' option needs label and effect');
 }}
for(const [id,card] of Object.entries(HELP))
 for(const r of card.related||[])assert.ok(HELP[r],id+' points at unknown related card '+r);
const helpCount=Object.keys(HELP).length;
// An alias must point at a scope that actually has cards, or captured screens silently lose them.
const aliases=JSON.parse(fs.readFileSync(helpDir+'/_aliases.json'));
const screenIds=new Set(inventory.screens.map(s=>s.id));
const scopes=new Set(Object.keys(HELP).map(id=>id.split('.').slice(0,2).join('.')));
for(const [screen,scope] of Object.entries(aliases)){
 if(screen==='_comment')continue;
 assert.ok(screenIds.has(screen),'alias for unknown screen '+screen);
 assert.ok(scopes.has(scope),'alias '+screen+' points at scope '+scope+' which has no cards');
}
const bads=[{}, {...tour,schema_version:9},{...tour,steps:[{screen:'missing',target:'x',card:'x'}]}, {...tour,screens:{x:{extends:'x'}},steps:[{screen:'x',target:'x',card:'x'}]},{...tour,screens:{x:{blocks:[{type:'script'}]}},steps:[{screen:'x',target:'x',card:'x'}]}];
for(const t of bads)assert.throws(()=>ctx.validateReplayTour(t));
assert.ok(!ctx.renderReplayBlocks([{type:'text',text:'<script>alert(1)</script>'}]).includes('<script>'));
const flows=JSON.parse(fs.readFileSync(root+'/data/workflows.json')),tickets=JSON.parse(fs.readFileSync(root+'/data/ticket-library.json')),help=JSON.parse(fs.readFileSync(root+'/data/tool-help.json'));
for(const t of tickets){if(t.tourId)assert.ok(flows.some(f=>f.id===t.tourId),t.id+' tour');if(t.screenId)assert.ok(inventory.screens.some(s=>s.id===t.screenId),t.id+' screen');if(t.tool)assert.ok(help[t.tool],t.id+' tool');}
vm.runInContext('const TICKETS='+JSON.stringify(tickets)+';'+fs.readFileSync(root+'/src/support.js','utf8').split("document.addEventListener")[0],ctx);
assert.equal(ctx.searchSupport('student cannot see final grade')[0].id,'grades-final-not-visible');
assert.ok(ctx.searchSupport('extra time for one quiz').some(t=>t.tourId==='quiz-special'));
console.log((tour.steps.length+gsTour.steps.length)+' replay targets across '+2+' tours, '+noteCount+' researched tool notes, '+linkLabels.length+' Course Admin links with destinations, '+helpCount+' help cards, '+gsInventory.screens.length+' Gradescope screens, 5 invalid tour cases, escaped text, '+tickets.length+' ticket references, and 2 ticket search examples passed.');
