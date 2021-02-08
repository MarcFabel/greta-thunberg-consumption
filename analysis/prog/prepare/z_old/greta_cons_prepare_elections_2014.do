// prepare 2014 election data


	global path   	   			"W:\EoCC\analysis"	
	global data_temp			"$path/data/temp"
	global election_source		"$path/data/source/elections/elections_2014"
	global election_intermed	"$path/data/intermediate/elections"
	global election_source_19	"$path/data/source/elections"



	
	
	
********************************************************************************
*	PREPARE 2014
********************************************************************************	
	
	
	
	
// EU **************************************************************************
	
	 import excel "$election_source\elections_eu_2014_ags5.xlsx", sheet("14211-01-03-4") clear

	* rename variables
	qui rename A ags
	qui rename B ags_name
	qui rename C eligibile
	qui rename D voter_turnout
	qui rename E valid
	qui rename F union
	qui rename G spd
	qui rename H the_greens
	qui rename I fdp
	qui rename J the_left
	qui rename K afd
	qui rename L others
	
	* drop header & footer
	qui gen temp = _n 
	keep if temp >9
	keep if temp<546
	drop temp
	
	* correct hamburg and berlin
	qui replace ags = "02000" if ags == "02"
	qui replace ags = "11000" if ags == "11"
	
	
	* keep only ags5
	keep if inrange(length(ags),5,5)
	qui gen ags5 = substr(ags,1,5)
	order ags5
	drop ags
	
	* drop irrelevant rows
	drop if voter_turnout == "-"
	
	* corect for district reforms Niedersachsen (03XXX)
	 qui replace ags5 = "03159" if ags5 == "03156"  //Osterode im Harz -> Göttingen
	 qui replace ags5 = "03159" if ags5 == "03152"
	 drop voter_turnout	// has to be calculated again, as I have to aggregate
	 ds ags5, not
	 destring `r(varlist)' , replace
	 ds ags*, not
	 collapse (sum) `r(varlist)', by(ags5)
	 
	 * define outcomes as fractions
	 qui ds ags5 eligibile valid, not
	 foreach var of varlist `r(varlist)' {
		qui replace `var' = `var'/valid *100
	 } 
	 
	 * voter_turnout
	 qui gen voter_turnout = valid / eligibile *100
	 drop eligibile valid
	 
	 * export
	 qui gen election = "eu"
	 qui save "$data_temp/greta_cons_elections_2014_ags5.dta", replace
	 
	 
	 
	 
// Brandenburg *****************************************************************
	import excel "$election_source\elections_brandenburg_2014_ags5.xlsx", sheet("14342-01-03-4") clear

	 
	 * rename variables
	qui rename A ags
	qui rename B ags_name
	qui rename C eligibile
	qui rename D voter_turnout
	qui rename E valid
	qui rename F union
	qui rename G spd
	qui rename H the_greens
	qui rename I fdp
	qui rename J the_left
	qui rename K afd
	qui rename L others
	
	* drop header & footer
	qui gen temp = _n 
	order temp
	keep if temp >8
	keep if temp<27
	drop temp
	
	
	* keep only ags5
	keep if inrange(length(ags),5,5)
	qui gen ags5 = substr(ags,1,5)
	order ags5
	drop ags
	

	* encode 
	 ds ags* voter_turnout, not
	 destring `r(varlist)' , replace
	 
	 
	 * correct for district reforms (12051-12054)
	 
	 
	 * define outcomes as fractions
	 qui ds ags* eligibile valid voter_turnout, not
	 foreach var of varlist `r(varlist)' {
		qui replace `var' = `var'/valid *100
	 } 
	 
	 
	 
	 * voter_turnout
	 drop voter_turnout	// harmonize across samples
	 qui gen voter_turnout = valid / eligibile *100
	 drop eligibile valid ags_name

	 *export
	 qui gen election = "brandenburg"
	 qui append using "$data_temp/greta_cons_elections_2014_ags5.dta"
	 qui save "$data_temp/greta_cons_elections_2014_ags5.dta", replace
	
	
	
	
	
	
// Sachsen **************************************************************************
	
	import excel "$election_source\elections_sachsen_2014_ags5.xlsx", sheet("14344-01-03-4") clear

	* rename variables
	qui rename A ags
	qui rename B ags_name
	qui rename C eligibile
	qui rename D voter_turnout
	qui rename E valid
	qui rename F union
	qui rename G spd
	qui rename H the_greens
	qui rename I fdp
	qui rename J the_left
	qui rename K afd
	qui rename L others
	
	* drop header & footer
	qui gen temp = _n 
	order temp
	keep if temp >9
	keep if temp<57
	drop temp
	
	
	* keep only ags5
	keep if inrange(length(ags),5,5)
	qui gen ags5 = substr(ags,1,5)
	order ags5
	drop ags
	
	* drop irrelevant rows
	drop if voter_turnout == "-"
	
	* encode
	 drop voter_turnout	// has to be calculated again, harmonization
	 ds ags*, not
	 destring `r(varlist)' , replace
	 
	 
	 * define outcomes as fractions
	 qui ds ags* eligibile valid, not
	 foreach var of varlist `r(varlist)' {
		qui replace `var' = `var'/valid *100
	 } 
	 
	 * voter_turnout
	 qui gen voter_turnout = valid / eligibile *100
	 drop eligibile valid ags_name
	 
	 * export
	 qui gen election = "saxony"
	 qui append using "$data_temp/greta_cons_elections_2014_ags5.dta"
	 qui save "$data_temp/greta_cons_elections_2014_ags5.dta", replace
	
	
	
