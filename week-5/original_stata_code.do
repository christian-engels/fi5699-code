*DATA / CODE FOR TABLES & FIGURES IN BENA, ORTIZ-MOLINA, & SIMINTZI "SHIELDING FIRM VALUE: EMPLOYMENT PROTECTION AND PROCESS INNOVATION"
*******************************************************************************************************************************************

*NOTE: 

* This Stata code replicates the tables & figures in the paper using our original files "main_data.dta" & "Fig_3_5_data.dta"

* In the versions of "main_data.dta" & "Fig_3_5_data.dta" provided in this repository we have kept "gvkey" and "fyear" and the innovation variables  
* (e.g., process & non-process innovation) but the values of all variables available from other sources are set to missing.

* The Appendix to our paper contains the definitions and construction details for of all other required variables.


cd "\path\"
set more off

log using results.log, replace

*TABLE 1
*******************************************************************************************************************************************
{
use main_data.dta, clear

quietly: reghdfe cl_pcs gf ic pp, absorb(gvkey fyear) cluster(statecd)

tabstat cl_pcs cl_pdt   pt_pure_pcs_CT3 pt_pure_pdt_CT3   cl_pcs_shr pt_pcs_pure_shr_CT3   gf ic pp    logklr log_capx_lat logppent logemp  logsale_emp roa chglogmvaleq     L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if e(sample), stat(mean sd p10 p50 p90 n) long col(stat)
desc    cl_pcs cl_pdt   pt_pure_pcs_CT3 pt_pure_pdt_CT3   cl_pcs_shr pt_pcs_pure_shr_CT3   gf ic pp    logklr log_capx_lat logppent logemp  logsale_emp roa chglogmvaleq     L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem             
}



*TABLE 2
*******************************************************************************************************************************************
{
*Panel A:
********************************************************************************
use main_data.dta, clear

gen period=""
replace period="1975-80" if fyear>=1975&fyear<=1980
replace period="1981-85" if fyear>=1981&fyear<=1985
replace period="1986-90" if fyear>=1986&fyear<=1990
replace period="1991-97" if fyear>=1991&fyear<=1997

collapse (sum) cl_process_N cl_product_N, by(sich2 period)
sort sich2 period

egen process_i=sum(cl_process_N), by(sich2)
egen process_t=sum(cl_process_N)
gen pcs_shr_75_97=process_i/process_t
drop process_i process_t
gsort -pcs_shr_75_97 period
egen rank=seq(), by(period)

replace rank=11 if rank>=11

collapse (sum) cl_process_N cl_product_N pcs_shr_75_97 (first) sich2 , by(rank period)
order rank sich2 period cl_process_N cl_product_N
replace sich2=. if rank==11
tostring rank, force replace
replace rank="Rest" if rank=="11"

egen process_i=sum(cl_process_N), by(sich2 period)
egen process_t=sum(cl_process_N), by(period)
gen pcs_shr_p=process_i/process_t
drop process_i process_t

br rank sich2 period pcs_shr_75_97 pcs_shr_p // industry share in process innovation



*Panel B:  
************************************************************************************
use main_data.dta, clear

gen period=""
replace period="1975-80" if fyear>=1975&fyear<=1980
replace period="1981-85" if fyear>=1981&fyear<=1985
replace period="1986-90" if fyear>=1986&fyear<=1990
replace period="1991-97" if fyear>=1991&fyear<=1997

collapse (sum) cl_process_N cl_product_N, by(sich2 period)
sort sich2 period

egen process_i=sum(cl_process_N), by(sich2)
egen process_t=sum(cl_process_N)
gen pcs_shr_75_97=process_i/process_t
drop process_i process_t
gsort -pcs_shr_75_97 period
egen rank=seq(), by(period)
drop pcs_shr_75_97
order rank sich2 period cl_process_N cl_product_N

replace rank=11 if rank>=11
collapse (sum) cl_process_N cl_product_N (first) sich2, by(rank period)
order rank sich2 period cl_process_N cl_product_N
replace sich2=. if rank==11
tostring rank, force replace
replace rank="Rest" if rank=="11"

egen process_i=sum(cl_process_N), by(sich2)
egen product_i=sum(cl_product_N), by(sich2)
gen pcs_shr_75_97_p=process_i/(process_i+product_i)
drop process_i product_i

egen process_i=sum(cl_process_N), by(sich2 period)
egen product_i=sum(cl_product_N), by(sich2 period)
gen pcs_shr_p=process_i/(process_i+product_i)
drop process_i product_i

br rank sich2 pcs_shr_75_97 pcs_shr_p // share of process innovation in total innovation
}


  
*TABLE 3: 
*******************************************************************************************************************************************
{
use main_data.dta, clear

*Panel A 
**********************************************************
reghdfe cl_pcs gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pure_pcs_CT3 gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)


