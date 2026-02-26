# ============================================================================
# Week 4: Working with Data in Python
# 07 - Working with Real Stock Returns (Tidy Finance)
# ============================================================================
# Downloads real stock price data from Yahoo Finance via tidyfinance,
# then applies every concept from scripts 01-06 on actual market data.
#
# Based on: https://www.tidy-finance.org/python/working-with-stock-returns.html
# ============================================================================

from pathlib import Path

import polars as pl
import numpy as np
import tidyfinance as tf
from plotnine import (
    ggplot, aes, geom_line, geom_histogram, geom_col, geom_point,
    geom_vline, labs, theme_minimal, scale_x_continuous, scale_x_datetime,
    theme, element_text,
)
from mizani.formatters import percent_format


# ============================================================================
# 1. Downloading Stock Prices
# ============================================================================
# tidyfinance wraps Yahoo Finance into a clean download function.
# It returns a pandas DataFrame, which we convert to Polars.

print("=" * 60)
print("1. DOWNLOADING STOCK PRICES")
print("=" * 60)

# Download daily prices for five stocks
symbols = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]

prices_pd = tf.download_data(
    domain="stock_prices",
    symbols=symbols,
    start_date="2020-01-01",
    end_date="2024-12-31",
)

# Convert to Polars — our tool for the course
prices = pl.from_pandas(prices_pd)

print(f"Downloaded {prices.shape[0]:,} rows for {len(symbols)} stocks")
print(f"Date range: {prices['date'].min()} to {prices['date'].max()}")
print()
print(prices.head(10))


# ============================================================================
# 2. Inspecting the Data (Script 01 concepts)
# ============================================================================

print("\n" + "=" * 60)
print("2. INSPECTING THE DATA")
print("=" * 60)

print(f"\nShape: {prices.shape}")
print(f"Columns: {prices.columns}")
print(f"\nSchema:")
print(prices.schema)

print("\nSummary statistics:")
print(prices.describe())


# ============================================================================
# 3. Computing Daily Returns (Scripts 02-03 concepts)
# ============================================================================
# A return is the percentage change in adjusted closing price:
#   r_t = (P_t / P_{t-1}) - 1

print("\n" + "=" * 60)
print("3. COMPUTING DAILY RETURNS")
print("=" * 60)

returns_daily = (
    prices
    .sort("symbol", "date")
    .with_columns(
        ret=pl.col("adjusted_close").pct_change().over("symbol")
    )
    .filter(pl.col("ret").is_not_null())
    .select("symbol", "date", "adjusted_close", "volume", "ret")
)

print(f"\n{returns_daily.shape[0]:,} daily return observations")
print(returns_daily.head(10))


# ============================================================================
# 4. Summary Statistics by Stock (Script 02: group_by)
# ============================================================================

print("\n" + "=" * 60)
print("4. SUMMARY STATISTICS BY STOCK")
print("=" * 60)

summary = returns_daily.group_by("symbol").agg(
    n_obs=pl.len(),
    mean_ret=pl.col("ret").mean(),
    std_ret=pl.col("ret").std(),
    min_ret=pl.col("ret").min(),
    max_ret=pl.col("ret").max(),
    median_ret=pl.col("ret").median(),
)

print(summary.sort("symbol"))


# ============================================================================
# 5. Filtering and Expressions (Script 03 concepts)
# ============================================================================

print("\n" + "=" * 60)
print("5. FILTERING AND EXPRESSIONS")
print("=" * 60)

# Which stock had the best average return?
best_stock = summary.sort("mean_ret", descending=True).head(1)
print(f"\nBest average daily return: {best_stock['symbol'][0]}")
print(f"  Mean: {best_stock['mean_ret'][0]:.6f}")

# Extreme return days (more than 5% move)
extreme_days = returns_daily.filter(pl.col("ret").abs() > 0.05)
print(f"\nDays with |return| > 5%: {extreme_days.shape[0]}")
print(extreme_days.sort("ret").head(5))
print(extreme_days.sort("ret", descending=True).head(5))

