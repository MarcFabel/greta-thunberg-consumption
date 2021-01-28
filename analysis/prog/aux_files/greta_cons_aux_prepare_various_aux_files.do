	global path   	   			"W:\EoCC\analysis"	
	global data_final			"$path/data/final"
	global data_temp			"$path/data/temp"
	global data_pop				"$path/data/intermediate/population"
	global regional_database 	"$path/data/intermediate/regional_database"


	
	
	
	
	
	// generate travel distance table ******************************************
	use "$data_final/greta_cons_teralytics_prepared.dta", clear
	
	keep startid endid tripdistancekm
	duplicates drop 
	
	qui save "$data_temp/greta_cons_table_distance_start_end.dta", replace
	
	
	
	// generate conversion table teralytics_id ags_5 ***************************
	use "$data_final/greta_cons_teralytics_prepared.dta", clear
	keep if date == td(01jan2019)
	keep start_aks startid
	
	qui gen ags5  = string(start_aks,"%05.0f")
	drop start_aks
	rename startid teralytics_id
	duplicates drop
	qui save "$data_temp/greta_cons_conversion_table_teralytics_ags5.dta", replace
	
	
	
	// import population data **************************************************
	import delimited "$data_pop/population_ags5_prepared.csv", encoding(UTF-16LE) stringcols(1) clear
	qui egen pop_10_34 = rowtotal(pop_10_14_t pop_15_17_t pop_18_19_t pop_20_24_t pop_25_29_t pop_30_34_t)
	qui egen pop_15_24 = rowtotal(pop_15_17_t pop_18_19_t pop_20_24_t)
	keep ags ags_name pop_t pop_10_34 pop_15_24
	qui save "$data_final/population/greta_cons_population_ags5_prepared.dta", replace
	
	
	
	// import regional data base ***********************************************
	 import delimited "$regional_database/greta_cons_regional_controls.csv", encoding(UTF-8) stringcols(1) clear 
	 encode pop_density_cat, gen(pop_density_cat_num)
	 drop ags_name pop_density_cat
	 qui rename pop_density_cat_num pop_density_cat
	 rename ags ags5
	 qui save "$data_final/regional_database/greta_cons_regional_database_ags5_prepared.dta", replace


	// conversion table ags5 -> ags8 ***********************************************
	use "$regional_intermediate/regional_variables_ags8", clear
	keep ags8 ags5 ags8_name
	qui save "$data_temp/greta_cons_conversion_ags8_ags5_2019.dta", replace
	