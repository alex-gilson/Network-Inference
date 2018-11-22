#!/usr/local/bin/bash

tr '\n' ';' < w/cascades.csv > w/cascades.csv.temp
sed '$ s/.$//' w/cascades.csv.temp  > w/cascades.csv
rm w/cascades.csv.temp

tr '\n' ';' < w/a_bad.csv > w/a_bad.csv.temp
sed '$ s/.$//' w/a_bad.csv.temp  > w/a_bad.csv
rm w/a_bad.csv.temp

tr '\n' ';' < w/a_potential.csv > w/a_potential.csv.temp
sed '$ s/.$//' w/a_potential.csv.temp  > w/a_potential.csv
rm w/a_potential.csv.temp

tr '\n' ';' < w/S_matrix.csv > w/S_matrix.csv.temp
sed '$ s/.$//' w/S_matrix.csv.temp  > w/S_matrix.csv
rm w/S_matrix.csv.temp