# Home-based telecommuting in Switzerland, 2015-2050

This codes estimates a binary logit from the data of the Mobility and Transport Microcensus explaining the "choice" of making - at least from time to time - home office. The outputs are available in an HTML file.
The results are described in two conference papers:
- "<a href="http://strc.ch/2021/Danalet_EtAl_2.pdf">Working from home in Switzerland, 2015-2050</a>", published for the <a href="http://strc.ch/2021.php">21th</a> <a href="http://strc.ch/">Swiss Transport Research Conference (STRC)</a>, published in September 2021 using the data of the Mobility and Transport Microcensus 2015. The slides are available <a href="https://www.slideshare.net/AntoninDanalet/working-from-home-in-switzerland-20152050">here</a>.
- "<a href="https://github.com/antonindanalet/home_office_in_microcensus/blob/master/WorkingFromHome2050_ICMC.pdf">Working from home: Forecasting 2050</a>", <a href="https://easychair.org/smart-program/ICMC2022/2022-05-25.html#talk:193097">presented at the 7th International Choice Modelling Conference (ICMC) that took place in Mai 2022</a> using the data of the Mobility and Transport Microcensus 2015 and 2020. The slides are available <a href="https://github.com/antonindanalet/home_office_in_microcensus/blob/master/WorkingFromHome_ICMC_slides.pdf">here</a>.

## Getting Started

If you want to estimate and validate the model, you need this code and the data of the Mobility and Transport Microcensus 2015 & 2020.

### Prerequisites to run the code

To run the code itself, you need python 3, pandas, Geopandas, xlrd, PandasBiogeme and pygeos.

### Data prerequisites

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015 & 2020, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">form in German</a>, <a href="https://www.are.admin.ch/are/fr/home/mobilite/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/mobilita/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the files haushalte.csv and zielpersonen.csv of the Mobility and Transport Microcensus 2015 that you receive from the Federal Statistical Office in the folders <a href="https://github.com/antonindanalet/home_office_in_microcensus/tree/master/data/input/mtmc/2015">data/input/mtmc/2015/</a>. Then run <a href="https://github.com/antonindanalet/home_office_in_microcensus/blob/master/src/run_home_office_in_microcensus.py">run_home_office_in_microcensus.py</a>.

DO NOT commit or share in any way the CSV files haushalte.csv and zielpersonen.csv! These are personal data.
