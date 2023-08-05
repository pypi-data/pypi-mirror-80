(self.webpackJsonp=self.webpackJsonp||[]).push([[290],{866:function(t,e,s){"use strict";s.r(e);var a=s(3),i=s(4),r=s(32),o=s(596),n=s(222);s(645);class c extends r.a{static get template(){return i.a`
      <style>
        .child-card {
          margin-bottom: 8px;
        }

        .child-card:last-child {
          margin-bottom: 0;
        }
      </style>

      <div id="groupedControlDetails"></div>
      <template is="dom-repeat" items="[[states]]" as="state">
        <div class="child-card">
          <state-card-content
            state-obj="[[state]]"
            hass="[[hass]]"
          ></state-card-content>
        </div>
      </template>
    `}static get properties(){return{hass:{type:Object},stateObj:{type:Object},states:{type:Array,computed:"computeStates(stateObj, hass)"}}}static get observers(){return["statesChanged(stateObj, states)"]}computeStates(t,e){const s=[],a=t.attributes.entity_id||[];for(let i=0;i<a.length;i++){const t=e.states[a[i]];t&&s.push(t)}return s}statesChanged(t,e){let s=!1,i=!1;if(e&&e.length>0){const a=e.find(t=>"on"===t.state)||e[0];if(i=Object(n.a)(a),"group"!==i){s={...a,entity_id:t.entity_id,attributes:{...a.attributes}};for(let t=0;t<e.length;t++)if(i!==Object(n.a)(e[t])){s=!1;break}}}if(s)Object(o.a)(this.$.groupedControlDetails,"MORE-INFO-"+i.toUpperCase(),{stateObj:s,hass:this.hass});else{const t=Object(a.a)(this.$.groupedControlDetails);t.lastChild&&t.removeChild(t.lastChild)}}}customElements.define("more-info-group",c)}}]);
//# sourceMappingURL=chunk.0e54c41e8de3d47c010f.js.map