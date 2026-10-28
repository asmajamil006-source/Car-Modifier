const hx=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16));
const sh=(h,a)=>"#"+hx(h).map(v=>{v=a>0?v+(255-v)*a:v*(1+a);return Math.round(Math.max(0,Math.min(255,v))).toString(16).padStart(2,"0")}).join("");
const CAL=["#d4152a","#f0b90b","#2457c5","#2b2d33"],UG=[null,"#35b6ff","#ff2a3d","#b04dff","#3dff9a"];
function wheelP(cx,P){
 const rr=[30,33,36,39][P.size],c=RC[P.rimc],st=P.rim;let g="";
 if(st==0)for(let i=0;i<5;i++)g+=`<rect x="-5" y="${-rr+3}" width="10" height="${rr-3}" rx="3" transform="rotate(${i*72})"/>`;
 if(st==1)for(let i=0;i<10;i++)g+=`<rect x="-2" y="${-rr+3}" width="4" height="${rr-3}" rx="2" transform="rotate(${i*36})"/>`;
 if(st==2){for(let i=0;i<24;i++)g+=`<rect x="-1" y="${-rr+3}" width="2" height="${rr-3}" transform="rotate(${i*15})"/>`;g+=`<circle r="${rr*.55}" fill="none" stroke-width="2.5"/>`}
 if(st==3)for(let i=0;i<8;i++)g+=`<path d="M-3 0L-9 ${-rr+3}L8 ${-rr+3}Q6 ${-rr/2} 3 0Z" transform="rotate(${i*45})"/>`;
 return `<g transform="translate(${cx} 245)"><circle r="50" fill="#0e0f12" stroke="#25272d" stroke-width="2"/><circle r="47" fill="none" stroke="#1c1e23" stroke-width="3" stroke-dasharray="4 3"/><circle r="${rr+3}" fill="#17181c" stroke="#2c2f36" stroke-width="2"/><circle r="${rr-4}" fill="#7d838e" stroke="#444"/><circle r="${rr-4}" fill="none" stroke="${CAL[P.cal]}" stroke-width="8" stroke-dasharray="26 300" transform="rotate(-45)"/><g class="${P.spin?"w1":""}"><g fill="${c}" stroke="${c}"><circle r="${rr}" fill="none" stroke-width="4"/>${g}<circle r="7" fill="#22252b" stroke="none"/></g></g><circle r="${rr+1}" fill="none" stroke="#f1f4f9" opacity=".6"/></g>`}
