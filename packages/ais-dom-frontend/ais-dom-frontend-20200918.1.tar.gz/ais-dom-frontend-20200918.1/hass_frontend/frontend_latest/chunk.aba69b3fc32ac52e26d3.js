(self.webpackJsonp=self.webpackJsonp||[]).push([[40],{939:function(e,t,i){"use strict";i.r(t);i(313);var n=i(112),o=i(0),r=i(49),s=i(156),a=i(11),l=i(155),c=i(211),d=i(641),p=i(159),u=(i(332),i(311),i(210),i(255),i(183),i(234),i(600)),h=i(393),f=i(642),m=(i(195),i(191),i(55));function y(e){var t,i=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function x(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,n=new Array(t);i<t;i++)n[i]=e[i];return n}function w(e,t,i){return(w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=E(e)););return e}(e,t);if(n){var o=Object.getOwnPropertyDescriptor(n,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function E(e){return(E=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const O=["Alexa.EndpointHealth"];!function(e,t,i,n){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var o=t.placement;if(t.kind===n&&("static"===o||"prototype"===o)){var r="static"===o?e:i;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!g(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:i,finishers:n};var r=this.decorateConstructor(i,t);return n.push.apply(n,r.finishers),r.finishers=n,r},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],o=e.decorators,r=o.length-1;r>=0;r--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[r])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var o=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[n])(o)||o);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return x(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?x(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=k(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:n,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:_(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=_(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(n)for(var r=0;r<n.length;r++)o=n[r](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},n=0;n<e.length;n++){var o,r=e[n];if("method"===r.kind&&(o=t.find(i)))if(b(r.descriptor)||b(o.descriptor)){if(g(r)||g(o))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");o.descriptor=r.descriptor}else{if(g(r)){if(g(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");o.decorators=r.decorators}v(r,o)}else t.push(r)}return t}(s.d.map(y)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([Object(o.d)("cloud-alexa")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(o.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(o.h)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(o.h)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[Object(o.g)()],key:"_entities",value:void 0},{kind:"field",decorators:[Object(o.h)()],key:"_entityConfigs",value:()=>({})},{kind:"field",key:"_popstateSyncAttached",value:()=>!1},{kind:"field",key:"_popstateReloadStatusAttached",value:()=>!1},{kind:"field",key:"_isInitialExposed",value:void 0},{kind:"field",key:"_getEntityFilterFunc",value:()=>Object(s.a)(e=>Object(d.a)(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities))},{kind:"method",key:"render",value:function(){if(void 0===this._entities)return o.f` <hass-loading-screen></hass-loading-screen> `;const e=Object(d.b)(this.cloudStatus.alexa_entities),t=this._getEntityFilterFunc(this.cloudStatus.alexa_entities),i=this._isInitialExposed||new Set,s=void 0===this._isInitialExposed;let a=0;const l=[],c=[];return this._entities.forEach(d=>{const p=this.hass.states[d.entity_id],u=this._entityConfigs[d.entity_id]||{should_expose:null},h=e?this._configIsExposed(d.entity_id,u):t(d.entity_id),f=e?this._configIsDomainExposed(d.entity_id):t(d.entity_id);h&&(a++,s&&i.add(d.entity_id));const m=i.has(d.entity_id)?l:c,y=o.f`<mwc-icon-button
        slot="trigger"
        class=${Object(r.a)({exposed:h,"not-exposed":!h})}
        .disabled=${!e}
        .title=${this.hass.localize("ui.panel.config.cloud.google.expose")}
      >
        <ha-svg-icon
          .path=${null!==u.should_expose?h?n.w:n.D:f?n.x:n.E}
        ></ha-svg-icon>
      </mwc-icon-button>`;m.push(o.f`
        <ha-card>
          <div class="card-content">
            <div class="top-line">
              <state-info
                .hass=${this.hass}
                .stateObj=${p}
                secondary-line
                @click=${this._showMoreInfo}
              >
                ${d.interfaces.filter(e=>!O.includes(e)).map(e=>e.replace(/(Alexa.|Controller)/g,"")).join(", ")}
              </state-info>
              ${e?o.f`<ha-button-menu
                    corner="BOTTOM_START"
                    .entityId=${p.entity_id}
                    @action=${this._exposeChanged}
                  >
                    ${y}
                    <mwc-list-item hasMeta>
                      ${this.hass.localize("ui.panel.config.cloud.google.expose_entity")}
                      <ha-svg-icon
                        class="exposed"
                        slot="meta"
                        .path=${n.w}
                      ></ha-svg-icon>
                    </mwc-list-item>
                    <mwc-list-item hasMeta>
                      ${this.hass.localize("ui.panel.config.cloud.google.dont_expose_entity")}
                      <ha-svg-icon
                        class="not-exposed"
                        slot="meta"
                        .path=${n.D}
                      ></ha-svg-icon>
                    </mwc-list-item>
                    <mwc-list-item hasMeta>
                      ${this.hass.localize("ui.panel.config.cloud.google.follow_domain")}
                      <ha-svg-icon
                        class=${Object(r.a)({exposed:f,"not-exposed":!f})}
                        slot="meta"
                        .path=${f?n.x:n.E}
                      ></ha-svg-icon>
                    </mwc-list-item>
                  </ha-button-menu>`:o.f`${y}`}
            </div>
          </div>
        </ha-card>
      `)}),s&&(this._isInitialExposed=i),o.f`
      <hass-subpage header="${this.hass.localize("ui.panel.config.cloud.alexa.title")}">
        ${e?o.f`
                <mwc-button
                  slot="toolbar-icon"
                  @click=${this._openDomainToggler}
                  >${this.hass.localize("ui.panel.config.cloud.alexa.manage_domains")}</mwc-button
                >
              `:""}
        ${e?"":o.f`
                <div class="banner">
                  ${this.hass.localize("ui.panel.config.cloud.alexa.banner")}
                </div>
              `}
          ${l.length>0?o.f`
                  <div class="header">
                    <h3>
                      ${this.hass.localize("ui.panel.config.cloud.alexa.exposed_entities")}
                    </h3>
                    ${this.narrow?a:this.hass.localize("ui.panel.config.cloud.alexa.exposed","selected",a)}
                  </div>
                  <div class="content">${l}</div>
                `:""}
          ${c.length>0?o.f`
                  <div class="header second">
                    <h3>
                      ${this.hass.localize("ui.panel.config.cloud.alexa.not_exposed_entities")}
                    </h3>
                    ${this.narrow?this._entities.length-a:this.hass.localize("ui.panel.config.cloud.alexa.not_exposed","selected",this._entities.length-a)}
                  </div>
                  <div class="content">${c}</div>
                `:""}
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){w(E(i.prototype),"firstUpdated",this).call(this,e),this._fetchData()}},{kind:"method",key:"updated",value:function(e){w(E(i.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&(this._entityConfigs=this.cloudStatus.prefs.alexa_entity_configs)}},{kind:"method",key:"_fetchData",value:async function(){const e=await Object(u.a)(this.hass);e.sort((e,t)=>{const i=this.hass.states[e.entity_id],n=this.hass.states[t.entity_id];return Object(p.b)(i?Object(c.a)(i):e.entity_id,n?Object(c.a)(n):t.entity_id)}),this._entities=e}},{kind:"method",key:"_showMoreInfo",value:function(e){const t=e.currentTarget.stateObj.entity_id;Object(a.a)(this,"hass-more-info",{entityId:t})}},{kind:"method",key:"_configIsDomainExposed",value:function(e){const t=Object(l.a)(e);return!this.cloudStatus.prefs.alexa_default_expose||this.cloudStatus.prefs.alexa_default_expose.includes(t)}},{kind:"method",key:"_configIsExposed",value:function(e,t){var i;return null!==(i=t.should_expose)&&void 0!==i?i:this._configIsDomainExposed(e)}},{kind:"method",key:"_exposeChanged",value:async function(e){const t=e.currentTarget.entityId;let i=null;switch(e.detail.index){case 0:i=!0;break;case 1:i=!1;break;case 2:i=null}await this._updateExposed(t,i)}},{kind:"method",key:"_updateExposed",value:async function(e,t){await this._updateConfig(e,{should_expose:t}),this._ensureEntitySync()}},{kind:"method",key:"_updateConfig",value:async function(e,t){const i=await Object(h.i)(this.hass,e,t);this._entityConfigs={...this._entityConfigs,[e]:i},this._ensureStatusReload()}},{kind:"method",key:"_openDomainToggler",value:function(){Object(f.a)(this,{domains:this._entities.map(e=>Object(l.a)(e.entity_id)).filter((e,t,i)=>i.indexOf(e)===t),exposedDomains:this.cloudStatus.prefs.alexa_default_expose,toggleDomain:(e,t)=>{this._updateDomainExposed(e,t)},resetDomain:e=>{this._entities.forEach(t=>{Object(l.a)(t.entity_id)===e&&this._updateExposed(t.entity_id,null)})}})}},{kind:"method",key:"_updateDomainExposed",value:async function(e,t){const i=this.cloudStatus.prefs.alexa_default_expose||this._entities.map(e=>Object(l.a)(e.entity_id)).filter((e,t,i)=>i.indexOf(e)===t);t&&i.includes(e)||!t&&!i.includes(e)||(t?i.push(e):i.splice(i.indexOf(e),1),await Object(h.k)(this.hass,{alexa_default_expose:i}),Object(a.a)(this,"ha-refresh-cloud-status"))}},{kind:"method",key:"_ensureStatusReload",value:function(){if(this._popstateReloadStatusAttached)return;this._popstateReloadStatusAttached=!0;const e=this.parentElement;window.addEventListener("popstate",()=>Object(a.a)(e,"ha-refresh-cloud-status"),{once:!0})}},{kind:"method",key:"_ensureEntitySync",value:function(){this._popstateSyncAttached||(this._popstateSyncAttached=!0,window.addEventListener("popstate",()=>{},{once:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[m.c,o.c`
        mwc-list-item > [slot="meta"] {
          margin-left: 4px;
        }
        .banner {
          color: var(--primary-text-color);
          background-color: var(
            --ha-card-background,
            var(--card-background-color, white)
          );
          padding: 16px 8px;
          text-align: center;
        }
        .content {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          grid-gap: 8px 8px;
          padding: 8px;
        }
        .card-content {
          padding-bottom: 12px;
        }
        state-info {
          cursor: pointer;
        }
        ha-switch {
          padding: 8px 0;
        }
        .top-line {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--app-header-background-color);
        }
        .header.second {
          border-top: 1px solid var(--divider-color);
        }
        .exposed {
          color: var(--success-color);
        }
        .not-exposed {
          color: var(--error-color);
        }
        @media all and (max-width: 450px) {
          ha-card {
            max-width: 100%;
          }
        }
      `]}}]}}),o.a)}}]);
//# sourceMappingURL=chunk.aba69b3fc32ac52e26d3.js.map