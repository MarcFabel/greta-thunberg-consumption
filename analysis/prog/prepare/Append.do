clear 
clear matrix
set more off
capture log close


*** Alina's GLOBALS DIRECTORIES ***
*global dir_FFF "W:\AG-INT\Alina\FFF2"
global dir_data "W:\EoCC\analysis\data\source\fff_strikes"
global dir_temp "W:\EoCC\analysis\output\temp"
global dir_prepare "W:\EoCC\analysis\prog\prepare"




/*-------------IMPORT CSV FILES-----------------------------*/
cd "W:\EoCC\analysis\data\source\fff_strikes"
clear
local myfilelist : dir . files"*.csv"
foreach file of local myfilelist {
drop _all
import delimited using `"`file'"', charset(utf8)
local outfile = subinstr("`file'",".csv","",.)
save "`outfile'", replace
}

/*-------------GENERATE DATE-----------------------------*/

tempvar appendsource
local allfiles : dir . files "*.dta"
dis `allfiles'
clear
generate filename=""
foreach file of local allfiles {
display `"adding file: {it:`file'}"'
append using `"`file'"', generate(`appendsource') force
quietly : replace filename=substr(`"`file'"', 1,strlen(`"`file'"')) if (`appendsource'==1)
drop `appendsource'
display `"{tab}...done"'
}


split       filename, parse(_) gen(date)
split       date5, parse(.) gen(file)
drop        filename
drop        date1-date2
drop        date5
drop        file2
gen         date = date3 + "/" + date4 + "/" + file1
drop        date3-date4 file1

gen         date_format = date(date, "YMD")
format      date_format %d

drop        date



/*-------------RENAME VARABLES-----------------------------*/ 

rename      v1 city
rename      v2 hour
rename      v3 location


gen         city2 = city
gen         location2 = location

replace     location2=strtrim(location2)
replace     city2=strtrim(city2)
split       hour, parse(" ") gen(time)
drop        time2 hour
rename      time1 time


gen id=_n




/*-------------DUPLICATE DROP-----------------------------*/

sort        city2 location2
quietly     by city2 location2:  gen dup = cond(_N==1,0,_n)
tabulate    dup
drop        if dup>1	
		
		
/*-------------REMOVE BLANK SPACES-----------------------------*/		

replace     city2 = regexr(city2, "\((.)+\)", "")
*li
replace     city2=strtrim(city2)


replace     location2 = regexr(location2, "\((.)+\)", "")
*li
replace     location2=strtrim(location2)



/*-------------DUPLICATE DROP-----------------------------*/

sort        city2 location2
quietly     by city2 location2:  gen dup2 = cond(_N==1,0,_n)
tabulate    dup2
drop        if dup2>1	

drop        in 1/4
drop        dup dup2
drop        time3-time5


/*-------------DELETE .DTA FILES-----------------------------*/ 

cd "W:\EoCC\analysis\data\source\fff_strikes"

local datafiles: dir "`workdir'" files "*.dta"

