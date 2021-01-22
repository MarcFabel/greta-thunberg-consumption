* File name: fridays_for_future_matching_locations_of_strikes_ordnungsämter_social_media_20201106_review.do
* Author: LLeutner
* Date: 11/06/20
* Description: This program replaces missing information about locations of the strikes reported by the Ordnungsämter with information
* from social media channels
* 1. Matching locations with dta-file 
* 2. Obtaining information about remaining missing locations from social media

* Inputs: G:\Praktikanten\PRAKTIKANTEN\Leutner\Fridays_for_Future\data\raw\appended_cleaned_geocoded.dta
* https://www.instagram.com/fffleipzig/
* https://www.instagram.com/fridaysforfuturestuttgart/
* https://www.facebook.com/pg/fridaysforfuturestuttgart/events/?ref=page_internal
* https://www.instagram.com/fridaysforfuture.zwickau/
* https://www.l-iz.de/politik/engagement/2019/05/Wenn-Menschen-vor-McDonalds-liegen-Fridays-for-Future-macht-auch-in-den-Ferien-weiter-Video-278158)
***************************************************************************/
//******* Step 1: Match locations with dta-file *******
// missing locations and addresses in bernkastel-wittlich, leipzig, stuttgart, ulm & zwickau: matching locations of strikes with "appended_cleaned_geocoded.dta" 
replace municipality = "Wittlich" if county == "bernkastel-wittlich" & day == "29" & month == "11" & year == "2019" & expectedparticipants == "50"
replace location = "Schlossstraße" if county == "bernkastel-wittlich" & day == "29" & month == "11" & year == "2019" & expectedparticipants == "50"
replace municipality = "Bernkastel-Kues" if county == "bernkastel-wittlich" & day == "29" & month == "11" & year == "2019" & expectedparticipants == "100"
replace location = "Peter-Kremer-Weg" if county == "bernkastel-wittlich" & day == "29" & month == "11" & year == "2019" & expectedparticipants == "100"
replace municipality = "Bernkastel-Kues" if county == "bernkastel-wittlich" & day == "05" & month == "04" & year == "2019"
replace location = "Peter-Kremer-Weg" if county == "bernkastel-wittlich" & day == "05" & month == "04" & year == "2019"
replace municipality = "Bernkastel-Kues" if county == "bernkastel-wittlich" & day == "29" & month == "03" & year == "2019" & expectedparticipants == "110"
replace location = "Peter-Kremer-Weg" if county == "bernkastel-wittlich" & day == "29" & month == "03" & year == "2019" & expectedparticipants == "110"
replace municipality = "Wittlich" if county == "bernkastel-wittlich" & day == "20" & month == "09" & year == "2019"
replace location = "Schlossstraße" if county == "bernkastel-wittlich" & day == "20" & month == "09" & year == "2019"

replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "15" & month == "03" & year == "2019"
replace location = "Willy-Brandt-Platz" if municipality == "leipzig" & day == "22" & month == "03" & year == "2019"
replace location = "Rosental" if municipality == "leipzig" & day == "29" & month == "03" & year == "2019"
replace location = "Willy-Brandt-Platz" if municipality == "leipzig" & day == "05" & month == "04" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "12" & month == "04" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "03" & month == "05" & year == "2019"
replace comment = "Müll-Sammelaktion" if municipality == "leipzig" & day == "03" & month == "05" & year == "2019"
replace location = "Simsonplatz" if municipality == "leipzig" & day == "24" & month == "05" & year == "2019"
replace location = "Neues Rathaus" if municipality == "leipzig" & day == "23" & month == "08" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "30" & month == "08" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "20" & month == "09" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "18" & month == "10" & year == "2019"
replace comment = "Mahnwache" if municipality == "leipzig" & day == "18" & month == "10" & year == "2019"
replace location = "Simsonplatz" if municipality == "leipzig" & day == "29" & month == "11" & year == "2019"

replace location = "Rathaus" if municipality == "stuttgart" & day == "14" & month == "02" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "15" & month == "03" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "22" & month == "03" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "29" & month == "03" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "05" & month == "04" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "12" & month == "04" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "03" & month == "05" & year == "2019"
replace location = "Schlossplatz" if municipality == "stuttgart" & day == "24" & month == "05" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "19" & month == "07" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "09" & month == "08" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "16" & month == "08" & year == "2019"
replace location = "Schlossplatz" if municipality == "stuttgart" & day == "30" & month == "08" & year == "2019"
replace comment = "Klimaquiz" if municipality == "stuttgart" & day == "30" & month == "08" & year == "2019"
replace location = "Kernerplatz" if municipality == "stuttgart" & day == "20" & month == "09" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "18" & month == "10" & year == "2019"
replace location = "Erwin-Schoettle-Platz" if municipality == "stuttgart" & day == "29" & month == "11" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "14" & month == "02" & year == "2020"

