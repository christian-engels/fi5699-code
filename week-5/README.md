# Week 5: Fixed Effects Regressions in Corporate Finance

## Research Paper

**Bena, J., Ortiz-Molina, H. & Simintzi, E. (2022). "Shielding Firm Value: Employment Protection and Process Innovation." *Journal of Financial Economics*, 146(2), 637-664.**

- DOI: https://doi.org/10.1016/j.jfineco.2021.10.005
- Data and code: https://data.mendeley.com/datasets/jpg9bjzjwk/1
- Licence: CC BY 4.0

### What the paper studies

Following state-level legal changes that increase labour dismissal costs (the "good faith" exception to employment at will), firms increase their innovation in new processes that facilitate the adoption of cost-saving production methods. The effect is concentrated among firms in industries with high labour cost shares and high innovation ability. The paper uses a difference-in-differences design with firm and year fixed effects, clustering standard errors at the state level.

### Methodology (relevant to the lecture)

The Stata command used throughout the paper is:

```stata
reghdfe cl_pcs gf ic pp [controls], absorb(gvkey fyear) cluster(statecd)
```

This is a **two-way fixed effects regression** with:
- `absorb(gvkey fyear)` = firm FE + year FE
- `cluster(statecd)` = standard errors clustered by state

The Python equivalent using `pyfixest`:

```python
pf.feols("cl_pcs ~ gf + ic + pp | gvkey + fyear", data=df, vcov={"CRV1": "statecd"})
```

## Data

The public replication extract (in `data/`) contains the authors' novel measures of process and product innovation but sets Compustat variables to missing (these require a WRDS subscription). The available variables are sufficient to demonstrate fixed effects methodology.

| Variable | Description |
|----------|-------------|
| `gvkey` | Firm identifier (Compustat) |
| `fyear` | Fiscal year |
| `cl_pcs` | Process innovation: log(1 + process claims) |
| `cl_pdt` | Product innovation: log(1 + product claims) |
| `pt_pure_pcs_CT3` | Pure process patents (citation-weighted) |
| `pt_pure_pdt_CT3` | Pure product patents (citation-weighted) |
| `L1log1pspat` | Lagged log(1 + patent stock) |
| `logstyrpat` | Log state-year patent count |
| `cl_N` | Total patent claims |
| `invout` | Indicator: firm has out-of-state investment |
| `dispinv` | Indicator: firm has dispersed investment |

Panel: **45,263 firm-year observations**, **4,447 firms**, **1975-1997**.

## Files

```
01_fixed_effects_regressions.py   Python script demonstrating FE regressions
original_stata_code.do            Original Stata code from the paper
data/
  bena_ortiz_molina_simintzi_2022.csv   Panel data (CSV, available variables)
  main_data.dta                         Original Stata data file
  fig_data.dta                          Data for figures 3 and 5
```

## Requirements

```
pip install pandas pyfixest pyreadstat
```

## Key references on methodology

- Petersen, M.A. (2009). "Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches." *Review of Financial Studies*, 22(1), 435-480.
- Breuer, M. et al. (2024). "Using and Interpreting Fixed Effects Models." *Journal of Accounting Research*, 62(4).
- Angrist, J.D. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*, Chapter 5.
