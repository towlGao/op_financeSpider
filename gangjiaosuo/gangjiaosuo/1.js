// @charset "utf-8";
/********************************************************************
ths analytics(TA script)
author: away@myhexin.com
history:
2011-05-27	创建
2011-06-15
	增加了自动判断是否是client的功能。对于客户端和网站，可以不使用ld
	增加了_top选项，如果是false,则取当前页面url以及referrer，否则取父frame的url和referrer.默认为true
2011-08-22
    增加了cs字段，表示clientSize，也就是客户view的大小。
usage:
    兼容原stat方法:
    TA.log(10347, 'client');
    TA.log({id: 10347, ld: 'client'});
    TA.log(10348); // 默认ld='browser'
    对于需要传递的参数可以任意增加，例如
    TA.log({cost: 1024, type: 'school', author: '10jqka'});
    那么以上所有参数都会被带到url中进行传递。

    另外ta对象提供了对点击事件的记录，以下代码在id为btn1的对象点击时，会向日志服务器发送一个点击记录,该记录带有鼠标点击位置信息。
    TA.logElementClick(document.getElementById('btn1'), {eid: 'btn1'});

    对于在屏幕上的任意点击也可以记录。
    TA.logClick({eid: 'window', _sid: '__ta_wclick__', _top: false});

    对于document所有的锚点点击可以进行自动加载处理。日志中会带有该锚点的href信息
    TA.logArchorClick({type: 'archor'});
   
    两个内部属性：
    _base:	基本的点击路径的信息。默认是http://stat.10jqka.com.cn/q?。可以在传递参数中修改。
    _sid:    点击统计是通过在文档中插入图片实现的。这个图片id默认为__ths_stat__，如果存在同时激发多个记录，那么需要对id进行区分。这个时候需要重定义_sid

*********************************************************************/
// 日志记录对象
// 提供 add和log两个方法进行日志记录
var ths_stat = function() {
	this.id = 0;
	this.ld = 'browser';
	try {
		if (typeof external != 'undefined' && typeof external.createObject != 'undefined') {
			this.ld = 'client';
		}
	} catch (e) {}
	this._top = true;
	this.size = screen.width+"x"+screen.height;
	this._base = '//stat.10jqka.com.cn/q?';
	this._sid = '__ths_stat__';
};

// 具体访问进行日志记录
// @param url string 记录的日志
ths_stat.prototype._navigate = function(url) {
	var el = document.getElementById(this._sid);
	if (!el) {
		el = document.createElement('img');
		el.id = this._sid;
		el.height = 0;
		el.width = 0;
		el.setAttribute("style", "display:none");
		document.body.appendChild(el);
	}
	if (typeof this.callback == "function") {
		var me		= this,
		rcallback	= function() {
			me.callback(this);
		};
		if (el.addEventListener) {
			el.addEventListener('error', rcallback, false);
		} else {
			el.attachEvent('onerror', rcallback);
		}
	}
	el.src   = url;
};

// 增加提交的参数信息
// @param p1 Object|number  对于Object方式，将所有属性加入到this.否则认为是id
// @param p2 string ld
ths_stat.prototype.add = function(p1, p2) {
	if (p1 && p2) {
		this.id = p1;
		this.ld = p2;
	} else if (p1 instanceof Object){
		for(k in p1) {
			this[k] = p1[k];
		}
	} else if (p1) {
		this.id = p1;
	}
}

// 设置访问的location地址
ths_stat.prototype._setLocation = function() {
	if (this._top && top) {
		try{
			if (!this.ref) {
				this.ref = top.document.referrer;
			}
			if (!this.url) {
				this.url = top.location.href;
			}
		}catch(e) {}
	}
	if (!this.ref) {
		this.ref = (document.referrer) ? document.referrer : null;
	}
	if (!this.url) {
		this.url = window.location.href;
	}
	// 客户区大小在这个时候再进行设置。
	this.cs = document.body.clientWidth+"x"+document.body.clientHeight;
	this.ts = (new Date()).getTime();
}

// 返回访问的url
ths_stat.prototype._getUrl = function() {
	this._setLocation();
	var url = [];
	for(k in this) {
		if (k && k.charAt(0) != '_' && this[k] && typeof(this[k]) != 'function') {
			if (url.length) {
				url.push('&');
			}
			url = url.concat([encodeURIComponent(k), "=", encodeURIComponent(this[k])]);
		}
	}
	return this._base + url.join('');
}

// 对本对象进行日志记录
ths_stat.prototype.log = function() {
	this._navigate(this._getUrl());
};

// 取得event对象。为了取得点击的位置
ths_stat.prototype.getEvent = function(event) {
	event = event ? event : windows.event;
	if ( event.pageX == null && event.clientX !=  null ) {
		var doc = document.documentElement, body = document.body;
		event.pageX = event.clientX + (doc && doc.scrollLeft || body && body.scrollLeft || 0) - (doc && doc.clientLeft  || body && body.clientLeft || 0);
		event.pageY = event.clientY + (doc && doc.scrollTop  ||  body && body.scrollTop  || 0) - (doc && doc.clientTop  || body && body.clientTop  || 0);
	}
	return event;
}


// 记录点击点
ths_stat.prototype._onClick = function(event) {
	event = this.getEvent(event);
	var pos = event.pageX + ',' + event.pageY;
	this._navigate(this._getUrl() + '&mouse=' + pos);
};

// 绑定点击动作
ths_stat.prototype.bindClick = function(el, attrs) {
	var stat = this;
	var onclick = function(e) {
		for(index in attrs) {
			attr = attrs[index];
			stat[attr] = el.getAttribute(attr);
		}
		stat._onClick(e);
	};
	if (el.addEventListener) {
		el.addEventListener('click', onclick, false);
	} else {
		el.attachEvent('onclick', onclick);
	}
};

