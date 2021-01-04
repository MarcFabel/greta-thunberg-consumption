
/* Download maps with German administrative boundaries from 01/01/2019.
Download maps in geographic coordinate system to make sure that geo2xy uses same projection and spmap works properly. 
Two types of administrative maps are available: 
1) Compact (in German "Kompakt"): Only the smallest administrative units are available, since all larger administrative untis can be obtained by aggregation 
2) Levels (in German: "Ebenen"): Every level of administration (municipalities, counties, areas , states, country)  is available in a separate shape file.
*/


* Ebenen
{
cd W:\EoCC\analysis\data\source\maps
* Note this is a link to a FTP server where maps in other formats or other dates can be dowonlodad as well
*copy "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2019/vg250_01-01.geo84.shape.ebenen.zip" "vg250_01-01.geo84.shape.ebenen.zip", replace
*unzipfile "vg250_01-01.geo84.shape.ebenen.zip", replace

* To display maps (e.g. points on administrative map) correctly, Stata command "spmap" (or "grmap") requires that that shp files are transformed to dta files AND that any geopgraphical information (lat/lon)) is projected into the same reference system. "shp2dta" does the first and "geo2xy" doest the latter.

* Transfor shape files to dta files (shp2dta only works in working directory)
cd W:\EoCC\analysis\data\source\maps\vg250_2019-01-01.geo84.shape.ebenen\vg250_ebenen
shp2dta using VG250_LAN, data("ger_data_lan")  coor("ger_coordinates_lan") replace // STA = all of Germany
use ger_data_lan, clear
spmap using "ger_coordinates_lan.dta", id(_ID) //Map is distorted because it uses degrees from geographical coordinate system and not meters from projected coordinate system). Reporjection is needed.

* Transrmation of geographicial coordinates in degres into "Web Mercator" projection in meters
* Note: the same procedure is done for the cities in "append.do"
use ger_coordinates_lan, clear
rename _Y ylat
rename _X xlon
geo2xy ylat xlon , gen(_Y _X)
save ger_coordinates_transformed_lan, replace
}

*Test if maps work
use ger_data_lan, clear
spmap using "ger_coordinates_transformed_lan.dta", id(_ID)  // No distortions

*-----------------------------Sebastian-----------------------------------
cd W:\EoCC\analysis\data\source\maps\vg250_2019-01-01.geo84.shape.ebenen\vg250_ebenen
use "W:\EoCC\analysis\output\temp\appended_cleaned_geocoded_map.dta", clear

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

gen obs = 1
bys g_state: gen obs_sum = _N


duplicates drop  g_state, force
sort g_state
order g_state obs_sum
browse

drop if g_state== ""


gen id_state = _n
drop state
rename g_state GEN

merge 1:m GEN using ger_data_lan

spmap obs_sum using ger_coordinates_transformed_lan, id(_ID) fcolor(Blues) title("Number of Protests by State", size(*0.75)) legend(title("Number of Protests", size(*0.5) bexpand)) 

graph export "W:\EoCC\analysis\output\graphs\descriptive\protests_by_state_map.pdf", replace


*---------------------------------- Adding names of regions---------------

cd W:\EoCC\analysis\data\source\maps\vg250_2019-01-01.geo84.shape.ebenen\vg250_ebenen

use "W:\EoCC\analysis\output\temp\appended_cleaned_geocoded_map.dta", clear

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

gen obs = 1
bys g_state: gen obs_sum = _N


duplicates drop  g_state, force
sort g_state
order g_state obs_sum
browse

drop if g_state== ""


gen id_state = _n
drop state
rename g_state GEN

save geocoded_16states.dta, replace

*make labels to plot on the map
use "geocoded_16states.dta", clear

gen labtype = 1
append using "geocoded_16states.dta"
replace labtype = 2 if labtype==.
generate label = GEN if labtype==1
replace label = string(obs_sum, "%4.1f" ) if labtype == 2


