
num_nodes=10
num_processors=(2)
train_test_split=50
dataset=4
diffusion_type=rayleigh
stimulation_type=random_spikes
simulation_times=(10)
horizon=20
seeds=(1)
infer_network=1
sparsity=0.1
cascadeOption=maximum_independence
repeat=0
I_var=4

for n in ${num_nodes[*]}
do
	for j in ${simulation_times[*]}
	do
		for s in ${seeds[*]}
		do
			 mkdir -p r/no_ground_truth/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}
			for i in ${num_processors[*]}
			do
				echo "Dataset: $dataset, Train test split: $train_test_split, Number of processors: $num_processors, Seed $s:"
				folderName=r/no_ground_truth/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/
				indicesFileName="${folderName}indices_$s.csv"
				firingsFileName="${folderName}firings_$s.csv"
				networkFileName="${folderName}network_$s.csv"
				# indicesFileName="/home/alex/Documents/Final-Year-Project/r/network_10_nodes/network_stimulation_random_spikes_stimulation_time_100_4/indices_1.csv"
				# firingsFileName="/home/alex/Documents/Final-Year-Project/r/network_10_nodes/network_stimulation_random_spikes_stimulation_time_100_4/firings_1.csv"
				trainIndicesFileName="${folderName}train_indices_${train_test_split}_$s.csv"
				testIndicesFileName="${folderName}test_indices_${train_test_split}_$s.csv"
				trainFiringsFileName="${folderName}train_firings_${train_test_split}_$s.csv"
				testFiringsFileName="${folderName}test_firings_${train_test_split}_$s.csv"
				resultsFileName="${folderName}results_${train_test_split}_$s.csv"
				inferredNetworkFileName="${folderName}inferred_network_${train_test_split}_$s.csv"
				cascadesFileName="${folderName}cascades_${cascadeOption}_${train_test_split}_$s.csv"
				aBadFileName="${folderName}a_bad_${cascadeOption}_${train_test_split}_$s.csv"
				aPotentialFileName="${folderName}a_potential_${cascadeOption}_${train_test_split}_$s.csv"
				numCascadesFileName="${folderName}num_cascades_${cascadeOption}_${train_test_split}_$s.csv"
				aHatFileName="${folderName}a_hat_${train_test_split}_"
				timeFileName="${folderName}initial_time.pickle"
				numFiringsFileName="${folderName}num_firings_${cascadeOption}_${train_test_split}_$s.csv"

				bash main_real.sh $s $train_test_split $indicesFileName $firingsFileName $networkFileName $trainIndicesFileName $testIndicesFileName $trainFiringsFileName $testFiringsFileName $resultsFileName $inferredNetworkFileName $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $aHatFileName $numFiringsFileName $diffusion_type $num_nodes $sparsity $horizon $j $I_var $cascadeOption

			done
		done
	done
done





