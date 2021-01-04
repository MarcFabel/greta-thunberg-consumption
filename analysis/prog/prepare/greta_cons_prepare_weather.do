
* original code obtained from Victor Alipour, adjusted to meet our needs


	cap log close
	set more off
	clear all 
	set maxvar 10000


	global path 				"W:\EoCC\analysis\data"
	global weather_source 		"$path\source\weather_data\cdc_download_2020-12-09_16-44\data"
	global temp 				"$path\temp/\weather_preparation"
	global weather_output		"$path/intermediate/weather"

	


//////////////////////////////////////////////////////////////////////////////////
///////////////////// Weather data (Deutscher Wetterdienst) //////////////////////
/////////////////////////////////////////////////////////////////////////////////

/* Notes:
- weather data from 01. jan 2019 - 31. dec 2019
- aggregate weather information to the county level using weighted average
	of values from all weather station within a X km radius; weight = inverse distance
	between centroid of the county and station
	=> X = 50 km for hours of sunlight
	=> X = 30km for precipitaion
- gtools package needed

output files:  greta_cons_weather_daily
*/

********************************************************************************
*** STEP 1: Drop weather stations that do not measure EVERY DAY
	
* PULL: Sunlight hours data
	import delim "$weather_source/data_SDK_MN004.csv", clear varnames(1)
	
	bys sdo_id: gen N = _N
	su N,d
	
	// drop stations that do not record every day (38 = 14%)
	drop if N < r(max)
	
	keep sdo_id
	
	duplicates drop sdo_id, force
	
	// save active station ids in macro: 'sun_ids'
	levelsof sdo_id, local(sun_ids)
	global sun_ids `sun_ids'
	
	// save
	save "$temp/sdo_act_sun.dta", replace
	
* PULL: Precipitation (hight in mm)
	import delim "$weather_source/data_RS_MN006.csv", clear varnames(1)
	
	bys sdo_id: gen N = _N
	su N
	
	// drop stations that do not record every day (13.5%)
	drop if N < r(max)
	
	keep sdo_id
	
	duplicates drop sdo_id, force
	
	// save active station ids in macro: 'rain_ids'
	levelsof sdo_id, local(rain_ids)
	global rain_ids `rain_ids'
	
	// save
	save "$temp/sdo_act_rain.dta", replace
	
