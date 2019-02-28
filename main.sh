# !/usr/local/bin/bash

seed="$1"
num_nodes="$2"
sparsity="$3"
simulation_duration="$4"
networkFileName="$5"
firingsFileName="$6"
indicesFileName="$7"
resultsFileName="$8"
matlabNetworkFileName="$9"
fileToTrackProgress="${10}"
diffusion_type="${11}"
horizon="${12}"
num_processors="${13}"

# seed=1
# num_nodes=10
# sparsity=0.1
# simulation_duration=4000
# networkFileName=r/for_histogram/network_sim_time_4000/network_seed_1.csv
# firingsFileName=w/firing.csv
# indicesFileName=w/indice.csv
# resultsFileName=r/for_histogram/network_sim_time_4000/results.csv
# matlabNetworkFileName=r/for_histogram/network_sim_time_4000/matlab_inferred_matrix_seed_1.csv 
# fileToTrackProgress=r/for_histogram/network_sim_time_4000/progress_tracker_seed_1.txt
# diffusion_type=rayleigh
# horizon=20
# num_processors=1
#
mkdir temporary
# Activate virtual environment
. py27env/bin/activate

# if [ ! -f $networkFileName ] || [ ! -f $firingsFileName ] || [ ! -f $indicesFileName ]; then
	python izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName


echo -e "Found Brian Simulator files"

echo -e "\tGenerating cascades..."

matlab -nodesktop -nosplash -nojvm -r "generate_cascades('$firingsFileName','$indicesFileName','$networkFileName',$num_nodes,$horizon,$sparsity,'$diffusion_type','$resultsFileName','$matlabNetworkFileName','$fileToTrackProgress');exit;"

# Get current time and store it into a pickle file
python initial_time.py

echo -e "\tComputing Netrate..." 

python parallelize_cvx.py $num_processors $num_nodes $horizon $diffusion_type $fileToTrackProgress

# echo -e "Processing results..."
#
# matlab -nodesktop -nosplash -nojvm -r "process_results($sparsity,'$resultsFileName','$diffusion_type','$matlabNetworkFileName','$fileToTrackProgress');exit;"
#
# echo -e "Calculating elapsed time..."
#
# python final_time.py $resultsFileName $seed $num_nodes $sparsity $networkFileName $firingsFileName $indicesFileName $matlabNetworkFileName $fileToTrackProgress $horizon $num_processors
#
# rm initial_time.pickle
# rm temporary/*
#
# echo "Results are available at '$resultsFileName'"
#

