// Descriptive figures background

	clear all 
	set more off
	set matsize 11000
	
	*paths
	global path   	   			"W:\EoCC\analysis"	
	global data_final			"$path/data/final"
	global data_temp			"$path/data/temp"
	global graphs_paper			"$path\output\graphs\descriptive"
	
	
	
	
	
********************************************************************************
*	1) print media graph
********************************************************************************	

	import delimited "$data_temp\twitter_print_media\greta_cons_fff_ratio_2019_with_ma.csv", clear
	qui rename date date_s
	
	qui gen date = date(date_s, "YMD")
	format date %td
	drop date_s
	
	
	line art_fff_ratio date, color(gs12) || ///
		line art_fff_ratio_ma3 date, color(navy) ///
		scheme(s1mono) plotregion(color(white)) ///
		legend(label(1 "unsmoothed") label(2 "smoothed") pos(11) ring(0) col(1) ///
		region(color(none)) size(small))  ///
		ytitle("Share articles covering FFF [per 1,000]") xtitle("Date") ///
		tlabel(01jan2019 (61) 1dec2019, format(%tdm) ) ///
		tmtick(01feb2019 (61) 3dec2019)
	graph export "$graphs_paper/greta_cons_fff_print_media_articles_2019.pdf", as(pdf) replace
	
	
	
	
********************************************************************************
*	2) Greta Thunberg Twitter
********************************************************************************

	* the data is the output from a .py file, in which I upsampled to the weekly level
	import delimited "$data_temp\twitter_print_media\greta_cons_greta_2019_weekly_favorites_retweets.csv", clear

	qui rename date date_s
	qui gen date = date(date_s, "YMD")
	format date %td
	drop date_s

	gen weekly_data = wofd(date)
	format weekly_data %tw
	
	line favorites weekly_data, color(maroon) yaxis(1) || ///
		line retweets weekly_data,color(navy) yaxis(2) ///
		legend(off)  ///
		scheme(s1mono) plotregion(color(white)) ///
		ytitle("Favorites [in 1,000]", axis(1) color(maroon)) xtitle("Date") ///
		ylabel(, axis(1) labcolor(maroon)) /// 
		ytitle("Retweets [in 1,000]", axis(2) color(navy)) ///
		ylabel(,  axis(2) labcolor(navy)) /// 
		tlabel(2019w1 (9) 2019w50, format(%twm) ) ///
		tmtick(2019w5 (9) 2019w52)
	graph export "$graphs_paper/greta_cons_twitter_gt_favorites_retweets_2019.pdf", as(pdf) replace




