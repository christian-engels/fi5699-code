# ============================================================================
# Week 4: Working with Data in Python
# 01b - Reading and Writing Data (CSV & Excel)
# ============================================================================
# Covers: read_csv, write_csv, scan_csv (lazy), read_excel, write_excel
#
# Dependencies:
#   uv add fastexcel   (for reading .xlsx)
#   uv add xlsxwriter  (for writing .xlsx)
# ============================================================================

import polars as pl
from pathlib import Path

# Create an output directory for our files
Path("data").mkdir(exist_ok=True)


# ============================================================================
# 1. Writing a CSV File
# ============================================================================
# First, let's create a DataFrame and save it so we have a file to read.

stocks = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "price":  [189.84, 378.91, 248.42, 178.25, 141.80],
    "shares": [50, 30, 20, 40, 35],
    "sector": ["Tech", "Tech", "Auto", "Retail", "Tech"],
})

stocks.write_csv("data/portfolio.csv")
print("=== Wrote data/portfolio.csv ===")
print(stocks)


# ============================================================================
# 2. Reading a CSV File
# ============================================================================

print("\n=== Reading it back with pl.read_csv() ===")
df = pl.read_csv("data/portfolio.csv")
print(df)


# ============================================================================
# 3. Useful read_csv Parameters
# ============================================================================

# Create a more complex CSV to demonstrate parameters
prices_data = pl.DataFrame({
    "date":   ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
    "ticker": ["AAPL", "AAPL", "AAPL", "AAPL"],
    "close":  [185.64, 184.25, 181.91, 185.56],
    "volume": [82488700, 58414500, 71983600, 49899900],
})
prices_data.write_csv("data/stock_prices.csv")

print("\n=== read_csv with parameters ===")
df = pl.read_csv(
    "data/stock_prices.csv",
    separator=",",          # default; use "\t" for TSV
    has_header=True,        # first row is column names
    n_rows=3,               # read only the first 3 rows
    try_parse_dates=True,   # auto-detect date columns
)
print(df)
print(f"Date column type: {df.schema['date']}")
# With try_parse_dates=True, the "date" column becomes a Date type
# instead of a plain string.


# ============================================================================
# 4. Write CSV with Options
# ============================================================================

print("\n=== Write with tab separator ===")
stocks.write_csv("data/portfolio.tsv", separator="\t")
print("Wrote data/portfolio.tsv (tab-separated)")

# Read the TSV back
df_tsv = pl.read_csv("data/portfolio.tsv", separator="\t")
print(df_tsv)


# ============================================================================
# 5. Lazy Reading with scan_csv
# ============================================================================
# For large files, scan_csv returns a LazyFrame instead of loading everything.
# Polars optimises the query before reading the data.

print("\n=== scan_csv: lazy reading ===")

# scan_csv does NOT read the file yet — it creates a query plan
lf = pl.scan_csv("data/stock_prices.csv", try_parse_dates=True)
print(f"Type: {type(lf)}")  # LazyFrame, not DataFrame

# Build a query (still no data read)
query = (
    lf
    .filter(pl.col("close") > 184)
    .select("date", "close")
)

# .collect() executes the optimised query and returns a DataFrame
result = query.collect()
print(result)

# Comparison:
#   read_csv  → reads entire file → returns DataFrame → filter in memory
#   scan_csv  → builds plan → optimises → reads only what's needed → returns DataFrame


# ============================================================================
# 6. Reading Excel Files
# ============================================================================
# Requires: uv add fastexcel (for reading)

# First, write an Excel file so we have one to read
stocks.write_excel("data/portfolio.xlsx")
print("\n=== Wrote data/portfolio.xlsx ===")

# Read it back
print("\n=== Reading Excel with pl.read_excel() ===")
df_excel = pl.read_excel("data/portfolio.xlsx")
print(df_excel)


# ============================================================================
# 7. Writing Excel with Sheet Names
# ============================================================================
# Requires: uv add xlsxwriter (for writing)

stocks.write_excel("data/portfolio.xlsx", worksheet="Holdings")
print("\n=== Wrote data/portfolio.xlsx (worksheet='Holdings') ===")

# Read a specific sheet
df_sheet = pl.read_excel("data/portfolio.xlsx", sheet_name="Holdings")
print(df_sheet)


# ============================================================================
# 8. Round-Trip Verification
# ============================================================================
# Write → Read → Compare: does the data survive the round trip?

print("\n=== Round-trip verification ===")

# CSV round-trip
stocks.write_csv("data/roundtrip.csv")
csv_back = pl.read_csv("data/roundtrip.csv")
print(f"CSV round-trip matches: {stocks.equals(csv_back)}")

# Excel round-trip
stocks.write_excel("data/roundtrip.xlsx")
xlsx_back = pl.read_excel("data/roundtrip.xlsx")
print(f"Excel round-trip matches: {stocks.equals(xlsx_back)}")


# ============================================================================
# Summary
# ============================================================================
# Function        | What it does                 | Notes
# --------------- | ---------------------------- | ----------------------------
# pl.read_csv()   | Read CSV → DataFrame         | Simple, immediate
# pl.scan_csv()   | Read CSV → LazyFrame         | Optimised for large files
# df.write_csv()  | DataFrame → CSV file         | Fast, universal format
# pl.read_excel() | Read .xlsx → DataFrame       | Needs fastexcel or openpyxl
# df.write_excel()| DataFrame → .xlsx file       | Needs xlsxwriter
#
# Performance tip: CSV and Parquet are much faster than Excel for large
# datasets. Use Excel when sharing with non-programmers; use CSV or
# Parquet for your own analysis pipelines.

print("\n=== Files created ===")
for f in sorted(Path("data").glob("*")):
    print(f"  {f}  ({f.stat().st_size:,} bytes)")
