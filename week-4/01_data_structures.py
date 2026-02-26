# ============================================================================
# Week 4: Working with Data in Python
# 01 - Polars Data Structures
# ============================================================================
# Covers: DataFrames, Series, data types, inspecting data, null handling
# ============================================================================

import polars as pl

# ----------------------------------------------------------------------------
# 1. Creating a DataFrame
# ----------------------------------------------------------------------------
# A DataFrame is a table of rows and columns — like a spreadsheet.
# Each column has a name and a data type. All values in a column share a type.

stocks = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "price":  [189.84, 378.91, 248.42, 178.25, 141.80],
    "shares": [50, 30, 20, 40, 35],
    "sector": ["Tech", "Tech", "Auto", "Retail", "Tech"],
})

print("=== Our stocks DataFrame ===")
print(stocks)


# ----------------------------------------------------------------------------
# 2. Data Types
# ----------------------------------------------------------------------------
# Polars infers types automatically from the data you provide.
# Common types:
#   Int64    — whole numbers (shares: 50, 30, 20)
#   Float64  — decimal numbers (price: 189.84, 378.91)
#   String   — text (ticker: "AAPL", "MSFT")
#   Boolean  — True / False
#   Date     — 2024-01-15
#   Datetime — 2024-01-15 09:30:00
#   Null     — missing value

print("\n=== Schema: column names and types ===")
print(stocks.schema)


# ----------------------------------------------------------------------------
# 3. Series — a single column
# ----------------------------------------------------------------------------
# A Series is a one-dimensional typed array — one column of a DataFrame.

prices = pl.Series("price", [189.84, 378.91, 248.42])
print("\n=== A Series ===")
print(prices)
print(f"Type:  {prices.dtype}")
print(f"Mean:  {prices.mean():.2f}")


# ----------------------------------------------------------------------------
# 4. Inspecting Your Data
# ----------------------------------------------------------------------------
# Five quick methods to understand what you have:

print("\n=== .head(3) — first 3 rows ===")
print(stocks.head(3))

print("\n=== .tail(2) — last 2 rows ===")
print(stocks.tail(2))

print("\n=== .shape — (rows, columns) ===")
print(stocks.shape)

print("\n=== .columns — column names ===")
print(stocks.columns)

print("\n=== .schema — names and types ===")
print(stocks.schema)


# ----------------------------------------------------------------------------
# 5. Summary Statistics with describe()
# ----------------------------------------------------------------------------
# One command gives you count, mean, std, min, max, and quartiles.

print("\n=== .describe() — summary statistics ===")
print(stocks.describe())


# ----------------------------------------------------------------------------
# 6. Null Means Missing
# ----------------------------------------------------------------------------
# Polars uses null for missing data. Every data type supports it.
# Unlike Excel's blank cells, a null is explicit and typed.

stocks_with_nulls = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA"],
    "price":  [189.84, None, 248.42],       # None becomes null
    "volume": [1000000, 2500000, None],
})

print("\n=== DataFrame with null values ===")
print(stocks_with_nulls)

# null propagates through calculations: null + 5 = null
print("\n=== null propagation: price + 10 ===")
print(stocks_with_nulls.with_columns(
    price_plus_10=pl.col("price") + 10,
))

# Detecting and filling nulls
print("\n=== Detecting nulls with .is_null() ===")
print(stocks_with_nulls.with_columns(
    price_missing=pl.col("price").is_null(),
))

print("\n=== Filling nulls with .fill_null() ===")
print(stocks_with_nulls.with_columns(
    price_filled=pl.col("price").fill_null(0.0),
))
