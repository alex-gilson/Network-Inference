#!/usr/local/bin/bash

simulation_times=(100)
num_nodes=(7)
num_processors=(3)
stimulation_type=random_spikes
diffusion_type=rayleigh
I_var=4
horizon=20
s=1
sparsity=(0.1)
infer_network=1
cascadeOption=maximum_cascades
repeat=0

for j in ${simulation_times[*]}
do
	for n in ${num_nodes[*]}
	do
		mkdir -p r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}
		for i in ${num_processors[*]}
		do
			echo "Number of nodes: $num_nodes, Simulation Time: $j, Number of processors: $num_processors, Seed $s:"
			folderName=r/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/
			indicesFileName="${folderName}indices_$s.csv"
			firingsFileName="${folderName}firings_$s.csv"
			networkFileName="${folderName}network_$s.csv"
			resultsFileName="${folderName}results_$s.csv"
			inferredNetworkFileName="${folderName}inferred_network_$s.csv"
			cascadesFileName="${folderName}cascades_${cascadeOption}_$s.csv"
			aBadFileName="${folderName}a_bad_${cascadeOption}_$s.csv"
			aPotentialFileName="${folderName}a_potential_${cascadeOption}_$s.csv"
			numCascadesFileName="${folderName}num_cascades_${cascadeOption}_$s.csv"

			bash main.sh $s $n $sparsity $j $networkFileName $firingsFileName $indicesFileName $resultsFileName $inferredNetworkFileName $diffusion_type $horizon $i $stimulation_type $I_var $infer_network $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $cascadeOption $repeat

		done
	done
done

# poweroff
