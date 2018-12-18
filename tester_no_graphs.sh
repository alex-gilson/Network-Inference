#!/usr/local/bin/bash

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
# diffusion_type="$11"

seed=1
num_nodes=10
sparsity=0.1
simulation_duration=1000
networkFileName=r/for_histogram/network_sim_time_1000/network_seed_1.csv
firingsFileName=w/firing.csv
indicesFileName=w/indice.csv
resultsFileName=r/for_histogram/network_sim_time_1000/results.txt
matlabNetworkFileName=r/for_histogram/network_sim_time_5000/matlab_inferred_matrix_seed_1.csv 
fileToTrackProgress=r/for_histogram/network_sim_time_5000/progress_tracker_seed_1.txt
diffusion_type=rayleigh
horizon=20
num_processors=3

echo "Seed:$seed,num_nodes:$num_nodes,sparsity:$sparsity,n=$networkFileName,f:$firingsFileName,i:$indicesFileName,r:$resultsFileName,m=$matlabNetworkFileName,fileToTrackProgress:$fileToTrackProgress" >> $resultsFileName

rtime="$( TIMEFORMAT='%lR';time ( python izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName ) 2>&1 1>/dev/null )"

# ./izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName

echo -e "\tDone with simulation, Took Approximately $rtime"
echo -e "\tStarting Matlab"

# rtime="$( TIMEFORMAT='%lR';time ( matlab -nodesktop -nosplash -nojvm -r "f='$firingsFileName';t='$indicesFileName';n='$networkFileName';N=$num_nodes;horizon=20;sparsity=$sparsity;diffusion_type='exp';r='$resultsFileName';m='$matlabNetworkFileName';fileToTrackProgress='$fileToTrackProgress';brianIzhikevichSolver;exit" ) 2>&1)"

# echo -e "\tDone with Matlab Took Approximately $rtime"

matlab -nodesktop -nosplash -nojvm -r "f=$firingsFileName;t=$indicesFileName;n=$networkFileName;N=$num_nodes;horizon=$horizon;sparsity=$sparsity;type_diffusion=$diffusion_type;r=$resultsFileName;m=$matlabNetworkFileName;fileToTrackProgress=$fileToTrackProgress;generate_cascades.m;exit;"

python parallelize_cvx.py $num_processors $num_nodes $horizon $diffusion_type $fileToTrackProgress

#matlab -nodesktop -nosplash -nojvm -r "n='$networkFileName';sparsity=$sparsity;diffusion_type=$diffusion_type;r='$resultsFileName';m='$matlabNetworkFileName';fileToTrackProgress='$fileToTrackProgress';process_results.m;exit"

echo >> $resultsFileName
