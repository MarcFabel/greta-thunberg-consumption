/*



Soccer exercise with the full matrix to see where people were coming from


updates: 16.09.2020 - include transport mode "not classified" to see whether this captures U & S-Bahn of 
adjacent municipalities
-> save it as V2

v1 contains only train & road journeys

*/


	clear all 
	set more off
	set processors 4
	set matsize 11000
	
	*paths
	global path   	   		"W:\EoCC\analysis"	
	global data				"$path\data\source\mobilephone"
	global holidays_data	"F:\econ\soc_ext\analysis\data\final\holidays\"
	global temp_data		"$path/data/temp/mobile_phone_soccer_residuals"
	global graphs			"$path/output/graphs/mobile_phone_exploration/"

	
	
	qui use "$data/raw_daily/teralytics_daily_fullmatrix.dta", clear
	qui keep if (mode == 4)  | (mode==1)											// Train 4 & Road 3 & not categorized 1 		| (mode == 3)
	qui collapse (sum) count dist, by(refdate startid endid)
	qui drop if startid == . | endid == .
	
	// * merge ags of start and end IDs & add other variables ******************
	
	* start id
	qui rename startid id
	qui merge m:1 id using "$data/conc_teralytics_idlandkreis.dta"					// perfect match
	qui rename id startid
	qui rename idlandkreis start_ags
	qui drop _merge aks_name name 
	
	* end id
	qui rename endid id
	qui merge m:1 id using "$data/conc_teralytics_idlandkreis.dta"					// perfect match
	qui rename id endid // keep variable name idlandkreis to merge weather information
	qui rename idlandkreis end_ags
	qui drop _merge aks_name name 
	
	* add weather data at start & endid (destination)
	qui rename refdate date
	qui rename start_ags idlandkreis
	qui merge m:1 idlandkreis date using "$data/weather_daily.dta"					// 15 % no weather info
	qui drop if _merge == 2
	qui rename idlandkreis start_ags
	qui drop zeitstempel _merge
	qui rename sun sun_start
	qui rename rain rain_start
	qui rename maxtemp maxtemp_start
	
	qui rename end_ags idlandkreis
	qui merge m:1 idlandkreis date using "$data/weather_daily.dta"					// 15 % no weather info
	qui drop if _merge == 2
	qui rename idlandkreis end_ags
	qui drop zeitstempel _merge
	qui rename sun sun_end
	qui rename rain rain_end
	qui rename maxtemp maxtemp_end
	qui rename date refdatum
	
	* add holidays
	qui gen bula = floor(start_ags/1000)
	qui merge m:1 bula refdatum using "$holidays_data/Schulferien_2020_Jan_Apr.dta"
	qui drop if _merge == 2	// zweite Jahreshälfte in 2020
	qui drop _merge ferien feiertag
	qui rename bula bula_start
	qui rename sch_hday sch_hday_start
	qui rename pub_hday pub_hday_start
	qui rename fasching fasching_start
	
	qui gen bula = floor(end_ags/1000)
	qui merge m:1 bula refdatum using "$holidays_data/Schulferien_2020_Jan_Apr.dta"
	qui drop if _merge == 2	// zweite Jahreshälfte in 2020
	qui drop _merge ferien feiertag
	qui rename bula bula_end
	qui rename sch_hday sch_hday_end
	qui rename pub_hday pub_hday_end
	qui rename fasching fasching_end
	
	
	* pairwise identifier
	qui tostring startid endid, gen(start_s end_s) 
	qui gen start_end_id_string = start_s + end_s
	qui drop start_s end_s
	egen start_end_id_num = group(start_end_id_string)
	xtset start_end_id_num refdatum 
	
	* generate date variables
	qui gen dow = dow(refdatum)
	label define DOW  0 "Sun" 1 "Mon" 2 "Tue" 3 "Wed" 4 "Thu" 5 "Fri" 6 "Sat"
	label val dow DOW
	qui gen month = month(refdatum)
	qui gen woy = week(refdatum)	
	
	* generate corona dummy
	capture drop corona
	qui gen corona = cond(refdatum>=td(22mar2020),1,0)
	order corona
	
	qui gen corona_v2 = cond(refdatum>=td(13mar2020),1,0)
	
	