*Panel B
********************************************************** 
reghdfe cl_pdt gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pure_pdt_CT3 gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)
}


  
*TABLE 4
*******************************************************************************************************************************************
{
use main_data.dta, clear


*Panel A 
******************************************************************
reghdfe cl_pcs gf GFxCS3 CS3 ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr) cluster(statecd)
reghdfe cl_pcs    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe pt_pure_pcs_CT3 gf GFxCS3 CS3 ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr) cluster(statecd)
reghdfe pt_pure_pcs_CT3    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr sic2_yr) cluster(statecd)


*Panel B 
******************************************************************
reghdfe cl_pdt gf GFxCS3 CS3 ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr) cluster(statecd)
reghdfe cl_pdt    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe pt_pure_pdt_CT3 gf GFxCS3 CS3 ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr) cluster(statecd)
reghdfe pt_pure_pdt_CT3    GFxCS3 CS3       L1log1pspat L1log1psrd L1logsales L1logmtbr                 , absorb(gvkey state_yr sic2_yr) cluster(statecd)
}



*TABLE 5
*******************************************************************************************************************************************
{
use main_data.dta, clear

reghdfe cl_pcs              gf gf_other ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)
reghdfe pt_pure_pcs_CT3     gf gf_other ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)
reghdfe cl_pdt              gf gf_other ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)
reghdfe pt_pure_pdt_CT3     gf gf_other ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)
}



*TABLE 6
*******************************************************************************************************************************************
{
use main_data.dta, clear


*Panel A
*******************************************************************************************
reghdfe cl_pcs gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem logstyrpat ,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe cl_pcs gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if fyear<=1990,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe cl_pcs gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if state!="CA"&state!="MA",absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pure_pcs_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem logstyrpat ,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe pt_pure_pcs_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if fyear<=1990, absorb(gvkey sic2_yr) cluster(statecd)
reghdfe pt_pure_pcs_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if state!="CA"&state!="MA", absorb(gvkey sic2_yr) cluster(statecd)


*Panel B
*******************************************************************************************
reghdfe cl_pdt gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem logstyrpat ,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe cl_pdt gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if fyear<=1990,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe cl_pdt gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if state!="CA"&state!="MA",absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pure_pdt_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem logstyrpat ,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe pt_pure_pdt_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if fyear<=1990,absorb(gvkey sic2_yr) cluster(statecd)
reghdfe pt_pure_pdt_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if state!="CA"&state!="MA",absorb(gvkey sic2_yr) cluster(statecd)
}
 
 
  
*TABLE 7
*******************************************************************************************************************************************
{
use main_data.dta, clear

*Panel A
*******************************************************************************************************************************************
reghdfe cl_pcs gf GFxInvout invout  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs    GFxInvout invout        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
reghdfe cl_pcs gf GFxDispinv dispinv  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs    GFxDispinv dispinv        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe pt_pure_pcs_CT3 gf GFxInvout invout  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3    GFxInvout invout        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
reghdfe pt_pure_pcs_CT3 gf GFxDispinv dispinv  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3    GFxDispinv dispinv        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)

*Panel B
*******************************************************************************************************************************************
reghdfe cl_pdt gf GFxInvout invout  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt    GFxInvout invout        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
reghdfe cl_pdt gf GFxDispinv dispinv  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt    GFxDispinv dispinv        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe pt_pure_pdt_CT3 gf GFxInvout invout  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3    GFxInvout invout        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
reghdfe pt_pure_pdt_CT3 gf GFxDispinv dispinv  ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3    GFxDispinv dispinv        L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
}


  
*TABLE 8 
*******************************************************************************************************************************************
{
use main_data.dta, clear

*Panel A
**********************************************************
reghdfe cl_pcs_pos gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pure_pcs_CT3_pos gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)


*Panel B
************************************************************
reghdfe cl_pdt_pos gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pure_pdt_CT3_pos gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3_pos gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)


*Panel C
********************************************************
reghdfe cl_pcs_shr gf ic pp                                                             if cl_N>=5, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs_shr gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if cl_N>=5, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs_shr gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem if cl_N>=5, absorb(gvkey sic2_yr) cluster(statecd)

