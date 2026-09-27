# synthetic-smells

**Proves:** `changelog_architecture` catches real fixes and stays quiet otherwise.

A tiny Python shop with two deliberately planted smells:

- **before/**: `Billing ↔ Notifications` dependency cycle + `utils/helpers.py` god module
  (20 unrelated helpers)
- **after/**: `InvoiceIssued` domain event breaks the cycle; god module split into
  `text`/`crypto`/`timex`; 16 dead helpers deleted

Expected result: 39 → 20 entities, **2 → 0 smells**, 2 resolved / 0 new, ~0.2s.

```bash
python run.py --out ../../docs/reports
```

Live report: `docs/reports/synthetic_after.html` (published by CI).