replace location = "Marktplatz" if municipality == "ulm" & day == "20" & month == "09" & year == "2019" 
replace location = "Marktplatz" if municipality == "ulm" & day == "29" & month == "11" & year == "2019" 

replace municipality = "Zwickau" if county == "zwickau" & day == "24" & month == "05" & year == "2019"
replace location = "Schumannplatz" if county == "zwickau" & day == "26" & month == "04" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "09" & month == "08" & year == "2019"
replace location = "Hauptmarkt" if county == "zwickau" & day == "09" & month == "08" & year == "2019"
replace comment = "Fahrraddemo" if county == "zwickau" & day == "09" & month == "08" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "30" & month == "08" & year == "2019"
replace location = "Georgenplatz" if county == "zwickau" & day == "30" & month == "08" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "20" & month == "09" & year == "2019"
replace location = "Hauptmarkt" if county == "zwickau" & day == "20" & month == "09" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "29" & month == "11" & year == "2019"
replace location = "Schumannplatz" if county == "zwickau" & day == "29" & month == "11" & year == "2019"


//******* Step 2: Obtaining information about remaining missing locations from social media *******
/* remaining missing locations and addresses in leipzig, stuttgart & zwickau: obtaining information from the respective Instagram
 * and Facebook profiles (https://www.instagram.com/fffleipzig/ & https://www.instagram.com/fridaysforfuturestuttgart/,
 * https://www.facebook.com/pg/fridaysforfuturestuttgart/events/?ref=page_internal, https://www.instagram.com/fridaysforfuture.zwickau/) and other sources 
 * (https://www.l-iz.de/politik/engagement/2019/05/Wenn-Menschen-vor-McDonalds-liegen-Fridays-for-Future-macht-auch-in-den-Ferien-weiter-Video-278158) */
replace location = "Willhelm-Leuschner-Platz" if municipality == "leipzig" & day == "11" & month == "01" & year == "2019"
replace location = "Willy-Brandt-Platz" if municipality == "leipzig" & day == "18" & month == "01" & year == "2019"
replace location = "Anton-Bruckner-Allee" if municipality == "leipzig" & day == "25" & month == "01" & year == "2019"
replace location = "goerdelerring" if municipality == "leipzig" & day == "01" & month == "02" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "08" & month == "02" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "15" & month == "02" & year == "2019"
replace location = "Grimmaische Straße" if municipality == "leipzig" & day == "08" & month == "03" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "19" & month == "04" & year == "2019"
replace location = "Clara-Zetkin-Park" if municipality == "leipzig" & day == "26" & month == "04" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "10" & month == "05" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "17" & month == "05" & year == "2019"
replace location = "Markt" if municipality == "leipzig" & day == "31" & month == "05" & year == "2019"
replace location = "Neues Rathaus" if municipality == "leipzig" & day == "14" & month == "06" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "15" & month == "06" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "21" & month == "06" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "28" & month == "06" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "05" & month == "07" & year == "2019"
replace location = "Willhelm-Leuschner-Platz" if municipality == "leipzig" & day == "12" & month == "07" & year == "2019"
replace location = "Willy-Brandt-Platz" if municipality == "leipzig" & day == "06" & month == "09" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "04" & month == "10" & year == "2019"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "01" & month == "11" & year == "2019"
replace location = "gerberstrasse" if municipality == "leipzig" & day == "08" & month == "11" & year == "2019"
replace location = "neues rathaus" if municipality == "leipzig" & day == "15" & month == "11" & year == "2019"
replace location = "Willy-Brandt-Platz" if municipality == "leipzig" & day == "22" & month == "11" & year == "2019"
replace location = "am hallischen tor" if municipality == "leipzig" & day == "06" & month == "12" & year == "2019"
replace location = "lessingstraße" if municipality == "leipzig" & day == "13" & month == "12" & year == "2019"
replace location = "Willy-Brandt-Platz" if municipality == "leipzig" & day == "20" & month == "12" & year == "2019"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "03" & month == "01" & year == "2020"
replace location = "Richard-Wagner-Straße" if municipality == "leipzig" & day == "11" & month == "01" & year == "2020"
replace location = "Augustusplatz" if municipality == "leipzig" & day == "24" & month == "01" & year == "2020"
replace location = "Richard-Wagner-Platz" if municipality == "leipzig" & day == "06" & month == "03" & year == "2020"