reghdfe pt_pcs_pure_shr_CT3 gf ic pp                                                             , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pcs_pure_shr_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pcs_pure_shr_CT3 gf ic pp L1log1pspat L1log1psrd L1logsales L1logmtbr L1pgdp L1pctdem , absorb(gvkey sic2_yr) cluster(statecd)
}

 
 
*TABLE 9
*******************************************************************************************************************************************
{
use main_data.dta, clear

*Panel A
****************************************************************************
reghdfe cl_pcs    gf GFxSRDS0  ic pp                                     , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs    gf GFxSRDS0  ic pp L1logmtbr L1logsales L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pcs       GFxSRDS0        L1logmtbr L1logsales                , absorb(gvkey state_yr) cluster(statecd)
reghdfe cl_pcs       GFxSRDS0        L1logmtbr L1logsales                , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe pt_pure_pcs_CT3    gf GFxSRDS0 ic pp                                     , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3    gf GFxSRDS0 ic pp L1logmtbr L1logsales L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pcs_CT3       GFxSRDS0       L1logmtbr L1logsales                , absorb(gvkey state_yr) cluster(statecd)
reghdfe pt_pure_pcs_CT3       GFxSRDS0       L1logmtbr L1logsales                , absorb(gvkey state_yr sic2_yr) cluster(statecd)



*Panel B
****************************************************************************
reghdfe cl_pdt    gf GFxSRDS0 ic pp                                     , absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt    gf GFxSRDS0 ic pp L1logmtbr L1logsales L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt       GFxSRDS0       L1logmtbr L1logsales                , absorb(gvkey state_yr) cluster(statecd)
reghdfe cl_pdt       GFxSRDS0       L1logmtbr L1logsales                , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe pt_pure_pdt_CT3    gf GFxSRDS0 ic pp                                     , absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3    gf GFxSRDS0 ic pp L1logmtbr L1logsales L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe pt_pure_pdt_CT3        GFxSRDS0      L1logmtbr L1logsales                , absorb(gvkey state_yr) cluster(statecd)
reghdfe pt_pure_pdt_CT3       GFxSRDS0       L1logmtbr L1logsales                , absorb(gvkey state_yr sic2_yr) cluster(statecd)
}



*TABLE 10
*******************************************************************************************************************************************
{
use main_data.dta, clear

*Panel A
*******************************************************************************************************************************
reghdfe logklr            gf GFxSRDS0 ic pp                                                       , absorb(gvkey fyear) cluster(statecd)
reghdfe logklr            gf GFxSRDS0 ic pp L1logsales L1logmtbr L1sales_gr L1blev L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe logklr               GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr) cluster(statecd)
reghdfe logklr               GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe log_capx_lat      gf GFxSRDS0 ic pp                                                       , absorb(gvkey fyear) cluster(statecd)
reghdfe log_capx_lat      gf GFxSRDS0 ic pp L1logsales L1logmtbr L1sales_gr L1blev L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe log_capx_lat         GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr) cluster(statecd)
reghdfe log_capx_lat         GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr sic2_yr) cluster(statecd)

*Panel B
*******************************************************************************************************************************
reghdfe logppent          gf GFxSRDS0 ic pp                                                       , absorb(gvkey fyear) cluster(statecd)
reghdfe logppent          gf GFxSRDS0 ic pp L1logsales L1logmtbr L1sales_gr L1blev L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe logppent             GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr) cluster(statecd)
reghdfe logppent             GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe logemp            gf GFxSRDS0 ic pp                                                       , absorb(gvkey fyear) cluster(statecd)
reghdfe logemp            gf GFxSRDS0 ic pp L1logsales L1logmtbr L1sales_gr L1blev L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe logemp               GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr) cluster(statecd)
reghdfe logemp               GFxSRDS0       L1logsales L1logmtbr L1sales_gr L1blev                , absorb(gvkey state_yr sic2_yr) cluster(statecd)
}



*TABLE 11
*******************************************************************************************************************************************
{
use main_data.dta, clear

reghdfe chglogmvaleq      gf_ado_m3-gf_ado_5p GF_m3xSRDS0-GF_5pxSRDS0 ic pp                                                    , absorb(gvkey fyear) cluster(statecd)
reghdfe chglogmvaleq      gf_ado_m3-gf_ado_5p GF_m3xSRDS0-GF_5pxSRDS0 ic pp L1logsales L1sales_gr L1blev L1fata L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe chglogmvaleq                          GF_m3xSRDS0-GF_5pxSRDS0       L1logsales L1sales_gr L1blev L1fata                , absorb(gvkey state_yr) cluster(statecd)
reghdfe chglogmvaleq                          GF_m3xSRDS0-GF_5pxSRDS0       L1logsales L1sales_gr L1blev L1fata                , absorb(gvkey state_yr sic2_yr) cluster(statecd)
}



