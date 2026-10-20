# Tol Stack

Tolerance stack-up arithmetic. Parts of 10, 25.5 and 8 mm stack to a nominal 43.5 mm. With tolerances of 0.1, 0.2 and 0.3 mm the worst case runs from 42.9 to 44.1 mm, plus or minus 0.6 mm.

## What it computes

- **The stack truth** - the nominal total of three parts in a row (0.01 to 1000 mm each) and the worst case range from adding every plus or minus tolerance (0 to 50 mm each).
- **The root sum square truth** - the same tolerances combined as the square root of the sum of their squares, beside the worst case.
- **The gap truth** - the worst case gap between the stack and a pocket (0.01 to 3100 mm, with its own tolerance). A negative figure means overlap in that case.

## Boundary

Arithmetic only. The sizes and tolerances are the owner's own entries, every tolerance is treated as plus or minus, and every part as lying in one line. It has not seen any part and does not know shape, tilt, wear, temperature or how parts are made, and it gives no verdict that a fit will work or that a tolerance is good enough. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a mm, half-up rounding, integer square root).
- `oracle.py` - the Python mirror (Fractions and a 60 digit Decimal square root) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/tolstack/
Repo: https://github.com/iLanis-agent/tolstack
