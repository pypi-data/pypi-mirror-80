(self.webpackJsonp=self.webpackJsonp||[]).push([[126],{210:function(e,t,r){"use strict";var i=r(0);function n(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function o(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function s(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function l(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function c(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var p=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!a(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return c(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?c(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:l(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=l(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var h=0;h<i.length;h++)p=i[h](p);var m=t((function(e){p.initializeInstanceElements(e,u.elements)}),r),u=p.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===l.key&&e.placement===l.placement},i=0;i<e.length;i++){var n,l=e[i];if("method"===l.kind&&(n=t.find(r)))if(s(l.descriptor)||s(n.descriptor)){if(a(l)||a(n))throw new ReferenceError("Duplicated methods ("+l.key+") can't be decorated.");n.descriptor=l.descriptor}else{if(a(l)){if(a(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+l.key+").");n.decorators=l.decorators}o(l,n)}else t.push(l)}return t}(m.d.map(n)),e);p.initializeClassElements(m.F,u.elements),p.runClassFinishers(m.F,u.finishers)}([Object(i.d)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"header",value:void 0},{kind:"field",decorators:[Object(i.h)({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 4px);
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 32px;
        padding: 24px 16px 16px;
        display: block;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return i.f`
      ${this.header?i.f` <div class="card-header">${this.header}</div> `:i.f``}
      <slot></slot>
    `}}]}}),i.a)},236:function(e,t,r){"use strict";var i=r(0),n=r(49);function o(e){var t,r=c(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function c(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function p(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!s(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return p(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?p(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=c(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var h=0;h<i.length;h++)n=i[h](n);var m=t((function(e){n.initializeInstanceElements(e,u.elements)}),r),u=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(l(o.descriptor)||l(n.descriptor)){if(s(o)||s(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(s(o)){if(s(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}a(o,n)}else t.push(o)}return t}(m.d.map(o)),e);n.initializeClassElements(m.F,u.elements),n.runClassFinishers(m.F,u.finishers)}([Object(i.d)("ha-config-section")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"isWide",value:()=>!1},{kind:"method",key:"render",value:function(){return i.f`
      <div
        class="content ${Object(n.a)({narrow:!this.isWide})}"
      >
        <div class="header"><slot name="header"></slot></div>
        <div
          class="together layout ${Object(n.a)({narrow:!this.isWide,vertical:!this.isWide,horizontal:this.isWide})}"
        >
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        display: block;
      }
      .content {
        padding: 28px 20px 0;
        max-width: 1040px;
        margin: 0 auto;
      }

      .layout {
        display: flex;
      }

      .horizontal {
        flex-direction: row;
      }

      .vertical {
        flex-direction: column;
      }

      .flex-auto {
        flex: 1 1 auto;
      }

      .header {
        font-family: var(--paper-font-headline_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-headline_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        letter-spacing: var(--paper-font-headline_-_letter-spacing);
        line-height: var(--paper-font-headline_-_line-height);
        opacity: var(--dark-primary-opacity);
      }

      .together {
        margin-top: 32px;
      }

      .intro {
        font-family: var(--paper-font-subhead_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-subhead_-_-webkit-font-smoothing
        );
        font-weight: var(--paper-font-subhead_-_font-weight);
        line-height: var(--paper-font-subhead_-_line-height);
        width: 100%;
        max-width: 400px;
        margin-right: 40px;
        opacity: var(--dark-primary-opacity);
        font-size: 14px;
        padding-bottom: 20px;
      }

      .panel {
        margin-top: -24px;
      }

      .panel ::slotted(*) {
        margin-top: 24px;
        display: block;
      }

      .narrow.content {
        max-width: 640px;
      }
      .narrow .together {
        margin-top: 20px;
      }
      .narrow .intro {
        padding-bottom: 20px;
        margin-right: 0;
        max-width: 500px;
      }
    `}}]}}),i.a)},978:function(e,t,r){"use strict";r.r(t);r(100),r(75),r(247);var i=r(112),n=r(4),o=r(32),a=r(11);const s=()=>Promise.all([r.e(1),r.e(5),r.e(186),r.e(63)]).then(r.bind(null,929));r(210),r(132),r(236);class l extends o.a{static get template(){return n.a`
      <style include="ha-style">
        app-toolbar {
          background-color: var(--primary-color);
        }
        div.content {
          background-color: var(--primary-background-color);
          width: 100%;
          min-height: 100%;
        }
        .galery_content {
          overflow: hidden;
          width: 100%;
          min-height: 80%;
          position: absolute;
        }
        figcaption {
          font-size: small;
        }
        img,
        video {
          width: 100%;
          max-width: 600px;
          object-fit: contain;
        }
        .image-viewer .btn {
          position: absolute;
          transform: translate(-50%, -50%);
          -ms-transform: translate(-50%, -50%);
          background-color: #555;
          color: white;
          font-size: 16px;
          padding: 12px 12px;
          border: none;
          cursor: pointer;
          border-radius: 5px;
          opacity: 0;
          transition: opacity 0.35s ease;
        }
        .image-viewer:hover .btn {
          opacity: 1;
        }
        .image-viewer .btn-left {
          left: 0%;
          margin-left: 65px;
        }
        .image-viewer .btn-right {
          right: 0%;
          margin-right: 30px;
        }
        figure.selected {
          opacity: 0.5;
        }
        figure:hover {
          cursor: pointer;
        }
        .duration {
          font-style: italic;
        }
        @media all and (max-width: 600px) {
          .image-viewer {
            width: 100%;
            max-width: 400px;
            margin: auto;
          }
          .image-viewer .btn {
            top: 33%;
          }
          .image-menu {
            width: 100%;
            max-width: 300px;
            overflow-y: hidden;
            overflow-x: scroll;
            display: flex;
          }
          .image-menu figure {
            margin: 0px;
            padding: 12px;
          }
        }

        @media all and (min-width: 600px) {
          .image-viewer {
            width: 75%;
            max-width: 500px;
            position: relative;
            margin: auto;
          }
          .image-viewer .btn {
            top: 40%;
          }

          .image-menu {
            width: 25%;
            max-width: 300px;
            height: calc(100vh - 120px);
            overflow-y: scroll;
            position: absolute;
            top: 0px;
            right: 0px;
          }
        }

        @media all and (max-width: 800px) {
          img,
          video {
            width: 100%;
            max-width: 300px;
          }
          .image-viewer {
            width: 75%;
            max-width: 300px;
          }
          div.image-menu > img,
          video {
            width: 100%;
            max-width: 150px;
          }
        }

        mwc-fab {
          position: fixed;
          bottom: 16px;
          right: 16px;
          z-index: 1;
        }

        mwc-fab[is-wide] {
          bottom: 24px;
          right: 24px;
        }
        ha-icon-button {
          vertical-align: middle;
        }
      </style>
      <div class="content">
        <app-toolbar>
          <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
          <div main-title>[[panel.title]]</div>
          <ha-icon-button
            aria-label="Instrukcja"
            icon="mdi:information-outline"
            on-click="_showHelp"
          ></ha-icon-button>
        </app-toolbar>
        <div class="galery_content" id="content">
          <template is="dom-if" if="[[showImages]]">
            <div class="image-viewer">
              <figure>
                <img
                  src="{{currentImage.path}}"
                  hidden$="[[isVideo(currentImage.extension)]]"
                />
                <video
                  controls
                  src="{{currentImage.path}}#t=0.1"
                  hidden$="[[!isVideo(currentImage.extension)]]"
                  on-loadedmetadata="videoLoaded"
                  on-canplay="startVideo"
                ></video>
                <figcaption>
                  <span style="display: block; text-align: right;">
                    <ha-icon-button
                      icon="mdi:image-edit-outline"
                      on-click="_editImage"
                      title="Edycja"
                    ></ha-icon-button>
                    <ha-icon-button
                      icon="hass:delete"
                      on-click="_deleteImage"
                    ></ha-icon-button
                    ><br /> </span
                  ><br />
                  URLs:<br />
                  <ha-icon-button icon="mdi:monitor-dashboard"></ha-icon-button>
                  {{currentImage.path}}<br />
                  <ha-icon-button
                    icon="mdi:home-import-outline"
                  ></ha-icon-button>
                  http://{{aisLocalIP}}{{currentImage.path}}<br />
                  <ha-icon-button
                    icon="mdi:weather-cloudy-arrow-right"
                  ></ha-icon-button>
                  {{remoteDomain}}{{currentImage.path}}
                  <span
                    class="duration"
                    hidden$="[[!isVideo(currentImage.extension)]]"
                  ></span>
                </figcaption>
              </figure>
              <button class="btn btn-left" on-click="previousImage">
                &lt;
              </button>
              <button class="btn btn-right" on-click="nextImage">
                &gt;
              </button>
            </div>
          </template>
          <div class="image-menu">
            <template is="dom-repeat" items="{{images}}">
              <figure
                id="image[[item.index]]"
                data-imageIndex="{{item.index}}"
                on-click="imageMenuClick"
                class$="[[getImageMenuClass(item, currentImgIdx)]]"
              >
                <img
                  src="{{item.path}}"
                  hidden$="[[isVideo(item.extension)]]"
                />
                <video
                  src="{{item.path}}#t=0.1"
                  hidden$="[[!isVideo(item.extension)]]"
                  on-loadedmetadata="videoLoaded"
                ></video>
                <figcaption>
                  {{item.date}}
                  <span
                    class="duration"
                    hidden$="[[!isVideo(item.extension)]]"
                  ></span>
                </figcaption>
              </figure>
            </template>
          </div>
        </div>
        <mwc-fab
          slot="fab"
          is-wide$="[[isWide]]"
          title="[[localize('ui.common.add')]]"
          on-click="addImage"
        >
          <ha-svg-icon slot="icon" path="[[addIcon()]]"></ha-svg-icon>
        </mwc-fab>
      </div>
    `}static get properties(){return{hass:Object,narrow:Boolean,showMenu:{type:Boolean,value:!1},aisLocalIP:{type:String,computed:"_computeAisLocalIP(hass)"},remoteDomain:{type:String,computed:"_computeRemoteDomain(hass)"},panel:Object,images:{type:Object,computed:"getImages(hass)"},currentImage:Object,currentImgIdx:{type:Number,computed:"getcurrentImgIdx(hass)"},autoPlayVideo:{type:Boolean,value:!1},showImages:Boolean}}async _deleteImage(){const e=this.getImage(this.currentImgIdx);await this.hass.callService("ais_files","remove_file",{path:e.path})}async _editImage(){const e=this.getImage(this.currentImgIdx);window.open("/static/ais_dom/design_tool/index.html?img="+e.path,"_blank").focus()}async _showHelp(){window.open("https://www.ai-speaker.com/docs/ais_app_integration_gallery/","_blank").focus()}_computeAisLocalIP(e){return e.states["sensor.internal_ip_address"].state}_computeRemoteDomain(e){return this.aisSecureAndroidId=e.states["sensor.ais_secure_android_id_dom"].state,"https://"+this.aisSecureAndroidId+".paczka.pro"}addIcon(){return i.Mb}addImage(){var e;e=this,Object(a.a)(e,"show-dialog",{dialogTag:"ha-dialog-aisgalery",dialogImport:s,dialogParams:{}})}getImage(e){return void 0!==this.images&&void 0!==e?this.images[e]:0}isVideo(e){return!!e&&["mp4","webm"].includes(e)}imageMenuClick(e){this.autoPlayVideo=!0,this.setcurrentImgIdx(e.model.item.index)}previousImage(){let e=0;this.autoPlayVideo=!0,e=0===this.currentImgIdx?this.images.length-1:Number(this.currentImgIdx)-1,this.setcurrentImgIdx(e)}nextImage(){let e=0;this.autoPlayVideo=!0,e=this.currentImgIdx>=this.images.length-1?0:Number(this.currentImgIdx)+1,this.setcurrentImgIdx(e)}ready(){super.ready(),this.autoPlayVideo=!1,this.setcurrentImgIdx(0)}setcurrentImgIdx(e){this.hass.callService("ais_files","pick_file",{idx:e}),this.getImages(this.hass),this.currentImage=this.getImage(e)}getcurrentImgIdx(e){try{const t=Number(e.states["sensor.ais_gallery_img"].state);return this.currentImage=this.getImage(t),t}catch(t){return 0}}getImages(e){let t=[];try{t=e.states["sensor.ais_gallery_img"].attributes.fileList}catch(i){console.log("getImages error: "+i)}const r=[];for(let n=t.length-1;n>=0;n--){const e=t[n],i=e.split("/");let o=i[i.length-1];const a=o.split("."),s=a[a.length-1].toLowerCase();o=o.substring(0,o.length-s.length-1);const l={path:e,name:o,extension:s,date:o,index:r.length};r.push(l)}return r.length>0?this.showImages=!0:this.showImages=!1,r}getImageMenuClass(e,t){return e.index===t?"selected":""}videoLoaded(e){this.getVideoDuration(e)}getVideoDuration(e){let t=parseInt(e.target.duration/60);t<10&&(t="0"+t);let r=parseInt(e.target.duration%60);r="0"+r,r=r.substring(r.length-2),e.target.parentNode.querySelector(".duration").innerHTML="["+t+":"+r+"]"}startVideo(e){this.autoPlayVideo&&e.target.play()}}customElements.define("ha-panel-aisgalery",l)}}]);
//# sourceMappingURL=chunk.327bc5e1b69b4709ac4f.js.map