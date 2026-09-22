const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root=__dirname+'/..',base=root+'/data/capture/';
const tour=JSON.parse(fs.readFileSync(base+'gradebook-lab-msu.tour.json'));
const inventory=JSON.parse(fs.readFileSync(base+'d2l-ui-inventory.json'));
const code=fs.readFileSync(root+'/src/capture.js','utf8');
const ctx={clone:x=>structuredClone(x),h:s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))};vm.createContext(ctx);vm.runInContext(code.slice(code.indexOf('function validateReplayTour('),code.indexOf('function replayPage(')),ctx);
ctx.validateReplayTour(tour);
for(const step of tour.steps){const html=ctx.renderReplayBlocks(ctx.resolveReplayScreen(tour,step.screen));assert.ok([step.target,'menu:'+step.target,'dialog:'+step.target].some(t=>html.includes('data-replay-label="'+ctx.h(t)+'"')),step.id+' missing target');}
const bads=[{}, {...tour,schema_version:9},{...tour,steps:[{screen:'missing',target:'x',card:'x'}]}, {...tour,screens:{x:{extends:'x'}},steps:[{screen:'x',target:'x',card:'x'}]},{...tour,screens:{x:{blocks:[{type:'script'}]}},steps:[{screen:'x',target:'x',card:'x'}]}];
for(const t of bads)assert.throws(()=>ctx.validateReplayTour(t));
assert.ok(!ctx.renderReplayBlocks([{type:'text',text:'<script>alert(1)</script>'}]).includes('<script>'));
const flows=JSON.parse(fs.readFileSync(root+'/data/workflows.json')),tickets=JSON.parse(fs.readFileSync(root+'/data/ticket-library.json')),help=JSON.parse(fs.readFileSync(root+'/data/tool-help.json'));
for(const t of tickets){if(t.tourId)assert.ok(flows.some(f=>f.id===t.tourId),t.id+' tour');if(t.screenId)assert.ok(inventory.screens.some(s=>s.id===t.screenId),t.id+' screen');if(t.tool)assert.ok(help[t.tool],t.id+' tool');}
vm.runInContext('const TICKETS='+JSON.stringify(tickets)+';'+fs.readFileSync(root+'/src/support.js','utf8').split("document.addEventListener")[0],ctx);
assert.equal(ctx.searchSupport('student cannot see final grade')[0].id,'grades-final-not-visible');
assert.ok(ctx.searchSupport('extra time for one quiz').some(t=>t.tourId==='quiz-special'));
console.log(tour.steps.length+' replay targets, 5 invalid tour cases, escaped text, '+tickets.length+' ticket references, and 2 ticket search examples passed.');
