#!/usr/local/bin/bash

simulation_times=(5000)

# for i in ${simulation_times[*]}
# do
# 	echo $i
# 	./tester_no_graphs.sh 1 10 0.1 $i networks.csv firings.csv indices.csv results_simulation_times.csv

for j in ${simulation_times[*]}
do
	mkdir r/for_histogram/network_sim_time_$j
	for i in $(seq 40 $1)
	do
		echo "Simulation Time: $j, Seed $i:"
		./tester_no_graphs.sh $i 10 0.1 $j r/for_histogram/network_sim_time_$j/network_seed_$i.csv w/firing.csv w/indice.csv r/for_histogram/network_sim_time_$j/results.txt r/for_histogram/network_sim_time_$j/matlab_inferred_matrix_seed_$i.csv r/for_histogram/network_sim_time_$j/progress_tracker_seed_$i.txt
	done
done

