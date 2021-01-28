

// origin - destination distance cutoffs

	global path   	   				"W:\EoCC\analysis"	
	global data_temp				"$path/data/temp"
	global regional_intermediate 	"$path/data/intermediate/regional_database"
	global tables 					"$path\output\tables"
	global data_final				"$path/data/final"
	global tables_temp				"$path/output/temp"

	
	
********************************************************************************



* initiate new tables
	eststo clear
	qui use "$data_temp/greta_cons_strike_participation_election_prepared", clear
	qui eststo a1: reghdfe fd_the_greens	cum_res_ols [pw=pop_t], absorb(i.bula_num i.election_num)
	qui esttab a* using "$tables_temp/distance_cutoffs.csv", replace wide ///
		se nostar keep(cum_res_*) ///
		nomtitles nonumbers  nonote nogaps noline nopar noobs ///
		sfmt( %12.0fc)	b(%12.4f) se(%12.4f) 
		
		


forval distance = 1/800 {
	disp `distance'


	qui use "$data_temp/greta_cons_strikes_with_resids_ALL_STRIKES.dta", clear // greta_cons_strikes_with_resids_ALL_STRIKES.dta
	
	qui rename ags5 endags5
	
	*drop specifications that are not needed
	qui drop res_p_int_large res_p_int_small res_p_int_*
	
	
	* rename
	qui rename res_p_interaction_small   res_p_int_small
	qui rename res_p_interaction_large   res_p_int_large
	qui rename res_p_desired 			 res_p_int_only
	qui rename res_ols_interaction_small res_ols_int_small
	qui rename res_ols_interaction_large res_ols_int_large
	qui rename res_ols_desired 			 res_ols_int_only
	
	
	
	* merge distances 
	qui merge m:1 startid endid using "$data_temp/greta_cons_table_distance_start_end.dta", keep(match)
	qui drop _merge
	
	
	* keep if region is in certain distance
	qui keep if tripdistancekm <= `distance'
	
	* keep only positive residuals
	foreach var of varlist res* {
		qui replace `var' = 0 if `var' < 0
	}
	
	
	* add startags to be able to collapse over it in the next step
	qui rename startid teralytics_id
	qui merge m:1 teralytics_id using "$data_temp/greta_cons_conversion_table_teralytics_ags5.dta"
	qui drop _merge
	qui rename teralytics_id startid
	qui rename ags5 startags5
	qui order date startid startags5 endags5 endid municipality source
	
	* aggregation if there is more than one destination with a strike
	qui collapse (sum) count res*, by(startags5 date)
	
	
	* cummulative number of strike participants
	foreach var of varlist res* {
		qui bys startags5: gen cum_`var' = sum(`var')
	}
	
	qui rename startags5 ags5
	qui save "$data_temp/greta_cons_origin_residuals_ags5.dta", replace
	
	
**************************************
	* allocate to municipaliyt level

	// expand to ags8 dimension
	qui use "$data_temp/greta_cons_conversion_ags8_ags5_2019.dta", clear
	qui joinby ags5 using "$data_temp/greta_cons_origin_residuals_ags5.dta"
	qui order date
	qui sort ags8 date
	
	
	
	* allocate residuals from districts to municipalities & make per population

	qui merge m:1 ags8 using  "$regional_intermediate/regional_variables_ags8", keepusing(share_munic_pop_10_34 pop_t ags8)
	qui keep if _merge == 3
	qui drop _merge
	*order date ags8 ags5 ags8_name pop_10_34
	
	foreach var of varlist  res_* cum_*   {
		* allocate residuals according to weights
		qui replace `var' = `var' * share_munic_pop_10_34
		
		*per population 
		qui replace `var' = (`var'/pop_t) *100
		
		*qui summ `var'
		*qui replace `var' = (`var' - `r(mean)')/`r(sd)'
		
	}
	
	
	
	qui save "$data_temp/greta_cons_strikes_participation_ags8.dta", replace

	
	
*********************************************************************	
	
	// merge with election outcomes and regional controls
	
	
	
	* eu ***********************************************************************
	qui use "$data_temp/greta_cons_strikes_participation_ags8.dta", clear
	qui sort ags8 date
	qui keep if date < td(26may2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags8[_n] != ags8[_n+1]
	qui keep if temp == 1
	qui drop temp
	qui qui gen election = "eu"
	qui merge 1:1 ags8 election using  "$regional_intermediate/regional_variables_ags8"
	qui keep if _merge == 3 
	qui save "$data_temp/greta_cons_strikes_participation_election_controls", replace
	
	
	* brandenburg **************************************************************
	qui use "$data_temp/greta_cons_strikes_participation_ags8.dta", clear
	qui sort ags8 date
	qui keep if date < td(01sep2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags8[_n] != ags8[_n+1]
	qui keep if temp == 1
	qui drop temp
	qui gen election = "brandenburg"
	qui merge 1:1 ags8 election using  "$regional_intermediate/regional_variables_ags8_brandenburg"
	qui keep if _merge == 3 
	qui append using "$data_temp/greta_cons_strikes_participation_election_controls"
	qui save "$data_temp/greta_cons_strikes_participation_election_controls", replace
	
	
	
	* saxony **************************************************************
	qui use "$data_temp/greta_cons_strikes_participation_ags8.dta", clear
	qui sort ags8 date
	qui keep if date < td(01sep2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags8[_n] != ags8[_n+1]
	qui keep if temp == 1
	qui drop temp
	qui gen election = "saxony"
	qui merge 1:1 ags8 election using  "$regional_intermediate/regional_variables_ags8_saxony"
	qui keep if _merge == 3 
	qui append using "$data_temp/greta_cons_strikes_participation_election_controls"
	qui save "$data_temp/greta_cons_strikes_participation_election_controls", replace
	
	
	
	* thuringia **************************************************************
	qui use "$data_temp/greta_cons_strikes_participation_ags8.dta", clear
	qui sort ags8 date
	qui keep if date < td(27oct2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags8[_n] != ags8[_n+1]
	qui keep if temp == 1
	qui drop temp
	qui gen election = "thuringia"
	qui merge 1:1 ags8 election using  "$regional_intermediate/regional_variables_ags8_thuringia"
	qui keep if _merge == 3 
	qui append using "$data_temp/greta_cons_strikes_participation_election_controls"
	qui save "$data_temp/greta_cons_strikes_participation_election_controls", replace
	drop _merge
	
	
	
	///////////////////////
	* merge degree urbanization
	qui merge m:1 ags8 using "$data_temp/greta_cons_degree_urbanization_ags8"
	qui keep if _merge == 3
	qui drop _merge
	
	
	///////////////////////
	* merge with kreis controls
	
	
	qui merge m:1 ags5 using "$data_final/regional_database/greta_cons_regional_database_ags5_prepared.dta"
	qui keep if _merge == 3
	qui drop _merge
	
	
	* gnerate varibales
	qui gen log_pop = log(pop_t)
	
	
	* standardize  variables
	foreach var of varlist res_* cum_* the_greens fd_the_greens  {
		qui summ `var' [fw=pop_t]
		qui replace `var' = (`var' - `r(mean)')/`r(sd)'
	}
	
	
		
	* gen variables
	qui encode ags5, gen(ags5_num)
	qui encode election, gen(election_num)
	qui gen bula = substr(ags5,1,2)
	qui encode bula, gen(bula_num)
	
	* dummy urban rural - pop_density median split 
	qui summ pop_density, d
	qui gen d_urban = cond(pop_density > `r(p50)', 1, 0)
	
	
	
	
	foreach var of varlist pop_t log_pop pop_density ue_rate log_IncomeperTP IncomeperCapita log_IncomeperCapita share_* residential commercial green agriculture forest per_young support_ratio  {
		qui summ `var'  [fw=pop_t]
		qui gen `var'_st = (`var' - `r(mean)')/`r(sd)'
	}
	
	

	
********************************************************************
// analysis

	
	
	eststo clear 
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" "p" "p_int_small" "p_int_large" "p_int_only" {		
		qui eststo a2: reghdfe fd_the_greens	cum_res_`row' [pw=pop_t], absorb(i.bula_num i.election_num)
		
		qui esttab a* using "$tables_temp/distance_cutoffs.csv", append wide ///
		se nostar keep(cum_res_*) ///
		nomtitles nonumbers  nonote nogaps noline nopar ///
		sfmt( %12.0fc)	b(%12.5f) se(%12.5f) ///
		coeflabels(cum_res_`row' "`row'")
	}
	
	* save number of observations
	
	
	
	} // end: loop over distance
	
	
	
	
	