foreach datafile of local datafiles {
        rm `datafile'
}


/*-------------CLEAN LOCATION2-----------------------------*/ 

replace location2 = "Elisenbrunnen" if city2 == "Aachen"
replace location2 = "Rossmarkt" if city2 == "Alzey"
replace location2 = subinstr(location2, "Fahrraddemo", "", .)
replace location2 = subinstr(location2, "ABG", "", .)
replace location2 = "Marktplatz" if city2 == "Anklam"
replace location2 = "Bürgerhaus" if city2 == "Anröchte"
replace location2 = "Martin-Luther-Platz" if city2 == "Ansbach"
replace location2 = "Theaterplatz" if city2 == "Aschaffenburg"
replace location2 = subinstr(location2, "Vor dem", "", .)
replace location2 = "Sparkassen-Arena" if city2 == "Aurich"
replace location2 = subinstr(location2, "Globaler Klimastreik", "", .)
replace location2 = "Marktplatz" if city2 == "Bad Belzig"
replace location2 = subinstr(location2, "Westportal", "", .)
replace location2 = "Karlspark" if city2 == "Bad Reichenhall"
replace location2 = "Marktplatz" if city2 == "Bad Segeberg"
replace location2 = subinstr(location2, "Tölz", "", .)
replace location2 = subinstr(location2, "zw. Gymnasium & Realschule", "", .)
replace location2 = "Bahnhof" if city2 == "Bamberg"
replace location2 = "Bahnhof" if city2 == "Bassum"
replace location2 = subinstr(location2, "#INSMbedrohtParis", "", .)
replace location2 = subinstr(location2, "Kundgebung", "", .)
replace location2 = subinstr(location2, "()", "", .)
replace location2 = "Busparkplatz" if city2 == "Bernkastel-Kues"
replace location2 = subinstr(location2, "Fahrrad-Demo und normaler Demozug + weitere Aktionen", "", .)
replace location2 = subinstr(location2, "Demozug", "", .)
replace location2 = subinstr(location2, "week4CLIMATE", "", .)
replace location2 = subinstr(location2, "Demo + Rave", "", .)
replace location2 = subinstr(location2, "Bochum", "", .)
replace location2 = subinstr(location2, "Filmabend", "", .)
replace location2 = subinstr(location2, "Vorm", "", .)
replace location2 = "Schulzentrum" if city2 == "Boizenburg"
replace location2 = subinstr(location2, "Demo anschließend streikwoche", "", .)
replace location2 = subinstr(location2, "Fokusdemo Thema: Earth", "", .)
replace location2 = subinstr(location2, "Bushaltestelle an der", "", .)
replace location2 = subinstr(location2, "Start am", "", .)
replace location2 = "Neustadtmarkt" if city2 == "Brandenburg an der Havel"
replace location2 = subinstr(location2, "Earth Strike", "", .)
replace location2 = subinstr(location2, "Week4Climate - Tanzdemo!", "", .)
replace location2 = "Marktplatz" if city2 == "Bünde"
replace location2 = subinstr(location2, "Clean-Up", "", .)
replace location2 = subinstr(location2, "Startpunkt", "", .)
replace location2 = subinstr(location2, ":", "", .)
replace location2 = subinstr(location2, "- 1300 Uhr HDA", "", .)
replace location2 = "Neumarkt" if city2 == "Datteln"
replace location2 = subinstr(location2, "Delmenhorst", "", .)
replace location2 = subinstr(location2, "- Kinoseite", "", .)
replace location2 = "Luisenplatz" if city2 == "Demmin"
replace location2 = subinstr(location2, "Detmold", "", .)
replace location2 = subinstr(location2, "- Musik und Reden  &", "", .)
replace location2 = "Friedhofsparkplatz" if city2 == "Dorfen"
replace location2 = "Hauptbahnhof" if city2 == "Duisburg"
replace location2 = "Rathaus Obermarkt" if city2 == "Döbeln"
replace location2 = subinstr(location2, "Picknick und Workshops", "", .)
replace location2 = subinstr(location2, "Düsseldorf", "", .)
replace location2 = subinstr(location2, "Edingen", "", .)
replace location2 = "St-Nikolai-Kirche" if city2 == "Elmshorn"
replace location2 = subinstr(location2, "Fahrt mit dem Bus zur Demo nach", "", .)
replace location2 = subinstr(location2, "Hauptdemo", "", .)
replace location2 = subinstr(location2, "12 Stunden Aktion mit Bühnenprogramm und Infoständen nach dem Demonstrationszug", "", .)
replace location2 = subinstr(location2, "Demo + Bühnenprogramm", "", .)
replace location2 = subinstr(location2, "Esslingen  ab 1130", "", .)
replace location2 = subinstr(location2, "- Schlusskundgebung diesmal vorm Kreishaus", "", .)
replace location2 = subinstr(location2, ">  > Programm vorm Rathaus", "", .)
replace location2 = subinstr(location2, "Treffpunkt am", "", .)
replace location2 = "S-Bahnhof" if city2 == "Filderstadt/Bernhausen"
replace location2 = "Marktplatz" if city2 == "Finsterwalde"
replace location2 = "Speyerer Tor" if city2 == "Frankenthal" & city == "Frankenthal (Pfalz)"
replace location2 = subinstr(location2, "& Zoo", "", .)
replace location2 = subinstr(location2, "1000 Uhr Platz an der alten Synagoge Andacht/Gebet", "", .)
replace location2 = "Kriegerdenkmal" if city2 == "Freising"
replace location2 = "Stadtbahnhof" if city2 == "Friedrichshafen"
replace location2 = subinstr(location2, "Treffen bein", "", .)
replace location2 = subinstr(location2, "Einzelhandelsgeschäft Feneberg -", "", .)
replace location2 = "Rathausplatz" if city2 == "Garmisch-Partenkirchen"
replace location2 = "Heinrich-König-Platz" if city2 == "Gelsenkirchen" & time == "12:00"
replace location2 = subinstr(location2, "vor dem", "", .)
replace location2 = subinstr(location2, "Demo", "", .)
replace location2 = subinstr(location2, "Die In", "", .)
replace location2 = "Theodor-Heuss-Platz" if city2 == "Gronau"
replace location2 = subinstr(location2, "Görlitz", "", .)
replace location2 = subinstr(location2, "und Rannischer Platz 15 Uhr  vom Riebeckplatz", "", .)
replace location2 = "Bei der Stadtbücherei" if city2 == "Hamm"
replace location2 = "Marktplatz vor der St. Jürgen Kirche" if city2 == "Heide"
replace location2 = subinstr(location2, "Sitzdemo", "", .)
replace location2 = "Haupteingang CFGS" if city2 == "Hemmingen"
replace location2 = "Gymnasium" if city2 == "Herzogenaurach" & time == "13:00"
replace location2 = "Gauß Gymnasium" if city2 == "Hockenheim" 
replace location2 = subinstr(location2, "Umzug und CleanUp", "", .)
replace location2 = "Neue Freiheit" if city2 == "Husum" & time == "12:30"
replace location2 = "Bahnhof Idstein" if city2 == "Idstein" 
replace location2 = "Hemberg Parkplatz" if city2 == "Iserlohn" & time == "10:00"
replace location2 = subinstr(location2, "isny + clean up", "", .)
replace location2 = "Schlossplatz" if city2 == "Jülich" 
replace location2 = "Am Neumarkt" if city2 == "Kaarst" 
replace location2 = subinstr(location2, "1800 Uhr Zirkus Maccaroni", "", .)
replace location2 = "Am Gymnasium" if city2 == "Kempen" & time == "10:00"
replace location2 = "Forum" if city2 == "Kempten im Allgäu" 
replace location2 = subinstr(location2, "Kerpen", "", .)
replace location2 = subinstr(location2, "1900 Uhr Marktstätte Laternenumzug", "", .)
replace location2 = "Herosé-Park" if city2 == "Konstanz" & time == "11:30"
replace location2 = subinstr(location2, "Fußgängerzone -T iefebene am", "", .)
replace location2 = "Hauptbahnhof" if city2 == "Krefeld" & time == "11:00"
replace location2 = subinstr(location2, "Kulmbach", "", .)
replace location2 = subinstr(location2, "Königs Wusterhausen", "", .)
replace location2 = subinstr(location2, "mit anschließendem", "", .)
replace location2 = subinstr(location2, "gegenüber vom", "", .)
replace location2 = subinstr(location2, "Langenberg", "", .)
replace location2 = subinstr(location2, "Workshops & Streik", "", .)
replace location2 = "Neues Zentrum" if city2 == "Lehrte" 
replace location2 = subinstr(location2, "Müll-Sammelaktion – 1500 Uhr am", "", .)
replace location2 = subinstr(location2, "Lemgoer", "", .)
replace location2 = subinstr(location2, "Leopoldshöhe Trillerpfeifen-Konzert", "", .)
replace location2 = "Rathaus" if city2 == "Leverkusen" 
replace location2 = "Altes Rathaus" if city2 == "Lindau" & time == "12:00"
replace location2 = subinstr(location2, "Lindenberg", "", .)
replace location2 = subinstr(location2, "(beim Kugelbrunnen", "", .)
replace location2 = "Bahnhof" if city2 == "Ludwigsfelde" 
replace location2 = subinstr(location2, "Schulhof des Wittekind-Gymnasiums 1100 Uhr", "", .)
replace location2 = subinstr(location2, "+", "", .)
replace location2 = "Marktplatz" if city2 == "Lüneburg" & time != "11:00"
replace location2 = "Europaplatz" if city2 == "Lünen" 
replace location2 = subinstr(location2, "- 1700 Uhr Marktplatz Straßenfest Straßenfest", "", .)
replace location2 = "Dr. Franz Schütz Platz" if city2 == "Meerbusch" 
replace location2 = subinstr(location2, "Alle Schulen 1400 Uhr", "", .)
replace location2 = subinstr(location2, "Hinter dem", "", .)
replace location2 = "Marienkirchplatz" if city2 == "Neuss" & time == "12:15"
replace location2 = subinstr(location2, "Aktion mit Kerzen - Laternen und Lampen", "", .)
replace location2 = "Cagnes-sur-Mer-Promenade" if city2 == "Passau" & time != "17:00"
replace location2 = subinstr(location2, "Penzberg", "", .)
replace location2 = subinstr(location2, "Ravensburg", "", .)
replace location2 = subinstr(location2, "()", "", .)
replace location2 = subinstr(location2, "1330  1500 Übergabe Resolution an die Stadt", "", .)
replace location2 = subinstr(location2, "1330  durch die Stadt", "", .)
replace location2 = subinstr(location2, "Oranienburg", "", .)
replace location2 = "Geschwister-Scholl-Platz" if city2 == "München" & id == 831
replace location2 = subinstr(location2, "Tanzdemo", "", .)
replace location2 = subinstr(location2, "Lärmdemo", "", .)
replace location2 = subinstr(location2, " und 24h-Mahnwache", "", .)
replace location2 = subinstr(location2, "Infostand", "", .)
replace location2 = subinstr(location2, " mit   Rathaus", "", .)
replace location2 = subinstr(location2, "Laternenumzug", "", .)
replace location2 = subinstr(location2, "Busreise nach Aurich", "", .)
replace location2 = subinstr(location2, "Norderstedt.", "", .)
replace location2 = subinstr(location2, "geplant", "", .)
replace location2 = subinstr(location2, "Mahnwache", "", .)
replace location2 = "Neptunbrunnen am Domplatz" if id == 365
replace location2 = "Neptunbrunnen am Domplatz" if id == 725
replace location2 = subinstr(location2, "Papenburg  und anschliessende nstration - zuvor 15 Minuten Glockengeläut", "", .)
replace location2 = subinstr(location2, " - Wimmerross", "", .)
replace location2 = subinstr(location2, "  - nstrationszug", "", .)
replace location2 = subinstr(location2, " Streik zum Exerzierplatz", "", .)
replace location2 = subinstr(location2, "Laufdemo", "", .)
replace location2 = subinstr(location2, "Sterndemo", "", .)
replace location2 = subinstr(location2, "Rees nstration mit schauspielerischen Unterbrechungen", "", .)
replace location2 = subinstr(location2, " 1700 Uhr Ernst Reuter Platz", "", .)
replace location2 = subinstr(location2, "Kreativ", "", .)
replace location2 = "Hauptbahnhof" if id == 830
replace location2 = "Rathaus Rheydt" if id == 255
replace location2 = "Rathaus Rheydt" if id == 145
replace location2 = "Blobach" if id == 147
replace location2 = "Historischen Rathaus" if id == 149
replace location2 = "Karl-Friedrich-Schinkel Gymnasium" if id == 711
replace location2 = "Carolinum/Strelitzhalle" if city2 == "Neustrelitz"
replace location2 = "Bahnhof" if id == 1399
replace location2 = "Schulhof KGS" if id == 2126
replace location2 = "Schulhof KGS" if id == 1427
replace location2 = "Hauptbahnhof" if id == 513
replace location2 = "Stadtgraben" if id == 183
replace location2 = "Rathausturmplatz" if id == 1445
replace location2 = "Capitolplatz" if id == 1447
replace location2 = "Capitolplatz" if id == 186
replace location2 = "KGS Schneverdingen" if id == 2151
replace location2 = "Markplatz Schorndorf" if id == 1451
replace location2 = "Schillerplatz" if city2 == "Schweinfurt"
replace location2 = "Markt" if id == 192
replace location2 = "Rathaus" if id == 2177
replace location2 = "Sankt-Guido-Stifts-Platz" if id == 2180
replace location2 = "Forum Stein" if city2 == "Stein"
replace location2 = subinstr(location2, "Westerland 24-Stunden-Streik /", "", .)
replace location2 = "Kurmeile" if id == 767
replace location2 = "Marktplatz" if city2 == "Ulm"
replace location2 = "Amtsgericht" if id == 859
replace location2 = "Bahnhof" if id == 377
replace location2 = "Bahnhof" if id == 1705
replace location2 = subinstr(location2, " -  1430 Uhr Stadtplatz", "", .)
replace location2 = "Gymnasium Walsrode Sporthalle" if city2 == "Walsrode"
replace location2 = "BSW Südgebäude" if city2 == "Wangen im Allgäu"
replace location2 = "KGS" if city2 == "Wennigsen"
replace location2 = "Rathaus" if city2 == "Wermelskirchen"
replace location2 = "Nicolaiplatz" if id == 1536
replace location2 = "Rathaus" if city2 == "Wesel"
replace location2 = "Kaiserplatz" if city2 == "Willich"
replace location2 = "Ottensteinplatz" if city2 == "Wittlich"
replace location2 = "Hauptbahnhof" if city2 == "Wolfsburg"
replace location2 = "Hauptbahnhof" if city2 == "Worms"
replace location2 = "Sparkasse Wülfrath" if city2 == "Wülfrath"
replace location2 = "Bahnhofsplatz" if id == 319




/*-------------CLEAN CITY2-----------------------------*/

replace city2 = "Bad Neustadt an der Saale" if location2 == "Busbahnhof"
replace city2 = subinstr(city2, "Gesundbrunnen", "", .)
replace city2 = subinstr(city2, "Annemirl-Bauer", "", .)
replace city2 = subinstr(city2, "Rathaus Schöneberg", "", .)
replace city2 = subinstr(city2, "Reinickendorf", "", .)
replace city2 = subinstr(city2, "Westkreuz", "", .)
replace city2 = "Buchholz in der Nordheide" if location2 == "Schützenplatz" 
replace city2 = "Cloppenburg" if location2 == "Bernay Platz - Nebengebäude VHS" 
replace city2 = subinstr(city2, "Kreis Pinneberg", "", .)
replace city2 = subinstr(city2, "Architects 4 Future", "", .)
replace city2 = "Garmisch-Partenkirchen" if location2 == "Rathausplatz" & city == "Garmisch Partenkirchen (BY)"
replace city2 = "Neuburg an der Donau" if id==1371
replace city2 = "Neustadt an der Aisch" if id==2078
replace city2 = "Neustadt an der Aisch" if id==155
replace city2 = "Neustadt an der Weinstraße" if id==156
replace city2 = "Mülheim an der Ruhr" if id==2058
replace city2 = "Pfarrkirchen" if id==1415
replace city2 = "Rothenburg ob der Tauber" if id==743
replace city2 = "Rothenburg ob der Tauber" if id==2141
replace city2 = "Rottenburg am Neckar" if id==2142
replace city2 = "Weißenburg in Bayern" if id==214 
replace city2 = "Weißenburg in Bayern" if id == 784 



		
/*-------------REMOVE BLANK SPACES-----------------------------*/		

replace     city2 = regexr(city2, "\((.)+\)", "")
*li
replace     city2=strtrim(city2)


replace     location2 = regexr(location2, "\((.)+\)", "")
*li
replace     location2=strtrim(location2)



/*-------------DUPLICATE DROP-----------------------------*/

sort        city2 location2
quietly     by city2 location2:  gen dup3 = cond(_N==1,0,_n)
tabulate    dup3
drop        if dup3>1	

drop        dup3
drop        in 1/1


save       "$dir_temp\Appended.dta", replace
		
		
		
		
		
		
		