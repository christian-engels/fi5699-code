# ============================================================================
# Week 4: Working with Data in Python
# 04 - Combining DataFrames
# ============================================================================
# Covers: joins (inner, left, anti, semi, full) and concatenation
# ============================================================================

import polars as pl

# ----------------------------------------------------------------------------
# Setup: two tables sharing a "ticker" key column
# ----------------------------------------------------------------------------

stocks = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "price":  [189.84, 378.91, 248.42, 178.25, 141.80],
    "shares": [50, 30, 20, 40, 35],
    "sector": ["Tech", "Tech", "Auto", "Retail", "Tech"],
})

company_info = pl.DataFrame({
    "ticker":    ["AAPL", "MSFT", "TSLA", "META", "NVDA"],
    "employees": [164000, 221000, 128000, 67317, 29600],
    "founded":   [1976, 1975, 2003, 2004, 1993],
})

print("=== stocks ===")
print(stocks)
print("\n=== company_info ===")
print(company_info)


# ----------------------------------------------------------------------------
# 1. Inner Join: Only Matching Rows Survive
# ----------------------------------------------------------------------------
# Keeps only rows where the key appears in BOTH tables.

print("\n=== Inner join ===")
result = stocks.join(company_info, on="ticker", how="inner")
print(result)
# Only AAPL, MSFT, TSLA remain. AMZN, GOOGL, META, NVDA are dropped.


# ----------------------------------------------------------------------------
# 2. Left Join: Keep All Left Rows
# ----------------------------------------------------------------------------
# Keeps all rows from the LEFT table. Where no match, fills null.

print("\n=== Left join ===")
result = stocks.join(company_info, on="ticker", how="left")
print(result)
# All 5 stocks survive. AMZN and GOOGL get null for employees/founded.


# ----------------------------------------------------------------------------
# 3. Anti Join: Find What's Missing
# ----------------------------------------------------------------------------
# Returns left-table rows that have NO match on the right.
# Useful for finding gaps in your data.

print("\n=== Anti join: stocks missing from company_info ===")
result = stocks.join(company_info, on="ticker", how="anti")
print(result)
# AMZN and GOOGL — they have no match in company_info.


# ----------------------------------------------------------------------------
# 4. Semi Join: Filter by Existence
# ----------------------------------------------------------------------------
# Returns left-table rows that HAVE a match on the right.
# Like filter, but using another table as the condition.

print("\n=== Semi join: stocks that appear in company_info ===")
result = stocks.join(company_info, on="ticker", how="semi")
print(result)
# AAPL, MSFT, TSLA — same rows as inner join, but only left columns.


# ----------------------------------------------------------------------------
# 5. Full Join: Keep Everything
# ----------------------------------------------------------------------------
# All rows from both sides. Unmatched rows get null.

print("\n=== Full join ===")
result = stocks.join(company_info, on="ticker", how="full", coalesce=True)
print(result)


# ----------------------------------------------------------------------------
# Join Types Summary
# ----------------------------------------------------------------------------
# Type   | Rows kept                    | Use when...
# ------ | ---------------------------- | --------------------------------
# inner  | Only matching from both      | Need complete records from both
# left   | All left, matches from right | Enrich a primary table
# full   | All rows from both sides     | Full union of both datasets
# anti   | Left rows with NO match      | Finding gaps or missing data
# semi   | Left rows that HAVE a match  | Filtering by existence


# ============================================================================
# Concatenation: Stacking DataFrames
# ============================================================================

# ----------------------------------------------------------------------------
# 6. Vertical Concatenation: Stack Rows
# ----------------------------------------------------------------------------
# Use when data is split across files (e.g. one CSV per month).

jan = pl.DataFrame({"ticker": ["AAPL", "MSFT"], "return_pct": [5.2, 3.1]})
feb = pl.DataFrame({"ticker": ["AAPL", "MSFT"], "return_pct": [-1.4, 2.8]})

print("\n=== Vertical concatenation: stack rows ===")
result = pl.concat([jan, feb], how="vertical")
print(result)
# Same columns, more rows.


# ----------------------------------------------------------------------------
# 7. Horizontal Concatenation: Add Columns Side by Side
# ----------------------------------------------------------------------------
# Use when you have separate columns that share the same row order.

tickers = pl.DataFrame({"ticker": ["AAPL", "MSFT", "TSLA"]})
metrics = pl.DataFrame({"pe_ratio": [28.5, 35.2, 62.1]})

print("\n=== Horizontal concatenation: add columns ===")
result = pl.concat([tickers, metrics], how="horizontal")
print(result)
# Same rows, more columns.