********************************************************************************
*	Play around with model
********************************************************************************

	global region_fe 		"i.start_end_id_num"
	global time_fe 			"i.dow i.woy i.month" //   i.woy
	global weather			"sun_start rain_start maxtemp_start sun_end rain_end maxtemp_end"
	global holiday 			"i.sch_hday_start i.pub_hday_start i.fasching_start i.sch_hday_end i.pub_hday_end i.fasching_end"
	global interaction 		"i.start_end_id_num##i.dow i.start_end_id_num##i.woy i.start_end_id_num##i.month" // woy 
	global corona1			"i.dow##i.woy##i.bula_end" // i.corona#i.bula
	
	global time_fe2			"i.dow i.woy"	
	global interaction2		"i.start_end_id_num##i.dow i.start_end_id_num##i.woy"
	global corona2			"i.corona##i.bula_end i.corona##i.dow"
	
	global time_fe3	 		"i.dow i.month"
	global interaction3		"i.start_end_id_num##i.dow i.start_end_id_num##i.month"
	
	global corona3 			"i.corona_v2##i.dow i.corona_v2##i.bula_end"


	*OLS
	reghdfe count , absorb($region_fe $time_fe $holiday $corona1) res(res_small)
	reghdfe count , absorb($region_fe $time_fe $interaction $holiday $corona1) res(res_full)
	
	reghdfe count $weather , absorb($region_fe $time_fe $holiday $corona1) res(res_small_weather)
	reghdfe count $weather , absorb($region_fe $time_fe $interaction $holiday $corona1) res(res_full_weather)
	
	reghdfe count , absorb($region_fe $time_fe2 $holiday $corona1) res(res_small_nomonth)
	reghdfe count , absorb($region_fe $time_fe2 $interaction2 $holiday $corona1) res(res_full_nomonth)
	
	reghdfe count , absorb($region_fe $time_fe $holiday $corona2) res(res_small_corona2)
	reghdfe count , absorb($region_fe $time_fe $interaction $holiday $corona2) res(res_full_corona2)
	
	
	*Poisson
	foreach var of varlist count {
		capture drop res_p*
		ppmlhdfe `var', absorb($region_fe $time_fe $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_small = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var', absorb($region_fe $time_fe $interaction $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_small_weather = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $interaction $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full_weather = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' , absorb($region_fe $time_fe $holiday $corona2) d
		predict fit_poisson
		qui gen res_p_small_corona2 = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' , absorb($region_fe $time_fe $interaction $holiday $corona2) d
		predict fit_poisson
		qui gen res_p_full_corona2 = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe2 $interaction2 $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full2 = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe3 $interaction3 $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full3 = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe i.start_end_id_num##i.dow $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full4 = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe i.start_end_id_num##i.dow $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full4 = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}

	
	qui save "$temp_data/greta_cons_soccer_ex_orig_post_est_oepnv", replace
	
	
// check whether it works the same way as the aggregated data
	
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv, clear
	
	
	keep if endid == 6242802
	collapse (sum) res_small res_full_model, by(refdatum)
	
	
	twoway scatter res_small refdatum || ///
		scatter res_full_model refdatum , tline(25jan2020 09feb2020 21feb2020 08mar2020)
	
	
********************************************************************************
*	Export 
********************************************************************************
	
	
// export for Munich 
	use $temp_data/greta_cons_soccer_ex_orig_post_est_V2, clear	
	keep if endid == 6242802
	keep if refdatum == td(25jan2020) | refdatum == td(09feb2020) | refdatum == td(21feb2020) | refdatum == td(08mar2020) 
	collapse (sum) count res_small res_full_model, by(refdatum start_ags)
	tostring start_ags, replace format(%05.0f)
	
	
	*export excel "$temp_data/soccer_cellphone_origin.xlsx", firstrow(variables) replace
	foreach match in "25jan2020" "09feb2020" "21feb2020" "08mar2020" {
		preserve
			keep if refdatum == td(`match')
			drop refdatum
			export delimited "$temp_data/munich_`match'.csv", delimiter(";") replace
		restore
	}
	

	
