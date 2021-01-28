// prepare regional controls on ags8 

	global regional_source_ags8 	"G:\Internes\Mitarbeiter\DLR\4 - manipulated datasets\Master Dataset"
	global election_source_ags8		"$path/data\intermediate\elections"
	global regional_intermediate 	"$path/data/intermediate/regional_database"
	
	global path   	   			"W:\EoCC\analysis"
	global data_temp			"$path/data/temp"


	
	
********************************************************************************
*	EU
********************************************************************************
	
	
	* open electoral outcomes and combine with regional controls
	import delimited "$election_source_ags8\election_eu2019_ags8_prepared.csv", stringcols(1) clear
	qui gen election = "eu"
	qui save "$data_temp/greta_cons_elections_ags8.dta", replace
	
	
	* import delimited "$election_source_ags8\election_eu2019_ags8_prepared.csv", stringcols(1) clear
	 qui rename ags8 AGS
	 merge m:1 AGS using "$regional_source_ags8/Master_Dataset.dta"
	 keep if _merge == 3

	keep voter_turnout-fd_the_greens AGS name  popunder3 - pop25to65 ags_kreis pop_density unemployment_rate ///
	log_IncomeperTP IncomeperCapita log_IncomeperCapita election ///
	residential commercial green agriculture forest ///
	per_young support_ratio

	
	* gen ags
	qui gen ags8 = substr(AGS,1,8)
	order ags8
	qui gen ags5 = substr(ags_kreise,1,5)
	drop AGS ags_kreise
	
	* harmonize variables
	qui egen pop_10_34 = rowtotal(pop10to15 pop15to17 pop18to19 pop20to24 pop25to29 pop30to34)
	qui replace unemployment_rate = unemployment_rate * 100
	qui rename unemployment_rate ue_rate
	qui rename poptotal pop_t
	qui rename name ags8_name
	
	* drop unnecessary variables
	drop popunder3 - popabove75 pop15to65 pop25to65
	
	
	* generate municipality share young people
	bys ags5: egen krs_pop_10_34 = total(pop_10_34)
	qui gen share_munic_pop_10_34 = pop_10_34/krs_pop_10_34
	drop krs_pop_10_34
	
	
	sort ags8
	order ags8 ags5 ags8_name pop_10_34 share pop_t ue_rate pop_density
	
	* correct Hamburg and Berlin
	qui replace ags5 = "02000" if ags5 == "02"
	qui replace ags5 = "11000" if ags5 == "11"
	
	qui save "$regional_intermediate/regional_variables_ags8", replace
	
	
********************************************************************************
*	Brandenburg
********************************************************************************	
	
	* open electoral outcomes and combine with regional controls
	import delimited "$election_source_ags8\election_brandenburg_ags8_prepared.csv", stringcols(1) clear
	qui gen election = "brandenburg"
	 qui rename ags AGS
	 merge m:1 AGS using "$regional_source_ags8/Master_Dataset.dta"
	 keep if _merge == 3

	keep voter_turnout-fd_the_greens AGS name  popunder3 - pop25to65 ags_kreis pop_density unemployment_rate ///
	log_IncomeperTP IncomeperCapita log_IncomeperCapita election ///
	residential commercial green agriculture forest ///
	per_young support_ratio

	
	* gen ags
	qui gen ags8 = substr(AGS,1,8)
	order ags8
	qui gen ags5 = substr(ags_kreise,1,5)
	drop AGS ags_kreise
	
	* harmonize variables
	qui egen pop_10_34 = rowtotal(pop10to15 pop15to17 pop18to19 pop20to24 pop25to29 pop30to34)
	qui replace unemployment_rate = unemployment_rate * 100
	qui rename unemployment_rate ue_rate
	qui rename poptotal pop_t
	qui rename name ags8_name
	
	* drop unnecessary variables
	drop popunder3 - popabove75 pop15to65 pop25to65
	
	
	* generate municipality share young people
	bys ags5: egen krs_pop_10_34 = total(pop_10_34)
	qui gen share_munic_pop_10_34 = pop_10_34/krs_pop_10_34
	drop krs_pop_10_34
	
	sort ags8
	order ags8 ags5 ags8_name pop_10_34 share pop_t ue_rate pop_density
	
	
	qui save "$regional_intermediate/regional_variables_ags8_brandenburg", replace
	
	
	
	
