// ***************************** PREAMBLE***************************************
*	Created: 11.08.2020
*	Author: Marc Fabel
*	
*	Description:
*		Regression analysis of impact of soccer matches on persons
*
*	Input:
*		teralytics_daily_tottrips_modeall.dta
*		weather_daily
*		Schulferien_2020_Jan_Apr.dta			contains school and public holidays
*
*	Output:
*		-
*
* data note: mostly one AGS corresponds to one id (teralytics)
*	sporadically: one AGS contains more than one teralytics_id
	
	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   		"W:\EoCC\analysis"	
	global data				"$path\data\source\mobilephone"
	global holidays_data	"F:\econ\soc_ext\analysis\data\final\holidays\"

	
	
	
	
********************************************************************************
*	Prepare Soccer
********************************************************************************	
/*	
	// import soccer
	import delimited "$path\data\source\soccer\soccer_prepared.csv", encoding(UTF-8) clear
	qui gen refdatum = date(date, "DMY")
	order refdatum 
	format refdatum %td
	qui gen idlandkreis = floor(ags/1000)
	keep if refdatum > mdy(01,01,2020) 
	
	keep refdatum gameday home_team  attendance idlandkreis
	sort refdatum idlandkreis
	qui save "$path\data\source\soccer\soccer_prepared.dta", replace
*/	
	
	
	
********************************************************************************
*	Open and prepare data
********************************************************************************	
	
	*first shot - ignore mode of transportation
	qui use "$data/teralytics_daily_tottrips_modeall.dta", clear
	*drop if modeoftransport == "Plane"
	keep if modeoftransport == "Train" || modeoftransport == "Road"
	collapse (sum) inb outb within , by(id refdatum)
	qui merge m:1 id using "$data/conc_teralytics_idlandkreis.dta"
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
	
	
	
	capture drop corona
	qui gen corona = cond(refdatum>=td(22mar2020),1,0)
	order corona
	
	
	
********************************************************************************
*	Play around with model
********************************************************************************
	
	// define regression variables *************************************************
	global gd 				"d_gameday"
	global region_fe 		"i.id"
	global time_fe 			"i.dow i.woy i.month" //   i.woy
	global weather			"sun rain maxtemp"
	global holiday 			"i.sch_hday i.pub_hday i.fasching"
	global interaction 		"i.id##i.dow i.id##i.woy i.id##i.month" // woy 
	global corona			"i.corona#i.bula"
	
	
	
	* OLS
	reghdfe inb $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res
	
	
	* use Poisson
	capture drop resid_poisson
	foreach var of varlist inb {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $interaction $holiday $corona) d
		predict fit_poisson
		qui gen resid_poisson = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	
/*
-----------------------------------------------------+
 Absorbed FE | Categories  - Redundant  = Num. Coefs |
-------------+---------------------------------------|
          id |       513           0         513     |
         dow |         7           1           6     |
         woy |        18           1          17    ?|
       month |         4           2           2    ?|
      id#dow |      3591         401        3190    ?|
      id#woy |      9234         513        8721    ?|
    id#month |      2052        1026        1026    ?|
    sch_hday |         2           1           1    ?|
    pub_hday |         2           1           1    ?|
    fasching |         2           1           1    ?|
-----------------------------------------------------+
*/	
	
	
	qui merge m:1 refdatum idlandkreis using "$path\data\source\soccer\soccer_prepared.dta"
	drop _merge
	
	order id refdatum idlandkreis dow woy month inb outb within home_team attendance _reg name  // modeoftransport
	sort idlandkreis refdatum
	
	
	
	// Dortmund
	twoway scatter _reg refdatum if idlandkreis == 5913 || ///
		scatter resid_poisson refdatum if idlandkreis == 5913, tline(24jan2020 01feb2020 14feb2020 29feb2020)
	
	
	// MUnich (Stadtbezirk
	twoway scatter _reg refdatum if id == 6242802 || ///
		scatter resid_poisson refdatum if id == 6242802, tline(25jan2020 09feb2020 21feb2020 08mar2020)
	/* ids von munich 
	6242800
	6242801    
	6242802
	6242803	
	6242804	
	*/
	
	
	
	// Dusseldorf
	twoway scatter _reg  refdatum if id == 6253904 || ///
		scatter resid_poisson refdatum if id == 6253904, tline(18jan2020 01feb2020 15feb2020 28feb2020)
	/*
	6253900
	6253901
	6253902
	6253903
    6253904
	*/

	
	// Freiburg
	twoway scatter _reg refdatum if idlandkreis == 8311 || ///
		scatter resid_poisson refdatum if idlandkreis == 8311, tline(25jan2020 08feb2020 22feb2020 07mar2020)
	 
	// Paderborn
	twoway scatter _reg refdatum if id ==  6241701 || ///
		scatter resid_poisson refdatum if id ==  6241701, tline(19jan2020 02feb2020 15feb2020 06mar2020)
	/*
	id
	6241701
	6241700
	6241702
	6241703
	*/
	
	// Hamburg Streikt
	*twoway scatter _reg refdatum if id ==  6278201 || ///
	*	scatter resid_poisson refdatum if id ==  6278201, tline(21feb2020)
	/*
	6278200
    6278201 
    6278202
	*/

	
	
	

/* Questions:
		- population weights
		- weather variables - Verfeinerung?
*/
	
	