// 全局namespace
var TA = {

	// 进行日志记录
	log: function() {
		var stat = new ths_stat();
		stat.add.apply(stat, arguments);
		stat.log();
	},
	// 记录点击
	logClick: function() {
		var stat = new ths_stat();
		stat.add.apply(stat, arguments);
		stat.bindClick.call(stat, window);
	},

	// 绑定页面上所有锚的点击事件
	logArchorClick: function() {
		var stat = new ths_stat();
		stat.add.apply(stat, arguments);
		var archors = document.getElementsByTagName('a');
		for(var i = 0; i < archors.length; ++i) {
			stat.bindClick.call(stat, archors[i], ['href']);
		}
	},

	// 绑定指定element的点击事件
	logElementClick: function(el, params) {
		var stat = new ths_stat();
		stat.add(params);
		stat.bindClick.call(stat, el);
	}
};
var Zepto=function(){function a(a){return null==a?String(a):U[V.call(a)]||"object"}function b(b){return"function"==a(b)}function c(a){return null!=a&&a==a.window}function d(a){return null!=a&&a.nodeType==a.DOCUMENT_NODE}function e(b){return"object"==a(b)}function f(a){return e(a)&&!c(a)&&Object.getPrototypeOf(a)==Object.prototype}function g(a){return"number"==typeof a.length}function h(a){return D.call(a,function(a){return null!=a})}function i(a){return a.length>0?x.fn.concat.apply([],a):a}function j(a){return a.replace(/::/g,"/").replace(/([A-Z]+)([A-Z][a-z])/g,"$1_$2").replace(/([a-z\d])([A-Z])/g,"$1_$2").replace(/_/g,"-").toLowerCase()}function k(a){return a in G?G[a]:G[a]=new RegExp("(^|\\s)"+a+"(\\s|$)")}function l(a,b){return"number"!=typeof b||H[j(a)]?b:b+"px"}function m(a){var b,c;return F[a]||(b=E.createElement(a),E.body.appendChild(b),c=getComputedStyle(b,"").getPropertyValue("display"),b.parentNode.removeChild(b),"none"==c&&(c="block"),F[a]=c),F[a]}function n(a){return"children"in a?C.call(a.children):x.map(a.childNodes,function(a){return 1==a.nodeType?a:void 0})}function o(a,b,c){for(w in b)c&&(f(b[w])||Z(b[w]))?(f(b[w])&&!f(a[w])&&(a[w]={}),Z(b[w])&&!Z(a[w])&&(a[w]=[]),o(a[w],b[w],c)):b[w]!==v&&(a[w]=b[w])}function p(a,b){return null==b?x(a):x(a).filter(b)}function q(a,c,d,e){return b(c)?c.call(a,d,e):c}function r(a,b,c){null==c?a.removeAttribute(b):a.setAttribute(b,c)}function s(a,b){var c=a.className,d=c&&c.baseVal!==v;return b===v?d?c.baseVal:c:void(d?c.baseVal=b:a.className=b)}function t(a){var b;try{return a?"true"==a||("false"==a?!1:"null"==a?null:/^0/.test(a)||isNaN(b=Number(a))?/^[\[\{]/.test(a)?x.parseJSON(a):a:b):a}catch(c){return a}}function u(a,b){b(a);for(var c=0,d=a.childNodes.length;d>c;c++)u(a.childNodes[c],b)}var v,w,x,y,z,A,B=[],C=B.slice,D=B.filter,E=window.document,F={},G={},H={"column-count":1,columns:1,"font-weight":1,"line-height":1,opacity:1,"z-index":1,zoom:1},I=/^\s*<(\w+|!)[^>]*>/,J=/^<(\w+)\s*\/?>(?:<\/\1>|)$/,K=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,L=/^(?:body|html)$/i,M=/([A-Z])/g,N=["val","css","html","text","data","width","height","offset"],O=["after","prepend","before","append"],P=E.createElement("table"),Q=E.createElement("tr"),R={tr:E.createElement("tbody"),tbody:P,thead:P,tfoot:P,td:Q,th:Q,"*":E.createElement("div")},S=/complete|loaded|interactive/,T=/^[\w-]*$/,U={},V=U.toString,W={},X=E.createElement("div"),Y={tabindex:"tabIndex",readonly:"readOnly","for":"htmlFor","class":"className",maxlength:"maxLength",cellspacing:"cellSpacing",cellpadding:"cellPadding",rowspan:"rowSpan",colspan:"colSpan",usemap:"useMap",frameborder:"frameBorder",contenteditable:"contentEditable"},Z=Array.isArray||function(a){return a instanceof Array};return W.matches=function(a,b){if(!b||!a||1!==a.nodeType)return!1;var c=a.webkitMatchesSelector||a.mozMatchesSelector||a.oMatchesSelector||a.matchesSelector;if(c)return c.call(a,b);var d,e=a.parentNode,f=!e;return f&&(e=X).appendChild(a),d=~W.qsa(e,b).indexOf(a),f&&X.removeChild(a),d},z=function(a){return a.replace(/-+(.)?/g,function(a,b){return b?b.toUpperCase():""})},A=function(a){return D.call(a,function(b,c){return a.indexOf(b)==c})},W.fragment=function(a,b,c){var d,e,g;return J.test(a)&&(d=x(E.createElement(RegExp.$1))),d||(a.replace&&(a=a.replace(K,"<$1></$2>")),b===v&&(b=I.test(a)&&RegExp.$1),b in R||(b="*"),g=R[b],g.innerHTML=""+a,d=x.each(C.call(g.childNodes),function(){g.removeChild(this)})),f(c)&&(e=x(d),x.each(c,function(a,b){N.indexOf(a)>-1?e[a](b):e.attr(a,b)})),d},W.Z=function(a,b){return a=a||[],a.__proto__=x.fn,a.selector=b||"",a},W.isZ=function(a){return a instanceof W.Z},W.init=function(a,c){var d;if(!a)return W.Z();if("string"==typeof a)if(a=a.trim(),"<"==a[0]&&I.test(a))d=W.fragment(a,RegExp.$1,c),a=null;else{if(c!==v)return x(c).find(a);d=W.qsa(E,a)}else{if(b(a))return x(E).ready(a);if(W.isZ(a))return a;if(Z(a))d=h(a);else if(e(a))d=[a],a=null;else if(I.test(a))d=W.fragment(a.trim(),RegExp.$1,c),a=null;else{if(c!==v)return x(c).find(a);d=W.qsa(E,a)}}return W.Z(d,a)},x=function(a,b){return W.init(a,b)},x.extend=function(a){var b,c=C.call(arguments,1);return"boolean"==typeof a&&(b=a,a=c.shift()),c.forEach(function(c){o(a,c,b)}),a},W.qsa=function(a,b){var c,e="#"==b[0],f=!e&&"."==b[0],g=e||f?b.slice(1):b,h=T.test(g);return d(a)&&h&&e?(c=a.getElementById(g))?[c]:[]:1!==a.nodeType&&9!==a.nodeType?[]:C.call(h&&!e?f?a.getElementsByClassName(g):a.getElementsByTagName(b):a.querySelectorAll(b))},x.contains=E.documentElement.contains?function(a,b){return a!==b&&a.contains(b)}:function(a,b){for(;b&&(b=b.parentNode);)if(b===a)return!0;return!1},x.type=a,x.isFunction=b,x.isWindow=c,x.isArray=Z,x.isPlainObject=f,x.isEmptyObject=function(a){var b;for(b in a)return!1;return!0},x.inArray=function(a,b,c){return B.indexOf.call(b,a,c)},x.camelCase=z,x.trim=function(a){return null==a?"":String.prototype.trim.call(a)},x.uuid=0,x.support={},x.expr={},x.map=function(a,b){var c,d,e,f=[];if(g(a))for(d=0;d<a.length;d++)c=b(a[d],d),null!=c&&f.push(c);else for(e in a)c=b(a[e],e),null!=c&&f.push(c);return i(f)},x.each=function(a,b){var c,d;if(g(a)){for(c=0;c<a.length;c++)if(b.call(a[c],c,a[c])===!1)return a}else for(d in a)if(b.call(a[d],d,a[d])===!1)return a;return a},x.grep=function(a,b){return D.call(a,b)},window.JSON&&(x.parseJSON=JSON.parse),x.each("Boolean Number String Function Array Date RegExp Object Error".split(" "),function(a,b){U["[object "+b+"]"]=b.toLowerCase()}),x.fn={forEach:B.forEach,reduce:B.reduce,push:B.push,sort:B.sort,indexOf:B.indexOf,concat:B.concat,map:function(a){return x(x.map(this,function(b,c){return a.call(b,c,b)}))},slice:function(){return x(C.apply(this,arguments))},ready:function(a){return S.test(E.readyState)&&E.body?a(x):E.addEventListener("DOMContentLoaded",function(){a(x)},!1),this},get:function(a){return a===v?C.call(this):this[a>=0?a:a+this.length]},toArray:function(){return this.get()},size:function(){return this.length},remove:function(){return this.each(function(){null!=this.parentNode&&this.parentNode.removeChild(this)})},each:function(a){return B.every.call(this,function(b,c){return a.call(b,c,b)!==!1}),this},filter:function(a){return b(a)?this.not(this.not(a)):x(D.call(this,function(b){return W.matches(b,a)}))},add:function(a,b){return x(A(this.concat(x(a,b))))},is:function(a){return this.length>0&&W.matches(this[0],a)},not:function(a){var c=[];if(b(a)&&a.call!==v)this.each(function(b){a.call(this,b)||c.push(this)});else{var d="string"==typeof a?this.filter(a):g(a)&&b(a.item)?C.call(a):x(a);this.forEach(function(a){d.indexOf(a)<0&&c.push(a)})}return x(c)},has:function(a){return this.filter(function(){return e(a)?x.contains(this,a):x(this).find(a).size()})},eq:function(a){return-1===a?this.slice(a):this.slice(a,+a+1)},first:function(){var a=this[0];return a&&!e(a)?a:x(a)},last:function(){var a=this[this.length-1];return a&&!e(a)?a:x(a)},find:function(a){var b,c=this;return b=a?"object"==typeof a?x(a).filter(function(){var a=this;return B.some.call(c,function(b){return x.contains(b,a)})}):1==this.length?x(W.qsa(this[0],a)):this.map(function(){return W.qsa(this,a)}):[]},closest:function(a,b){var c=this[0],e=!1;for("object"==typeof a&&(e=x(a));c&&!(e?e.indexOf(c)>=0:W.matches(c,a));)c=c!==b&&!d(c)&&c.parentNode;return x(c)},parents:function(a){for(var b=[],c=this;c.length>0;)c=x.map(c,function(a){return(a=a.parentNode)&&!d(a)&&b.indexOf(a)<0?(b.push(a),a):void 0});return p(b,a)},parent:function(a){return p(A(this.pluck("parentNode")),a)},children:function(a){return p(this.map(function(){return n(this)}),a)},contents:function(){return this.map(function(){return C.call(this.childNodes)})},siblings:function(a){return p(this.map(function(a,b){return D.call(n(b.parentNode),function(a){return a!==b})}),a)},empty:function(){return this.each(function(){this.innerHTML=""})},pluck:function(a){return x.map(this,function(b){return b[a]})},show:function(){return this.each(function(){"none"==this.style.display&&(this.style.display=""),"none"==getComputedStyle(this,"").getPropertyValue("display")&&(this.style.display=m(this.nodeName))})},replaceWith:function(a){return this.before(a).remove()},wrap:function(a){var c=b(a);if(this[0]&&!c)var d=x(a).get(0),e=d.parentNode||this.length>1;return this.each(function(b){x(this).wrapAll(c?a.call(this,b):e?d.cloneNode(!0):d)})},wrapAll:function(a){if(this[0]){x(this[0]).before(a=x(a));for(var b;(b=a.children()).length;)a=b.first();x(a).append(this)}return this},wrapInner:function(a){var c=b(a);return this.each(function(b){var d=x(this),e=d.contents(),f=c?a.call(this,b):a;e.length?e.wrapAll(f):d.append(f)})},unwrap:function(){return this.parent().each(function(){x(this).replaceWith(x(this).children())}),this},clone:function(){return this.map(function(){return this.cloneNode(!0)})},hide:function(){return this.css("display","none")},toggle:function(a){return this.each(function(){var b=x(this);(a===v?"none"==b.css("display"):a)?b.show():b.hide()})},prev:function(a){return x(this.pluck("previousElementSibling")).filter(a||"*")},next:function(a){return x(this.pluck("nextElementSibling")).filter(a||"*")},html:function(a){return 0 in arguments?this.each(function(b){var c=this.innerHTML;x(this).empty().append(q(this,a,b,c))}):0 in this?this[0].innerHTML:null},text:function(a){return 0 in arguments?this.each(function(b){var c=q(this,a,b,this.textContent);this.textContent=null==c?"":""+c}):0 in this?this[0].textContent:null},attr:function(a,b){var c;return"string"!=typeof a||1 in arguments?this.each(function(c){if(1===this.nodeType)if(e(a))for(w in a)r(this,w,a[w]);else r(this,a,q(this,b,c,this.getAttribute(a)))}):this.length&&1===this[0].nodeType?!(c=this[0].getAttribute(a))&&a in this[0]?this[0][a]:c:v},removeAttr:function(a){return this.each(function(){1===this.nodeType&&r(this,a)})},prop:function(a,b){return a=Y[a]||a,1 in arguments?this.each(function(c){this[a]=q(this,b,c,this[a])}):this[0]&&this[0][a]},data:function(a,b){var c="data-"+a.replace(M,"-$1").toLowerCase(),d=1 in arguments?this.attr(c,b):this.attr(c);return null!==d?t(d):v},val:function(a){return 0 in arguments?this.each(function(b){this.value=q(this,a,b,this.value)}):this[0]&&(this[0].multiple?x(this[0]).find("option").filter(function(){return this.selected}).pluck("value"):this[0].value)},offset:function(a){if(a)return this.each(function(b){var c=x(this),d=q(this,a,b,c.offset()),e=c.offsetParent().offset(),f={top:d.top-e.top,left:d.left-e.left};"static"==c.css("position")&&(f.position="relative"),c.css(f)});if(!this.length)return null;var b=this[0].getBoundingClientRect();return{left:b.left+window.pageXOffset,top:b.top+window.pageYOffset,width:Math.round(b.width),height:Math.round(b.height)}},css:function(b,c){if(arguments.length<2){var d=this[0],e=getComputedStyle(d,"");if(!d)return;if("string"==typeof b)return d.style[z(b)]||e.getPropertyValue(b);if(Z(b)){var f={};return x.each(Z(b)?b:[b],function(a,b){f[b]=d.style[z(b)]||e.getPropertyValue(b)}),f}}var g="";if("string"==a(b))c||0===c?g=j(b)+":"+l(b,c):this.each(function(){this.style.removeProperty(j(b))});else for(w in b)b[w]||0===b[w]?g+=j(w)+":"+l(w,b[w])+";":this.each(function(){this.style.removeProperty(j(w))});return this.each(function(){this.style.cssText+=";"+g})},index:function(a){return a?this.indexOf(x(a)[0]):this.parent().children().indexOf(this[0])},hasClass:function(a){return a?B.some.call(this,function(a){return this.test(s(a))},k(a)):!1},addClass:function(a){return a?this.each(function(b){y=[];var c=s(this),d=q(this,a,b,c);d.split(/\s+/g).forEach(function(a){x(this).hasClass(a)||y.push(a)},this),y.length&&s(this,c+(c?" ":"")+y.join(" "))}):this},removeClass:function(a){return this.each(function(b){return a===v?s(this,""):(y=s(this),q(this,a,b,y).split(/\s+/g).forEach(function(a){y=y.replace(k(a)," ")}),void s(this,y.trim()))})},toggleClass:function(a,b){return a?this.each(function(c){var d=x(this),e=q(this,a,c,s(this));e.split(/\s+/g).forEach(function(a){(b===v?!d.hasClass(a):b)?d.addClass(a):d.removeClass(a)})}):this},scrollTop:function(a){if(this.length){var b="scrollTop"in this[0];return a===v?b?this[0].scrollTop:this[0].pageYOffset:this.each(b?function(){this.scrollTop=a}:function(){this.scrollTo(this.scrollX,a)})}},scrollLeft:function(a){if(this.length){var b="scrollLeft"in this[0];return a===v?b?this[0].scrollLeft:this[0].pageXOffset:this.each(b?function(){this.scrollLeft=a}:function(){this.scrollTo(a,this.scrollY)})}},position:function(){if(this.length){var a=this[0],b=this.offsetParent(),c=this.offset(),d=L.test(b[0].nodeName)?{top:0,left:0}:b.offset();return c.top-=parseFloat(x(a).css("margin-top"))||0,c.left-=parseFloat(x(a).css("margin-left"))||0,d.top+=parseFloat(x(b[0]).css("border-top-width"))||0,d.left+=parseFloat(x(b[0]).css("border-left-width"))||0,{top:c.top-d.top,left:c.left-d.left}}},offsetParent:function(){return this.map(function(){for(var a=this.offsetParent||E.body;a&&!L.test(a.nodeName)&&"static"==x(a).css("position");)a=a.offsetParent;return a})}},x.fn.detach=x.fn.remove,["width","height"].forEach(function(a){var b=a.replace(/./,function(a){return a[0].toUpperCase()});x.fn[a]=function(e){var f,g=this[0];return e===v?c(g)?g["inner"+b]:d(g)?g.documentElement["scroll"+b]:(f=this.offset())&&f[a]:this.each(function(b){g=x(this),g.css(a,q(this,e,b,g[a]()))})}}),O.forEach(function(b,c){var d=c%2;x.fn[b]=function(){var b,e,f=x.map(arguments,function(c){return b=a(c),"object"==b||"array"==b||null==c?c:W.fragment(c)}),g=this.length>1;return f.length<1?this:this.each(function(a,b){e=d?b:b.parentNode,b=0==c?b.nextSibling:1==c?b.firstChild:2==c?b:null;var h=x.contains(E.documentElement,e);f.forEach(function(a){if(g)a=a.cloneNode(!0);else if(!e)return x(a).remove();e.insertBefore(a,b),h&&u(a,function(a){null==a.nodeName||"SCRIPT"!==a.nodeName.toUpperCase()||a.type&&"text/javascript"!==a.type||a.src||window.eval.call(window,a.innerHTML)})})})},x.fn[d?b+"To":"insert"+(c?"Before":"After")]=function(a){return x(a)[b](this),this}}),W.Z.prototype=x.fn,W.uniq=A,W.deserializeValue=t,x.zepto=W,x}();window.Zepto=Zepto,void 0===window.$&&(window.$=Zepto),function(a){function b(a){var b=this.os={},c=this.browser={},d=a.match(/Web[kK]it[\/]{0,1}([\d.]+)/),e=a.match(/(Android);?[\s\/]+([\d.]+)?/),f=!!a.match(/\(Macintosh\; Intel /),g=a.match(/(iPad).*OS\s([\d_]+)/),h=a.match(/(iPod)(.*OS\s([\d_]+))?/),i=!g&&a.match(/(iPhone\sOS)\s([\d_]+)/),j=a.match(/(webOS|hpwOS)[\s\/]([\d.]+)/),k=a.match(/Windows Phone ([\d.]+)/),l=j&&a.match(/TouchPad/),m=a.match(/Kindle\/([\d.]+)/),n=a.match(/Silk\/([\d._]+)/),o=a.match(/(BlackBerry).*Version\/([\d.]+)/),p=a.match(/(BB10).*Version\/([\d.]+)/),q=a.match(/(RIM\sTablet\sOS)\s([\d.]+)/),r=a.match(/PlayBook/),s=a.match(/Chrome\/([\d.]+)/)||a.match(/CriOS\/([\d.]+)/),t=a.match(/Firefox\/([\d.]+)/),u=a.match(/MSIE\s([\d.]+)/)||a.match(/Trident\/[\d](?=[^\?]+).*rv:([0-9.].)/),v=!s&&a.match(/(iPhone|iPod|iPad).*AppleWebKit(?!.*Safari)/),w=v||a.match(/Version\/([\d.]+)([^S](Safari)|[^M]*(Mobile)[^S]*(Safari))/);(c.webkit=!!d)&&(c.version=d[1]),e&&(b.android=!0,b.version=e[2]),i&&!h&&(b.ios=b.iphone=!0,b.version=i[2].replace(/_/g,".")),g&&(b.ios=b.ipad=!0,b.version=g[2].replace(/_/g,".")),h&&(b.ios=b.ipod=!0,b.version=h[3]?h[3].replace(/_/g,"."):null),k&&(b.wp=!0,b.version=k[1]),j&&(b.webos=!0,b.version=j[2]),l&&(b.touchpad=!0),o&&(b.blackberry=!0,b.version=o[2]),p&&(b.bb10=!0,b.version=p[2]),q&&(b.rimtabletos=!0,b.version=q[2]),r&&(c.playbook=!0),m&&(b.kindle=!0,b.version=m[1]),n&&(c.silk=!0,c.version=n[1]),!n&&b.android&&a.match(/Kindle Fire/)&&(c.silk=!0),s&&(c.chrome=!0,c.version=s[1]),t&&(c.firefox=!0,c.version=t[1]),u&&(c.ie=!0,c.version=u[1]),w&&(f||b.ios)&&(c.safari=!0,f&&(c.version=w[1])),v&&(c.webview=!0),b.tablet=!!(g||r||e&&!a.match(/Mobile/)||t&&a.match(/Tablet/)||u&&!a.match(/Phone/)&&a.match(/Touch/)),b.phone=!(b.tablet||b.ipod||!(e||i||j||o||p||s&&a.match(/Android/)||s&&a.match(/CriOS\/([\d.]+)/)||t&&a.match(/Mobile/)||u&&a.match(/Touch/)))}b.call(a,navigator.userAgent),a.__detect=b}(Zepto),function(a){function b(a){return a._zid||(a._zid=m++)}function c(a,c,f,g){if(c=d(c),c.ns)var h=e(c.ns);return(q[b(a)]||[]).filter(function(a){return!(!a||c.e&&a.e!=c.e||c.ns&&!h.test(a.ns)||f&&b(a.fn)!==b(f)||g&&a.sel!=g)})}function d(a){var b=(""+a).split(".");return{e:b[0],ns:b.slice(1).sort().join(" ")}}function e(a){return new RegExp("(?:^| )"+a.replace(" "," .* ?")+"(?: |$)")}function f(a,b){return a.del&&!s&&a.e in t||!!b}function g(a){return u[a]||s&&t[a]||a}function h(c,e,h,i,k,m,n){var o=b(c),p=q[o]||(q[o]=[]);e.split(/\s/).forEach(function(b){if("ready"==b)return a(document).ready(h);var e=d(b);e.fn=h,e.sel=k,e.e in u&&(h=function(b){var c=b.relatedTarget;return!c||c!==this&&!a.contains(this,c)?e.fn.apply(this,arguments):void 0}),e.del=m;var o=m||h;e.proxy=function(a){if(a=j(a),!a.isImmediatePropagationStopped()){a.data=i;var b=o.apply(c,a._args==l?[a]:[a].concat(a._args));return b===!1&&(a.preventDefault(),a.stopPropagation()),b}},e.i=p.length,p.push(e),"addEventListener"in c&&c.addEventListener(g(e.e),e.proxy,f(e,n))})}function i(a,d,e,h,i){var j=b(a);(d||"").split(/\s/).forEach(function(b){c(a,b,e,h).forEach(function(b){delete q[j][b.i],"removeEventListener"in a&&a.removeEventListener(g(b.e),b.proxy,f(b,i))})})}function j(b,c){return(c||!b.isDefaultPrevented)&&(c||(c=b),a.each(y,function(a,d){var e=c[a];b[a]=function(){return this[d]=v,e&&e.apply(c,arguments)},b[d]=w}),(c.defaultPrevented!==l?c.defaultPrevented:"returnValue"in c?c.returnValue===!1:c.getPreventDefault&&c.getPreventDefault())&&(b.isDefaultPrevented=v)),b}function k(a){var b,c={originalEvent:a};for(b in a)x.test(b)||a[b]===l||(c[b]=a[b]);return j(c,a)}var l,m=1,n=Array.prototype.slice,o=a.isFunction,p=function(a){return"string"==typeof a},q={},r={},s="onfocusin"in window,t={focus:"focusin",blur:"focusout"},u={mouseenter:"mouseover",mouseleave:"mouseout"};r.click=r.mousedown=r.mouseup=r.mousemove="MouseEvents",a.event={add:h,remove:i},a.proxy=function(c,d){var e=2 in arguments&&n.call(arguments,2);if(o(c)){var f=function(){return c.apply(d,e?e.concat(n.call(arguments)):arguments)};return f._zid=b(c),f}if(p(d))return e?(e.unshift(c[d],c),a.proxy.apply(null,e)):a.proxy(c[d],c);throw new TypeError("expected function")},a.fn.bind=function(a,b,c){return this.on(a,b,c)},a.fn.unbind=function(a,b){return this.off(a,b)},a.fn.one=function(a,b,c,d){return this.on(a,b,c,d,1)};var v=function(){return!0},w=function(){return!1},x=/^([A-Z]|returnValue$|layer[XY]$)/,y={preventDefault:"isDefaultPrevented",stopImmediatePropagation:"isImmediatePropagationStopped",stopPropagation:"isPropagationStopped"};a.fn.delegate=function(a,b,c){return this.on(b,a,c)},a.fn.undelegate=function(a,b,c){return this.off(b,a,c)},a.fn.live=function(b,c){return a(document.body).delegate(this.selector,b,c),this},a.fn.die=function(b,c){return a(document.body).undelegate(this.selector,b,c),this},a.fn.on=function(b,c,d,e,f){var g,j,m=this;return b&&!p(b)?(a.each(b,function(a,b){m.on(a,c,d,b,f)}),m):(p(c)||o(e)||e===!1||(e=d,d=c,c=l),(o(d)||d===!1)&&(e=d,d=l),e===!1&&(e=w),m.each(function(l,m){f&&(g=function(a){return i(m,a.type,e),e.apply(this,arguments)}),c&&(j=function(b){var d,f=a(b.target).closest(c,m).get(0);return f&&f!==m?(d=a.extend(k(b),{currentTarget:f,liveFired:m}),(g||e).apply(f,[d].concat(n.call(arguments,1)))):void 0}),h(m,b,e,d,c,j||g)}))},a.fn.off=function(b,c,d){var e=this;return b&&!p(b)?(a.each(b,function(a,b){e.off(a,c,b)}),e):(p(c)||o(d)||d===!1||(d=c,c=l),d===!1&&(d=w),e.each(function(){i(this,b,d,c)}))},a.fn.trigger=function(b,c){return b=p(b)||a.isPlainObject(b)?a.Event(b):j(b),b._args=c,this.each(function(){"dispatchEvent"in this?this.dispatchEvent(b):a(this).triggerHandler(b,c)})},a.fn.triggerHandler=function(b,d){var e,f;return this.each(function(g,h){e=k(p(b)?a.Event(b):b),e._args=d,e.target=h,a.each(c(h,b.type||b),function(a,b){return f=b.proxy(e),e.isImmediatePropagationStopped()?!1:void 0})}),f},"focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select keydown keypress keyup error".split(" ").forEach(function(b){a.fn[b]=function(a){return a?this.bind(b,a):this.trigger(b)}}),["focus","blur"].forEach(function(b){a.fn[b]=function(a){return a?this.bind(b,a):this.each(function(){try{this[b]()}catch(a){}}),this}}),a.Event=function(a,b){p(a)||(b=a,a=b.type);var c=document.createEvent(r[a]||"Events"),d=!0;if(b)for(var e in b)"bubbles"==e?d=!!b[e]:c[e]=b[e];return c.initEvent(a,d,!0),j(c)}}(Zepto),function(a){function b(b,c,d){var e=a.Event(c);return a(b).trigger(e,d),!e.isDefaultPrevented()}function c(a,c,d,e){return a.global?b(c||s,d,e):void 0}function d(b){b.global&&0===a.active++&&c(b,null,"ajaxStart")}function e(b){b.global&&!--a.active&&c(b,null,"ajaxStop")}function f(a,b){var d=b.context;return b.beforeSend.call(d,a,b)===!1||c(b,d,"ajaxBeforeSend",[a,b])===!1?!1:void c(b,d,"ajaxSend",[a,b])}function g(a,b,d,e){var f=d.context,g="success";d.success.call(f,a,g,b),e&&e.resolveWith(f,[a,g,b]),c(d,f,"ajaxSuccess",[b,d,a]),i(g,b,d)}function h(a,b,d,e,f){var g=e.context;e.error.call(g,d,b,a),f&&f.rejectWith(g,[d,b,a]),c(e,g,"ajaxError",[d,e,a||b]),i(b,d,e)}function i(a,b,d){var f=d.context;d.complete.call(f,b,a),c(d,f,"ajaxComplete",[b,d]),e(d)}function j(){}function k(a){return a&&(a=a.split(";",2)[0]),a&&(a==x?"html":a==w?"json":u.test(a)?"script":v.test(a)&&"xml")||"text"}function l(a,b){return""==b?a:(a+"&"+b).replace(/[&?]{1,2}/,"?")}function m(b){b.processData&&b.data&&"string"!=a.type(b.data)&&(b.data=a.param(b.data,b.traditional)),!b.data||b.type&&"GET"!=b.type.toUpperCase()||(b.url=l(b.url,b.data),b.data=void 0)}function n(b,c,d,e){return a.isFunction(c)&&(e=d,d=c,c=void 0),a.isFunction(d)||(e=d,d=void 0),{url:b,data:c,success:d,dataType:e}}function o(b,c,d,e){var f,g=a.isArray(c),h=a.isPlainObject(c);a.each(c,function(c,i){f=a.type(i),e&&(c=d?e:e+"["+(h||"object"==f||"array"==f?c:"")+"]"),!e&&g?b.add(i.name,i.value):"array"==f||!d&&"object"==f?o(b,i,d,c):b.add(c,i)})}var p,q,r=0,s=window.document,t=/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,u=/^(?:text|application)\/javascript/i,v=/^(?:text|application)\/xml/i,w="application/json",x="text/html",y=/^\s*$/;a.active=0,a.ajaxJSONP=function(b,c){if(!("type"in b))return a.ajax(b);var d,e,i=b.jsonpCallback,j=(a.isFunction(i)?i():i)||"jsonp"+ ++r,k=s.createElement("script"),l=window[j],m=function(b){a(k).triggerHandler("error",b||"abort")},n={abort:m};return c&&c.promise(n),a(k).on("load error",function(f,i){clearTimeout(e),a(k).off().remove(),"error"!=f.type&&d?g(d[0],n,b,c):h(null,i||"error",n,b,c),window[j]=l,d&&a.isFunction(l)&&l(d[0]),l=d=void 0}),f(n,b)===!1?(m("abort"),n):(window[j]=function(){d=arguments},k.src=b.url.replace(/\?(.+)=\?/,"?$1="+j),s.head.appendChild(k),b.timeout>0&&(e=setTimeout(function(){m("timeout")},b.timeout)),n)},a.ajaxSettings={type:"GET",beforeSend:j,success:j,error:j,complete:j,context:null,global:!0,xhr:function(){return new window.XMLHttpRequest},accepts:{script:"text/javascript, application/javascript, application/x-javascript",json:w,xml:"application/xml, text/xml",html:x,text:"text/plain"},crossDomain:!1,timeout:0,processData:!0,cache:!0},a.ajax=function(b){var c=a.extend({},b||{}),e=a.Deferred&&a.Deferred();for(p in a.ajaxSettings)void 0===c[p]&&(c[p]=a.ajaxSettings[p]);d(c),c.crossDomain||(c.crossDomain=/^([\w-]+:)?\/\/([^\/]+)/.test(c.url)&&RegExp.$2!=window.location.host),c.url||(c.url=window.location.toString()),m(c);var i=c.dataType,n=/\?.+=\?/.test(c.url);if(n&&(i="jsonp"),c.cache!==!1&&(b&&b.cache===!0||"script"!=i&&"jsonp"!=i)||(c.url=l(c.url,"_="+Date.now())),"jsonp"==i)return n||(c.url=l(c.url,c.jsonp?c.jsonp+"=?":c.jsonp===!1?"":"callback=?")),a.ajaxJSONP(c,e);var o,r=c.accepts[i],s={},t=function(a,b){s[a.toLowerCase()]=[a,b]},u=/^([\w-]+:)\/\//.test(c.url)?RegExp.$1:window.location.protocol,v=c.xhr(),w=v.setRequestHeader;if(e&&e.promise(v),c.crossDomain||t("X-Requested-With","XMLHttpRequest"),t("Accept",r||"*/*"),(r=c.mimeType||r)&&(r.indexOf(",")>-1&&(r=r.split(",",2)[0]),v.overrideMimeType&&v.overrideMimeType(r)),(c.contentType||c.contentType!==!1&&c.data&&"GET"!=c.type.toUpperCase())&&t("Content-Type",c.contentType||"application/x-www-form-urlencoded"),c.headers)for(q in c.headers)t(q,c.headers[q]);if(v.setRequestHeader=t,v.onreadystatechange=function(){if(4==v.readyState){v.onreadystatechange=j,clearTimeout(o);var b,d=!1;if(v.status>=200&&v.status<300||304==v.status||0==v.status&&"file:"==u){i=i||k(c.mimeType||v.getResponseHeader("content-type")),b=v.responseText;try{"script"==i?(1,eval)(b):"xml"==i?b=v.responseXML:"json"==i&&(b=y.test(b)?null:a.parseJSON(b))}catch(f){d=f}d?h(d,"parsererror",v,c,e):g(b,v,c,e)}else h(v.statusText||null,v.status?"error":"abort",v,c,e)}},f(v,c)===!1)return v.abort(),h(null,"abort",v,c,e),v;if(c.xhrFields)for(q in c.xhrFields)v[q]=c.xhrFields[q];var x="async"in c?c.async:!0;v.open(c.type,c.url,x,c.username,c.password);for(q in s)w.apply(v,s[q]);return c.timeout>0&&(o=setTimeout(function(){v.onreadystatechange=j,v.abort(),h(null,"timeout",v,c,e)},c.timeout)),v.send(c.data?c.data:null),v},a.get=function(){return a.ajax(n.apply(null,arguments))},a.post=function(){var b=n.apply(null,arguments);return b.type="POST",a.ajax(b)},a.getJSON=function(){var b=n.apply(null,arguments);return b.dataType="json",a.ajax(b)},a.fn.load=function(b,c,d){if(!this.length)return this;var e,f=this,g=b.split(/\s/),h=n(b,c,d),i=h.success;return g.length>1&&(h.url=g[0],e=g[1]),h.success=function(b){f.html(e?a("<div>").html(b.replace(t,"")).find(e):b),i&&i.apply(f,arguments)},a.ajax(h),this};var z=encodeURIComponent;a.param=function(a,b){var c=[];return c.add=function(a,b){this.push(z(a)+"="+z(b))},o(c,a,b),c.join("&").replace(/%20/g,"+")}}(Zepto),function(a){a.fn.serializeArray=function(){var b,c=[];return a([].slice.call(this.get(0).elements)).each(function(){b=a(this);var d=b.attr("type");"fieldset"!=this.nodeName.toLowerCase()&&!this.disabled&&"submit"!=d&&"reset"!=d&&"button"!=d&&("radio"!=d&&"checkbox"!=d||this.checked)&&c.push({name:b.attr("name"),value:b.val()})}),c},a.fn.serialize=function(){var a=[];return this.serializeArray().forEach(function(b){a.push(encodeURIComponent(b.name)+"="+encodeURIComponent(b.value))}),a.join("&")},a.fn.submit=function(b){if(b)this.bind("submit",b);else if(this.length){var c=a.Event("submit");this.eq(0).trigger(c),c.isDefaultPrevented()||this.get(0).submit()}return this}}(Zepto),function(a,b){function c(a){return a.replace(/([a-z])([A-Z])/,"$1-$2").toLowerCase()}function d(a){return e?e+a:a.toLowerCase()}var e,f,g,h,i,j,k,l,m,n,o="",p={Webkit:"webkit",Moz:"",O:"o"},q=window.document,r=q.createElement("div"),s=/^((translate|rotate|scale)(X|Y|Z|3d)?|matrix(3d)?|perspective|skew(X|Y)?)$/i,t={};a.each(p,function(a,c){return r.style[a+"TransitionProperty"]!==b?(o="-"+a.toLowerCase()+"-",e=c,!1):void 0}),f=o+"transform",t[g=o+"transition-property"]=t[h=o+"transition-duration"]=t[j=o+"transition-delay"]=t[i=o+"transition-timing-function"]=t[k=o+"animation-name"]=t[l=o+"animation-duration"]=t[n=o+"animation-delay"]=t[m=o+"animation-timing-function"]="",a.fx={off:e===b&&r.style.transitionProperty===b,speeds:{_default:400,fast:200,slow:600},cssPrefix:o,transitionEnd:d("TransitionEnd"),animationEnd:d("AnimationEnd")},a.fn.animate=function(c,d,e,f,g){return a.isFunction(d)&&(f=d,e=b,d=b),a.isFunction(e)&&(f=e,e=b),a.isPlainObject(d)&&(e=d.easing,f=d.complete,g=d.delay,d=d.duration),d&&(d=("number"==typeof d?d:a.fx.speeds[d]||a.fx.speeds._default)/1e3),g&&(g=parseFloat(g)/1e3),this.anim(c,d,e,f,g)},a.fn.anim=function(d,e,o,p,q){var r,u,v,w={},x="",y=this,z=a.fx.transitionEnd,A=!1;if(e===b&&(e=a.fx.speeds._default/1e3),q===b&&(q=0),a.fx.off&&(e=0),"string"==typeof d)w[k]=d,w[l]=e+"s",w[n]=q+"s",w[m]=o||"linear",z=a.fx.animationEnd;else{u=[];for(r in d)s.test(r)?x+=r+"("+d[r]+") ":(w[r]=d[r],u.push(c(r)));x&&(w[f]=x,u.push(f)),e>0&&"object"==typeof d&&(w[g]=u.join(", "),w[h]=e+"s",w[j]=q+"s",w[i]=o||"linear")}return v=function(b){if("undefined"!=typeof b){if(b.target!==b.currentTarget)return;a(b.target).unbind(z,v)}else a(this).unbind(z,v);A=!0,a(this).css(t),p&&p.call(this)},e>0&&(this.bind(z,v),setTimeout(function(){A||v.call(y)},1e3*e+25)),this.size()&&this.get(0).clientLeft,this.css(w),0>=e&&setTimeout(function(){y.each(function(){v.call(this)})},0),this},r=null}(Zepto),function(a){function b(b){return b=a(b),!(!b.width()&&!b.height())&&"none"!==b.css("display")}function c(a,b){a=a.replace(/=#\]/g,'="#"]');var c,d,e=h.exec(a);if(e&&e[2]in g&&(c=g[e[2]],d=e[3],a=e[1],d)){var f=Number(d);d=isNaN(f)?d.replace(/^["']|["']$/g,""):f}return b(a,c,d)}var d=a.zepto,e=d.qsa,f=d.matches,g=a.expr[":"]={visible:function(){return b(this)?this:void 0},hidden:function(){return b(this)?void 0:this},selected:function(){return this.selected?this:void 0},checked:function(){return this.checked?this:void 0},parent:function(){return this.parentNode},first:function(a){return 0===a?this:void 0},last:function(a,b){return a===b.length-1?this:void 0},eq:function(a,b,c){return a===c?this:void 0},contains:function(b,c,d){return a(this).text().indexOf(d)>-1?this:void 0},has:function(a,b,c){return d.qsa(this,c).length?this:void 0}},h=new RegExp("(.*):(\\w+)(?:\\(([^)]+)\\))?$\\s*"),i=/^\s*>/,j="Zepto"+ +new Date;d.qsa=function(b,f){return c(f,function(c,g,h){try{var k;!c&&g?c="*":i.test(c)&&(k=a(b).addClass(j),c="."+j+" "+c);var l=e(b,c)}catch(m){throw console.error("error performing selector: %o",f),m}finally{k&&k.removeClass(j)}return g?d.uniq(a.map(l,function(a,b){return g.call(a,b,l,h)})):l})},d.matches=function(a,b){return c(b,function(b,c,d){return!(b&&!f(a,b)||c&&c.call(a,null,d)!==a)})}}(Zepto),function(a){a.Callbacks=function(b){b=a.extend({},b);var c,d,e,f,g,h,i=[],j=!b.once&&[],k=function(a){for(c=b.memory&&a,d=!0,h=f||0,f=0,g=i.length,e=!0;i&&g>h;++h)if(i[h].apply(a[0],a[1])===!1&&b.stopOnFalse){c=!1;break}e=!1,i&&(j?j.length&&k(j.shift()):c?i.length=0:l.disable())},l={add:function(){if(i){var d=i.length,h=function(c){a.each(c,function(a,c){"function"==typeof c?b.unique&&l.has(c)||i.push(c):c&&c.length&&"string"!=typeof c&&h(c)})};h(arguments),e?g=i.length:c&&(f=d,k(c))}return this},remove:function(){return i&&a.each(arguments,function(b,c){for(var d;(d=a.inArray(c,i,d))>-1;)i.splice(d,1),e&&(g>=d&&--g,h>=d&&--h)}),this},has:function(b){return!(!i||!(b?a.inArray(b,i)>-1:i.length))},empty:function(){return g=i.length=0,this},disable:function(){return i=j=c=void 0,this},disabled:function(){return!i},lock:function(){return j=void 0,c||l.disable(),this},locked:function(){return!j},fireWith:function(a,b){return!i||d&&!j||(b=b||[],b=[a,b.slice?b.slice():b],e?j.push(b):k(b)),this},fire:function(){return l.fireWith(this,arguments)},fired:function(){return!!d}};return l}}(Zepto),function(a){function b(c){var d=[["resolve","done",a.Callbacks({once:1,memory:1}),"resolved"],["reject","fail",a.Callbacks({once:1,memory:1}),"rejected"],["notify","progress",a.Callbacks({memory:1})]],e="pending",f={state:function(){return e},always:function(){return g.done(arguments).fail(arguments),this},then:function(){var c=arguments;return b(function(b){a.each(d,function(d,e){var h=a.isFunction(c[d])&&c[d];g[e[1]](function(){var c=h&&h.apply(this,arguments);if(c&&a.isFunction(c.promise))c.promise().done(b.resolve).fail(b.reject).progress(b.notify);else{var d=this===f?b.promise():this,g=h?[c]:arguments;b[e[0]+"With"](d,g)}})}),c=null}).promise()},promise:function(b){return null!=b?a.extend(b,f):f}},g={};return a.each(d,function(a,b){var c=b[2],h=b[3];f[b[1]]=c.add,h&&c.add(function(){e=h},d[1^a][2].disable,d[2][2].lock),g[b[0]]=function(){return g[b[0]+"With"](this===g?f:this,arguments),this},g[b[0]+"With"]=c.fireWith}),f.promise(g),c&&c.call(g,g),g}var c=Array.prototype.slice;a.when=function(d){var e,f,g,h=c.call(arguments),i=h.length,j=0,k=1!==i||d&&a.isFunction(d.promise)?i:0,l=1===k?d:b(),m=function(a,b,d){return function(f){b[a]=this,d[a]=arguments.length>1?c.call(arguments):f,d===e?l.notifyWith(b,d):--k||l.resolveWith(b,d)
}};if(i>1)for(e=new Array(i),f=new Array(i),g=new Array(i);i>j;++j)h[j]&&a.isFunction(h[j].promise)?h[j].promise().done(m(j,g,h)).fail(l.reject).progress(m(j,f,e)):--k;return k||l.resolveWith(g,h),l.promise()},a.Deferred=b}(Zepto);