********************************************************************************
*	Saxony
********************************************************************************	
	
	* open electoral outcomes and combine with regional controls
	import delimited "$election_source_ags8\election_sachsen_ags8_prepared.csv", stringcols(1) clear
	qui gen election = "saxony"
	 qui rename ags AGS
	 merge m:1 AGS using "$regional_source_ags8/Master_Dataset.dta"
	 keep if _merge == 3

	keep voter_turnout-fd_the_greens AGS name  popunder3 - pop25to65 ags_kreis pop_density unemployment_rate ///
	log_IncomeperTP IncomeperCapita log_IncomeperCapita election ///
	residential commercial green agriculture forest ///
	per_young support_ratio

	
	* gen ags
	qui gen ags8 = substr(AGS,1,8)
	order ags8
	qui gen ags5 = substr(ags_kreise,1,5)
	drop AGS ags_kreise
	
	* harmonize variables
	qui egen pop_10_34 = rowtotal(pop10to15 pop15to17 pop18to19 pop20to24 pop25to29 pop30to34)
	qui replace unemployment_rate = unemployment_rate * 100
	qui rename unemployment_rate ue_rate
	qui rename poptotal pop_t
	qui rename name ags8_name
	
	* drop unnecessary variables
	drop popunder3 - popabove75 pop15to65 pop25to65
	
	
	* generate municipality share young people
	bys ags5: egen krs_pop_10_34 = total(pop_10_34)
	qui gen share_munic_pop_10_34 = pop_10_34/krs_pop_10_34
	drop krs_pop_10_34
	
	sort ags8
	order ags8 ags5 ags8_name pop_10_34 share pop_t ue_rate pop_density
	
	qui save "$regional_intermediate/regional_variables_ags8_saxony", replace	
	
	
	
********************************************************************************
*	Thuringia
********************************************************************************	
	
	* open electoral outcomes and combine with regional controls
	import delimited "$election_source_ags8\election_thueringen_ags8_prepared.csv", stringcols(1) clear
	qui gen election = "thuringia"
	 qui rename ags AGS
	 merge m:1 AGS using "$regional_source_ags8/Master_Dataset.dta"
	 keep if _merge == 3

	keep voter_turnout-fd_the_greens AGS name  popunder3 - pop25to65 ags_kreis pop_density unemployment_rate ///
	log_IncomeperTP IncomeperCapita log_IncomeperCapita election ///
	residential commercial green agriculture forest ///
	per_young support_ratio

	
	* gen ags
	qui gen ags8 = substr(AGS,1,8)
	order ags8
	qui gen ags5 = substr(ags_kreise,1,5)
	drop AGS ags_kreise
	
	* harmonize variables
	qui egen pop_10_34 = rowtotal(pop10to15 pop15to17 pop18to19 pop20to24 pop25to29 pop30to34)
	qui replace unemployment_rate = unemployment_rate * 100
	qui rename unemployment_rate ue_rate
	qui rename poptotal pop_t
	qui rename name ags8_name
	
	* drop unnecessary variables
	drop popunder3 - popabove75 pop15to65 pop25to65
	
	
	* generate municipality share young people
	bys ags5: egen krs_pop_10_34 = total(pop_10_34)
	qui gen share_munic_pop_10_34 = pop_10_34/krs_pop_10_34
	drop krs_pop_10_34
	
	sort ags8
	order ags8 ags5 ags8_name pop_10_34 share pop_t ue_rate pop_density
	
	qui save "$regional_intermediate/regional_variables_ags8_thuringia", replace		
	
	
	
