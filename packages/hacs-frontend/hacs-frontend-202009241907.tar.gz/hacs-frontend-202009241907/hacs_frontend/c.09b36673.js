import{P as e,q as t,r as i,t as n,_ as o,L as s,p as r,n as a,h as c,u as h,g as l,c as d}from"./c.9b7ee8e9.js";function u(e){const t=e.language||"en";return e.translationMetadata.translations[t]&&e.translationMetadata.translations[t].isRTL||!1}function p(e){return u(e)?"rtl":"ltr"}class y{constructor(e){y[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return y.types[e]&&y.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=y.types[t]=y.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=y.types[this.type];return e?Object.keys(e).map((function(e){return v[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}y[" "]=function(){},y.types={};var v=y.types;e({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var n=new y({type:e,key:t});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new y({type:this.type,key:e}).value}}),e({_template:t`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:i.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&n(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,n(this.root).appendChild(this._img))}});const m=window;"customIconsets"in m||(m.customIconsets={});const _=m.customIconsets;const f={version:"0",parts:[]};class g{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise((i,n)=>{const o=indexedDB.open(e,1);o.onerror=()=>n(o.error),o.onsuccess=()=>i(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(t)}})}_withIDBStore(e,t){return this._dbp.then(i=>new Promise((n,o)=>{const s=i.transaction(this.storeName,e);s.oncomplete=()=>n(),s.onabort=s.onerror=()=>o(s.error),t(s.objectStore(this.storeName))}))}}let k;function w(){return k||(k=new g),k}function b(e,t,i=w()){return i._withIDBStore("readwrite",i=>{i.put(t,e)})}const I=new g("hass-icon-db","mdi-icon-store"),S=["mdi","hass","hassio","hademo"];let x=[];const B={scooter:{removeIn:"117",newName:"human-scooter"}},$={};(function(e,t=w()){let i;return t._withIDBStore("readonly",t=>{i=t.get(e)}).then(()=>i.result)})("_version",I).then(e=>{e?e!==f.version&&function(e=w()){return e._withIDBStore("readwrite",e=>{e.clear()})}(I).then(()=>b("_version",f.version,I)):b("_version",f.version,I)});const N=((e,t,i=!1)=>{let n;return function(...o){const s=this,r=i&&!n;clearTimeout(n),n=setTimeout(()=>{n=null,i||e.apply(s,o)},t),r&&e.apply(s,o)}})(()=>(async e=>{const t=Object.keys(e),i=await Promise.all(Object.values(e));I._withIDBStore("readwrite",n=>{i.forEach((i,o)=>{Object.entries(i).forEach(([e,t])=>{n.put(t,e)}),delete e[t[o]]})})})($),2e3),C={};o([d("ha-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[r()],key:"icon",value:void 0},{kind:"field",decorators:[a()],key:"_path",value:void 0},{kind:"field",decorators:[a()],key:"_viewBox",value:void 0},{kind:"field",decorators:[a()],key:"_legacy",value:()=>!1},{kind:"method",key:"updated",value:function(e){e.has("icon")&&(this._path=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?c`<iron-icon .icon=${this.icon}></iron-icon>`:c`<ha-svg-icon
      .path=${this._path}
      .viewBox=${this._viewBox}
    ></ha-svg-icon>`:c``}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const[e,t]=this.icon.split(":",2);let i,n=t;if(!e||!n)return;if(!S.includes(e)){if(e in _){const t=_[e];return void(t&&this._setCustomPath(t(n)))}return void(this._legacy=!0)}if(this._legacy=!1,n in B){const t=B[n];let i;t.newName?(i=`Icon ${e}:${n} was renamed to ${e}:${t.newName}, please change your config, it will be removed in version ${t.removeIn}.`,n=t.newName):i=`Icon ${e}:${n} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${t.removeIn}.`,console.warn(i),h(this,"write_log",{level:"warning",message:i})}if(n in C)return void(this._path=C[n]);try{i=await(e=>new Promise((t,i)=>{if(x.push([e,t,i]),x.length>1)return;const n=[];I._withIDBStore("readonly",e=>{for(const[t,i]of x)n.push([i,e.get(t)]);x=[]}).then(()=>{for(const[e,t]of n)e(t.result)}).catch(()=>{for(const[,,e]of x)e();x=[]})}))(n)}catch(e){i=void 0}if(i)return this._path=i,void(C[n]=i);const o=(e=>{let t;for(const i of f.parts){if(void 0!==i.start&&e<i.start)break;t=i}return t.file})(n);if(o in $)return void this._setPath($[o],n);const s=fetch(`/static/mdi/${o}.json`).then(e=>e.json());$[o]=s,this._setPath(s,n),N()}},{kind:"method",key:"_setCustomPath",value:async function(e){const t=await e;this._path=t.path,this._viewBox=t.viewBox}},{kind:"method",key:"_setPath",value:async function(e,t){const i=await e;this._path=i[t],C[t]=i[t]}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        fill: currentcolor;
      }
    `}}]}}),s),o([d("ha-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[r({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[r({type:String})],key:"icon",value:()=>""},{kind:"field",decorators:[r({type:String})],key:"label",value:()=>""},{kind:"method",key:"createRenderRoot",value:function(){return this.attachShadow({mode:"open",delegatesFocus:!0})}},{kind:"method",key:"render",value:function(){return c`
      <mwc-icon-button .label=${this.label} .disabled=${this.disabled}>
        <ha-icon .icon=${this.icon}></ha-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),s),o([d("hacs-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[r({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[r({type:String})],key:"icon",value:()=>""},{kind:"method",key:"createRenderRoot",value:function(){return this.attachShadow({mode:"open",delegatesFocus:!0})}},{kind:"method",key:"render",value:function(){return c`
      <mwc-icon-button .disabled=${this.disabled}>
        <ha-svg-icon .path=${this.icon}></ha-svg-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-svg-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),s);export{y as I,u as a,p as c};
