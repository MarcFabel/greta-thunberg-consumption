// ***************************** PREAMBLE***************************************
*	Created: 12.12.2020
*	Author: Marc Fabel
*	
*	Description:
*		Prepare region-day-panel
*
*	Input:
*		deldd-1-daily_long_distance_journeys_hX.csv		[source]				
*		greta_cons_weather_daily						[intermediate]
*		Schulferien_201.dta								[intermediate]			contains school and public holidays
*
*	Output:
*		greta_cons_teralytics_prepared.dta				[final]
*

	
	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   			"W:\EoCC\analysis"	
	global data_source			"$path\data\source"
	global data_intermediate	"$path/data/intermediate"
	global data_temp			"$path/data/temp"
	global data_final			"$path/data/final" 

	
	global program_start_time "$S_DATE $S_TIME"

	
********************************************************************************
*	Combine data sets
********************************************************************************


	// append Teraltics data stes (half-year) ***********************************
	import delimited "$data_source/teralytics/deldd-1-daily_long_distance_journeys_h1.csv", encoding(UTF-8) stringcols(2 4) clear 
	qui save "$data_temp/greta_cons_teralytics_h1.dta", replace


	import delimited "$data_source/teralytics/deldd-1-daily_long_distance_journeys_h2.csv", encoding(UTF-8) stringcols(2 4) clear 
	qui append using "$data_temp/greta_cons_teralytics_h1.dta"
	
	qui erase "$data_temp/greta_cons_teralytics_h1.dta"
	

	// Work with small subsample to check code
	*qui use "$data_temp/temp.dta", clear // small subsmaple of h1 to try code
	
	
	
	
	// generate date and reshape data  *****************************************
	
	capture drop date
	qui gen date = date(substr(bucket,1,10), "YMD")
	format date %td
	drop bucket 
	
	
	* reshape 
	qui gen mode = "_nc" if modeoftransport == "Not Classified"
	qui replace mode = "_plane" if modeoftransport == "Plane"
	qui replace mode = "_road" if modeoftransport == "Road"
	qui replace mode = "_train" if modeoftransport == "Train"
	qui drop modeoftransport
	qui reshape wide count, i(date startid startname endid endname tripdistancekm) j(mode) string
	
	*set missing to zero
	foreach var of varlist count* {
		qui replace `var' = 0 if `var' == .
	}
	
	
	* to check length of data set
	qui summ date
	local N_start_of_program = `r(N)'
	
	
	
	// combine with AGS information, weather and holiday ***********************
	
	* start
	qui destring startid, gen(id) 
	qui merge m:1 id using "$data_source/geography/conc_teralytics_idlandkreis.dta"
	qui count if _merge != 3
	assert r(N) == 0
	qui drop _merge name id startname
	
	qui merge m:1 idlandkreis date using  "$data_intermediate/weather/greta_cons_weather_daily.dta"
	qui keep if _merge == 3  // teralytix does not have data for 27feb2019
	qui drop _merge zeitstempel
	qui rename sun sun_start
	qui rename rain rain_start
	qui rename maxtemp maxtemp_start
	
	qui gen bula = floor(idlandkreis/1000)
	qui merge m:1 bula date using "$data_intermediate/holidays/Schulferien_2019.dta"
	qui keep if _merge == 3  // teralytix does not have data for 27feb2019
	qui drop _merge ferien feiertag 
	qui rename bula bula_start
	qui rename sch_hday sch_hday_start
	qui rename pub_hday pub_hday_start
	qui rename fasching fasching_start

	qui rename idlandkreis start_aks
	qui rename aks_name    start_aks_name

	
	
	* end 
	qui destring endid, gen(id) 
	qui merge m:1 id using "$data_source/geography/conc_teralytics_idlandkreis.dta"
	qui count if _merge != 3
	assert r(N) == 0
	qui drop _merge name id endname
	
	qui merge m:1 idlandkreis date using  "$data_intermediate/weather/greta_cons_weather_daily.dta"
	qui keep if _merge == 3  // teralytix does not have data for 27feb2019
	qui drop _merge zeitstempel
	qui rename sun sun_end
	qui rename rain rain_end
	qui rename maxtemp maxtemp_end
	
	qui gen bula = floor(idlandkreis/1000)
	qui merge m:1 bula date using "$data_intermediate/holidays/Schulferien_2019.dta"
	qui keep if _merge == 3  // teralytix does not have data for 27feb2019
	qui drop _merge ferien feiertag 
	qui rename bula bula_end
	qui rename sch_hday sch_hday_end
	qui rename pub_hday pub_hday_end
	qui rename fasching fasching_end
		
	qui rename idlandkreis end_aks
	qui rename aks_name    end_aks_name

	
	
	
	// generate variables ******************************************************
	
	* date variables	
	qui gen dow = dow(date)
	label define DOW  0 "Sun" 1 "Mon" 2 "Tue" 3 "Wed" 4 "Thu" 5 "Fri" 6 "Sat"
	label val dow DOW
	qui gen month = month(date)
	qui gen woy = week(date)
	

	* pairwise identifier
	qui gen start_end_id_string = startid + endid
	qui egen start_end_id_num = group(start_end_id_string)
	qui drop start_end_id_string
	xtset start_end_id_num date
	
	
	*export data
	order date dow start_aks startid start_aks_name end_aks endid end_aks_name
	sort date start_aks end_aks
	qui save "$data_final/greta_cons_teralytics_prepared.dta", replace
	
	
	*qui gen N = _n
	*keep if N < 1000000
	*drop N
	*qui save "$data_temp/temp_final.dta"
	
	
	* check length of data sets
	qui summ date
	local N_end_of_program = `r(N)'
	assert `N_start_of_program' == `N_end_of_program'
	
	

	// stop running time *******************************************************
	global program_end_time "$S_DATE $S_TIME"
	global temp_start =  clock("$program_start_time", "DMYhms")
	global temp_end   =   clock("$program_end_time", "DMYhms")
	global temp_diff = minutes($temp_end - $temp_start)
	
	disp "Runtime: $temp_diff minutes"







	


	
	
	
	
	
	