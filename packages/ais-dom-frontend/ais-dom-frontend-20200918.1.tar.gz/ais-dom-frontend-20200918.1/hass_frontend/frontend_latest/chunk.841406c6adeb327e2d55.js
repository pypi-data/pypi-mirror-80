(self.webpackJsonp=self.webpackJsonp||[]).push([[261],{401:function(e,t,i){"use strict";i.d(t,"a",(function(){return n}));const r=e=>{const t=parseFloat(e);if(isNaN(t))throw new Error(e+" is not a number");return t};function n(e){if(!e)return null;try{if(e.endsWith("%"))return{w:100,h:r(e.substr(0,e.length-1))};const t=e.replace(":","x").split("x");return 0===t.length?null:1===t.length?{w:r(t[0]),h:1}:{w:r(t[0]),h:r(t[1])}}catch(t){}return null}},490:function(e,t,i){"use strict";var r=i(0),n=i(49),o=i(88),a=i(212),s=i(401),c=(i(504),i(500)),l=i(221);function d(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function v(e,t,i){return(v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!f(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(u(o.descriptor)||u(n.descriptor)){if(f(o)||f(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(f(o)){if(f(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}h(o,n)}else t.push(o)}return t}(a.d.map(d)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([Object(r.d)("hui-image")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(r.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"entity",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"image",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"stateImage",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"cameraImage",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"cameraView",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"aspectRatio",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"filter",value:void 0},{kind:"field",decorators:[Object(r.h)()],key:"stateFilter",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_loadError",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_cameraImageSrc",value:void 0},{kind:"field",decorators:[Object(r.i)("img")],key:"_image",value:void 0},{kind:"field",key:"_lastImageHeight",value:void 0},{kind:"field",key:"_cameraUpdater",value:void 0},{kind:"method",key:"connectedCallback",value:function(){v(g(i.prototype),"connectedCallback",this).call(this),this.cameraImage&&"live"!==this.cameraView&&this._startUpdateCameraInterval()}},{kind:"method",key:"disconnectedCallback",value:function(){v(g(i.prototype),"disconnectedCallback",this).call(this),this._stopUpdateCameraInterval()}},{kind:"method",key:"render",value:function(){if(!this.hass)return r.f``;const e=this.aspectRatio?Object(s.a)(this.aspectRatio):null,t=this.entity?this.hass.states[this.entity]:void 0,i=t?t.state:l.b;let c,d,h=!this.stateImage;if(this.cameraImage)"live"===this.cameraView?d=this.hass.states[this.cameraImage]:c=this._cameraImageSrc;else if(this.stateImage){const e=this.stateImage[i];e?c=e:(c=this.image,h=!0)}else c=this.image;c&&(c=this.hass.hassUrl(c));let f=this.filter||"";if(this.stateFilter&&this.stateFilter[i]&&(f=this.stateFilter[i]),!f&&this.entity){f=(!t||a.i.includes(i))&&h?"grayscale(100%)":""}return r.f`
      <div
        style=${Object(o.a)({paddingBottom:e&&e.w>0&&e.h>0?(100*e.h/e.w).toFixed(2)+"%":""})}
        class=${Object(n.a)({ratio:Boolean(e&&e.w>0&&e.h>0)})}
      >
        ${this.cameraImage&&"live"===this.cameraView?r.f`
              <ha-camera-stream
                muted
                .hass=${this.hass}
                .stateObj=${d}
              ></ha-camera-stream>
            `:r.f`
              <img
                id="image"
                src=${c}
                @error=${this._onImageError}
                @load=${this._onImageLoad}
                style=${Object(o.a)({filter:f,display:this._loadError?"none":"block"})}
              />
            `}
        <div
          id="brokenImage"
          style=${Object(o.a)({height:(this._lastImageHeight||"100")+"px",display:this._loadError?"block":"none"})}
        ></div>
      </div>
    `}},{kind:"method",key:"updated",value:function(e){if(e.has("hass")){const t=e.get("hass");t&&t.connected===this.hass.connected||(this.hass.connected&&"live"!==this.cameraView?(this._updateCameraImageSrc(),this._startUpdateCameraInterval()):this.hass.connected||(this._stopUpdateCameraInterval(),this._cameraImageSrc=void 0,this._loadError=!0))}else e.has("cameraImage")&&"live"!==this.cameraView&&(this._updateCameraImageSrc(),this._startUpdateCameraInterval())}},{kind:"method",key:"_startUpdateCameraInterval",value:function(){this._stopUpdateCameraInterval(),this.cameraImage&&this.isConnected&&(this._cameraUpdater=window.setInterval(()=>this._updateCameraImageSrc(),1e4))}},{kind:"method",key:"_stopUpdateCameraInterval",value:function(){this._cameraUpdater&&(clearInterval(this._cameraUpdater),this._cameraUpdater=void 0)}},{kind:"method",key:"_onImageError",value:function(){this._loadError=!0}},{kind:"method",key:"_onImageLoad",value:async function(){this._loadError=!1,await this.updateComplete,this._lastImageHeight=this._image.offsetHeight}},{kind:"method",key:"_updateCameraImageSrc",value:async function(){if(!this.hass||!this.cameraImage)return;this.hass.states[this.cameraImage]?this._cameraImageSrc=await Object(c.e)(this.hass,this.cameraImage):this._onImageError()}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      img {
        display: block;
        height: auto;
        transition: filter 0.2s linear;
        width: 100%;
      }

      .ratio {
        position: relative;
        width: 100%;
        height: 0;
      }

      .ratio img,
      .ratio div {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }

      #brokenImage {
        background: grey url("/static/images/image-broken.svg") center/36px
          no-repeat;
      }
    `}}]}}),r.a)},890:function(e,t,i){"use strict";i.r(t);var r=i(0),n=i(49),o=i(213),a=i(212),s=i(104),c=i(155),l=i(239),d=i(211),h=i(230),f=(i(210),i(183),i(243)),u=i(245),p=i(252),m=i(251),y=i(232),v=i(291),g=(i(490),i(225));i(375);function b(e){var t,i=O(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function w(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function E(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function O(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function j(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function x(e,t,i){return(x="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function C(e){return(C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const I=new Set(["closed","locked","not_home","off"]);!function(e,t,i,r){var n=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!w(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return j(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?j(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=O(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:E(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=E(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(_(o.descriptor)||_(n.descriptor)){if(w(o)||w(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(w(o)){if(w(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}k(o,n)}else t.push(o)}return t}(a.d.map(b)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([Object(r.d)("hui-picture-glance-card")],(function(e,t){class b extends t{constructor(...t){super(...t),e(this)}}return{F:b,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([i.e(0),i.e(1),i.e(3),i.e(4),i.e(97)]).then(i.bind(null,800)),document.createElement("hui-picture-glance-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,i){return{type:"picture-glance",title:"Kitchen",image:"https://demo.home-assistant.io/stub_config/kitchen.png",entities:Object(u.a)(e,2,t,i,["sensor","binary_sensor"])}}},{kind:"field",decorators:[Object(r.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_config",value:void 0},{kind:"field",key:"_entitiesDialog",value:void 0},{kind:"field",key:"_entitiesToggle",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(!e||!e.entities||!Array.isArray(e.entities)||!(e.image||e.camera_image||e.state_image)||e.state_image&&!e.entity)throw new Error("Invalid card configuration");const t=Object(v.a)(e.entities);this._entitiesDialog=[],this._entitiesToggle=[],t.forEach(t=>{e.force_dialog||!a.e.has(Object(c.a)(t.entity))?this._entitiesDialog.push(t):this._entitiesToggle.push(t)}),this._config={hold_action:{action:"more-info"},...e}}},{kind:"method",key:"shouldUpdate",value:function(e){if(Object(y.b)(this,e))return!0;const t=e.get("hass");if(!t||t.themes!==this.hass.themes||t.language!==this.hass.language)return!0;if(this._entitiesDialog)for(const i of this._entitiesDialog)if(t.states[i.entity]!==this.hass.states[i.entity])return!0;if(this._entitiesToggle)for(const i of this._entitiesToggle)if(t.states[i.entity]!==this.hass.states[i.entity])return!0;return!1}},{kind:"method",key:"updated",value:function(e){if(x(C(b.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),i=e.get("_config");t&&i&&t.themes===this.hass.themes&&i.theme===this._config.theme||Object(s.a)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?r.f`
      <ha-card>
        <hui-image
          class=${Object(n.a)({clickable:Boolean(this._config.tap_action||this._config.hold_action||this._config.camera_image)})}
          @action=${this._handleAction}
          .actionHandler=${Object(f.a)({hasHold:Object(m.a)(this._config.hold_action),hasDoubleClick:Object(m.a)(this._config.double_tap_action)})}
          tabindex=${Object(o.a)(Object(m.a)(this._config.tap_action)?"0":void 0)}
          .config=${this._config}
          .hass=${this.hass}
          .image=${this._config.image}
          .stateImage=${this._config.state_image}
          .stateFilter=${this._config.state_filter}
          .cameraImage=${this._config.camera_image}
          .cameraView=${this._config.camera_view}
          .entity=${this._config.entity}
          .aspectRatio=${this._config.aspect_ratio}
        ></hui-image>
        <div class="box">
          ${this._config.title?r.f` <div class="title">${this._config.title}</div> `:""}
          <div class="row">
            ${this._entitiesDialog.map(e=>this.renderEntity(e,!0))}
          </div>
          <div class="row">
            ${this._entitiesToggle.map(e=>this.renderEntity(e,!1))}
          </div>
        </div>
      </ha-card>
    `:r.f``}},{kind:"method",key:"renderEntity",value:function(e,t){const i=this.hass.states[e.entity];return e={tap_action:{action:t?"more-info":"toggle"},hold_action:{action:"more-info"},...e},i?r.f`
      <div class="wrapper">
        <ha-icon-button
          @action=${this._handleAction}
          .actionHandler=${Object(f.a)({hasHold:Object(m.a)(e.hold_action),hasDoubleClick:Object(m.a)(e.double_tap_action)})}
          tabindex=${Object(o.a)(Object(m.a)(e.tap_action)?void 0:"-1")}
          .disabled=${!Object(m.a)(e.tap_action)}
          .config=${e}
          class=${Object(n.a)({"state-on":!I.has(i.state)})}
          .icon=${e.icon||Object(h.a)(i)}
          title=${`\n            ${Object(d.a)(i)} : ${Object(l.a)(this.hass.localize,i,this.hass.language)}\n          `}
        ></ha-icon-button>
        ${!0!==this._config.show_state&&!0!==e.show_state?r.f` <div class="state"></div> `:r.f`
              <div class="state">
                ${e.attribute?r.f`
                      ${e.prefix}${i.attributes[e.attribute]}${e.suffix}
                    `:Object(l.a)(this.hass.localize,i,this.hass.language)}
              </div>
            `}
      </div>
    `:r.f`
        <hui-warning-element
          .label=${Object(g.a)(this.hass,e.entity)}
        ></hui-warning-element>
      `}},{kind:"method",key:"_handleAction",value:function(e){const t=e.currentTarget.config;Object(p.a)(this,this.hass,t,e.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      ha-card {
        position: relative;
        min-height: 48px;
        overflow: hidden;
      }

      hui-image.clickable {
        cursor: pointer;
      }

      .box {
        /* start paper-font-common-nowrap style */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        /* end paper-font-common-nowrap style */

        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.3);
        padding: 4px 8px;
        font-size: 16px;
        line-height: 40px;
        color: white;
        display: flex;
        justify-content: space-between;
        flex-direction: row;
      }

      .box .title {
        font-weight: 500;
        margin-left: 8px;
      }

      ha-icon-button {
        --mdc-icon-button-size: 40px;
        --disabled-text-color: currentColor;
        color: #a9a9a9;
      }

      ha-icon-button.state-on {
        color: white;
      }
      .state {
        display: block;
        font-size: 12px;
        text-align: center;
        line-height: 12px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .row {
        display: flex;
        flex-direction: row;
      }
      .wrapper {
        display: flex;
        flex-direction: column;
        width: 40px;
      }
    `}}]}}),r.a)}}]);
//# sourceMappingURL=chunk.841406c6adeb327e2d55.js.map