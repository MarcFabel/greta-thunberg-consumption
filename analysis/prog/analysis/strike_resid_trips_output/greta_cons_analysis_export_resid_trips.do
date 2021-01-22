// ***************************** PREAMBLE***************************************
*	Created: 18.12.2020
*	Author: Marc Fabel
*	
*	Description:
*		Save only specific destinations
*
*	Input:
*		greta_cons_trips_resid_ols.dta				[temp]
*
*	Output:
*		
*
	
	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   			"W:\EoCC\analysis"	
	global data_temp			"$path/data/temp"

	global program_start_time "$S_DATE $S_TIME"
	
	
	
// 1) for selected places 	
	
	use "$data_temp/greta_cons_trips_resid_ols.dta", replace
	
	
	keep if endid == "006266500" & date==td(21jun2019) || ///
			endid == "006253500" & date==td(22jun2019) || ///
			endid == "006257100" & date==td(02aug2019) || ///
			endid == "006268300" & date==td(30nov2019) || ///
			endid == "006242203" & date==td(29mar2019) || ///
			endid == "006278202" & date==td(01mar2019)
			
			//Aachen, Garzweiler, Luebbenau, Jenschwalde, Berlin, Hamburg
			
	export delimited using "$data_temp/mobile_phone_resid_strikes/greta_cons_resid_ols_selected_places.csv", delimiter(";") replace
		
	
// 2) for selected dates - given the date where are all the residuals
	use "$data_temp/greta_cons_trips_resid_ols.dta", replace

	keep if date == td(01mar2019) || ///
			date == td(15mar2019) || ///
			date == td(24may2019) || ///
			date == td(21jun2019) || ///
			date == td(20sep2019) || ///
			date == td(27sep2019) || ///
			date == td(29nov2019) 
			
	collapse (sum) res* count, by(date endid)
	
	export delimited using "$data_temp/mobile_phone_resid_strikes/greta_cons_resid_ols_selected_times.csv", delimiter(";") replace

	
	
	
	
	
	
	//////////////////////////////////////////////////////
	// POISSON
	
	
	// 1) for selected places 	
	
	use "$data_temp/greta_cons_trips_resid_poisson.dta", replace
	
	
	keep if endid == "006266500" & date==td(21jun2019) || ///
			endid == "006253500" & date==td(22jun2019) || ///
			endid == "006257100" & date==td(02aug2019) || ///
			endid == "006268300" & date==td(30nov2019) || ///
			endid == "006242203" & date==td(29mar2019) || ///
			endid == "006278202" & date==td(01mar2019)
			
			//Aachen, Garzweiler, Luebbenau, Jenschwalde, Berlin, Hamburg
			
	export delimited using "$data_temp/mobile_phone_resid_strikes/greta_cons_resid_poisson_selected_places.csv", delimiter(";") replace
		
	
// 2) for selected dates - given the date where are all the residuals
	use "$data_temp/greta_cons_trips_resid_poisson.dta", replace

	keep if date == td(01mar2019) || ///
			date == td(15mar2019) || ///
			date == td(24may2019) || ///
			date == td(21jun2019) || ///
			date == td(20sep2019) || ///
			date == td(27sep2019) || ///
			date == td(29nov2019) 
			
	collapse (sum) res* count, by(date endid)
	
	export delimited using "$data_temp/mobile_phone_resid_strikes/greta_cons_resid_poisson_selected_times.csv", delimiter(";") replace
	
	
	
	
// try out new (desired) model	(until now just ols1)
	use "$data_temp/greta_cons_trips_resids_desired_model.dta", replace
	
	
	keep if endid == "006266500" & date==td(21jun2019) || ///
			endid == "006253500" & date==td(22jun2019) || ///
			endid == "006257100" & date==td(02aug2019) || ///
			endid == "006268300" & date==td(30nov2019) || ///
			endid == "006242203" & date==td(29mar2019) || ///
			endid == "006278202" & date==td(01mar2019)
			
			//Aachen, Garzweiler, Luebbenau, Jenschwalde, Berlin, Hamburg
			
	export delimited using "$data_temp/mobile_phone_resid_strikes/greta_cons_resid_desired_selected_places.csv", delimiter(";") replace



