// import degree urbanization
	global path   	   				"W:\EoCC\analysis"	
	global data_temp				"$path/data/temp"

* read in
import excel "W:\EoCC\analysis\data\source\population\degree_urbanization_ags8_2018.xlsx", sheet("Onlineprodukt_Gemeinden_311218") cellrange(A4:AN16086) firstrow allstring clear

qui drop if insgesamt == ""

qui gen ags8 = Land + RB + Kreis + Gem

qui encode T, gen(degree_urbanization)
qui rename H name
keep ags degree


* drop duplicates
duplicates drop

qui save "$data_temp/greta_cons_degree_urbanization_ags8", replace