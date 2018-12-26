# !/usr/local/bin/bash

# seed="$1"
# num_nodes="$2"
# sparsity="$3"
# simulation_duration="$4"
# networkFileName="$5"
# firingsFileName="$6"
# indicesFileName="$7"
# resultsFileName="$8"
# matlabNetworkFileName="$9"
# fileToTrackProgress="${10}"
# diffusion_type="${11}"
# horizon="${12}"
# num_processors="${13}"
#
seed=1
num_nodes=10
sparsity=0.1
simulation_duration=4000
networkFileName=r/for_histogram/network_sim_time_4000/network_seed_1.csv
firingsFileName=w/firing.csv
indicesFileName=w/indice.csv
resultsFileName=r/for_histogram/network_sim_time_4000/results.txt
matlabNetworkFileName=r/for_histogram/network_sim_time_4000/matlab_inferred_matrix_seed_1.csv 
fileToTrackProgress=r/for_histogram/network_sim_time_4000/progress_tracker_seed_1.txt
diffusion_type=rayleigh
horizon=100
num_processors=3

# Activate virtual environment
. py27env/bin/activate

echo "Seed:$seed,num_nodes:$num_nodes,sparsity:$sparsity,n=$networkFileName,f:$firingsFileName,i:$indicesFileName,r:$resultsFileName,m=$matlabNetworkFileName,fileToTrackProgress:$fileToTrackProgress,horizon=$horizon" >> $resultsFileName

python izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName

echo -e "\tDone with simulation"
echo -e "\tStarting Matlab"

matlab -nodesktop -nosplash -nojvm -r "generate_cascades('$firingsFileName','$indicesFileName','$networkFileName',$num_nodes,$horizon,$sparsity,'$diffusion_type','$resultsFileName','$matlabNetworkFileName','$fileToTrackProgress');exit;"

echo -e "\tDone with Matlab" 

# echo -e "\tDone with Matlab Took Approximately $rtime"

python parallelize_cvx.py $num_processors $num_nodes $horizon $diffusion_type $fileToTrackProgress

matlab -nodesktop -nosplash -nojvm -r "process_results($sparsity,'$resultsFileName','$diffusion_type','$matlabNetworkFileName','$fileToTrackProgress', '$matlabNetworkFileName');exit;"

echo >> $resultsFileName
echo "Results are available at '$resultsFileName'"



