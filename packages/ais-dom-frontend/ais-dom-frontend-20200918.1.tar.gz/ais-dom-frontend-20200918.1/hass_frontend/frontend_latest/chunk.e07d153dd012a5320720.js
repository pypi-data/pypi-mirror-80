/*! For license information please see chunk.e07d153dd012a5320720.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[234],{157:function(e,t,r){"use strict";r(5),r(39),r(140),r(75),r(160),r(145),r(52),r(186),r(187);var i=r(67),n=r(44),o=r(68),s=r(69),a=r(6),l=r(3),c=r(40),d=r(4);Object(a.a)({_template:d.a`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <!-- this div fulfills an a11y requirement for combobox, do not remove -->
    <span role="button"></span>
    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[i.a,n.a,o.a,s.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(l.a)(this.$.content).getDistributedNodes(),t=0,r=e.length;t<r;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){c.c(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},189:function(e,t,r){"use strict";r(157);const i=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends i{ready(){super.ready(),setTimeout(()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")},100)}})},192:function(e,t,r){"use strict";r(168);const i=customElements.get("paper-slider");customElements.define("ha-paper-slider",class extends i{static get template(){const e=document.createElement("template");e.innerHTML=i.template.innerHTML;const t=document.createElement("style");return t.innerHTML='\n      .pin > .slider-knob > .slider-knob-inner {\n        font-size:  var(--ha-paper-slider-pin-font-size, 10px);\n        line-height: normal;\n      }\n\n      .disabled.ring > .slider-knob > .slider-knob-inner {\n        background-color: var(--paper-slider-disabled-knob-color, var(--paper-grey-400));\n        border: 2px solid var(--paper-slider-disabled-knob-color, var(--paper-grey-400));\n      }\n\n      .pin > .slider-knob > .slider-knob-inner::before {\n        top: unset;\n        margin-left: unset;\n\n        bottom: calc(15px + var(--calculated-paper-slider-height)/2);\n        left: 50%;\n        width: 2.2em;\n        height: 2.2em;\n\n        -webkit-transform-origin: left bottom;\n        transform-origin: left bottom;\n        -webkit-transform: rotate(-45deg) scale(0) translate(0);\n        transform: rotate(-45deg) scale(0) translate(0);\n      }\n\n      .pin.expand > .slider-knob > .slider-knob-inner::before {\n        -webkit-transform: rotate(-45deg) scale(1) translate(7px, -7px);\n        transform: rotate(-45deg) scale(1) translate(7px, -7px);\n      }\n\n      .pin > .slider-knob > .slider-knob-inner::after {\n        top: unset;\n        font-size: unset;\n\n        bottom: calc(15px + var(--calculated-paper-slider-height)/2);\n        left: 50%;\n        margin-left: -1.1em;\n        width: 2.2em;\n        height: 2.1em;\n\n        -webkit-transform-origin: center bottom;\n        transform-origin: center bottom;\n        -webkit-transform: scale(0) translate(0);\n        transform: scale(0) translate(0);\n      }\n\n      .pin.expand > .slider-knob > .slider-knob-inner::after {\n        -webkit-transform: scale(1) translate(0, -10px);\n        transform: scale(1) translate(0, -10px);\n      }\n\n      :host([dir="rtl"]) .pin.expand > .slider-knob > .slider-knob-inner::after {\n        -webkit-transform: scale(1) translate(0, -17px) scaleX(-1) !important;\n        transform: scale(1) translate(0, -17px) scaleX(-1) !important;\n        }\n\n        .slider-input {\n          width: 54px;\n        }\n    ',e.content.appendChild(t),e}})},226:function(e,t,r){"use strict";r.d(t,"a",(function(){return o}));var i=r(9),n=r(11);const o=Object(i.a)(e=>class extends e{fire(e,t,r){return r=r||{},Object(n.a)(r.node||this,e,t,r)}})},333:function(e,t,r){"use strict";r.d(t,"a",(function(){return s}));var i=r(15),n=r(14);const o=new WeakMap,s=Object(n.f)((...e)=>t=>{let r=o.get(t);void 0===r&&(r={lastRenderedIndex:2147483647,values:[]},o.set(t,r));const n=r.values;let s=n.length;r.values=e;for(let o=0;o<e.length&&!(o>r.lastRenderedIndex);o++){const a=e[o];if(Object(i.h)(a)||"function"!=typeof a.then){t.setValue(a),r.lastRenderedIndex=o;break}o<s&&a===n[o]||(r.lastRenderedIndex=2147483647,s=0,Promise.resolve(a).then(e=>{const i=r.values.indexOf(a);i>-1&&i<r.lastRenderedIndex&&(r.lastRenderedIndex=i,t.setValue(e),t.commit())}))}})},344:function(e,t,r){"use strict";const i={DOMAIN_DEVICE_CLASS:{binary_sensor:["battery","cold","connectivity","door","garage_door","gas","heat","light","lock","moisture","motion","moving","occupancy","opening","plug","power","presence","problem","safety","smoke","sound","vibration","window"],cover:["awning","blind","curtain","damper","door","garage","shade","shutter","window"],humidifier:["dehumidifier","humidifier"],sensor:["battery","humidity","illuminance","temperature","pressure","power","signal_strength","timestamp"],switch:["switch","outlet"]},UNKNOWN_TYPE:"json",ADD_TYPE:"key-value",TYPE_TO_TAG:{string:"ha-customize-string",json:"ha-customize-string",icon:"ha-customize-icon",boolean:"ha-customize-boolean",array:"ha-customize-array","key-value":"ha-customize-key-value"}};i.LOGIC_STATE_ATTRIBUTES=i.LOGIC_STATE_ATTRIBUTES||{entity_picture:void 0,friendly_name:{type:"string",description:"Name"},icon:{type:"icon"},emulated_hue:{type:"boolean",domains:["emulated_hue"]},emulated_hue_name:{type:"string",domains:["emulated_hue"]},haaska_hidden:void 0,haaska_name:void 0,supported_features:void 0,attribution:void 0,restored:void 0,custom_ui_more_info:{type:"string"},custom_ui_state_card:{type:"string"},device_class:{type:"array",options:i.DOMAIN_DEVICE_CLASS,description:"Device class",domains:["binary_sensor","cover","humidifier","sensor","switch"]},assumed_state:{type:"boolean",domains:["switch","light","cover","climate","fan","humidifier","group","water_heater"]},initial_state:{type:"string",domains:["automation"]},unit_of_measurement:{type:"string"}},t.a=i},359:function(e,t,r){"use strict";var i=r(0),n=r(333),o=r(344);function s(e){var t,r=h(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function h(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let p;!function(e,t,r,i){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=h(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var p=t((function(e){n.initializeInstanceElements(e,f.elements)}),r),f=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(c(o.descriptor)||c(n.descriptor)){if(l(o)||l(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(l(o)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}a(o,n)}else t.push(o)}return t}(p.d.map(s)),e);n.initializeClassElements(p.F,f.elements),n.runClassFinishers(p.F,f.finishers)}([Object(i.d)("ha-attributes")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"stateObj",value:void 0},{kind:"field",decorators:[Object(i.h)({attribute:"extra-filters"})],key:"extraFilters",value:void 0},{kind:"method",key:"render",value:function(){return this.stateObj?i.f`
      <div>
        ${this.computeDisplayAttributes(Object.keys(o.a.LOGIC_STATE_ATTRIBUTES).concat(this.extraFilters?this.extraFilters.split(","):[])).map(e=>i.f`
            <div class="data-entry">
              <div class="key">${e.replace(/_/g," ")}</div>
              <div class="value">
                ${this.formatAttribute(e)}
              </div>
            </div>
          `)}
        ${this.stateObj.attributes.attribution?i.f`
              <div class="attribution">
                ${this.stateObj.attributes.attribution}
              </div>
            `:""}
      </div>
    `:i.f``}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      .data-entry {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }
      .data-entry .value {
        max-width: 200px;
        overflow-wrap: break-word;
      }
      .attribution {
        color: var(--secondary-text-color);
        text-align: right;
      }
      pre {
        font-family: inherit;
        font-size: inherit;
      }
    `}},{kind:"method",key:"computeDisplayAttributes",value:function(e){return this.stateObj?Object.keys(this.stateObj.attributes).filter(t=>-1===e.indexOf(t)):[]}},{kind:"method",key:"formatAttribute",value:function(e){if(!this.stateObj)return"-";const t=this.stateObj.attributes[e];return this.formatAttributeValue(t)}},{kind:"method",key:"formatAttributeValue",value:function(e){if(null===e)return"-";if(Array.isArray(e)&&e.some(e=>e instanceof Object)||!Array.isArray(e)&&e instanceof Object){p||(p=r.e(9).then(r.t.bind(null,324,7)));const t=p.then(t=>t.safeDump(e));return i.f` <pre>${Object(n.a)(t,"")}</pre> `}return Array.isArray(e)?e.join(", "):e}}]}}),i.a)},396:function(e,t,r){"use strict";r.d(t,"a",(function(){return i})),r.d(t,"c",(function(){return n})),r.d(t,"d",(function(){return o})),r.d(t,"b",(function(){return s})),r.d(t,"e",(function(){return a}));const i=1,n=2,o=4,s=16,a=128},547:function(e,t,r){"use strict";var i=r(4),n=r(32);r(138),r(192);class o extends n.a{static get template(){return i.a`
      <style>
        :host {
          display: block;
          border-radius: 4px;
        }

        .title {
          margin-bottom: 16px;
          color: var(--secondary-text-color);
        }

        .slider-container {
          display: flex;
        }

        ha-icon {
          margin-top: 4px;
          color: var(--secondary-text-color);
        }

        ha-paper-slider {
          flex-grow: 1;
          background-image: var(--ha-slider-background);
        }
      </style>

      <div class="title">[[caption]]</div>
      <div class="extra-container"><slot name="extra"></slot></div>
      <div class="slider-container">
        <ha-icon icon="[[icon]]" hidden$="[[!icon]]"></ha-icon>
        <ha-paper-slider
          min="[[min]]"
          max="[[max]]"
          step="[[step]]"
          pin="[[pin]]"
          disabled="[[disabled]]"
          disabled="[[disabled]]"
          value="{{value}}"
        ></ha-paper-slider>
      </div>
    `}static get properties(){return{caption:String,disabled:Boolean,min:Number,max:Number,pin:Boolean,step:Number,extra:{type:Boolean,value:!1},ignoreBarTouch:{type:Boolean,value:!0},icon:{type:String,value:""},value:{type:Number,notify:!0}}}}customElements.define("ha-labeled-slider",o)},984:function(e,t,r){"use strict";r.r(t);r(139),r(144);var i=r(0),n=r(49),o=r(293),s=(r(359),r(4)),a=r(32),l=r(226);class c extends(Object(l.a)(a.a)){static get template(){return s.a`
      <style>
        :host {
          user-select: none;
          -webkit-user-select: none;
        }

        #canvas {
          position: relative;
          width: 100%;
          max-width: 330px;
        }
        #canvas > * {
          display: block;
        }
        #interactionLayer {
          color: white;
          position: absolute;
          cursor: crosshair;
          width: 100%;
          height: 100%;
          overflow: visible;
        }
        #backgroundLayer {
          width: 100%;
          overflow: visible;
          --wheel-bordercolor: var(--ha-color-picker-wheel-bordercolor, white);
          --wheel-borderwidth: var(--ha-color-picker-wheel-borderwidth, 3);
          --wheel-shadow: var(
            --ha-color-picker-wheel-shadow,
            rgb(15, 15, 15) 10px 5px 5px 0px
          );
        }

        #marker {
          fill: currentColor;
          stroke: var(--ha-color-picker-marker-bordercolor, white);
          stroke-width: var(--ha-color-picker-marker-borderwidth, 3);
          filter: url(#marker-shadow);
        }
        .dragging #marker {
        }

        #colorTooltip {
          display: none;
          fill: currentColor;
          stroke: var(--ha-color-picker-tooltip-bordercolor, white);
          stroke-width: var(--ha-color-picker-tooltip-borderwidth, 3);
        }

        .touch.dragging #colorTooltip {
          display: inherit;
        }
      </style>
      <div id="canvas">
        <svg id="interactionLayer">
          <defs>
            <filter
              id="marker-shadow"
              x="-50%"
              y="-50%"
              width="200%"
              height="200%"
              filterUnits="objectBoundingBox"
            >
              <feOffset
                result="offOut"
                in="SourceAlpha"
                dx="2"
                dy="2"
              ></feOffset>
              <feGaussianBlur
                result="blurOut"
                in="offOut"
                stdDeviation="2"
              ></feGaussianBlur>
              <feComponentTransfer in="blurOut" result="alphaOut">
                <feFuncA type="linear" slope="0.3"></feFuncA>
              </feComponentTransfer>
              <feBlend
                in="SourceGraphic"
                in2="alphaOut"
                mode="normal"
              ></feBlend>
            </filter>
          </defs>
        </svg>
        <canvas id="backgroundLayer"></canvas>
      </div>
    `}static get properties(){return{hsColor:{type:Object},desiredHsColor:{type:Object,observer:"applyHsColor"},width:{type:Number,value:500},height:{type:Number,value:500},radius:{type:Number,value:225},hueSegments:{type:Number,value:0,observer:"segmentationChange"},saturationSegments:{type:Number,value:0,observer:"segmentationChange"},ignoreSegments:{type:Boolean,value:!1},throttle:{type:Number,value:500}}}ready(){super.ready(),this.setupLayers(),this.drawColorWheel(),this.drawMarker(),this.desiredHsColor&&(this.setMarkerOnColor(this.desiredHsColor),this.applyColorToCanvas(this.desiredHsColor)),this.interactionLayer.addEventListener("mousedown",e=>this.onMouseDown(e)),this.interactionLayer.addEventListener("touchstart",e=>this.onTouchStart(e))}convertToCanvasCoordinates(e,t){const r=this.interactionLayer.createSVGPoint();r.x=e,r.y=t;const i=r.matrixTransform(this.interactionLayer.getScreenCTM().inverse());return{x:i.x,y:i.y}}onMouseDown(e){const t=this.convertToCanvasCoordinates(e.clientX,e.clientY);this.isInWheel(t.x,t.y)&&(this.onMouseSelect(e),this.canvas.classList.add("mouse","dragging"),this.addEventListener("mousemove",this.onMouseSelect),this.addEventListener("mouseup",this.onMouseUp))}onMouseUp(){this.canvas.classList.remove("mouse","dragging"),this.removeEventListener("mousemove",this.onMouseSelect)}onMouseSelect(e){requestAnimationFrame(()=>this.processUserSelect(e))}onTouchStart(e){const t=e.changedTouches[0],r=this.convertToCanvasCoordinates(t.clientX,t.clientY);if(this.isInWheel(r.x,r.y)){if(e.target===this.marker)return e.preventDefault(),this.canvas.classList.add("touch","dragging"),this.addEventListener("touchmove",this.onTouchSelect),void this.addEventListener("touchend",this.onTouchEnd);this.tapBecameScroll=!1,this.addEventListener("touchend",this.onTap),this.addEventListener("touchmove",()=>{this.tapBecameScroll=!0},{passive:!0})}}onTap(e){this.tapBecameScroll||(e.preventDefault(),this.onTouchSelect(e))}onTouchEnd(){this.canvas.classList.remove("touch","dragging"),this.removeEventListener("touchmove",this.onTouchSelect)}onTouchSelect(e){requestAnimationFrame(()=>this.processUserSelect(e.changedTouches[0]))}processUserSelect(e){const t=this.convertToCanvasCoordinates(e.clientX,e.clientY),r=this.getColor(t.x,t.y);this.onColorSelect(r)}onColorSelect(e){if(this.setMarkerOnColor(e),this.ignoreSegments||(e=this.applySegmentFilter(e)),this.applyColorToCanvas(e),this.colorSelectIsThrottled)return clearTimeout(this.ensureFinalSelect),void(this.ensureFinalSelect=setTimeout(()=>{this.fireColorSelected(e)},this.throttle));this.fireColorSelected(e),this.colorSelectIsThrottled=!0,setTimeout(()=>{this.colorSelectIsThrottled=!1},this.throttle)}fireColorSelected(e){this.hsColor=e,this.fire("colorselected",{hs:{h:e.h,s:e.s}})}setMarkerOnColor(e){if(!this.marker||!this.tooltip)return;const t=e.s*this.radius,r=(e.h-180)/180*Math.PI,i=`translate(${-t*Math.cos(r)},${-t*Math.sin(r)})`;this.marker.setAttribute("transform",i),this.tooltip.setAttribute("transform",i)}applyColorToCanvas(e){this.interactionLayer&&(this.interactionLayer.style.color=`hsl(${e.h}, 100%, ${100-50*e.s}%)`)}applyHsColor(e){this.hsColor&&this.hsColor.h===e.h&&this.hsColor.s===e.s||(this.setMarkerOnColor(e),this.ignoreSegments||(e=this.applySegmentFilter(e)),this.hsColor=e,this.applyColorToCanvas(e))}getAngle(e,t){return Math.atan2(-t,-e)/Math.PI*180+180}isInWheel(e,t){return this.getDistance(e,t)<=1}getDistance(e,t){return Math.sqrt(e*e+t*t)/this.radius}getColor(e,t){const r=this.getAngle(e,t),i=this.getDistance(e,t);return{h:r,s:Math.min(i,1)}}applySegmentFilter(e){if(this.hueSegments){const t=360/this.hueSegments,r=t/2;e.h-=r,e.h<0&&(e.h+=360);const i=e.h%t;e.h-=i-t}if(this.saturationSegments)if(1===this.saturationSegments)e.s=1;else{const t=1/this.saturationSegments,r=1/(this.saturationSegments-1),i=Math.floor(e.s/t)*r;e.s=Math.min(i,1)}return e}setupLayers(){this.canvas=this.$.canvas,this.backgroundLayer=this.$.backgroundLayer,this.interactionLayer=this.$.interactionLayer,this.originX=this.width/2,this.originY=this.originX,this.backgroundLayer.width=this.width,this.backgroundLayer.height=this.height,this.interactionLayer.setAttribute("viewBox",`${-this.originX} ${-this.originY} ${this.width} ${this.height}`)}drawColorWheel(){let e,t,r,i;const n=this.backgroundLayer.getContext("2d"),o=this.originX,s=this.originY,a=this.radius,l=window.getComputedStyle(this.backgroundLayer,null),c=parseInt(l.getPropertyValue("--wheel-borderwidth"),10),d=l.getPropertyValue("--wheel-bordercolor").trim(),h=l.getPropertyValue("--wheel-shadow").trim();if("none"!==h){const n=h.split("px ");e=n.pop(),t=parseInt(n[0],10),r=parseInt(n[1],10),i=parseInt(n[2],10)||0}const u=a+c/2,p=a,f=a+c;"none"!==l.shadow&&(n.save(),n.beginPath(),n.arc(o,s,f,0,2*Math.PI,!1),n.shadowColor=e,n.shadowOffsetX=t,n.shadowOffsetY=r,n.shadowBlur=i,n.fillStyle="white",n.fill(),n.restore()),function(e,t){const r=360/(e=e||360),i=r/2;for(let a=0;a<=360;a+=r){const e=(a-i)*(Math.PI/180),r=(a+i+1)*(Math.PI/180);n.beginPath(),n.moveTo(o,s),n.arc(o,s,p,e,r,!1),n.closePath();const l=n.createRadialGradient(o,s,0,o,s,p);let c=100;if(l.addColorStop(0,`hsl(${a}, 100%, ${c}%)`),t>0){const e=1/t;let r=0;for(let i=1;i<t;i+=1){const t=c;r=i*e,c=100-50*r,l.addColorStop(r,`hsl(${a}, 100%, ${t}%)`),l.addColorStop(r,`hsl(${a}, 100%, ${c}%)`)}l.addColorStop(r,`hsl(${a}, 100%, 50%)`)}l.addColorStop(1,`hsl(${a}, 100%, 50%)`),n.fillStyle=l,n.fill()}}(this.hueSegments,this.saturationSegments),c>0&&(n.beginPath(),n.arc(o,s,u,0,2*Math.PI,!1),n.lineWidth=c,n.strokeStyle=d,n.stroke())}drawMarker(){const e=this.interactionLayer,t=.08*this.radius,r=.15*this.radius,i=-3*r;e.marker=document.createElementNS("http://www.w3.org/2000/svg","circle"),e.marker.setAttribute("id","marker"),e.marker.setAttribute("r",t),this.marker=e.marker,e.appendChild(e.marker),e.tooltip=document.createElementNS("http://www.w3.org/2000/svg","circle"),e.tooltip.setAttribute("id","colorTooltip"),e.tooltip.setAttribute("r",r),e.tooltip.setAttribute("cx",0),e.tooltip.setAttribute("cy",i),this.tooltip=e.tooltip,e.appendChild(e.tooltip)}segmentationChange(){this.backgroundLayer&&this.drawColorWheel()}}customElements.define("ha-color-picker",c);r(183),r(547),r(189);var d=r(396);function h(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(f(o.descriptor)||f(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}u(o,n)}else t.push(o)}return t}(s.d.map(h)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([Object(i.d)("more-info-light")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_brightnessSliderValue",value:()=>0},{kind:"field",decorators:[Object(i.g)()],key:"_ctSliderValue",value:()=>0},{kind:"field",decorators:[Object(i.g)()],key:"_wvSliderValue",value:()=>0},{kind:"field",decorators:[Object(i.g)()],key:"_hueSegments",value:()=>24},{kind:"field",decorators:[Object(i.g)()],key:"_saturationSegments",value:()=>8},{kind:"field",decorators:[Object(i.g)()],key:"_colorPickerColor",value:void 0},{kind:"method",key:"render",value:function(){var e;return this.hass&&this.stateObj?i.f`
      <div
        class="content ${Object(n.a)({"is-on":"on"===this.stateObj.state})}"
      >
        ${Object(o.a)(this.stateObj,d.a)?i.f`
              <ha-labeled-slider
                caption=${this.hass.localize("ui.card.light.brightness")}
                icon="hass:brightness-5"
                min="1"
                max="255"
                value=${this._brightnessSliderValue}
                @change=${this._brightnessSliderChanged}
              ></ha-labeled-slider>
            `:""}
        ${"on"===this.stateObj.state?i.f`
              ${Object(o.a)(this.stateObj,d.c)?i.f`
                    <ha-labeled-slider
                      class="color_temp"
                      caption=${this.hass.localize("ui.card.light.color_temperature")}
                      icon="hass:thermometer"
                      .min=${this.stateObj.attributes.min_mireds}
                      .max=${this.stateObj.attributes.max_mireds}
                      .value=${this._ctSliderValue}
                      @change=${this._ctSliderChanged}
                    ></ha-labeled-slider>
                  `:""}
              ${Object(o.a)(this.stateObj,d.e)?i.f`
                    <ha-labeled-slider
                      caption=${this.hass.localize("ui.card.light.white_value")}
                      icon="hass:file-word-box"
                      max="255"
                      .value=${this._wvSliderValue}
                      @change=${this._wvSliderChanged}
                    ></ha-labeled-slider>
                  `:""}
              ${Object(o.a)(this.stateObj,d.b)?i.f`
                    <div class="segmentationContainer">
                      <ha-color-picker
                        class="color"
                        @colorselected=${this._colorPicked}
                        .desiredHsColor=${this._colorPickerColor}
                        throttle="500"
                        .hueSegments=${this._hueSegments}
                        .saturationSegments=${this._saturationSegments}
                      >
                      </ha-color-picker>
                      <ha-icon-button
                        icon="hass:palette"
                        @click=${this._segmentClick}
                        class="segmentationButton"
                      ></ha-icon-button>
                    </div>
                  `:""}
              ${Object(o.a)(this.stateObj,d.d)&&(null===(e=this.stateObj.attributes.effect_list)||void 0===e?void 0:e.length)?i.f`
                    <ha-paper-dropdown-menu
                      .label=${this.hass.localize("ui.card.light.effect")}
                    >
                      <paper-listbox
                        slot="dropdown-content"
                        .selected=${this.stateObj.attributes.effect||""}
                        @iron-select=${this._effectChanged}
                        attr-for-selected="item-name"
                        >${this.stateObj.attributes.effect_list.map(e=>i.f`
                            <paper-item .itemName=${e}
                              >${e}</paper-item
                            >
                          `)}
                      </paper-listbox>
                    </ha-paper-dropdown-menu>
                  `:""}
            `:""}
        <ha-attributes
          .stateObj=${this.stateObj}
          extra-filters="brightness,color_temp,white_value,effect_list,effect,hs_color,rgb_color,xy_color,min_mireds,max_mireds,entity_id"
        ></ha-attributes>
      </div>
    `:i.f``}},{kind:"method",key:"updated",value:function(e){const t=this.stateObj;e.has("stateObj")&&"on"===t.state&&(this._brightnessSliderValue=t.attributes.brightness,this._ctSliderValue=t.attributes.color_temp,this._wvSliderValue=t.attributes.white_value,t.attributes.hs_color&&(this._colorPickerColor={h:t.attributes.hs_color[0],s:t.attributes.hs_color[1]/100}))}},{kind:"method",key:"_effectChanged",value:function(e){const t=e.detail.item.itemName;t&&this.stateObj.attributes.effect!==t&&this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,effect:t})}},{kind:"method",key:"_brightnessSliderChanged",value:function(e){const t=parseInt(e.target.value,10);isNaN(t)||this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,brightness:t})}},{kind:"method",key:"_ctSliderChanged",value:function(e){const t=parseInt(e.target.value,10);isNaN(t)||this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,color_temp:t})}},{kind:"method",key:"_wvSliderChanged",value:function(e){const t=parseInt(e.target.value,10);isNaN(t)||this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,white_value:t})}},{kind:"method",key:"_segmentClick",value:function(){24===this._hueSegments&&8===this._saturationSegments?(this._hueSegments=0,this._saturationSegments=0):(this._hueSegments=24,this._saturationSegments=8)}},{kind:"method",key:"_colorPicked",value:function(e){this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,hs_color:[e.detail.hs.h,100*e.detail.hs.s]})}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      .content {
        display: flex;
        flex-direction: column;
        align-items: center;
      }

      .content.is-on {
        margin-top: -16px;
      }

      .content > * {
        width: 100%;
        max-height: 84px;
        overflow: hidden;
        padding-top: 16px;
      }

      .color_temp {
        --ha-slider-background: -webkit-linear-gradient(
          right,
          rgb(255, 160, 0) 0%,
          white 50%,
          rgb(166, 209, 255) 100%
        );
        /* The color temp minimum value shouldn't be rendered differently. It's not "off". */
        --paper-slider-knob-start-border-color: var(--primary-color);
      }

      .segmentationContainer {
        position: relative;
        max-height: 500px;
      }

      ha-color-picker {
        --ha-color-picker-wheel-borderwidth: 5;
        --ha-color-picker-wheel-bordercolor: white;
        --ha-color-picker-wheel-shadow: none;
        --ha-color-picker-marker-borderwidth: 2;
        --ha-color-picker-marker-bordercolor: white;
      }

      .segmentationButton {
        position: absolute;
        top: 5%;
        color: var(--secondary-text-color);
      }

      paper-item {
        cursor: pointer;
      }
    `}}]}}),i.a)}}]);
//# sourceMappingURL=chunk.e07d153dd012a5320720.js.map