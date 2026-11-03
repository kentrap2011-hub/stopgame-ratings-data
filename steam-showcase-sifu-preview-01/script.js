'use strict';
const items = Object.freeze({
  a: {title:'A — Коридор свернулся', name:'Коридор свернулся',file:'images/corridor-fold.png',width:1914,height:822},
  b: {title:'B — Тень не умеет воскресать', name:'Тень не умеет воскресать',file:'images/aging-shadow.png',width:2172,height:724},
  c: {title:'C — Ниже линии удара',name:'Ниже линии удара',file:'images/below-strike.png',width:2172,height:724}
});
const photo=document.getElementById('preview-image');
const title=document.getElementById('current-title');
const link=document.getElementById('full-link');
const tabs=[...document.querySelectorAll('[data-pick]')];
function choose(key){
  const item=items[key]; if(!item)return;
  photo.src=item.file; photo.width=item.width;photo.height=item.height;photo.alt='Sifu — '+item.name;
  title.textContent=item.title; link.href=item.file;
  for(const tab of tabs){const selected=tab.dataset.pick===key;tab.classList.toggle('active',selected);tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;}
  if(window.history && window.history.replaceState){window.history.replaceState(null,'','#'+key);}
}
for(const tab of tabs){tab.addEventListener('click',()=>choose(tab.dataset.pick));tab.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const keys=['a','b','c'];const index=keys.indexOf(tab.dataset.pick);let next=keys[(index+(e.key==='ArrowRight'?1:2))%3];choose(next);document.getElementById('tab-'+next).focus();});}
choose(items[window.location.hash.substring(1)]?window.location.hash.substring(1):'a');
