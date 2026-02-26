# ============================================================================
# Week 4: Working with Data in Python
# 03 - Working with Expressions
# ============================================================================
# Covers: arithmetic, comparisons, boolean combining, when/then/otherwise,
#         casting, expression expansion, naming (alias, prefix, suffix)
# ============================================================================

import polars as pl

# Our working dataset
stocks = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "price":  [189.84, 378.91, 248.42, 178.25, 141.80],
    "shares": [50, 30, 20, 40, 35],
    "sector": ["Tech", "Tech", "Auto", "Retail", "Tech"],
})


# ----------------------------------------------------------------------------
# 1. Column Arithmetic Works Element-Wise
# ----------------------------------------------------------------------------
# Polars applies operations to entire columns at once — no loops needed.

print("=== Arithmetic: scalar and column operations ===")
result = stocks.select(
    "ticker",
    (pl.col("price") + 10).alias("price_adj"),            # scalar
    (pl.col("price") * pl.col("shares")).alias("value"),   # column
)
print(result)


# ----------------------------------------------------------------------------
# 2. Comparisons Return Boolean Columns
# ----------------------------------------------------------------------------

print("\n=== Comparisons: Boolean columns ===")
result = stocks.select(
    "ticker", "price",
    is_expensive=pl.col("price") > 200,
    is_tech=pl.col("sector") == "Tech",
)
print(result)


# ----------------------------------------------------------------------------
# 3. Combining Conditions with & and |
# ----------------------------------------------------------------------------
# Use & (and) and | (or) to combine Boolean expressions.
# PARENTHESES ARE REQUIRED around each condition.

print("\n=== Combining conditions: Tech stocks above 150 ===")
result = stocks.filter(
    (pl.col("price") > 150) & (pl.col("sector") == "Tech")
)
print(result)

print("\n=== Using | (or): price > 300 OR sector is Auto ===")
result = stocks.filter(
    (pl.col("price") > 300) | (pl.col("sector") == "Auto")
)
print(result)


# ----------------------------------------------------------------------------
# 4. Conditionals: when / then / otherwise
# ----------------------------------------------------------------------------
# Create new values based on conditions — like Excel's IF() but chainable.

print("\n=== when/then/otherwise: size labels ===")
result = stocks.select(
    "ticker", "price",
    size=pl.when(pl.col("price") > 300).then(pl.lit("Large"))
           .when(pl.col("price") > 200).then(pl.lit("Mid"))
           .otherwise(pl.lit("Small"))
)
print(result)


# ----------------------------------------------------------------------------
# 5. Casting: Changing Data Types
# ----------------------------------------------------------------------------
# Use .cast() to convert a column's type.

print("\n=== Casting: Float64 -> Int64, Int64 -> Float64 ===")
result = stocks.select(
    "ticker",
    pl.col("price").cast(pl.Int64).alias("price_int"),
    pl.col("shares").cast(pl.Float64).alias("shares_f"),
)
print(result)
# Note: floats are TRUNCATED (not rounded) when cast to integers.
# 189.84 becomes 189.


# ----------------------------------------------------------------------------
# 6. Expression Expansion: Many Columns at Once
# ----------------------------------------------------------------------------
# Pass multiple names to pl.col() to apply the same expression to all of them.

print("\n=== Expression expansion: mean of price and shares ===")
result = stocks.select(
    pl.col("price", "shares").mean(),
)
print(result)


# ----------------------------------------------------------------------------
# 7. Naming Results with alias, prefix, and suffix
# ----------------------------------------------------------------------------

# .alias() renames a single result
print("\n=== .alias() for single column ===")
result = stocks.select(
    pl.col("price").mean().alias("avg_price"),
)
print(result)

# .name.prefix() / .name.suffix() for batches
print("\n=== .name.prefix() for multiple columns ===")
result = stocks.select(
    pl.col("price", "shares").mean().name.prefix("avg_"),
)
print(result)

print("\n=== .name.suffix() for multiple columns ===")
result = stocks.select(
    pl.col("price", "shares").max().name.suffix("_max"),
)
print(result)
