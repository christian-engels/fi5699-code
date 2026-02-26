# ============================================================================
# Week 4: Working with Data in Python
# 02 - Expressions and Contexts
# ============================================================================
# Covers: select, with_columns, filter, group_by — the four core contexts
# ============================================================================

import polars as pl

# Our working dataset
stocks = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "price":  [189.84, 378.91, 248.42, 178.25, 141.80],
    "shares": [50, 30, 20, 40, 35],
    "sector": ["Tech", "Tech", "Auto", "Retail", "Tech"],
})

print("=== Starting data ===")
print(stocks)


# ----------------------------------------------------------------------------
# Key concept: Expressions vs Contexts
# ----------------------------------------------------------------------------
# An EXPRESSION describes WHAT to compute:
#     pl.col("price") * pl.col("shares")
#
# A CONTEXT describes WHERE to put the result:
#     df.select(...)       — pick and transform columns
#     df.with_columns(...) — add new columns, keep existing
#     df.filter(...)       — keep matching rows
#     df.group_by(...)     — aggregate by group


# ----------------------------------------------------------------------------
# 1. select — Pick and Transform Columns
# ----------------------------------------------------------------------------
# select returns ONLY the columns you ask for.

print("\n=== Context 1: select ===")
result = stocks.select(
    "ticker",
    (pl.col("price") * pl.col("shares")).alias("position_value"),
)
print(result)


# ----------------------------------------------------------------------------
# 2. with_columns — Add New Columns
# ----------------------------------------------------------------------------
# with_columns keeps ALL existing columns and adds new ones.

print("\n=== Context 2: with_columns ===")
result = stocks.with_columns(
    position_value=pl.col("price") * pl.col("shares"),
)
print(result)


# ----------------------------------------------------------------------------
# 3. filter — Keep Matching Rows
# ----------------------------------------------------------------------------
# filter keeps only rows where the condition is True.

print("\n=== Context 3: filter (price > 200) ===")
result = stocks.filter(pl.col("price") > 200)
print(result)


# ----------------------------------------------------------------------------
# 4. group_by — Aggregate by Group
# ----------------------------------------------------------------------------
# group_by splits data into groups, then applies aggregation functions.

print("\n=== Context 4: group_by ===")
result = stocks.group_by("sector").agg(
    pl.col("price").mean().alias("avg_price"),
    pl.len().alias("count"),
)
print(result.sort("sector"))


# ----------------------------------------------------------------------------
# Summary: The Four Contexts at a Glance
# ----------------------------------------------------------------------------
# Context       | What it does              | Excel analogy
# ------------- | ------------------------- | ---------------------------
# select        | Pick and transform cols   | Choosing columns to display
# with_columns  | Add or overwrite columns  | Adding a formula column
# filter        | Keep matching rows        | AutoFilter on a column
# group_by      | Aggregate by group        | Pivot table: group + summarise
