#!/usr/local/bin/bash

simulation_times=(4000)
num_nodes=(10)
num_processors=(1)
s=1
for j in ${simulation_times[*]}
do
	for n in ${num_nodes[*]}
	do
		mkdir -p r/network_${n}_nodes/network_sim_time_$j
		for i in ${num_processors[*]}
		do
			echo "Number of nodes: $num_nodes, Simulation Time: $j, Number of processors: $num_processors, Seed $s:"
			bash main.sh 1 $n 0.1 $j r/network_${n}_nodes/network_sim_time_$j/network_seed_$s.csv w/firing.csv w/indice.csv r/network_${n}_nodes/network_sim_time_$j/results.csv r/network_${n}_nodes/network_sim_time_$j/matlab_inferred_matrix_seed_$s.csv r/network_${n}_nodes/network_sim_time_$j/progress_tracker_seed_$s.txt rayleigh 20 $i
		done
	done
done

poweroff
