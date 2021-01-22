//****************************************************************************
* File name: fridays_for_future_master_geocoding_addresses_of_strikes_internet_20201208_review.do
* Author: LLeutner
* Date: 12/08/20
* Description: This program allocates geo-coordinates to the locations of the individual strikes so that the strikes can be assigned to Bundestagswahlkreisen
* 1. Using STATA Output (strikes are already assigned to geo-coordinates in this output but not uniformly)
* 2. Creating string variables of the variables "id" and "diff_city", so that these variables can be used in the "replace" command
* 3. Renaming "city3" and "location3" (variables which are used for geocoding) to fix inconsistencies
* 4. Changing the variable "diff_citystr" if there is no information on the fff-webpage that the strike took place exclusively in another city 
* 5. Dropping all strikes which were just (train)rides to get to another strike in another city
* 6. Dropping redundant variables (lon, lat, id, city, city2, location, location2)
* 7. Dropping variables which were created during the preceding geocoding
* 8. Using the location/municipality where the municipality/county had the most strikes during the observation period if location or municipality is missing,
* but necessary to assign the strike to a electoral district 
* 9. Adding state information if information about the respective state is missing
* 10. Changing locations or addresses if they do not provide street information
* 11. Creating the "plz" variable for locations where geocoding cannot be performed without this information
* 12. Adding information about plz if required
* 13. Creating the "comment" variable for further information on geo-coordinates
* 14. Indicating by the variable "comment" if the available information is sufficient to assign strikes to Bundestagswahlkreisen
* 15. Dropping variables which are not required for geocoding (dates of the individual strikes)
* 16. Generating a new variable that combines all necessary address information for geocoding
* 17. Dropping duplicates
* 18. Geocoding using Stata modul "Opencagegeo"
* 19. Indicating by the column "comment" if the information of "g_quality" is wrong
* 20. Changing coordinates manually if they are not matching to the address of the strike (with help of maps.google.com)
* 21. Preparing data for export and further work with QGIS: Replace umlauts and similar, drop unrequired variables, sort by address
* 22. Dropping duplicates in terms of all variables and in terms of g_lat & g_lon
* 23. Exporting data to XLSX-File

* Inputs: G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\data\raw\appended_cleaned_geocoded.dta
* https://www.bundestag.de/abgeordnete/wahlkreise/
* https://web.archive.org/web/*/https://fridaysforfuture.de/streiktermine/
* wikipedia.org
* maps.google.com
* G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\Geocoding\opencagegeo.pdf
*
* Outputs: xxxx
*
* Problems encountered: Since the module "Opencageo" can only identify correct street names and sometimes cannot find the whole place if the street name is
* wrong, it was necessary to check all places and addresses to see if they are really street names and if they are spelled correctly. 
* The geocoding could partly not be carried out correctly despite correct street/location, so that the geocoordinates had to be completed manually. 
* The variable "g_quality" of the output, which indicates how exactly the coordinates were determined (the most exact is Number - i.e. the house number)
* sometimes indicates that the coordinates were determined based on the postal code or state, although the module could actually return the street/city of 
* the strike.
*
***************************************************************************/

// Initialize environment
	clear
	set more off
	capture log close
	set mem 8000m


	global path 				"W:\EoCC\analysis\data"
	global strike_source 		"G:\Praktikanten\HIWIS\Wintersteller\FFF"
	global strike_dofiles		"W:\EoCC\analysis\prog\prepare\strikes_subfiles"
	global temp 				"$path\temp/"
	global strike_output		"$path\intermediate\fff_strikes"



//******* Step 1: Use dta-File *******
use "G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\data\raw\appended_cleaned_geocoded.dta", clear

//******* Step 2: Create a string variable of the variables "id" and "diff_city", so that these variables can be used in the "replace" command*******
gen str idstr = string(id, "%04.0f")
gen str diff_citystr = string(diff_city, "%01.0f")

