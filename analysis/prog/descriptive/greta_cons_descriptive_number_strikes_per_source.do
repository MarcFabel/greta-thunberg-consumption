	global data_final			"$path/data/final"
	global graphs_paper			"$path\output\graphs\descriptive"


	import delimited "$data_final\fff_strikes\greta_cons_fff_all_strikes_ags5_wkr_teralyticsid.csv", delimiter(";") encoding(UTF-8) stringcols(1 2 3 5 14 16) clear 

	qui gen date_s = day +"/"+ month +"/"+ year
	qui gen date = date(date_s, "DMY")
	order date teralytics_id
	format date %td
	drop day month year date_s
	
	keep date source
	
	encode source, gen(source_s)
	drop source
	rename source_s source
	
	qui gen count = 1
	qui collapse (sum) count, by(date source)
	

	twoway line count date if source == 2, color(maroon)  || ///
		line count date if source == 3, color(navy) || ///
		scatter count date if source == 1, color(forest_green) m(Oh) ///
		xtitle("Date") ytitle("Number of strikes") ///
		scheme(s1mono) plotregion(color(white)) ///
		tlabel(01jan2019 (61) 1dec2019, format(%tdm) ) ///
		tmtick(01feb2019 (61) 3dec2019) ///
		legend(label(1 "authorities") label(2 "social media") label(3 "fff website") pos(11) ring(0) col(1) ///
		 order(1 2 3) size(small)) || ///
			pcarrowi 150 21600 120 21620 (11) "15.03." , color(black) || ///
			pcarrowi 170 21670 140 21690 (11) "24.05." , color(black) || ///
			pcarrowi 260 21789 230 21809 (11) "20.09." , color(black) || ///
			pcarrowi 216 21859 186 21879 (11) "29.11." , color(black)
			
	graph export "$graphs_paper/greta_cons_number_strikes_per_source.pdf", as(pdf) replace
		
		

/*	
		
		21623 15 mar 
		21693 24 may
		21812 20 sep
		21882 29 nov