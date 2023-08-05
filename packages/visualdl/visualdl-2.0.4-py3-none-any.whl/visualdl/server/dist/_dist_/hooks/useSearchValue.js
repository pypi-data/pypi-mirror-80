import i from"./useDebounce.js";const r=e=>Array.isArray(e)&&!e.length||typeof e=="string"&&e==="",o=(e,n=275)=>{const t=i(e,n);return r(e)||r(t)?e:t};export default o;
