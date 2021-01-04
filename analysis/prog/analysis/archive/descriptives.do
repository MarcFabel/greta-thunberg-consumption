clear 
clear matrix
set more off
capture log close

/*-------------PREAMBLE -----------------------------*/
global dir_data "W:\EoCC\analysis\data\source\fff_strikes"
global dir_temp "W:\EoCC\analysis\output\temp"
global dir_prepare "W:\EoCC\analysis\prog\prepare"
global dir_graph "W:\EoCC\analysis\output\graphs\descriptive"

use "$dir_temp\appended_raw.dta", clear
gen obs = 1
bys date_format: gen obs_sum = _N


* Number of protest by date
tab date_format

* Graph
graph bar (sum) obs, over(date_format)
twoway line obs_sum date_format, ytitle(Protests) xtitle(Date) xlabel(, format(%dM/CY))

* Absolute amount of protest days and average protests per day, min, max
tabstat obs_sum, statistics (count mean median min max)


use "$dir_temp\appended_cleaned.dta", clear
gen obs = 1
bys city3: gen obs_sum = _N

* Number of protest by city
tab city3

* Number of cities and (average) protests per city
tabstat obs_sum, statistics (count mean median min max)

* Protests in small communities (define small community: less then 3 protests)
preserve
drop if diff_city == 1
keep if obs_sum <= 2		
tabulate date_format
graph bar (sum) obs, over (date_format)
restore		///Protests in rather inactive communities mainly take place at standard, national-wide dates. Those are spread all over 2019

use "$dir_temp\appended_cleaned_geocoded.dta", clear
gen obs = 1
bys g_state: gen obs_sum = _N

* Protests by state
tab g_state
tabstat obs_sum, statistics (count mean median min max)
graph bar (sum) obs, over (g_state)

*Protests by location within city
bysort city3 location3: egen loc_sum = sum(obs)
tabstat loc_sum, statistics (count mean median min max)