function carSvg(P,u){
 const m=MODELS[P.model],base=COL[P.color][1],[x1,x2]=m.w,d=P.drop*.8,lc=LC[P.light],ni=P.scene==1,k=P.kit,sp=P.spo,[sx,sy]=m.s,suv=["hrv","jazz","crv","brv","brio"].includes(P.model),mt=P.fin==1,by=suv?168:173,col=base;
 const bg=[["#f1f3f8","#b7bfcc"],["#05070f","#14204a"],["#ffb070","#4a2a52"]][P.scene],fl=[["#d3d8e1","#9aa3b3"],["#0a1020","#04060b"],["#5a3550","#1f1228"]][P.scene];
 const a=mt?.1:.42,gl=["#7894ad","#324a62","#111c28","#06090e"][P.tint],ug=UG[P.ug];
 let spo="";
 if(sp==1)spo=`<path d="M${sx-30} ${sy+2}L${sx+14} ${sy-4}L${sx+16} ${sy+1}L${sx-26} ${sy+8}Z" fill="#14161b"/>`;
 if(sp==2)spo=`<path d="M${sx-36} ${sy+6}Q${sx-20} ${sy-10} ${sx+18} ${sy-6}L${sx+14} ${sy+2}Q${sx-12} ${sy} ${sx-30} ${sy+10}Z" fill="#14161b"/>`;
 if(sp==3)spo=`<rect x="${sx-4}" y="${sy-22}" width="5" height="24" fill="#14161b"/><rect x="${sx-34}" y="${sy-22}" width="5" height="24" fill="#14161b"/><rect x="${sx-44}" y="${sy-34}" width="72" height="9" rx="3" fill="#14161b" stroke="#555"/>`;
 const kit=k?`<rect x="${x1+58}" y="${k==2?248:252}" width="${x2-x1-116}" height="${k==2?15:11}" rx="4" fill="#14161b" stroke="${k==2?"#d4152a":"#444"}"/><path d="M690 262L752 262L758 272L698 274Z" fill="#14161b"/><path d="M54 262L112 262L108 273L50 271Z" fill="#14161b"/>`:"";
 const stc=["","#f4f4f4","#0d0e11","#d4152a"][P.str];
 const str=P.str?`<g clip-path="url(#${u}k)"><rect x="0" y="232" width="800" height="5" fill="${stc}"/><rect x="0" y="241" width="800" height="2" fill="${stc}"/></g>`:"";
 const roof=P.roof?`<g clip-path="url(#${u}k)"><rect x="0" y="90" width="800" height="32" fill="${P.roof==1?"#0c0d10":"#1b1e24"}"/>${P.roof==2?'<rect x="0" y="90" width="800" height="32" fill="url(#'+u+'cf)"/>':""}</g>`:"";
 const beam=(P.light||ni)?`<path d="M742 206L800 172L800 248Z" fill="${lc}" opacity="${ni?.42:.2}"/><circle cx="742" cy="208" r="${ni?46:30}" fill="${lc}" opacity=".3"/>`:"";
 const bok=ni?[80,190,330,470,640,740].map((x,i)=>`<circle cx="${x}" cy="${60+i*17%70}" r="${8+i*3}" fill="${["#35b6ff","#ff2a3d","#ffd35a"][i%3]}" opacity=".22"/>`).join(""):P.scene==2?`<circle cx="610" cy="150" r="70" fill="#fff2c9" opacity=".55"/>`:"";
 const car=`<g id="${u}c"><g transform="translate(0 ${d})"><circle cx="${x1}" cy="245" r="57" fill="#07080b"/><circle cx="${x2}" cy="245" r="57" fill="#07080b"/>
<g mask="url(#${u}m)"><path d="${m.b}" fill="url(#${u}p)"/>${roof}<g clip-path="url(#${u}k)"><rect x="0" y="200" width="800" height="22" fill="url(#${u}s)"/><rect x="0" y="252" width="800" height="12" fill="#000" opacity=".25"/></g>${str}
<path d="${m.g}" fill="${gl}"/><path d="${m.g}" fill="url(#${u}r)"/><path d="M${x1+60} ${by}L${x2-12} ${by}" stroke="#e4e8ef" stroke-width="2.5"/>
<path d="M437 124V262" stroke="#000" opacity=".4"/><path d="M437 124V262" stroke="#fff" opacity=".18" transform="translate(1.5 0)"/><rect x="460" y="184" width="28" height="5" rx="2" fill="#000" opacity=".45"/><rect x="340" y="184" width="28" height="5" rx="2" fill="#000" opacity=".35"/></g>
<ellipse cx="${x2+8}" cy="${by+2}" rx="14" ry="8" fill="${base}" stroke="#0006"/>
${spo}${kit}<path d="M${x1-57} 245A57 57 0 0 1 ${x1+57} 245M${x2-57} 245A57 57 0 0 1 ${x2+57} 245" fill="none" stroke="#0b0d11" stroke-width="5"/>
<path d="M690 199L738 205L734 219L694 214Z" fill="url(#${u}h)" stroke="#222"/><circle cx="712" cy="209" r="5" fill="#fff" opacity=".9"/><path d="M700 222L740 224" stroke="${P.light?lc:"#bbb"}" stroke-width="3"/><rect x="704" y="230" width="40" height="5" rx="2" fill="#0c0d10"/>
<rect x="${suv?70:58}" y="203" width="14" height="12" rx="3" fill="#e0182d" ${ni?'filter="url(#'+u+'bl)"':""}/><rect x="${suv?70:58}" y="203" width="14" height="12" rx="3" fill="#e0182d"/></g>${wheelP(x1,P)}${wheelP(x2,P)}</g>`;
 return `<svg viewBox="0 0 800 330" role="img" aria-label="${m.n} preview"><defs>
<linearGradient id="${u}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${bg[0]}"/><stop offset="1" stop-color="${bg[1]}"/></linearGradient>
<linearGradient id="${u}fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${fl[0]}"/><stop offset="1" stop-color="${fl[1]}"/></linearGradient>
<linearGradient id="${u}f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${fl[0]}" stop-opacity=".1"/><stop offset="1" stop-color="${fl[1]}"/></linearGradient>
<linearGradient id="${u}p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${sh(base,a)}"/><stop offset=".3" stop-color="${sh(base,a/3)}"/><stop offset=".62" stop-color="${base}"/><stop offset="1" stop-color="${sh(base,-a*1.3)}"/></linearGradient>
<linearGradient id="${u}s"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity="${mt?.05:.4}"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="${u}r" x1="0" y1="0" x2="1" y2="1"><stop offset=".25" stop-color="#fff" stop-opacity=".28"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset=".7" stop-color="#fff" stop-opacity=".12"/></linearGradient>
<radialGradient id="${u}h"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="${P.light?lc:"#e8dfbd"}"/></radialGradient>
<pattern id="${u}cf" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#15171c"/><path d="M0 0H3V3H0ZM3 3H6V6H3Z" fill="#2b2f38"/></pattern>
<clipPath id="${u}k"><path d="${m.b}"/></clipPath>
<mask id="${u}m"><rect width="800" height="340" fill="#fff"/><circle cx="${x1}" cy="245" r="57" fill="#000"/><circle cx="${x2}" cy="245" r="57" fill="#000"/></mask>
<filter id="${u}bl"><feGaussianBlur stdDeviation="7"/></filter></defs>
<rect width="800" height="296" fill="url(#${u}g)"/>${bok}<rect y="296" width="800" height="34" fill="url(#${u}fl)"/>
<g opacity=".2" transform="translate(0 592) scale(1 -1)"><use href="#${u}c"/></g><rect y="296" width="800" height="34" fill="url(#${u}f)"/>
${ug?`<ellipse cx="400" cy="298" rx="340" ry="16" fill="${ug}" opacity=".85" filter="url(#${u}bl)"/>`:""}<ellipse cx="400" cy="297" rx="350" ry="7" fill="#000" opacity=".5" filter="url(#${u}bl)"/>
${beam}${car}</svg>`}
function car(){
 if(!S.cmp)return carSvg(S,"a");
 return `<div style="position:relative">${carSvg({...D,model:S.model,scene:S.scene},"b")}<div id="top" style="position:absolute;inset:0;clip-path:inset(0 ${100-S.cmpPos}% 0 0)">${carSvg(S,"a")}</div><div id="ln" style="position:absolute;top:0;bottom:0;left:${S.cmpPos}%;width:3px;background:#fff;box-shadow:0 0 8px #000"></div><input type="range" id="cmpr" min="2" max="98" value="${S.cmpPos}" aria-label="Before and after slider" style="position:absolute;left:0;right:0;bottom:4px;width:100%"><div style="position:absolute;top:8px;left:10px;color:#fff;font-weight:700;text-shadow:0 1px 4px #000">Your build</div><div style="position:absolute;top:8px;right:10px;color:#fff;font-weight:700;text-shadow:0 1px 4px #000">Stock</div></div>`}