replace location = "Rathaus" if municipality == "stuttgart" & day == "21" & month == "12" & year == "2018"
replace location = "Rathaus" if municipality == "stuttgart" & day == "28" & month == "12" & year == "2018"
replace location = "Rathaus" if municipality == "stuttgart" & day == "04" & month == "01" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "11" & month == "01" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "18" & month == "01" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "25" & month == "01" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "01" & month == "02" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "08" & month == "02" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "01" & month == "03" & year == "2019"
replace location = "rotebühlplatz" if municipality == "stuttgart" & day == "01" & month == "03" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "26" & month == "04" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "10" & month == "05" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "17" & month == "05" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "31" & month == "05" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "07" & month == "06" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "14" & month == "06" & year == "2019"
replace location = "Schlossplatz" if municipality == "stuttgart" & day == "21" & month == "06" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "28" & month == "06" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "05" & month == "07" & year == "2019"
replace location = "rotebühlplatz" if municipality == "stuttgart" & day == "12" & month == "07" & year == "2019"
replace location = "Schlossplatz" if municipality == "stuttgart" & day == "23" & month == "08" & year == "2019"
replace location = "Lautenschlagerstraße" if municipality == "stuttgart" & day == "06" & month == "09" & year == "2019" 
replace location = "Schlossplatz" if municipality == "stuttgart" & day == "13" & month == "09" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "27" & month == "09" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "04" & month == "10" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "11" & month == "10" & year == "2019"
replace location = "Porsche Museum" if municipality == "stuttgart" & day == "25" & month == "10" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "01" & month == "11" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "08" & month == "11" & year == "2019"
replace location = "Rathaus" if municipality == "stuttgart" & day == "08" & month == "11" & year == "2019"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "22" & month == "11" & year == "2019"
replace location = "Königstraße" if municipality == "stuttgart" & day == "13" & month == "12" & year == "2019"
replace location = "Weissacher Straße" if municipality == "stuttgart" & day == "10" & month == "01" & year == "2020"
replace location = "Marktplatz" if municipality == "stuttgart" & day == "24" & month == "01" & year == "2020"
replace location = "Leitzstraße 45" if municipality == "stuttgart" & day == "21" & month == "02" & year == "2020"

replace municipality = "Zwickau" if county == "zwickau" & day == "05" & month == "04" & year == "2019"
replace comment = "Ampelaktion" if county == "zwickau" & day == "05" & month == "04" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "26" & month == "04" & year == "2019"
replace comment = "Ampelaktion" if county == "zwickau" & day == "26" & month == "04" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "14" & month == "06" & year == "2019"
replace location = "Innere Plauensche Straße" if county == "zwickau" & day == "14" & month == "06" & year == "2019"
replace municipality = "zwickau" if county == "zwickau" & day == "23" & month == "08" & year == "2019"
replace location = "Innere Plauensche Straße" if county == "zwickau" & day == "23" & month == "08" & year == "2019"
replace municipality = "zwickau" if county == "zwickau" & day == "06" & month == "09" & year == "2019"
replace location = "Äußere Schneeberger Straße" if county == "zwickau" & day == "06" & month == "09" & year == "2019"
replace comment = "Ampelaktion" if county == "zwickau" & day == "06" & month == "09" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "23" & month == "10" & year == "2019"
replace location = "Hauptmarkt" if county == "zwickau" & day == "23" & month == "10" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "25" & month == "10" & year == "2019"
replace location = "Hauptmarkt" if county == "zwickau" & day == "25" & month == "10" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "15" & month == "11" & year == "2019"
replace location = "Kornmarkt" if county == "zwickau" & day == "15" & month == "11" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "20" & month == "12" & year == "2019"
replace location = "Georgenplatz" if county == "zwickau" & day == "20" & month == "12" & year == "2019"
replace municipality = "Zwickau" if county == "zwickau" & day == "31" & month == "01" & year == "2020"
replace location = "Leipziger Straße" if county == "zwickau" & day == "31" & month == "01" & year == "2020"
replace comment = "Ampelaktion" if county == "zwickau" & day == "31" & month == "01" & year == "2020"
replace municipality = "Zwickau" if county == "zwickau" & day == "13" & month == "03" & year == "2020"
replace location = "Georgenplatz" if county == "zwickau" & day == "13" & month == "03" & year == "2020"