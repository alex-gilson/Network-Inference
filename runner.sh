
# simulation_times=(1)
# simulation_times=(5000 4500)
# simulation_times=(2000 2500 3000)
simulation_times=(1 2 3 4 5 6 7 8 9 11 12 13 14 16 17 18 19)
num_nodes=(10 20)
num_processors=(2)
stimulation_type=random_spikes
diffusion_type=rayleigh
I_var=4
horizon=20
seeds=(1 2 3 4 5)
# seeds=1
sparsity=(0.1)
infer_network=1
cascadeOption=maximum_independence
repeat=0

for n in ${num_nodes[*]}
do
	for j in ${simulation_times[*]}
	do
		for s in ${seeds[*]}
		do
			mkdir -p r/sim_times/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}
			for i in ${num_processors[*]}
			do
				echo "Number of nodes: $num_nodes, Simulation Time: $j, Number of processors: $num_processors, Seed $s:"
				folderName=r/sim_times/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/
				indicesFileName="${folderName}indices_$s.csv"
				firingsFileName="${folderName}firings_$s.csv"
				networkFileName="${folderName}network_$s.csv"
				resultsFileName="${folderName}results_$s.csv"
				inferredNetworkFileName="${folderName}inferred_network_$s.csv"
				cascadesFileName="${folderName}cascades_${cascadeOption}_$s.csv"
				aBadFileName="${folderName}a_bad_${cascadeOption}_$s.csv"
				aPotentialFileName="${folderName}a_potential_${cascadeOption}_$s.csv"
				numCascadesFileName="${folderName}num_cascades_${cascadeOption}_$s.csv"
				aHatFileName="${folderName}a_hat_"
				timeFileName="${folderName}initial_time.pickle"
				numFiringsFileName="${folderName}num_firings_${cascadeOption}_$s.csv"

				bash main.sh $s $n $sparsity $j $networkFileName $firingsFileName $indicesFileName $resultsFileName $inferredNetworkFileName $diffusion_type $horizon $i $stimulation_type $I_var $infer_network $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $cascadeOption $repeat $aHatFileName $timeFileName $numFiringsFileName

			done
		done
	done
done

# poweroff
