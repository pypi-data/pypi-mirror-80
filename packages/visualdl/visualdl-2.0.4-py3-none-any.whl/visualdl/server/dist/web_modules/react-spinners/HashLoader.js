import{g as j,c as g,a as l}from"../common/_commonjsHelpers-2c0027bd.js";import{r as y}from"../common/index-6f180876.js";import{h as p,c as x}from"../common/index-7febf921.js";import"../common/memoize.browser.esm-b0306449.js";var O=g(function(k,u){var v=l&&l.__extends||function(){var o=function(s,e){return o=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(n,t){n.__proto__=t}||function(n,t){for(var a in t)t.hasOwnProperty(a)&&(n[a]=t[a])},o(s,e)};return function(s,e){o(s,e);function n(){this.constructor=s}s.prototype=e===null?Object.create(e):(n.prototype=e.prototype,new n)}}(),c=l&&l.__makeTemplateObject||function(o,s){return Object.defineProperty?Object.defineProperty(o,"raw",{value:s}):o.raw=s,o},m=l&&l.__importStar||function(o){if(o&&o.__esModule)return o;var s={};if(o!=null)for(var e in o)Object.hasOwnProperty.call(o,e)&&(s[e]=o[e]);return s.default=o,s};Object.defineProperty(u,"__esModule",{value:!0});var b=m(y),w=function(o){v(s,o);function s(){var e=o!==null&&o.apply(this,arguments)||this;return e.thickness=function(){var n=e.props.size,t=p.parseLengthAndUnit(n).value;return t/5},e.lat=function(){var n=e.props.size,t=p.parseLengthAndUnit(n).value;return(t-e.thickness())/2},e.offset=function(){return e.lat()-e.thickness()},e.color=function(){var n=e.props.color;return p.calculateRgba(n,.75)},e.before=function(){var n=e.props.size,t=e.color(),a=e.lat(),i=e.thickness(),r=e.offset();return x.keyframes(f||(f=c([`
      0% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {width: `,";box-shadow: 0 ","px ",", 0 ","px ",`}
      70% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `],[`
      0% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {width: `,";box-shadow: 0 ","px ",", 0 ","px ",`}
      70% {width: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `])),i,a,-r,t,-a,r,t,p.cssValue(n),-r,t,r,t,i,-a,-r,t,a,r,t,a,-r,t,-a,r,t)},e.after=function(){var n=e.props.size,t=e.color(),a=e.lat(),i=e.thickness(),r=e.offset();return x.keyframes(h||(h=c([`
      0% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {height: `,";box-shadow: ","px 0 ",", ","px 0 ",`}
      70% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `],[`
      0% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      35% {height: `,";box-shadow: ","px 0 ",", ","px 0 ",`}
      70% {height: `,"px;box-shadow: ","px ","px ",", ","px ","px ",`}
      100% {box-shadow: `,"px ","px ",", ","px ","px ",`}
    `])),i,r,a,t,-r,-a,t,p.cssValue(n),r,t,-r,t,i,r,-a,t,-r,a,t,r,a,t,-r,-a,t)},e.style=function(n){var t=e.props.size,a=p.parseLengthAndUnit(t),i=a.value,r=a.unit;return x.css(d||(d=c([`
      position: absolute;
      content: "";
      top: 50%;
      left: 50%;
      display: block;
      width: `,`;
      height: `,`;
      border-radius: `,`;
      transform: translate(-50%, -50%);
      animation-fill-mode: none;
      animation: `,` 2s infinite;
    `],[`
      position: absolute;
      content: "";
      top: 50%;
      left: 50%;
      display: block;
      width: `,`;
      height: `,`;
      border-radius: `,`;
      transform: translate(-50%, -50%);
      animation-fill-mode: none;
      animation: `,` 2s infinite;
    `])),""+i/5+r,""+i/5+r,""+i/10+r,n===1?e.before():e.after())},e.wrapper=function(){var n=e.props.size;return x.css(_||(_=c([`
      position: relative;
      width: `,`;
      height: `,`;
      transform: rotate(165deg);
    `],[`
      position: relative;
      width: `,`;
      height: `,`;
      transform: rotate(165deg);
    `])),p.cssValue(n),p.cssValue(n))},e}return s.prototype.render=function(){var e=this.props,n=e.loading,t=e.css;return n?x.jsx("div",{css:[this.wrapper(),t]},x.jsx("div",{css:this.style(1)}),x.jsx("div",{css:this.style(2)})):null},s.defaultProps=p.sizeDefaults(50),s}(b.PureComponent);u.default=w;var f,h,d,_}),z=j(O);export default z;
