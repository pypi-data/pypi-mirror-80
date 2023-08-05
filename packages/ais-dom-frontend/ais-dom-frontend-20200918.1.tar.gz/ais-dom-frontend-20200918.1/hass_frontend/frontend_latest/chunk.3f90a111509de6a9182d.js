/*! For license information please see chunk.3f90a111509de6a9182d.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[186],{140:function(t,n,i){"use strict";i(47),i(78);var e=i(6),o=i(3),s=i(4),a=i(5);Object(e.a)({_template:s.a`
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
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:a.a.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var n=(t||"").split(":");this._iconName=n.pop(),this._iconsetName=n.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&Object(o.a)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,Object(o.a)(this.root).appendChild(this._img))}})},167:function(t,n,i){"use strict";i(5);const e={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(t,n){for(var i in n)t[i]=n[i]},_cloneConfig:function(t){var n={isClone:!0};return this._copyProperties(n,t),n},_getAnimationConfigRecursive:function(t,n,i){var e;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(e=t?this.animationConfig[t]:this.animationConfig,Array.isArray(e)||(e=[e]),e)for(var o,s=0;o=e[s];s++)if(o.animatable)o.animatable._getAnimationConfigRecursive(o.type||t,n,i);else if(o.id){var a=n[o.id];a?(a.isClone||(n[o.id]=this._cloneConfig(a),a=n[o.id]),this._copyProperties(a,o)):n[o.id]=o}else i.push(o)},getAnimationConfig:function(t){var n={},i=[];for(var e in this._getAnimationConfigRecursive(t,n,i),n)i.push(n[e]);return i}};i.d(n,"a",(function(){return o}));const o=[e,{_configureAnimations:function(t){var n=[],i=[];if(t.length>0)for(let s,a=0;s=t[a];a++){let t=document.createElement(s.name);if(t.isNeonAnimation){let n=null;t.configure||(t.configure=function(t){return null}),n=t.configure(s),i.push({result:n,config:s,neonAnimation:t})}else console.warn(this.is+":",s.name,"not found!")}for(var e=0;e<i.length;e++){let t=i[e].result,s=i[e].config,a=i[e].neonAnimation;try{"function"!=typeof t.cancel&&(t=document.timeline.play(t))}catch(o){t=null,console.warn("Couldnt play","(",s.name,").",o)}t&&n.push({neonAnimation:a,config:s,animation:t})}return n},_shouldComplete:function(t){for(var n=!0,i=0;i<t.length;i++)if("finished"!=t[i].animation.playState){n=!1;break}return n},_complete:function(t){for(var n=0;n<t.length;n++)t[n].neonAnimation.complete(t[n].config);for(n=0;n<t.length;n++)t[n].animation.cancel()},playAnimation:function(t,n){var i=this.getAnimationConfig(t);if(i){this._active=this._active||{},this._active[t]&&(this._complete(this._active[t]),delete this._active[t]);var e=this._configureAnimations(i);if(0!=e.length){this._active[t]=e;for(var o=0;o<e.length;o++)e[o].animation.onfinish=function(){this._shouldComplete(e)&&(this._complete(e),delete this._active[t],this.fire("neon-animation-finish",n,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",n,{bubbles:!1})}},cancelAnimation:function(){for(var t in this._active){var n=this._active[t];for(var i in n)n[i].animation.cancel()}this._active={}}}]},190:function(t,n,i){"use strict";i(5),i(47);var e=i(6),o=i(4);Object(e.a)({_template:o.a`
    <style>

      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        position: relative;
        height: 64px;
        padding: 0 16px;
        pointer-events: none;
        font-size: var(--app-toolbar-font-size, 20px);
      }

      :host ::slotted(*) {
        pointer-events: auto;
      }

      :host ::slotted(paper-icon-button) {
        /* paper-icon-button/issues/33 */
        font-size: 0;
      }

      :host ::slotted([main-title]),
      :host ::slotted([condensed-title]) {
        pointer-events: none;
        @apply --layout-flex;
      }

      :host ::slotted([bottom-item]) {
        position: absolute;
        right: 0;
        bottom: 0;
        left: 0;
      }

      :host ::slotted([top-item]) {
        position: absolute;
        top: 0;
        right: 0;
        left: 0;
      }

      :host ::slotted([spacer]) {
        margin-left: 64px;
      }
    </style>

    <slot></slot>
`,is:"app-toolbar"})},216:function(t,n,i){"use strict";i.d(n,"a",(function(){return e}));const e=t=>(n,i)=>{if(n.constructor._observers){if(!n.constructor.hasOwnProperty("_observers")){const t=n.constructor._observers;n.constructor._observers=new Map,t.forEach((t,i)=>n.constructor._observers.set(i,t))}}else{n.constructor._observers=new Map;const t=n.updated;n.updated=function(n){t.call(this,n),n.forEach((t,n)=>{const i=this.constructor._observers.get(n);void 0!==i&&i.call(this,this[n],t)})}}n.constructor._observers.set(i,t)}},246:function(t,n,i){"use strict";i.d(n,"b",(function(){return s})),i.d(n,"a",(function(){return a}));i(5);var e=i(114),o=i(3);const s={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(t,n){n&&(t?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(t){this.closingReason=this.closingReason||{},this.closingReason.confirmed=t},_onDialogClick:function(t){for(var n=Object(o.a)(t).path,i=0,e=n.indexOf(this);i<e;i++){var s=n[i];if(s.hasAttribute&&(s.hasAttribute("dialog-dismiss")||s.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(s.hasAttribute("dialog-confirm")),this.close(),t.stopPropagation();break}}}},a=[e.a,s]},277:function(t,n,i){"use strict";i(5),i(47),i(52),i(56),i(113);const e=document.createElement("template");e.setAttribute("style","display: none;"),e.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(e.content);var o=i(167),s=i(246),a=i(6),r=i(4);Object(a.a)({_template:r.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[s.a,o.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},63:function(t,n,i){"use strict";i.d(n,"a",(function(){return e})),i.d(n,"c",(function(){return a})),i.d(n,"d",(function(){return r})),i.d(n,"b",(function(){return c}));class e{constructor(t="keyval-store",n="keyval"){this.storeName=n,this._dbp=new Promise((i,e)=>{const o=indexedDB.open(t,1);o.onerror=()=>e(o.error),o.onsuccess=()=>i(o.result),o.onupgradeneeded=()=>{o.result.createObjectStore(n)}})}_withIDBStore(t,n){return this._dbp.then(i=>new Promise((e,o)=>{const s=i.transaction(this.storeName,t);s.oncomplete=()=>e(),s.onabort=s.onerror=()=>o(s.error),n(s.objectStore(this.storeName))}))}}let o;function s(){return o||(o=new e),o}function a(t,n=s()){let i;return n._withIDBStore("readonly",n=>{i=n.get(t)}).then(()=>i.result)}function r(t,n,i=s()){return i._withIDBStore("readwrite",i=>{i.put(n,t)})}function c(t=s()){return t._withIDBStore("readwrite",t=>{t.clear()})}}}]);
//# sourceMappingURL=chunk.3f90a111509de6a9182d.js.map