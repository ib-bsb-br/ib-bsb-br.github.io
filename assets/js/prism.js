var _self = "undefined" != typeof window ? window : "undefined" != typeof WorkerGlobalScope && self instanceof WorkerGlobalScope ? self : {},
	Prism = function(e) {
		function t(e, t, n, r) {
			this.type = e, this.content = t, this.alias = n, this.length = 0 | (r || "").length
		}

		function n(e, t, n, r) {
			e.lastIndex = t;
			var a = e.exec(n);
			if (a && r && a[1]) {
				var i = a[1].length;
				a.index += i, a[0] = a[0].slice(i)
			}
			return a
		}

		function r(e, a, l, s, u, c) {
			for (var d in l)
				if (l.hasOwnProperty(d) && l[d]) {
					var m = l[d];
					m = Array.isArray(m) ? m : [m];
					for (var g = 0; g < m.length; ++g) {
						if (c && c.cause == d + "," + g) return;
						var p = m[g],
							h = p.inside,
							v = !!p.lookbehind,
							y = !!p.greedy,
							b = p.alias;
						if (y && !p.pattern.global) {
							var k = p.pattern.toString().match(/[imsuy]*$/)[0];
							p.pattern = RegExp(p.pattern.source, k + "g")
						}
						for (var w = p.pattern || p, x = s.next, A = u; x !== a.tail && !(c && A >= c.reach); A += x.value.length, x = x.next) {
							var C = x.value;
							if (a.length > e.length) return;
							if (!(C instanceof t)) {
								var E, P = 1;
								if (y) {
									if (E = n(w, A, e, v), !E || E.index >= e.length) break;
									var L = E.index,
										S = E.index + E[0].length,
										N = A;
									for (N += x.value.length; L >= N;) x = x.next, N += x.value.length;
									if (N -= x.value.length, A = N, x.value instanceof t) continue;
									for (var T = x; T !== a.tail && (S > N || "string" == typeof T.value); T = T.next) P++, N += T.value.length;
									P--, C = e.slice(A, N), E.index -= A
								} else if (E = n(w, 0, C, v), !E) continue;
								var L = E.index,
									O = E[0],
									z = C.slice(0, L),
									H = C.slice(L + O.length),
									j = A + C.length;
								c && j > c.reach && (c.reach = j);
								var q = x.prev;
								z && (q = i(a, q, z), A += z.length), o(a, q, P);
								var B = new t(d, h ? f.tokenize(O, h) : O, b, O);
								if (x = i(a, q, B), H && i(a, x, H), P > 1) {
									var I = {
										cause: d + "," + g,
										reach: j
									};
									r(e, a, l, x.prev, A, I), c && I.reach > c.reach && (c.reach = I.reach)
								}
							}
						}
					}
				}
		}

		function a() {
			var e = {
					value: null,
					prev: null,
					next: null
				},
				t = {
					value: null,
					prev: e,
					next: null
				};
			e.next = t, this.head = e, this.tail = t, this.length = 0
		}

		function i(e, t, n) {
			var r = t.next,
				a = {
					value: n,
					prev: t,
					next: r
				};
			return t.next = a, r.prev = a, e.length++, a
		}

		function o(e, t, n) {
			for (var r = t.next, a = 0; n > a && r !== e.tail; a++) r = r.next;
			t.next = r, r.prev = t, e.length -= a
		}

		function l(e) {
			for (var t = [], n = e.head.next; n !== e.tail;) t.push(n.value), n = n.next;
			return t
		}

		function s() {
			f.manual || f.highlightAll()
		}
		var u = /(?:^|\s)lang(?:uage)?-([\w-]+)(?=\s|$)/i,
			c = 0,
			d = {},
			f = {
				manual: e.Prism && e.Prism.manual,
				disableWorkerMessageHandler: e.Prism && e.Prism.disableWorkerMessageHandler,
				util: {
					encode: function p(e) {
						return e instanceof t ? new t(e.type, p(e.content), e.alias) : Array.isArray(e) ? e.map(p) : e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\u00a0/g, " ")
					},
					type: function(e) {
						return Object.prototype.toString.call(e).slice(8, -1)
					},
					objId: function(e) {
						return e.__id || Object.defineProperty(e, "__id", {
							value: ++c
						}), e.__id
					},
					clone: function h(e, t) {
						t = t || {};
						var n, r;
						switch (f.util.type(e)) {
							case "Object":
								if (r = f.util.objId(e), t[r]) return t[r];
								n = {}, t[r] = n;
								for (var a in e) e.hasOwnProperty(a) && (n[a] = h(e[a], t));
								return n;
							case "Array":
								return r = f.util.objId(e), t[r] ? t[r] : (n = [], t[r] = n, e.forEach(function(e, r) {
									n[r] = h(e, t)
								}), n);
							default:
								return e
						}
					},
					getLanguage: function(e) {
						for (; e;) {
							var t = u.exec(e.className);
							if (t) return t[1].toLowerCase();
							e = e.parentElement
						}
						return "none"
					},
					setLanguage: function(e, t) {
						e.className = e.className.replace(RegExp(u, "gi"), ""), e.classList.add("language-" + t)
					},
					currentScript: function() {
						if ("undefined" == typeof document) return null;
						if ("currentScript" in document) return document.currentScript;
						try {
							throw new Error
						} catch (e) {
							var t = (/at [^(\r\n]*\((.*):[^:]+:[^:]+\)$/i.exec(e.stack) || [])[1];
							if (t) {
								var n = document.getElementsByTagName("script");
								for (var r in n)
									if (n[r].src == t) return n[r]
							}
							return null
						}
					},
					isActive: function(e, t, n) {
						for (var r = "no-" + t; e;) {
							var a = e.classList;
							if (a.contains(t)) return !0;
							if (a.contains(r)) return !1;
							e = e.parentElement
						}
						return !!n
					}
				},
				languages: {
					plain: d,
					plaintext: d,
					text: d,
					txt: d,
					extend: function(e, t) {
						var n = f.util.clone(f.languages[e]);
						for (var r in t) n[r] = t[r];
						return n
					},
					insertBefore: function(e, t, n, r) {
						r = r || f.languages;
						var a = r[e],
							i = {};
						for (var o in a)
							if (a.hasOwnProperty(o)) {
								if (o == t)
									for (var l in n) n.hasOwnProperty(l) && (i[l] = n[l]);
								n.hasOwnProperty(o) || (i[o] = a[o])
							} var s = r[e];
						return r[e] = i, f.languages.DFS(f.languages, function(t, n) {
							n === s && t != e && (this[t] = i)
						}), i
					},
					DFS: function v(e, t, n, r) {
						r = r || {};
						var a = f.util.objId;
						for (var i in e)
							if (e.hasOwnProperty(i)) {
								t.call(e, i, e[i], n || i);
								var o = e[i],
									l = f.util.type(o);
								"Object" !== l || r[a(o)] ? "Array" !== l || r[a(o)] || (r[a(o)] = !0, v(o, t, i, r)) : (r[a(o)] = !0, v(o, t, null, r))
							}
					}
				},
				plugins: {},
				highlightAll: function(e, t) {
					f.highlightAllUnder(document, e, t)
				},
				highlightAllUnder: function(e, t, n) {
					var r = {
						callback: n,
						container: e,
						selector: 'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'
					};
					f.hooks.run("before-highlightall", r), r.elements = Array.prototype.slice.apply(r.container.querySelectorAll(r.selector)), f.hooks.run("before-all-elements-highlight", r);
					for (var a, i = 0; a = r.elements[i++];) f.highlightElement(a, t === !0, r.callback)
				},
				highlightElement: function(t, n, r) {
					function a(e) {
						u.highlightedCode = e, f.hooks.run("before-insert", u), u.element.innerHTML = u.highlightedCode, f.hooks.run("after-highlight", u), f.hooks.run("complete", u), r && r.call(u.element)
					}
					var i = f.util.getLanguage(t),
						o = f.languages[i];
					f.util.setLanguage(t, i);
					var l = t.parentElement;
					l && "section" === l.nodeName.toLowerCase() && f.util.setLanguage(l, i);
					var s = t.textContent,
						u = {
							element: t,
							language: i,
							grammar: o,
							code: s
						};
					if (f.hooks.run("before-sanity-check", u), l = u.element.parentElement, l && "section" === l.nodeName.toLowerCase() && !l.hasAttribute("tabindex") && l.setAttribute("tabindex", "0"), !u.code) return f.hooks.run("complete", u), void(r && r.call(u.element));
					if (f.hooks.run("before-highlight", u), !u.grammar) return void a(f.util.encode(u.code));
					if (n && e.Worker) {
						var c = new Worker(f.filename);
						c.onmessage = function(e) {
							a(e.data)
						}, c.postMessage(JSON.stringify({
							language: u.language,
							code: u.code,
							immediateClose: !0
						}))
					} else a(f.highlight(u.code, u.grammar, u.language))
				},
				highlight: function(e, n, r) {
					var a = {
						code: e,
						grammar: n,
						language: r
					};
					if (f.hooks.run("before-tokenize", a), !a.grammar) throw new Error('The language "' + a.language + '" has no grammar.');
					return a.tokens = f.tokenize(a.code, a.grammar), f.hooks.run("after-tokenize", a), t.stringify(f.util.encode(a.tokens), a.language)
				},
				tokenize: function(e, t) {
					var n = t.rest;
					if (n) {
						for (var o in n) t[o] = n[o];
						delete t.rest
					}
					var s = new a;
					return i(s, s.head, e), r(e, s, t, s.head, 0), l(s)
				},
				hooks: {
					all: {},
					add: function(e, t) {
						var n = f.hooks.all;
						n[e] = n[e] || [], n[e].push(t)
					},
					run: function(e, t) {
						var n = f.hooks.all[e];
						if (n && n.length)
							for (var r, a = 0; r = n[a++];) r(t)
					}
				},
				Token: t
			};
		if (e.Prism = f, t.stringify = function y(e, t) {
				if ("string" == typeof e) return e;
				if (Array.isArray(e)) {
					var n = "";
					return e.forEach(function(e) {
						n += y(e, t)
					}), n
				}
				var r = {
						type: e.type,
						content: y(e.content, t),
						tag: "span",
						classes: ["token", e.type],
						attributes: {},
						language: t
					},
					a = e.alias;
				a && (Array.isArray(a) ? Array.prototype.push.apply(r.classes, a) : r.classes.push(a)), f.hooks.run("wrap", r);
				var i = "";
				for (var o in r.attributes) i += " " + o + '="' + (r.attributes[o] || "").replace(/"/g, "&quot;") + '"';
				return "<" + r.tag + ' class="' + r.classes.join(" ") + '"' + i + ">" + r.content + "</" + r.tag + ">"
			}, !e.document) return e.addEventListener ? (f.disableWorkerMessageHandler || e.addEventListener("message", function(t) {
			var n = JSON.parse(t.data),
				r = n.language,
				a = n.code,
				i = n.immediateClose;
			e.postMessage(f.highlight(a, f.languages[r], r)), i && e.close()
		}, !1), f) : f;
		var m = f.util.currentScript();
		if (m && (f.filename = m.src, m.hasAttribute("data-manual") && (f.manual = !0)), !f.manual) {
			var g = document.readyState;
			"loading" === g || "interactive" === g && m && m.defer ? document.addEventListener("DOMContentLoaded", s) : window.requestAnimationFrame ? window.requestAnimationFrame(s) : window.setTimeout(s, 16)
		}
		return f
	}(_self);
"undefined" != typeof module && module.exports && (module.exports = Prism), "undefined" != typeof global && (global.Prism = Prism),
	function() {
		if ("undefined" != typeof Prism) {
			var e = /\b([a-z]{3,7}:\/\/|tel:)[\w\-+%~/.:=&!$'()*,;@]+(?:\?[\w\-+%~/.:=?&!$'()*,;@]*)?(?:#[\w\-+%~/.:#=?&!$'()*,;@]*)?/,
				t = /\b\S+@[\w.]+[a-z]{2}/,
				n = /\[([^\]]+)\]\(([^)]+)\)/,
				r = ["comment", "url", "attr-value", "string"];
			Prism.plugins.autolinker = {
				processGrammar: function(a) {
					a && !a["url-link"] && (Prism.languages.DFS(a, function(a, i, o) {
						r.indexOf(o) > -1 && !Array.isArray(i) && (i.pattern || (i = this[a] = {
							pattern: i
						}), i.inside = i.inside || {}, "comment" == o && (i.inside["md-link"] = n), "attr-value" == o ? Prism.languages.insertBefore("inside", "punctuation", {
							"url-link": e
						}, i) : i.inside["url-link"] = e, i.inside["email-link"] = t)
					}), a["url-link"] = e, a["email-link"] = t)
				}
			}, Prism.hooks.add("before-highlight", function(e) {
				Prism.plugins.autolinker.processGrammar(e.grammar)
			}), Prism.hooks.add("wrap", function(e) {
				if (/-link$/.test(e.type)) {
					e.tag = "a";
					var t = e.content;
					if ("email-link" == e.type && 0 != t.indexOf("mailto:")) t = "mailto:" + t;
					else if ("md-link" == e.type) {
						var r = e.content.match(n);
						t = r[2], e.content = r[1]
					}
					e.attributes.href = t;
					try {
						e.content = decodeURIComponent(e.content)
					} catch (a) {}
				}
			})
		}
	}(),
	function() {
		function e(e) {
			for (; e;) {
				var t = e.getAttribute("data-toolbar-order");
				if (null != t) return t = t.trim(), t.length ? t.split(/\s*,\s*/g) : [];
				e = e.parentElement
			}
		}
		if ("undefined" != typeof Prism && "undefined" != typeof document) {
			var t = [],
				n = {},
				r = function() {};
			Prism.plugins.toolbar = {};
			var a = Prism.plugins.toolbar.registerButton = function(e, r) {
					var a;
					return a = "function" == typeof r ? r : function(e) {
						var t;
						return "function" == typeof r.onClick ? (t = document.createElement("button"), t.type = "button", t.addEventListener("click", function() {
							r.onClick.call(this, e)
						})) : "string" == typeof r.url ? (t = document.createElement("a"), t.href = r.url) : t = document.createElement("span"), r.className && t.classList.add(r.className), t.textContent = r.text, t
					}, e in n ? void console.warn('There is a button with the key "' + e + '" registered already.') : void t.push(n[e] = a)
				},
				i = Prism.plugins.toolbar.hook = function(a) {
					var i = a.element.parentNode;
					if (i && /section/i.test(i.nodeName) && !i.parentNode.classList.contains("code-toolbar")) {
						var o = document.createElement("div");
						o.classList.add("code-toolbar"), i.parentNode.insertBefore(o, i), o.appendChild(i);
						var l = document.createElement("div");
						l.classList.add("toolbar");
						var s = t,
							u = e(a.element);
						u && (s = u.map(function(e) {
							return n[e] || r
						})), s.forEach(function(e) {
							var t = e(a);
							if (t) {
								var n = document.createElement("div");
								n.classList.add("toolbar-item"), n.appendChild(t), l.appendChild(n)
							}
						}), o.appendChild(l)
					}
				};
			a("label", function(e) {
				var t = e.element.parentNode;
				if (t && /section/i.test(t.nodeName) && t.hasAttribute("data-label")) {
					var n, r, a = t.getAttribute("data-label");
					try {
						r = document.querySelector("template#" + a)
					} catch (i) {}
					return r ? n = r.content : (t.hasAttribute("data-url") ? (n = document.createElement("a"), n.href = t.getAttribute("data-url")) : n = document.createElement("span"), n.textContent = a), n
				}
			}), Prism.hooks.add("complete", i)
		}
	}(),
	function() {
		function e(e, t) {
			e.addEventListener("click", function() {
				n(t)
			})
		}

		function t(e) {
			var t = document.createElement("textarea");
			t.value = e.getText(), t.style.top = "0", t.style.left = "0", t.style.position = "fixed", document.body.appendChild(t), t.focus(), t.select();
			try {
				var n = document.execCommand("copy");
				setTimeout(function() {
					n ? e.success() : e.error()
				}, 1)
			} catch (r) {
				setTimeout(function() {
					e.error(r)
				}, 1)
			}
			document.body.removeChild(t)
		}

		function n(e) {
			navigator.clipboard ? navigator.clipboard.writeText(e.getText()).then(e.success, function() {
				t(e)
			}) : t(e)
		}

		function r(e) {
			window.getSelection().selectAllChildren(e)
		}

		function a(e) {
			var t = {
					copy: "Copy",
					"copy-error": "press Ctrl+C to copy",
					"copy-success": "Copied!",
					"copy-timeout": 5e3
				},
				n = "data-prismjs-";
			for (var r in t) {
				for (var a = n + r, i = e; i && !i.hasAttribute(a);) i = i.parentElement;
				i && (t[r] = i.getAttribute(a))
			}
			return t
		}
		if ("undefined" != typeof Prism && "undefined" != typeof document) return Prism.plugins.toolbar ? void Prism.plugins.toolbar.registerButton("copy-to-clipboard", function(t) {
			function n() {
				setTimeout(function() {
					i("copy")
				}, l["copy-timeout"])
			}

			function i(e) {
				u.textContent = l[e], s.setAttribute("data-copy-state", e)
			}
			var o = t.element,
				l = a(o),
				s = document.createElement("button");
			s.className = "copy-to-clipboard-button", s.setAttribute("type", "button");
			var u = document.createElement("span");
			return s.appendChild(u), i("copy"), e(s, {
				getText: function() {
					return o.textContent
				},
				success: function() {
					i("copy-success"), n()
				},
				error: function() {
					i("copy-error"), setTimeout(function() {
						r(o)
					}, 1), n()
				}
			}), s
		}) : void console.warn("Copy to Clipboard plugin loaded before Toolbar plugin.")
	}(),
	function() {
		"undefined" != typeof Prism && "undefined" != typeof document && document.querySelector && Prism.plugins.toolbar.registerButton("download-file", function(e) {
			var t = e.element.parentNode;
			if (t && /section/i.test(t.nodeName) && t.hasAttribute("data-code") && t.hasAttribute("data-filename") && t.hasAttribute("data-download-link")) {
				var n = t.getAttribute("data-filename"),
					r = t.getAttribute("data-code"),
					a = t.getAttribute("data-download-link-label") || "Download",
					i = document.createElement("a");
				return i.textContent = a, i.onclick = function(e) {
					e.preventDefault();
					var t = new Blob([r], {
							type: "text/plain"
						}),
						a = URL.createObjectURL(t),
						i = document.createElement("a");
					i.href = a, i.setAttribute("download", n), document.body.appendChild(i), i.click(), document.body.removeChild(i), URL.revokeObjectURL(a)
				}, i
			}
		})
	}();
