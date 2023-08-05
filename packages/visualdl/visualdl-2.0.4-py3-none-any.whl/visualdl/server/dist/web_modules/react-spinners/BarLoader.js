import{g as y,c as x,a as l}from"../common/_commonjsHelpers-2c0027bd.js";import{r as O}from"../common/index-6f180876.js";import{c as a,h as s}from"../common/index-7febf921.js";import"../common/memoize.browser.esm-b0306449.js";var k=x(function(L,f){var c=l&&l.__makeTemplateObject||function(e,n){return Object.defineProperty?Object.defineProperty(e,"raw",{value:n}):e.raw=n,e},m=l&&l.__extends||function(){var e=function(n,t){return e=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(r,o){r.__proto__=o}||function(r,o){for(var i in o)o.hasOwnProperty(i)&&(r[i]=o[i])},e(n,t)};return function(n,t){e(n,t);function r(){this.constructor=n}n.prototype=t===null?Object.create(t):(r.prototype=t.prototype,new r)}}(),b=l&&l.__importStar||function(e){if(e&&e.__esModule)return e;var n={};if(e!=null)for(var t in e)Object.hasOwnProperty.call(e,t)&&(n[t]=e[t]);return n.default=e,n};Object.defineProperty(f,"__esModule",{value:!0});var v=b(O),j=a.keyframes(h||(h=c([`
  0% {left: -35%;right: 100%}
  60% {left: 100%;right: -90%}
  100% {left: 100%;right: -90%}
`],[`
  0% {left: -35%;right: 100%}
  60% {left: 100%;right: -90%}
  100% {left: 100%;right: -90%}
`]))),w=a.keyframes(d||(d=c([`
  0% {left: -200%;right: 100%}
  60% {left: 107%;right: -8%}
  100% {left: 107%;right: -8%}
`],[`
  0% {left: -200%;right: 100%}
  60% {left: 107%;right: -8%}
  100% {left: 107%;right: -8%}
`]))),p=function(e){m(n,e);function n(){var t=e!==null&&e.apply(this,arguments)||this;return t.style=function(r){var o=t.props,i=o.height,u=o.color;return a.css(_||(_=c([`
      position: absolute;
      height: `,`;
      overflow: hidden;
      background-color: `,`;
      background-clip: padding-box;
      display: block;
      border-radius: 2px;
      will-change: left, right;
      animation-fill-mode: forwards;
      animation: `," 2.1s ",`
        `,`
        infinite;
    `],[`
      position: absolute;
      height: `,`;
      overflow: hidden;
      background-color: `,`;
      background-clip: padding-box;
      display: block;
      border-radius: 2px;
      will-change: left, right;
      animation-fill-mode: forwards;
      animation: `," 2.1s ",`
        `,`
        infinite;
    `])),s.cssValue(i),u,r===1?j:w,r===2?"1.15s":"",r===1?"cubic-bezier(0.65, 0.815, 0.735, 0.395)":"cubic-bezier(0.165, 0.84, 0.44, 1)")},t.wrapper=function(){var r=t.props,o=r.width,i=r.height,u=r.color;return a.css(g||(g=c([`
      position: relative;
      width: `,`;
      height: `,`;
      overflow: hidden;
      background-color: `,`;
      background-clip: padding-box;
    `],[`
      position: relative;
      width: `,`;
      height: `,`;
      overflow: hidden;
      background-color: `,`;
      background-clip: padding-box;
    `])),s.cssValue(o),s.cssValue(i),s.calculateRgba(u,.2))},t}return n.prototype.render=function(){var t=this.props,r=t.loading,o=t.css;return r?a.jsx("div",{css:[this.wrapper(),o]},a.jsx("div",{css:this.style(1)}),a.jsx("div",{css:this.style(2)})):null},n.defaultProps=s.heightWidthDefaults(4,100),n}(v.PureComponent);f.Loader=p,f.default=p;var h,d,_,g}),P=y(k);export default P;
