(this.webpackJsonpvide_viewer_fe=this.webpackJsonpvide_viewer_fe||[]).push([[0],{55:function(e,t,n){},57:function(e,t,n){},63:function(e,t,n){"use strict";n.r(t);var a=n(0),l=n.n(a),i=n(8),c=n.n(i),s=(n(55),n(30)),d=(n(56),n(57),window.location.protocol+"//"+window.location.hostname+":5000/api/"),r=n(97),o=n(4);function j(e){var t=e.stream;return Object(o.jsx)(r.a,{className:"d-flex",children:Object(o.jsx)("img",{className:"ms-auto me-auto",style:{height:"calc(100vh - 70px)"},src:t})})}var u=n(38),v=n.n(u),b=n(31),x=n(41),h=n(91),O=n(98),p=n(95),m=n(96);function f(e){var t=e.name,n=e.value;return Object(o.jsxs)("tr",{children:[Object(o.jsxs)("td",{className:"fw-bold",style:{width:"200px"},children:[t,":"]}),Object(o.jsx)("td",{className:"text-end",children:n})]})}function w(e){var t,n,l,i,c,r,j,u,w=Object(a.useState)(),y=Object(s.a)(w,2),g=y[0],N=y[1],_=e.options,z=e.onChangeOptions;function F(){return(F=Object(x.a)(v.a.mark((function e(){var t,n;return v.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch(d+"params");case 2:if(!(t=e.sent).ok){e.next=8;break}return e.next=6,t.json();case 6:n=e.sent,N(n);case 8:case"end":return e.stop()}}),e)})))).apply(this,arguments)}return Object(a.useEffect)((function(){var e=setInterval((function(){!function(){F.apply(this,arguments)}()}),5e3);return function(){return clearInterval(e)}}),[e]),console.log("opt",_),Object(o.jsxs)("div",{className:"w-auto me-2",children:[Object(o.jsxs)("div",{className:"border p-2",children:[Object(o.jsxs)(h.a,{className:"m-2 w-100",variant:"standard",sx:{m:1,minWidth:120},children:[Object(o.jsx)(O.a,{id:"type-label",children:"\u0422\u0438\u043f"}),Object(o.jsxs)(p.a,{labelId:"type-label",id:"type-select",value:null===_||void 0===_?void 0:_.type,label:"\u0422\u0438\u043f",variant:"standard",sx:{width:400},onChange:function(e){return null===z||void 0===z?void 0:z(Object(b.a)(Object(b.a)({},_),{},{type:e.target.value}))},children:[Object(o.jsx)(m.a,{value:"raw",children:"raw"}),Object(o.jsx)(m.a,{value:"detected",children:"detected"})]})]}),Object(o.jsxs)(h.a,{className:"m-2 w-100",variant:"standard",sx:{m:1,minWidth:120},children:[Object(o.jsx)(O.a,{id:"size-label",children:"\u0420\u0430\u0437\u043c\u0435\u0440"}),Object(o.jsxs)(p.a,{labelId:"size-label",id:"size-select",value:null===_||void 0===_?void 0:_.size,label:"\u0420\u0430\u0437\u043c\u0435\u0440",variant:"standard",sx:{width:400},onChange:function(e){return null===z||void 0===z?void 0:z(Object(b.a)(Object(b.a)({},_),{},{size:e.target.value}))},children:[Object(o.jsx)(m.a,{value:"1080",children:"1080p"}),Object(o.jsx)(m.a,{value:"720",children:"720p"}),Object(o.jsx)(m.a,{value:"540",children:"540p"}),Object(o.jsx)(m.a,{value:"480",children:"480p"}),Object(o.jsx)(m.a,{value:"360",children:"360p"})]})]})]}),Object(o.jsx)("div",{className:"border p-2",children:Object(o.jsx)("table",{children:Object(o.jsxs)("tbody",{children:[Object(o.jsx)(f,{name:"read fps",value:null===g||void 0===g||null===(t=g.read_fps)||void 0===t||null===(n=t.toFixed)||void 0===n?void 0:n.call(t,3)}),Object(o.jsx)(f,{name:"detect fps",value:null===g||void 0===g||null===(l=g.detect_fps)||void 0===l||null===(i=l.toFixed)||void 0===i?void 0:i.call(l,3)}),Object(o.jsx)(f,{name:"yolo time",value:null===g||void 0===g||null===(c=g.yolo_time)||void 0===c||null===(r=c.toFixed)||void 0===r?void 0:r.call(c,3)}),Object(o.jsx)(f,{name:"DeepSort time",value:null===g||void 0===g||null===(j=g.deep_sort_time)||void 0===j||null===(u=j.toFixed)||void 0===u?void 0:u.call(j,3)})]})})})]})}var y=function(e){var t=Object(a.useState)(0),n=Object(s.a)(t,2),l=(n[0],n[1],Object(a.useState)({size:"1080",type:"detected"})),i=Object(s.a)(l,2),c=i[0],r=i[1];return Object(o.jsx)("div",{children:Object(o.jsxs)("div",{className:"d-flex mt-2",children:[Object(o.jsx)(j,{stream:d+"stream?type="+(null===c||void 0===c?void 0:c.type)+"&size="+(null===c||void 0===c?void 0:c.size)}),Object(o.jsx)(w,{options:c,onChangeOptions:function(e){return r(e)}})]})})},g=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,100)).then((function(t){var n=t.getCLS,a=t.getFID,l=t.getFCP,i=t.getLCP,c=t.getTTFB;n(e),a(e),l(e),i(e),c(e)}))};c.a.render(Object(o.jsx)(l.a.StrictMode,{children:Object(o.jsx)(y,{})}),document.getElementById("root")),g()}},[[63,1,2]]]);
//# sourceMappingURL=main.a5cf68be.chunk.js.map