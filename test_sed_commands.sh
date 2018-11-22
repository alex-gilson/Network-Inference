#!/usr/local/bin/bash

# simulation_times=(100 150 200 250 300 350 400 450 500 1000 2000 3000 4000 5000)

for dir in ./r/for_histogram/*/
do
	(echo $dir && cd "$dir" && sed '/^Seed/d' results.txt > results.txt.tmp && sed 's/:/,/g' results.txt.tmp > results.txt && rm results.txt.tmp && ../../../collate_results.py results.txt ../collated_sim_time_100.csv)
done