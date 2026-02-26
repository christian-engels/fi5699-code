# =============================================================================
# Fixed Effects Regressions in Corporate Finance
# =============================================================================
#
# This script demonstrates fixed effects panel regressions using data from:
#
#   Bena, Ortiz-Molina & Simintzi (2022)
#   "Shielding Firm Value: Employment Protection and Process Innovation"
#   Journal of Financial Economics, 146(2), 637-664.
#   https://doi.org/10.1016/j.jfineco.2021.10.005
#
# Data source (CC BY 4.0):
#   https://data.mendeley.com/datasets/jpg9bjzjwk/1
#
# Original analysis was conducted in Stata using reghdfe.
# Here we replicate the methodology in Python using pyfixest.
#
# =============================================================================

import pandas as pd
import pyfixest as pf

# ── 1. Load the panel data ───────────────────────────────────────────────────

df = pd.read_csv("data/bena_ortiz_molina_simintzi_2022.csv")

print("=" * 70)
print("PANEL DATA OVERVIEW")
print("=" * 70)
print(f"Observations : {len(df):,}")
print(f"Firms        : {df['gvkey'].nunique():,}")
print(f"Years        : {df['fyear'].min()} – {df['fyear'].max()}")
print(f"Columns      : {df.shape[1]}")
print()

# ── 2. Understand the variables ──────────────────────────────────────────────
#
# Key variables in the dataset:
#
#   gvkey          – Firm identifier (Compustat global company key)
#   fyear          – Fiscal year
#   cl_pcs         – Process innovation (log of 1 + process claims)
#   cl_pdt         – Product innovation (log of 1 + product claims)
#   pt_pure_pcs_CT3 – Pure process patents (citation-weighted)
#   pt_pure_pdt_CT3 – Pure product patents (citation-weighted)
#   L1log1pspat    – Lagged log(1 + patent stock): a firm's cumulative
#                    innovation capacity
#   logstyrpat     – Log state-year patent count: captures the regional
#                    innovation environment over time
#   cl_N           – Total patent claims (process + product)
#   invout         – Indicator: firm has investment outside its home state
#   dispinv        – Indicator: firm has dispersed investment
#
# The original paper studies how changes in employment protection laws
# (the "good faith" exception to at-will employment) affect firms'
# decisions to invest in process innovation versus product innovation.
# The full regression includes treatment variables and Compustat controls
# that are not available in this public extract.
#
# For the purpose of learning fixed effects methodology, we use the
# available innovation and patent variables.
# ─────────────────────────────────────────────────────────────────────────────

print("SUMMARY STATISTICS")
print("=" * 70)
summary_vars = ["cl_pcs", "cl_pdt", "L1log1pspat", "logstyrpat", "cl_N"]
print(df[summary_vars].describe().round(3).to_string())
print()


# ── 3. Pooled OLS (no fixed effects) ────────────────────────────────────────
#
# We start with a simple pooled OLS regression:
#   Process Innovation = β₀ + β₁·L1log1pspat + β₂·logstyrpat + ε
#
# This IGNORES firm-specific and time-specific unobserved heterogeneity.

print("=" * 70)
print("MODEL 1: POOLED OLS (No Fixed Effects)")
print("=" * 70)

m1 = pf.feols("cl_pcs ~ L1log1pspat + logstyrpat", data=df)
print(m1.summary())


# ── 4. Firm fixed effects ───────────────────────────────────────────────────
#
# Adding firm fixed effects controls for ALL time-invariant firm
# characteristics (e.g., industry, founding date, location, management
# quality, corporate culture). This is equivalent to including a dummy
# variable for each firm.
#
# With firm FE, β₁ is identified only from WITHIN-FIRM variation over
# time: how does a change in a firm's patent stock relate to a change
# in its process innovation?

print("=" * 70)
print("MODEL 2: FIRM FIXED EFFECTS")
print("=" * 70)

m2 = pf.feols("cl_pcs ~ L1log1pspat + logstyrpat | gvkey", data=df)
print(m2.summary())


# ── 5. Year fixed effects ───────────────────────────────────────────────────
#
# Adding year fixed effects controls for economy-wide shocks that affect
# all firms in a given year (e.g., recessions, changes in patent law,
# technological breakthroughs).

print("=" * 70)
print("MODEL 3: YEAR FIXED EFFECTS")
print("=" * 70)

m3 = pf.feols("cl_pcs ~ L1log1pspat + logstyrpat | fyear", data=df)
print(m3.summary())


# ── 6. Two-way fixed effects (firm + year) ──────────────────────────────────
#
# The standard specification in corporate finance panel regressions:
# firm FE + year FE.
#
# This absorbs both time-invariant firm heterogeneity AND common
# time shocks, isolating the within-firm, within-year variation.
#
# In the original paper, the Stata command is:
#   reghdfe cl_pcs [...], absorb(gvkey fyear) cluster(statecd)
#
# Note: logstyrpat varies at the state-year level, so it will be
# partially absorbed by year FE (but not fully, since it also varies
# across states).

