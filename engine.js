// Tol Stack engine: a row of three parts and a pocket. Nominal total, worst case range, root sum square tolerance, and the worst case gap. Exact integers on hundredths of a mm, results rounded half up.
function _d(t, err, lo, hi) { // mm text with at most two decimals -> hundredths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]{1,2}))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 100 + (m[2] ? parseInt(m[2].padEnd(2, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _NOM = "each part size must be from 0.01 to 1000 mm with at most two decimal places";
var _TOL = "each tolerance must be from 0 to 50 mm with at most two decimal places";
var _POCK = "the pocket size must be from 0.01 to 3100 mm with at most two decimal places";
function _dec(v) { // signed hundredths -> text
  var neg = v < 0; if (neg) v = -v;
  var s = String(Math.floor(v / 100)), f = String(v % 100).padStart(2, "0").replace(/0+$/, "");
  return (neg && v !== 0 ? "-" : "") + (f ? s + "." + f : s);
}
function _list(a) { return a.length === 1 ? a[0] : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]; }
function _isqrt(n) { var r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }
function _rss(ts) { // half up square root of the sum of squares, on hundredths
  var s = 0; for (var i = 0; i < ts.length; i++) s += ts[i] * ts[i];
  var r = _isqrt(s);
  return s <= r * r + r ? r : r + 1;
}
function _in(n1, t1, n2, t2, n3, t3) {
  return { n: [_d(n1, _NOM, 1, 100000), _d(n2, _NOM, 1, 100000), _d(n3, _NOM, 1, 100000)], t: [_d(t1, _TOL, 0, 5000), _d(t2, _TOL, 0, 5000), _d(t3, _TOL, 0, 5000)] };
}
function _sum(a) { return a[0] + a[1] + a[2]; }

function stackTruth(n1, t1, n2, t2, n3, t3) {
  var p = _in(n1, t1, n2, t2, n3, t3), N = _sum(p.n), T = _sum(p.t);
  return "Parts of " + _list(p.n.map(_dec)) + " mm stack to a nominal " + _dec(N) + " mm. With tolerances of " + _list(p.t.map(_dec)) + " mm the worst case runs from " + _dec(N - T) + " to " + _dec(N + T) + " mm, plus or minus " + _dec(T) + " mm.";
}
function rssTruth(n1, t1, n2, t2, n3, t3) {
  var p = _in(n1, t1, n2, t2, n3, t3), N = _sum(p.n), T = _sum(p.t), R = _rss(p.t);
  return "Taken as a root sum square, the same tolerances combine to plus or minus " + _dec(R) + " mm, so the stack is " + _dec(N) + " mm plus or minus " + _dec(R) + " mm, against plus or minus " + _dec(T) + " mm in the worst case.";
}
function gapTruth(n1, t1, n2, t2, n3, t3, pocket, pocketTol) {
  var p = _in(n1, t1, n2, t2, n3, t3), N = _sum(p.n), T = _sum(p.t);
  var k = _d(pocket, _POCK, 1, 310000), kt = _d(pocketTol, _TOL, 0, 5000);
  return "In a " + _dec(k) + " mm pocket, plus or minus " + _dec(kt) + " mm, the worst case gap runs from " + _dec((k - kt) - (N + T)) + " mm to " + _dec((k + kt) - (N - T)) + " mm. A negative figure means the parts overlap in that case.";
}
