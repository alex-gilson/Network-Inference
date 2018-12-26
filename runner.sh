#!/usr/local/bin/bash

simulation_times=(4000)

for j in ${simulation_times[*]}
do
	mkdir r/for_histogram/network_sim_time_$j
	for i in $(seq 1 $1)
	do
		echo "Simulation Time: $j, Seed $i:"
		bash tester_no_graphs.sh $i 10 0.1 $j r/for_histogram/network_sim_time_$j/network_seed_$i.csv w/firing.csv w/indice.csv r/for_histogram/network_sim_time_$j/results.txt r/for_histogram/network_sim_time_$j/matlab_inferred_matrix_seed_$i.csv r/for_histogram/network_sim_time_$j/progress_tracker_seed_$i.txt rayleigh 20 3
	done
done