//******* Step 3: Rename "city3" and "location3" (variables which are used for geocoding) to fix inconsistencies*******
do "G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\do_files\internet\subfiles\s3_fridays_for_future_fix_inconsistencies_internet_20201208_review.do"

//******* Step 4: Change the variable "diff_city" if there is no information on the fff-webpage that the strike took place exclusively in another city *******
replace diff_citystr = "0" if idstr == "0586"
replace diff_citystr = "0" if idstr == "0603"
replace diff_citystr = "0" if idstr == "1884"
replace diff_citystr = "0" if idstr == "2047"

//******* Step 5: Drop all strikes which were just (train)rides to get to another strike in another city *******
drop if diff_citystr == "1"

//******* Step 6: Drop redundant variables (lon, lat, id, city, city2, location, location2, diff_city)*******
drop id
drop idstr
drop lon
drop lat
drop city
drop location
drop city2
drop location2
drop address
drop diff_city
drop diff_citystr
rename city3 city
rename location3 location

//******* Step 7: Drop variables which were created during the preceding geocoding*******
drop g_lat
drop g_lon
drop g_country
drop g_state
drop g_county
drop g_city
drop g_postcode
drop g_street
drop g_number
drop g_confidence
drop g_formatted
drop g_quality

//******* Step 8: If location or municipality is missing, but necessary to assign the strike to a electoral district: use the location/municipality where the
********* municipality/county had the most strikes during the observation period.  ******** 
replace location = "Invalidenpark" if location == "" & city == "Berlin"
replace location = "Hauptbahnhof" if location == "" & city == "Bochum"
replace location = "Marktplatz" if location == "" & city == "Bremen"
replace location = "Friedensplatz" if location == "" & city == "Dortmund"
replace location = "Bahnhof" if location == "" & city == "Dresden"
replace location = "Corneliusplatz" if location == "" & city == "Düsseldorf"
replace location = "Willy-Brandt-Platz" if location == "" & city == "Essen"
replace location = "Bockenheimer Warte" if location == "" & city == "Frankfurt am Main"
replace location = "Hachmannplatz" if location == "" & city == "Hamburg"
replace location = "Alter Markt" if location == "" & city == "Köln"
replace location = "Richard-Wagner-Platz" if location == "" & city == "Leipzig"
replace location = "Marienplatz" if location == "" & city == "München"
replace location = "Lorenzkirche" if location == "" & city == "Nürnberg"
replace location = "Lorenzkirche" if location == "Nürnberg" & city == "Nürnberg"
replace location = "Marktplatz" if location == "" & city == "Stuttgart"

******* Step 9: Add state information if information about the respective state is missing******** 
do "G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\do_files\internet\subfiles\s9_fridays_for_future_add_states_of_strikes_internet_20201208_review.do"

//******* Step 10: Change locations or cities if they are not related to any street information ********
do "G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\do_files\internet\subfiles\s10_fridays_for_future_change_addresses_of_strikes_internet_20201208_review.do"

//******* Step 11: Create the "plz" variable for locations where geocoding cannot be performed without this information ********
gen str5 plz=""

//******* Step 12: Add information about plz if required ********
do "G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\do_files\internet\subfiles\s12_fridays_for_future_add_plz_of_strikes_internet_20201208_review.do"

//******* Step 13: Create the "comment" variable for further information on geo-coordinates ********
gen str comment=""

//******* Step 14: Indicate by the variable "comment" if the available information is sufficient to assign strikes to Bundestagswahlkreisen********* 
do "G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\do_files\internet\subfiles\s14_fridays_for_future_comment_information_sufficient_internet_20201208_review.do"

//******* Step 15: Drop variables which are not required for geocoding (dates of the individual strikes)********* 
drop time_format

//******* Step 16: Generating a new variable that combines all necessary address information for geocoding)*********
gen str1 leer=" "
egen fulladdress=concat(location leer plz leer city leer state)
drop leer
 
//******* Step 17: Drop duplicates*********

qui save "$temp/greta_cons_strikes_internet_all_strikes.dta", replace
keep location city plz fulladdress comment
duplicates drop

