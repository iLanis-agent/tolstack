#!/usr/bin/env python3
# Tol Stack oracle - mirrors engine.js with Fractions and Decimal: the sizes and tolerances are added exactly, the root sum square uses a 60 digit Decimal square root, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 60

NOM = "each part size must be from 0.01 to 1000 mm with at most two decimal places"
TOL = "each tolerance must be from 0 to 50 mm with at most two decimal places"
POCK = "the pocket size must be from 0.01 to 3100 mm with at most two decimal places"
def dec(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}(\.[0-9]{1,2})?", t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def txt(x):
    if isinstance(x, Decimal): d = x
    else: d = Decimal(x.numerator) / Decimal(x.denominator)
    v = d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = format(v, "f")
    neg = s.startswith("-") and v != 0
    s = s.lstrip("-")
    ip, fp = s.split(".")
    fp = fp.rstrip("0")
    return ("-" if neg else "") + (f"{ip}.{fp}" if fp else ip)
def lst(a): return a[0] if len(a) == 1 else ", ".join(a[:-1]) + " and " + a[-1]
def inp(n1, t1, n2, t2, n3, t3):
    return [dec(x, NOM, "0.01", "1000") for x in (n1, n2, n3)], [dec(x, TOL, "0", "50") for x in (t1, t2, t3)]

def stack(*a):
    n, t = inp(*a); N = sum(n); T = sum(t)
    return f"Parts of {lst([txt(x) for x in n])} mm stack to a nominal {txt(N)} mm. With tolerances of {lst([txt(x) for x in t])} mm the worst case runs from {txt(N-T)} to {txt(N+T)} mm, plus or minus {txt(T)} mm."
def rss(*a):
    n, t = inp(*a); N = sum(n); T = sum(t)
    S = sum(x * x for x in t)
    R = (Decimal(S.numerator) / Decimal(S.denominator)).sqrt()
    return f"Taken as a root sum square, the same tolerances combine to plus or minus {txt(R)} mm, so the stack is {txt(N)} mm plus or minus {txt(R)} mm, against plus or minus {txt(T)} mm in the worst case."
def gap(n1, t1, n2, t2, n3, t3, k, kt):
    n, t = inp(n1, t1, n2, t2, n3, t3); N = sum(n); T = sum(t)
    K = dec(k, POCK, "0.01", "3100"); KT = dec(kt, TOL, "0", "50")
    lo = K - KT - (N + T); hi = K + KT - (N - T)
    return f"In a {txt(K)} mm pocket, plus or minus {txt(KT)} mm, the worst case gap runs from {txt(lo)} mm to {txt(hi)} mm. A negative figure means the parts overlap in that case."

FNS = {"stackTruth": stack, "rssTruth": rss, "gapTruth": gap}
def cases():
    c = []
    base = ["10", "0.1", "25.5", "0.2", "8", "0.3"]
    sets = [base, ["0.01", "0", "0.01", "0", "0.01", "0"], ["1000", "50", "1000", "50", "1000", "50"], ["12.34", "0.05", "7.89", "0.05", "3.21", "0.05"],
            ["5", "0.15", "5", "0.15", "5", "0.15"], ["20", "0.01", "30", "0.02", "40", "0.03"], ["1", "0", "2", "0.5", "3", "0"], ["99.99", "1.25", "0.5", "0.75", "100", "2"]]
    for s in sets:
        c += [("stackTruth", s), ("rssTruth", s)]
        for k, kt in [("44", "0.2"), ("43.5", "0"), ("40", "0.5"), ("3100", "50"), ("0.01", "0"), ("60", "0.1")]:
            c.append(("gapTruth", s + [k, kt]))
    for a in [" 10 ", "10.0", "10.00", "10.5", "010"]:
        c += [("stackTruth", [a, " 0.1 ", "25.5", "0.2", "8", "0.30"]), ("rssTruth", [a, " 0.1 ", "25.5", "0.2", "8", "0.30"])]
    bad = ["", "x", "0", "-1", ".5", "5.", "1e2", "0.001", "1.234", "10000", "99999"]
    for v in bad:
        c += [("stackTruth", [v, "0.1", "25.5", "0.2", "8", "0.3"]), ("stackTruth", ["10", v, "25.5", "0.2", "8", "0.3"]), ("rssTruth", ["10", "0.1", "25.5", "0.2", v, "0.3"]), ("rssTruth", ["10", "0.1", "25.5", "0.2", "8", v]),
              ("gapTruth", base + [v, "0.2"]), ("gapTruth", base + ["44", v])]
    for t in [["1000.01", "0.1", "25.5", "0.2", "8", "0.3"], ["10", "50.01", "25.5", "0.2", "8", "0.3"], ["0", "0", "25.5", "0.2", "8", "0.3"]]:
        c += [("stackTruth", t), ("rssTruth", t)]
    c += [("gapTruth", base + ["3100.01", "0.2"]), ("gapTruth", base + ["44", "50.01"]), ("gapTruth", base + ["0", "0.2"])]
    r = random.Random(714)
    for _ in range(8):
        s = []
        for _ in range(3): s += [f"{r.randint(0, 999)}.{r.randint(0, 99):02d}".replace("0.00", "0.01"), f"{r.randint(0, 5)}.{r.randint(0, 99):02d}"]
        k = f"{r.randint(1, 3000)}.{r.randint(0, 99):02d}"; kt = f"{r.randint(0, 3)}.{r.randint(0, 99):02d}"
        c += [("stackTruth", s), ("rssTruth", s), ("gapTruth", s + [k, kt])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