*TABLE 12
*******************************************************************************************************************************************
{
use main_data.dta, clear

reghdfe logsale_emp      gf GFxSRDS0 ic pp                                                    , absorb(gvkey fyear) cluster(statecd)
reghdfe logsale_emp      gf GFxSRDS0 ic pp L1logsales L1sales_gr L1blev L1fata L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe logsale_emp         GFxSRDS0       L1logsales L1sales_gr L1blev L1fata                , absorb(gvkey state_yr) cluster(statecd)
reghdfe logsale_emp         GFxSRDS0       L1logsales L1sales_gr L1blev L1fata                , absorb(gvkey state_yr sic2_yr) cluster(statecd)

reghdfe roa      gf GFxSRDS0 ic pp                                                    , absorb(gvkey fyear) cluster(statecd)
reghdfe roa      gf GFxSRDS0 ic pp L1logsales L1sales_gr L1blev L1fata L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe roa         GFxSRDS0       L1logsales L1sales_gr L1blev L1fata                , absorb(gvkey state_yr) cluster(statecd)
reghdfe roa         GFxSRDS0       L1logsales L1sales_gr L1blev L1fata                , absorb(gvkey state_yr sic2_yr) cluster(statecd)
}



*FIGURE 1
*******************************************************************************************************************************************
{
use main_data.dta, clear

table fyear, contents(mean cl_N mean cl_pcs_shr)
}



*FIGURE 2
*******************************************************************************************************************************************
{
use main_data.dta, clear

reghdfe cl_pcs gf_ado_m3 gf_ado_m2 gf_ado_m1 gf_ado_0 gf_ado_p1 gf_ado_p2 gf_ado_p3 gf_ado_p4 gf_ado_5p ic pp  L1log1pspat L1log1psrd L1logsales             L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
reghdfe cl_pdt gf_ado_m3 gf_ado_m2 gf_ado_m1 gf_ado_0 gf_ado_p1 gf_ado_p2 gf_ado_p3 gf_ado_p4 gf_ado_5p ic pp  L1log1pspat L1log1psrd L1logsales             L1logmtbr L1pgdp L1pctdem, absorb(gvkey fyear) cluster(statecd)
}



*FIGURE 3
*******************************************************************************************************************************************
{
use Fig_3_5_data.dta, clear

gen treated=0 // treated states
replace treated=1 if state=="AZ" | state=="CA" | state=="CT" | state=="DE" | state=="ID" | state=="MA" | state=="MT" | state=="NV" | state=="OK" | state=="WY"


tabstat cl_pcs_e1 if treated==1, by(eyear) statistics(mean)
tabstat cl_pcs_e1 if treated==0, by(eyear) statistics(mean)
}



*FIGURE 4
*******************************************************************************************************************************************
{
use main_data.dta, clear

reghdfe cl_pcs GF_m3xCS3 GF_m2xCS3 GF_m1xCS3 GF_0xCS3 GF_p1xCS3 GF_p2xCS3 GF_p3xCS3 GF_p4xCS3 GF_5pxCS3 CS3 L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
reghdfe cl_pdt GF_m3xCS3 GF_m2xCS3 GF_m1xCS3 GF_0xCS3 GF_p1xCS3 GF_p2xCS3 GF_p3xCS3 GF_p4xCS3 GF_5pxCS3 CS3 L1log1pspat L1log1psrd L1logsales L1logmtbr, absorb(gvkey state_yr sic2_yr) cluster(statecd)
}



*FIGURE 5
*******************************************************************************************************************************************
{
use Fig_3_5_data.dta, clear

gen treated=0 // treated states
replace treated=1 if state=="AZ" | state=="CA" | state=="CT" | state=="DE" | state=="ID" | state=="MA" | state=="MT" | state=="NV" | state=="OK" | state=="WY"

drop if icostshr==.
egen medCS3=median(icostshr)

tabstat cl_pcs_e1 if treated==1&icostshr>=medCS3, by(eyear) statistics(mean)
tabstat cl_pcs_e1 if treated==0&icostshr>=medCS3, by(eyear) statistics(mean)
}


log close
