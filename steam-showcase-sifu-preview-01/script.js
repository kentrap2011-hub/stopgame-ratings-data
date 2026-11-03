'use strict';
const items=Object.freeze({
 a:{title:'A — Коридор свернулся',name:'Коридор свернулся',file:'./images/corridor-fold.png',width:1914,height:822},
 b:{title:'B — Тень не умеет воскресать',name:'Тень не умеет воскресать',file:'./images/aging-shadow.png',width:2172,height:724},
 c:{title:'C — Ниже линии удара',name:'Ниже линии удара',file:'./images/below-strike.png',width:2172,height:724},
 d:{title:'D — Графит · контраст',name:'Графит · контраст',file:'./images/sifu-d-graphite.webp',original:'./images/sifu-d-full.webp',width:626,height:850},
 e:{title:'E — Алый · контраст',name:'Алый · контраст',file:'./images/sifu-e-ashen.webp',original:'./images/sifu-e-full.webp',width:626,height:850},
 f:{title:'F — Исходник 1 · Красный свет',name:'Исходник 1 · Красный свет',file:'./images/sifu-original-red-light.jpg',width:691,height:1536},
 g:{title:'G — Исходник 2 · Графика',name:'Исходник 2 · Графика',file:'./images/sifu-original-graphic.jpg',width:691,height:1536}
});
const image=document.getElementById('preview-image');
const title=document.getElementById('current-title');
const renderSize=document.getElementById('render-size');
const link=document.getElementById('full-link');
const panel=document.getElementById('showcase-panel');
const tabs=[...document.querySelectorAll('[data-pick]')];
const viewport=document.getElementById('scene-viewport');
const sizer=document.getElementById('scene-sizer');
const scene=document.getElementById('desktop-scene');
const zoomButton=document.getElementById('scale-mode');
let fullSize=false;
let activeKey='a';
const gradeCache=new Map();
const clamp=(x,lo=0,hi=1)=>Math.max(lo,Math.min(hi,x));

// Non-destructive browser colour grade: originals remain untouched on GitHub.
// This is a high-contrast black/white treatment with selective blood-red ink.
async function makeNoir(key,item){
 if(gradeCache.has(key))return gradeCache.get(key);
 const base=new Image();
 base.src=item.file;
 await base.decode();
 const canvas=document.createElement('canvas');
 canvas.width=item.width; canvas.height=item.height;
 const ctx=canvas.getContext('2d',{willReadFrequently:true});
 if(!ctx)throw new Error('Canvas 2D unavailable');
 ctx.drawImage(base,0,0,canvas.width,canvas.height);
 const frame=ctx.getImageData(0,0,canvas.width,canvas.height);
 const pixels=frame.data, w=canvas.width;
 const dmode=key==='d', mid=dmode?83:86, steep=dmode?19:18;
 for(let i=0;i<pixels.length;i+=4){
  const r=pixels[i],g=pixels[i+1],b=pixels[i+2];
  const px=(i/4)%w, py=Math.floor((i/4)/w);
  const lum=.23*r+.70*g+.07*b;
  const white=255/(1+Math.exp(-clamp((lum-mid)/steep,-15,15)));
  const redDominance=r-Math.max(g,b);
  let redMask=0;
  if(dmode){
   if(py<330)redMask=clamp((redDominance-22)/17)*clamp((r-65)/40);
   else if(py<650)redMask=clamp((redDominance-34)/20,0,.8)*clamp((r-75)/50);
  }else{
   if(py<210&&px>120&&px<520)redMask=clamp((redDominance-30)/27)*clamp((r-72)/35);
   else if(py>450)redMask=clamp((redDominance-26)/22,0,.8)*clamp((r-80)/40);
  }
  const rr=clamp(195+Math.max(0,redDominance)*1.5,0,255);
  pixels[i]=white*.96*(1-redMask)+rr*redMask;
  pixels[i+1]=white*.985*(1-redMask)+14*redMask;
  pixels[i+2]=white*(1-redMask)+24*redMask;
 }
 ctx.putImageData(frame,0,0);
 const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));
 if(!blob)throw new Error('PNG export failed');
 const url=URL.createObjectURL(blob);
 gradeCache.set(key,url);
 return url;
}
async function renderVariant(key,item){
 if(key!=='d'&&key!=='e')return;
 try{
  const url=await makeNoir(key,item);
  if(activeKey!==key)return;
  image.src=url;
  link.href=url;
  link.textContent='Открыть контрастный PNG';
  scaleScene();
 }catch(error){
  console.warn('Noir preview unavailable, using unchanged source',error);
 }
}
function choose(key){
 const item=items[key];
 if(!item)return;
 activeKey=key;
 image.src=item.file;
 image.alt='Sifu — '+item.name;
 link.href=item.original||item.file;
 link.textContent='Открыть оригинал';
 title.textContent=item.title;
 renderSize.textContent='Высота ≈ '+Math.round(626*item.height/item.width)+' px (по пропорциям PNG)';
 panel.setAttribute('aria-labelledby','tab-'+key);
 for(const tab of tabs){
  const active=tab.dataset.pick===key;
  tab.classList.toggle('active',active);
  tab.setAttribute('aria-selected',String(active));
  tab.tabIndex=active?0:-1;
 }
 if(window.history&&window.history.replaceState)window.history.replaceState(null,'','#'+key);
 renderVariant(key,item);
}
for(const tab of tabs){
 tab.addEventListener('click',()=>choose(tab.dataset.pick));
 tab.addEventListener('keydown',event=>{
  if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const keys=Object.keys(items);
  let next;
  if(event.key==='Home')next='a';
  else if(event.key==='End')next=keys[keys.length-1];
  else next=keys[(keys.indexOf(tab.dataset.pick)+(event.key==='ArrowRight'?1:keys.length-1))%keys.length];
  choose(next);
  document.getElementById('tab-'+next).focus();
 });
}
function scaleScene(){
 const scale=fullSize?1:Math.min(1,Math.max(.1,viewport.clientWidth/1200));
 scene.style.transform='scale('+scale+')';
 sizer.style.width=(1200*scale)+'px';
 sizer.style.height=(scene.offsetHeight*scale)+'px';
 zoomButton.setAttribute('aria-pressed',String(fullSize));
 zoomButton.textContent=fullSize?'Уместить по ширине':'Приблизить макет';
}
zoomButton.addEventListener('click',()=>{fullSize=!fullSize;scaleScene();viewport.scrollLeft=fullSize?Math.max(0,(1200-viewport.clientWidth)/2):0;});
window.addEventListener('resize',scaleScene,{passive:true});
window.addEventListener('load',scaleScene,{once:true});
image.addEventListener('load',scaleScene);
choose(items[window.location.hash.slice(1)]?window.location.hash.slice(1):'a');
scaleScene();