// export for Freiburg
	use $temp_data/greta_cons_soccer_ex_orig_post_est_V2, clear	
	keep if endid == 6276800
	keep if refdatum == td(25jan2020) | refdatum == td(08feb2020) | refdatum == td(22feb2020) | refdatum == td(07mar2020) 
	collapse (sum) count res_small res_full_model, by(refdatum start_ags)
	tostring start_ags, replace format(%05.0f)
	
	
	*export excel "$temp_data/soccer_cellphone_origin.xlsx", firstrow(variables) replace
	foreach match in "25jan2020" "08feb2020" "22feb2020" "07mar2020" {
		preserve
			keep if refdatum == td(`match')
			drop refdatum
			export delimited "$temp_data/FRI_`match'.csv", delimiter(";") replace
		restore
	}
		
	
	
	
// export for Dusseldorf
	use $temp_data/greta_cons_soccer_ex_orig_post_est_V2, clear
	keep if endid == 6253904
	keep if refdatum == td(18jan2020) | refdatum == td(01feb2020) | refdatum == td(15feb2020) | refdatum == td(28feb2020) 
	collapse (sum) count res_small res_full_model, by(refdatum start_ags)
	tostring start_ags, replace format(%05.0f)
	

	foreach match in "18jan2020" "01feb2020" "15feb2020" "28feb2020" {
		preserve
			keep if refdatum == td(`match')
			drop refdatum
			export delimited "$temp_data/dusseldorf_`match'.csv", delimiter(";") replace
		restore
	}
	
	
// export Dortmund 
	use $temp_data/greta_cons_soccer_ex_orig_post_est_V2, clear	
	keep if endid == 182906500
	keep if refdatum == td(24jan2020) | refdatum == td(01feb2020) | refdatum == td(14feb2020) | refdatum == td(29feb2020) 
	collapse (sum) count res_small res_full_model, by(refdatum start_ags)
	tostring start_ags, replace format(%05.0f)
	
	
	*export excel "$temp_data/soccer_cellphone_origin.xlsx", firstrow(variables) replace
	foreach match in "24jan2020" "01feb2020" "14feb2020" "29feb2020" {
		preserve
			keep if refdatum == td(`match')
			drop refdatum
			export delimited "$temp_data/DTM_`match'.csv", delimiter(";") replace
		restore
	}
	
	
	
	
// export Hamburg	
	use $temp_data/greta_cons_soccer_ex_orig_post_est_nc, clear	
	keep if endid == 6278202
	keep if refdatum == td(21feb2020) 
	collapse (sum) count res_*, by(refdatum start_ags)
	tostring start_ags, replace format(%05.0f)
	
	
	*export excel "$temp_data/soccer_cellphone_origin.xlsx", firstrow(variables) replace
	foreach match in "21feb2020" {
		preserve
			keep if refdatum == td(`match')
			drop refdatum
			export delimited "$temp_data/HH_`match'_oepnv.csv", delimiter(";") replace
		restore
	}	
	

	
	
	*check aggregate
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv, clear	
	keep if endid == 6278202
	collapse (sum) count res_p*, by(refdatum)
	qui gen dow = dow(refdatum)
	qui gen count_thsd = count/1000
	qui gen res_thsd = res_p_full_corona2/1000
	
	twoway scatter res_p_full_corona2 refdatum  , color(pink) yaxis(1) || ///
		scatter res_p_full2 refdatum,  yaxis(1) || ///
		line count refdatum, yaxis(2) ///
		tline(21feb2020 )  yline(0)
	
	
	twoway scatter res_thsd refdatum if abs(res_p_full_corona2) < 100000  , ///
			color(navy) yaxis(1) || ///
		line count_thsd refdatum, yaxis(2)  color(maroon%60) lw(medthick) ///
			tline(21feb2020, lcolor(cranberry))  yline(0, lc(black)) ///
			legend(off) ytitle("Residuals [in 1,000]", axis(1))  ytitle("Journeys [in 1,000]", axis(2)) ///
			xtitle(Date) title("Inb & within residuals oepnv") subtitle("train & not classified") ///
			scheme(s1mono)
		
			 
			
	
	
	
	
	*check distribution of residuals
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv, clear	
	keep if endid == 6278202
	keep if refdatum == td(21feb2020) 
	collapse (sum) count res_p_*, by(refdatum start_ags)
	
	
	hist  res_p_full2 if   res_p_full2 < 6000, ///
		title("Distribution of OEPNV (train&nc) residuals") subtitle("Top 10% (resids > 17) w/o Hamburg, AGS level") ///
		xtitle(Residuals) plotregion(color(white)) scheme(s1mono)
	graph export "$graphs/histogram_residuals_oepnv_top10pct_HH_2020_02_21.pdf", as(pdf) replace
	
	
	* what is the within Hamburg mobility pattern
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv, clear	
	keep if endid == 6278202
	keep if refdatum == td(21feb2020)
	keep if start_ags == 2000
	order res_p_full*
	
	
	
	