function inter(){
 const dc=DC[S.dash],sc=SC[S.seat],am=AC[S.amb],ste=["#15171c","#15171c","#2a2d34"][S.steer];
 const sp=[0,1,2].map(i=>`<line x1="290" y1="250" x2="${290+Math.cos((i*120+210)*Math.PI/180)*70}" y2="${250+Math.sin((i*120+210)*Math.PI/180)*70}" stroke="${ste}" stroke-width="10"/>`).join("");
 return `<svg viewBox="0 0 800 330" role="img" aria-label="Interior preview"><rect width="800" height="330" fill="#0d1320"/>
 <path d="M0 40Q400 -10 800 40L800 150L0 150Z" fill="#1a2740"/><path d="M0 150Q400 118 800 150L800 240L0 240Z" fill="${dc}"/>
 ${am?`<path d="M18 186Q400 160 782 186" stroke="${am}" stroke-width="4" fill="none"/><path d="M18 186Q400 160 782 186" stroke="${am}" stroke-width="14" fill="none" opacity=".25"/>`:""}
 <rect x="226" y="162" width="128" height="42" rx="10" fill="#06090f"/><circle cx="262" cy="183" r="15" fill="none" stroke="#6b7690" stroke-width="2"/><circle cx="318" cy="183" r="15" fill="none" stroke="#6b7690" stroke-width="2"/>
 <rect x="470" y="166" width="140" height="64" rx="8" fill="#05080d" stroke="#333"/><rect x="480" y="176" width="52" height="8" rx="3" fill="${am||"#3a4560"}"/><rect x="480" y="192" width="100" height="6" rx="3" fill="#222c42"/>
 <rect x="640" y="176" width="90" height="10" rx="4" fill="#0006"/><rect x="60" y="176" width="90" height="10" rx="4" fill="#0006"/>
 <rect x="388" y="262" width="64" height="68" rx="10" fill="#14161b"/><circle cx="420" cy="258" r="13" fill="${S.gear?"#c9ced6":"#2a2d34"}" stroke="#555"/>
 <rect x="10" y="226" width="130" height="104" rx="34" fill="${sc}" stroke="#0006" stroke-width="3"/><rect x="662" y="226" width="130" height="104" rx="34" fill="${sc}" stroke="#0006" stroke-width="3"/>
 <circle cx="290" cy="250" r="62" fill="none" stroke="${ste}" stroke-width="16"/>${S.steer==1?`<circle cx="290" cy="250" r="62" fill="none" stroke="#e0182d" stroke-width="2" stroke-dasharray="6 6"/>`:""}
 ${S.steer==2?`<rect x="220" y="280" width="140" height="40" fill="#0d1320"/>`:""}${sp}<circle cx="290" cy="250" r="14" fill="${ste}" stroke="#555"/></svg>`}

