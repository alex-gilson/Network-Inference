#!/usr/local/bin/bash

simulation_times=(4000)
num_nodes=(10)

for j in ${simulation_times[*]}
do
	for n in ${num_nodes[*]}
	do
		mkdir r/network_$n/network_sim_time_$j
		for i in $(seq 4 $1)
		do
			echo "Simulation Time: $j, Seed $i:"
			bash main.sh 1 $n 0.1 $j r/for_histogram/network_sim_time_$j/network_seed_$i.csv w/firing.csv w/indice.csv r/for_histogram/network_sim_time_$j/results.csv r/for_histogram/network_sim_time_$j/matlab_inferred_matrix_seed_$i.csv r/for_histogram/network_sim_time_$j/progress_tracker_seed_$i.txt rayleigh 20 $i
		done
	done
done

# poweroff
