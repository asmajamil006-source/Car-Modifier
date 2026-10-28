const MODELS={
civic:{n:"Civic",b:"M58 262L60 212Q64 195 100 190L215 178Q270 112 380 106L500 106Q570 112 622 168L722 188Q748 196 750 226L750 262Z",g:"M262 172Q300 124 376 120L432 120L432 172ZM446 120L498 120Q548 126 590 172L446 172Z",w:[195,598],s:[100,192]},
city:{n:"City",b:"M62 262L62 208Q66 192 105 188L225 180Q268 114 360 108L495 108Q560 112 600 170L712 190Q744 198 746 228L746 262Z",g:"M270 174Q300 126 360 122L428 122L428 174ZM442 122L494 122Q540 128 578 174L442 174Z",w:[195,590],s:[106,190]},
accord:{n:"Accord",b:"M50 262L52 210Q58 194 100 188L215 176Q275 108 390 104L510 104Q585 110 635 166L725 186Q752 194 754 226L754 262Z",g:"M265 170Q305 120 388 118L440 118L440 170ZM454 118L508 118Q560 124 604 170L454 170Z",w:[190,605],s:[96,190]},
hrv:{n:"HR-V",b:"M62 262L62 190Q64 160 90 150L110 112Q116 100 140 100L470 100Q560 104 612 170L715 192Q745 200 748 228L748 262Z",g:"M150 112L300 112L300 168L130 168ZM312 112L470 112Q540 118 580 168L312 168Z",w:[200,590],s:[116,100]},
jazz:{n:"Jazz",b:"M70 262L70 190Q74 160 110 148L130 112Q140 102 170 102L440 102Q520 108 570 165L700 190Q736 198 738 228L738 262Z",g:"M148 114L290 114L290 166L128 166ZM302 114L440 114Q500 120 546 166L302 166Z",w:[195,580],s:[126,104]},
crv:{n:"CR-V",b:"M52 262L52 192Q54 160 84 150L104 108Q112 98 140 98L520 98Q590 102 632 165L722 190Q750 198 752 228L752 262Z",g:"M140 110L310 110L310 166L120 166ZM322 110L520 110Q574 114 606 166L322 166Z",w:[190,596],s:[110,100]},
brv:{n:"BR-V",b:"M54 262L54 196Q56 166 90 156L116 116Q124 104 152 104L540 104Q600 108 636 168L722 190Q748 198 750 228L750 262Z",g:"M150 116L290 116L290 168L128 168ZM302 116L408 116L408 168L302 168ZM420 116L538 116Q582 120 606 168L420 168Z",w:[192,598],s:[122,106]},
amaze:{n:"Amaze",b:"M66 262L66 214Q70 200 104 196L208 184Q258 118 360 112L480 112Q548 116 592 176L708 192Q740 200 742 230L742 262Z",g:"M258 178Q290 130 360 126L424 126L424 178ZM438 126L478 126Q528 132 566 178L438 178Z",w:[192,586],s:[108,194]},
brio:{n:"Brio",b:"M74 262L74 194Q78 166 112 154L132 118Q140 108 168 108L430 108Q505 114 552 170L700 192Q736 200 738 230L738 262Z",g:"M150 120L284 120L284 168L132 168ZM296 120L430 120Q486 126 528 168L296 168Z",w:[190,570],s:[128,110]}
};
const COL=[["White","#e9ecf1"],["Red","#d4152a"],["Black","#14161b"],["Blue","#2457c5"],["Gunmetal","#5b6270"],["Yellow","#f0b90b"],["Lime","#8bd13a"],["Orange","#f26a1b"]];
const O={
fin:[["Gloss",0],["Matte wrap",90],],kit:[["Stock",0],["Sport",85],["Aggressive",160]],spo:[["None",0],["Lip",15],["Ducktail",25],["GT wing",55]],
light:[["Stock",0],["LED white",35],["Ice blue",40],["Amber DRL",40]],rim:[["Stock 5-spoke",0],["Multi-spoke",120],["Mesh",160],["Turbine",190]],
rimc:[["Silver",0],["Black",0],["Gold",0],["Bronze",0]],size:[["16\u2033",0],["17\u2033",30],["18\u2033",60],["19\u2033",90]],
dash:[["Stock",0],["Carbon",30],["Wood",35],["Red",30]],seat:[["Fabric",0],["Black leather",85],["Red leather",95],["Tan leather",95],["Blue leather",95]],
steer:[["Stock",0],["Sport stitched",25],["Flat carbon",45]],amb:[["Off",0],["Red",15],["Blue",15],["Purple",15],["Green",15]],
eng:[["Stock",0],["Stage 1 intake + exhaust",90],["Stage 2 ECU tune",190],["Turbo kit",650]],gear:[["Stock",0],["Short shifter",22],["Close-ratio gears",140]]};
const LC=["#ffe9b0","#fff","#8fd8ff","#ffb347"],RC=["#c9ced6","#1a1c20","#d4a72c","#8b5a2b"],DC=["#2a2e36","#171a20","#6b4423","#7a1220"],SC=["#4a4f58","#16181d","#b01226","#b58a5a","#1f3f8a"],AC=[null,"#ff2a3d","#35b6ff","#b04dff","#3dff9a"];
COL.splice(0,8,["Platinum White Pearl","#eceff3"],["Rallye Red","#c3102a"],["Crystal Black Pearl","#0f1115"],["Aegean Blue","#1f4e9c"],["Modern Steel Metallic","#6a717d"],["Lunar Silver","#b9bec7"],["Meteoroid Gray","#42464f"],["Phoenix Orange","#e2571d"]);
Object.assign(O,{tint:[["Clear",0],["Light",8],["Dark",12],["Limo",15]],str:[["None",0],["White side stripe",20],["Black side stripe",20],["Red side stripe",25]],roof:[["Body colour",0],["Gloss black",45],["Carbon",120]],ug:[["Off",0],["Ice blue",25],["Red",25],["Purple",25],["Green",25]],cal:[["Red",0],["Yellow",12],["Blue",12],["Black",8]],scene:[["Studio",0],["Night city",0],["Sunset",0]]});
