// ***************************** PREAMBLE***************************************
*	Created: 06.01.2021
*	Author: Marc Fabel
*	
*	Description:
*		prepares data for electoral outcomes
*			1) combine residualized journeys
*			2) export residuals
*			3) generate participation index
*			4) combine with election data/final
*			5) combine with regional database
*
*	Input:
*		greta_cons_fff_all_strikes_ags5_wkr_teralyticsid.csv		[final]		prepared strike database
*
*		greta_cons_trips_resid_poisson.dta							[temp]		residual specification
*		greta_cons_trips_resid_ols.dta								[temp]		residual specification		
*		greta_cons_trips_resids_desired_model.dta 					[temp]		residual specification
*		greta_cons_trips_resid_close_regions.dta 					[temp]		residual specification
*
*		greta_cons_table_distance_start_end.dta						[temp]		travel distances
*		greta_cons_conversion_table_teralytics_ags5.dta				[temp]		conversion table
*
*		greta_cons_population_ags5_prepared.dta						[final]		population data prepared
*
*		greta_cons_elections_ags5_prepared.dta						[final]		election data
*
*
*
*
*	Output:
*		greta_cons_resid_all_models.csv								[temp]		export for other programs
*		greta_cons_strikes_participation_election_outcomes.dta		[temp]		prepared data for analysis of electoral outcomes



	
	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   			"W:\EoCC\analysis"	
	global data_final			"$path/data/final"
	global data_temp			"$path/data/temp"

	
	
	
********************************************************************************
*	´1) open strike data and combine with residuals
********************************************************************************	



	import delimited "$data_final\fff_strikes\greta_cons_fff_all_strikes_ags5_wkr_teralyticsid.csv", delimiter(";") encoding(UTF-8) stringcols(1 2 3 5 14 16) clear 

	qui gen date_s = day +"/"+ month +"/"+ year
	qui gen date = date(date_s, "DMY")
	order date teralytics_id
	format date %td
	drop day month year date_s
	rename teralytics_id endid
	
	
	* keep only ordnungsamt & cities
	*keep if source == "ordnungsamt"
	drop if source == "fff_webiste"
	
	
	* keep only 1 strike per day and teralytics_id
	 duplicates drop date endid municipality, force
	 
	 drop if municipality == "luenen" // 6 obs, duplicates with dortmund-id
	 duplicates tag date endid , generate(temp)
	 order temp
	 
	 duplicates drop date endid, force
	 * check that there are no duplicates with large cities that I condition on later
	 
	 drop temp plz state location geometry wkr_nr
	 order date ags5
	 
	 
	
	* combine with poisson residuals
	merge 1:m date endid using "$data_temp/greta_cons_trips_resid_poisson.dta",  keep(match)
	qui drop _merge
	merge 1:1 date endid startid count using "$data_temp/greta_cons_trips_resid_ols.dta",  keep(match)
	qui drop _merge

	*merge 1:1 date endid startid using "$data_temp/greta_cons_trips_resid_poisson_ln.dta",  keep(match)
	*qui drop _merge
	
	*merge 1:1 date endid startid using "$data_temp/greta_cons_trips_resid_ols_ln.dta",  keep(match)
	*qui drop _merge
	
	merge 1:1 date endid startid count  using "$data_temp/greta_cons_trips_resids_desired_model.dta",  keep(match)
	qui drop _merge
	
	merge 1:1 date endid startid count using "$data_temp/greta_cons_trips_resid_close_regions.dta" // cannot be condition on match only
	drop if _merge ==2
	qui drop _merge
	
	
	
	
	
	
	// save all combined residuals for strikes
	drop res_ols_desired_nocons // no new insight
	drop res_p_int_only // is the same as res_p_desired (and the other has the advantage of having all areas)
	
	
	// shorten variable name
	
	
	
	qui save "$data_temp/greta_cons_strikes_with_resids.dta", replace
	
	
	
	
	
********************************************************************************
*	2) export Residuals
********************************************************************************	
	
	
	
	use "$data_temp/greta_cons_strikes_with_resids.dta", clear
	order date ags5 endid municipality startid count ///
	res_ols res_ols_interaction_small res_ols_interaction_large   ///
	res_p res_p_interaction_small res_p_interaction_large  ///
	res_ols_desired  res_p_desired ///
	res_p_int_small_w res_p_int_small res_p_int_large_w res_p_int_large res_p_int_only_w   res_p_int_only
	
	
	* export 
	keep if ((date==td(15mar2019) | dat ==td(24may2019) | date==td(20sep2019)) & ///
	(municipality=="berlin"|municipality=="hamburg"|municipality=="münchen"|municipality=="köln" | ///
	municipality=="frankfurt am main"|municipality=="stuttgart"|municipality=="düsseldorf" | ///
	municipality=="leipzig"|municipality=="dortmund"|municipality=="essen"|municipality=="bremen" | ///
	municipality=="dresden"|municipality=="hannover"|municipality=="nuernberg"|municipality=="duisburg")) | ///
	((date==td(01mar2019) & municipality=="hamburg" | date==td(29mar2019) & municipality=="berlin" | date==td(21jun2019) & municipality=="aachen"))
	
	export delimited using "$data_temp/mobile_phone_resid_strikes/greta_cons_resid_all_models.csv", delimiter(";") replace
	
	
	
	