print("=" * 70)
print("MODEL 4: TWO-WAY FIXED EFFECTS (Firm + Year)")
print("=" * 70)

m4 = pf.feols("cl_pcs ~ L1log1pspat + logstyrpat | gvkey + fyear", data=df)
print(m4.summary())


# ── 7. Clustered standard errors ────────────────────────────────────────────
#
# In corporate finance, residuals are often correlated within firms
# over time (firm-level persistence) and across firms within the same
# year (common shocks). Petersen (2009, RFS) shows that OLS standard
# errors are biased when this dependence is ignored.
#
# The standard practice is to cluster standard errors by firm to account
# for within-firm serial correlation. Two-way clustering (by firm and
# year) is sometimes used to also account for cross-sectional dependence.
#
# Reference: Petersen, M.A. (2009). "Estimating Standard Errors in
# Finance Panel Data Sets: Comparing Approaches." Review of Financial
# Studies, 22(1), 435-480.

print("=" * 70)
print("MODEL 5: Two-Way FE with CLUSTERED Standard Errors (by firm)")
print("=" * 70)

m5 = pf.feols(
    "cl_pcs ~ L1log1pspat + logstyrpat | gvkey + fyear",
    data=df,
    vcov={"CRV1": "gvkey"},
)
print(m5.summary())


# ── 8. Comparison table ─────────────────────────────────────────────────────
#
# A regression table comparing all specifications side by side.
# This is the standard way to present results in a corporate finance paper.

print("=" * 70)
print("COMPARISON TABLE: Process Innovation (cl_pcs)")
print("=" * 70)

table = pf.etable(
    [m1, m2, m3, m4, m5],
    labels={
        "cl_pcs": "Process Innovation",
        "L1log1pspat": "Lagged Patent Stock",
        "logstyrpat": "State-Year Patents",
    },
)
print(table)


# ── 9. Product innovation as dependent variable ─────────────────────────────
#
# The paper also examines product (non-process) innovation. We re-run
# the two-way FE specification for product innovation.

print("=" * 70)
print("MODEL 6: Product Innovation with Two-Way FE + Clustered SE")
print("=" * 70)

m6 = pf.feols(
    "cl_pdt ~ L1log1pspat + logstyrpat | gvkey + fyear",
    data=df,
    vcov={"CRV1": "gvkey"},
)
print(m6.summary())


# ── 10. Multiple outcomes in one table ───────────────────────────────────────
#
# Compare the effect on process vs product innovation side by side.

print("=" * 70)
print("COMPARISON: Process vs Product Innovation (Two-Way FE)")
print("=" * 70)

table2 = pf.etable(
    [m5, m6],
    labels={
        "cl_pcs": "Process Innovation",
        "cl_pdt": "Product Innovation",
        "L1log1pspat": "Lagged Patent Stock",
        "logstyrpat": "State-Year Patents",
    },
)
print(table2)


# ── 11. Key takeaways for your dissertation ─────────────────────────────────
#
# 1. ALWAYS include fixed effects in panel regressions. Pooled OLS
#    produces biased estimates when unobserved heterogeneity is
#    correlated with the regressors (omitted variable bias).
#
# 2. Firm FE absorb time-invariant firm characteristics. This is
#    critical when studying outcomes that differ systematically
#    across firms (e.g., large vs small, R&D-intensive vs not).
#
# 3. Year FE absorb common time shocks. This matters when aggregate
#    trends (e.g., the business cycle, regulatory changes) affect
#    all firms simultaneously.
#
# 4. Two-way FE (firm + year) is the standard in corporate finance.
#    The Stata equivalent is: reghdfe y x, absorb(firm year)
#    The Python equivalent is: pf.feols("y ~ x | firm + year", ...)
#
# 5. ALWAYS cluster standard errors. At minimum, cluster by firm
#    (to account for within-firm serial correlation). The paper
#    clusters by state since the treatment (legal change) varies
#    at the state level.
#
# 6. When writing your dissertation, present multiple specifications
#    (OLS, firm FE, two-way FE) to show robustness. Readers expect
#    to see how coefficients change across specifications.
#
# Further reading:
#   - Petersen (2009, RFS): Standard errors in panel data
#   - Angrist & Pischke (2009): Mostly Harmless Econometrics, Ch. 5
#   - Wooldridge (2010): Econometric Analysis of Cross Section and
#     Panel Data, Ch. 10
#   - Breuer et al. (2024, JAR): "Using and Interpreting Fixed Effects
#     Models"
# =============================================================================
