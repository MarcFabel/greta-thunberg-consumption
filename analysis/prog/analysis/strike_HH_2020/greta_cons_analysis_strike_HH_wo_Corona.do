
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
	qui drop if refdate >= td(10mar2020)
	
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


	
	
	*Poisson
		
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
	
	

	
	qui save "$temp_data/greta_cons_soccer_ex_orig_post_est_oepnv_wo_corona", replace
	
	
	
	

// export Hamburg	
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv_wo_corona, clear	
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
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv_wo_corona, clear	
	keep if endid == 6278202
	collapse (sum) count res_p*, by(refdatum)
	qui gen dow = dow(refdatum)
	
	twoway scatter res_p_full_weather refdatum  , color(pink) yaxis(1) || ///
		scatter res_p_full2 refdatum,  yaxis(1) || ///
		line count refdatum, yaxis(2) ///
		tline(21feb2020 )  yline(0)
	
	
	
	
	
	
	
	*check distribution of residuals
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv_wo_corona, clear	
	keep if endid == 6278202
	keep if refdatum == td(21feb2020) 
	collapse (sum) count res_p_*, by(refdatum start_ags)
	
	hist res_p_small_weather if res_p_small_weather < 50000 & res_p_small_weather > 73, w(250) ///
		title("Distribution of OEPNV (train&nc) residuals") subtitle("Top 10% (resids > 73) w/o Hamburg, AGS level") ///
		xtitle(Residuals) plotregion(color(white)) scheme(s1mono)
	graph export "$graphs/histogram_residuals_oepnv_top10pct_HH_2020_02_21.pdf", as(pdf) replace
	
	
	* what is the within Hamburg mobility pattern
	use $temp_data/greta_cons_soccer_ex_orig_post_est_oepnv_wo_corona, clear	
	keep if endid == 6278202
	keep if refdatum == td(21feb2020)
	keep if start_ags == 2000
	order res_p_full_weather	