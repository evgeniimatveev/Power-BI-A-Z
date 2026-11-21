"""Check the numbers printed in the Power BI report screenshots (PDF) against the source data.

Power BI Desktop exports each report page to PDF. The values a visual shows (shares, totals, counts)
can be re-computed from the dataset the report was built on; a check passes when every value is reproduced.

    uv run --no-project --with pandas --with openpyxl --with pypdf python .github/scripts/check_reports.py
"""
import os
import re
import sys
from collections import Counter

import pandas as pd
from pypdf import PdfReader

results = []  # (name, compared, mismatches, examples)


def pdf_text(path):
    return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)


def record_sets(name, in_report, in_data):
    """every id of the data must appear in the report and vice versa"""
    bad = [f"id {i}: " + ("missing in the report" if i in in_data else "not in the data") for i in sorted(in_report ^ in_data)]
    results.append((name, len(in_data), len(bad), bad[:3]))


def record(name, pairs):
    """pairs: list of (label, from_pdf, from_data)"""
    bad = [f"{lab}: report {a} vs data {b}" for lab, a, b in pairs if a != b]
    results.append((name, len(pairs), len(bad), bad[:3]))


# 1. Section 1 - the Users sheet printed as PDF
users = pd.read_excel("data/superstore-us-2015.xlsx", sheet_name="Users")
txt = pdf_text("01-getting-started/screenshots/users-sheet.pdf")
record("S1  Users sheet: manager per region", [(r.Region, f"{r.Region} {r.Manager}" in txt, True) for r in users.itertuples()])

# 2. Section 1 - the Returns sheet printed as PDF: every returned order id
ret = pd.read_excel("data/superstore-us-2015.xlsx", sheet_name="Returns")
ids = {int(m) for m in re.findall(r"^(\d+) Returned\s*$", pdf_text("01-getting-started/screenshots/returns-sheet.pdf"), re.M)}
record_sets("S1  Returns sheet: returned order ids", ids, set(ret["Order ID"]))

# 3. Section 1 - the Orders sheet printed as PDF: every Row ID
orders = pd.read_excel("data/superstore-us-2015.xlsx", sheet_name="Orders")
rows = {int(m) for m in re.findall(r"^(\d+) (?:Critical|High|Medium|Low|Not Specified) ", pdf_text("01-getting-started/screenshots/orders-sheet.pdf"), re.M)}
record_sets("S1  Orders sheet: Row IDs", rows, set(orders["Row ID"]))

# 4. Section 2 - units by region (donut) and by sales rep (bar chart)
off = pd.read_csv("data/office-supplies.csv")
txt = pdf_text("02-first-bar-chart/screenshots/s2-final.pdf")
share = (off.groupby("Region")["Units"].sum() / off["Units"].sum() * 100).round(2)
pairs = [(f"{reg} share", f"{share[reg]:.2f}%" in txt, True) for reg in share.index]
rep_totals = off.groupby(["Rep", "Region"])["Units"].sum().tolist()      # one bar per rep and region
shown = Counter(int(n) for n in re.findall(r"\b(\d{2,3})\b", txt[txt.index("Rep"):]))
need = Counter(rep_totals)
pairs += [(f"bar value {v} (x{c})", shown[v] >= c, True) for v, c in sorted(need.items())]
record("S2  Office supplies: units by region and by rep", pairs)

# 5. Section 5 - UK bank customers: card, pie chart and tree map
bank = pd.read_excel("data/uk-bank-customers.xlsx", sheet_name="Data")
txt = pdf_text("05-robust-bi-dashboard/screenshots/s5-bi-report-final.pdf")
pairs = [("customer count", f"{len(bank):,}" in txt, True)]
for col in ("Gender", "Job Classification"):
    sh = (bank[col].value_counts(normalize=True) * 100).round(2)
    pairs += [(f"{col}: {k}", f"{v:.2f}%" in txt, True) for k, v in sh.items()]
pairs += [("regions on the map", all(r in txt for r in bank["Region"].unique()), True)]
record("S5  UK bank: customers, gender, job classification, regions", pairs)

width = max(len(n) for n, *_ in results)
failed = 0
lines = ["| Report page | Values checked | Mismatches |", "|---|--:|--:|"]
for name, n, bad, ex in results:
    ok = bad == 0 and n > 0
    failed += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {name:<{width}}  {n:>5} values compared, {bad} mismatching")
    for e in ex:
        print("      ", e)
    lines.append(f"| {name} | {n} | {'✅ 0' if ok else '❌ ' + str(bad)} |")
summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as fh:
        fh.write("## Report screenshots checked against the data\n\n" + "\n".join(lines) + "\n")
print(f"\n{len(results) - failed} of {len(results)} report checks passed")
sys.exit(1 if failed else 0)
