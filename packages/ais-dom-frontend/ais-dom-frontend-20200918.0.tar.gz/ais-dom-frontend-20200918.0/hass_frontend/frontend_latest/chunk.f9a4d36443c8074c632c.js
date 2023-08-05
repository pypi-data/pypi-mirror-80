/*! For license information please see chunk.f9a4d36443c8074c632c.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[187],{163:function(e,t,r){"use strict";r(5);var a=r(68),o=r(69);const i={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},c=[a.a,o.a,i];var n=r(103),l=r(126);r.d(t,"a",(function(){return p}));const s={_checkedChanged:function(){i._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){l.a._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},p=[n.a,c,s]},165:function(e,t,r){"use strict";r(5),r(52);var a=r(163),o=r(103),i=r(6),c=r(4),n=r(71);const l=c.a`<style>
  :host {
    display: inline-block;
    white-space: nowrap;
    cursor: pointer;
    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);
    /* -1px is a sentinel for the default and is replaced in \`attached\`. */
    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);
    @apply --paper-font-common-base;
    line-height: 0;
    -webkit-tap-highlight-color: transparent;
  }

  :host([hidden]) {
    display: none !important;
  }

  :host(:focus) {
    outline: none;
  }

  .hidden {
    display: none;
  }

  #checkboxContainer {
    display: inline-block;
    position: relative;
    width: var(--calculated-paper-checkbox-size);
    height: var(--calculated-paper-checkbox-size);
    min-width: var(--calculated-paper-checkbox-size);
    margin: var(--paper-checkbox-margin, initial);
    vertical-align: var(--paper-checkbox-vertical-align, middle);
    background-color: var(--paper-checkbox-unchecked-background-color, transparent);
  }

  #ink {
    position: absolute;

    /* Center the ripple in the checkbox by negative offsetting it by
     * (inkWidth - rippleWidth) / 2 */
    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    width: var(--calculated-paper-checkbox-ink-size);
    height: var(--calculated-paper-checkbox-ink-size);
    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
  }

  #ink:dir(rtl) {
    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: auto;
  }

  #ink[checked] {
    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));
  }

  #checkbox {
    position: relative;
    box-sizing: border-box;
    height: 100%;
    border: solid 2px;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    border-radius: 2px;
    pointer-events: none;
    -webkit-transition: background-color 140ms, border-color 140ms;
    transition: background-color 140ms, border-color 140ms;

    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);
    transition-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  /* checkbox checked animations */
  #checkbox.checked #checkmark {
    -webkit-animation: checkmark-expand 140ms ease-out forwards;
    animation: checkmark-expand 140ms ease-out forwards;

    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);
    animation-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  @-webkit-keyframes checkmark-expand {
    0% {
      -webkit-transform: scale(0, 0) rotate(45deg);
    }
    100% {
      -webkit-transform: scale(1, 1) rotate(45deg);
    }
  }

  @keyframes checkmark-expand {
    0% {
      transform: scale(0, 0) rotate(45deg);
    }
    100% {
      transform: scale(1, 1) rotate(45deg);
    }
  }

  #checkbox.checked {
    background-color: var(--paper-checkbox-checked-color, var(--primary-color));
    border-color: var(--paper-checkbox-checked-color, var(--primary-color));
  }

  #checkmark {
    position: absolute;
    width: 36%;
    height: 70%;
    border-style: solid;
    border-top: none;
    border-left: none;
    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-color: var(--paper-checkbox-checkmark-color, white);
    -webkit-transform-origin: 97% 86%;
    transform-origin: 97% 86%;
    box-sizing: content-box; /* protect against page-level box-sizing */
  }

  #checkmark:dir(rtl) {
    -webkit-transform-origin: 50% 14%;
    transform-origin: 50% 14%;
  }

  /* label */
  #checkboxLabel {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    padding-left: var(--paper-checkbox-label-spacing, 8px);
    white-space: normal;
    line-height: normal;
    color: var(--paper-checkbox-label-color, var(--primary-text-color));
    @apply --paper-checkbox-label;
  }

  :host([checked]) #checkboxLabel {
    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));
    @apply --paper-checkbox-label-checked;
  }

  #checkboxLabel:dir(rtl) {
    padding-right: var(--paper-checkbox-label-spacing, 8px);
    padding-left: 0;
  }

  #checkboxLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #checkbox {
    opacity: 0.5;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
  }

  :host([disabled][checked]) #checkbox {
    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #checkboxLabel  {
    opacity: 0.65;
  }

  /* invalid state */
  #checkbox.invalid:not(.checked) {
    border-color: var(--paper-checkbox-error-color, var(--error-color));
  }
</style>

<div id="checkboxContainer">
  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">
    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>
  </div>
</div>