********************************************************************************
*	3) generate strike participation index
********************************************************************************	
	
	use "$data_temp/greta_cons_strikes_with_resids.dta", clear
	
	qui rename ags5 endags5
	
	*drop specifications that are not needed
	drop res_p_int_large res_p_int_small res_p_int_*
	
	
	* rename
	qui rename res_p_interaction_small   res_p_int_small
	qui rename res_p_interaction_large   res_p_int_large
	qui rename res_p_desired 			 res_p_int_only
	qui rename res_ols_interaction_small res_ols_int_small
	qui rename res_ols_interaction_large res_ols_int_large
	qui rename res_ols_desired 			 res_ols_int_only
	
	
	
	* merge distances 
	qui merge m:1 startid endid using "$data_temp/greta_cons_table_distance_start_end.dta", keep(match)
	drop _merge
	
	
	* keep if region is in certain distance
	keep if tripdistancekm <= 75
	
	* keep only positive residuals
	foreach var of varlist res* {
		replace `var' = 0 if `var' < 0
	}
	
	
	* add startags to be able to collapse over it in the next step
	qui rename startid teralytics_id
	qui merge m:1 teralytics_id using "$data_temp/greta_cons_conversion_table_teralytics_ags5.dta"
	drop _merge
	qui rename teralytics_id startid
	qui rename ags5 startags5
	order date startid startags5 endags5 endid municipality source
	
	* aggregation if there is more than one destination with a strike
	collapse (sum) count res*, by(startags5 date)
	
		
	* cummulative number of strike participants
	foreach var of varlist res* {
		bys startags5: gen cum_`var' = sum(`var')
	}
	
	* merge population data to startags5
	qui rename startags5 ags
	merge m:1 ags using "$data_final/population/greta_cons_population_ags5_prepared.dta"
	drop _merge
	
	
	* ratio cummulative number per population
	foreach var of varlist cum* {
		qui gen r_`var' = (`var'/pop_10_34)*100
	}
	
	qui save "$data_temp/greta_cons_strikes_participation.dta", replace
	
	
********************************************************************************
*	4) Combine with election data
********************************************************************************	
	
	
	
	// EU **********************************************************************
	use  "$data_temp/greta_cons_strikes_participation.dta", clear
	keep if date < td(26may2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags[_n] != ags[_n+1]
	keep if temp == 1
	drop temp
	qui gen election = "eu"

	rename ags ags5
	merge 1:1 ags5 election using "$data_final/elections/greta_cons_elections_ags5_prepared.dta"
	keep if _merge == 3 // drop other elections
	drop _merge
	qui save "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", replace
	
	
	
	// Brandenburg *************************************************************
	use  "$data_temp/greta_cons_strikes_participation.dta", clear
	keep if date < td(01sep2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags[_n] != ags[_n+1]
	keep if temp == 1
	drop temp
	qui gen election = "brandenburg"
	
	rename ags ags5
	merge 1:1 ags5 election using "$data_final/elections/greta_cons_elections_ags5_prepared.dta"
	keep if _merge == 3
	drop _merge
	qui append using "$data_temp/greta_cons_strikes_participation_election_outcomes.dta"
	qui save "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", replace
	
	
	// Saxony ******************************************************************
	use  "$data_temp/greta_cons_strikes_participation.dta", clear
	keep if date < td(01sep2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags[_n] != ags[_n+1]
	keep if temp == 1
	drop temp
	qui gen election = "saxony"
	
	rename ags ags5
	merge 1:1 ags5 election using "$data_final/elections/greta_cons_elections_ags5_prepared.dta"
	keep if _merge == 3
	drop _merge
	qui append using "$data_temp/greta_cons_strikes_participation_election_outcomes.dta"
	qui save "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", replace
	
	
	// Thuringia ***************************************************************
	use  "$data_temp/greta_cons_strikes_participation.dta", clear

	keep if date < td(27oct2019)
	capture drop temp 
	qui gen temp = . 
	qui replace temp = 1 if ags[_n] != ags[_n+1]
	keep if temp == 1
	drop temp
	qui gen election = "thuringia"
	
	rename ags ags5
	merge 1:1 ags5 election using "$data_final/elections/greta_cons_elections_ags5_prepared.dta"
	keep if _merge == 3
	drop _merge
	qui append using "$data_temp/greta_cons_strikes_participation_election_outcomes.dta"
	qui save "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", replace
	
	
	
********************************************************************************
*	5) Combine with regional database
********************************************************************************



	qui use "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", clear
	merge m:1 ags5 using "$data_final/regional_database/greta_cons_regional_database_ags5_prepared.dta"
	drop _merge
	
	
	
	
	
	// generate variables ******************************************************
	// bula
	qui gen bula = substr(ags5,1,2)
	qui destring bula, replace

	encode election, gen(election_num)
	qui gen ln_pop = ln(pop_t)
	
	
	
	// standardize variables	
	qui ds date ags5 ags_name count election pop_density_cat    , not
	foreach var of varlist `r(varlist)' {
		qui summ `var'  [fw=pop_t]
		qui gen `var'_st = (`var' - `r(mean)')/`r(sd)' 
	}	
	
	
	
	order date ags5 ags_name
	
	qui save "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", replace
	
	
	

