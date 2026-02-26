# ============================================================================
# Week 4: Working with Data in Python
# 05 - Reshaping Data
# ============================================================================
# Covers: pivot (long to wide) and unpivot (wide to long)
# ============================================================================

import polars as pl


# ----------------------------------------------------------------------------
# Wide vs Long: Two Ways to Organise the Same Data
# ----------------------------------------------------------------------------
#
# WIDE format — each variable gets its own column:
#   ticker | Jan  | Feb
#   AAPL   |  5.2 | -1.4
#   MSFT   |  3.1 |  2.8
#   → Compact, human-readable. Good for summary tables.
#
# LONG format — one row per observation:
#   ticker | month | return
#   AAPL   | Jan   |  5.2
#   AAPL   | Feb   | -1.4
#   MSFT   | Jan   |  3.1
#   MSFT   | Feb   |  2.8
#   → Tidy, easy to plot and analyse. Good for computation.


# ----------------------------------------------------------------------------
# 1. Pivot: Long to Wide
# ----------------------------------------------------------------------------

returns_long = pl.DataFrame({
    "ticker":     ["AAPL", "AAPL", "MSFT", "MSFT"],
    "month":      ["Jan", "Feb", "Jan", "Feb"],
    "return_pct": [5.2, -1.4, 3.1, 2.8],
})

print("=== Long format (starting data) ===")
print(returns_long)

result = returns_long.pivot(
    index="ticker",     # rows
    on="month",         # becomes new columns
    values="return_pct" # fills the cells
)

print("\n=== After pivot: wide format ===")
print(result)
# Each unique value in "month" becomes a new column.
# The table gets wider and shorter.


# ----------------------------------------------------------------------------
# 2. Unpivot: Wide to Long
# ----------------------------------------------------------------------------

returns_wide = pl.DataFrame({
    "ticker": ["AAPL", "MSFT"],
    "jan":    [5.2, 3.1],
    "feb":    [-1.4, 2.8],
})

print("\n=== Wide format (starting data) ===")
print(returns_wide)

result = returns_wide.unpivot(
    index="ticker",          # stays as rows
    on=["jan", "feb"],       # these columns become values
)

print("\n=== After unpivot: long format ===")
print(result)
# Column names become values in a new "variable" column.
# The table gets taller and narrower.


# ----------------------------------------------------------------------------
# 3. Round-Trip: Long -> Wide -> Long
# ----------------------------------------------------------------------------

print("\n=== Round-trip demonstration ===")

# Start long
data_long = pl.DataFrame({
    "ticker":     ["AAPL", "AAPL", "AAPL", "MSFT", "MSFT", "MSFT"],
    "month":      ["Jan", "Feb", "Mar", "Jan", "Feb", "Mar"],
    "return_pct": [5.2, -1.4, 2.1, 3.1, 2.8, -0.5],
})
print("Long:")
print(data_long)

# Pivot to wide
data_wide = data_long.pivot(
    index="ticker", on="month", values="return_pct"
)
print("\nWide (after pivot):")
print(data_wide)

# Unpivot back to long
data_back = data_wide.unpivot(
    index="ticker", on=["Jan", "Feb", "Mar"]
)
print("\nLong again (after unpivot):")
print(data_back)


# ----------------------------------------------------------------------------
# When to Use Which Format
# ----------------------------------------------------------------------------
#          | Wide                          | Long
# ---------|-------------------------------|-----------------------------
# Good for | Reading, summary tables       | Plotting, group_by, regression
# Shape    | Fewer rows, more columns      | More rows, fewer columns
# Convert  | .pivot()                      | .unpivot()
# Analogy  | Excel pivot table output      | Tidy data, "one row per obs"
#
# Rule of thumb:
#   Need to group_by or plot? → go long
#   Human needs to read a table? → go wide