// Thuringia **************************************************************************
	
	import excel "$election_source\elections_thüringen_2014_ags5.xlsx", sheet("14346-01-03-4") clear
	
	* rename variables
	qui rename A ags
	qui rename B ags_name
	qui rename C eligibile
	qui rename D voter_turnout
	qui rename E valid
	qui rename F union
	qui rename G spd
	qui rename H the_greens
	qui rename I fdp
	qui rename J the_left
	qui rename K afd
	qui rename L others
	
	* drop header & footer
	qui gen temp = _n 
	order temp
	keep if temp >8
	keep if temp<32
	drop temp
	
	
	* keep only ags5
	keep if inrange(length(ags),5,5)
	qui gen ags5 = substr(ags,1,5)
	order ags5
	drop ags
	
	* drop irrelevant rows
	drop if voter_turnout == "-"
	
	* encode
	 drop voter_turnout	// has to be calculated again, harmonization
	 ds ags*, not
	 destring `r(varlist)' , replace
	 
	 
	 * define outcomes as fractions
	 qui ds ags* eligibile valid, not
	 foreach var of varlist `r(varlist)' {
		qui replace `var' = `var'/valid *100
	 } 
	 
	 * voter_turnout
	 qui gen voter_turnout = valid / eligibile *100
	 drop eligibile valid ags_name
	 
	 * export
	 qui gen election = "thuringia"
	 qui append using "$data_temp/greta_cons_elections_2014_ags5.dta"
	 
	 
	 
	 * rename variables 
	 qui ds ags5 election, not
	 foreach var of varlist `r(varlist)' {
		qui rename `var' `var'_2014
	 }
	 qui save "$data_temp/greta_cons_elections_2014_ags5.dta", replace	
	 
	 
	
********************************************************************************
*	PREPARE 2019
********************************************************************************


	* brandenburg 
	import excel "$election_source_19/landtag_brandenburg_2019/elections_brandenburg_2019_ags5.xlsx", sheet("14342-01-03-4") clear

	
	* rename variables
	qui rename A ags
	qui rename B ags_name
	qui rename C eligibile
	qui rename D voter_turnout
	qui rename E valid
	qui rename F union
	qui rename G spd
	qui rename H the_greens
	qui rename I fdp
	qui rename J the_left
	qui rename K afd
	qui rename L others
	
	* drop header & footer
	qui gen temp = _n 
	order temp
	keep if temp >8
	keep if temp<27
	drop temp
	
	
	* keep only ags5
	keep if inrange(length(ags),5,5)
	qui gen ags5 = substr(ags,1,5)
	order ags5
	drop ags
	
	* drop irrelevant rows
	drop if voter_turnout == "-"
	
	* encode
	 drop voter_turnout	// has to be calculated again, harmonization
	 ds ags*, not
	 destring `r(varlist)' , replace
	 
	 
	 * define outcomes as fractions
	 qui ds ags* eligibile valid, not
	 foreach var of varlist `r(varlist)' {
		qui replace `var' = `var'/valid *100
	 } 
	 
	 * voter_turnout
	 qui gen voter_turnout = valid / eligibile *100
	 drop eligibile valid ags_name
	 
	 * export
	 qui gen election = "brandenburg"
	qui save "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta", replace
	
	
	

	* EU ***********************************************************************
	import delimited "$data_elections/election_eu2019_ags5_prepared.csv", stringcols(1) clear
	qui gen election = "eu"
	qui append using "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta"
	qui save "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta", replace
	
	
	* Saxony  ***********************************************************************
	import delimited "$data_elections/election_sachsen2019_ag5s_prepared.csv", stringcols(1) clear
	qui gen election = "saxony"
	qui append using "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta"
	qui save "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta", replace
	

	
	* thuringia  ***********************************************************************
	import delimited "W:\EoCC\analysis\data\intermediate\elections\election_thueringen2019_ags5_prepared.csv", stringcols(1) clear
	qui gen election = "thuringia"
	qui append using "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta"
	qui save "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta", replace
	
	
	
	* rename variables
	 qui ds ags5 election, not
	 foreach var of varlist `r(varlist)' {
		qui rename `var' `var'_2019
	 }
	 

	 
********************************************************************************
*	Combine two data sets
********************************************************************************	 
	 
	 * merge with 2014
	 merge 1:1 ags5 election using "$data_temp/greta_cons_elections_2014_ags5.dta", keep(match)
	 drop _merge
	 
	 * generate first difference
	 foreach var in "union" "spd" "the_greens" "the_left" "afd" "fdp" "others" "voter_turnout" {
		qui gen fd_`var' = `var'_2019 - `var'_2014
		drop `var'_2014
		qui rename `var'_2019 `var'
	 }
	 
	 
	 
	  order ags5 election
	  qui save "$data_final/elections/greta_cons_elections_ags5_prepared.dta", replace
	 qui erase "$data_final/elections/greta_cons_elections_2019_ags5_prepared.dta"
	 
	 
	
	 
	
	
