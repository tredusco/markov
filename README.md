# Simple Markov Name Generator
It takes a CSV of sample names and generate new names based on the frequencies of the samples.

# Dependencies
It requires Pandas to execute

# Usage
```
usage: markov.py [-h] [-n NUM] [-s SEP] [-c COL] [-t TEMP] FILE

positional arguments:
  FILE                  Sample names file (CSV format)

optional arguments:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     Number of names to generate. DEFAULT: 10
  -s SEP, --sep SEP     Field separator in CSV file. DEFAULT: ;
  -c COL, --col COL     Name of the column to use. DEFAULT: name
  -t TEMP, --temp TEMP  Temperature, integer for randomness of the results (The lower the more random). DEFAULT: 3
  -cc CATEGORY, --category CATEGORY
                        Category to filter data. If not provided, not filtering is done.
  -cn CATNAME, --catname CATNAME
                        Category column name. DEFAULT: category
```  

# Samples

You can use both local or remote file for samples (anything supported by Pandas csv import

## Local executon over a set of Pokemon names (column in CSV is Name)
```
python3 markov.py --n 12 -c Name -s "," -t 2 pokemon.csv
['Wobbullspunk', 'Croundacracticull', 'Skacher', 'Lede', 'Kradamat', 'Corna', 'Shelect', 'Hel', 'Mack', 'Scrad', 'Lartomb', 'Pern']
```
## Remote execution over a set of common English baby names
```
python3 markov.py -n 12 -c name -s "," -t 5 "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
['Dandreas', 'Austine', 'Kelvina', 'Shelle', 'Lamberto', 'Santine', 'Demarie', 'Demarie', 'Normando', 'Esmerald', 'Maximilliams', 'Geralda']
```

## Remote execution filtering by category column
```
python3 markov.py -n 12 -c name -s "," -t 4 -cc girl -cn sex "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
['Aracey', 'Lissetta', 'Destine', 'Mariley', 'Tracelyn', 'Arabelle', 'Carles', 'Guadalyn', 'Danie', 'Karandee', 'Yarita', 'Ceciliana']
```