# Add classification: large gain, large loss, or normal day
classified = returns_daily.with_columns(
    day_type=pl.when(pl.col("ret") > 0.02).then(pl.lit("Large gain"))
              .when(pl.col("ret") < -0.02).then(pl.lit("Large loss"))
              .otherwise(pl.lit("Normal"))
)

day_counts = classified.group_by("day_type").agg(
    count=pl.len(),
    avg_ret=pl.col("ret").mean(),
)
print("\nDay classification:")
print(day_counts.sort("day_type"))


# ============================================================================
# 6. Monthly Returns (Script 05: reshaping + aggregation)
# ============================================================================
# Compound daily returns into monthly: (1+r1)(1+r2)...(1+rn) - 1

print("\n" + "=" * 60)
print("6. MONTHLY RETURNS")
print("=" * 60)

returns_monthly = (
    returns_daily
    .with_columns(
        year_month=pl.col("date").dt.strftime("%Y-%m")
    )
    .group_by("symbol", "year_month")
    .agg(
        ret_monthly=(pl.col("ret") + 1).product() - 1,
        n_trading_days=pl.len(),
    )
    .sort("symbol", "year_month")
)

print(f"{returns_monthly.shape[0]} monthly observations")
print(returns_monthly.head(10))

# Monthly summary by stock
monthly_summary = returns_monthly.group_by("symbol").agg(
    mean_monthly=pl.col("ret_monthly").mean(),
    std_monthly=pl.col("ret_monthly").std(),
    best_month=pl.col("ret_monthly").max(),
    worst_month=pl.col("ret_monthly").min(),
)
print("\nMonthly return summary:")
print(monthly_summary.sort("symbol"))


# ============================================================================
# 7. Pivot: Monthly Returns Table (Script 05 concepts)
# ============================================================================

print("\n" + "=" * 60)
print("7. PIVOT: MONTHLY RETURNS TABLE (last 6 months)")
print("=" * 60)

# Get last 6 months and pivot to wide format
last_6_months = (
    returns_monthly
    .select("year_month")
    .unique()
    .sort("year_month", descending=True)
    .head(6)
    .to_series()
    .to_list()
)

recent = (
    returns_monthly
    .sort("year_month", descending=True)
    .filter(pl.col("year_month").is_in(last_6_months))
    .select("symbol", "year_month", "ret_monthly")
)

wide_returns = recent.pivot(
    index="symbol",
    on="year_month",
    values="ret_monthly",
)

print(wide_returns.sort("symbol"))


# ============================================================================
# 8. Visualisation (Script 06 concepts)
# ============================================================================

print("\n" + "=" * 60)
print("8. VISUALISATION")
print("=" * 60)

Path("figures").mkdir(exist_ok=True)

# --- Plot 1: Stock Price Time Series ---
prices_plot_data = prices.select("symbol", "date", "adjusted_close").to_pandas()

p1 = (
    ggplot(prices_plot_data, aes(x="date", y="adjusted_close", color="symbol"))
    + geom_line(size=0.5)
    + labs(
        title="Stock Prices (2020-2024)",
        x="", y="Adjusted Close ($)", color="",
    )
    + theme_minimal()
    + theme(figure_size=(10, 6))
)
p1.save("figures/stock_prices.pdf")
p1.show()
print("Saved: figures/stock_prices.pdf")

# --- Plot 2: Return Distribution for One Stock ---
aapl_returns = returns_daily.filter(pl.col("symbol") == "AAPL").to_pandas()
q05 = aapl_returns["ret"].quantile(0.05)

