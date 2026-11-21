# 📂 Data

The five datasets behind the five sections. The Power BI reports in the sections are built on these files.

| File | Sheet | Rows × columns | Size | Used in | What it is |
|---|---|:-:|--:|---|---|
| [`superstore-us-2015.xlsx`](superstore-us-2015.xlsx) | Orders | 1,952 × 25 | 530 KB | Section 1 | Orders, returns and regional managers of a US retailer |
| [`superstore-us-2015.xlsx`](superstore-us-2015.xlsx) | Returns | 1,634 × 2 | 530 KB | Section 1 | Orders, returns and regional managers of a US retailer |
| [`superstore-us-2015.xlsx`](superstore-us-2015.xlsx) | Users | 4 × 2 | 530 KB | Section 1 | Orders, returns and regional managers of a US retailer |
| [`office-supplies.csv`](office-supplies.csv) | – | 43 × 6 | 2 KB | Section 2 | Office supply orders by region, rep and item |
| [`long-term-unemployment.xlsx`](long-term-unemployment.xlsx) | Sheet1 | 1,708 × 4 | 46 KB | Section 3 | Monthly long-term unemployed by age group and gender |
| [`amazing-mart-eu-geo.xlsx`](amazing-mart-eu-geo.xlsx) | ListOfOrders | 4,117 × 12 | 731 KB | Section 4 | Orders with city coordinates and order lines with sales and profit |
| [`amazing-mart-eu-geo.xlsx`](amazing-mart-eu-geo.xlsx) | OrderBreakdown | 8,047 × 8 | 731 KB | Section 4 | Orders with city coordinates and order lines with sales and profit |
| [`uk-bank-customers.xlsx`](uk-bank-customers.xlsx) | Sheet2 | 175 × 3 | 356 KB | Section 5 | Bank customers: gender, age, region, job class, balance |
| [`uk-bank-customers.xlsx`](uk-bank-customers.xlsx) | Data | 4,014 × 9 | 356 KB | Section 5 | Bank customers: gender, age, region, job class, balance |

> `superstore-us-2015.xlsx` has 1,952 order lines but 1,951 distinct `Row ID` values: one `Row ID` appears twice. `uk-bank-customers.xlsx` and `long-term-unemployment.xlsx` also contain empty helper sheets that are not listed.

---

*Built by [Evgenii Matveev](https://github.com/evgeniimatveev) · Data Analyst / Analytics & MLOps Engineer*
