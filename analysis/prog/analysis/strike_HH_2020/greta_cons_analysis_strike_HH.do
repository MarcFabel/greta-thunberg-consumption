// First FFF Strike



	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   		"W:\EoCC\analysis"	
	global data				"$path\data\source\mobilephone"
	global holidays_data	"F:\econ\soc_ext\analysis\data\final\holidays\"
	global graphs			"$path/output/graphs/mobile_phone_exploration/"

	
	*first shot - ignore mode of transportation
	qui use "$data/teralytics_daily_tottrips_modeall.dta", clear
	drop outb
	qui replace modeoftransport = "_nc" if modeoftransport == "Not Classified"
	qui replace modeoftransport = "_r" if modeoftransport == "Road"
	qui replace modeoftransport = "_p" if modeoftransport == "Plane"
	qui replace modeoftransport = "_t" if modeoftransport == "Train"
	
	
	qui reshape wide inb within, i(id refdatum name) j(modeoftransport) s
	
	*drop if modeoftransport == "Plane" | modeoftransport == "Road" 				// keep only public transport
	*collapse (sum) inb outb within , by(id refdatum)
	merge m:1 id using "$data/conc_teralytics_idlandkreis.dta"
	qui drop _merge
	qui rename refdatum date
	merge m:1 idlandkreis date using "$data/weather_daily.dta"					// for 12 % of days no weather information
	qui rename date refdatum
	qui drop zeitstempel _merge
	
	qui gen bula = floor(idlandkreis/1000)
	merge m:1 bula refdatum using "$holidays_data/Schulferien_2020_Jan_Apr.dta"
	drop if _merge == 2
	drop _merge
	
	xtset id refdatum
	
	* generate date variables
	qui gen dow = dow(refdatum)
	label define DOW  0 "Sun" 1 "Mon" 2 "Tue" 3 "Wed" 4 "Thu" 5 "Fri" 6 "Sat"
	label val dow DOW
	qui gen month = month(refdatum)
	qui gen woy = week(refdatum)
	
	
	* generate corona variable
	capture drop corona
	qui gen corona = cond(refdatum>=td(22mar2020),1,0)
	order corona
	
	*add soccer information	
	qui merge m:1 refdatum idlandkreis using "$path\data\source\soccer\soccer_prepared.dta"
	drop _merge
	qui gen d_gameday = cond((refdatum == td(30jan2020) | ///
							  refdatum == td(01feb2020) | ///
							  refdatum == td(08feb2020) | ///
							  refdatum == td(14feb2020) | ///
							  refdatum == td(22feb2020) | ///
							  refdatum == td(01mar2020) | ///
							  refdatum == td(07mar2020)) & (idlandkreis == 2000), 1, 0)



	
	
	
	
	* generate outcome variable
	qui egen oepnv = rowtotal(inb_nc within_nc inb_t within_t)
	qui egen train = rowtotal(inb_t within_t)
	qui egen notcl = rowtotal(inb_nc within_nc)
	qui egen road = rowtotal(inb_r within_r)
	
	qui egen temp = rowtotal(inb_t within_nc)
	
	
	
	foreach mode in "oepnv" "train" "notcl" "road" "temp"{
	capture drop `mode'_thousand
		qui gen `mode'_thousand = `mode' /1000
	}
	
	
	
	order id refdatum idlandkreis aks_name dow woy month oepnv inb* within* home_team attendance name  // modeoftransport
	sort idlandkreis refdatum

	
********************************************************************************
*	Play around with model
********************************************************************************
	// define regression variables *************************************************
	global region_fe 		"i.id"
	global time_fe 			"i.dow##i.woy i.month" 
	global weather			"sun rain maxtemp"
	global holiday 			"i.sch_hday i.pub_hday i.fasching"
	global interaction 		"i.id##i.dow i.id##i.woy i.id##i.month" // woy 
	global corona			"i.woy##i.bula##i.dow"
	
	
	
	* OLS
	reghdfe oepnv $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res(res_ols_oepnv)
	reghdfe train $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res(res_ols_train)
	reghdfe notcl $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res(res_ols_notcl)
	reghdfe road $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res(res_ols_road)
	reghdfe temp $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res(res_ols_temp)
	
	
	* use Poisson
	
	foreach var of varlist oepnv {
		capture drop res_poisson_`var'
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $interaction $holiday $corona) d
		predict fit_poisson
		qui gen res_poisson_`var' = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	
	twoway scatter res_poisson_oepnv refdatum if id == 6278202,tline(21feb2020)  yline(0)
	
	
	* overview of variable specification (train, notcl & oepnv)
	foreach mode in "oepnv" "train" "notcl" "road" {	// loop through transport mode
		twoway scatter res_ols_`mode' refdatum if id == 6278202, yaxis(1) || ///
			scatter res_poisson_`mode' refdatum if id == 6278202, yaxis(1) || ///
			line `mode'_thousand refdatum if id == 6278202, yaxis(2) color(blue%50) ///
			tline(21feb2020)  yline(0) legend(off) title(`mode')
		graph export "$graphs/strike_HH_2020_feb_21_residuals_inb_within_`mode'.pdf", as(pdf) replace
	}
	
	
* inspect single aspects	
	foreach mode in "temp" {
		twoway scatter res_ols_`mode' refdatum if id == 6278202, yaxis(1) || ///
			scatter res_poisson_`mode' refdatum if id == 6278202, yaxis(1) || ///
			scatter res_ols_`mode' refdatum if id == 6278202 & dow == 0, yaxis(1) color(green) || ///
			line `mode'_thousand refdatum if id == 6278202, yaxis(2) color(blue%50) ///
			tline(21feb2020)  yline(0) legend(off) 
	}	
	
	
	
	
		foreach mode in "temp" {
		twoway scatter res_poisson_`mode' refdatum if id == 6278202, yaxis(1) || ///
			line `mode'_thousand refdatum if id == 6278202, yaxis(2) color(blue%50) ///
			tline(21feb2020)  yline(0) legend(off) 
	}	
	
	
	
	
	
	
	* in relation to the mean
	twoway scatter _reg refdatum if id == 6278202, yaxis(1) || ///
		line oepnv refdatum if id == 6278202, yaxis(2) color(blue%50) || ///
		scatter _reg refdatum if id == 6278202 & dow == 0, yaxis(1) color(red) ///
		tline(21feb2020 )  yline(0)
	
	
	
	
	preserve
		keep if refdatum >= td(01feb2020) & refdatum < td(01mar2020)
		
		twoway scatter _reg refdatum if id == 6278202 || ///
			scatter _reg refdatum if id == 6278202 & dow == 0  ,  color(red) || ///
			scatter _reg refdatum if id == 6278202 & d_gameday == 1  ,  color(green) tline(21feb2020 22mar2020) yline(0)
	restore
	
	
	
	
	
	// Hamburg Streikt (Heiligenfeld)
	preserve
	drop if d_gameday == 1
	twoway scatter _reg refdatum if id ==  6278202 || ///
		scatter resid_poisson_simple refdatum if id == 6278202 || ///
		scatter resid_poisson_full refdatum if id ==  6278202, tline(21feb2020 22mar2020)
	
	restore
	
	
	preserve
	drop if d_gameday == 1
	keep if refdatum >= td(01feb2020) & refdatum < td(01mar2020)
	twoway scatter _reg refdatum if id ==  6278202 , tline(21feb2020 22mar2020)
	
	restore
	
	
	
	