//******* Step 18: Geocoding using Stata modul "Opencagegeo"*********
opencagegeo, key (66e8c8a686e64fa5803fa4958e006ed3) fulladdress (fulladdress) countrycode (DE) replace

	*qui save "$temp/strikes_internet_geo.dta", replace
	use "$temp/strikes_internet_geo.dta", clear

	
//******* Step 19: Indicate by the column "comment" if the information of "g_quality" is wrong ********
replace comment = "location used for geocoding" if location == "Maltesergarten" & city == "Amberg"
replace comment = "location used for geocoding" if location == "Herrenbreite" & city == "Aschersleben"
replace comment = "location used for geocoding" if location == "Schilde-Park" & city == "Bad Hersfeld"
replace comment = "location used for geocoding" if location == "Karlspark" & city == "Bad Reichenhall"
replace comment = "location used for geocoding" if location == "Annemirl-Bauer Platz" & city == "Berlin"
replace comment = "location used for geocoding" if location == "Invalidenpark" & city == "Berlin"
replace comment = "location used for geocoding" if location == "Kesselbrink" & city == "Bielefeld"
replace comment = "location used for geocoding" if location == "Dr. Ruer Platz" & city == "Bochum"
replace comment = "location used for geocoding" if location == "Hauptbahnhof" & city == "Bochum"
replace comment = "location used for geocoding" if location == "Rathaus" & city == "Bochum"
replace comment = "location used for geocoding" if location == "Marktplatz" & city == "Bünde"
replace comment = "municipality used for geocoding" if location == "Lily-Herkin-Platz" & city == "Dessau-Roßlau"
replace comment = "location used for geocoding" if location == "Stadtgarten" & city == "Dortmund"
replace comment = "location used for geocoding" if location == "Marktplatz" & city == "Eichstätt"
replace comment = "location used for geocoding" if location == "Schlosspark" & city == "Eschwege"
replace comment = "location used for geocoding" if location == "Carlisle Park" & city == "Flensburg"
replace comment = "location used for geocoding" if location == "Hafenspitze" & city == "Flensburg"
replace comment = "location used for geocoding" if location == "Stadtpark" & city == "Forchheim"
replace comment = "location used for geocoding" if location == "Europaplatz" & city == "Friedberg"
replace comment = "location used for geocoding" if location == "Therese-Giehse-Platz" & city == "Germering"
replace comment = "location used for geocoding" if location == "Unterer Hauptmarkt" & city == "Gotha"
replace comment = "location used for geocoding" if location == "Stadtpark" & city == "Grafing bei München"
replace comment = "location used for geocoding" if location == "Kirchplatz" & city == "Greiz"
replace comment = "location used for geocoding" if location == "Berliner Platz" & city == "Hagen"
replace comment = "location used for geocoding" if location == "Theaterplatz" & city == "Hagen"
replace comment = "location used for geocoding" if location == "Alter Markt" & city == "Haan"
replace comment = "location used for geocoding" if location == "Neuer Markt" & city == "Haan"
replace comment = "location used for geocoding" if location == "St Pauli (U-Bahn Station)" & city == "Hamburg"
replace comment = "location used for geocoding" if location == "Wilhelmsburg" & city == "Hamburg"
replace comment = "location used for geocoding" if location == "Friedensplatz" & city == "Heilbronn"
replace comment = "location used for geocoding" if location == "Schlossplatz" & city == "Jülich"
replace comment = "location used for geocoding" if location == "Berndorfer Tor" & city == "Korbach"
replace comment = "location used for geocoding" if location == "Rathausplatz" & city == "Lahr"
replace comment = "location used for geocoding" if location == "Augustusplatz" & city == "Leipzig"
replace comment = "location used for geocoding" if location == "Rosental" & city == "Leipzig"
replace comment = "location used for geocoding" if location == "Simsonplatz" & city == "Leipzig"
replace comment = "location used for geocoding" if location == "Marktplatz" & city == "Leopoldshöhe"
replace comment = "location used for geocoding" if location == "Königsplatz" & city == "München"
replace comment = "location used for geocoding" if location == "Hofgarten" & city == "Neuburg an der Donau"
replace comment = "location used for geocoding" if location == "Rathausplatz" & city == "Niebüll"
replace comment = "location used for geocoding" if location == "Fischmarkt" & city == "Offenburg"
replace comment = "location used for geocoding" if location == "Wendelsteinpark Prien" & city == "Prien am Chiemsee"
replace comment = "location used for geocoding" if location == "Marktplatz" & city == "Radolfzell"
replace comment = "location used for geocoding" if location == "Dr.-Helene-Kuhlmann-Park" & city == "Recklinghausen"
replace comment = "location used for geocoding" if location == "Mangfallpark" & city == "Rosenheim"
replace comment = "location used for geocoding" if location == "Bahnhofsplatz" & city == "Rüsselsheim am Main"
replace comment = "location used for geocoding" if location == "Capitolplatz" & city == "Schleswig"
replace comment = "location used for geocoding" if location == "Marktplatz" & city == "Schwäbisch Hall"
replace comment = "location used for geocoding" if location == "Erwin-Schoettle-Platz" & city == "Stuttgart"
replace comment = "location used for geocoding" if location == "Marktplatz" & city == "Stuttgart"
replace comment = "location used for geocoding" if location == "Schlossplatz" & city == "Stuttgart"
replace comment = "location used for geocoding" if location == "Europagarten" & city == "Syke"
replace comment = "location used for geocoding" if location == "Schlossplatz" & city == "Tauberbischofsheim"
replace comment = "location used for geocoding" if location == "Valentinspark" & city == "Unterschleißheim"
replace comment = "municipality used for geocoding" if city == "Weiden in der Oberpfalz"
replace comment = "location used for geocoding" if location == "Goetheplatz" & city == "Weimar"
replace comment = "location used for geocoding" if location == "Theaterplatz" & city == "Weimar"
replace comment = "location used for geocoding" if location == "Liebfrauenkirche" & city == "Westerburg"
replace comment = "municipality used for geocoding" if location == "Marktplatz" & city == "Wittenberg, Lutherstadt"
replace comment = "municipality used for geocoding" if location == "Schlossplatz" & city == "Wittenberg, Lutherstadt"
replace comment = "location used for geocoding" if location == "Schloßplatz" & city == "Wolfenbüttel"