p2 = (
    ggplot(aapl_returns, aes(x="ret"))
    + geom_histogram(bins=80, fill="#2166AC", color="white", alpha=0.8)
    + geom_vline(aes(xintercept=q05), linetype="dashed", color="red")
    + labs(
        title="Distribution of Daily AAPL Returns (2020-2024)",
        subtitle=f"Dashed line = 5th percentile ({q05:.4f})",
        x="Daily Return", y="Count",
    )
    + scale_x_continuous(labels=percent_format())
    + theme_minimal()
    + theme(figure_size=(10, 6))
)
p2.save("figures/return_distribution.pdf")
p2.show()
print("Saved: figures/return_distribution.pdf")

# --- Plot 3: Cumulative Growth of $100 ---
growth = (
    returns_daily
    .sort("symbol", "date")
    .with_columns(
        growth=(pl.col("ret") + 1).cum_prod().over("symbol") * 100
    )
    .select("symbol", "date", "growth")
    .to_pandas()
)

p3 = (
    ggplot(growth, aes(x="date", y="growth", color="symbol"))
    + geom_line(size=0.6)
    + labs(
        title="Growth of $100 Investment (2020-2024)",
        x="", y="Portfolio Value ($)", color="",
    )
    + theme_minimal()
    + theme(figure_size=(10, 6))
)
p3.save("figures/cumulative_growth.pdf")
p3.show()
print("Saved: figures/cumulative_growth.pdf")

# --- Plot 4: Monthly Return Bar Chart (Most Recent Year) ---
last_year = (
    returns_monthly
    .filter(pl.col("symbol") == "AAPL")
    .sort("year_month", descending=True)
    .head(12)
    .with_columns(
        direction=pl.when(pl.col("ret_monthly") >= 0)
                   .then(pl.lit("Positive"))
                   .otherwise(pl.lit("Negative"))
    )
    .to_pandas()
)

p4 = (
    ggplot(last_year, aes(x="year_month", y="ret_monthly", fill="direction"))
    + geom_col()
    + labs(
        title="AAPL Monthly Returns (Last 12 Months)",
        x="", y="Monthly Return", fill="",
    )
    + theme_minimal()
    + theme(
        axis_text_x=element_text(rotation=45, ha="right"),
        figure_size=(10, 6),
    )
)
p4.save("figures/monthly_returns_bar.pdf")
p4.show()
print("Saved: figures/monthly_returns_bar.pdf")

# --- Plot 5: Volatility vs Return Scatter ---
scatter_data = monthly_summary.to_pandas()

p5 = (
    ggplot(scatter_data, aes(x="std_monthly", y="mean_monthly", label="symbol"))
    + geom_point(size=4, color="#2166AC")
    + labs(
        title="Risk vs Return (Monthly, 2020-2024)",
        x="Standard Deviation (Monthly)",
        y="Mean Return (Monthly)",
    )
    + theme_minimal()
    + theme(figure_size=(8, 6))
)
p5.save("figures/risk_return.pdf")
p5.show()
print("Saved: figures/risk_return.pdf")


# ============================================================================
# 9. Value at Risk: The 5th Percentile
# ============================================================================

print("\n" + "=" * 60)
print("9. VALUE AT RISK (5th PERCENTILE)")
print("=" * 60)

var_by_stock = returns_daily.group_by("symbol").agg(
    var_5pct=pl.col("ret").quantile(0.05),
    mean_ret=pl.col("ret").mean(),
    n_obs=pl.len(),
)

print("If you invest $10,000, the worst expected daily loss (95% confidence):")
var_table = var_by_stock.with_columns(
    dollar_var=(pl.col("var_5pct") * 10_000).round(2),
)
print(var_table.sort("symbol"))


print("\n" + "=" * 60)
print("ALL DONE")
print("=" * 60)
print("\nGenerated plots (in figures/):")
print("  - figures/stock_prices.pdf        (price time series)")
print("  - figures/return_distribution.pdf (daily return histogram)")
print("  - figures/cumulative_growth.pdf   (growth of $100)")
print("  - figures/monthly_returns_bar.pdf (monthly return bars)")
print("  - figures/risk_return.pdf         (risk vs return scatter)")
