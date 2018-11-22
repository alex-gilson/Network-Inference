#!/usr/local/bin/bash

# Edit the S_matrix
tr '\n' ';' < w/S_matrix.csv > w/S_matrix_temp.csv
sed '$ s/.$//' w/S_matrix_temp.csv > w/S_matrix.csv 
rm w/S_matrix_temp.csv

# Edit the a_bad
tr '\n' ';' < w/a_bad.csv > w/a_bad_temp.csv
sed '$ s/.$//' w/a_bad_temp.csv > w/a_bad.csv 
rm w/a_bad_temp.csv


# Edit the a_potential
tr '\n' ';' < w/a_potential.csv > w/a_potential_temp.csv
sed '$ s/.$//' w/a_potential_temp.csv > w/a_potential.csv 
rm w/a_potential_temp.csv


# Edit the cascades
tr '\n' ';' < w/cascades.csv > w/cascades_temp.csv
sed '$ s/.$//' w/cascades_temp.csv > w/cascades.csv 
rm w/cascades_temp.csv

