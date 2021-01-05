// ***************************** PREAMBLE***************************************
*	Created: 05.01.2021
*	Author: Marc Fabel
*	
*	Description:
*		Prepare Ordnungsamt Strike Database
*
*	Input:
*		Data.xlsx										[source]				raw Data from Franziska Wintersteller\FFF	
*		sub_dofiles		
*
*	Output:
*		greta_cons_fff_strikes_ordnungsamt_geocoordinates_all_strikes.csv				[intermediate]
*
* API1: 81c48b3e0c2247819f75f1c975e1f026 (ifo)
* API2: 66e8c8a686e64fa5803fa4958e006ed3 (cofc)


	cap log close
	set more off
	clear all 
	set maxvar 10000


	global path 				"W:\EoCC\analysis\data"
	global strike_source 		"G:\Praktikanten\HIWIS\Wintersteller\FFF"
	global strike_dofiles		"W:\EoCC\analysis\prog\prepare\strikes_subfiles"
	global temp 				"$path\temp/"
	global strike_output		"$path\intermediate\fff_strikes"
	
	
	
	
********************************************************************************
*	Prepare data for geocoding
********************************************************************************	
	
	*open 
	import excel "$strike_source/Data.xlsx", sheet("Tabelle1") firstrow clear
	
	*comment column
	gen str comment=""
	replace comment = "marsch vom deich" if municipality == "juist" & location == "marsch vom deich"
	replace comment = "radkorso im kreis" if municipality == "karlsruhe" & location == "radkorso im kreis"
	replace comment = "an kreisverkehren" if municipality == "melle" & location == "an kreisverkehren"
	replace comment = "an ampeln" if municipality == "melle" & location == "an ampeln"
	
	
	* make string variables
	gen str daystr2 = string(day, "%02.0f")
	gen str monthstr2 = string(month, "%02.0f")
	gen str yearstr4 = string(year, "%04.0f")
	gen str5 plzstr = string(plz, "%05.0f")
	
	drop day
	drop month 
	drop year
	drop plz
	
	rename daystr2 day  
	rename monthstr2 month
	rename yearstr4 year
	
	
	* replace wrong dates
	replace day = "14" if municipality == "stuttgart" & day == "15" & month == "02" & year == "2019"
	replace day = "21" if municipality == "stuttgart" & day == "22" & month == "02" & year == "2019"
	
	
	* match location of strikes with locations of ohter inputs
	do "$strike_dofiles/match_locations_social_media.do"
	
	
	*If location or municipality is missing, but necessary to assign the strike to a electoral district:
	* use the location/municipality where the municipality/county had the most strikes during the observation period.
	replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & location == ""
	replace location = "Marktplatz" if municipality == "stuttgart" & location == ""
	replace municipality = "mainz" if county == "mainz-bingen" & municipality == ""
	replace municipality = "Zwickau" if county == "zwickau" & municipality == ""
	replace municipality = "Fürth" if county == "fuerth" & municipality == ""
	replace municipality = "Gotha" if county == "gotha" & municipality == ""
	replace municipality = "Sonneberg" if county == "sonneberg" & municipality == ""
	
	
	* change typos and teh like
	replace municipality=subinstr(municipality,"i b","im breisgau",.)
	replace municipality=subinstr(municipality,"a.t.w.","am teutoburger wald",.)
	replace municipality=subinstr(municipality,"leutkirch","leutkirch im allgaeu",.)
	replace municipality=subinstr(municipality,"lutherstadt wittenberg","wittenberg, lutherstadt",.)
	replace municipality=subinstr(municipality,"gross-bieberau","groß-bieberau",.)
	replace municipality=subinstr(municipality,"gros-gerau","gross-gerau",.)
	replace municipality=subinstr(municipality,"bad winsheim","bad windsheim",.)
	replace county=subinstr(county,"gros-gerau","gross-gerau",.)
	replace county=subinstr(county,"neustadt an der aisch-bad winsheim","neustadt an der aisch - bad windsheim",.)
	replace state=subinstr(state,"thueringen","thuringia",.)
	replace county = "karlsruhe" if municipality == "karlsruhe"
	//delete -stadt
	replace county=subinstr(county,"-stadt","",.)
	replace county=subinstr(county," - stadt","",.)
	
	
	
	// Change missing or not matching postcodes 
	*(which help of https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/_inhalt.html)
	replace plzstr = "57610" if municipality == "altenkirchen (westerwald)"
	replace plzstr= "63741" if municipality == "aschaffenburg"
	replace plzstr = "86150" if municipality == "augsburg"
	replace plzstr = "55545" if municipality == "bad kreuznach"
	replace plzstr = "97980" if municipality == "bad mergentheim"
	replace plzstr = "76530" if municipality == "baden baden"
	replace plzstr = "72336" if municipality == "balingen"
	replace plzstr = "06766" if municipality == "bitterfeld-wolfen"
	replace plzstr = "09111" if municipality == "chemnitz"
	replace plzstr = "06844" if municipality == "dessau-roßlau"
	replace plzstr = "99084" if municipality == "erfurt"
	replace plzstr = "67227" if municipality == "frankenthal (pfalz)"
	replace plzstr = "79098" if municipality == "freiburg im breisgau"
	replace plzstr = "85354" if municipality == "freising"
	replace plzstr = "88045" if municipality == "friedrichshafen"
	replace plzstr = "90744" if municipality == "fuerth"
	replace plzstr = "07545" if municipality == "gera"
	replace plzstr = "98693" if municipality == "ilmenau"
	replace plzstr = "56068" if municipality == "koblenz"
	replace plzstr = "61462" if municipality == "koenigstein im taunus"
	replace plzstr = "77933" if municipality == "lahr/schwarzwald"
	replace plzstr = "88299" if municipality == "leutkirch im allgaeu"
	replace plzstr = "67059" if municipality == "ludwigshafen"
	replace plzstr = "23552" if municipality == "luebeck"
	replace plzstr = "06886" if municipality == "wittenberg, lutherstadt" 
	replace plzstr = "55116" if municipality == "mainz" 
	replace plzstr = "22846" if municipality == "norderstedt"
	replace plzstr = "99734" if municipality == "nordhausen"
	replace plzstr = "66953" if municipality == "pirmasens"
	replace plzstr = "54290" if municipality == "trier"
	replace plzstr = "29308" if municipality == "winsen (aller)"
	
	replace plzstr = "90762" if municipality == "fuerth" & location == "schwabacher straße"
	replace plzstr = "30169" if municipality == "hannover" & address == "friederikenplatz"
	replace plzstr = "30167" if municipality == "hannover" & address == "georgengarten"
	replace plzstr = "30173" if municipality == "hannover" & address == "hildesheimer straße"
	replace plzstr = "76189" if municipality == "karlsruhe" & address == "rudolf-freytag-straße 7"
	replace plzstr = "76189" if municipality == "karlsruhe" & address == "rudolf-freytag-straße 8"
	replace plzstr = "76189" if municipality == "karlsruhe" & address == "rudolf-freytag-straße 9"
	replace plzstr = "76189" if municipality == "karlsruhe" & address == "rudolf-freytag-straße 6"
	replace plzstr = "04107" if municipality == "leipzig" & location == "Willhelm-Leuschner-Platz"
	replace plzstr = "04105" if municipality == "leipzig" & location == "gerberstrasse"
	replace plzstr = "26122" if municipality == "oldenburg" & location == "bahnhofsplatz"
	replace plzstr = "08056" if municipality == "Zwickau" & location == "Leipziger Straße"


	// Change locations or addresses if they are not related to any street information
	do "$strike_dofiles/change_addresses_of_strikes_ordnungsämter.do"

	// Delete locations or addresses if they are not related to any street information or if both variables are given, but only one is required
	do "$strike_dofiles/delete_addresses_of_strikes_ordnungsämter_social_media.do"


	// combine all addresss information
	gen str1 space=" "
	egen street=concat(location space address)
	egen fulladdress=concat(location space address space plzstr space municipality space county space state)
	drop space
	
	
	drop if fulladdress == ".  saarpfalz-kreis saarland" // not enough information
	
	*qui save "$temp/greta_cons_strikes_ordnungsamt_all_strikes.dta", replace
	
	
	
	
