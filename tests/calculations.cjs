const fs=require('fs'),vm=require('vm'),assert=require('assert');
const code=fs.readFileSync(__dirname+'/../src/app.js','utf8');
const sample=code.slice(code.indexOf('function sampleCourse('),code.indexOf('function initialState('));
const calc=code.slice(code.indexOf('function calculate('),code.indexOf('function recalculate('));
const ctx={};vm.createContext(ctx);vm.runInContext(sample+`function gradeRecord(c,u,i){return c.grades[u]?.[i]||{score:null,exempt:false};}`+calc,ctx);
let count=0;
function test(name,mode,modify,expected){const c=ctx.sampleCourse('c','Test','TEST');c.settings.mode=mode;modify(c);const r=ctx.calculate(c,'u1');assert.equal(r.warnings.length,0,name+' unexpected limitation: '+r.warnings);if(expected===null)assert.equal(r.value,null,name);else assert.ok(Math.abs(r.value-expected)<1e-8,`${name}: ${r.value} != ${expected}`);count++;}
for(const mode of ['weighted','points']){
test('base '+mode,mode,c=>{},mode==='weighted'?82:104/120*100);
test('blank excluded '+mode,mode,c=>c.grades.u1.q2.score=null,mode==='weighted'?86:98/110*100);
test('blank zero '+mode,mode,c=>{c.grades.u1.q2.score=null;c.settings.blanks='zero';},mode==='weighted'?70:98/120*100);
test('actual zero '+mode,mode,c=>c.grades.u1.q2.score=0,mode==='weighted'?70:98/120*100);
test('exempt '+mode,mode,c=>{c.grades.u1.q2.exempt=true;c.settings.blanks='zero';},mode==='weighted'?86:98/110*100);
test('drop lowest '+mode,mode,c=>c.categories[0].dropLowest=1,mode==='weighted'?86:98/110*100);
test('whole category exempt '+mode,mode,c=>{c.grades.u1.q1.exempt=true;c.grades.u1.q2.exempt=true;},90);
test('all exempt '+mode,mode,c=>Object.values(c.grades.u1).forEach(g=>g.exempt=true),null);
test('all blank as zero '+mode,mode,c=>{Object.values(c.grades.u1).forEach(g=>g.score=null);c.settings.blanks='zero';},0);
test('hidden still counts '+mode,mode,c=>c.items[1].hidden=true,mode==='weighted'?82:104/120*100);
}
test('points bonus capped','points',c=>{c.categories=[];c.items=[{id:'p',max:100,weight:100,categoryId:null},{id:'b',max:10,weight:0,categoryId:null,bonus:true}];c.grades.u1={p:{score:95},b:{score:10}};},100);
test('points bonus exceed','points',c=>{c.categories=[];c.settings.finalCanExceed=true;c.items=[{id:'p',max:100,weight:100,categoryId:null},{id:'b',max:10,weight:0,categoryId:null,bonus:true}];c.grades.u1={p:{score:95},b:{score:10}};},105);
test('weighted course bonus','weighted',c=>{c.categories=[];c.items=[{id:'p',max:100,weight:100,categoryId:null},{id:'b',max:10,weight:4,categoryId:null,bonus:true}];c.grades.u1={p:{score:80},b:{score:5}};},82);
for(const exceed of [true,false])test('weighted category bonus '+exceed,'weighted',c=>{c.categories=[{id:'a',weight:50,canExceed:exceed,dropLowest:0}];c.items=[{id:'p',categoryId:'a',max:100,weight:100},{id:'b',categoryId:'a',max:10,weight:10,bonus:true},{id:'p2',categoryId:null,max:100,weight:50}];c.grades.u1={p:{score:100},b:{score:10},p2:{score:80}};},exceed?95:90);
const limited=ctx.sampleCourse('c','Test','TEST');limited.categories[0].dropLowest=1;limited.grades.u1.q2.score=null;assert.ok(ctx.calculate(limited,'u1').warnings.length);count++;
console.log(`${count} calculation checks passed, including blank/zero, exemptions, drops, hidden items, bonuses, caps, and unsupported-case reporting.`);
