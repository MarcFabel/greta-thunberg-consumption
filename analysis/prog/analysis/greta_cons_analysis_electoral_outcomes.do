
	
	
	
	// graphical impression 
	foreach var_spec of varlist r_cum_res_p_interaction_small{
		twoway scatter the_greens `var_spec' if election == "eu", color(navy%20) m(o) || ///
			scatter the_greens `var_spec' if election == "brandenburg", color(maroon%40) m(D) || ///
			scatter the_greens `var_spec' if election == "saxony", color(forest_green%40) m(S) || ///
			scatter the_greens `var_spec' if election == "thuringia", color(dkorange%40) m(T) || ///
			lfit the_greens `var_spec' if election == "eu", color(navy%30) lp(dash) || ///
			lfit the_greens `var_spec' if election == "brandenburg", color(maroon%30) lp(dash) || ///
			lfit the_greens `var_spec' if election == "saxony", color(forest_green%30) lp(dash) || ///
			lfit the_greens `var_spec' if election == "thuringia", color(dkornage%30) lp(dash) ///
			scheme(s1mono) plotregion(color(white)) ///
			legend(label(1 "eu") label(2 "b") label(3 "sa") label(4 "th") pos(2) ring(0) col(2) ///
			region(color(none)) size(small) order(1 2 3 4))  ///
			ytitle("Election results the greens") xtitle("Participation index")
	}
	
	
	
	// regression
	use "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", clear
	
	
	
	
	
	
	// compare standardized specificationsz
	eststo clear
	foreach y of varlist the_greens_st {
		qui eststo a1: reg `y' r_cum_res_ols_st i.bula i.election_num
		qui eststo a2: reg `y' r_cum_res_ols_int_small_st i.bula i.election_num
		qui eststo a3: reg `y' r_cum_res_ols_int_large_st i.bula i.election_num
		qui eststo a4: reg `y' r_cum_res_ols_int_only_st i.bula i.election_num
		
		qui eststo a5: reg `y' r_cum_res_p_st i.bula i.election_num
		qui eststo a6: reg `y' r_cum_res_p_int_small_st i.bula i.election_num
		qui eststo a7: reg `y' r_cum_res_p_int_large_st i.bula i.election_num
		qui eststo a8: reg `y' r_cum_res_p_int_only_st i.bula i.election_num
	}
	esttab a*,  													///
		se star(* 0.10 ** 0.05 *** 0.01) keep(r_cum_res_*) 		
		
	
	
	
	// generate overview table (rows:part-spec - columns: y-spec & controls)
	
	* define controls
	
	global x_pop  		"ln_pop_st i.pop_density_cat"
	global x_educ 		"share_university_degree_st"
	global x_ue   		"ue_rate_st"
	global x_sectors	"share_agriculture_st share_industry_st share_building_st share_trade_st share_service_st share_public_st"
	global x_1_urban	"" //	   pop_density_st 
	
	global district_controls "$x_pop $x_educ $x_ue $x_sectors $x_1_urban"
	
	
	// greens and FD greens w/o controls
	eststo clear
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" "p" "p_int_small" "p_int_large" "p_int_only" {
	disp "`row'"
		qui eststo a1: reg the_greens_st 	r_cum_res_`row'_st i.bula i.election_num
		qui eststo a2: reg fd_the_greens_st r_cum_res_`row'_st i.bula i.election_num
		
		esttab a*, ///
		se star(* 0.10 ** 0.05 *** 0.01) keep(r_cum_res_*)
	}
	
	
	
	// adding controls
	use "$data_temp/greta_cons_strikes_participation_election_outcomes.dta", clear
	
	eststo clear 
	foreach row in "ols" "ols_int_small" "ols_int_large" "ols_int_only" "p" "p_int_small" "p_int_large" "p_int_only" {
		disp "`row'"
		qui eststo a1: reg the_greens_st 	r_cum_res_`row'_st i.bula i.election_num 
		qui eststo a2: reg fd_the_greens_st r_cum_res_`row'_st i.bula i.election_num 
		qui eststo a3: reg the_greens_st 	r_cum_res_`row'_st i.bula i.election_num $x_pop
		qui eststo a4: reg fd_the_greens_st r_cum_res_`row'_st i.bula i.election_num $x_pop
		qui eststo a5: reg the_greens_st 	r_cum_res_`row'_st i.bula i.election_num $x_ue $x_sectors
		qui eststo a6: reg fd_the_greens_st r_cum_res_`row'_st i.bula i.election_num $x_ue $x_sectors
		qui eststo a7: reg the_greens_st 	r_cum_res_`row'_st i.bula i.election_num $x_educ
		qui eststo a8: reg fd_the_greens_st r_cum_res_`row'_st i.bula i.election_num $x_educ
		
		esttab a*, ///
		se star(* 0.10 ** 0.05 *** 0.01) keep(r_cum_res_*)
	}
	
	
	