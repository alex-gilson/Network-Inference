
num_nodes=10
num_processors=(2)
train_test_split=70
dataset=4
diffusion_type=rayleigh
stimulation_type=random_spikes
simulation_times=(15)
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
			for i in ${num_processors[*]}
			do
				echo "Dataset: $dataset, Train test split: $train_test_split, Number of processors: $num_processors, Seed $s:"
				if (($dataset == 0))
				then
					folderName=r/no_ground_truth/network_${n}_nodes/network_stimulation_${stimulation_type}_stimulation_time_${j}_${I_var}/
				else
					folderName=r/no_ground_truth/CRCNS_${dataset}/train_test_split_${train_test_split}/
				fi
				mkdir -p $folderName
				indicesFileName="${folderName}indices_$s.csv"
				firingsFileName="${folderName}firings_$s.csv"
				networkFileName="${folderName}network_$s.csv"
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

				bash main_real.sh $s $train_test_split $indicesFileName $firingsFileName $networkFileName $trainIndicesFileName $testIndicesFileName $trainFiringsFileName $testFiringsFileName $resultsFileName $inferredNetworkFileName $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $aHatFileName $numFiringsFileName $diffusion_type $num_nodes $sparsity $horizon $j $I_var $cascadeOption $dataset $num_processors

			done
		done
	done
done





