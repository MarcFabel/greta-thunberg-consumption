* File name: fridays_for_future_delete_addresses_of_strikes_ordnungsämter_20201106_review.do
* Author: LLeutner
* Date: 11/06/20
* Description: This program replaces missing information about locations of the strikes reported by the Ordnungsämter with information
* from social media channels
***************************************************************************/
replace location = "" if municipality == "adelsheim" & location == "stadtgarten" 
replace location = "" if municipality == "amberg" & location == "innenstadt" & address == "marktplatz"
replace location = "" if municipality == "amberg" & location == "multifunktionsplatz" & address == "kaiser-ludwig-ring 2"
replace location = "" if municipality == "augsburg" & location == "regierung von schwaben" & address == "fronhof"
replace location = "" if municipality == "augsburg" & location == "vor kongress am park" & address == "goegginger straße 10"
replace location = "" if municipality == "augsburg" & location == "anwesen werner-von-siemens-straße" & address == "werner-von-siemens-straße"
replace location = "" if municipality == "augsburg" & location == "hollbeingymnasium" & address == "hallstraße"
replace location = "" if municipality == "augsburg" & location == "rathausplatz" & address == "am katzenstadel 20"
replace location = "" if municipality == "augsburg" & location == "koenigsplatz" & address == "bahnhofstraße 2"
replace location = "" if municipality == "bad essen" & location == "marienkirche" & address == "lindenstrasse"
replace location = "" if municipality == "bad reichenhall" & location == "innenstadt" & address == "ludwigstraße 23"
replace location = "" if municipality == "bad reichenhall" & location == "innenstadt" & address == "ludwigstraße 24"
replace location = "" if municipality == "bad reichenhall" & location == "vorplatz evangelische kirche" & address == "kurstraße"
replace location = "" if municipality == "bersenbrueck" & location == "rathaus" & address == "lindenstraße"
replace location = "" if municipality == "blaubeuren" & location == "klosterhof" & address == "karlstraße"
replace location = "" if municipality == "bramsche" & location == "rathaus" & address == "hasestraße 11"
replace location = "" if municipality == "braunschweig" & location == "schlossplatz" & address == "kohlmarkt"
replace address = "" if municipality == "bremen" & location == "universitätsallee" & address == "bahnhofsplatz"
replace location = "" if municipality == "bremen" & location == "bahnhofsplatz" & address == "schillerstraße 10"
replace address = "" if municipality == "bremen" & location == "am markt" & address == "marktplatz"
replace location = "" if municipality == "bremen" & location == "oberschule findorff " & address == "buergerweide"
replace location = "" if municipality == "bremen" & location == "theater am goetheplatz" & address == "goetheplatz"
replace location = "" if municipality == "bremen" & location == "kastanienwaeldchen" & address == "herdentorsteinweg"
replace address = "" if municipality == "bremen" & location == "domshof" & address == "grasmarkt"
replace location = "" if municipality == "bruchsal" & location == "zentrum"
replace address = "" if municipality == "brühl" & address == "wiesenplaetz 7"
replace location = "" if municipality == "burghausen" & location == "bahnhof" & address == "marktlerstraße"
replace location = "" if municipality == "cham" & location == "innenstadt"
replace address = "" if municipality == "cuxhaven" & location == "am bahnhof" & address == "bahnhofsplatz"
replace address = "" if municipality == "deggendorf" & location == "luitpoldplatz" & address == "egger straße 30"
replace location  = "" if municipality == "dillingen" & location == "stadtsaal" & address == "adolph-kolping-platz 1"
replace location  = "" if municipality == "dissen am teutoburger wald" & location == "schwarzer platz" & address == "lerchenstraße"
replace location  = "" if municipality == "dorfen" & location == "friedhofsparkplatz" & address == "erdinger straße"
replace address = "" if municipality == "feuchtwangen" & location == "am zwinger" & address == "stadtpark"
replace address = "" if municipality == "frankenberg (eder)" & location == "obermarkt" & address == "obermarkt"
replace location = "" if municipality == "frankenberg (eder)" & location == "landratsamtsgarten" & address == "bahnhofstraße"
replace address = "" if municipality == "frankenberg (eder)" & location == "neustädter straße" & address == "obermarkt"
replace location = "" if municipality == "frankfurt am main" & location == "deutsche bank" & address == "taunusanlage 12"
replace address = "" if municipality == "frankfurt am main" & location == "mainkai" & address == "alte bruecke"
replace location = "" if municipality == "frankfurt am main" & location == "parteibuero gruene" & address == "oppenheimer strasse 17"
replace location = "" if municipality == "frankfurt am main" & location == "fraport gebaeude" & address == "hugo-eckener ring"
replace location = "" if municipality == "frankfurt am main" & location == "taunusanlage" & address == "mainzer landstrasse"
replace location = "" if municipality == "frankfurt am main" & location == "cafe koz" & address == "juegelstrasse"
replace location = "" if municipality == "frankfurt am main" & location == "tram-haltestelle" & address == "ludwig-erhard-anlage 1"
replace location = "" if municipality == "frankfurt am main" & location == "ezb" & address == "horst-schulmann-strasse"
replace location = "" if municipality == "frankfurt am main" & location == "ctr-platz" & address == "hasengasse"
replace location = "" if municipality == "frankfurt am main" & location == "schoene aussicht" & address == "kurt-schumacher-strasse"
replace location = "" if municipality == "frankfurt am main" & location == "paulsplatz" & address == "berliner strasse"
replace address = "" if municipality == "frankfurt am main" & location == "stiftstraße" & address == "brockhausbrunnen"
replace location = "" if municipality == "freising" & location == "kriegerdenkmal" & address == "obere hauptstraße"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "hannah-arendt-platz 1"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "trammplatz"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "friederikenplatz"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "georgsplatz"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "karmarschstraße"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "ständehausstraße"
replace location = "" if municipality == "hannover" & location == "innenstadt" &address == "ernst-august-platz"
replace location = "" if municipality == "hannover" & location == "innenstadt" & address == "jägerstraße"
replace location = "" if municipality == "hannover" & location == "landtag" & address == "hannah-arendt-platz 1"
replace location = "" if municipality == "hannover" & location == "innenstadt" & address == "opernplatz"
replace location = "" if municipality == "hannover" & location == "innenstadt" & address == "hildesheimer straße"
replace location = "" if municipality == "hockenheim" & location == "carl-friedrich-gauß-gymnasium" & address == "schubertstraße 5"
replace address = "" if municipality == "horb am neckar" & location == "floeßerwasen" & address == "schillerstraße"
replace location = "" if municipality == "isny" & address == "Wassertorstraße"
replace location = "" if municipality == "isny" & location == "kirchplatz"
replace location = "" if municipality == "juist" & location == "nationalpark haus" & address == "carl-stegmann-straße 5"
replace location = "" if municipality == "juist" & location == "marsch vom deich" & address == "an't diekskant"
replace location = "" if municipality == "karlsruhe" & location == "radkorso im kreis" & address == "rudolf-freytag-straße 7"
replace location = "" if municipality == "karlsruhe" & location == "radkorso im kreis" & address == "rudolf-freytag-straße 8"
replace location = "" if municipality == "karlsruhe" & location == "radkorso im kreis" & address == "rudolf-freytag-straße 9"
replace location = "" if municipality == "karlsruhe" & location == "radkorso im kreis" & address == "rudolf-freytag-straße 6"
// duplication of addresses in constancy
replace address = "" if municipality == "konstanz" & location == "marktstaette"
replace address = "" if municipality == "konstanz" & location == "hafenstrasse" & address == "marktstaette"
// "kreuzlingen hafenplatz" not located in Germany
replace location = "" if municipality == "konstanz" & location == "kreuzlingen hafenplatz 8280"
replace address = "" if municipality == "konstanz" & location == "herosé park" & address == "marktstaette"
replace address = "" if municipality == "konstanz" & location == "sankt-stephans-platz"
replace location = "" if municipality == "konstanz" & location == "muensterplatz" & address == "herosé park"
replace location = "" if municipality == "konstanz" & location == "herosé park" & address == "stadtgarten"
replace location = "" if municipality == "konstanz" & location == "siemens" & address == "lilienthalstraße 16"
replace location = "" if municipality == "konstanz" & location == "herosé park" & address == "bodanstraße"
replace address = "" if municipality == "konstanz" & location == "mainaustraße" & address == "marktstaette"
replace location = "" if municipality == "landau an der isar" & location == "volksfestplatz" & address == "harburgerstraße"
replace location = "" if municipality == "landshut" & location == "rathaus" & address == "altstadt 315"
replace location = "" if municipality == "leer" & location == "rathaus" & address == "rathausstraße"
replace location = "" if municipality == "melle" & location == "an kreisverkehren"
replace location = "" if municipality == "melle" & location == "an ampeln"
replace location = "" if municipality == "muennerstadt" & location == "gymnasium" & address == "marktplatz"
replace address = "" if municipality == "neckargemuend" & location == "hauptstrasse" & address == "b37"
replace location = "" if municipality == "neu wulmstorf" & location == "rathaus" & address == "bahnhofstraße 39"
replace location = "" if municipality == "neu wulmstorf" & location == "rathaus" & address == "bahnhofstraße 40"
replace address = "" if municipality == "neuenburg" & location == "dekan-martin-straße" & address == "umzug"
replace location = "" if municipality == "neuendettelsau" & location == "gebaeude mission eine welt" & address == "hauptstraße"
replace location = "" if municipality == "norderney" & location == "stadt norderney" & address == "am kurplatz 1"
replace location = "" if municipality == "nuernberg" & location == "lorenzkirche" & address == "rathausplatz"
replace location = "" if municipality == "oberkochen" & location == "rathaus" & address == "eugen-bolz-platz"
replace address = "" if municipality == "olching" & location == "hauptstraße" & address == "neu-estinger-strasse"
replace address = "" if municipality == "oldenburg" & location == "bahnhofsplatz" & address == "schloßplatz"
replace location = "" if municipality == "parsberg" & location == "rathaus" & address == "alte seer straße 3"
replace location = "" if municipality == "parsberg" & location == "rathaus" & address == "alte seer straße 2"
replace location = "" if municipality == "regensburg" & location == "stadtgebiet"
replace location = "" if municipality == "regensburg" & location == "rathausplatz" & address == "haidplatz"
replace location = "" if municipality == "regensburg" & location == "innenstadt"
replace location = "" if municipality == "regensburg" & location == "jakobstor" & address == "goethestraße"
replace location = "" if municipality == "rottenburg am neckar" & location == "rathaus" & address == "marktplatz"
replace location = "" if municipality == "schriesheim" & location == "rathaus" & address == "friedrichstraße 28"
replace location = "" if municipality == "schwalmstadt" & location == "totenkirche" & address == "burggasse"
replace location = "" if municipality == "schweinfurt" & location == "markt " & address == "markt"
replace location = "" if municipality == "schwetzingen" & location == "kleine planken" & address == "mannheimer straße"
replace location = "" if municipality == "stroehen" & location == "dorfplatz"
replace location = "" if municipality == "teterow" & location == "innenstadt"
replace location = "" if municipality == "tostedt" & location == "rathaus" & address == "schuetzenstraße 24"
replace location = "" if municipality == "waldshut-tiengen" & location == "rathaus" & address == "kaiserstraße"
replace location = "" if municipality == "wertingen" & location == "stadthalle" & address == "landrat-anton-rauch-platz 3"
replace location = "" if municipality == "wuerzburg" & location == "niederlassung siemens ag" & address == "schweinfurter straße 1"