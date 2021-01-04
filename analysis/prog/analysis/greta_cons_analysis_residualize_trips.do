// ***************************** PREAMBLE***************************************
*	Created: 14.12.2020
*	Author: Marc Fabel
*	
*	Description:
*		First set of regressions - using residualized movements
*
*	Input:
*		greta_cons_teralytics_prepared.dta				[final]
*
*	Output:
*		
*
	
	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   			"W:\EoCC\analysis"	
	global data_final			"$path/data/final"
	global data_temp			"$path/data/temp"

	global program_start_time "$S_DATE $S_TIME"

	

	// Define covariates
	global region_fe 			"i.start_end_id_num"
	global time_fe 				"i.dow i.woy i.month" //   i.woy
	global weather				"sun_start rain_start maxtemp_start sun_end rain_end maxtemp_end"
	global holiday 				"i.sch_hday_start i.pub_hday_start i.fasching_start i.sch_hday_end i.pub_hday_end i.fasching_end"
	global interaction 			"i.start_end_id_num##i.dow i.start_end_id_num##i.woy i.start_end_id_num##i.month"
	global interaction_small	"i.start_end_id_num##i.woy i.start_end_id_num##i.month"





********************************************************************************
*	OLS
********************************************************************************

	use "$data_final/greta_cons_teralytics_prepared.dta", clear

	qui egen count = rowtotal(count*)

	foreach var of varlist count {	
		reghdfe `var' $weather , absorb($region_fe $time_fe $holiday ) res(res_ols)
		reghdfe `var' $weather , absorb($region_fe $time_fe $holiday $interaction_small) res(res_ols_interaction_small)
		reghdfe `var' $weather , absorb($region_fe $time_fe $holiday $interaction) res(res_ols_interaction_large)
	}
	
	* export
	qui keep date startid endid	count res_ols*
	qui save "$data_temp/greta_cons_trips_resid_ols.dta", replace
	
	// stop running time *******************************************************
	global program_end_time "$S_DATE $S_TIME"
	global temp_start =  clock("$program_start_time", "DMYhms")
	global temp_end   =   clock("$program_end_time", "DMYhms")
	global temp_diff = hours($temp_end - $temp_start)
	disp "Runtime: $temp_diff hours"
	
	
	* Runtime: 17 hours
	
	
	
********************************************************************************
*	Poisson
********************************************************************************	
	
	
	
	global program_start_time "$S_DATE $S_TIME"
	
	use "$data_final/greta_cons_teralytics_prepared.dta", clear

	qui egen count = rowtotal(count*)

	foreach var of varlist count {	
		/*ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday) d
		predict fit_poisson
		qui gen res_p = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
		
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday $interaction_small) d
		predict fit_poisson
		qui gen res_p_interaction_small = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson*/
		
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday $interaction) d
		predict fit_poisson
		qui gen res_p_interaction_large = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	* export
	qui keep date startid endid	count res_p*
	qui save "$data_temp/greta_cons_trips_resid_poisson_3.dta", replace
	
	// stop running time *******************************************************
	global program_end_time "$S_DATE $S_TIME"
	global temp_start =  clock("$program_start_time", "DMYhms")
	global temp_end   =   clock("$program_end_time", "DMYhms")
	global temp_diff = hours($temp_end - $temp_start)
	disp "Runtime: $temp_diff hours"
	
	
	
	
		
		
	* Alle drei residualsätze kombinieren
	qui use "$data_temp/greta_cons_trips_resid_poisson_3.dta", clear
	drop count 
	qui merge 1:1 date startid endid using "$data_temp/greta_cons_trips_resid_poisson_12.dta"
	
	qui keep date startid endid	count res_p*
	qui save "$data_temp/greta_cons_trips_resid_poisson.dta", replace
	
	* Missings? unklar
	
	
	


	
	////////////////////////////////
	// Logarithm
	
	
	use "$data_final/greta_cons_teralytics_prepared.dta", clear

	qui egen count = rowtotal(count*)
	qui gen ln_count = ln(count)

	foreach var of varlist ln_count {	
		reghdfe `var' $weather , absorb($region_fe $time_fe $holiday ) res(res_ols_ln)
		reghdfe `var' $weather , absorb($region_fe $time_fe $holiday $interaction_small) res(res_ols_ln_interaction_small)
		reghdfe `var' $weather , absorb($region_fe $time_fe $holiday $interaction) res(res_ols_ln_interaction_large)
	}
	
	* export
	qui keep date startid endid	ln_count res_ols*
	qui save "$data_temp/greta_cons_trips_resid_ols_ln.dta", replace
	
	// stop running time *******************************************************
	global program_end_time "$S_DATE $S_TIME"
	global temp_start =  clock("$program_start_time", "DMYhms")
	global temp_end   =   clock("$program_end_time", "DMYhms")
	global temp_diff = hours($temp_end - $temp_start)
	disp "Runtime: $temp_diff hours"
	
	
	* Runtime: 17 hours
	
	
	
********************************************************************************
*	Poisson
********************************************************************************	
	
	
	
	global program_start_time "$S_DATE $S_TIME"
	
	use "$data_final/greta_cons_teralytics_prepared.dta", clear

	qui egen count = rowtotal(count*)
	qui gen ln_count = ln(count)

	foreach var of varlist ln_count {	
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday) d
		predict fit_poisson
		qui gen res_p_ln = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
		
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday $interaction_small) d
		predict fit_poisson
		qui gen res_p_ln_interaction_small = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
		
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday $interaction) d
		predict fit_poisson
		qui gen res_p_ln_interaction_large = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	* export
	qui keep date startid endid	ln_count res_p*
	qui save "$data_temp/greta_cons_trips_resid_poisson_ln.dta", replace
	
	// stop running time *******************************************************
	global program_end_time "$S_DATE $S_TIME"
	global temp_start =  clock("$program_start_time", "DMYhms")
	global temp_end   =   clock("$program_end_time", "DMYhms")
	global temp_diff = hours($temp_end - $temp_start)
	disp "Runtime: $temp_diff hours"	
	
	
	
	
	
	