<div id="checkboxLabel"><slot></slot></div>`;l.setAttribute("strip-whitespace",""),Object(i.a)({_template:l,is:"paper-checkbox",behaviors:[a.a],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){Object(n.a)(this,(function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",r=e.match(/[A-Za-z]+$/);null!==r&&(t=r[0]);var a=parseFloat(e),o=8/3*a;"px"===t&&(o=Math.floor(o))%2!=a%2&&o++,this.updateStyles({"--paper-checkbox-ink-size":o+t})}}))},_computeCheckboxClass:function(e,t){var r="";return e&&(r+="checked "),t&&(r+="invalid"),r},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,o.b._createRipple.call(this)}})},166:function(e,t,r){"use strict";r.d(t,"a",(function(){return p}));const a=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),i=Symbol("Comlink.releaseProxy"),c=Symbol("Comlink.thrown"),n=e=>"object"==typeof e&&null!==e||"function"==typeof e,l=new Map([["proxy",{canHandle:e=>n(e)&&e[a],serialize(e){const{port1:t,port2:r}=new MessageChannel;return function e(t,r=self){r.addEventListener("message",(function o(i){if(!i||!i.data)return;const{id:n,type:l,path:p}=Object.assign({path:[]},i.data),h=(i.data.argumentList||[]).map(k);let d;try{const r=p.slice(0,-1).reduce((e,t)=>e[t],t),o=p.reduce((e,t)=>e[t],t);switch(l){case 0:d=o;break;case 1:r[p.slice(-1)[0]]=k(i.data.value),d=!0;break;case 2:d=o.apply(r,h);break;case 3:d=function(e){return Object.assign(e,{[a]:!0})}(new o(...h));break;case 4:{const{port1:r,port2:a}=new MessageChannel;e(t,a),d=function(e,t){return u.set(e,t),e}(r,[r])}break;case 5:d=void 0}}catch(m){d={value:m,[c]:0}}Promise.resolve(d).catch(e=>({value:e,[c]:0})).then(e=>{const[t,a]=b(e);r.postMessage(Object.assign(Object.assign({},t),{id:n}),a),5===l&&(r.removeEventListener("message",o),s(r))})})),r.start&&r.start()}(e,t),[r,[r]]},deserialize:e=>(e.start(),p(e))}],["throw",{canHandle:e=>n(e)&&c in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function s(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function p(e,t){return function e(t,r=[],a=function(){}){let c=!1;const n=new Proxy(a,{get(a,o){if(h(c),o===i)return()=>m(t,{type:5,path:r.map(e=>e.toString())}).then(()=>{s(t),c=!0});if("then"===o){if(0===r.length)return{then:()=>n};const e=m(t,{type:0,path:r.map(e=>e.toString())}).then(k);return e.then.bind(e)}return e(t,[...r,o])},set(e,a,o){h(c);const[i,n]=b(o);return m(t,{type:1,path:[...r,a].map(e=>e.toString()),value:i},n).then(k)},apply(a,i,n){h(c);const l=r[r.length-1];if(l===o)return m(t,{type:4}).then(k);if("bind"===l)return e(t,r.slice(0,-1));const[s,p]=d(n);return m(t,{type:2,path:r.map(e=>e.toString()),argumentList:s},p).then(k)},construct(e,a){h(c);const[o,i]=d(a);return m(t,{type:3,path:r.map(e=>e.toString()),argumentList:o},i).then(k)}});return n}(e,[],t)}function h(e){if(e)throw new Error("Proxy has been released and is not useable")}function d(e){const t=e.map(b);return[t.map(e=>e[0]),(r=t.map(e=>e[1]),Array.prototype.concat.apply([],r))];var r}const u=new WeakMap;function b(e){for(const[t,r]of l)if(r.canHandle(e)){const[a,o]=r.serialize(e);return[{type:3,name:t,value:a},o]}return[{type:0,value:e},u.get(e)||[]]}function k(e){switch(e.type){case 3:return l.get(e.name).deserialize(e.value);case 0:return e.value}}function m(e,t,r){return new Promise(a=>{const o=new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-");e.addEventListener("message",(function t(r){r.data&&r.data.id&&r.data.id===o&&(e.removeEventListener("message",t),a(r.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:o},t),r)})}},185:function(e,t,r){"use strict";r(5),r(47),r(56),r(141);var a=r(6),o=r(4),i=r(101);Object(a.a)({_template:o.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[i.a]})},296:function(e,t,r){"use strict";r(5),r(47),r(52);var a=r(246),o=r(6),i=r(4);Object(o.a)({_template:i.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(a.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},63:function(e,t,r){"use strict";r.d(t,"a",(function(){return a})),r.d(t,"c",(function(){return c})),r.d(t,"d",(function(){return n})),r.d(t,"b",(function(){return l}));class a{constructor(e="keyval-store",t="keyval"){this.storeName=t,this._dbp=new Promise((r,a)=>{const o=indexedDB.open(e,1);o.onerror=()=>a(o.error),o.onsuccess=()=>r(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(t)}})}_withIDBStore(e,t){return this._dbp.then(r=>new Promise((a,o)=>{const i=r.transaction(this.storeName,e);i.oncomplete=()=>a(),i.onabort=i.onerror=()=>o(i.error),t(i.objectStore(this.storeName))}))}}let o;function i(){return o||(o=new a),o}function c(e,t=i()){let r;return t._withIDBStore("readonly",t=>{r=t.get(e)}).then(()=>r.result)}function n(e,t,r=i()){return r._withIDBStore("readwrite",r=>{r.put(t,e)})}function l(e=i()){return e._withIDBStore("readwrite",e=>{e.clear()})}}}]);
//# sourceMappingURL=chunk.f9a4d36443c8074c632c.js.map