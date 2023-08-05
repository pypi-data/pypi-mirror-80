/*! For license information please see chunk.ea3b9fab72f53a985207.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[173],{124:function(e){e.exports=JSON.parse('{"version":"5.5.55","parts":[{"file":"8f7750e029a6ef516f402ba2a18f770d535730f8"},{"start":"airp","file":"02d396c32a0838028ca9d3b77163bfc174dded67"},{"start":"application-e","file":"a3b90c7426c62b9ba0c903ee8499ea13e6d80390"},{"start":"bag","file":"931ef6eadb58a42752c76e0d9784f2d9893fe734"},{"start":"bell-ch","file":"99431a3dab8cc1ecbd6404326a3469023a04aa60"},{"start":"bowl-","file":"fe82f15d3b3d4ef76fc0df861c815f3b71571d0a"},{"start":"camera-ou","file":"f6da031d601a409af4fe7b862c9b1a8deacfd0c9"},{"start":"cash-usd-","file":"726046c723a50453af2dd599b65c07fe18f3f316"},{"start":"clipboard-check-multiple-","file":"5b628a66092f32694caca6d5b270d6f66825881a"},{"start":"cogs","file":"7c06349e47a105ff951b01d9727e6f6ccbfcc2d9"},{"start":"crosshairs-o","file":"e09a84b8762d7159f8be429777de522783716fcb"},{"start":"dice-d4","file":"51a5204002b9cb9cef6321d8f72ceb0d39a1f926"},{"start":"email-open-multiple-","file":"c0493b85640302e62061ff2356b912e554bc01e7"},{"start":"face-mask-","file":"f867c6738fc9438cf93415e9dc41faf5d6821e9e"},{"start":"file-sync-","file":"f9f4564f510950e3b9a8417fa0ae0198b284519c"},{"start":"folder-mo","file":"ed885efd3686085c617745e253ae2b6a8212e100"},{"start":"fun","file":"93815bf15911bdec529eae8508ba3d3a816149a5"},{"start":"google-k","file":"566ed4f9438f515ba9ceb2afa4d78d72cac38e1a"},{"start":"heart-c","file":"2413a098f909b54b47a4d07f1a4f8e4d41cc43c9"},{"start":"image-filter-center-focus-strong-","file":"6313b3e660bd71e875b8c57ee9c88a2688c04735"},{"start":"l","file":"a9b4de440880e5ea07ea9ec73fda61bf5df4f0cd"},{"start":"lit","file":"2cde0f2919ec2d5103b37dbe4c9b37be0bc9dd6e"},{"start":"microsoft-az","file":"5412abda0c1b32f0d660d704eedaed8fa477b6d1"},{"start":"music-accidental-f","file":"89efc5a3501973d24465220c43064c67d012a5ed"},{"start":"ord","file":"ef55c1695d3e36fcfa67094c7acfb9b56b191d27"},{"start":"phone-l","file":"ccc6d99bb8fb02cc6fc5c9dd27cbaa28070b0c30"},{"start":"progress-c","file":"1dbad43c24c5e811f44dfefa70dfd225f74c47e6"},{"start":"repeat-on","file":"c949a7296882b0b15d91e85626ae7e6e2c9f6875"},{"start":"seg","file":"ce1da38ae8627bfdb244817db929bf4251446058"},{"start":"silverware-v","file":"f4c36c6f418f73dda1aed0f633316eaa6cf41314"},{"start":"soy-sauce-","file":"36307bb3554e34044047bca76b5ff136b242a84d"},{"start":"table-c","file":"a7d2046ca64e34c8ebe63fdadf44ffd002de34c9"},{"start":"timeline-m","file":"0dbd004bc7a4765ffcc347d8e2e5458897bcbaa2"},{"start":"uf","file":"1cf75c1f12e44659f1a95b899cad59f5f1d9f07a"},{"start":"watch-vibrate-","file":"70d3b6c741d0d366074cf12cbde349a268c575f8"},{"start":"wifi-strength-3-","file":"94b094d25866125d4376b21042e0e513af0c618f"}]}')},138:function(e,t,i){"use strict";i(140);var r=i(0);i(111);const a=window;"customIconsets"in a||(a.customIconsets={});const n=a.customIconsets;const o=i(124);var s=i(63);const c=new s.a("hass-icon-db","mdi-icon-store"),l=["mdi","hass","hassio","hademo"];let d=[];var f=i(64),u=i(11);function p(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const w={scooter:{removeIn:"117",newName:"human-scooter"}},k={};Object(s.c)("_version",c).then(e=>{e?e!==o.version&&Object(s.b)(c).then(()=>Object(s.d)("_version",o.version,c)):Object(s.d)("_version",o.version,c)});const _=Object(f.a)(()=>(async e=>{const t=Object.keys(e),i=await Promise.all(Object.values(e));c._withIDBStore("readwrite",r=>{i.forEach((i,a)=>{Object.entries(i).forEach(([e,t])=>{r.put(t,e)}),delete e[t[a]]})})})(k),2e3),E={};!function(e,t,i,r){var a=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var n="static"===a?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!m(e))return i.push(e);var t=this.decorateElement(e,a);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],a=e.decorators,n=a.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,a[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var n=0;n<r.length;n++)a=r[n](a);var o=t((function(e){a.initializeInstanceElements(e,s.elements)}),i),s=a.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var a,n=e[r];if("method"===n.kind&&(a=t.find(i)))if(b(n.descriptor)||b(a.descriptor)){if(m(n)||m(a))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");a.descriptor=n.descriptor}else{if(m(n)){if(m(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");a.decorators=n.decorators}h(n,a)}else t.push(n)}return t}(o.d.map(p)),e);a.initializeClassElements(o.F,s.elements),a.runClassFinishers(o.F,s.finishers)}([Object(r.d)("ha-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(r.h)()],key:"icon",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_path",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_legacy",value:()=>!1},{kind:"method",key:"updated",value:function(e){e.has("icon")&&(this._path=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?r.f`<iron-icon .icon=${this.icon}></iron-icon>`:r.f`<ha-svg-icon
      .path=${this._path}
      .viewBox=${this._viewBox}
    ></ha-svg-icon>`:r.f``}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const[e,t]=this.icon.split(":",2);let i,r=t;if(!e||!r)return;if(!l.includes(e)){if(e in n){const t=n[e];return void(t&&this._setCustomPath(t(r)))}return void(this._legacy=!0)}if(this._legacy=!1,r in w){const t=w[r];let i;t.newName?(i=`Icon ${e}:${r} was renamed to ${e}:${t.newName}, please change your config, it will be removed in version ${t.removeIn}.`,r=t.newName):i=`Icon ${e}:${r} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${t.removeIn}.`,console.warn(i),Object(u.a)(this,"write_log",{level:"warning",message:i})}if(r in E)return void(this._path=E[r]);try{i=await(e=>new Promise((t,i)=>{if(d.push([e,t,i]),d.length>1)return;const r=[];c._withIDBStore("readonly",e=>{for(const[t,i]of d)r.push([i,e.get(t)]);d=[]}).then(()=>{for(const[e,t]of r)e(t.result)}).catch(()=>{for(const[,,e]of d)e();d=[]})}))(r)}catch(f){i=void 0}if(i)return this._path=i,void(E[r]=i);const a=(e=>{let t;for(const i of o.parts){if(void 0!==i.start&&e<i.start)break;t=i}return t.file})(r);if(a in k)return void this._setPath(k[a],r);const s=fetch(`/static/mdi/${a}.json`).then(e=>e.json());k[a]=s,this._setPath(s,r),_()}},{kind:"method",key:"_setCustomPath",value:async function(e){const t=await e;this._path=t.path,this._viewBox=t.viewBox}},{kind:"method",key:"_setPath",value:async function(e,t){const i=await e;this._path=i[t],E[t]=i[t]}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      :host {
        fill: currentcolor;
      }
    `}}]}}),r.a)},211:function(e,t,i){"use strict";i.d(t,"a",(function(){return a}));var r=i(235);const a=e=>void 0===e.attributes.friendly_name?Object(r.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},219:function(e,t,i){"use strict";var r=i(9);t.a=Object(r.a)(e=>class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}})},222:function(e,t,i){"use strict";i.d(t,"a",(function(){return a}));var r=i(155);const a=e=>Object(r.a)(e.entity_id)},226:function(e,t,i){"use strict";i.d(t,"a",(function(){return n}));var r=i(9),a=i(11);const n=Object(r.a)(e=>class extends e{fire(e,t,i){return i=i||{},Object(a.a)(i.node||this,e,t,i)}})},235:function(e,t,i){"use strict";i.d(t,"a",(function(){return r}));const r=e=>e.substr(e.indexOf(".")+1)},270:function(e,t,i){"use strict";i(48);var r=i(55);const a=document.createElement("template");a.setAttribute("style","display: none;"),a.innerHTML=`<dom-module id="ha-style">\n  <template>\n    <style>\n    ${r.c.cssText}\n    </style>\n  </template>\n</dom-module>`,document.head.appendChild(a.content)},299:function(e,t,i){"use strict";i(258);var r=i(4);i(32);class a extends(customElements.get("app-header-layout")){static get template(){return r.a`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",a)},350:function(e,t,i){"use strict";i.d(t,"b",(function(){return r})),i.d(t,"a",(function(){return a}));const r=async(e,t,r=!1)=>{if(!e.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const a=(await i.e(197).then(i.t.bind(null,433,7))).default;a.Icon.Default.imagePath="/static/images/leaflet/images/",r&&await i.e(198).then(i.t.bind(null,434,7));const o=a.map(e),s=document.createElement("link");s.setAttribute("href","/static/images/leaflet/leaflet.css"),s.setAttribute("rel","stylesheet"),e.parentNode.appendChild(s),o.setView([52.3731339,4.8903147],13);return[o,a,n(a,Boolean(t)).addTo(o)]},a=(e,t,i,r)=>(t.removeLayer(i),(i=n(e,r)).addTo(t),i),n=(e,t)=>e.tileLayer(`https://{s}.basemaps.cartocdn.com/${t?"dark_all":"light_all"}/{z}/{x}/{y}${e.Browser.retina?"@2x.png":".png"}`,{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})},351:function(e,t,i){"use strict";i.d(t,"b",(function(){return a})),i.d(t,"f",(function(){return n})),i.d(t,"g",(function(){return o})),i.d(t,"d",(function(){return s})),i.d(t,"a",(function(){return c})),i.d(t,"i",(function(){return l})),i.d(t,"c",(function(){return d})),i.d(t,"h",(function(){return u})),i.d(t,"e",(function(){return p}));var r=i(123);const a="#FF9800",n="#ff9800",o="#9b9b9b",s=e=>e.callWS({type:"zone/list"}),c=(e,t)=>e.callWS({type:"zone/create",...t}),l=(e,t,i)=>e.callWS({type:"zone/update",zone_id:t,...i}),d=(e,t)=>e.callWS({type:"zone/delete",zone_id:t});let f;const u=(e,t)=>{f=t,Object(r.a)(e,"/config/zone/new")},p=()=>{const e=f;return f=void 0,e}},453:function(e,t,i){"use strict";i(414);var r=i(4),a=i(32),n=i(226);class o extends(Object(n.a)(a.a)){static get template(){return r.a`
      <style include="iron-positioning"></style>
      <style>
        .marker {
          vertical-align: top;
          position: relative;
          display: block;
          margin: 0 auto;
          width: 2.5em;
          text-align: center;
          height: 2.5em;
          line-height: 2.5em;
          font-size: 1.5em;
          border-radius: 50%;
          border: 0.1em solid var(--ha-marker-color, var(--primary-color));
          color: rgb(76, 76, 76);
          background-color: white;
        }
        iron-image {
          border-radius: 50%;
        }
      </style>

      <div class="marker" style$="border-color:{{entityColor}}">
        <template is="dom-if" if="[[entityName]]">[[entityName]]</template>
        <template is="dom-if" if="[[entityPicture]]">
          <iron-image
            sizing="cover"
            class="fit"
            src="[[entityPicture]]"
          ></iron-image>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},entityId:{type:String,value:""},entityName:{type:String,value:null},entityPicture:{type:String,value:null},entityColor:{type:String,value:null}}}ready(){super.ready(),this.addEventListener("click",e=>this.badgeTap(e))}badgeTap(e){e.stopPropagation(),this.entityId&&this.fire("hass-more-info",{entityId:this.entityId})}}customElements.define("ha-entity-marker",o)},849:function(e,t,i){"use strict";i.r(t);i(190);var r=i(4),a=i(32),n=i(350),o=i(222),s=i(211),c=i(123),l=(i(138),i(161),i(351)),d=i(219);i(453),i(270),i(299);class f extends(Object(d.a)(a.a)){static get template(){return r.a`
      <style include="ha-style">
        #map {
          height: calc(100vh - 64px);
          width: 100%;
          z-index: 0;
          background: inherit;
        }

        .icon {
          color: var(--primary-text-color);
        }
      </style>

      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              hass="[[hass]]"
              narrow="[[narrow]]"
            ></ha-menu-button>
            <div main-title>[[localize('panel.map')]]</div>
            <template is="dom-if" if="[[computeShowEditZone(hass)]]">
              <ha-icon-button
                icon="hass:pencil"
                on-click="openZonesEditor"
              ></ha-icon-button>
            </template>
          </app-toolbar>
        </app-header>
        <div id="map"></div>
      </ha-app-layout>
    `}static get properties(){return{hass:{type:Object,observer:"drawEntities"},narrow:Boolean}}connectedCallback(){super.connectedCallback(),this.loadMap()}async loadMap(){this._darkMode=this.hass.themes.darkMode,[this._map,this.Leaflet,this._tileLayer]=await Object(n.b)(this.$.map,this._darkMode),this.drawEntities(this.hass),this._map.invalidateSize(),this.fitMap()}disconnectedCallback(){this._map&&this._map.remove()}computeShowEditZone(e){return e.user.is_admin}openZonesEditor(){Object(c.a)(this,"/config/zone")}fitMap(){let e;0===this._mapItems.length?this._map.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),14):(e=new this.Leaflet.latLngBounds(this._mapItems.map(e=>e.getLatLng())),this._map.fitBounds(e.pad(.5)))}drawEntities(e){const t=this._map;if(!t)return;this._darkMode!==this.hass.themes.darkMode&&(this._darkMode=this.hass.themes.darkMode,this._tileLayer=Object(n.a)(this.Leaflet,t,this._tileLayer,this.hass.themes.darkMode)),this._mapItems&&this._mapItems.forEach((function(e){e.remove()}));const i=this._mapItems=[];this._mapZones&&this._mapZones.forEach((function(e){e.remove()}));const r=this._mapZones=[];Object.keys(e.states).forEach(a=>{const n=e.states[a];if("home"===n.state||!("latitude"in n.attributes)||!("longitude"in n.attributes))return;const c=Object(s.a)(n);let d;if("zone"===Object(o.a)(n)){if(n.attributes.passive)return;let e="";if(n.attributes.icon){const t=document.createElement("ha-icon");t.setAttribute("icon",n.attributes.icon),e=t.outerHTML}else{const t=document.createElement("span");t.innerHTML=c,e=t.outerHTML}return d=this.Leaflet.divIcon({html:e,iconSize:[24,24],className:"icon"}),r.push(this.Leaflet.marker([n.attributes.latitude,n.attributes.longitude],{icon:d,interactive:!1,title:c}).addTo(t)),void r.push(this.Leaflet.circle([n.attributes.latitude,n.attributes.longitude],{interactive:!1,color:l.b,radius:n.attributes.radius}).addTo(t))}const f=n.attributes.entity_picture||"",u=c.split(" ").map((function(e){return e.substr(0,1)})).join("");d=this.Leaflet.divIcon({html:"<ha-entity-marker entity-id='"+n.entity_id+"' entity-name='"+u+"' entity-picture='"+f+"'></ha-entity-marker>",iconSize:[45,45],className:""}),i.push(this.Leaflet.marker([n.attributes.latitude,n.attributes.longitude],{icon:d,title:Object(s.a)(n)}).addTo(t)),n.attributes.gps_accuracy&&i.push(this.Leaflet.circle([n.attributes.latitude,n.attributes.longitude],{interactive:!1,color:"#0288D1",radius:n.attributes.gps_accuracy}).addTo(t))})}}customElements.define("ha-panel-map",f)}}]);
//# sourceMappingURL=chunk.ea3b9fab72f53a985207.js.map