********************************************************************************
*	Geo-Coding
********************************************************************************	
	
	*use "$temp/greta_cons_strikes_ordnungsamt_all_strikes.dta", clear
	keep fulladdress municipality plzstr street
	duplicates drop

	opencagegeo, key (81c48b3e0c2247819f75f1c975e1f026) fulladdress (fulladdress) countrycode (DE) replace

	*qui save "$temp/temp.dta", replace
	*use "$temp/temp.dta", clear
	
	
	
	// correct manually ********************************************************
	capture program drop coordinates
	program define coordinates
		replace g_lat = "`3'" if municipality == "`1'" & g_qua == `2'
		replace g_lon = "`4'" if municipality == "`1'" & g_qua == `2'
		replace g_quality = 8 if municipality == "`1'" & g_qua == `2'
	end
	
	* not found g_quality == 0
	coordinates "pforzheim" 0  "48.891003" "8.702268"
	coordinates "bruehl" 0  "49.389059" "8.530634"
	
	* state g_quality == 2
	coordinates "zella-mehlis" 2 	"50.656317" "10.664349"
	coordinates "mölln" 2  			"53.629415" "10.690762"
	coordinates "geesthacht" 2  	"53.433383" "10.369790"
	coordinates "wentorf " 2  		"53.493791" "10.253471"
	coordinates "boppard" 2  		"50.231818" "7.586415"
	
	* county g_quality == 3
	coordinates "aschaffenburg" 3	"49.973837" "9.144532"
	coordinates "mainz"			3	"49.999469" "8.273347"
	coordinates "bad wildungen" 3 	"51.119732" "9.121295"
	coordinates "koenigstein im taunus" 3 "50.182557" "8.465762"
	
	* city g_quality == 4 (only where there is more than 1 teraltics id)
	capture program drop coordinates2
	program define coordinates2 // alows to include additional condition
		replace g_lat = "`3'" if municipality == "`1'" & g_qua == `2' & street == "`5'"
		replace g_lon = "`4'" if municipality == "`1'" & g_qua == `2' & street == "`5'"
		replace g_quality = 8 if municipality == "`1'" & g_qua == `2' & street == "`5'"
	end
	coordinates2 "hannover" 	4	"52.371307" "9.736590" "karmarschstraße"
	coordinates2 "hannover" 	4	"52.372588" "9.741115" "opernplatz"
	coordinates2 "hannover" 	4	"52.380904" "9.714598" "jägerstraße"
	coordinates2 "hannover" 	4	"52.335784" "9.771541" "hildesheimer straße"
	coordinates2 "hannover" 	4	"52.372588" "9.741115" "ständehausstraße"
	coordinates2 "hannover" 	4	"52.375856" "9.740757" "ernst-august-platz"
	coordinates2 "hannover" 	4	"52.367659" "9.738996" "trammplatz"
	coordinates2 "hannover" 	4	"52.370255" "9.741761" "georgsplatz"
	coordinates2 "hannover" 	4	"52.368943" "9.732209" "friederikenplatz"
	coordinates2 "ingolstadt" 	4 	"48.763658" "11.424788" "altstadt"

	
	* other changes made by Lina
	replace g_lat = "50.298193" if municipality == "bad camberg" & plzstr == "65520" & street == "marktplatz"
	replace g_lon = "8.269698" if municipality == "bad camberg" & plzstr == "65520" & street == "marktplatz"
	replace g_quality = 8 if municipality == "bad camberg" & plzstr == "65520" & street == "marktplatz"
	replace g_lat = "52.319911" if municipality == "bad essen" & plzstr == "49152" & street == "lindenstrasse"
	replace g_lon = "8.343521" if municipality == "bad essen" & plzstr == "49152" & street == "lindenstrasse"
	replace g_quality = 8 if municipality == "bad essen" & plzstr == "49152" & street == "lindenstrasse"
	replace g_lat = "47.709297" if municipality == "benediktbeuern" & plzstr == "83671"
	replace g_lon = "11.403428" if municipality == "benediktbeuern" & plzstr == "83671"
	replace g_quality = 8 if municipality == "benediktbeuern" & plzstr == "83671"
	replace g_lat = "50.127101" if municipality == "frankfurt am main" & plzstr == "60323" & street == "gisèle-freud-platz"
	replace g_lon = "8.670918" if  municipality == "frankfurt am main" & plzstr == "60323" & street == "gisèle-freud-platz"
	replace g_quality = 8 if  municipality == "frankfurt am main" & plzstr == "60323" & street == "gisèle-freud-platz"
	replace g_lat = "49.801878" if municipality == "groß-bieberau" & plzstr == "64401" & street == "huegelstraße 20"
	replace g_lon = "8.823273" if municipality == "groß-bieberau" & plzstr == "64401" & street == "huegelstraße 20"
	replace g_quality = 8 if municipality == "groß-bieberau" & plzstr == "64401" & street == "huegelstraße 20"
	replace g_lat = "52.596080" if municipality == "hansestadt stendal" & plzstr == "39576"
	replace g_lon = "11.858493" if municipality == "hansestadt stendal" & plzstr == "39576"
	replace g_quality = 8 if municipality == "hansestadt stendal" & plzstr == "39576"
	replace g_lat = "50.182862" if municipality == "koenigstein im taunus" & plzstr == "61462" & street == "hauptstrasse"
	replace g_lon = "8.465478" if municipality == "koenigstein im taunus" & plzstr == "61462" & street == "hauptstrasse"
	replace g_quality = 8 if municipality == "koenigstein im taunus" & plzstr == "61462" & street == "hauptstrasse"
	replace g_lat = "47.815174" if municipality == "neuenburg" & plzstr == "79395" & street == "dekan-martin-straße"
	replace g_lon = "7.561710" if municipality == "neuenburg" & plzstr == "79395" & street == "dekan-martin-straße"
	replace g_quality = 8 if municipality == "neuenburg" & plzstr == "79395" & street == "dekan-martin-straße"
	replace g_lat = "49.156928" if municipality == "parsberg" & plzstr == "92331" & street == "alte seer straße 2"
	replace g_lon = "11.722022" if municipality == "parsberg" & plzstr == "92331" & street == "alte seer straße 2"
	replace g_quality = 8 if municipality == "parsberg" & plzstr == "92331" & street == "alte seer straße 2"
	replace g_lat = "49.156928" if municipality == "parsberg" & plzstr == "92331" & street == "alte seer straße 3"
	replace g_lon = "11.722022" if municipality == "parsberg" & plzstr == "92331" & street == "alte seer straße 3"
	replace g_quality = 8 if municipality == "parsberg" & plzstr == "92331" & street == "alte seer straße 3"
	replace g_lat = "49.012736" if municipality == "regensburg" & plzstr == "93047" & street == ""
	replace g_lon = "12.099696" if municipality == "regensburg" & plzstr == "93047" & street == ""
	replace g_quality = 8 if municipality == "regensburg" & plzstr == "93047" & street == ""
	replace g_lat = "52.532881" if municipality == "stroehen" & plzstr == "49419"
	replace g_lon = "8.693654" if municipality == "stroehen" & plzstr == "49419"
	replace g_quality = 8 if municipality == "stroehen" & plzstr == "49419"
	replace g_lat = "48.203072" if municipality == "waldkraiburg" & plzstr == "84478"
	replace g_lon = "12.408320" if municipality == "waldkraiburg" & plzstr == "84478"
	replace g_quality = 8 if municipality == "waldkraiburg" & plzstr == "84478"
	
	
	
	
********************************************************************************
*	Combine with full strike data base & exoirt
********************************************************************************
	
	merge 1:m fulladdress using "$temp/greta_cons_strikes_ordnungsamt_all_strikes.dta"
	count if _merge != 3
	assert r(N) == 0
	drop _merge
	
	
	order day month year g_quality state county  plzstr  municipality street location address g_lat g_lon
	
	drop g_country g_state g_county  g_city g_postcode g_street g_number ///
		g_confidence location address fulladdress g_formatted

	
	rename plzstr plz 
	rename g_lat latitude
	rename g_lon longitude
	rename street location
	
	drop if day == "."
	
	
	export delimited using "$strike_output\greta_cons_fff_strikes_ordnungsamt_geocoordinates_all_strikes.csv", delimiter(";") replace

	
	
	
	
	
	
	
	
	
	