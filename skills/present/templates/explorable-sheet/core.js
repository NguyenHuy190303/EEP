<script>
(function(){
  function el(id){return document.getElementById(id)}
  var TOK=["The","cache","keeps","keys","and","values","so","decode","never","redoes","the","past"];
  var N=TOK.length, PROMPT=4;
  var S={t:5,sub:0,cache:true};
  var SUB=[
    {k:"append",h:"Store the new row.",p:"One new row. Nothing above it moves.",
     hx:"Rebuild every row.",px:"All t rows again — identical to last step."},
    {k:"attend",h:"Read every row.",p:"The query reads all t rows. This read still grows."},
    {k:"emit",h:"Write one token.",p:"Token t + 1 appears. Next step, it is the new row."}
  ];
  function w(i,t){var x=Math.sin(i*2.3+t*1.7)*.5+.5; return .15+.85*x*x;}
  function cells(cls,seed){var s="";for(var j=0;j<8;j++){var o=.35+.65*(Math.sin(seed*3.1+j*1.3)*.5+.5);s+='<i class="c '+cls+'" style="opacity:'+o.toFixed(2)+'"></i>';}return s;}
  function render(){
    var t=S.t, sub=S.sub, x=SUB[sub], off=!S.cache, h="";
    var i,ws=[],sum=0; for(i=0;i<t;i++){ws[i]=w(i,t);sum+=ws[i];}
    for(i=0;i<N;i++){
      var st = i>=t ? "fut" : (i===t-1 ? "new" : "old");
      var tag="";
      if(st==="new") tag = sub===0 ? (off?"recomputed":"computed") : "cached";
      else if(st==="old") tag = (sub===0&&off) ? "recomputed" : "reused";
      var cls="row "+st+((sub===0&&off&&st!=="fut")?" redo":"")+(i<PROMPT?" pr":"");
      var wt = (sub===1&&st!=="fut") ? '<span class="wt"><i style="width:'+Math.min(100,ws[i]/sum*100*2.2).toFixed(1)+'%"></i></span>' : '<span class="wt"></span>';
      h+='<div class="'+cls+'"><span class="tk">'+String(i+1).padStart(2,"0")+' '+TOK[i]+'</span><span class="kv">'+cells("k",i)+'</span><span class="kv">'+cells("v",i+7)+'</span>'+wt+'<span class="tg">'+(st==="fut"?"":tag)+'</span></div>';
    }
    el("rows").innerHTML=h;
    var out=TOK.slice(0,t).join(" ");
    var nxt = t<N ? TOK[t] : "⏹";
    el("outline").innerHTML='<span class="o-l">Text so far</span> '+out+(sub===2?' <b class="o-n">'+nxt+'</b>':' <span class="o-c">▍</span>');
    el("side-eb").textContent="Step 0"+(sub+1)+" · "+x.k+(off?" · cache off":"");
    el("side-h").textContent=(off&&sub===0&&x.hx)?x.hx:x.h;
    el("side-p").textContent=(off&&sub===0&&x.px)?x.px:x.p;
    el("ctr-t").textContent="token t = "+t+" · “"+TOK[t-1]+"”";
    var now = off? t : 1, done = off? t*(t+1)/2 : t;
    el("c-now").textContent = now;
    el("c-sum").textContent = done;
    el("c-no").textContent = t*(t+1)/2;
    el("c-read").textContent = t;
    var M=N*(N+1)/2;
    el("w-on").style.width=(t/M*100).toFixed(1)+"%"; el("w-on-n").textContent=t;
    el("w-off").style.width=(t*(t+1)/2/M*100).toFixed(1)+"%"; el("w-off-n").textContent=t*(t+1)/2;
    el("mech").classList.toggle("off",off);
    el("pos").textContent="0"+(sub+1)+" / 03 · token "+t+" of "+N;
    el("next").textContent = sub<2 ? "Next: "+SUB[sub+1].k+" →" : (t<N ? "Next token →" : "Done");
    el("p-cache").textContent = off ? "Turn the cache back on" : "Turn the cache off";
    el("p-cache").setAttribute("aria-pressed", String(off));
    document.querySelectorAll(".tab").forEach(function(b){b.classList.toggle("on",+b.dataset.sub===sub)});
  }
  function step(d){ var k=S.t*3+S.sub+d; k=Math.max(3,Math.min(N*3+2,k)); S.t=Math.floor(k/3); S.sub=k%3; render(); }
  el("next").addEventListener("click",function(){step(1)});
  el("prev").addEventListener("click",function(){step(-1)});
  document.querySelectorAll(".tab").forEach(function(b){b.addEventListener("click",function(){S.sub=+b.dataset.sub;render();})});
  el("p-cache").addEventListener("click",function(){S.cache=!S.cache;S.sub=0;render();});
  el("p-end").addEventListener("click",function(){S.t=N;S.sub=1;render();});
  el("p-back").addEventListener("click",function(){S.t=Math.max(1,S.t-1);render();});
  el("p-reset").addEventListener("click",function(){S={t:5,sub:0,cache:true};render();});
  document.querySelectorAll(".q[data-go]").forEach(function(a){a.addEventListener("click",function(){
    if(a.dataset.go==="nocache"){S.cache=false;S.sub=0;S.t=8;} else {S.cache=true;S.sub=0;S.t=5;} render();})});

  /* change one thing */
  var GI=Math.pow(2,30), WT=8.03e9*2;
  var V={seq:13,kv:8,b:2};
  function fmt(b){ if(b>=GI) {var g=b/GI; return [g>=10?g.toFixed(0):g.toFixed(2),"GiB"];} return [(b/1048576).toFixed(0),"MiB"]; }
  function lx(b){ var lo=Math.log2(GI/16), hi=Math.log2(GI*64); return 40+(Math.log2(b)-lo)/(hi-lo)*680; }
  function plot(cur,base){
    var s="", ticks=[[GI/16,"1/16"],[GI/4,"1/4"],[GI,"1"],[GI*4,"4"],[GI*16,"16"],[GI*64,"64 GiB"]];
    s+='<line class="ax" x1="30" y1="70" x2="720" y2="70"/>';
    ticks.forEach(function(k){var x=lx(k[0]);s+='<line class="tk" x1="'+x+'" y1="66" x2="'+x+'" y2="74"/><text x="'+x+'" y="94" text-anchor="middle" font-size="12" class="m">'+k[1]+'</text>';});
    var xw=lx(WT); s+='<line class="wl" x1="'+xw+'" y1="34" x2="'+xw+'" y2="78"/><text x="'+(xw+6)+'" y="40" font-size="12" class="m wlt">weights 15.0 GiB</text>';
    var xb=lx(base), xc=lx(cur);
    if(Math.abs(xc-xb)>1) s+='<line class="cn" x1="'+xb+'" y1="70" x2="'+xc+'" y2="70"/>';
    s+='<circle class="db" cx="'+xb+'" cy="70" r="7"/>';
    if(Math.abs(xc-xb)>1) s+='<circle class="dc" cx="'+xc+'" cy="70" r="7"/>';
    var lb='base 1 GiB'; s+='<text x="'+xb+'" y="54" text-anchor="middle" font-size="13" class="dbl">'+lb+'</text>';
    if(Math.abs(xc-xb)>1){var f=fmt(cur); s+='<text x="'+xc+'" y="'+(xc>xw-40&&xc<xw+80?112:54)+'" text-anchor="middle" font-size="13" class="dcl">'+f[0]+' '+f[1]+'</text>';}
    el("plot").innerHTML=s;
  }
  function what(){
    var S2=Math.pow(2,V.seq), tok=2*32*V.kv*128*V.b, tot=tok*S2, base=2*32*8*128*2*8192;
    var f=fmt(tot); el("wi-v").textContent=f[0]; el("wi-u").textContent=f[1]+" per sequence";
    var r=tot/base;
    el("wi-d").textContent = r===1 ? "same as base" : (r>1? "×"+r+" relative to base" : "÷"+(1/r)+" relative to base");
    el("wi-d").className="delta "+(r>1?"up":r<1?"dn":"");
    var isBase=V.seq===13&&V.kv===8&&V.b===2;
    el("wi-lbl").textContent=(isBase?"Base · ":"Variant · ")+S2.toLocaleString("en-US")+" tok · "+V.kv+" KV · "+(V.b===2?"bf16":"fp8");
    el("wi-f").textContent="2 × 32 × "+V.kv+" × 128 × "+V.b+" B × "+S2.toLocaleString("en-US");
    plot(tot,base);
    document.querySelectorAll("#cmp > div").forEach(function(d){d.classList.toggle("on",+d.dataset.kv===V.kv)});
    document.querySelectorAll(".seg").forEach(function(g){g.querySelectorAll("button").forEach(function(b){b.classList.toggle("on",+b.dataset.v===V[g.dataset.k])})});
  }
  document.querySelectorAll(".seg button").forEach(function(b){b.addEventListener("click",function(){V[b.parentNode.dataset.k]=+b.dataset.v;what();})});
  document.querySelectorAll("[data-variant]").forEach(function(a){a.addEventListener("click",function(){V={seq:13,kv:32,b:2};what();})});

  /* toc + motion */
  var links=document.querySelectorAll(".toc a");
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle("on",a.getAttribute("href")==="#"+e.target.id)})}})},{rootMargin:"-30% 0px -60% 0px"});
    document.querySelectorAll(".sec").forEach(function(s){io.observe(s)});
  }
  el("motion").addEventListener("click",function(){var on=document.documentElement.classList.toggle("still");el("motion").textContent="Motion: "+(on?"off":"on");el("motion").setAttribute("aria-pressed",String(!on));});

  /* deep-link state, for screenshots and sharing: ?t=8&sub=1&cache=off&seq=17&kv=32&b=1 */
  var q=new URLSearchParams(location.search);
  if(q.get("t")) S.t=Math.max(1,Math.min(N,+q.get("t")));
  if(q.get("sub")) S.sub=Math.max(0,Math.min(2,+q.get("sub")));
  if(q.get("cache")==="off") S.cache=false;
  ["seq","kv","b"].forEach(function(k){if(q.get(k)) V[k]=+q.get(k);});
  if(q.has("still")) document.documentElement.classList.add("still");
  render(); what();
})();
</script>