gen length = length(GEN)
split label if length> 10
replace label1 = label if label1 == ""
drop label
*reshape long label, i(id_state lon lat GEN) j(labtype)
drop if label == ""
save "labels1.dta", replace


use "geocoded_16states.dta", clear

merge 1:m GEN using ger_data_lan

spmap obs_sum using ger_coordinates_transformed_lan, id(_ID) fcolor(PuBuGn) title("Number of Protests by State", size(*0.75)) legend(title("Number of Protests", size(*0.5) bexpand)) ///
label(data(Labels1) xcoord(lon)  ycoord(lat) ///
label(label) by(labtype) size(*0.85 ..) pos(0 6) length(21) )

graph export "W:\EoCC\analysis\output\graphs\descriptive\protests_by_state_map_labels.pdf", replace


****** use centroids to make labels appear in the center of the state
// name of states don't appear in the center of state because we didn't generate centroids.
//but this code doesn't work
cd W:\EoCC\analysis\data\source\maps\vg250_2019-01-01.geo84.shape.ebenen\vg250_ebenen
shp2dta using VG250_LAN, data("ger_data_lan")  coor("ger_coordinates_lan") genid(id) gencentroids(c) replace 


use ger_coordinates_lan, clear
rename _Y ylat
rename _X xlon
geo2xy ylat xlon , gen(_Y _X)
local lon0 = r(lon0)
local f = r(f)
local a = r(a)
save ger_coordinates_transformed_lan, replace



use ger_data_lan, clear
gen x = runiform()
save ger_data_lan2, replace

gen labtype  = 1
append using ger_data_lan2
replace labtype = 2 if labtype==.
replace GEN = string(x, "%3.2f") if labtype ==2
geo2xy  y_c x_c,   projection( mercator, `a' `f' `lon0' ) replace
save maplabels, replace

use ger_data_lan2,clear

spmap x using "ger_coordinates_transformed_lan.dta", id(id) /// 
  fcolor(BuRd) ocolor(white ..) /// 
   label(data(maplabels) xcoord(x_c)  ycoord(y_c) ///
  label(GEN) by(labtype)  size(*0.85 ..) pos(12 0) )


spmap using "ger_coordinates_lan.dta", id(_ID) //Map is distorted because it uses degrees from geographical coordinate system and not meters from projected coordinate system). Reporjection is needed.

* Transrmation of geographicial coordinates in degres into "Web Mercator" projection in meters
* Note: the same procedure is done for the cities in "append.do"
use ger_coordinates_lan, clear
rename _Y ylat
rename _X xlon
geo2xy ylat xlon , gen(_Y _X)
save ger_coordinates_transformed_lan, replace
}

*Test if maps work
use ger_data_lan, clear
spmap using "ger_coordinates_transformed_lan.dta", id(_ID)  // No distortions


***-------------------------------------Interactive map--------------------------------***
sysdir set PERSONAL "c:\ado\personal"
set scheme ifo2017                    // does not change the colors


ssc install geochart
use "geocoded_16states.dta", clear

geochart obs_sum GEN , ///
    region("DE") resolution("provinces") ///
    title("Number of protests by state") ///
	note("Fridays For Future data") ///
    width(1280) height(800) save("W:\EoCC\analysis\data\source\maps/FFF.htm") replace  	colorlow("#ffe4c4") colorhigh("#008b8b") savebtn


_______________________________________________________________________

global dir_leaflet "G:\02_Personen\Hiwis\Alina\stataleaflet\stata2leaflet-master"
global dir_data "W:\EoCC\analysis\output\temp"

use "$dir_data/appended_cleaned_geocoded_map.dta", clear

cd "G:\02_Personen\Hiwis\Alina\stataleaflet\stata2leaflet-master"

gen mcol="red"
keep in 1/100
keep if g_state=="Bavaria"
stata2leaflet lat lon location3,  mcolorvar(mcol) replace nocomments ///
	title("Here's my new map") ///
	caption("Here's some more details")





















