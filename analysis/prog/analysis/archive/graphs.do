clear 
clear matrix
set more off
capture log close

/*-------------PREAMBLE -----------------------------*/
global dir_data "W:\EoCC\analysis\data\source\fff_strikes"
global dir_temp "W:\EoCC\analysis\output\temp"
global dir_prepare "W:\EoCC\analysis\prog\prepare"
global dir_descriptive "W:\EoCC\analysis\output\graphs\descriptive"



use "$dir_temp/appended_raw.dta"

/*-----------------SCHEME---------------*/

sysdir set PERSONAL "c:\ado\personal"  //ifo scheme, but I think it doesn't look so nice
set scheme ifo2017


/*-------------GRAPH PROTESTS BY DATE-----------------------------*/

bysort date_format: egen protests=count(city2)
gen pr=protests if protests>=130

twoway bar protests date_format, ytitle(Protests) xtitle(Date) xlabel(, format(%dM/CY)) ///
|| scatter protests date_format, mlabel(pr) mlabpos(1) legend(off)
graph export "$dir_descriptive/protest.pdf", replace


/*-------------SHADED AREA PROTESTS BY DATE-----------------------------*/
** with this command I can depict only one shaded area, not multiples
twoway (scatteri 600 `=d(20sep2019)' 600 `=d(29nov2019)', bcolor(gs11) recast(area)  ///
legend(on order(1 "Greta timeline" 2 "Protests"))) ///
(bar protests date_format, clpattern(solid)), xlabel(, format(%dM/CY)) ///
|| scatter protests date_format, mlabel(pr) mlabpos(1) ///
title("Number of protests") xtitle("Year") ytitle("Protests")
graph export "$dir_descriptive/protests_shaded_area.pdf", replace


*****************************Try
twoway (scatteri 600 `=d(20sep2019)' 600 `=d(29nov2019)', bcolor(gs11) recast(area)  ///
legend(on order(1 "Time" 2 "Protests"))) ///
(bar protests date_format, clpattern(solid)), xlabel(, format(%dM/CY)) ///
|| scatter protests date_format, mlabel(pr) mlabpos(1) 


*****try multiple areas

 twoway ///
(scatteri 600 `=d(20sep2019)' 600 `=d(29nov2019)', bcolor(gs11) recast(area)  || ///
	(scatteri 600 `=d(2dec2019)', 600 `=d(13dec2019)', bcolor(gs11) recast(area)   ///
legend(on order(1 "Time" 2 "Protests")))) ///
(bar protests date_format, clpattern(solid)), xlabel(, format(%dM/CY)) 
|| scatter protests date_format, mlabel(pr) mlabpos(1) 

*----------------Shaded area using BGSHADE------------------------------*
* it works with multiple areas but the area between two lines is not shaded
generate date_text2 = string(date_format, "%d")

ssc install bgshade
gen GT = 0
replace GT = 1 if date_text2 == "16aug2019"
replace GT = 1 if date_text2 == "23aug2019"
replace GT = 1 if date_text2 == "27sep2019"
drop GT


bgshade date_format, shaders(GT day) legend   ///
sstyle(noextend lcolor("255 0 0" green blue) lpattern(_ - -_)) ///
twoway(bar protests date_format, title("Number of Protests") lcolor(navy) ///
  legend(cols(1) order(3 1 2 "Greta")))

  
  
  *---------------------------------
  


  
  
**

twoway (scatteri ///
	 600 `=d(20sep2019)' 600 `=d(29nov2019)', bcolor(gs11) recast(area))///
	 (scatteri ///
	 600 `=d(2dec2019)', 600 `=d(13dec2019)', bcolor(gs11) recast(area)) ///
	legend(on order(1 "Time" 2 "Protests"))) ///
(bar protests date_format, clpattern(solid)), xlabel(, format(%dM/CY)) ///
|| scatter protests date_format, mlabel(pr) mlabpos(1) 










/*-------------GRAPH BY STATE-----------------------------*/

clear
cd "W:\EoCC\analysis\output\temp"
use appended_cleaned_geocoded_map.dta
//clean state name because some appear in German some in English
replace g_state = "Nordrhein-Westfalen" if g_state == "North Rhine-Westphalia" 
replace g_state = "Sachsen" if g_state == "Saxony" 
replace g_state = "Bayern" if g_state == "Bavaria" 
replace g_state = "Niedersachsen" if g_state == "Lower Saxony" 
replace g_state = "Rheinland-Pfalz" if g_state == "Rhineland-Palatinate" 
replace g_state = "Thüringen" if g_state == "Thuringia" 
replace g_state = "Hessen" if g_state == "Hesse" 
replace g_state = "Sachsen-Anhalt" if g_state == "Saxony-Anhalt" 
replace g_state = "Bremen" if g_state == "Free Hanseatic City of Bremen" 
replace g_state = "Mecklenburg-Vorpommern" if g_state == "Mecklenburg-Western Pomerania" 
replace g_state = "Thüringen" if g_state == "Free Thuringia" 


bysort g_state: egen protests2=count(g_state)
*gen pr2=protests2 if protests2>=100   //only if i want the number of protests above 100
encode g_state, gen(State)

twoway (bar protests2 State), ytitle(Protests) xlabel(#20, labsize(vsmall) angle(forty_five) valuelabel alternate) ///
|| scatter protests2 State, mlabel(protests2) mlabpos(1) legend(off) ///
title("Number of protests by state", size(*0.7))

graph export "$dir_descriptive/protests_by_state.pdf", replace


		