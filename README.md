# Home-based telecommuting in Switzerland, 2015-2050: simple binary logit

This codes estimates a (very simple) binary logit from the data of the Mobility and Transport Microcensus 2015 explaining the "choice" of making - at least from time to time - home office. The outputs are available in an HTML file.

## Getting Started

If you want to estimate and validate the model, you need this code and the data of the Mobility and Transport Microcensus 2015.

### Prerequisites to run the code

To run the code itself, you need python 3, pandas, Geopandas, xlrd, PandasBiogeme and pygeos.

### Data prerequisites

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">form in German</a>, <a href="https://www.are.admin.ch/are/fr/home/transports-et-infrastructures/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/trasporti-e-infrastrutture/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the files haushalte.csv and zielpersonen.csv of the Mobility and Transport Microcensus 2015 that you receive from the Federal Statistical Office in the folders <a href="https://github.com/antonindanalet/home_office_in_microcensus/tree/master/data/input/mtmc/2015">data/input/mtmc/2015/</a>. Then run run_home_office_in_microcensus.py.

DO NOT commit or share in any way the CSV files haushalte.csv and zielpersonen.csv! These are personal data.

## Contact

Please don't hesitate to contact me if you have questions or comments about this code: antonin.danalet@are.admin.ch
