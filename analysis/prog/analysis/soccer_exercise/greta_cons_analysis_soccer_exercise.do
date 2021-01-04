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
	global graphs			"$path/output/graphs/mobile_phone_exploration/"

	
	
	
	
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
	*keep if modeoftransport == "Train" | modeoftransport == "Road"
	drop if modeoftransport == "Plane" | modeoftransport == "Road" 				// keep only public transport
	collapse (sum) inb outb within , by(id refdatum)
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
	
	
	
	capture drop corona
	qui gen corona = cond(refdatum>=td(13mar2020),1,0)
	order corona
	
	qui gen inb_within = inb + within
	qui gen inb_within_thsd = inb_within/1000
	qui gen inb_thsd = inb/1000
	qui gen within_thsd = within/1000
	
********************************************************************************
*	Play around with model
********************************************************************************
	
	// define regression variables *************************************************
	global region_fe 		"i.id"
	global time_fe 			"i.dow i.woy i.month" //   i.woy
	global weather			"sun rain maxtemp"
	global holiday 			"i.sch_hday i.pub_hday i.fasching"
	global interaction 		"i.id##i.dow i.id##i.woy i.id##i.month" // woy 
	global corona 			"i.dow##i.woy##i.bula"
	global time_fe2			"i.dow i.woy"	
	global interaction2		"i.id##i.dow i.id##i.woy"
	global corona2			"i.corona##i.bula i.corona##i.dow"
	global corona3			"i.dow##i.corona"
	
	

	
	* OLS
	reghdfe inb $weather , absorb($region_fe $time_fe $interaction $holiday $corona) res
	
	
	* use Poisson
	capture drop resid_poisson_full
	foreach var of varlist inb_withtin {
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $interaction $holiday $corona) d
		predict fit_poisson
		qui gen resid_poisson_full = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	capture drop res_p_full
	foreach var of varlist inb_within inb within{
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe $interaction $holiday $corona) d
		predict fit_poisson
		qui gen res_p_full_`var' = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist inb_within inb within{
		ppmlhdfe `var' $weather, absorb($region_fe $time_fe2 $interaction2 $holiday $corona) d
		predict fit_poisson
		qui gen res_p_full2_`var' = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	foreach var of varlist inb_within inb within {
		ppmlhdfe `var' , absorb($region_fe $time_fe $interaction $holiday $corona2) d
		predict fit_poisson
		qui gen res_p_full_corona2_`var' = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}
	
	
// Leave weather out as it is missing for too many observations

* try easy small model w/o interaction
	
/*	
	* use Poisson
	capture drop resid_poisson_simple
	foreach var of varlist inb {
		ppmlhdfe `var' , absorb($region_fe $time_fe $interaction $holiday $corona) d
		predict fit_poisson
		qui gen resid_poisson_simple = `var' - fit_poisson
		drop _ppmlhdfe_d fit_poisson
	}	
*/	
	
	
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
		scatter resid_poisson_full refdatum if id == 6242802, tline(25jan2020 09feb2020 21feb2020 08mar2020)
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

	
	
	*inbound & within
	foreach var of varlist res_p_full_corona2_inb_within  {
		capture drop res_thsd
		qui gen res_thsd = `var'/1000
	}
	
	twoway scatter res_thsd refdatum if id ==  6278202, yaxis(1) color(navy)  ///
			yline(0, lcolor(cranberry) axis(1))	|| ///
		line inb_within_thsd refdatum if  id ==  6278202 & sun !=., ///
			tline(21feb2020, lcolor(cranberry))  yaxis(2) color(maroon%60) lw(medthick) ///
			ytitle("Residuals [in 1,000]", axis(1)) ytitle("Inb & withtin journeys [in 1,000]", axis(2)) ///
			xtitle(Date) title("Inb & within residuals oepnv") subtitle("train & not classified") ///
			legend(off) scheme(s1mono)
	graph export "$graphs/HH_res_p_full_inb_within.pdf", as(pdf) replace
	
	
	*within
	foreach var of varlist res_p_full_corona2_within  {
		capture drop res_thsd
		qui gen res_thsd = `var'/1000
	}
	twoway scatter res_thsd refdatum if id ==  6278202, yaxis(1) color(navy)  ///
			yline(0, lcolor(cranberry) axis(1))	|| ///
		line within_thsd refdatum if  id ==  6278202 & sun !=., ///
			tline(21feb2020, lcolor(cranberry))  yaxis(2) color(maroon%60) lw(medthick) ///
			ytitle("Residuals [in 1,000]", axis(1)) ytitle("Withtin journeys [in 1,000]", axis(2)) ///
			xtitle(Date) title("Within residuals oepnv") subtitle("train & not classified") ///
			legend(off) scheme(s1mono)
	graph export "$graphs/HH_res_p_full_within.pdf", as(pdf) replace
	
	
	*inbound
	foreach var of varlist res_p_full_corona2_inb  {
		capture drop res_thsd
		qui gen res_thsd = `var'/1000
	}
	twoway scatter res_thsd refdatum if id ==  6278202 & abs(res_thsd)<50, yaxis(1) color(navy)  ///
			yline(0, lcolor(cranberry) axis(1))	|| ///
		line inb_thsd refdatum if  id ==  6278202 & sun !=., ///
			tline(21feb2020, lcolor(cranberry))  yaxis(2) color(maroon%60) lw(medthick) ///
			ytitle("Residuals [in 1,000]", axis(1)) ytitle("Inb journeys [in 1,000]", axis(2)) ///
			xtitle(Date) title("Inb  residuals oepnv") subtitle("train & not classified") ///
			legend(off) scheme(s1mono)
	graph export "$graphs/HH_res_p_full_inb.pdf", as(pdf) replace
	
	/*
	6278200
    6278201 
    6278202
	*/

	

	