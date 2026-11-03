'use strict';
const items=Object.freeze({
 a:{title:'A — Коридор свернулся',name:'Коридор свернулся',file:'./images/corridor-fold.png',width:1914,height:822},
 b:{title:'B — Тень не умеет воскресать',name:'Тень не умеет воскресать',file:'./images/aging-shadow.png',width:2172,height:724},
 c:{title:'C — Ниже линии удара',name:'Ниже линии удара',file:'./images/below-strike.png',width:2172,height:724}
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
function choose(key){
 const item=items[key];
 if(!item)return;
 image.src=item.file;
 image.alt='Sifu — '+item.name;
 link.href=item.file;
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
}
for(const tab of tabs){
 tab.addEventListener('click',()=>choose(tab.dataset.pick));
 tab.addEventListener('keydown',event=>{
  if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const keys=['a','b','c'];
  let next;
  if(event.key==='Home')next='a';
  else if(event.key==='End')next='c';
  else next=keys[(keys.indexOf(tab.dataset.pick)+(event.key==='ArrowRight'?1:2))%3];
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