//******* Step 20: Change coordinates manually if they are not matching to the address of the strike (with help of maps.google.com) ********
replace g_lat = "50.7772821" if city == "Aachen" & plz == "52062" & location == "Volkshochschule"
replace g_lon = "6.0904406" if city == "Aachen" & plz == "52062" & location == "Volkshochschule"
replace comment = "g_lat & g_lon changed manually" if city == "Aachen" & plz == "52062" & location == "Volkshochschule"
replace g_lat = "52.6896178" if city == "Beetzendorf" & plz == "38486" & location == "Sieben Linden 1"
replace g_lon = "11.1433342" if city == "Beetzendorf" & plz == "38486" & location == "Sieben Linden 1"
replace comment = "g_lat & g_lon changed manually" if city == "Beetzendorf" & plz == "38486" & location == "Sieben Linden 1"






merge 1:m fulladdress using "$temp/greta_cons_strikes_internet_all_strikes.dta"
count if _merge != 3
assert r(N) == 0
drop _merge



// date formatation
qui gen day = day(date_format)
qui gen month = month(date_format)
qui gen year  = year(date_format)
drop date_format


order day month year g_quality state plz city location g_lat g_lon

drop g_country g_state g_county  g_city g_postcode g_street g_number ///
		g_confidence fulladdress g_formatted

rename city municipality
rename g_lat latitude
rename g_lon longitude

	export delimited using "$strike_output\greta_cons_fff_strikes_internet_geocoordinates_all_strikes.csv", delimiter(";") replace

