	// train only
	
	
	clear all 
	set more off
	set processors 4
	set matsize 11000
	
	*paths
	global path   	   		"W:\EoCC\analysis"	
	global data				"$path\data\source\mobilephone"
	global holidays_data	"F:\econ\soc_ext\analysis\data\final\holidays\"
	global temp_data		"$path/data/temp/mobile_phone_soccer_residuals" 	
	
	
	qui use "$data/raw_daily/teralytics_daily_fullmatrix.dta", clear
	qui keep if (mode == 1)  													// Train 4 & Road 3 & not categorized 1 		| (mode == 3)
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
		qui gen res_p_small_we = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist count {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $interaction $holiday $corona1) d
		predict fit_poisson
		qui gen res_p_full_we = `var' - fit_poisson
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
	
	
	qui save "$temp_data/greta_cons_soccer_ex_orig_post_est_nc", replace
	
	
	use "$temp_data/greta_cons_soccer_ex_orig_post_est_nc", clear