/*! For license information please see chunk.97905d75268763f4c192.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[240],{157:function(e,t,a){"use strict";a(5),a(39),a(140),a(75),a(160),a(145),a(52),a(186),a(187);var n=a(67),r=a(44),o=a(68),i=a(69),s=a(6),l=a(3),p=a(40),c=a(4);Object(s.a)({_template:c.a`
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
`,is:"paper-dropdown-menu",behaviors:[n.a,r.a,o.a,i.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(l.a)(this.$.content).getDistributedNodes(),t=0,a=e.length;t<a;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){p.c(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},189:function(e,t,a){"use strict";a(157);const n=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends n{ready(){super.ready(),setTimeout(()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")},100)}})},192:function(e,t,a){"use strict";a(168);const n=customElements.get("paper-slider");customElements.define("ha-paper-slider",class extends n{static get template(){const e=document.createElement("template");e.innerHTML=n.template.innerHTML;const t=document.createElement("style");return t.innerHTML='\n      .pin > .slider-knob > .slider-knob-inner {\n        font-size:  var(--ha-paper-slider-pin-font-size, 10px);\n        line-height: normal;\n      }\n\n      .disabled.ring > .slider-knob > .slider-knob-inner {\n        background-color: var(--paper-slider-disabled-knob-color, var(--paper-grey-400));\n        border: 2px solid var(--paper-slider-disabled-knob-color, var(--paper-grey-400));\n      }\n\n      .pin > .slider-knob > .slider-knob-inner::before {\n        top: unset;\n        margin-left: unset;\n\n        bottom: calc(15px + var(--calculated-paper-slider-height)/2);\n        left: 50%;\n        width: 2.2em;\n        height: 2.2em;\n\n        -webkit-transform-origin: left bottom;\n        transform-origin: left bottom;\n        -webkit-transform: rotate(-45deg) scale(0) translate(0);\n        transform: rotate(-45deg) scale(0) translate(0);\n      }\n\n      .pin.expand > .slider-knob > .slider-knob-inner::before {\n        -webkit-transform: rotate(-45deg) scale(1) translate(7px, -7px);\n        transform: rotate(-45deg) scale(1) translate(7px, -7px);\n      }\n\n      .pin > .slider-knob > .slider-knob-inner::after {\n        top: unset;\n        font-size: unset;\n\n        bottom: calc(15px + var(--calculated-paper-slider-height)/2);\n        left: 50%;\n        margin-left: -1.1em;\n        width: 2.2em;\n        height: 2.1em;\n\n        -webkit-transform-origin: center bottom;\n        transform-origin: center bottom;\n        -webkit-transform: scale(0) translate(0);\n        transform: scale(0) translate(0);\n      }\n\n      .pin.expand > .slider-knob > .slider-knob-inner::after {\n        -webkit-transform: scale(1) translate(0, -10px);\n        transform: scale(1) translate(0, -10px);\n      }\n\n      :host([dir="rtl"]) .pin.expand > .slider-knob > .slider-knob-inner::after {\n        -webkit-transform: scale(1) translate(0, -17px) scaleX(-1) !important;\n        transform: scale(1) translate(0, -17px) scaleX(-1) !important;\n        }\n\n        .slider-input {\n          width: 54px;\n        }\n    ',e.content.appendChild(t),e}})},226:function(e,t,a){"use strict";a.d(t,"a",(function(){return o}));var n=a(9),r=a(11);const o=Object(n.a)(e=>class extends e{fire(e,t,a){return a=a||{},Object(r.a)(a.node||this,e,t,a)}})},546:function(e,t,a){"use strict";a.d(t,"a",(function(){return r}));var n=a(293);const r=(e,t)=>e&&e.attributes.supported_features?Object.keys(t).map(a=>Object(n.a)(e,Number(a))?t[a]:"").filter(e=>""!==e).join(" "):""},987:function(e,t,a){"use strict";a.r(t);a(290),a(139),a(144);var n=a(12),r=a(22),o=a(4),i=a(32),s=a(546),l=a(293),p=(a(189),a(192),a(234),a(183),a(226));class c extends(Object(p.a)(i.a)){static get template(){return o.a`
      <style include="iron-flex iron-flex-alignment"></style>
      <style>
        /* local DOM styles go here */
        :host {
          @apply --layout-flex;
          @apply --layout-horizontal;
          @apply --layout-justified;
        }
        .in-flux#target_temperature {
          color: var(--error-color);
        }
        #target_temperature {
          @apply --layout-self-center;
          font-size: 200%;
        }
        .control-buttons {
          font-size: 200%;
          text-align: right;
        }
        ha-icon-button {
          height: 48px;
          width: 48px;
        }
      </style>

      <!-- local DOM goes here -->
      <div id="target_temperature">[[value]] [[units]]</div>
      <div class="control-buttons">
        <div>
          <ha-icon-button
            icon="hass:chevron-up"
            on-click="incrementValue"
          ></ha-icon-button>
        </div>
        <div>
          <ha-icon-button
            icon="hass:chevron-down"
            on-click="decrementValue"
          ></ha-icon-button>
        </div>
      </div>
    `}static get properties(){return{value:{type:Number,observer:"valueChanged"},units:{type:String},min:{type:Number},max:{type:Number},step:{type:Number,value:1}}}temperatureStateInFlux(e){this.$.target_temperature.classList.toggle("in-flux",e)}incrementValue(){const e=this.value+this.step;this.value<this.max&&(this.last_changed=Date.now(),this.temperatureStateInFlux(!0)),e<=this.max?e<=this.min?this.value=this.min:this.value=e:this.value=this.max}decrementValue(){const e=this.value-this.step;this.value>this.min&&(this.last_changed=Date.now(),this.temperatureStateInFlux(!0)),e>=this.min?this.value=e:this.value=this.min}valueChanged(){this.last_changed&&window.setTimeout(()=>{Date.now()-this.last_changed>=2e3&&(this.fire("change"),this.temperatureStateInFlux(!1),this.last_changed=null)},2010)}}customElements.define("ha-water_heater-control",c);var d=a(219);class u extends(Object(d.a)(Object(p.a)(i.a))){static get template(){return o.a`
      <style include="iron-flex"></style>
      <style>
        :host {
          color: var(--primary-text-color);
        }

        ha-paper-dropdown-menu {
          width: 100%;
        }

        paper-item {
          cursor: pointer;
        }

        ha-paper-slider {
          width: 100%;
        }

        ha-water_heater-control.range-control-left,
        ha-water_heater-control.range-control-right {
          float: left;
          width: 46%;
        }
        ha-water_heater-control.range-control-left {
          margin-right: 4%;
        }
        ha-water_heater-control.range-control-right {
          margin-left: 4%;
        }

        .single-row {
          padding: 8px 0;
        }
        }
      </style>

      <div class$="[[computeClassNames(stateObj)]]">
        <div class="container-temperature">
          <div class$="[[stateObj.attributes.operation_mode]]">
            <div hidden$="[[!supportsTemperatureControls(stateObj)]]">
              [[localize('ui.card.water_heater.target_temperature')]]
            </div>
            <template is="dom-if" if="[[supportsTemperature(stateObj)]]">
              <ha-water_heater-control
                value="[[stateObj.attributes.temperature]]"
                units="[[hass.config.unit_system.temperature]]"
                step="[[computeTemperatureStepSize(hass, stateObj)]]"
                min="[[stateObj.attributes.min_temp]]"
                max="[[stateObj.attributes.max_temp]]"
                on-change="targetTemperatureChanged"
              >
              </ha-water_heater-control>
            </template>
          </div>
        </div>

        <template is="dom-if" if="[[supportsOperationMode(stateObj)]]">
          <div class="container-operation_list">
            <div class="controls">
              <ha-paper-dropdown-menu
                label-float=""
                dynamic-align=""
                label="[[localize('ui.card.water_heater.operation')]]"
              >
                <paper-listbox
                  slot="dropdown-content"
                  selected="[[stateObj.attributes.operation_mode]]"
                  attr-for-selected="item-name"
                  on-selected-changed="handleOperationmodeChanged"
                >
                  <template
                    is="dom-repeat"
                    items="[[stateObj.attributes.operation_list]]"
                  >
                    <paper-item item-name$="[[item]]"
                      >[[_localizeOperationMode(localize, item)]]</paper-item
                    >
                  </template>
                </paper-listbox>
              </ha-paper-dropdown-menu>
            </div>
          </div>
        </template>

        <template is="dom-if" if="[[supportsAwayMode(stateObj)]]">
          <div class="container-away_mode">
            <div class="center horizontal layout single-row">
              <div class="flex">
                [[localize('ui.card.water_heater.away_mode')]]
              </div>
              <ha-switch
                checked="[[awayToggleChecked]]"
                on-change="awayToggleChanged"
              >
              </ha-switch>
            </div>
          </div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},stateObj:{type:Object,observer:"stateObjChanged"},awayToggleChecked:Boolean}}stateObjChanged(e,t){e&&this.setProperties({awayToggleChecked:"on"===e.attributes.away_mode}),t&&(this._debouncer=r.a.debounce(this._debouncer,n.d.after(500),()=>{this.fire("iron-resize")}))}computeTemperatureStepSize(e,t){return t.attributes.target_temp_step?t.attributes.target_temp_step:-1!==e.config.unit_system.temperature.indexOf("F")?1:.5}supportsTemperatureControls(e){return this.supportsTemperature(e)}supportsTemperature(e){return Object(l.a)(e,1)&&"number"==typeof e.attributes.temperature}supportsOperationMode(e){return Object(l.a)(e,2)}supportsAwayMode(e){return Object(l.a)(e,4)}computeClassNames(e){const t=[Object(s.a)(e,{1:"has-target_temperature",2:"has-operation_mode",4:"has-away_mode"})];return t.push("more-info-water_heater"),t.join(" ")}targetTemperatureChanged(e){const t=e.target.value;t!==this.stateObj.attributes.temperature&&this.callServiceHelper("set_temperature",{temperature:t})}awayToggleChanged(e){const t="on"===this.stateObj.attributes.away_mode,a=e.target.checked;t!==a&&this.callServiceHelper("set_away_mode",{away_mode:a})}handleOperationmodeChanged(e){const t=this.stateObj.attributes.operation_mode,a=e.detail.value;a&&t!==a&&this.callServiceHelper("set_operation_mode",{operation_mode:a})}callServiceHelper(e,t){t.entity_id=this.stateObj.entity_id,this.hass.callService("water_heater",e,t).then(()=>{this.stateObjChanged(this.stateObj)})}_localizeOperationMode(e,t){return e("component.water_heater.state._."+t)||t}}customElements.define("more-info-water_heater",u)}}]);
//# sourceMappingURL=chunk.97905d75268763f4c192.js.map