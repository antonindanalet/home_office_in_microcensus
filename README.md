# home_office_in_microcensus

This codes estimates a (very simple) binary logit from the data of the Mobility and Transport Microcensus 2015 explaining the "choice" of making - at least from time to time - home office. The outputs are available in the following HTML files:
- without gender and without error in 
- with gender and with optimization error in 

## Getting Started

If you want to reproduce the error, you need this code and the data of the Mobility and Transport Microcensus 2015.

### Prerequisites to run the code

To run the code itself, you need python 3 and PandasBiogeme. Here is my configuration:

Cython 0.29.14, 

Fiona 1.8.16

GDAL 3.1.2 

Rtree 0.9.4

Shapely 1.7.1

Unidecode 1.1.1

attrs 20.2.0

biogeme 3.2.0b0 installed from wheel for Windows

certifi 2020.4.5.2

chardet 3.0.4

click 7.1.2

click-plugins 1.1.1

cligj 0.5.0

cycler 0.10.0	

cythonarrays 1.3.7

cythoninstallhelpers 1.1.3

geopandas 0.8.1

idna 2.9

kiwisolver 1.1.0

matplotlib 3.1.1

munch 2.5.0

numpy 1.18.2

pandas 1.0.1

pip 20.2.2

pyparsing 2.4.2

pyproj 2.6.1.post1

pyreadstat 0.2.9

python-dateutil 2.8.1

pytz 2019.3

requests 2.23.0

savReaderWriter 3.4.2

scipy 1.4.1

seaborn 0.9.0

setuptools 49.2.0

six 1.14.0

urllib3 1.25.9

xarray 0.16.0

xlrd 1.2.0

### Data prerequisites

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2005, 2010 & 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">form in German</a>, <a href="https://www.are.admin.ch/are/fr/home/transports-et-infrastructures/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/trasporti-e-infrastrutture/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the files haushalte.csv and zielpersonen.csv of the Mobility and Transport Microcensus 2015 that you receive from the Federal Statistical Office in the folders data/input/mtmc/2015/. Then run run_home_office_in_microcensus.py.

DO NOT commit or share in any way the CSV files haushalte.csv and zielpersonen.csv! These are personal data.

## Contact

Please don't hesitate to contact me if you have questions or comments about this code: antonin.danalet@are.admin.ch
