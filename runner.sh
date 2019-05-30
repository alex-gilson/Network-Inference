#!/usr/local/bin/bash

simulation_times=(200)
num_nodes=(5)
num_processors=(3)
stimulation_type=abs
diffusion_type=rayleigh
I_var=6
horizon=20
s=2
sparsity=(0.1)
for j in ${simulation_times[*]}
do
	for n in ${num_nodes[*]}
	do
		mkdir -p r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}
		for i in ${num_processors[*]}
		do
			echo "Number of nodes: $num_nodes, Simulation Time: $j, Number of processors: $num_processors, Seed $s:"
			indicesFileName=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/indices_$s.csv
			firingsFileName=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/firings_$s.csv
			networkFileName=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/network_$s.csv
			resultsFileName=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/results_$s.csv
			inferredMatrixFileName=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/inferred_matrix_$s.csv
			fileToTrackProgress=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/progress_tracker_$s.txt

			bash main.sh $s $n $sparsity $j $networkFileName $firingsFileName $indicesFileName $resultsFileName $inferredMatrixFileName $fileToTrackProgress $diffusion_type $horizon $i $stimulation_type

		done
	done
done

# poweroff