* PULL: maximal Temperature (2m above the ground)
	import delim "$weather_source/data_TXK_MN004.csv", clear varnames(1)
	
	bys sdo_id: gen N = _N
	su N
	
	// drop stations that do not record every day (5%)
	drop if N < r(max)
	
	keep sdo_id
	
	duplicates drop sdo_id, force
	
	// save active station ids in macro: 'rain_ids'
	levelsof sdo_id, local(tmax_ids)
	global tmax_ids `tmax_ids'
	
	// save
	save "$temp/sdo_act_tmpmax.dta", replace
	
********************************************************************************

********************************************************************************
*** STEP 2: Prepare Locations of counties

	/*--- PULL:  Landkreise - Standorte  ----*/
	import delim "$path\source\weather_data/landkreise_geo.csv", clear varnames(1)

	// clean
	keep 	geopoint cca
	rename 	cca2 	id			// Landkreis-ID
	split 	geopoint, parse(,)
	rename 	geopoint1 Lat
	rename 	geopoint2 Lon
	drop 	geopoint

	// Account for change in admin boundary of Göttingen/ Osterode am Harz
	*	before: only Göttingen: now Göttingen + Osterode am H.; latter is dropped
	replace id = 3159 if id == 3152
	drop if id == 3156 | missing(id)

	// keep only Kreise needed for dataset
	*rename id idlandkreis
	*merge 1:1 idlandkreis using "F:\Projekte\WFHCovid\01 Build\Output\wfh_destatis_nuts3.dta", keepusing(idlandkreis) nogen assert(3)
	* rename idlandkreis id

	destring Lon Lat, replace
	gen aux = 1
	
	lab var id "AKS 19"
	// save
	save "$temp/kreise_locations.dta", replace


********************************************************************************
*** STEP 3: Calculate inverse weighing matrix between LK and weather stations

** 3.1 Sunlight

	/*--- PULL:  Sonnenschein-Messstationen - Standorte  ----*/
	import delim "$weather_source/sdo_SDK_MN004.csv", clear varnames(1)
	
	// drop stations that do not record every day
	merge 1:1 sdo_id using "$temp/sdo_act_sun.dta", keep(3) nogen
	
	rename geogr_laenge 	Lon
	rename geogr_breite 	Lat
	
	keep sdo_id Lon Lat

	gen aux = 1
	
	reshape wide Lon Lat, i(aux) j(sdo_id)
	
	// merge stations with landkreise
	merge 1:m aux using "$temp/kreise_locations.dta", assert(3) nogen
	drop aux
	order id Lat Lon
	
	// calculate distances
	foreach j in $sun_ids {
					geodist Lat Lon Lat`j' Lon`j', generate(dist_`j')
	}
	drop Lon* Lat*
	
	// invert distances
	greshape long dist_, i(id) j(sdo_id)
	rename 	dist_ invdist
	replace invdist = 1/ invdist
		
	// save: LK + distances to stations, sunlight
	save "$temp/id_sdo_match_sun.dta", replace
	
** 3.2 Precipitation height in mm

	/*--- PULL:  Niederschlag -Messstationen - Standorte  ----*/
	import delim "$weather_source\sdo_RS_MN006.csv", clear varnames(1)
	
	// drop stations that do not record every day
	merge 1:1 sdo_id using "$temp/sdo_act_rain.dta", keep(3) nogen
	
	rename geogr_laenge 	Lon
	rename geogr_breite 	Lat
	
	keep sdo_id Lon Lat

	gen aux = 1
	
	greshape wide Lon Lat, i(aux) j(sdo_id)
	
	// merge stations with landkreise
	merge 1:m aux using "$temp/kreise_locations.dta", assert(3) nogen
	drop aux
	order id Lat Lon
	
	// calculate distances
	foreach j in $rain_ids {
					geodist Lat Lon Lat`j' Lon`j', generate(dist_`j')
	}
	drop Lon* Lat*
	
	// invert distances
	greshape long dist_, i(id) j(sdo_id)
	rename 	dist_ invdist
	replace invdist = 1/ invdist
		
	// save: LK + distances to stations, precipitation
	save "$temp/id_sdo_match_rain.dta", replace
	
** 3.2 (max) Temperature

	/*--- PULL:  Niederschlag -Messstationen - Standorte  ----*/
	import delim "$weather_source\sdo_TXK_MN004.csv", clear varnames(1)
	
	// drop stations that do not record every day
	merge 1:1 sdo_id using "$temp/sdo_act_tmpmax.dta", keep(3) nogen
	
	rename geogr_laenge 	Lon
	rename geogr_breite 	Lat
	
	keep sdo_id Lon Lat

	gen aux = 1
	
	greshape wide Lon Lat, i(aux) j(sdo_id)
	
	// merge stations with landkreise
	merge 1:m aux using "$temp/kreise_locations.dta", assert(3) nogen
	drop aux
	order id Lat Lon
	
	// calculate distances
	foreach j in $tmax_ids {
					geodist Lat Lon Lat`j' Lon`j', generate(dist_`j')
	}
	drop Lon* Lat*
	
	// invert distances
	greshape long dist_, i(id) j(sdo_id)
	rename 	dist_ invdist
	replace invdist = 1/ invdist
		
	// save: LK + distances to stations, precipitation
	save "$temp/id_sdo_match_tmpmax.dta", replace
********************************************************************************

********************************************************************************
*** STEP 4. Merge weather data with matrix and computed weighted average

* 4.1 Hours of sunlight

	// prep weather data
	import delim "$weather_source/data_SDK_MN004.csv", clear varnames(1)
	
	todate zeit, gen(date) p(yyyymmdd) f(%ddmcy)
	
	drop quali* produkt
		
	// merge with LK + matrix of inv. distances
	joinby sdo_id using "$temp/id_sdo_match_sun.dta"
	
	// drop station which are not within 50km distance from LK-centroid
	replace invdist = . if 1/invdist > 50

		
	// generate weighted mean of sunlight for each LK-day
	bys id date: egen sun = wtmean(wert), weight(invdist)
	keep zeitstempel date id sun
	
	// collapse
	gduplicates drop zeitstempel id, force 
	
	lab var sun "Sunshine duration in hours, DWD SDK_MN004"
	
	// save: LK-day, hrs of sunlight
	save "$temp/hrs_sunlight_kreise.dta", replace


	
* 4.2 Precipitation hight in mm

	// prep weather data
	import delim "$weather_source\data_RS_MN006.csv", clear varnames(1)
	
	todate zeit, gen(date) p(yyyymmdd) f(%ddmcy)
	
	drop quali* produkt
		
	// merge with LK + matrix of inv. distances
	joinby sdo_id using "$temp/id_sdo_match_rain.dta"
	
	// drop station which are not within 30km distance from LK-centroid
	replace invdist = . if 1/invdist > 30

		
	// generate weighted mean of rain for each LK-day
	bys id date: egen rain = wtmean(wert), weight(invdist)
	keep zeitstempel date id rain
	
	// collapse
	gduplicates drop zeitstempel id, force 
	
	lab var rain "Precipitaion hight in mm, DWD RS MN006"
	
	// save: LK-day, hrs of sunlight
	save "$temp/precipitaion_kreise.dta", replace

* 4.3 max temperature

	// prep weather data
	import delim "$weather_source\data_TXK_MN004.csv", clear varnames(1)
	
	todate zeit, gen(date) p(yyyymmdd) f(%ddmcy)
	
	drop quali* produkt
		
	// merge with LK + matrix of inv. distances
	joinby sdo_id using "$temp/id_sdo_match_tmpmax.dta"
	
	// drop station which are not within 50km distance from LK-centroid
	replace invdist = . if 1/invdist > 50

		
	// generate weighted mean of temp. for each LK-day
	bys id date: egen maxtemp = wtmean(wert), weight(invdist)
	keep zeitstempel date id maxtemp
	
	// collapse
	gduplicates drop zeitstempel id, force 
	
	lab var maxtemp "Maximal temperature, DWD TXK MN004"
	
	// save: LK-day, max. temp
	save "$temp/maxtemp_kreise.dta", replace

	
********************************************************************************
*** STEP 5. Merge into final file

* 1) sunlight
	use "$temp/hrs_sunlight_kreise.dta", clear
	
* 2) precipitation
	merge 1:1 id date using "$temp/precipitaion_kreise.dta", assert(3) nogen
	
* 3) max temperature
	merge 1:1 id date using "$temp/maxtemp_kreise.dta", assert(3) nogen
	
 	
	// finalize & save
	rename id idlandkreis
	
* save: daily data	
	save "$weather_output/greta_cons_weather_daily.dta", replace

	
	
	
	
	
	
	
	