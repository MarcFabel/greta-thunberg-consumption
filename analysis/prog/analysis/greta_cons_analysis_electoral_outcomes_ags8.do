
********************************************************************************
// ANALYSIS
********************************************************************************

	 use "$data_temp/greta_cons_strike_participation_election_prepared", clear



	* weighted
	eststo clear 
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" "p" "p_int_small" "p_int_large" "p_int_only" {		
		qui eststo a1: reghdfe the_greens 		cum_res_`row' [pw=pop_t], absorb(i.bula_num i.election_num) 
		qui eststo a2: reghdfe fd_the_greens	cum_res_`row' [pw=pop_t], absorb(i.bula_num i.election_num)
		
		* income
		qui eststo a3: reghdfe fd_the_greens	cum_res_`row' log_IncomeperCapita_st  [pw=pop_t], absorb(i.bula_num  i.election_num) vce(cluster ags5_num)
		
		* ue rate
		qui eststo a4: reghdfe fd_the_greens	cum_res_`row' ue_rate_st [pw=pop_t], absorb(i.bula_num  i.election_num) vce(cluster ags5_num)
		
		* demographics
		qui eststo a5: reghdfe fd_the_greens	cum_res_`row'   i.d_urban per_young  [pw=pop_t], absorb(i.bula_num i.election_num) vce(cluster ags5_num)
		
		
		* all 
		*qui eststo a6: reghdfe fd_the_greens	cum_res_`row' log_IncomeperCapita_st ue_rate_st i.d_urban per_young  [pw=pop_t], absorb(i.bula_num i.election_num) vce(cluster ags5_num)
		
		*qui eststo a6: reghdfe fd_the_greens	cum_res_`row'  share_university_degree_st  [pw=pop_t], absorb(i.bula_num i.election_num) vce(cluster ags5_num)
		
		
		esttab a*, ///
		se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
		sfmt( %12.0fc)	b(%12.3f) se(%12.3f) nonote  nonumbers ///
		coeflabels(cum_res_`row' "`row'")
		
		/*esttab a* using "$tables/temp/election_eu_ags8_`row'_weighted.tex", replace ///
			se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
			sfmt( %12.0fc)	b(%12.3f) se(%12.3f) ///
			 booktabs fragment label ///									///
			nomtitles nonumbers noobs nonote nogaps noline*/
		 
	}
	
	
	* check indiv regressions
	eststo clear 
	
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" { //  "p" "p_int_small" "p_int_large" "p_int_only"
		* baseline
		qui eststo a1: reghdfe fd_the_greens	cum_res_`row' [pw=pop_t], absorb(i.bula_num i.election_num)
		
		* education
		qui eststo a2: reghdfe fd_the_greens	cum_res_`row'  share_public    [pw=pop_t], absorb(i.bula_num i.election_num )
		
		esttab a*, ///
			se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
			sfmt( %12.0fc)	b(%12.4f) se(%12.3f) nonote noobs nonum  ///
			coeflabels(cum_res_`row' "`row'")
	}
	
	residential commercial green agriculture forest
	share_agriculture share_industry share_building share_trade share_service share_public

	
	* education funktioniert nicht
	
	
	
	
	
	// controls 
	eststo clear 
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" "p" "p_int_small" "p_int_large" "p_int_only" {
		disp "`row'"
		 *baseline
		qui eststo a1: reghdfe fd_the_greens	cum_res_`row' [pw=pop_t], absorb(i.bula_num)

		* income
		qui eststo a2: reghdfe fd_the_greens	cum_res_`row' log_IncomeperCapita  [pw=pop_t], absorb(i.bula_num)
		
		* ue_rate
		qui eststo a3: reghdfe fd_the_greens	cum_res_`row' ue_rate [pw=pop_t], absorb(i.bula_num)
		
		* population
		qui eststo a4: reghdfe fd_the_greens	cum_res_`row' pop_t_st [pw=pop_t], absorb(i.bula_num)
		
		* all
		qui eststo a5: reghdfe fd_the_greens	cum_res_`row' log_IncomeperCapita ue_rate  [pw=pop_t], absorb(i.bula_num)
		
		esttab a*, ///
		se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
		sfmt( %12.0fc)	b(%12.3f) se(%12.3f)
	}
	
	
	
	 reghdfe fd_the_greens	cum_res_p_int_small share_public  share_service [pw=pop_t], absorb(i.bula_num i.election_num) vce(cluster ags5_num)
	
	share_agriculture share_industry share_building share_trade share_service share_public
	
	esttab a* using "$tables/temp/election_eu_ags8_`row'_controls.tex", replace ///
			se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
			sfmt( %12.0fc)	b(%12.3f) se(%12.3f) ///
			 booktabs fragment label ///									///
			nomtitles nonumbers noobs nonote nogaps noline
		
	
	// issue: standard error cluster on bula or something?

	
	
	
	
	* unweighted
	eststo clear 
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" "p" "p_int_small" "p_int_large" "p_int_only" {
		disp "`row'"
		
		qui eststo a1: reghdfe the_greens 		cum_res_`row', noabsorb 
		qui eststo a2: reghdfe fd_the_greens	cum_res_`row', noabsorb
		qui eststo a3: reghdfe the_greens 		cum_res_`row', absorb(i.bula_num i.election_num) 
		qui eststo a4: reghdfe fd_the_greens	cum_res_`row', absorb(i.bula_num i.election_num)
		qui eststo a5: reghdfe the_greens 		cum_res_`row', absorb(i.ags5_num i.election_num) 
		qui eststo a6: reghdfe fd_the_greens	cum_res_`row', absorb(i.ags5_num i.election_num)
		
		esttab a*, ///
		se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
		sfmt( %12.0fc)	b(%12.3f) se(%12.3f)
		
		/*esttab a* using "$tables/temp/election_eu_ags8_`row'.tex", replace ///
			se star(* 0.10 ** 0.05 *** 0.01) keep(cum_res_*) ///
			sfmt( %12.0fc)	b(%12.3f) se(%12.3f) ///
			 booktabs fragment label ///									///
			nomtitles nonumbers noobs nonote nogaps noline*/
		 
	}
	
	
	

** XXXX: condition on only RECENT STRIKES!