# ============================================================================
# Week 4: Working with Data in Python
# 06 - Visualising Data with plotnine
# ============================================================================
# Covers: Grammar of Graphics, bar charts, scatter plots, line charts,
#         histograms, themes and labels, saving plots
# ============================================================================

from pathlib import Path

import polars as pl
from plotnine import ggplot, aes, geom_col, geom_point, geom_line, geom_histogram
from plotnine import labs, theme_minimal


# ----------------------------------------------------------------------------
# The Grammar of Graphics
# ----------------------------------------------------------------------------
# plotnine implements the Grammar of Graphics — every plot is built from
# independent layers combined with +:
#
#   ggplot(data, aes(...))   — data + aesthetic mapping
#   + geom_*()               — geometry (points, bars, lines)
#   + labs(...)              — labels (title, axes)
#   + theme_*()             — visual polish
#
# plotnine works with pandas, so we convert: stocks.to_pandas()


# ----------------------------------------------------------------------------
# Setup: create our data
# ----------------------------------------------------------------------------

stocks = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
    "price":  [189.84, 378.91, 248.42, 178.25, 141.80],
    "shares": [50, 30, 20, 40, 35],
    "sector": ["Tech", "Tech", "Auto", "Retail", "Tech"],
})

# Add position_value and convert to pandas for plotnine
stocks_pd = stocks.with_columns(
    position_value=pl.col("price") * pl.col("shares"),
).to_pandas()

Path("figures").mkdir(exist_ok=True)

print("=== Data for plotting (pandas DataFrame) ===")
print(stocks_pd)


# ----------------------------------------------------------------------------
# 1. Bar Chart: Comparing Categories
# ----------------------------------------------------------------------------

print("\n=== Bar chart: position values by ticker ===")
p1 = (
    ggplot(stocks_pd, aes(x="ticker", y="position_value", fill="sector"))
    + geom_col()
    + labs(
        title="Portfolio Position Values",
        x="Ticker",
        y="Value ($)",
        fill="Sector",
    )
    + theme_minimal()
)
p1.save("figures/bar_chart.pdf", width=8, height=5)
p1.show()
print("Saved: figures/bar_chart.pdf")


# ----------------------------------------------------------------------------
# 2. Scatter Plot: Relationships Between Variables
# ----------------------------------------------------------------------------

print("\n=== Scatter plot: price vs shares ===")
p2 = (
    ggplot(stocks_pd, aes(x="price", y="shares", color="sector"))
    + geom_point(size=4)
    + labs(
        title="Price vs Shares Held",
        x="Price ($)",
        y="Shares",
        color="Sector",
    )
    + theme_minimal()
)
p2.save("figures/scatter_plot.pdf", width=8, height=5)
p2.show()
print("Saved: figures/scatter_plot.pdf")


# ----------------------------------------------------------------------------
# 3. Line Chart: Tracking Values Over Time
# ----------------------------------------------------------------------------

# Create time-series data
returns_data = pl.DataFrame({
    "ticker": ["AAPL"] * 6 + ["MSFT"] * 6 + ["TSLA"] * 6,
    "month":  list(range(1, 7)) * 3,
    "return_pct": [
        2.1, -0.5, 1.8, 3.2, -1.1, 2.4,   # AAPL
        1.5, 0.8, -0.3, 2.1, 1.7, 0.9,     # MSFT
        5.2, -3.1, 4.5, -2.8, 6.1, -1.5,   # TSLA
    ],
})

# Convert to pandas and compute cumulative growth of $100
returns_pd = returns_data.to_pandas()
returns_pd["cumulative"] = returns_pd.groupby("ticker")["return_pct"].transform(
    lambda x: 100 * (1 + x / 100).cumprod()
)

print("\n=== Line chart: cumulative growth of $100 ===")
p3 = (
    ggplot(returns_pd, aes(x="month", y="cumulative", color="ticker", group="ticker"))
    + geom_line(size=1.2)
    + geom_point(size=3)
    + labs(
        title="Growth of $100 Investment",
        x="Month",
        y="Value ($)",
        color="Ticker",
    )
    + theme_minimal()
)
p3.save("figures/line_chart.pdf", width=8, height=5)
p3.show()
print("Saved: figures/line_chart.pdf")


# ----------------------------------------------------------------------------
# 4. Histogram: Distribution of a Variable
# ----------------------------------------------------------------------------

print("\n=== Histogram: distribution of returns ===")
p4 = (
    ggplot(returns_pd, aes(x="return_pct"))
    + geom_histogram(bins=8, fill="#2166AC", color="white", alpha=0.8)
    + labs(
        title="Distribution of Monthly Returns",
        x="Return (%)",
        y="Count",
    )
    + theme_minimal()
)
p4.save("figures/histogram.pdf", width=8, height=5)
p4.show()
print("Saved: figures/histogram.pdf")


# ----------------------------------------------------------------------------
# Key geom_* functions summary
# ----------------------------------------------------------------------------
# Geom              | Plot type      | Use when...
# ------------------|----------------|----------------------------------
# geom_col()        | Bar chart      | Comparing categories
# geom_point()      | Scatter plot   | Relationships between two vars
# geom_line()       | Line chart     | Tracking values over time
# geom_histogram()  | Histogram      | Distribution of a variable
# geom_smooth()     | Trend line     | Adding a fitted line to scatter
#
# The pattern:
#   ggplot(data, aes(...)) + geom_*() + labs() + theme_*()
#   Swap the geom to change the chart type. Everything else stays the same.

print("\nAll plots saved to figures/. Open the PDF files to view them.")
