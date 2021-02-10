	global path   	   			"W:\EoCC\analysis"
	global data_source			"$path/data/source"
	global graphs_paper			"$path\output\graphs\descriptive"


	use "$data_source/gesis/ZA7599_v1-0-0.dta/ZA7599_v1-0-0.dta", clear
	
	
	
	* important issue
	qui gen environment = cond(V9==28|V10==28,1,0)
	order environment
	
	* generate date
	qui tostring V4 V5, gen(month week)
	qui gen year = "2019"
	qui gen date_s = week+"-"+year
	order date_s
	qui gen date = weekly(date_s, "WY")
	format date %tw
	order date
	
	* greens support
	qui gen greens = cond(V12==6,1,0)
	
	

	collapse (mean) environment greens, by(date)
	
	qui replace environment = environment *100
	qui replace greens = greens *100
	
	line environment date, color(navy) || ///
		scatter environment date, m(o)  color(navy) ///
		legend(off)  ///
		scheme(s1mono) plotregion(color(white)) ///
		ytitle("Environment an important issue [in %]") xtitle("Date") ///
		tlabel(2019w1 (9) 2019w50, format(%twm) ) ///
		tmtick(2019w5 (9) 2019w52)
	
	graph export "$graphs_paper/greta_cons_gesis_env_issue_2019.pdf", as(pdf) replace


	
	
	// long-term evolution of variable
	use "$data_source/gesis/ZA2391_v12-0-0.dta/ZA2391_v12-0-0.dta", clear
	
	keep if v4 > 1999
	
	* important issue
	qui gen environment = cond(v33==15|v34==15,1,0)
	order environment
	
	* generate date
	qui tostring v3 v4, gen(month year)
	qui gen date_s = month+"-"+year
	order date_s
	qui gen date = monthly(date_s, "MY")
	format date %tm
	order date
	
	
	collapse (mean) environment , by(date)
	
	qui replace environment = environment *100
	
	
	qui gen temp_l = 0 
	qui gen temp_h = 50
	
	
	twoway rarea temp_l temp_h date if date >= tm(2019m1), color(forest_green%40) lcolor(navy%0) || ///
		line environment date, color(black)  ///
		legend(off)  ///
		scheme(s1mono) plotregion(color(white)) ///
		ytitle("") xtitle("") ylabel(,nolabel noticks)  ///
		tlabel(2000m1 2005m1 2010m1 2015m1, format(%tmCY) labs(vlarge)) ///
		tmtick(2000m1(12)2020m1)
	graph export "$graphs_paper/greta_cons_gesis_env_issue_2000-2019.pdf", as(pdf) replace	
		
	
	